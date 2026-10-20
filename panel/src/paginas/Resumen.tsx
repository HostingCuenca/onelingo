import { useEffect, useState } from 'react'
import { api, IDIOMAS, minutos, nivelCorto, num, PLANES, PLATAFORMAS, SKILLS, usd } from '../api'
import { BarrasH, LineasDias } from '../Graficos'

const OTRAS_IA: Record<string, string> = {
  transcripcion: 'Transcripciones de voz', revision_escritura: 'Revisiones de escritura', diagnostico_pregunta: 'Preguntas de ubicación generadas', diagnostico_escritura: 'Evaluaciones de escritura (ubicación)',
}
const pct = (a: number, b: number) => (b ? `${Math.round((a / b) * 100)} %` : '—')

function Kpi({ v, l, nota }: { v: React.ReactNode; l: string; nota?: string }) {
  return <div className="kpi"><div className="v">{v}</div><div className="l">{l}</div>{nota && <div className="nota">{nota}</div>}</div>
}

function Reparto({ titulo, filas, nombres, total }: { titulo: string; filas: { valor: string; usuarios: number }[]; nombres: Record<string, string>; total: number }) {
  return (
    <div className="tarjeta"><h2>{titulo}</h2>
      <BarrasH filas={filas.map((f) => ({ etiqueta: nombres[f.valor] ?? f.valor, valor: f.usuarios, nota: pct(f.usuarios, total) }))} max={total} />
      {filas.length === 0 && <p className="muted">Sin datos.</p>}
    </div>
  )
}

function ClaseFila({ c }: { c: any }) {
  return <tr><td><b>{c.titulo || c.unidad}</b><br /><span className="muted mono">{c.unidad}</span></td><td>{IDIOMAS[c.idioma] ?? c.idioma ?? '—'} · {nivelCorto(c.nivel)}</td><td className="num"><b>{c.alumnos}</b></td></tr>
}

