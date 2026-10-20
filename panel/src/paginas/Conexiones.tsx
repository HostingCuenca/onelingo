import { useEffect, useState } from 'react'
import { api, ApiError, fecha, num, usd } from '../api'

type Verificacion = { ok: boolean; nivel: 'ok' | 'aviso' | 'error'; mensaje: string; detalles?: string[]; verificadoEn: string }
type Proveedor = {
  id: 'elevenlabs' | 'openai' | 'gemini'; nombre: string; uso: string; origen: 'panel' | 'servidor' | 'sin configurar'; claveOrigen: string
  clave: string | null; configurada: boolean; adminKey?: string | null; modelos: Record<string, string>
  campos: Record<string, { etiqueta: string; secreto: boolean }>; sugerencias: Record<string, string[]>
  ultimaVerificacion: Verificacion | null; actualizadoEn: string | null; avisos: string[]
}

const ORIGEN: Record<string, string> = { panel: 'Configurada desde el panel', servidor: 'Del servidor (.env)', 'sin configurar': 'Sin configurar' }
const ESTADO: Record<string, [string, string]> = { ok: ['ok', 'Verificada'], aviso: ['trial', 'Con avisos'], error: ['mal', 'Error'] }

/** Pasos para obtener cada clave (enlaces oficiales comprobados el 20-10-2026). */
const INSTRUCCIONES: Record<string, { pasos: React.ReactNode[]; formato: string }> = {
  elevenlabs: {
    formato: 'Empieza con sk_',
    pasos: [
      <>Entra en <a href="https://elevenlabs.io/app/developers/api-keys" target="_blank" rel="noreferrer">ElevenLabs → Developers → API Keys</a> con la cuenta que paga el plan.</>,
      <>Pulsa <b>Create API Key</b> y ponle un nombre (p. ej. «OneLingo servidor»).</>,
      <>Permisos (las claves vienen restringidas): <b>Text to Speech</b> = Access (obligatorio para generar audios), <b>User</b> = Read/Access (para ver aquí el consumo), y <b>Voices</b> y <b>Models</b> = Read (recomendado, para comprobar el modelo).</>,
      <>Copia la clave (solo se muestra una vez), pégala aquí y pulsa <b>Verificar</b> y luego <b>Guardar</b>.</>,
    ],
  },
  openai: {
    formato: 'Empieza con sk-proj- (Admin key: sk-admin-)',
    pasos: [
      <>Entra en <a href="https://platform.openai.com/api-keys" target="_blank" rel="noreferrer">OpenAI Platform → API keys</a> con la organización que paga.</>,
      <>Pulsa <b>Create new secret key</b>, elige el proyecto de OneLingo y permisos <b>All</b>. Copia la clave (solo se muestra una vez).</>,
      <>Comprueba que hay saldo en <a href="https://platform.openai.com/settings/organization/billing/overview" target="_blank" rel="noreferrer">Settings → Billing</a>: sin saldo la clave es válida pero el tutor falla con «insufficient_quota».</>,
      <>Costo real (opcional): el Owner de la organización crea una clave en <a href="https://platform.openai.com/settings/organization/admin-keys" target="_blank" rel="noreferrer">Settings → Organization → Admin keys</a> y la pega en «Admin key». Solo se usa para leer costos.</>,
    ],
  },
  gemini: {
    formato: 'Empieza con AIza o, las nuevas, con AQ.',
    pasos: [
      <>Entra en <a href="https://aistudio.google.com/apikey" target="_blank" rel="noreferrer">Google AI Studio → API keys</a>.</>,
      <>Pulsa <b>Create API key</b> y elige el proyecto de Google Cloud (si no aparece: Dashboard → Projects → Import projects).</>,
      <>Copia la clave y pégala aquí. Si la verificación responde 403 «denied access» o PERMISSION_DENIED, ese proyecto no tiene acceso a la Gemini API: revisa el proyecto y su facturación en AI Studio o crea la clave en otro proyecto.</>,
      <>El consumo se ve en <a href="https://aistudio.google.com/usage" target="_blank" rel="noreferrer">Google AI Studio → Usage</a> (Google no lo ofrece por API).</>,
    ],
  },
}

