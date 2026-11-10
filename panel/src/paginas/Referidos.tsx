import { useEffect, useState } from 'react'
import { api, fecha, hace, IDIOMAS, num } from '../api'
import ErrorCarga from '../ErrorCarga'

type Codigo = { codigo: string; vendedor: string; nota: string; activo: boolean; creadoEn: string; registrados: number; pagando: number; pagaronAlgunaVez: number; mensual: number; ultimo: string | null }
type Alumno = { id: string; nombre: string; apellido: string; email: string; idiomaMeta: string; registro: string; referidoEn: string | null; plan: string | null; origen: string | null; estado: string | null; pagando: boolean }
type Detalle = Omit<Codigo, 'registrados' | 'pagando' | 'pagaronAlgunaVez' | 'mensual' | 'ultimo'> & { alumnos: Alumno[] }

const dolares = (v: number) => `$${v.toLocaleString('es', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`

/**
 * Referidos: un código por vendedor. El alumno lo escribe al crear su cuenta (o
 * después, una vez) y aquí se ve quién trajo a quién y quién paga. Solo
 * seguimiento: no aplica descuentos ni premios.
 */
export default function Referidos({ abrirAlumno }: { abrirAlumno: (id: string) => void }) {
  const [d, setD] = useState<{ codigos: Codigo[]; sinCodigo: number } | null>(null)
  const [err, setErr] = useState(''); const [abierto, setAbierto] = useState<Detalle | null>(null)
  const [nuevo, setNuevo] = useState({ vendedor: '', codigo: '', nota: '' }); const [msg, setMsg] = useState(''); const [ocupado, setOcupado] = useState(false)
  const cargar = () => api<{ codigos: Codigo[]; sinCodigo: number }>('/admin/referidos').then((r) => { setD(r); setErr('') }).catch((x) => setErr(x.message))
  useEffect(() => { cargar() }, [])
  const abrir = (c: string) => api<Detalle>(`/admin/referidos/${encodeURIComponent(c)}`).then((r) => { setAbierto(r); setMsg('') }).catch((x) => setMsg(x.message))
  const crear = async (e: React.FormEvent) => {
    e.preventDefault(); setOcupado(true); setMsg('')
    try {
      const r = await api<{ codigo: string }>('/admin/referidos', { metodo: 'POST', cuerpo: nuevo })
      setNuevo({ vendedor: '', codigo: '', nota: '' }); await cargar(); await abrir(r.codigo); setMsg(`Código ${r.codigo} creado. Compártelo con el vendedor.`)
    } catch (x: any) { setMsg(x.message) } finally { setOcupado(false) }
  }
  const activar = async (c: Detalle) => {
    setOcupado(true)
    try { await api(`/admin/referidos/${encodeURIComponent(c.codigo)}`, { metodo: 'PATCH', cuerpo: { activo: !c.activo } }); await cargar(); await abrir(c.codigo) }
    catch (x: any) { setMsg(x.message) } finally { setOcupado(false) }
  }
  if (err) return <ErrorCarga msg={err} reintentar={() => { setErr(''); cargar() }} />
  const tot = d?.codigos.reduce((a, c) => ({ r: a.r + c.registrados, p: a.p + c.pagando, m: a.m + c.mensual }), { r: 0, p: 0, m: 0 })
  return (
    <>
      <div className="cab"><h1>Referidos</h1></div>
      <p className="muted pie-nota" style={{ margin: '-8px 0 16px' }}>Crea un código para cada vendedor. El alumno lo escribe al crear su cuenta en la app (campo «Código de referido») o después en su perfil, una sola vez. Aquí ves cuántos registró cada uno y cuántos pagan. No aplica descuentos ni premios automáticos.</p>
      {d && tot && <div className="kpis">
        <div className="kpi"><div className="v">{num(tot.r)}</div><div className="l">Registrados con código</div></div>
        <div className="kpi"><div className="v">{num(tot.p)}</div><div className="l">Pagando ahora</div></div>
        <div className="kpi"><div className="v">{dolares(tot.m)}</div><div className="l">Ingreso mensual</div><div className="nota">de los referidos que pagan</div></div>
        <div className="kpi"><div className="v">{num(d.sinCodigo)}</div><div className="l">Alumnos sin código</div></div>
      </div>}
      <div className="grid2">
        <div className="tarjeta">
          {!d ? <p className="muted">Cargando…</p> : d.codigos.length === 0 ? <p className="muted">Todavía no hay códigos. Crea el primero con el formulario.</p> :
            <div className="desliza"><table>
              <thead><tr><th>Código</th><th>Vendedor</th><th className="num">Registrados</th><th className="num">Pagando</th><th className="num">Mensual</th><th>Último</th></tr></thead>
              <tbody>{d.codigos.map((c) => <tr key={c.codigo} className="click" onClick={() => abrir(c.codigo)}>
                <td className="mono"><b>{c.codigo}</b>{!c.activo && <> <span className="pill">inactivo</span></>}</td>
                <td>{c.vendedor}</td>
                <td className="num">{num(c.registrados)}</td>
                <td className="num">{num(c.pagando)}</td>
                <td className="num">{dolares(c.mensual)}</td>
                <td>{hace(c.ultimo)}</td>
              </tr>)}</tbody>
            </table></div>}
        </div>
        <div className="tarjeta">
          {abierto ? <>
            <h2 className="mono">{abierto.codigo}</h2>
            <p>{abierto.vendedor}{abierto.nota && <span className="muted"> · {abierto.nota}</span>}</p>
            <p className="muted">Creado {fecha(abierto.creadoEn)} · {abierto.activo ? <span className="pill ok">activo</span> : <span className="pill">inactivo: la app ya no lo acepta</span>}</p>
            <div style={{ display: 'flex', gap: 8, margin: '8px 0 14px', flexWrap: 'wrap' }}>
              <button className="sec" disabled={ocupado} onClick={() => activar(abierto)}>{abierto.activo ? 'Desactivar' : 'Activar'}</button>
              <button className="sec" onClick={() => { setAbierto(null); setMsg('') }}>Nuevo código</button>
            </div>
            {abierto.alumnos.length === 0 ? <p className="muted">Nadie ha usado este código todavía.</p> :
              <div className="desliza"><table>
                <thead><tr><th>Alumno</th><th>Idioma</th><th>Plan</th><th>Con código desde</th></tr></thead>
                <tbody>{abierto.alumnos.map((a) => <tr key={a.id} className="click" onClick={() => abrirAlumno(a.id)}>
                  <td><b>{[a.nombre, a.apellido].filter(Boolean).join(' ')}</b><br /><span className="muted mono">{a.email}</span></td>
                  <td>{IDIOMAS[a.idiomaMeta] ?? a.idiomaMeta}</td>
                  <td>{a.pagando ? <span className="pill ok">{a.plan} · {a.origen === 'google' ? 'Google Play' : 'Stripe'}</span> : a.plan ? <span className="pill">{a.plan} · {a.estado}</span> : <span className="muted">gratis / prueba</span>}</td>
                  <td>{fecha(a.referidoEn)}</td>
                </tr>)}</tbody>
              </table></div>}
          </> : <form onSubmit={crear} style={{ display: 'grid', gap: 10 }}>
            <h2>Nuevo código</h2>
            <label className="campo"><span>Vendedor</span><input value={nuevo.vendedor} onChange={(e) => setNuevo({ ...nuevo, vendedor: e.target.value })} placeholder="Nombre de quien vende" required /></label>
            <label className="campo"><span>Código</span><input value={nuevo.codigo} onChange={(e) => setNuevo({ ...nuevo, codigo: e.target.value.toUpperCase() })} placeholder="Opcional: si lo dejas vacío se arma con el nombre" className="mono" /></label>
            <label className="campo"><span>Nota</span><input value={nuevo.nota} onChange={(e) => setNuevo({ ...nuevo, nota: e.target.value })} placeholder="Opcional: zona, comisión acordada…" /></label>
            <button disabled={ocupado || !nuevo.vendedor.trim()}>{ocupado ? 'Creando…' : 'Crear código'}</button>
          </form>}
          {msg && <p className="muted" style={{ marginTop: 10 }}>{msg}</p>}
        </div>
      </div>
    </>
  )
}
