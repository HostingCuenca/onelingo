import { useEffect, useState } from 'react'
import { api, IDIOMAS, minutos, NIVELES, SKILLS } from '../api'

export default function Resumen() {
  const [d, setD] = useState<any>(null)
  const [ia, setIa] = useState<any>(null)
  useEffect(() => { api('/admin/resumen').then(setD); api('/admin/estado-ia').then(setIa).catch(() => {}) }, [])
  if (!d) return <p className="muted">Cargando…</p>
  const maxAct = Math.max(1, ...d.actividad.map((a: any) => a.eventos))
  return (
    <>
      <div className="cab"><h1>Resumen</h1><span className="muted">Actualizado ahora</span></div>
      <div className="kpis">
        <div className="kpi"><div className="v">{d.usuarios}</div><div className="l">Alumnos</div></div>
        <div className="kpi"><div className="v">{d.activos7d}</div><div className="l">Activos 7 días</div></div>
        <div className="kpi"><div className="v">{d.nuevos7d}</div><div className="l">Nuevos 7 días</div></div>
        <div className="kpi"><div className="v">{d.con_plan}</div><div className="l">Con plan de pago</div></div>
        <div className="kpi"><div className="v">{d.lecciones}</div><div className="l">Lecciones completadas</div></div>
        <div className="kpi"><div className="v">{minutos(d.segundos)}</div><div className="l">Tiempo de estudio</div></div>
      </div>
      {ia?.servicios && <div className="tarjeta"><h2>Servicios de IA</h2>
        <table><tbody>{Object.entries(ia.servicios).map(([k, v]: any) => <tr key={k}><td><b>{k === 'openai' ? 'OpenAI' : k === 'gemini' ? 'Google Gemini' : 'ElevenLabs'}</b></td><td>{v.uso}</td><td className="mono">{v.modelo}</td><td style={{ textAlign: 'right' }}><span className={`pill ${v.activo ? 'ok' : 'mal'}`}>{v.activo ? 'Conectado' : 'Sin clave'}</span></td></tr>)}</tbody></table>
      </div>}
      <div className="grid2">
        <div className="tarjeta"><h2>Alumnos por idioma</h2>
          <table><tbody>{d.porIdioma.map((r: any) => <tr key={r.idioma}><td>{IDIOMAS[r.idioma] ?? r.idioma}</td><td style={{ width: 60, textAlign: 'right' }}><b>{r.usuarios}</b></td></tr>)}</tbody></table>
          {d.porIdioma.length === 0 && <p className="muted">Sin alumnos todavía.</p>}
        </div>
        <div className="tarjeta"><h2>Alumnos por nivel</h2>
          <table><tbody>{d.porNivel.map((r: any) => <tr key={r.nivel}><td>Nivel {r.nivel} · {NIVELES[r.nivel - 1]}</td><td style={{ width: 60, textAlign: 'right' }}><b>{r.usuarios}</b></td></tr>)}</tbody></table>
          {d.porNivel.length === 0 && <p className="muted">Sin progreso sincronizado.</p>}
        </div>
        <div className="tarjeta"><h2>Exámenes</h2>
          <p>{d.examenes.total} presentados · {d.examenes.aprobados} aprobados · nota media {d.examenes.media ?? '—'} %</p>
        </div>
        <div className="tarjeta"><h2>Errores por habilidad</h2>
          <table><tbody>{d.errores.map((r: any) => <tr key={r.skill}><td>{SKILLS[r.skill] ?? r.skill}</td><td style={{ width: 60, textAlign: 'right' }}><b>{r.total}</b></td></tr>)}</tbody></table>
          {d.errores.length === 0 && <p className="muted">Sin errores registrados.</p>}
        </div>
      </div>
      <div className="tarjeta"><h2>Actividad (14 días)</h2>
        <div className="barras">{d.actividad.map((a: any) => <div key={a.dia} style={{ height: `${(a.eventos / maxAct) * 100}%` }} title={`${a.dia}: ${a.eventos} eventos, ${a.usuarios} alumnos`}><span>{a.eventos}</span></div>)}</div>
        {d.actividad.length === 0 && <p className="muted">Sin eventos todavía.</p>}
      </div>
    </>
  )
}
