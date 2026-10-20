import { useEffect, useState } from 'react'
import { api, fecha } from '../api'

type Texto = { es: string; en: string }
type Plan = {
  id: string; nombre: Texto; descripcion: Texto; incluye: { es: string[]; en: string[] }; idiomas: number; precio: number; moneda: string
  intervalo: 'mes' | 'anio'; destacado: boolean; orden: number; visible: boolean; archivado: boolean; suscriptores: number; actualizadoEn: string
  stripe: { estado: 'sincronizado' | 'sin sincronizar' | 'sin stripe'; error: string | null; productoId: string | null; precioId: string | null; modo: string | null }
}
type Datos = { planes: Plan[]; ajustes: { pruebaMinutos: number; moneda: string }; pagos: { disponible: boolean; modo: 'test' | 'live' | null } }
type Form = { id: string; nombreEs: string; nombreEn: string; descEs: string; descEn: string; incluyeEs: string; incluyeEn: string; idiomas: string; precio: string; intervalo: 'mes' | 'anio'; orden: string; destacado: boolean; visible: boolean }

const INTERVALO: Record<string, string> = { mes: 'al mes', anio: 'al año' }
const SYNC: Record<string, [string, string]> = { sincronizado: ['ok', 'Sincronizado'], 'sin sincronizar': ['mal', 'Sin sincronizar'], 'sin stripe': ['', 'Stripe sin vincular'] }
const precio = (p: { precio: number; moneda: string; intervalo: string }) => `${p.precio.toLocaleString('es', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${p.moneda.toUpperCase()} ${INTERVALO[p.intervalo] ?? ''}`

const formDe = (p?: Plan, orden = 1): Form => ({
  id: p?.id ?? '', nombreEs: p?.nombre.es ?? '', nombreEn: p?.nombre.en ?? '', descEs: p?.descripcion.es ?? '', descEn: p?.descripcion.en ?? '',
  incluyeEs: (p?.incluye.es ?? []).join('\n'), incluyeEn: (p?.incluye.en ?? []).join('\n'), idiomas: String(p?.idiomas ?? 1),
  precio: p ? String(p.precio) : '', intervalo: p?.intervalo ?? 'mes', orden: String(p?.orden ?? orden), destacado: p?.destacado ?? false, visible: p?.visible ?? true,
})
const lineas = (s: string) => s.split('\n').map((x) => x.trim()).filter(Boolean)

/** El cambio de plan del Customer Portal se actualiza con cada plan sincronizado; un fallo no impide guardar. */
const avisoPortal = (p?: { ok: boolean; error?: string }) => (p && !p.ok ? ` No se pudo actualizar el cambio de plan del Customer Portal (${p.error}); se reintenta al sincronizar cualquier plan.` : '')