function Resultado({ v, titulo }: { v: Verificacion; titulo?: string }) {
  const [clase, etiqueta] = ESTADO[v.nivel]
  return (
    <div className={`verif ${v.nivel}`}>
      <div><span className={`pill ${clase}`}>{titulo ?? etiqueta}</span> {v.mensaje}</div>
      {v.detalles && <ul>{v.detalles.map((d, i) => <li key={i}>{d}</li>)}</ul>}
      <div className="muted cuando">{fecha(v.verificadoEn)}</div>
    </div>
  )
}

function Consumo({ id, c }: { id: string; c: any }) {
  if (!c) return <p className="muted">Cargando consumo…</p>
  if (id === 'elevenlabs') {
    const q = c.cuota
    const pct = q && q.limite ? Math.min(100, Math.round((q.usados / q.limite) * 100)) : 0
    return <>
      {q ? <>
        <div className="uso-fila"><b>{num(q.usados)}</b> de {num(q.limite)} caracteres · {pct} % <span className="pill ok">real</span></div>
        <div className="barra"><i style={{ width: `${pct}%`, background: pct > 90 ? 'var(--rojo)' : pct > 70 ? 'var(--naranja)' : undefined }} /></div>
        <div className="muted uso-nota">Plan {q.plan}{q.reinicio ? ` · se renueva el ${fecha(q.reinicio)}` : ''}</div>
      </> : <p className="muted uso-nota">{c.nota}</p>}
      {c.onelingo && <div className="muted uso-nota">OneLingo este mes: {num(c.onelingo.audios_mes)} audios nuevos, {num(c.onelingo.caracteres_mes)} caracteres (≈ {usd(c.onelingo.costeMesEstimado)} estimado). Los audios repetidos salen de la caché sin gastar cuota.</div>}
    </>
  }
  if (id === 'openai') {
    if (c.tipo === 'real') return <>
      <div className="uso-fila"><b>{usd(c.costeMes)}</b> este mes <span className="pill ok">real</span></div>
      {c.porConcepto?.length > 0 && <table><tbody>{c.porConcepto.slice(0, 6).map((x: any) => <tr key={x.concepto}><td>{x.concepto}</td><td className="num">{usd(x.coste)}</td></tr>)}</tbody></table>}
    </>
    return <>
      <div className="uso-fila"><b>{usd(c.estimado?.coste ?? 0)}</b> este mes <span className="pill trial">estimado</span> · {num(c.estimado?.conversaciones ?? 0)} turnos del tutor</div>
      <div className="muted uso-nota">{c.nota}</div>
    </>
  }
  return <>
    {c.tipo === 'estimado' && <div className="uso-fila"><b>{usd(c.estimado.coste)}</b> este mes <span className="pill trial">estimado</span> · {num(c.estimado.conversaciones)} turnos</div>}
    <div className="muted uso-nota">{c.nota} {c.enlace && <a href={c.enlace} target="_blank" rel="noreferrer">Abrir Google AI Studio</a>}</div>
  </>
}

