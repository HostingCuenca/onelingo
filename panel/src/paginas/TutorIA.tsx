import { useEffect, useState } from 'react'
import { api, fecha, IDIOMAS } from '../api'
import ErrorCarga from '../ErrorCarga'

type Ajustes = { enfoque: 'guiar' | 'equilibrado' | 'conversar'; opciones: 'pocas' | 'normal'; eco: boolean; pedirRepetir: boolean; frasesEvitar: string[]; instrucciones: string }
type Version = { id: number; datos: Ajustes; nota: string; creado_en: string }
type Datos = { actual: Ajustes; defecto: Ajustes; versiones: Version[]; ia: boolean }
type Prueba = { reply: string; espera: { tipo: string; modelo: string } | null; traduccion: string; correcciones: { original: string; correcto: string; explicacion: string }[]; notas: string[]; modelo: string; ms: number }

const ENFOQUES: { v: Ajustes['enfoque']; t: string; d: string }[] = [
  { v: 'guiar', t: 'Clase guiada', d: 'Propone un foco (una estructura y palabras de su nivel), da un ejemplo, lo hace practicar, sube un escalón y repasa. Recomendado.' },
  { v: 'equilibrado', t: 'Conversación que enseña', d: 'Charla del tema del alumno y cada 3 o 4 turnos enseña una palabra o estructura.' },
  { v: 'conversar', t: 'Conversación libre', d: 'Prioriza que el alumno hable; enseña solo cuando surge.' },
]
const TUTORES = ['frank', 'chloe', 'ana', 'elena', 'julia', 'nora', 'hana', 'lucas', 'tomas', 'diego', 'erik', 'andre', 'lumo']
const nombre = (id: string) => id[0].toUpperCase() + id.slice(1)
// Llamada real del 01-11-2026: el alumno se quejó de que el tutor repetía la pregunta.
const EJEMPLO = `T: I’m Frank. Nice to meet you, Roger! Do you live in Denver or another city?
A: I live with my parents.
T: You live with your parents. Do you live in Denver or another city?
A: I live in a house. And you?`
const ESPERA: Record<string, string> = { repetir: 'que repita', elegir: 'que elija', responder: 'que responda libre' }

/** «T: …» / «A: …» por línea → historial del tutor. */
function historialDe(texto: string) {
  return texto.split('\n').map((l) => l.trim()).filter(Boolean).map((l) => {
    const m = /^(T|A|Tutor|Alumno)\s*:\s*(.*)$/i.exec(l)
    return m ? { rol: m[1][0].toUpperCase() === 'T' ? 'tutor' as const : 'alumno' as const, texto: m[2] } : { rol: 'alumno' as const, texto: l }
  })
}
const resumen = (a: Ajustes) => `${ENFOQUES.find((e) => e.v === a.enfoque)?.t} · opciones ${a.opciones} · ${a.eco ? 'con eco' : 'sin eco'} · ${a.pedirRepetir ? 'pide repetir' : 'no pide repetir'}${a.instrucciones ? ' · con indicaciones' : ''}`
const iguales = (a: Ajustes, b: Ajustes) => JSON.stringify(a) === JSON.stringify(b)

function Resultado({ titulo, r }: { titulo: string; r: Prueba | string | null }) {
  if (!r) return null
  if (typeof r === 'string') return <div className="verif error"><b>{titulo}:</b> {r}</div>
  return (
    <div className="tarjeta prueba-res">
      <h2>{titulo}</h2>
      <p className="dicho">{r.reply}</p>
      <p className="muted" style={{ fontSize: 12 }}>{r.traduccion}</p>
      <div className="chips" style={{ margin: '8px 0' }}>
        {r.espera && <span className="pill">Espera {ESPERA[r.espera.tipo] ?? r.espera.tipo}{r.espera.modelo ? `: ${r.espera.modelo}` : ''}</span>}
        <span className="pill trial">{(r.ms / 1000).toFixed(1)} s · {r.modelo}</span>
      </div>
      {r.correcciones.map((c, i) => <div key={i} className="errcard"><s>{c.original}</s> → <b>{c.correcto}</b><br /><span className="muted">{c.explicacion}</span></div>)}
      {r.notas.length > 0 && <details className="instr"><summary>Lo que la app le dijo al tutor en este turno</summary>{r.notas.map((n, i) => <p key={i} className="mono">{n}</p>)}</details>}
    </div>
  )
}

