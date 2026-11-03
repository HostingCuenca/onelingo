import { useEffect, useState } from 'react'
import { api, fecha, IDIOMAS } from '../api'
import ErrorCarga from '../ErrorCarga'

type Turno = { id: number; fecha: string; alumno: string; tutor: string; espera: { tipo: string; modelo: string } | null; correcciones: { original: string; correcto: string }[]; marcas: string[] }
type Indicadores = { turnosTutor: number; preguntasRepetidas: number; eco: number; opciones: number; aperturasRepetidas: number; muletillas: Record<string, number> }
type Llamada = { inicio: string; fin: string; alumno: string; email: string; idioma: string; nivel: number; tutorId: string; situacionId: number | null; indicadores: Indicadores; turnos: Turno[] }

const pct = (n: number, t: number) => (t ? Math.round((100 * n) / t) : 0)
const tutorDe = (id: string) => { const s = id.replace(/^avatar_/, ''); return s[0].toUpperCase() + s.slice(1) }
const AVISO: Record<string, string> = { '[silencio]': 'Silencio del alumno', '[pista]': 'Pidió una pista' }
const muletillas = (i: Indicadores) => Object.values(i.muletillas).reduce((a, b) => a + b, 0)
/** Puntos de repetición de una llamada: lo que el alumno nota. */
const repeticion = (i: Indicadores) => i.preguntasRepetidas + i.eco + i.aperturasRepetidas + muletillas(i)

function Conversacion({ l }: { l: Llamada }) {
  return (
    <div className="dialogo">
      {l.turnos.map((t) => (
        <div key={t.id}>
          {t.alumno && (AVISO[t.alumno] ? <div className="aviso-turno muted">{AVISO[t.alumno]}</div> : <div className="burbuja alumno">{t.alumno}</div>)}
          <div className="burbuja tutor">
            {t.tutor}
            {(t.marcas.length > 0 || t.espera || t.correcciones.length > 0) && <div className="chips" style={{ marginTop: 6 }}>
              {t.marcas.map((m) => <span key={m} className="pill mal">{m}</span>)}
              {t.espera && <span className="pill">espera: {t.espera.tipo}</span>}
              {t.correcciones.map((c, i) => <span key={i} className="pill ok">{c.original} → {c.correcto}</span>)}
            </div>}
          </div>
        </div>
      ))}
    </div>
  )
}

export default function Conversaciones() {
  const [dias, setDias] = useState(7)
  const [d, setD] = useState<Llamada[] | null>(null)
  const [err, setErr] = useState(''); const [abierta, setAbierta] = useState<string | null>(null)
  const cargar = () => { setD(null); api<{ llamadas: Llamada[] }>(`/admin/practicas?dias=${dias}`).then((r) => { setD(r.llamadas); setErr('') }).catch((x) => setErr(x.message)) }
  useEffect(cargar, [dias])
  if (err) return <ErrorCarga msg={err} reintentar={() => { setErr(''); cargar() }} />
  const ls = d ?? []
  const tot = ls.reduce((a, l) => ({ t: a.t + l.indicadores.turnosTutor, o: a.o + l.indicadores.opciones, r: a.r + l.indicadores.preguntasRepetidas, e: a.e + l.indicadores.eco }), { t: 0, o: 0, r: 0, e: 0 })
  return (
    <>
      <div className="cab"><h1>Conversaciones IA</h1>
        <select value={dias} onChange={(e) => setDias(Number(e.target.value))}>{[1, 3, 7, 14, 30].map((n) => <option key={n} value={n}>Últimos {n} {n === 1 ? 'día' : 'días'}</option>)}</select></div>
      {!d ? <p className="muted">Cargando…</p> : <>
        <div className="kpis">
          <div className="kpi"><div className="v">{ls.length}</div><div className="l">Llamadas y chats</div></div>
          <div className="kpi"><div className="v">{tot.t}</div><div className="l">Turnos del tutor</div></div>
          <div className="kpi"><div className="v">{pct(tot.r, tot.t)} %</div><div className="l">Preguntas repetidas</div><div className="nota">{tot.r} veces volvió a preguntar lo mismo</div></div>
          <div className="kpi"><div className="v">{pct(tot.e, tot.t)} %</div><div className="l">Eco</div><div className="nota">repite lo que dijo el alumno</div></div>
          <div className="kpi"><div className="v">{pct(tot.o, tot.t)} %</div><div className="l">Dos opciones</div><div className="nota">turnos con «¿X o Y?»</div></div>
        </div>
        <div className="tarjeta">
          <div className="desliza"><table>
            <thead><tr><th>Alumno</th><th>Tutor · idioma</th><th className="num">Turnos</th><th>Repetición</th><th>Inicio</th></tr></thead>
            <tbody>{ls.map((l) => {
              const k = `${l.inicio}|${l.tutorId}|${l.email}`, i = l.indicadores, r = repeticion(i)
              return [
                <tr key={k} className="click" onClick={() => setAbierta(abierta === k ? null : k)}>
                  <td><b>{l.alumno}</b><br /><span className="muted mono">{l.email}</span></td>
                  <td>{tutorDe(l.tutorId)} · {IDIOMAS[l.idioma] ?? l.idioma} N{l.nivel}{l.situacionId != null && <><br /><span className="muted">situación {l.situacionId}</span></>}</td>
                  <td className="num">{i.turnosTutor}</td>
                  <td><div className="chips">
                    {r === 0 && <span className="pill ok">sin repetición</span>}
                    {i.preguntasRepetidas > 0 && <span className="pill mal">{i.preguntasRepetidas} preguntas repetidas</span>}
                    {i.eco > 0 && <span className="pill mal">{i.eco} eco</span>}
                    {i.aperturasRepetidas > 0 && <span className="pill trial">{i.aperturasRepetidas} misma apertura</span>}
                    {muletillas(i) > 0 && <span className="pill trial">{muletillas(i)} muletillas</span>}
                    {i.turnosTutor >= 4 && pct(i.opciones, i.turnosTutor) >= 50 && <span className="pill trial">{pct(i.opciones, i.turnosTutor)} % dos opciones</span>}
                  </div></td>
                  <td>{fecha(l.inicio)}</td>
                </tr>,
                abierta === k && <tr key={k + 'd'}><td colSpan={5}><Conversacion l={l} /></td></tr>,
              ]
            })}</tbody>
          </table></div>
          {ls.length === 0 && <p className="muted">Sin conversaciones en este periodo.</p>}
          <p className="muted pie-nota">Cada fila es una llamada o un chat (mismo alumno y tutor, sin pausas de más de 20 minutos). Toca una para ver la conversación con las repeticiones marcadas.
            Si el alumno siguió hablando antes de oír al tutor, esa respuesta se descartó en la app pero queda aquí: puede parecer una repetición que el alumno no oyó. Para cambiar cómo responde el tutor, ve a <b>Tutor IA</b>.</p>
        </div>
      </>}
    </>
  )
}
