import { useEffect, useState } from 'react'
import { api, fecha, hace, IDIOMAS, minutos, nivelCorto, num, PLANES, PLATAFORMAS, SKILLS, usd } from '../api'

const lista = (v: unknown) => (Array.isArray(v) ? v.join(', ') : typeof v === 'object' && v ? Object.keys(v).join(', ') : String(v ?? ''))

export default function UsuarioDetalle({ id, volver }: { id: string; volver: () => void }) {
  const [d, setD] = useState<any>(null)
  const [err, setErr] = useState('')
  useEffect(() => { api(`/admin/usuarios/${id}`).then(setD).catch((e) => setErr(e.message)) }, [id])
  if (err) return <p className="err">{err}</p>
  if (!d) return <p className="muted">Cargando…</p>
  const u = d.usuario, p = d.progreso, e = p?.estado ?? {}
  const g = e.diagnostico
  const nivelMax = Math.max(-1, ...(d.progresoIdiomas.find((x: any) => x.idioma === u.idioma_meta)?.niveles ?? []).filter((n: any) => n.clases > 0).map((n: any) => n.nivel))
  return (
    <>
      <div className="cab"><div><span className="volver" onClick={volver}>← Alumnos</span><h1>{u.nombre}</h1>
        <span className="muted mono">{u.email} · {PLATAFORMAS[u.plataforma || 'desconocida'] ?? u.plataforma} · registrado {fecha(u.creado_en)} · activo {hace(u.ultima_actividad)}</span></div>
        <div>{u.plan_id ? <span className="pill ok">{PLANES[u.plan_id] ?? u.plan_id}</span> : <span className="pill trial">Prueba gratuita · {Math.max(0, 60 - Math.round(u.trial_segundos / 60))} min</span>}</div></div>
      <div className="kpis">
        <div className="kpi"><div className="v">{IDIOMAS[u.idioma_meta] ?? u.idioma_meta}</div><div className="l">Aprende</div><div className="nota">nativo: {IDIOMAS[u.idioma_nativo] ?? u.idioma_nativo}</div></div>
        <div className="kpi"><div className="v">{d.clases}</div><div className="l">Clases completadas</div>{d.legado > 0 && <div className="nota">{d.legado} del temario antiguo</div>}</div>
        <div className="kpi"><div className="v">{nivelMax >= 0 ? nivelCorto(nivelMax) : '—'}</div><div className="l">Nivel más alto con clases</div></div>
        <div className="kpi"><div className="v">{p?.xp ?? 0}</div><div className="l">XP</div><div className="nota">racha {p?.racha ?? 0} d</div></div>
        <div className="kpi"><div className="v">{minutos(p?.segundos_estudio ?? 0)}</div><div className="l">Estudio</div></div>
        <div className="kpi"><div className="v">{d.ia.conversaciones}</div><div className="l">Turnos con tutor IA</div><div className="nota">{num(d.ia.entrada + d.ia.salida)} tokens · {usd(d.ia.coste)}</div></div>
      </div>

      <div className="grid2">
        <div className="tarjeta"><h2>Progreso por idioma y nivel</h2>
          {d.progresoIdiomas.map((pi: any) => <div key={pi.idioma} style={{ marginBottom: 12 }}>
            <b>{IDIOMAS[pi.idioma] ?? pi.idioma}</b> <span className="muted">· {pi.total} clases</span>
            <table><tbody>{pi.niveles.filter((n: any) => n.clases > 0 || n.nivel <= Math.max(1, nivelMax)).map((n: any) => <tr key={n.nivel}>
              <td style={{ width: 50 }}>{nivelCorto(n.nivel)}</td>
              <td><div className="barra"><i style={{ width: `${n.publicadas ? Math.min(100, (n.clases / n.publicadas) * 100) : n.clases ? 100 : 0}%` }} /></div></td>
              <td className="num" style={{ width: 80 }}>{n.clases}{n.publicadas ? ` / ${n.publicadas}` : ''}</td>
              <td className="num" style={{ width: 90 }}>{(() => { const ex = d.examenes.find((x: any) => x.nivel === n.nivel); return ex ? <span className={`pill ${ex.aprobado ? 'ok' : 'mal'}`}>Examen {ex.pct} %</span> : null })()}</td></tr>)}</tbody></table>
          </div>)}
          {d.progresoIdiomas.length === 0 && <p className="muted">Todavía no ha completado ninguna clase.</p>}
        </div>
        <div className="tarjeta"><h2>Prueba de ubicación</h2>
          {d.ubicacion.map((x: any, i: number) => { const v = x.datos ?? {}; return <div key={i} className="bloque-err">
            <div><b>{IDIOMAS[v.idioma] ?? v.idioma ?? '—'}</b> · nivel elegido <b>{v.nivelElegido ?? '—'}</b> (estimado {v.nivelEstimado ?? '—'}{v.cefr ? `, ${v.cefr}` : ''}) <span className="muted">· {fecha(x.fecha)}</span></div>
            <div className="muted">{v.preguntas !== undefined ? `${v.preguntas} preguntas` : ''}{v.precision !== undefined ? ` · ${v.precision} % de precisión` : v.aciertos !== undefined ? ` · ${v.aciertos} aciertos` : ''}{v.debilidades ? ` · reforzar: ${lista(v.debilidades)}` : ''}</div></div> })}
          {d.ubicacion.length === 0 && g && <p>Guardada en el progreso: nivel <b>{g.nivel ?? g.elegido ?? g.nivelCliente ?? '—'}</b>{g.cefr ? ` · ${g.cefr}` : ''}{g.preguntas ? ` · ${g.preguntas} preguntas` : ''}</p>}
          {d.ubicacion.length === 0 && !g && <p className="muted">No hizo la prueba de ubicación.</p>}
        </div>
        <div className="tarjeta"><h2>Últimas clases completadas</h2>
          <div className="desliza"><table><tbody>{d.ultimasClases.map((c: any) => <tr key={c.unidad}><td><b>{c.titulo || c.unidad}</b><br /><span className="muted mono">{c.unidad}</span></td><td>{nivelCorto(c.nivel)}</td><td className="num">{c.intentos > 1 ? `${c.intentos} intentos` : ''}</td><td className="num">{fecha(c.fecha)}</td></tr>)}</tbody></table></div>
          {d.ultimasClases.length === 0 && <p className="muted">Sin clases con fecha.</p>}
          {d.empezadas.length > 0 && <><h2 style={{ marginTop: 14 }}>Empezadas sin terminar</h2>
            <table><tbody>{d.empezadas.map((c: any) => <tr key={c.unidad}><td><b>{c.titulo || c.unidad}</b> <span className="muted mono">{c.unidad}</span></td><td className="num">{fecha(c.fecha)}</td></tr>)}</tbody></table></>}
        </div>
        <div className="tarjeta"><h2>Conversaciones con el tutor</h2>
          <table><tbody>{d.conversaciones.map((c: any) => <tr key={c.id}><td><span className="muted">{IDIOMAS[c.idioma] ?? c.idioma} · N{c.nivel}{c.situacion_id ? ` · situación ${c.situacion_id}` : ''}</span><br />{c.mensaje_alumno}<br /><span className="muted">↳ {c.respuesta}</span></td><td className="num" style={{ width: 110 }}>{fecha(c.fecha)}<br /><span className="muted">{c.tokens_entrada + c.tokens_salida} tokens</span></td></tr>)}</tbody></table>
          {d.conversaciones.length === 0 && <p className="muted">Sin conversaciones.</p>}
        </div>
        <div className="tarjeta"><h2>Errores recientes ({d.errores.length})</h2>
          {d.errores.slice(0, 12).map((x: any) => <div className="errcard" key={x.id}><span className="pill">{SKILLS[x.skill] ?? x.skill}</span> <span className="muted" style={{ fontSize: 12 }}>{x.origen} · {hace(x.fecha)}{x.practicado ? ' · practicado' : ''}</span><br /><s>{x.original}</s> → <b>{x.correccion}</b><br /><span className="muted" style={{ fontSize: 12 }}>{x.explicacion}</span></div>)}
          {d.errores.length === 0 && <p className="muted">Sin errores registrados.</p>}
        </div>
        <div className="tarjeta"><h2>Actividad reciente</h2>
          <div className="desliza"><table><tbody>{d.eventos.map((ev: any, i: number) => <tr key={i}><td>{ev.tipo}</td><td className="muted mono" style={{ wordBreak: 'break-all' }}>{JSON.stringify(ev.datos).slice(0, 160)}</td><td className="num">{fecha(ev.fecha)}</td></tr>)}</tbody></table></div>
          {d.eventos.length === 0 && <p className="muted">Sin eventos.</p>}
          <p className="muted pie-nota">Última sincronización: {fecha(p?.actualizado_en)} · tutor {u.tutor_id} · {(e.diasActividad ?? []).length} días con actividad registrados por la app · {Object.keys(e.practicas ?? {}).length} evidencias de práctica.</p>
        </div>
      </div>
    </>
  )
}