function Tarjeta({ p, consumo, alCambiar }: { p: Proveedor; consumo: any; alCambiar: () => void }) {
  const vacio = () => Object.fromEntries(Object.keys(p.campos).map((k) => [k, p.campos[k].secreto ? '' : p.modelos[k] ?? '']))
  const [form, setForm] = useState<Record<string, string>>(vacio)
  const [ver, setVer] = useState<Record<string, boolean>>({})
  const [ocupado, setOcupado] = useState<'' | 'verificar' | 'guardar' | 'volver'>('')
  const [errores, setErrores] = useState<Record<string, string>>({})
  const [res, setRes] = useState<{ v?: Verificacion; error?: string; guardado?: boolean; avisos?: string[] } | null>(null)
  const [quitarAdmin, setQuitarAdmin] = useState(false)
  useEffect(() => { setForm(vacio()) }, [p.actualizadoEn, p.origen]) // eslint-disable-line react-hooks/exhaustive-deps

  const cuerpo = () => {
    const c: Record<string, unknown> = {}
    for (const [k, def] of Object.entries(p.campos)) {
      const v = form[k] ?? ''
      if (def.secreto ? v.trim() : v.trim() && v.trim() !== p.modelos[k]) c[k] = v
    }
    if (quitarAdmin) c.quitarAdminKey = true
    return c
  }
  const enviar = async (accion: 'verificar' | 'guardar') => {
    setOcupado(accion); setErrores({}); setRes(null)
    try {
      const r = accion === 'verificar'
        ? await api(`/admin/conexiones/${p.id}/verificar`, { metodo: 'POST', cuerpo: cuerpo() })
        : await api(`/admin/conexiones/${p.id}`, { metodo: 'PUT', cuerpo: cuerpo() })
      setRes({ v: r.verificacion, guardado: accion === 'guardar', avisos: r.avisos })
      if (accion === 'guardar') { setQuitarAdmin(false); alCambiar() }
    } catch (x: any) {
      const d = x instanceof ApiError ? x.datos : null
      if (d?.errores) setErrores(d.errores)
      setRes({ v: d?.verificacion, error: d?.errores ? undefined : x.message, avisos: d?.avisos })
    } finally { setOcupado('') }
  }
  const volver = async () => {
    if (!confirm(`¿Volver a la configuración del servidor para ${p.nombre}? Se borra lo guardado en el panel y se usa la clave del .env.`)) return
    setOcupado('volver'); setRes(null)
    try { await api(`/admin/conexiones/${p.id}`, { metodo: 'DELETE' }); alCambiar() }
    catch (x: any) { setRes({ error: x.message }) } finally { setOcupado('') }
  }

  const uv = p.ultimaVerificacion
  const [clase, etiqueta] = uv ? ESTADO[uv.nivel] : ['', p.configurada ? 'Sin verificar' : 'Sin clave']
  const ins = INSTRUCCIONES[p.id]
  return (
    <div className="tarjeta conexion">
      <div className="conexion-cab">
        <div><h2>{p.nombre}</h2><div className="muted">{p.uso}</div></div>
        <span className={`semaforo ${uv?.nivel ?? (p.configurada ? '' : 'error')}`} title={etiqueta} />
      </div>
      <div className="conexion-estado">
        <span className={`pill ${clase}`}>{etiqueta}</span>
        <span className="pill">{ORIGEN[p.origen]}</span>
        {p.clave && <span className="mono">{p.clave}</span>}
        {p.origen === 'panel' && p.claveOrigen === 'servidor' && <span className="muted">(clave del servidor, modelos del panel)</span>}
      </div>
      {uv && <div className="muted ult">Última verificación {fecha(uv.verificadoEn)}: {uv.mensaje}</div>}
      {p.actualizadoEn && <div className="muted ult">Guardada en el panel el {fecha(p.actualizadoEn)}</div>}
      {p.avisos.map((a, i) => <div key={i} className="verif aviso">{a}</div>)}

      <h3 className="seccion">Consumo</h3>
      <Consumo id={p.id} c={consumo} />

      <h3 className="seccion">Cambiar</h3>
      <form className="conexion-form" onSubmit={(e) => { e.preventDefault(); enviar('guardar') }}>
        {Object.entries(p.campos).map(([k, def]) => (
          <label key={k} className="campo">
            <span>{def.etiqueta}</span>
            {def.secreto ? (
              <div className="clave-input">
                <input type={ver[k] ? 'text' : 'password'} value={form[k] ?? ''} autoComplete="off" spellCheck={false}
                  placeholder={(k === 'adminKey' ? p.adminKey : p.clave) ? `Vacío = conservar ${k === 'adminKey' ? p.adminKey : p.clave}` : `Pega aquí la clave (${ins.formato.toLowerCase()})`}
                  onChange={(e) => setForm({ ...form, [k]: e.target.value })} aria-invalid={!!errores[k]} />
                <button type="button" className="sec chico" onClick={() => setVer({ ...ver, [k]: !ver[k] })}>{ver[k] ? 'Ocultar' : 'Mostrar'}</button>
              </div>
            ) : (
              <>
                <input list={`sug-${p.id}-${k}`} value={form[k] ?? ''} onChange={(e) => setForm({ ...form, [k]: e.target.value })} aria-invalid={!!errores[k]} />
                <datalist id={`sug-${p.id}-${k}`}>{(p.sugerencias[k] ?? []).map((s) => <option key={s} value={s} />)}</datalist>
              </>
            )}
            {errores[k] && <span className="err campo-err">{errores[k]}</span>}
            {k === 'adminKey' && p.adminKey && <span className="check"><input type="checkbox" checked={quitarAdmin} onChange={(e) => setQuitarAdmin(e.target.checked)} /> Quitar la Admin key guardada</span>}
          </label>
        ))}
        <div className="acciones">
          <button type="button" className="sec" disabled={!!ocupado} onClick={() => enviar('verificar')}>{ocupado === 'verificar' ? 'Verificando…' : 'Verificar'}</button>
          <button type="submit" disabled={!!ocupado}>{ocupado === 'guardar' ? 'Verificando y guardando…' : 'Guardar'}</button>
          {p.origen === 'panel' && <button type="button" className="sec" disabled={!!ocupado} onClick={volver}>{ocupado === 'volver' ? 'Restaurando…' : 'Volver a la configuración del servidor'}</button>}
        </div>
      </form>
      {res?.error && <p className="err">{res.error}</p>}
      {res?.avisos?.map((a, i) => <p key={i} className="muted">{a}</p>)}
      {res?.v && <Resultado v={res.v} titulo={res.guardado ? 'Guardada y aplicada' : res.v.nivel === 'error' ? 'No válida' : undefined} />}
      {res?.v && res.v.nivel === 'error' && !res.guardado && <p className="muted uso-nota">No se guardó nada: la configuración actual sigue funcionando.</p>}

      <details className="instr">
        <summary>¿Cómo obtengo la clave?</summary>
        <ol>{ins.pasos.map((x, i) => <li key={i}>{x}</li>)}</ol>
        <p className="muted">Al guardar, la clave se aplica al instante en el servidor, sin reiniciar. Los audios ya generados se conservan (están en caché). Si algo falla, «Volver a la configuración del servidor» recupera la del .env.</p>
      </details>
    </div>
  )
}

