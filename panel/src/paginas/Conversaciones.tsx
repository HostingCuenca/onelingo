import { useEffect, useState } from 'react'
import { api, fecha, IDIOMAS } from '../api'

export default function Conversaciones() {
  const [lista, setLista] = useState<any[]>([]); const [estado, setEstado] = useState<any>(null)
  useEffect(() => { api('/admin/conversaciones').then(setLista); api('/admin/estado-ia').then(setEstado) }, [])
  const tokens = lista.reduce((a, c) => a + c.tokens_entrada + c.tokens_salida, 0)
  return (
    <>
      <div className="cab"><h1>Conversaciones con IA</h1>{estado && <span className={`pill ${estado.ia ? 'ok' : 'trial'}`}>{estado.ia ? `IA activa · ${estado.modelo}` : 'IA sin clave: la app usa el simulador'}</span>}</div>
      <div className="kpis"><div className="kpi"><div className="v">{lista.length}</div><div className="l">Turnos (últimos 100)</div></div><div className="kpi"><div className="v">{tokens.toLocaleString('es')}</div><div className="l">Tokens</div></div></div>
      <div className="tarjeta"><table><thead><tr><th>Alumno</th><th>Idioma · nivel</th><th>Situación</th><th>Alumno dijo</th><th>Tutor respondió</th><th>Correcciones</th><th>Fecha</th></tr></thead><tbody>
        {lista.map((c) => <tr key={c.id}><td><b>{c.nombre}</b><br /><span className="muted mono">{c.email}</span></td><td>{IDIOMAS[c.idioma] ?? c.idioma} · N{c.nivel}</td><td>{c.situacion_id ?? 'libre'}</td><td>{c.mensaje_alumno}</td><td>{c.respuesta?.reply}<br /><span className="muted" style={{ fontSize: 12 }}>{c.respuesta?.traduccion}</span></td><td>{(c.respuesta?.corrections ?? []).map((x: any, i: number) => <div key={i}><s>{x.original}</s> → <b>{x.correcto}</b></div>)}</td><td>{fecha(c.fecha)}</td></tr>)}
      </tbody></table>{lista.length === 0 && <p className="muted">Sin conversaciones con la IA real todavía. Configura ANTHROPIC_API_KEY en el backend.</p>}</div>
    </>
  )
}
