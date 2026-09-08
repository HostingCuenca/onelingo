import { useEffect, useState } from 'react'
import { api, fecha, hace, IDIOMAS, minutos, NIVELES, PLANES, SKILLS } from '../api'

export default function UsuarioDetalle({ id, volver }: { id: string; volver: () => void }) {
  const [d, setD] = useState<any>(null)
  useEffect(() => { api(`/admin/usuarios/${id}`).then(setD) }, [id])
  if (!d) return <p className="muted">Cargando…</p>
  const u = d.usuario, p = d.progreso, e = p?.estado ?? {}
  return (
    <>
      <div className="cab"><div><span className="volver" onClick={volver}>← Alumnos</span><h1>{u.nombre}</h1><span className="muted mono">{u.email} · {u.plataforma || 'app'} · registrado {fecha(u.creado_en)}</span></div>
        <div>{u.plan_id ? <span className="pill ok">{PLANES[u.plan_id]}</span> : <span className="pill trial">Prueba gratuita · {Math.max(0, 60 - Math.round(u.trial_segundos / 60))} min</span>}</div></div>
      <div className="kpis">
        <div className="kpi"><div className="v">{IDIOMAS[u.idioma_meta] ?? u.idioma_meta}</div><div className="l">Aprende</div></div>
        <div className="kpi"><div className="v">N{p?.nivel_actual ?? u.nivel_inicial}</div><div className="l">Nivel actual</div></div>
        <div className="kpi"><div className="v">{p?.lecciones_completadas ?? 0}</div><div className="l">Lecciones</div></div>
        <div className="kpi"><div className="v">{p?.xp ?? 0}</div><div className="l">XP</div></div>
        <div className="kpi"><div className="v">{p?.racha ?? 0} d</div><div className="l">Racha</div></div>
        <div className="kpi"><div className="v">{minutos(p?.segundos_estudio ?? 0)}</div><div className="l">Estudio</div></div>
      </div>
      {d.progreso?.estado?.diagnostico && (() => { const g = d.progreso.estado.diagnostico; return (
        <div className="tarjeta"><h2>Diagnóstico adaptativo</h2>
          <p><b>Nivel {g.nivel}</b> · {g.cefr} · declaró {g.declarado} · {g.preguntas} preguntas · {Math.round((g.aciertos / Math.max(1, g.preguntas)) * 100)} % aciertos · confianza {Math.round((g.confianza ?? 0) * 100)} %</p>
          <table><tbody>{Object.entries(g.skills ?? {}).map(([k, v]: any) => <tr key={k}><td style={{ width: 180 }}>{k}</td><td><div className="barra"><i style={{ width: `${(v / 10) * 100}%` }} /></div></td><td style={{ width: 40, textAlign: 'right' }}><b>{v}</b></td></tr>)}</tbody></table>
          {g.fortalezas?.length > 0 && <p><span className="pill ok">Fortalezas</span> {g.fortalezas.join(', ')}</p>}
          {g.debilidades?.length > 0 && <p><span className="pill mal">Debilidades</span> {g.debilidades.join(', ')}</p>}
          {g.refuerzo?.length > 0 && <p className="muted">Reforzar: {g.refuerzo.join(' · ')}</p>}
          {g.plan?.length > 0 && <ol style={{ paddingLeft: 18 }}>{g.plan.map((x: string, i: number) => <li key={i}>{x}</li>)}</ol>}
          {g.escritura && <p className="muted">Escritura {g.escritura.puntuacion}/10 {g.escritura.porIa ? '(IA)' : '(local)'} · {g.escritura.comentario}</p>}
        </div>) })()}
      <div className="grid2">
        <div className="tarjeta"><h2>Progreso por nivel</h2>
          <table><tbody>{d.porNivel.map((n: any) => {
            const ex = d.examenes.find((x: any) => x.nivel === n.nivel)
            return <tr key={n.nivel}><td>Nivel {n.nivel} · {NIVELES[n.nivel - 1]}</td>
              <td><div style={{ display: 'flex', alignItems: 'center', gap: 8 }}><div className="barra"><i style={{ width: `${n.lecciones}%` }} /></div><span>{n.lecciones}/100</span></div></td>
              <td style={{ textAlign: 'right' }}>{ex ? <span className={`pill ${ex.aprobado ? 'ok' : 'mal'}`}>Examen {ex.pct} %</span> : <span className="muted">sin examen</span>}</td></tr>
          })}</tbody></table>
        </div>
        <div className="tarjeta"><h2>Errores recientes ({d.errores.length})</h2>
          {d.errores.slice(0, 12).map((x: any) => <div className="errcard" key={x.id}><span className="pill">{SKILLS[x.skill] ?? x.skill}</span> <span className="muted" style={{ fontSize: 12 }}>{x.origen} · {hace(x.fecha)}{x.practicado ? ' · practicado' : ''}</span><br /><s>{x.original}</s> → <b>{x.correccion}</b><br /><span className="muted" style={{ fontSize: 12 }}>{x.explicacion}</span></div>)}
          {d.errores.length === 0 && <p className="muted">Sin errores registrados.</p>}
        </div>
        <div className="tarjeta"><h2>Actividad reciente</h2>
          <table><tbody>{d.eventos.map((ev: any, i: number) => <tr key={i}><td>{ev.tipo}</td><td className="muted mono">{JSON.stringify(ev.datos)}</td><td style={{ textAlign: 'right' }}>{fecha(ev.fecha)}</td></tr>)}</tbody></table>
          {d.eventos.length === 0 && <p className="muted">Sin eventos.</p>}
        </div>
        <div className="tarjeta"><h2>Datos sincronizados</h2>
          <p className="muted" style={{ fontSize: 12 }}>Última sincronización: {fecha(p?.actualizado_en)} · tutor {u.tutor_id} · nativo {IDIOMAS[u.idioma_nativo]}</p>
          <p className="muted mono" style={{ fontSize: 11, whiteSpace: 'pre-wrap', maxHeight: 220, overflow: 'auto' }}>{JSON.stringify({ ...e, completadas: `[${(e.completadas ?? []).length} lecciones]`, errores: `[${(e.errores ?? []).length}]` }, null, 1)}</p>
        </div>
      </div>
    </>
  )
}
