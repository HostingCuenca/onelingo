import { useEffect, useState } from 'react'
import { api, fecha, hace, IDIOMAS, num } from '../api'
import ErrorCarga from '../ErrorCarga'

type Estado = 'nueva' | 'contactada' | 'cerrada'
type Cotizacion = {
  id: number; empresa: string; empleados: number; idiomas: string[]; mensaje: string; nombre: string; email: string; telefono: string
  usuarioId: string | null; estado: Estado; nota: string; creadoEn: string; actualizadoEn: string
}
const ESTADO: Record<Estado, [string, string]> = { nueva: ['trial', 'Nueva'], contactada: ['ok', 'Contactada'], cerrada: ['', 'Cerrada'] }

/** Plan Empresarial: solicitudes de cotización que llegan desde la app. */
export default function Cotizaciones() {
  const [filtro, setFiltro] = useState<'' | Estado>('')
  const [d, setD] = useState<{ nuevas: number; cotizaciones: Cotizacion[] } | null>(null)
  const [err, setErr] = useState(''); const [abierta, setAbierta] = useState<Cotizacion | null>(null)
  const [nota, setNota] = useState(''); const [ocupado, setOcupado] = useState(false); const [msg, setMsg] = useState('')
  const cargar = () => api<{ nuevas: number; cotizaciones: Cotizacion[] }>(`/admin/cotizaciones?estado=${filtro}`).then((r) => { setD(r); setErr('') }).catch((x) => setErr(x.message))
  useEffect(() => { cargar() }, [filtro])
  const abrir = (c: Cotizacion) => { setAbierta(c); setNota(c.nota); setMsg('') }
  const guardar = async (estado?: Estado) => {
    if (!abierta) return
    setOcupado(true); setMsg('')
    try {
      await api(`/admin/cotizaciones/${abierta.id}`, { metodo: 'PUT', cuerpo: { nota, ...(estado ? { estado } : {}) } })
      setAbierta({ ...abierta, nota, estado: estado ?? abierta.estado }); setMsg('Guardado.'); await cargar()
    } catch (x: any) { setMsg(x.message) } finally { setOcupado(false) }
  }
  if (err) return <ErrorCarga msg={err} reintentar={() => { setErr(''); cargar() }} />
  return (
    <>
      <div className="cab"><h1>Cotizaciones</h1>{d && d.nuevas > 0 && <span className="pill trial">{num(d.nuevas)} nuevas</span>}</div>
      <p className="muted pie-nota" style={{ margin: '-8px 0 16px' }}>Solicitudes del plan Empresarial enviadas desde la app. El solicitante recibe un correo de confirmación; la propuesta se le envía desde tu correo.</p>
      <div className="filtros">
        <select value={filtro} onChange={(e) => setFiltro(e.target.value as '' | Estado)} aria-label="Estado">
          <option value="">Todas</option><option value="nueva">Nuevas</option><option value="contactada">Contactadas</option><option value="cerrada">Cerradas</option>
        </select>
      </div>
      <div className="grid2">
        <div className="tarjeta">
          {!d ? <p className="muted">Cargando…</p> : d.cotizaciones.length === 0 ? <p className="muted">Todavía no hay solicitudes.</p> :
            <div className="desliza"><table>
              <thead><tr><th>Empresa</th><th className="num">Personas</th><th>Estado</th><th>Recibida</th></tr></thead>
              <tbody>{d.cotizaciones.map((c) => <tr key={c.id} className="click" onClick={() => abrir(c)}>
                <td><b>{c.empresa}</b><br /><span className="muted mono">{c.email}</span></td>
                <td className="num">{num(c.empleados)}</td>
                <td><span className={`pill ${ESTADO[c.estado][0]}`}>{ESTADO[c.estado][1]}</span></td>
                <td>{hace(c.creadoEn)}</td>
              </tr>)}</tbody>
            </table></div>}
        </div>
        <div className="tarjeta">
          {!abierta ? <p className="muted">Selecciona una solicitud para verla.</p> : <>
            <h2>{abierta.empresa}</h2>
            <p><b>{num(abierta.empleados)}</b> personas · {abierta.idiomas.map((c) => IDIOMAS[c] ?? c).join(', ')}</p>
            <p>{abierta.nombre || '—'} · <a href={`mailto:${abierta.email}`} className="mono">{abierta.email}</a>{abierta.telefono && <> · <span className="mono">{abierta.telefono}</span></>}</p>
            {abierta.mensaje && <p style={{ whiteSpace: 'pre-wrap' }}>{abierta.mensaje}</p>}
            <p className="muted">Recibida el {fecha(abierta.creadoEn)}{abierta.usuarioId ? ' · enviada con una cuenta de alumno' : ' · sin cuenta'}</p>
            <label className="campo"><span>Nota interna</span><textarea rows={3} value={nota} maxLength={2000} onChange={(e) => setNota(e.target.value)} /></label>
            <div className="acciones">
              <button disabled={ocupado} onClick={() => guardar()}>Guardar nota</button>
              {abierta.estado !== 'contactada' && <button className="sec" disabled={ocupado} onClick={() => guardar('contactada')}>Marcar contactada</button>}
              {abierta.estado !== 'cerrada' && <button className="sec" disabled={ocupado} onClick={() => guardar('cerrada')}>Cerrar</button>}
              {abierta.estado !== 'nueva' && <button className="sec" disabled={ocupado} onClick={() => guardar('nueva')}>Volver a nueva</button>}
              {msg && <span className="muted">{msg}</span>}
            </div>
          </>}
        </div>
      </div>
    </>
  )
}