function Editor({ plan, orden, pagos, alGuardar, cancelar }: { plan?: Plan; orden: number; pagos: Datos['pagos']; alGuardar: (aviso: string) => void; cancelar: () => void }) {
  const [f, setF] = useState<Form>(() => formDe(plan, orden))
  const [err, setErr] = useState(''); const [ocupado, setOcupado] = useState(false)
  const c = (k: keyof Form) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) =>
    setF({ ...f, [k]: e.target.type === 'checkbox' ? (e.target as HTMLInputElement).checked : e.target.value })
  const cambiaPrecio = !!plan && (Number(f.precio) !== plan.precio || f.intervalo !== plan.intervalo)
  const guardar = async (e: React.FormEvent) => {
    e.preventDefault(); setErr(''); setOcupado(true)
    const cuerpo = {
      ...(plan || !f.id.trim() ? {} : { id: f.id.trim() }),
      nombre: { es: f.nombreEs, en: f.nombreEn }, descripcion: { es: f.descEs, en: f.descEn },
      incluye: { es: lineas(f.incluyeEs), en: lineas(f.incluyeEn) }, idiomas: Number(f.idiomas), precio: Number(String(f.precio).replace(',', '.')),
      intervalo: f.intervalo, orden: Number(f.orden), destacado: f.destacado, visible: f.visible,
    }
    try {
      const r = await api<{ sync: { ok: boolean; error?: string; precioNuevo?: boolean }; portal?: { ok: boolean; error?: string } }>(plan ? `/admin/planes/${plan.id}` : '/admin/planes', { metodo: plan ? 'PUT' : 'POST', cuerpo })
      alGuardar((!pagos.disponible ? 'Guardado. Se sincronizará con Stripe al vincularlo en Conexiones.'
        : r.sync.ok ? `Guardado y sincronizado con Stripe${r.sync.precioNuevo && plan ? ' (nuevo precio creado; los suscriptores actuales conservan el suyo)' : ''}.`
        : `Guardado, pero sin sincronizar con Stripe: ${r.sync.error}. Usa «Reintentar».`) + avisoPortal(r.portal))
    } catch (x: any) { setErr(x.datos?.detalles?.join(' · ') || x.message) } finally { setOcupado(false) }
  }
  return (
    <form className="tarjeta conexion-form" onSubmit={guardar}>
      <h2>{plan ? `Editar «${plan.nombre.es}»` : 'Nuevo plan'}</h2>
      <div className="form-grid">
        <label className="campo"><span>Nombre (español)</span><input required maxLength={80} value={f.nombreEs} onChange={c('nombreEs')} /></label>
        <label className="campo"><span>Nombre (inglés)</span><input maxLength={80} value={f.nombreEn} onChange={c('nombreEn')} /></label>
        <label className="campo"><span>Descripción (español)</span><input maxLength={500} value={f.descEs} onChange={c('descEs')} /></label>
        <label className="campo"><span>Descripción (inglés)</span><input maxLength={500} value={f.descEn} onChange={c('descEn')} /></label>
        <label className="campo"><span>Ventajas (español, una por línea)</span><textarea rows={5} value={f.incluyeEs} onChange={c('incluyeEs')} /></label>
        <label className="campo"><span>Ventajas (inglés, una por línea)</span><textarea rows={5} value={f.incluyeEn} onChange={c('incluyeEn')} /></label>
      </div>
      <div className="form-grid tres">
        <label className="campo"><span>Precio ({(plan?.moneda ?? 'usd').toUpperCase()})</span><input required inputMode="decimal" value={f.precio} onChange={c('precio')} placeholder="20.00" /></label>
        <label className="campo"><span>Cobro</span><select value={f.intervalo} onChange={c('intervalo')}><option value="mes">Mensual</option><option value="anio">Anual</option></select></label>
        <label className="campo"><span>Idiomas incluidos</span><input type="number" min={1} max={10} required value={f.idiomas} onChange={c('idiomas')} /></label>
        <label className="campo"><span>Orden</span><input type="number" min={0} value={f.orden} onChange={c('orden')} /></label>
        {!plan && <label className="campo"><span>Id (opcional)</span><input value={f.id} onChange={c('id')} placeholder="se genera del nombre" pattern="[a-z0-9][a-z0-9-]{0,39}" /></label>}
      </div>
      <div className="acciones">
        <label className="check-linea"><input type="checkbox" checked={f.visible} onChange={c('visible')} /> Visible en la app</label>
        <label className="check-linea"><input type="checkbox" checked={f.destacado} onChange={c('destacado')} /> Destacado</label>
      </div>
      {cambiaPrecio && pagos.disponible && <div className="verif aviso">Cambia el precio o el cobro: se creará un precio nuevo en Stripe para las nuevas suscripciones. Los {plan!.suscriptores} suscriptores actuales conservan el suyo.</div>}
      {err && <p className="err">{err}</p>}
      <div className="acciones">
        <button disabled={ocupado}>{ocupado ? 'Guardando…' : 'Guardar'}</button>
        <button type="button" className="sec" onClick={cancelar} disabled={ocupado}>Cancelar</button>
      </div>
    </form>
  )
}

