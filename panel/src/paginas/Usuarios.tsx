import { useEffect, useState } from 'react'
import { api, hace, IDIOMAS, minutos, PLANES } from '../api'

export default function Usuarios({ abrir }: { abrir: (id: string) => void }) {
  const [q, setQ] = useState(''); const [lista, setLista] = useState<any[]>([])
  useEffect(() => { const t = setTimeout(() => api(`/admin/usuarios?q=${encodeURIComponent(q)}`).then(setLista), 250); return () => clearTimeout(t) }, [q])
  return (
    <>
      <div className="cab"><h1>Alumnos</h1><div style={{ width: 280 }}><input placeholder="Buscar por nombre o correo…" value={q} onChange={(e) => setQ(e.target.value)} /></div></div>
      <div className="tarjeta">
        <table>
          <thead><tr><th>Alumno</th><th>Idioma</th><th>Nivel</th><th>Lecciones</th><th>XP</th><th>Racha</th><th>Tiempo</th><th>Errores</th><th>Plan</th><th>Última actividad</th></tr></thead>
          <tbody>
            {lista.map((u) => (
              <tr key={u.id} className="click" onClick={() => abrir(u.id)}>
                <td><b>{u.nombre}</b><br /><span className="muted mono">{u.email}</span></td>
                <td>{IDIOMAS[u.idioma_meta] ?? u.idioma_meta}</td>
                <td><span className="pill">N{u.nivel_actual}</span></td>
                <td><div style={{ display: 'flex', alignItems: 'center', gap: 8 }}><div className="barra"><i style={{ width: `${Math.min(100, u.lecciones % 100)}%` }} /></div><span>{u.lecciones}</span></div></td>
                <td>{u.xp}</td><td>{u.racha} d</td><td>{minutos(u.segundos)}</td>
                <td>{u.errores_pendientes > 0 ? <span className="pill mal">{u.errores_pendientes}</span> : <span className="muted">0</span>}</td>
                <td>{u.plan_id ? <span className="pill ok">{PLANES[u.plan_id] ?? u.plan_id}</span> : <span className="pill trial">{Math.max(0, 60 - Math.round(u.trial_segundos / 60))} min gratis</span>}</td>
                <td title={u.ultima_actividad}>{hace(u.ultima_actividad)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {lista.length === 0 && <p className="muted">No hay alumnos que coincidan.</p>}
      </div>
    </>
  )
}
