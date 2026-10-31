import { useEffect, useState } from 'react'
import { api, ESTADOS, fecha, hace, IDIOMAS, minutos, nivelCorto, num, PLATAFORMAS, SKILLS, usd } from '../api'
import ErrorCarga from '../ErrorCarga'

const lista = (v: unknown) => (Array.isArray(v) ? v.join(', ') : typeof v === 'object' && v ? Object.keys(v).join(', ') : String(v ?? ''))

/** Suscripción del alumno y cortesía (acceso sin pago dado por el administrador). */
const CODIGOS = ['en', 'fr', 'es', 'pt', 'de', 'it', 'zh', 'ja', 'ru', 'ko']

/** Chips para elegir idiomas; el orden de selección cuenta (al bajar de plan se conservan los primeros). */
function SelectorIdiomas({ valor, max, onChange }: { valor: string[]; max: number; onChange: (v: string[]) => void }) {
  return (
    <div className="chips">
      {CODIGOS.map((c) => {
        const i = valor.indexOf(c)
        return <button type="button" key={c} className={`chip ${i >= 0 ? 'si' : ''}`} disabled={i < 0 && valor.length >= max}
          onClick={() => onChange(i >= 0 ? valor.filter((x) => x !== c) : [...valor, c])}>{IDIOMAS[c] ?? c}{i >= 0 && <span className="n">{i + 1}</span>}</button>
      })}
    </div>
  )
}

const REGLAS: Record<string, string> = { libre: 'cambio libre', uno_por_periodo: 'un cambio por periodo', solo_admin: 'solo desde el panel' }

