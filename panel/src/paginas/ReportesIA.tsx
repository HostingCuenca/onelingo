import { useEffect, useState } from 'react'
import { api, fecha, hace, IDIOMAS, num } from '../api'
import ErrorCarga from '../ErrorCarga'

type Reporte = {
  id: number; origen: string; motivo: string; texto: string; comentario: string
  contexto: { idioma?: string; tutorId?: string; situacion?: string | number }
  revisado: boolean; creado_en: string; usuario_id: string; nombre: string; email: string
}
type Datos = { reportes: Reporte[]; total: number; pendientes: number }
const MOTIVOS: Record<string, string> = { ofensivo: 'Ofensivo', incorrecto: 'Incorrecto', inapropiado: 'Inapropiado', otro: 'Otro' }
const ORIGENES: Record<string, string> = { chat: 'Chat', llamada: 'Videollamada', situacion: 'Situación', ejercicio: 'Ejercicio', otro: 'Otro' }

/** Respuestas de la IA que los alumnos reportaron desde la app (política de Google Play). */
export default function ReportesIA({ abrirAlumno }: { abrirAlumno: (id: string) => void }) {
  const [filtro, setFiltro] = useState<'' | 'pendientes' | 'revisados'>('pendientes')
  const [d, setD] = useState<Datos | null>(null)
  const [err, setErr] = useState(''); const [abierto, setAbierto] = useState<Reporte | null>(null)
  const [ocupado, setOcupado] = useState(false); const [msg, setMsg] = useState('')
  const cargar = () => api<Datos>(`/admin/reportes-ia?estado=${filtro}`).then((r) => { setD(r); setErr('') }).catch((x) => setErr(x.message))
  useEffect(() => { cargar() }, [filtro])
  const marcar = async (revisado: boolean) => {
    if (!abierto) return
    setOcupado(true); setMsg('')
    try {
      await api(`/admin/reportes-ia/${abierto.id}`, { metodo: 'PUT', cuerpo: { revisado } })
      setAbierto({ ...abierto, revisado }); setMsg('Guardado.'); await cargar()
    } catch (x: any) { setMsg(x.message) } finally { setOcupado(false) }
  }
  if (err) return <ErrorCarga msg={err} reintentar={() => { setErr(''); cargar() }} />
  return (
    <>
      <div className="cab"><h1>Reportes de la IA</h1>{d && d.pendientes > 0 && <span className="pill trial">{num(d.pendientes)} por revisar</span>}</div>
      <p className="muted pie-nota" style={{ margin: '-8px 0 16px' }}>Respuestas del tutor que un alumno marcó como ofensivas, incorrectas o inapropiadas (chat y videollamada). Revísalas y marca cada una al terminar.</p>
      <div className="filtros">
        <select value={filtro} onChange={(e) => setFiltro(e.target.value as '' | 'pendientes' | 'revisados')} aria-label="Estado">
          <option value="pendientes">Por revisar</option><option value="revisados">Revisados</option><option value="">Todos</option>
        </select>
      </div>
      <div className="grid2">
        <div className="tarjeta">
          {!d ? <p className="muted">Cargando…</p> : d.reportes.length === 0 ? <p className="muted">No hay reportes en esta lista.</p> :
            <div className="desliza"><table>
              <thead><tr><th>Respuesta</th><th>Motivo</th><th>Origen</th><th>Recibido</th></tr></thead>
              <tbody>{d.reportes.map((r) => <tr key={r.id} className="click" onClick={() => { setAbierto(r); setMsg('') }}>
                <td>{r.texto.length > 90 ? r.texto.slice(0, 90) + '…' : r.texto}<br /><span className="muted mono">{r.email}</span></td>
                <td><span className={`pill ${r.revisado ? '' : r.motivo === 'ofensivo' || r.motivo === 'inapropiado' ? 'mal' : 'trial'}`}>{MOTIVOS[r.motivo] ?? r.motivo}</span></td>
                <td>{ORIGENES[r.origen] ?? r.origen}</td>
                <td>{hace(r.creado_en)}</td>
              </tr>)}</tbody>
            </table></div>}
        </div>
        <div className="tarjeta">
          {!abierto ? <p className="muted">Selecciona un reporte para verlo.</p> : <>
            <h2>{MOTIVOS[abierto.motivo] ?? abierto.motivo} · {ORIGENES[abierto.origen] ?? abierto.origen}</h2>
            <p style={{ whiteSpace: 'pre-wrap', background: 'var(--fondo, #f7f5ff)', borderRadius: 10, padding: 10 }}>{abierto.texto}</p>
            {abierto.comentario && <p><b>Comentario del alumno:</b> {abierto.comentario}</p>}
            <p className="muted">
              {abierto.contexto?.idioma && <>{IDIOMAS[abierto.contexto.idioma] ?? abierto.contexto.idioma} · </>}
              {abierto.contexto?.tutorId && <>tutor {abierto.contexto.tutorId} · </>}
              {abierto.contexto?.situacion !== undefined && <>situación {String(abierto.contexto.situacion)} · </>}
              {fecha(abierto.creado_en)}
            </p>
            <p><a className="click" onClick={() => abrirAlumno(abierto.usuario_id)}>{abierto.nombre || abierto.email}</a> <span className="muted mono">{abierto.email}</span></p>
            <div className="acciones">
              {abierto.revisado
                ? <button className="sec" disabled={ocupado} onClick={() => marcar(false)}>Volver a pendiente</button>
                : <button disabled={ocupado} onClick={() => marcar(true)}>Marcar revisado</button>}
              {msg && <span className="muted">{msg}</span>}
            </div>
          </>}
        </div>
      </div>
    </>
  )
}
