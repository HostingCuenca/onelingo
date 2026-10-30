import { useEffect, useState } from 'react'
import { api, descargar, hace, IDIOMAS, minutos, nivelCorto, PLANES, PLATAFORMAS } from '../api'

type Filtros = { q: string; idioma: string; plataforma: string; estado: string; plan: string; orden: string; dir: 'asc' | 'desc' }
const INICIAL: Filtros = { q: '', idioma: '', plataforma: '', estado: '', plan: '', orden: 'ultima_actividad', dir: 'desc' }
const consulta = (f: Filtros) => new URLSearchParams(Object.entries(f).filter(([, v]) => v !== '')).toString()

const COLUMNAS: { clave?: string; titulo: string }[] = [
  { clave: 'nombre', titulo: 'Alumno' }, { titulo: 'Idioma' }, { titulo: 'Plataforma' }, { clave: 'clases', titulo: 'Clases' }, { clave: 'xp', titulo: 'XP' },
  { clave: 'segundos', titulo: 'Tiempo' }, { clave: 'conversaciones', titulo: 'Tutor IA' }, { titulo: 'Plan' }, { clave: 'creado_en', titulo: 'Registro' }, { clave: 'ultima_actividad', titulo: 'Última actividad' },
]

export default function Usuarios({ abrir }: { abrir: (id: string) => void }) {
  const [f, setF] = useState<Filtros>(INICIAL)
  const [d, setD] = useState<{ total: number; filas: any[]; pruebaMinutos?: number } | null>(null)
  const [err, setErr] = useState('')
  const cambiar = (k: keyof Filtros, v: string) => setF((x) => ({ ...x, [k]: v }))
  const ordenar = (clave: string) => setF((x) => ({ ...x, orden: clave, dir: x.orden === clave && x.dir === 'desc' ? 'asc' : 'desc' }))
  useEffect(() => {
    const t = setTimeout(() => api(`/admin/usuarios?${consulta(f)}`).then((r) => { setD(r); setErr('') }).catch((e) => setErr(e.message)), 250)
    return () => clearTimeout(t)
  }, [f])
  const exportar = () => descargar(`/admin/usuarios.csv?${consulta(f)}`, `alumnos-onelingo.csv`).catch((e) => setErr(e.message))
  return (
    <>
      <div className="cab"><h1>Alumnos</h1><button className="sec" onClick={exportar}>Exportar CSV</button></div>
      <div className="filtros">
        <input placeholder="Buscar por nombre, correo o teléfono…" value={f.q} onChange={(e) => cambiar('q', e.target.value)} />
        <select value={f.idioma} onChange={(e) => cambiar('idioma', e.target.value)} aria-label="Idioma"><option value="">Todos los idiomas</option>{Object.entries(IDIOMAS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
        <select value={f.plataforma} onChange={(e) => cambiar('plataforma', e.target.value)} aria-label="Plataforma"><option value="">Todas las plataformas</option>{Object.entries(PLATAFORMAS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
        <select value={f.estado} onChange={(e) => cambiar('estado', e.target.value)} aria-label="Actividad"><option value="">Activos e inactivos</option><option value="activos">Activos (7 días)</option><option value="inactivos">Inactivos (más de 7 días)</option></select>
        <select value={f.plan} onChange={(e) => cambiar('plan', e.target.value)} aria-label="Plan"><option value="">Todos los planes</option><option value="pago">Con plan de pago</option><option value="prueba">En prueba gratuita</option></select>
        {JSON.stringify(f) !== JSON.stringify(INICIAL) && <button className="sec" onClick={() => setF(INICIAL)}>Limpiar</button>}
      </div>
      {err && <p className="err">{err}</p>}
      <div className="tarjeta">
        {d && <p className="muted" style={{ marginTop: 0 }}>{d.total === d.filas.length ? `${d.total} alumnos` : `Mostrando ${d.filas.length} de ${d.total} alumnos (el CSV los incluye todos)`}</p>}
        <div className="desliza"><table>
          <thead><tr>{COLUMNAS.map((c) => <th key={c.titulo} className={c.clave ? 'ordenable' : ''} onClick={c.clave ? () => ordenar(c.clave!) : undefined}>{c.titulo}{c.clave === f.orden ? (f.dir === 'desc' ? ' ↓' : ' ↑') : ''}</th>)}</tr></thead>
          <tbody>
            {d?.filas.map((u) => (
              <tr key={u.id} className="click" onClick={() => abrir(u.id)}>
                <td><b>{[u.nombre, u.apellido].filter(Boolean).join(' ')}</b><br /><span className="muted mono">{u.email}</span>{u.email_verificado ? <span className="ok-texto" title="Correo verificado"> ✓</span> : <span className="muted" title="Correo sin verificar"> · sin verificar</span>}{u.telefono && <><br /><span className="muted mono">{u.telefono}</span></>}</td>
                <td>{IDIOMAS[u.idioma_meta] ?? u.idioma_meta}{u.nivel_clases !== null && <> <span className="pill">{nivelCorto(u.nivel_clases)}</span></>}</td>
                <td>{PLATAFORMAS[u.plataforma] ?? u.plataforma}</td>
                <td className="num"><b>{u.clases}</b>{u.ultima_clase && <><br /><span className="muted" style={{ fontSize: 11 }}>{hace(u.ultima_clase)}</span></>}</td>
                <td className="num">{u.xp}</td><td className="num">{minutos(u.segundos)}</td><td className="num">{u.conversaciones}</td>
                <td>{u.plan_id ? <span className="pill ok">{PLANES[u.plan_id] ?? u.plan_id}</span> : <span className="pill trial">{Math.max(0, (d.pruebaMinutos ?? 60) - Math.round(u.trial_segundos / 60))} min gratis</span>}</td>
                <td title={u.creado_en}>{hace(u.creado_en)}</td>
                <td title={u.ultima_actividad}><span className={`punto ${u.activo ? 'ok' : ''}`} />{hace(u.ultima_actividad)}</td>
              </tr>
            ))}
          </tbody>
        </table></div>
        {d && d.filas.length === 0 && <p className="muted">No hay alumnos que coincidan.</p>}
        {!d && !err && <p className="muted">Cargando…</p>}
      </div>
    </>
  )
}