function Suscripcion({ id, s, alCambiar }: { id: string; s: any; alCambiar: () => void }) {
  const [planes, setPlanes] = useState<{ id: string; nombre: { es: string }; archivado: boolean; idiomas: number }[]>([])
  const [plan, setPlan] = useState(''); const [hasta, setHasta] = useState(''); const [nota, setNota] = useState('')
  const [modoIdiomas, setModoIdiomas] = useState<'meta' | 'lista' | 'todos'>('meta'); const [lista, setLista] = useState<string[]>([])
  const [editando, setEditando] = useState(false); const [nuevos, setNuevos] = useState<string[]>([])
  const [msg, setMsg] = useState(''); const [ocupado, setOcupado] = useState(false)
  const nPlanCortesia = planes.find((p) => p.id === plan)?.idiomas ?? 1
  const guardarIdiomas = async () => {
    setOcupado(true); setMsg('')
    try { await api(`/admin/usuarios/${id}/suscripcion/idiomas`, { metodo: 'PUT', cuerpo: { idiomas: nuevos } }); setEditando(false); alCambiar() }
    catch (x: any) { setMsg(x.message) } finally { setOcupado(false) }
  }
  useEffect(() => { api('/admin/planes').then((r) => { const l = r.planes.filter((p: any) => !p.archivado); setPlanes(l); setPlan((x) => x || l[0]?.id || '') }).catch(() => {}) }, [])
  const [clase, etq] = ESTADOS[s.estado] ?? ['', s.estado]
  const enStripe = s.origen === 'stripe' && ['activa', 'prueba_stripe', 'impago'].includes(s.estado)
  const dar = async (e: React.FormEvent) => {
    e.preventDefault(); setOcupado(true); setMsg('')
    try {
      const idiomas = nPlanCortesia === 0 ? undefined : modoIdiomas === 'todos' ? 'todos' : modoIdiomas === 'lista' ? lista : undefined
      await api(`/admin/usuarios/${id}/cortesia`, { metodo: 'POST', cuerpo: { planId: plan, idiomas, hasta: hasta ? new Date(`${hasta}T23:59:59`).toISOString() : null, nota } })
      setHasta(''); setNota(''); setLista([]); setModoIdiomas('meta'); alCambiar()
    } catch (x: any) { setMsg(x.datos?.detalles?.join(' · ') || x.message) } finally { setOcupado(false) }
  }
  const quitar = async () => {
    if (!confirm('¿Quitar la cortesía? El alumno pierde el acceso del plan.')) return
    setOcupado(true); setMsg('')
    try { await api(`/admin/usuarios/${id}/cortesia`, { metodo: 'DELETE' }); alCambiar() } catch (x: any) { setMsg(x.message) } finally { setOcupado(false) }
  }
  return (
    <div className="tarjeta">
      <h2>Suscripción</h2>
      <div className="conexion-estado" style={{ marginTop: 0 }}>
        <span className={`pill ${clase}`}>{etq}</span>
        {s.origen && <span className="pill">{s.origen === 'cortesia' ? 'Cortesía' : 'Stripe'}</span>}
        {s.modo && <span className={`pill ${s.modo === 'live' ? 'ok' : 'trial'}`}>{s.modo === 'live' ? 'MODO REAL' : 'MODO TEST'}</span>}
        <span className={`pill ${s.accesoPlan ? 'ok' : 'mal'}`}>{s.accesoPlan ? 'Con acceso' : 'Sin acceso'}</span>
        {s.accesoPlan && !s.acceso && <span className="pill trial">{IDIOMAS[s.idiomaMeta] ?? s.idiomaMeta} (idioma actual) en prueba</span>}
      </div>
      <div className="sus-datos">
        <div><div className="l">Plan</div><b>{s.planId || s.filaPlanId || '—'}</b></div>
        <div><div className="l">{s.cancelaAlFinal ? 'Se cancela el' : s.origen === 'cortesia' ? 'Hasta' : 'Periodo hasta'}</div>{s.periodoFin ? fecha(s.periodoFin) : s.origen === 'cortesia' ? 'Sin fecha' : '—'}</div>
        <div><div className="l">Prueba gratuita</div>{minutos(s.prueba.segundosUsados)} de {s.prueba.minutos} min{s.prueba.agotada ? ' · agotada' : ''}</div>
        {s.stripeClienteId && <div><div className="l">Cliente de Stripe</div><span className="mono">{s.stripeClienteId}</span></div>}
      </div>
      {s.idiomasPlan !== null && s.idiomasPlan !== undefined && <div style={{ margin: '4px 0 8px' }}>
        <div className="muted" style={{ fontSize: 12, marginBottom: 4 }}>Idiomas de pago{s.idiomasPlan > 0 ? ` (el plan incluye ${s.idiomasPlan})` : ''} · {REGLAS[s.cambioIdiomas?.regla] ?? ''}
          {s.cambioIdiomas?.proximoCambio ? ` · próximo cambio del alumno: ${fecha(s.cambioIdiomas.proximoCambio)}` : ''}</div>
        {editando ? <>
          <SelectorIdiomas valor={nuevos} max={s.idiomasPlan} onChange={setNuevos} />
          <div className="acciones"><button type="button" disabled={ocupado || nuevos.length === 0} onClick={guardarIdiomas}>{ocupado ? 'Guardando…' : 'Guardar idiomas'}</button>
            <button type="button" className="sec" onClick={() => setEditando(false)}>Cancelar</button>
            <span className="muted">{nuevos.length} de {s.idiomasPlan}. Sin aplicar la regla de cambios del alumno.</span></div>
        </> : <div className="chips">
          {s.todosLosIdiomas ? <span className="pill ok">Todos los idiomas</span> : s.idiomas.map((c: string) => <span key={c} className={`pill ${s.accesoPlan ? 'ok' : ''}`}>{IDIOMAS[c] ?? c}</span>)}
          {s.idiomasPorElegir > 0 && <span className="pill trial">{s.idiomasPorElegir} por elegir</span>}
          {!s.todosLosIdiomas && s.idiomasPlan > 0 && <button type="button" className="chip" onClick={() => { setNuevos(s.idiomas); setEditando(true) }}>Editar idiomas</button>}
        </div>}
      </div>}
      {s.nota && <p className="muted uso-nota">Nota: {s.nota}</p>}
      {s.origen === 'cortesia' && <div className="acciones"><button className="sec" disabled={ocupado} onClick={quitar}>Quitar cortesía</button></div>}
      {enStripe ? <p className="muted uso-nota">Paga con Stripe: los cambios (cancelar, tarjeta) se hacen en el portal del alumno o en el Dashboard de Stripe.</p> : (
        <form className="conexion-form" onSubmit={dar} style={{ marginTop: 12 }}>
          <h3 className="seccion" style={{ margin: '4px 0 0' }}>{s.origen === 'cortesia' ? 'Cambiar cortesía' : 'Dar cortesía'}</h3>
          <div className="form-grid tres">
            <label className="campo"><span>Plan</span><select value={plan} onChange={(e) => setPlan(e.target.value)} required>{planes.map((p) => <option key={p.id} value={p.id}>{p.nombre.es} ({p.id})</option>)}</select></label>
            <label className="campo"><span>Hasta (vacío = sin fecha)</span><input type="date" value={hasta} min={new Date().toISOString().slice(0, 10)} onChange={(e) => setHasta(e.target.value)} /></label>
            <label className="campo"><span>Nota</span><input maxLength={500} value={nota} onChange={(e) => setNota(e.target.value)} placeholder="Beca, socio, prueba…" /></label>
          </div>
          {nPlanCortesia === 0 ? <p className="muted uso-nota">Este plan incluye todos los idiomas.</p> : <>
            <label className="campo" style={{ maxWidth: 320 }}><span>Idiomas</span><select value={modoIdiomas} onChange={(e) => setModoIdiomas(e.target.value as any)}>
              <option value="meta">El que aprende ahora ({IDIOMAS[s.idiomaMeta] ?? s.idiomaMeta})</option>
              <option value="lista">Elegir (hasta {nPlanCortesia})</option>
              <option value="todos">Todos los idiomas</option>
            </select></label>
            {modoIdiomas === 'lista' && <SelectorIdiomas valor={lista.slice(0, nPlanCortesia)} max={nPlanCortesia} onChange={setLista} />}
          </>}
          <div className="acciones"><button disabled={ocupado || !plan}>{ocupado ? 'Guardando…' : 'Dar acceso'}</button></div>
        </form>
      )}
      {msg && <p className="err">{msg}</p>}
    </div>
  )
}