export default function TutorIA() {
  const [d, setD] = useState<Datos | null>(null)
  const [f, setF] = useState<Ajustes | null>(null)
  const [nota, setNota] = useState('')
  const [err, setErr] = useState(''); const [msg, setMsg] = useState(''); const [ocupado, setOcupado] = useState('')
  const [p, setP] = useState({ idioma: 'en', nivel: 1, tutor: 'frank', texto: EJEMPLO, alumno: '' })
  const [fichas, setFichas] = useState<{ usuario_id: string; idioma: string; nombre: string; email: string }[]>([])
  const [res, setRes] = useState<{ borrador: Prueba | string | null; guardado: Prueba | string | null }>({ borrador: null, guardado: null })
  const cargar = () => api<Datos>('/admin/tutor').then((r) => { setD(r); setF(r.actual); setErr('') }).catch((x) => setErr(x.message))
  useEffect(() => { cargar(); api('/admin/fichas').then(setFichas).catch(() => {}) }, [])
  if (err) return <ErrorCarga msg={err} reintentar={() => { setErr(''); cargar() }} />
  if (!d || !f) return <p className="muted">Cargando…</p>
  const cambiado = !iguales(f, d.actual)
  const set = <K extends keyof Ajustes>(k: K, v: Ajustes[K]) => { setF({ ...f, [k]: v }); setMsg('') }

  const guardar = async (e: React.FormEvent) => {
    e.preventDefault(); setOcupado('guardar'); setMsg('')
    try { const r = await api<{ actual: Ajustes; versiones: Version[] }>('/admin/tutor', { metodo: 'PUT', cuerpo: { ajustes: f, nota } }); setD({ ...d, ...r }); setF(r.actual); setNota(''); setMsg('Guardado: el tutor ya usa estos ajustes desde el próximo turno.') }
    catch (x: any) { setMsg(x.message) } finally { setOcupado('') }
  }
  const probar = async () => {
    const historial = historialDe(p.texto)
    if (historial.at(-1)?.rol !== 'alumno') { setRes({ borrador: 'La última línea debe ser del alumno (A: …).', guardado: null }); return }
    setOcupado('probar'); setRes({ borrador: null, guardado: null })
    const una = (a: Ajustes) => api<Prueba>('/admin/tutor/probar', { metodo: 'POST', cuerpo: { ajustes: a, idiomaMeta: p.idioma, nivel: p.nivel, tutorId: `avatar_${p.tutor}`, historial, ...(p.alumno ? { usuarioId: p.alumno } : {}) } }).catch((x) => String(x.message))
    // Con cambios sin guardar se comparan los dos: así se ve qué cambia.
    const [borrador, guardado] = await Promise.all([una(f), cambiado ? una(d.actual) : Promise.resolve(null)])
    setRes({ borrador, guardado }); setOcupado('')
  }

  return (
    <>
      <div className="cab"><h1>Tutor IA</h1><span className={`pill ${d.ia ? 'ok' : 'trial'}`}>{d.ia ? 'IA activa' : 'IA sin configurar'}</span></div>
      <p className="muted pie-nota" style={{ margin: '-8px 0 16px' }}>Cómo enseña el tutor en la videollamada y en el chat. Los cambios se aplican desde el siguiente turno, sin publicar la app. Prueba antes de guardar: cada prueba es una llamada real a la IA.</p>

      <form className="tarjeta conexion-form" onSubmit={guardar}>
        <h2>Cómo enseña</h2>
        <div className="enfoques">
          {ENFOQUES.map((e) => (
            <label key={e.v} className={`enfoque ${f.enfoque === e.v ? 'si' : ''}`}>
              <input type="radio" name="enfoque" checked={f.enfoque === e.v} onChange={() => set('enfoque', e.v)} />
              <b>{e.t}</b><span className="muted">{e.d}</span>
            </label>
          ))}
        </div>
        <div className="form-grid">
          <label className="campo"><span>Preguntas de dos opciones («¿café o té?»)</span>
            <select value={f.opciones} onChange={(e) => set('opciones', e.target.value as Ajustes['opciones'])}>
              <option value="pocas">Pocas: solo si el alumno se bloquea, nunca dos seguidas</option>
              <option value="normal">Normal: a menudo en niveles 1-2</option>
            </select></label>
          <div className="campo"><span>Al responder</span>
            <label className="check-linea"><input type="checkbox" checked={f.eco} onChange={(e) => set('eco', e.target.checked)} /> Repetir lo que dijo el alumno para confirmarlo («Coffee, yes…»)</label>
            <label className="check-linea"><input type="checkbox" checked={f.pedirRepetir} onChange={(e) => set('pedirRepetir', e.target.checked)} /> Tras corregir, pedirle que diga la frase completa</label>
          </div>
          <label className="campo"><span>Frases que nunca debe decir (una por línea, en cualquier idioma)</span>
            <textarea rows={6} value={f.frasesEvitar.join('\n')} onChange={(e) => set('frasesEvitar', e.target.value.split('\n').map((x) => x.trim()).filter(Boolean).slice(0, 40))} /></label>
          <label className="campo"><span>Indicaciones extra del equipo pedagógico</span>
            <textarea rows={6} maxLength={1500} value={f.instrucciones} onChange={(e) => set('instrucciones', e.target.value)}
              placeholder="Ej.: En niveles 1-2 trabaja sobre todo el presente simple. No hables de política." />
            <span className="muted uso-nota">{f.instrucciones.length}/1500 · Mandan sobre la forma de enseñar, nunca sobre el idioma de la respuesta ni los límites de seguridad.</span></label>
        </div>
        <label className="campo"><span>Nota del cambio (para el historial)</span><input maxLength={200} value={nota} onChange={(e) => setNota(e.target.value)} placeholder="Ej.: menos preguntas de opciones" /></label>
        <div className="acciones">
          <button disabled={!!ocupado || !cambiado}>{ocupado === 'guardar' ? 'Guardando…' : 'Guardar'}</button>
          <button type="button" className="sec" disabled={!cambiado} onClick={() => { setF(d.actual); setMsg('') }}>Descartar cambios</button>
          <button type="button" className="sec" disabled={iguales(f, d.defecto)} onClick={() => { setF(d.defecto); setMsg('') }}>Valores recomendados</button>
          {cambiado && !msg && <span className="muted">Cambios sin guardar</span>}{msg && <span className={msg.startsWith('Guardado') ? 'ok-texto' : 'err'}>{msg}</span>}
        </div>
      </form>

      <div className="tarjeta conexion-form">
        <h2>Probar un turno</h2>
        <p className="muted uso-nota" style={{ marginTop: -6 }}>Pega una conversación («T:» tutor, «A:» alumno) que termine con el alumno. Si hay cambios sin guardar, responde con los dos ajustes para comparar.</p>
        <div className="form-grid tres">
          <label className="campo"><span>Idioma</span><select value={p.idioma} onChange={(e) => setP({ ...p, idioma: e.target.value })}>{Object.entries(IDIOMAS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select></label>
          <label className="campo"><span>Nivel</span><select value={p.nivel} onChange={(e) => setP({ ...p, nivel: Number(e.target.value) })}>{Array.from({ length: 10 }, (_, i) => <option key={i} value={i + 1}>N{i + 1}</option>)}</select></label>
          <label className="campo"><span>Tutor</span><select value={p.tutor} onChange={(e) => setP({ ...p, tutor: e.target.value })}>{TUTORES.map((t) => <option key={t} value={t}>{nombre(t)}</option>)}</select></label>
          <label className="campo"><span>Como si hablara con</span><select value={p.alumno} onChange={(e) => setP({ ...p, alumno: e.target.value })}>
            <option value="">Un alumno nuevo (sin ficha)</option>
            {fichas.filter((x) => x.idioma === p.idioma).map((x) => <option key={x.usuario_id} value={x.usuario_id}>{x.nombre || x.email}</option>)}
          </select></label>
        </div>
        <label className="campo"><span>Conversación</span><textarea rows={7} className="mono" value={p.texto} onChange={(e) => setP({ ...p, texto: e.target.value })} /></label>
        <div className="acciones"><button type="button" disabled={!!ocupado || !d.ia} onClick={probar}>{ocupado === 'probar' ? 'El tutor está respondiendo…' : 'Probar'}</button></div>
        <div className={res.guardado ? 'grid2' : ''}>
          <Resultado titulo={cambiado ? 'Con los cambios' : 'Con los ajustes guardados'} r={res.borrador} />
          <Resultado titulo="Con los ajustes guardados" r={res.guardado} />
        </div>
      </div>

      <div className="tarjeta">
        <h2>Historial de cambios</h2>
        {d.versiones.length === 0 ? <p className="muted">Aún no se ha guardado ningún cambio: el tutor usa los valores recomendados.</p> : (
          <div className="desliza"><table>
            <thead><tr><th>Fecha</th><th>Nota</th><th>Ajustes</th><th></th></tr></thead>
            <tbody>{d.versiones.map((v, i) => <tr key={v.id}>
              <td>{fecha(v.creado_en)}{i === 0 && <> <span className="pill ok">Activa</span></>}</td><td>{v.nota || '—'}</td><td className="muted">{resumen(v.datos)}</td>
              <td className="num">{i > 0 && <button className="sec chico" onClick={() => { setF(v.datos); setNota(`Restaurada la versión del ${fecha(v.creado_en)}`); setMsg(''); window.scrollTo({ top: 0, behavior: 'smooth' }) }}>Cargar</button>}</td>
            </tr>)}</tbody>
          </table></div>
        )}
        <p className="muted pie-nota">«Cargar» pone esa versión en el formulario; se aplica al guardar.</p>
      </div>
    </>
  )
}