export default function Conexiones() {
  const [d, setD] = useState<{ iaProveedor: string; proveedores: Proveedor[] } | null>(null)
  const [consumo, setConsumo] = useState<any>(null)
  const [err, setErr] = useState('')
  const cargar = () => api('/admin/conexiones').then(setD).catch((x) => setErr(x.message))
  const cargarConsumo = () => api('/admin/conexiones/consumo').then(setConsumo).catch(() => setConsumo({}))
  useEffect(() => { cargar(); cargarConsumo() }, [])
  if (err) return <p className="err">{err}</p>
  if (!d) return <p className="muted">Cargando…</p>
  return (
    <>
      <div className="cab"><h1>Conexiones</h1><span className="muted">Tutor IA en uso: {d.iaProveedor}{consumo?.mes ? ` · consumo de ${consumo.mes}` : ''}</span></div>
      <p className="muted pie-nota" style={{ margin: '-8px 0 16px' }}>Claves y modelos de los proveedores externos. Cada clave se comprueba con el proveedor antes de guardarse; se guarda cifrada y tiene prioridad sobre el .env del servidor.</p>
      <div className="conexiones">
        {d.proveedores.map((p) => <Tarjeta key={p.id} p={p} consumo={consumo?.[p.id]} alCambiar={() => { cargar(); cargarConsumo() }} />)}
      </div>
    </>
  )
}