export default function Resumen() {
  const [d, setD] = useState<any>(null)
  const [ia, setIa] = useState<any>(null)
  const [err, setErr] = useState('')
  const cargar = () => { setErr(''); api('/admin/resumen').then(setD).catch((e) => setErr(e.message)) }
  useEffect(() => { cargar(); api('/admin/estado-ia').then(setIa).catch(() => {}) }, [])
  if (err) return <p className="err">{err} <button className="sec" onClick={cargar}>Reintentar</button></p>
  if (!d) return <p className="muted">Cargando…</p>
  const u = d.usuarios, total = u.total
  const base = d.embudo[0]?.usuarios ?? 0
  return (
    <>
      <div className="cab"><h1>Resumen</h1><span className="muted">Hoy {d.hoy} · hora de Ecuador <button className="sec chico" onClick={cargar}>Actualizar</button></span></div>

      <h3 className="seccion">Alumnos</h3>
      <div className="kpis">
        <Kpi v={num(total)} l="Registrados" nota={u.demo ? `${u.demo} sin contraseña (demo)` : undefined} />
        <Kpi v={u.nuevos_hoy} l="Nuevos hoy" nota={`${u.nuevos7d} en 7 días · ${u.nuevos30d} en 30`} />
        <Kpi v={u.dau} l="Activos hoy" />
        <Kpi v={u.wau} l="Activos 7 días" nota={`${pct(u.wau, total)} del total`} />
        <Kpi v={u.mau} l="Activos 30 días" nota={`${pct(u.mau, total)} del total`} />
        <Kpi v={u.con_plan} l="Con plan de pago" nota={`${u.en_prueba} en prueba · ${u.prueba_agotada} agotaron la prueba`} />
      </div>

      <div className="tarjeta"><h2>Registros y alumnos activos por día (30 días)</h2>
        <LineasDias datos={d.porDia} series={[{ nombre: 'Activos', clave: 'activos', color: 'var(--morado)' }, { nombre: 'Registros', clave: 'registros', color: 'var(--naranja)' }]} />
      </div>

      <div className="grid2">
        <div className="tarjeta"><h2>Embudo</h2>
          <BarrasH max={base} filas={d.embudo.map((e: any, i: number) => ({ etiqueta: e.paso, valor: e.usuarios, nota: i === 0 ? '' : pct(e.usuarios, base) }))} />
          <p className="muted pie-nota">Porcentaje sobre los registrados. «Volvieron otro día»: tuvieron actividad algún día posterior al de su registro.</p>
        </div>
        <div className="tarjeta"><h2>Retención</h2>
          <table><thead><tr><th>Volvieron…</th><th className="num">Alumnos</th><th className="num">%</th></tr></thead><tbody>
            {d.retencion.map((r: any) => <tr key={r.dias}><td>{r.dias === 1 ? 'al día siguiente o después (D1)' : `a los ${r.dias} días o después (D${r.dias})`}</td><td className="num">{r.retenidos} de {r.base}</td><td className="num"><b>{r.pct === null ? '—' : `${r.pct} %`}</b></td></tr>)}
          </tbody></table>
          <p className="muted pie-nota">Solo cuenta a quienes se registraron hace al menos esos días. «—» = aún no hay alumnos con esa antigüedad.</p>
        </div>
      </div>

      <div className="grid4">
        <Reparto titulo="Plataforma" filas={d.plataformas} nombres={PLATAFORMAS} total={total} />
        <Reparto titulo="Idioma que aprenden" filas={d.idiomasMeta} nombres={IDIOMAS} total={total} />
        <Reparto titulo="Idioma nativo" filas={d.idiomasNativos} nombres={IDIOMAS} total={total} />
        <Reparto titulo="Plan" filas={d.planes} nombres={{ ...PLANES, prueba: 'Prueba gratuita' }} total={total} />
      </div>

      <h3 className="seccion">Clases</h3>
      <div className="kpis">
        <Kpi v={num(d.clases.total)} l="Clases completadas" nota={d.clases.legado ? `${d.clases.legado} del temario antiguo` : undefined} />
        <Kpi v={d.clases.alumnos} l="Alumnos con alguna clase" nota={`${pct(d.clases.alumnos, total)} de los registrados`} />
        <Kpi v={minutos(d.estudio.segundos)} l="Tiempo de estudio" nota={`${num(d.estudio.xp)} XP en total`} />
      </div>
      <div className="tarjeta"><h2>Clases y conversaciones por día (30 días)</h2>
        <LineasDias datos={d.porDia} series={[{ nombre: 'Clases completadas', clave: 'clases', color: 'var(--verde)' }, { nombre: 'Turnos con el tutor IA', clave: 'conversaciones', color: 'var(--azul)' }]} />
      </div>
      <div className="tarjeta"><h2>Clases completadas por idioma y nivel</h2>
        <div className="desliza"><table className="matriz"><thead><tr><th>Idioma</th>{['F0', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10'].map((n) => <th key={n} className="num">{n}</th>)}<th className="num">Total</th></tr></thead>
          <tbody>{d.clases.tabla.map((f: any) => { const max = Math.max(1, ...f.niveles); return (
            <tr key={f.idioma}><td><b>{IDIOMAS[f.idioma] ?? f.idioma}</b></td>
              {f.niveles.map((v: number, i: number) => <td key={i} className="num" style={{ background: v ? `rgba(69,25,187,${0.08 + (v / max) * 0.3})` : undefined }} title={f.publicadas?.[i] ? `${v} clases completadas · ${f.publicadas[i]} clases publicadas en el nivel` : `${v} clases completadas`}>{v || ''}</td>)}
              <td className="num"><b>{f.total}</b></td></tr>) })}</tbody></table></div>
        {d.clases.tabla.length === 0 && <p className="muted">Todavía nadie ha completado una clase.</p>}
        <p className="muted pie-nota">Una clase cuenta cuando el alumno aprueba su evaluación. F0 = Fundamentos. Las lecciones del temario antiguo se asignan al idioma que el alumno estudia ahora.</p>
      </div>
      <div className="grid2">
        <div className="tarjeta"><h2>Clases más completadas</h2>
          <table><thead><tr><th>Clase</th><th>Idioma · nivel</th><th className="num">Alumnos</th></tr></thead><tbody>{d.clases.masHechas.map((c: any) => <ClaseFila key={c.unidad} c={c} />)}</tbody></table>
          {d.clases.masHechas.length === 0 && <p className="muted">Sin datos todavía.</p>}
        </div>
        <div className="tarjeta"><h2>Dónde más se abandona</h2>
          <table><thead><tr><th>Clase</th><th>Idioma · nivel</th><th className="num">Alumnos</th></tr></thead><tbody>{d.clases.abandonos.map((c: any) => <ClaseFila key={c.unidad} c={c} />)}</tbody></table>
          {d.clases.abandonos.length === 0 && <p className="muted">Nadie ha dejado una clase a medias.</p>}
          <p className="muted pie-nota">Clases abiertas hace más de {d.clases.diasAbandono} días y nunca aprobadas.{d.clases.suspensos.length > 0 && <> Evaluaciones suspendidas sin aprobar: {d.clases.suspensos.slice(0, 5).map((c: any) => `${c.titulo || c.unidad} (${c.alumnos})`).join(' · ')}.</>}</p>
        </div>
      </div>

      <div className="grid2">
        <div className="tarjeta"><h2>Prueba de ubicación</h2>
          <table><thead><tr><th>Idioma</th><th className="num">Pruebas</th><th className="num">Alumnos</th><th className="num">Nivel medio</th></tr></thead>
            <tbody>{d.ubicacion.map((r: any) => <tr key={r.idioma}><td>{IDIOMAS[r.idioma] ?? r.idioma}</td><td className="num">{r.pruebas}</td><td className="num">{r.alumnos}</td><td className="num">{r.nivel_medio ?? '—'}</td></tr>)}</tbody></table>
          {d.ubicacion.length === 0 && <p className="muted">Sin pruebas registradas.</p>}
        </div>
        <div className="tarjeta"><h2>Errores más frecuentes por habilidad</h2>
          {d.errores.map((e: any) => <div key={e.skill} className="bloque-err"><div><b>{SKILLS[e.skill] ?? e.skill}</b> <span className="muted">· {e.total} errores de {e.alumnos} alumnos · {e.pendientes} sin practicar</span></div>
            <div className="muted">{e.frecuentes.map((f: any) => `«${f.correccion}» (${f.n})`).join(' · ')}</div></div>)}
          {d.errores.length === 0 && <p className="muted">Sin errores registrados.</p>}
        </div>
      </div>

      <h3 className="seccion">IA y voz</h3>
      <div className="kpis">
        <Kpi v={num(d.ia.conversaciones)} l="Turnos con el tutor IA" />
        <Kpi v={num(d.ia.entrada)} l="Tokens de entrada" />
        <Kpi v={num(d.ia.salida)} l="Tokens de salida" />
        <Kpi v={usd(d.ia.coste)} l="Coste IA estimado" nota={`${usd(d.ia.coste30)} en 30 días`} />
        <Kpi v={num(d.voz.caracteres)} l="Caracteres de voz" nota={`${num(d.voz.audios)} audios · ${num(d.voz.caracteres30)} car. en 30 días`} />
        <Kpi v={usd(d.voz.coste)} l="Coste de voz estimado" nota={`${usd(d.voz.coste30)} en 30 días`} />
      </div>
      <div className="grid2">
        <div className="tarjeta"><h2>Tutor IA por modelo</h2>
          <div className="desliza"><table><thead><tr><th>Modelo</th><th className="num">Turnos</th><th className="num">Entrada</th><th className="num">Salida</th><th className="num">Coste</th></tr></thead>
            <tbody>{d.ia.modelos.map((m: any) => <tr key={m.modelo}><td className="mono">{m.modelo || '—'}<br /><span className="muted">${m.tarifa.entrada} / ${m.tarifa.salida} por millón</span></td><td className="num">{num(m.conversaciones)}</td><td className="num">{num(m.entrada)}</td><td className="num">{num(m.salida)}</td><td className="num"><b>{usd(m.coste)}</b></td></tr>)}</tbody></table></div>
          {d.ia.modelos.length === 0 && <p className="muted">Sin conversaciones todavía.</p>}
          <h2 style={{ marginTop: 14 }}>Por idioma</h2>
          <BarrasH filas={d.ia.porIdioma.map((r: any) => ({ etiqueta: IDIOMAS[r.idioma] ?? r.idioma, valor: r.conversaciones, nota: `· ${r.alumnos} alumnos` }))} />
          {d.ia.otras.length > 0 && <><h2 style={{ marginTop: 14 }}>Otras llamadas a IA (sin tokens registrados)</h2>
            <table><tbody>{d.ia.otras.map((o: any) => <tr key={o.tipo}><td>{OTRAS_IA[o.tipo] ?? o.tipo}</td><td className="num"><b>{o.total}</b> <span className="muted">({o.ultimos30} en 30 días)</span></td></tr>)}</tbody></table></>}
          <p className="muted pie-nota">Coste estimado con las tarifas de backend/src/lib/analitica.ts; revísalas contra la factura del proveedor.</p>
        </div>
        <div className="tarjeta"><h2>Audios generados por idioma</h2>
          <div className="desliza"><table><thead><tr><th>Idioma</th><th className="num">Audios</th><th className="num">Caracteres</th><th className="num">Reproducciones</th><th className="num">Coste</th></tr></thead>
            <tbody>{d.voz.porIdioma.map((a: any) => <tr key={a.idioma}><td>{IDIOMAS[a.idioma] ?? a.idioma}</td><td className="num">{num(a.audios)}</td><td className="num">{num(a.caracteres)}</td><td className="num">{num(a.usos)}</td><td className="num"><b>{usd(a.coste)}</b></td></tr>)}</tbody></table></div>
          {d.voz.porIdioma.length === 0 && <p className="muted">Todavía no hay audios.</p>}
          <p className="muted pie-nota">Cada frase se sintetiza una vez y se reutiliza; los aciertos de caché no gastan cuota. Estimación: {usd(d.voz.usdPorMilCaracteres)} por cada 1.000 caracteres.</p>
          {ia?.servicios && <><h2 style={{ marginTop: 14 }}>Servicios</h2>
            <div className="desliza"><table><tbody>{Object.entries(ia.servicios).map(([k, v]: any) => <tr key={k}><td><b>{k === 'openai' ? 'OpenAI' : k === 'gemini' ? 'Google Gemini' : 'ElevenLabs'}</b><br /><span className="muted">{v.uso}</span></td><td className="mono">{v.modelo}</td><td className="num"><span className={`pill ${v.activo ? 'ok' : 'mal'}`}>{v.activo ? 'Conectado' : 'Sin clave'}</span></td></tr>)}</tbody></table></div></>}
        </div>
      </div>
      {d.examenes.total > 0 && <div className="tarjeta"><h2>Exámenes de nivel (temario antiguo)</h2><p>{d.examenes.total} presentados · {d.examenes.aprobados} aprobados · nota media {d.examenes.media ?? '—'} %</p></div>}
    </>
  )
}