function Ajustes({ a, alGuardar }: { a: Datos['ajustes']; alGuardar: () => void }) {
  const [min, setMin] = useState(String(a.pruebaMinutos)); const [moneda, setMoneda] = useState(a.moneda)
  const [msg, setMsg] = useState(''); const [ocupado, setOcupado] = useState(false)
  const guardar = async (e: React.FormEvent) => {
    e.preventDefault(); setOcupado(true); setMsg('')
    try { await api('/admin/pagos/ajustes', { metodo: 'PUT', cuerpo: { pruebaMinutos: Number(min), moneda } }); setMsg('Guardado.'); alGuardar() }
    catch (x: any) { setMsg(x.datos?.detalles?.join(' · ') || x.message) } finally { setOcupado(false) }
  }
  return (
    <form className="tarjeta conexion-form" onSubmit={guardar}>
      <h2>Prueba gratuita</h2>
      <div className="form-grid tres">
        <label className="campo"><span>Minutos de uso real</span><input type="number" min={0} max={10000} required value={min} onChange={(e) => setMin(e.target.value)} /></label>
        <label className="campo"><span>Moneda de los planes nuevos</span><input maxLength={3} required value={moneda} onChange={(e) => setMoneda(e.target.value.toLowerCase())} /></label>
      </div>
      <div className="acciones"><button disabled={ocupado}>{ocupado ? 'Guardando…' : 'Guardar'}</button>{msg && <span className="muted">{msg}</span>}</div>
      <p className="muted uso-nota">La app la recibe en <span className="mono">GET /planes</span> y en la suscripción del alumno. El tiempo usado nunca baja aunque la app mande menos.</p>
    </form>
  )
}