export default function UsuarioDetalle({ id, volver, desde = 'usuarios' }: { id: string; volver: () => void; desde?: 'usuarios' | 'suscripciones' | 'reportes' }) {
  const [d, setD] = useState<any>(null)
  const [err, setErr] = useState('')
  const cargar = () => api(`/admin/usuarios/${id}`).then(setD).catch((e) => setErr(e.message))
  useEffect(() => { cargar() }, [id]) // eslint-disable-line react-hooks/exhaustive-deps
  if (err) return <ErrorCarga msg={err} reintentar={() => { setErr(''); cargar() }} />
  if (!d) return <p className="muted">Cargando…</p>
  const u = d.usuario, p = d.progreso, e = p?.estado ?? {}
  const g = e.diagnostico
  const nivelMax = Math.max(-1, ...(d.progresoIdiomas.find((x: any) => x.idioma === u.idioma_meta)?.niveles ?? []).filter((n: any) => n.clases > 0).map((n: any) => n.nivel))
  return (
    <>
      <div className="cab"><div><span className="volver" onClick={volver}>← {desde === 'suscripciones' ? 'Suscripciones' : desde === 'reportes' ? 'Reportes IA' : 'Alumnos'}</span><h1>{[u.nombre, u.apellido].filter(Boolean).join(' ')}</h1>
        <span className="muted mono">{u.email}{u.email_verificado ? ' ✓ verificado' : ' · sin verificar'}{u.telefono ? ` · ${u.telefono}` : ''} · {PLATAFORMAS[u.plataforma || 'desconocida'] ?? u.plataforma} · registrado {fecha(u.creado_en)} · activo {hace(u.ultima_actividad)}</span></div>
        <div>{d.suscripcion.accesoPlan ? <span className="pill ok">Plan {d.suscripcion.planId}</span> : <span className="pill trial">Prueba gratuita · {Math.round(d.suscripcion.prueba.restanteSegundos / 60)} min</span>}</div></div>
      <div className="kpis">
        <div className="kpi"><div className="v">{IDIOMAS[u.idioma_meta] ?? u.idioma_meta}</div><div className="l">Aprende</div><div className="nota">nativo: {IDIOMAS[u.idioma_nativo] ?? u.idioma_nativo}</div></div>
        <div className="kpi"><div className="v">{d.clases}</div><div className="l">Clases completadas</div>{d.legado > 0 && <div className="nota">{d.legado} del temario antiguo</div>}</div>
        <div className="kpi"><div className="v">{nivelMax >= 0 ? nivelCorto(nivelMax) : '—'}</div><div className="l">Nivel más alto con clases</div></div>
        <div className="kpi"><div className="v">{p?.xp ?? 0}</div><div className="l">XP</div><div className="nota">racha {p?.racha ?? 0} d</div></div>
        <div className="kpi"><div className="v">{minutos(p?.segundos_estudio ?? 0)}</div><div className="l">Estudio</div></div>
        <div className="kpi"><div className="v">{d.ia.conversaciones}</div><div className="l">Turnos con tutor IA</div><div className="nota">{num(d.ia.entrada + d.ia.salida)} tokens · {usd(d.ia.coste)}</div></div>
      </div>

      <Suscripcion id={id} s={d.suscripcion} alCambiar={cargar} />
      <div className="grid2">
        <div className="tarjeta"><h2>Progreso por idioma y nivel</h2>
          {d.progresoIdiomas.map((pi: any) => <div key={pi.idioma} style={{ marginBottom: 12 }}>
            <b>{IDIOMAS[pi.idioma] ?? pi.idioma}</b> <span className="muted">· {pi.total} clases</span>{' '}
            {d.suscripcion.accesoPorIdioma?.[pi.idioma] ? <span className="pill ok">De pago</span> : <span className="pill trial">Prueba</span>}
            <table><tbody>{pi.niveles.filter((n: any) => n.clases > 0 || n.nivel <= Math.max(1, nivelMax)).map((n: any) => <tr key={n.nivel}>
              <td style={{ width: 50 }}>{nivelCorto(n.nivel)}</td>
              <td><div className="barra"><i style={{ width: `${n.publicadas ? Math.min(100, (n.clases / n.publicadas) * 100) : n.clases ? 100 : 0}%` }} /></div></td>
              <td className="num" style={{ width: 80 }}>{n.clases}{n.publicadas ? ` / ${n.publicadas}` : ''}</td>
              <td className="num" style={{ width: 90 }}>{(() => { const ex = d.examenes.find((x: any) => x.nivel === n.nivel); return ex ? <span className={`pill ${ex.aprobado ? 'ok' : 'mal'}`}>Examen {ex.pct} %</span> : null })()}</td></tr>)}</tbody></table>
          </div>)}
          {d.progresoIdiomas.length === 0 && <p className="muted">Todavía no ha completado ninguna clase.</p>}
        </div>
        <div className="tarjeta"><h2>Prueba de ubicación</h2>
          {d.ubicacion.map((x: any, i: number) => { const v = x.datos ?? {}; return <div key={i} className="bloque-err">
            <div><b>{IDIOMAS[v.idioma] ?? v.idioma ?? '—'}</b> · nivel elegido <b>{v.nivelElegido ?? '—'}</b> (estimado {v.nivelEstimado ?? '—'}{v.cefr ? `, ${v.cefr}` : ''}) <span className="muted">· {fecha(x.fecha)}</span></div>
            <div className="muted">{v.preguntas !== undefined ? `${v.preguntas} preguntas` : ''}{v.precision !== undefined ? ` · ${v.precision} % de precisión` : v.aciertos !== undefined ? ` · ${v.aciertos} aciertos` : ''}{v.debilidades ? ` · reforzar: ${lista(v.debilidades)}` : ''}</div></div> })}
          {d.ubicacion.length === 0 && g && <p>Guardada en el progreso: nivel <b>{g.nivel ?? g.elegido ?? g.nivelCliente ?? '—'}</b>{g.cefr ? ` · ${g.cefr}` : ''}{g.preguntas ? ` · ${g.preguntas} preguntas` : ''}</p>}
          {d.ubicacion.length === 0 && !g && <p className="muted">No hizo la prueba de ubicación.</p>}
        </div>
        <div className="tarjeta"><h2>Últimas clases completadas</h2>
          <div className="desliza"><table><tbody>{d.ultimasClases.map((c: any) => <tr key={c.unidad}><td><b>{c.titulo || c.unidad}</b><br /><span className="muted mono">{c.unidad}</span></td><td>{nivelCorto(c.nivel)}</td><td className="num">{c.intentos > 1 ? `${c.intentos} intentos` : ''}</td><td className="num">{fecha(c.fecha)}</td></tr>)}</tbody></table></div>
          {d.ultimasClases.length === 0 && <p className="muted">Sin clases con fecha.</p>}
          {d.empezadas.length > 0 && <><h2 style={{ marginTop: 14 }}>Empezadas sin terminar</h2>
            <table><tbody>{d.empezadas.map((c: any) => <tr key={c.unidad}><td><b>{c.titulo || c.unidad}</b> <span className="muted mono">{c.unidad}</span></td><td className="num">{fecha(c.fecha)}</td></tr>)}</tbody></table></>}
        </div>
        <div className="tarjeta"><h2>Conversaciones con el tutor</h2>
          <table><tbody>{d.conversaciones.map((c: any) => <tr key={c.id}><td><span className="muted">{IDIOMAS[c.idioma] ?? c.idioma} · N{c.nivel}{c.situacion_id ? ` · situación ${c.situacion_id}` : ''}</span><br />{c.mensaje_alumno}<br /><span className="muted">↳ {c.respuesta}</span></td><td className="num" style={{ width: 110 }}>{fecha(c.fecha)}<br /><span className="muted">{c.tokens_entrada + c.tokens_salida} tokens</span></td></tr>)}</tbody></table>
          {d.conversaciones.length === 0 && <p className="muted">Sin conversaciones.</p>}
        </div>
        <div className="tarjeta"><h2>Errores recientes ({d.errores.length})</h2>
          {d.errores.slice(0, 12).map((x: any) => <div className="errcard" key={x.id}><span className="pill">{SKILLS[x.skill] ?? x.skill}</span> <span className="muted" style={{ fontSize: 12 }}>{x.origen} · {hace(x.fecha)}{x.practicado ? ' · practicado' : ''}</span><br /><s>{x.original}</s> → <b>{x.correccion}</b><br /><span className="muted" style={{ fontSize: 12 }}>{x.explicacion}</span></div>)}
          {d.errores.length === 0 && <p className="muted">Sin errores registrados.</p>}
        </div>
        <div className="tarjeta"><h2>Actividad reciente</h2>
          <div className="desliza"><table><tbody>{d.eventos.map((ev: any, i: number) => <tr key={i}><td>{ev.tipo}</td><td className="muted mono" style={{ wordBreak: 'break-all' }}>{JSON.stringify(ev.datos).slice(0, 160)}</td><td className="num">{fecha(ev.fecha)}</td></tr>)}</tbody></table></div>
          {d.eventos.length === 0 && <p className="muted">Sin eventos.</p>}
          <p className="muted pie-nota">Última sincronización: {fecha(p?.actualizado_en)} · tutor {u.tutor_id} · {(e.diasActividad ?? []).length} días con actividad registrados por la app · {Object.keys(e.practicas ?? {}).length} evidencias de práctica.</p>
        </div>
      </div>
    </>
  )
}
