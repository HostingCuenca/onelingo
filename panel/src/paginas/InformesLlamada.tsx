import { useEffect, useState } from 'react'
import { api, fecha, IDIOMAS } from '../api'

/** Criterios de la evaluación del tutor (lib/informe_llamada.ts). */
export const CRITERIOS: Record<string, string> = {
  habla: 'Habla', ensena: 'Enseña', correcciones: 'Corrige', apoyo: 'Apoyo', tema: 'Tema', escucha: 'Escucha',
}
export const nombreTutor = (t: string) => t.replace('avatar_', '').replace(/^./, (m) => m.toUpperCase())
export const claseNota = (n?: number | null) => n == null ? '' : n >= 8 ? 'ok' : n >= 6 ? 'trial' : 'mal'
const minutos = (s?: number) => s == null ? '—' : s < 60 ? `${s} s` : `${Math.round(s / 60)} min`

export type Informe = {
  id: number; idioma: string; nivel: number; tutorId: string; explica: string; turnos: number; nota: number | null; creadoEn: string
  resumen: { logros: string[]; mejorar: { original: string; correcto: string; explicacion: string }[]; vocabulario: { palabra: string; significado: string }[]; siguientePaso: string } | null
  evaluacion: { nota: number; puntos: Record<string, number>; bien: string[]; problemas: { criterio: string; cita: string; mejor: string }[]; alumno: { nivelReal: string; dificultades: string[] }; recomendacion: string } | null
  tecnico: { duracionSegundos?: number; turnosVivo?: number; turnosPulsar?: number; cortesVivo?: number; reintentosVivo?: number; ultimoErrorVivo?: string; frasesTutor?: number; frasesRespaldo?: number; avisos?: Record<string, number>; dispositivo?: string; prueba?: boolean }
}

/** Datos técnicos de una llamada en una línea. */
export function lineaTecnica(t: Informe['tecnico']) {
  const partes = [
    t.duracionSegundos != null && minutos(t.duracionSegundos),
    (t.turnosVivo || t.turnosPulsar) ? `${t.turnosVivo ?? 0} turnos en vivo · ${t.turnosPulsar ?? 0} pulsando` : '',
    t.cortesVivo ? `${t.cortesVivo} cortes de la escucha (${t.reintentosVivo ?? 0} reintentos)` : '',
    t.frasesTutor ? (t.frasesRespaldo ? `voz de respaldo en ${t.frasesRespaldo} de ${t.frasesTutor} frases` : `${t.frasesTutor} frases con ElevenLabs`) : '',
    t.avisos && Object.keys(t.avisos).length ? `silencios: ${Object.entries(t.avisos).map(([k, v]) => `${k} ${v}`).join(', ')}` : '',
    t.dispositivo, t.prueba ? 'prueba simulada' : '',
  ]
  return partes.filter(Boolean).join(' · ')
}

/** Un informe completo: evaluación del tutor, resumen para el alumno y datos técnicos. */
export function DetalleInforme({ i }: { i: Informe }) {
  const e = i.evaluacion
  return <div style={{ fontSize: 13 }}>
    {e ? <>
      <p style={{ margin: '4px 0' }}>{Object.entries(CRITERIOS).map(([k, n]) => <span key={k} className={`pill ${claseNota((e.puntos[k] ?? 0) * 2)}`} style={{ marginRight: 4 }}>{n} {e.puntos[k]}/5</span>)}</p>
      {e.bien.length > 0 && <p style={{ margin: '4px 0' }}><b>Bien:</b> {e.bien.join(' · ')}</p>}
      {e.problemas.length > 0 && <div style={{ margin: '4px 0' }}><b>A mejorar en el tutor:</b><ul style={{ margin: '2px 0 0 18px', padding: 0 }}>
        {e.problemas.map((p, k) => <li key={k}><span className="muted">({CRITERIOS[p.criterio] ?? p.criterio})</span> «{p.cita}» → {p.mejor}</li>)}</ul></div>}
      <p style={{ margin: '4px 0' }}><b>El alumno:</b> {e.alumno.nivelReal}{e.alumno.dificultades.length > 0 && <> Dificultades: {e.alumno.dificultades.join('; ')}.</>}</p>
      {e.recomendacion && <p style={{ margin: '4px 0' }}><b>Para la próxima:</b> {e.recomendacion}</p>}
    </> : <p className="muted">Sin evaluación (llamada muy corta o la IA no respondió).</p>}
    {i.resumen && <p style={{ margin: '4px 0' }} className="muted"><b>Lo que vio el alumno:</b> {[...i.resumen.logros, i.resumen.siguientePaso].filter(Boolean).join(' · ')}</p>}
    <p className="muted mono" style={{ margin: '4px 0', fontSize: 11 }}>{lineaTecnica(i.tecnico)}</p>
  </div>
}

/** Informes de las videollamadas de un alumno (en su ficha del panel). */
export default function InformesLlamada({ id }: { id: string }) {
  const [lista, setLista] = useState<Informe[] | null>(null); const [abierto, setAbierto] = useState<number | null>(null)
  useEffect(() => { api<Informe[]>(`/admin/usuarios/${id}/informes`).then(setLista).catch(() => setLista([])) }, [id])
  return (
    <div className="tarjeta"><h2>Informes de sus videollamadas</h2>
      <p className="muted pie-nota" style={{ marginTop: -4 }}>Al colgar, un revisor de IA evalúa cómo habló y enseñó el tutor (de 1 a 5 por criterio, con citas) y se guardan los datos técnicos: escucha en vivo o pulsando, cortes y voz de ElevenLabs o de respaldo. Sirve para darle retroalimentación al alumno y para mejorar el tutor.</p>
      {!lista ? <p className="muted">Cargando…</p> : lista.length === 0 ? <p className="muted">Todavía no hay informes: se crean al colgar una videollamada.</p> :
        <table><tbody>{lista.map((i) => <>
          <tr key={i.id} className="click" onClick={() => setAbierto(abierto === i.id ? null : i.id)}>
            <td><b>{nombreTutor(i.tutorId)}</b> <span className="muted">· {IDIOMAS[i.idioma] ?? i.idioma} N{i.nivel} · {i.turnos} turnos{i.explica === 'nativo' ? ' · explica en su idioma' : ''}</span></td>
            <td className="num">{i.nota != null ? <span className={`pill ${claseNota(i.nota)}`}>{i.nota}/10</span> : <span className="muted">—</span>}</td>
            <td className="num">{fecha(i.creadoEn)}</td>
          </tr>
          {abierto === i.id && <tr key={`${i.id}d`}><td colSpan={3}><DetalleInforme i={i} /></td></tr>}
        </>)}</tbody></table>}
    </div>
  )
}