export default function Planes() {
  const [d, setD] = useState<Datos | null>(null)
  const [err, setErr] = useState(''); const [aviso, setAviso] = useState('')
  const [editando, setEditando] = useState<Plan | 'nuevo' | null>(null)
  const [ocupado, setOcupado] = useState('')
  const cargar = () => api<Datos>('/admin/planes').then((r) => { setD(r); setErr('') }).catch((x) => setErr(x.message))
  useEffect(() => { cargar() }, [])
  const accion = async (p: Plan, tipo: 'visible' | 'archivar' | 'sincronizar') => {
    if (tipo === 'archivar' && !p.archivado && !confirm(`¿Archivar «${p.nombre.es}»? Deja de ofrecerse; ${p.suscriptores} suscriptores lo conservan.`)) return
    setOcupado(p.id + tipo); setAviso('')
    try {
      const r = tipo === 'visible' ? await api(`/admin/planes/${p.id}`, { metodo: 'PUT', cuerpo: { visible: !p.visible } })
        : tipo === 'archivar' ? await api(`/admin/planes/${p.id}/archivar`, { metodo: 'POST', cuerpo: { archivado: !p.archivado } })
        : await api(`/admin/planes/${p.id}/sincronizar`, { metodo: 'POST' })
      if (r.sync && !r.sync.ok && d?.pagos.disponible) setAviso(`«${p.nombre.es}»: sin sincronizar con Stripe (${r.sync.error}).${avisoPortal(r.portal)}`)
      else if (r.portal && !r.portal.ok) setAviso(avisoPortal(r.portal).trim())
      await cargar()
    } catch (x: any) { setAviso(x.message) } finally { setOcupado('') }
  }
  if (err) return <p className="err">{err}</p>
  if (!d) return <p className="muted">Cargando…</p>
  const pendientes = d.planes.filter((p) => !p.archivado && p.stripe.estado === 'sin sincronizar').length
  return (
    <>
      <div className="cab"><h1>Planes</h1>{!editando && <button onClick={() => { setEditando('nuevo'); setAviso('') }}>Nuevo plan</button>}</div>
      <p className="muted pie-nota" style={{ margin: '-8px 0 16px' }}>
        {d.pagos.disponible
          ? <>Stripe vinculado <span className={`pill ${d.pagos.modo === 'live' ? 'ok' : 'trial'}`}>{d.pagos.modo === 'live' ? 'MODO REAL' : 'MODO TEST'}</span> · al guardar, cada plan se sincroniza con su producto y precio en Stripe.{pendientes > 0 && <b className="err"> {pendientes} sin sincronizar.</b>}</>
          : <>Stripe no está vinculado: la app muestra «Próximamente» en lugar de «Suscribirme». Vincúlalo en <b>Conexiones</b>; los planes se sincronizan solos.</>}
      </p>
      {aviso && <div className="verif aviso" style={{ marginBottom: 16 }}>{aviso}</div>}
      {editando && <Editor key={editando === 'nuevo' ? 'nuevo' : editando.id} plan={editando === 'nuevo' ? undefined : editando} pagos={d.pagos}
        orden={Math.max(0, ...d.planes.map((p) => p.orden)) + 1}
        alGuardar={(m) => { setEditando(null); setAviso(m); cargar() }} cancelar={() => setEditando(null)} />}
      <div className="tarjeta">
        <div className="desliza"><table>
          <thead><tr><th>Plan</th><th className="num">Precio</th><th className="num">Idiomas</th><th>En la app</th><th className="num">Suscriptores</th><th>Stripe</th><th></th></tr></thead>
          <tbody>{d.planes.map((p) => {
            const [clase, etq] = SYNC[p.stripe.estado]
            return <tr key={p.id} style={p.archivado ? { opacity: 0.6 } : undefined}>
              <td><b>{p.nombre.es}</b>{p.destacado && <> <span className="pill">Destacado</span></>}<br /><span className="muted">{p.nombre.en || '— sin inglés —'} · <span className="mono">{p.id}</span> · orden {p.orden}</span></td>
              <td className="num">{precio(p)}</td>
              <td className="num">{p.idiomas}</td>
              <td>{p.archivado ? <span className="pill mal">Archivado</span> : p.visible ? <span className="pill ok">Visible</span> : <span className="pill trial">Oculto</span>}</td>
              <td className="num">{p.suscriptores}</td>
              <td><span className={`pill ${clase}`} title={p.stripe.error ?? p.stripe.precioId ?? ''}>{etq}</span>
                {p.stripe.estado === 'sin sincronizar' && <button className="sec chico" disabled={!!ocupado} onClick={() => accion(p, 'sincronizar')}>{ocupado === p.id + 'sincronizar' ? 'Reintentando…' : 'Reintentar'}</button>}
                {p.stripe.error && p.stripe.estado === 'sin sincronizar' && <div className="err campo-err">{p.stripe.error}</div>}</td>
              <td className="num">
                <button className="sec chico" onClick={() => { setEditando(p); setAviso(''); window.scrollTo({ top: 0, behavior: 'smooth' }) }}>Editar</button>
                {!p.archivado && <button className="sec chico" disabled={!!ocupado} onClick={() => accion(p, 'visible')}>{p.visible ? 'Ocultar' : 'Mostrar'}</button>}
                <button className="sec chico" disabled={!!ocupado} onClick={() => accion(p, 'archivar')}>{p.archivado ? 'Restaurar' : 'Archivar'}</button>
              </td>
            </tr>
          })}</tbody>
        </table></div>
        <p className="muted pie-nota">Ocultar = no se ofrece en la app. Archivar = además se desactiva en Stripe; no hay borrado si alguien lo usa. Cambiar el precio crea un precio nuevo en Stripe y archiva el anterior: quien ya paga conserva su precio. Última edición: {fecha(d.planes.map((p) => p.actualizadoEn).sort().at(-1))}</p>
      </div>
      <Ajustes a={d.ajustes} alGuardar={cargar} />
    </>
  )
}
