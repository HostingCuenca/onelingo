import { useEffect, useState } from 'react'
import { api, fecha, IDIOMAS, num } from '../api'
import ErrorCarga from '../ErrorCarga'
import { CRITERIOS, claseNota, lineaTecnica, nombreTutor, type Informe } from './InformesLlamada'

type PorTutor = { tutorId: string; llamadas: number; evaluadas: number; nota: number | null; frasesRespaldo: number; frasesTutor: number; turnosVivo: number; turnosPulsar: number; cortesVivo: number } & Record<string, number | null>
type Datos = {
  porTutor: PorTutor[]
  problemas: { criterio: string; veces: number; ejemplos: string[] }[]
  recientes: (Pick<Informe, 'id' | 'idioma' | 'nivel' | 'tutorId' | 'explica' | 'turnos' | 'nota' | 'creadoEn' | 'tecnico'> & { usuarioId: string; nombre: string; apellido: string; recomendacion: string | null })[]
}
const pct = (a: number, b: number) => b ? `${Math.round(a / b * 100)} %` : '—'

/** Calidad de las videollamadas: cómo habla y enseña cada tutor según los informes de llamadas reales. */
export default function CalidadLlamadas({ abrirAlumno }: { abrirAlumno: (id: string) => void }) {
  const [dias, setDias] = useState(30); const [d, setD] = useState<Datos | null>(null); const [err, setErr] = useState('')
  const cargar = () => api<Datos>(`/admin/informes-llamada?dias=${dias}`).then((r) => { setD(r); setErr('') }).catch((x) => setErr(x.message))
  useEffect(() => { cargar() }, [dias]) // eslint-disable-line react-hooks/exhaustive-deps
  if (err) return <ErrorCarga msg={err} reintentar={() => { setErr(''); cargar() }} />
  const total = d?.porTutor.reduce((a, t) => ({ ll: a.ll + t.llamadas, r: a.r + t.frasesRespaldo, f: a.f + t.frasesTutor, v: a.v + t.turnosVivo, p: a.p + t.turnosPulsar, c: a.c + t.cortesVivo }), { ll: 0, r: 0, f: 0, v: 0, p: 0, c: 0 })
  const evaluadas = d?.porTutor.filter((t) => t.nota != null) ?? []
  const notaMedia = evaluadas.length ? Math.round(evaluadas.reduce((a, t) => a + (t.nota ?? 0) * t.evaluadas, 0) / Math.max(1, evaluadas.reduce((a, t) => a + t.evaluadas, 0)) * 10) / 10 : null
  return (
    <>
      <div className="cab"><h1>Calidad de llamadas</h1>
        <select value={dias} onChange={(e) => setDias(Number(e.target.value))} aria-label="Periodo"><option value={7}>7 días</option><option value={30}>30 días</option><option value={90}>90 días</option></select>
      </div>
      <p className="muted pie-nota" style={{ margin: '-8px 0 16px' }}>Cada videollamada que termina deja un informe: un revisor de IA puntúa al tutor de 1 a 5 en seis criterios, con citas de lo que dijo, y la página guarda los datos técnicos. Abre un alumno para ver sus informes completos.</p>
      {d && total && <div className="kpis">
        <div className="kpi"><div className="v">{num(total.ll)}</div><div className="l">Llamadas</div></div>
        <div className="kpi"><div className="v">{notaMedia ?? '—'}</div><div className="l">Nota media del tutor</div><div className="nota">de 1 a 10</div></div>
        <div className="kpi"><div className="v">{pct(total.v, total.v + total.p)}</div><div className="l">Turnos en vivo</div><div className="nota">{num(total.c)} cortes de la escucha</div></div>
        <div className="kpi"><div className="v">{pct(total.r, total.f)}</div><div className="l">Voz de respaldo</div><div className="nota">ElevenLabs sin cuota o caído</div></div>
      </div>}
      <div className="tarjeta"><h2>Por tutor</h2>
        {!d ? <p className="muted">Cargando…</p> : d.porTutor.length === 0 ? <p className="muted">Todavía no hay informes en este periodo.</p> :
          <div className="desliza"><table>
            <thead><tr><th>Tutor</th><th className="num">Llamadas</th><th className="num">Nota</th>{Object.values(CRITERIOS).map((c) => <th key={c} className="num">{c}</th>)}<th className="num">En vivo</th><th className="num">Respaldo</th></tr></thead>
            <tbody>{d.porTutor.map((t) => <tr key={t.tutorId}>
              <td><b>{nombreTutor(t.tutorId)}</b></td><td className="num">{num(t.llamadas)}</td>
              <td className="num">{t.nota != null ? <span className={`pill ${claseNota(t.nota)}`}>{t.nota}</span> : '—'}</td>
              {Object.keys(CRITERIOS).map((c) => <td key={c} className="num">{t[c] ?? '—'}</td>)}
              <td className="num">{pct(t.turnosVivo, t.turnosVivo + t.turnosPulsar)}</td><td className="num">{pct(t.frasesRespaldo, t.frasesTutor)}</td>
            </tr>)}</tbody>
          </table></div>}
      </div>
      <div className="grid2">
        <div className="tarjeta"><h2>Problemas más repetidos</h2>
          {d?.problemas.length === 0 && <p className="muted">Sin problemas señalados.</p>}
          {d?.problemas.map((p) => <div key={p.criterio} className="bloque-err"><p style={{ margin: 0 }}><b>{CRITERIOS[p.criterio] ?? p.criterio}</b> <span className="muted">· {num(p.veces)} veces</span></p>
            <ul style={{ margin: '4px 0 0 18px', padding: 0, fontSize: 13 }}>{p.ejemplos.filter(Boolean).map((e, k) => <li key={k}>«{e}»</li>)}</ul></div>)}
        </div>
        <div className="tarjeta"><h2>Últimas llamadas</h2>
          <div className="desliza"><table><tbody>{d?.recientes.map((r) => <tr key={r.id} className="click" onClick={() => abrirAlumno(r.usuarioId)}>
            <td><b>{[r.nombre, r.apellido].filter(Boolean).join(' ')}</b> <span className="muted">· {nombreTutor(r.tutorId)} · {IDIOMAS[r.idioma] ?? r.idioma} N{r.nivel}</span>
              {r.recomendacion && <><br /><span className="muted" style={{ fontSize: 12 }}>{r.recomendacion}</span></>}
              <br /><span className="muted mono" style={{ fontSize: 11 }}>{lineaTecnica(r.tecnico)}</span></td>
            <td className="num">{r.nota != null ? <span className={`pill ${claseNota(r.nota)}`}>{r.nota}</span> : '—'}</td>
            <td className="num">{fecha(r.creadoEn)}</td>
          </tr>)}</tbody></table></div>
        </div>
      </div>
    </>
  )
}
