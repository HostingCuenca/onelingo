import { useEffect, useState } from 'react'
import { api, ESTADOS, fecha, hace, IDIOMAS, num, usd } from '../api'

type Fila = {
  usuarioId: string; nombre: string; email: string; planId: string; planNombre: string; origen: 'stripe' | 'cortesia' | 'familia'; estado: string; acceso: boolean
  cancelaAlFinal: boolean; periodoFin: string | null; modo: string | null; importe: number | null; moneda: string | null; intervalo: string | null; meses?: number | null; titularEmail?: string | null; nota: string; actualizadoEn: string
  idiomas: string[]; todosLosIdiomas: boolean; idiomasPorElegir: number
}
type PorIdioma = { idioma: string; suscriptores: number; cortesias: number; mrr: number }
type Datos = {
  resumen: { modo: string | null; activas: number; mrr: number; otrasMonedas: number; nuevas30: number; canceladas30: number; impagos: number; cortesias: number; familia?: number; otroModo: number; porIdioma?: PorIdioma[] }
  filas: Fila[]; total: number
}

const FILTROS: [string, string][] = [['', 'Todos los estados'], ['con_acceso', 'Con acceso'], ['activa', 'Activas'], ['prueba_stripe', 'En prueba (Stripe)'], ['impago', 'Impago'],
  ['cancela_al_final', 'Cancelan al final del periodo'], ['cancelada', 'Canceladas'], ['vencida', 'Vencidas'], ['cortesia', 'Cortesías'], ['familia', 'Miembros de un plan familiar']]

export default function Suscripciones({ abrir }: { abrir: (id: string) => void }) {
  const [q, setQ] = useState(''); const [estado, setEstado] = useState(''); const [idioma, setIdioma] = useState('')
  const [d, setD] = useState<Datos | null>(null); const [err, setErr] = useState('')
  useEffect(() => {
    const t = setTimeout(() => api<Datos>(`/admin/suscripciones?${new URLSearchParams({ q, estado, idioma })}`).then((r) => { setD(r); setErr('') }).catch((e) => setErr(e.message)), 250)
    return () => clearTimeout(t)
  }, [q, estado, idioma])
  const r = d?.resumen
  return (
    <>
      <div className="cab"><h1>Suscripciones</h1>{r?.modo && <span className={`pill ${r.modo === 'live' ? 'ok' : 'trial'}`}>{r.modo === 'live' ? 'MODO REAL' : 'MODO TEST'}</span>}</div>
      {r && <div className="kpis">
        <div className="kpi"><div className="v">{num(r.activas)}</div><div className="l">Activas (Stripe)</div></div>
        <div className="kpi"><div className="v">{usd(r.mrr)}</div><div className="l">MRR (USD)</div><div className="nota">anuales ÷ 12, de N meses ÷ N{r.otrasMonedas ? ` · ${r.otrasMonedas} en otra moneda sin contar` : ''}</div></div>
        <div className="kpi"><div className="v">{num(r.nuevas30)}</div><div className="l">Nuevas 30 días</div></div>
        <div className="kpi"><div className="v">{num(r.canceladas30)}</div><div className="l">Canceladas 30 días</div></div>
        <div className="kpi"><div className="v" style={r.impagos ? { color: 'var(--rojo)' } : undefined}>{num(r.impagos)}</div><div className="l">Impagos</div></div>
        <div className="kpi"><div className="v">{num(r.cortesias)}</div><div className="l">Cortesías vigentes</div></div>
        {r.familia !== undefined && <div className="kpi"><div className="v">{num(r.familia)}</div><div className="l">Miembros de planes familiares</div></div>}
      </div>}
      {r?.porIdioma && <div className="tarjeta">
        <h2>Por idioma</h2>
        <div className="desliza"><table>
          <thead><tr><th>Idioma</th><th className="num">Suscriptores (Stripe)</th><th className="num">Cortesías</th><th className="num">MRR (USD)</th></tr></thead>
          <tbody>{r.porIdioma.map((x) => <tr key={x.idioma} className={x.idioma.length === 2 ? 'click' : ''} onClick={() => x.idioma.length === 2 && setIdioma(x.idioma)}>
            <td>{x.idioma === 'todos' ? <i>Todos los idiomas</i> : x.idioma === 'por_elegir' ? <i>Sin idiomas elegidos</i> : IDIOMAS[x.idioma] ?? x.idioma}</td>
            <td className="num">{num(x.suscriptores)}</td><td className="num">{num(x.cortesias)}</td><td className="num">{usd(x.mrr)}</td>
          </tr>)}</tbody>
        </table></div>
        <p className="muted pie-nota">Cuenta suscripciones con acceso. El MRR de cada suscripción se reparte a partes iguales entre sus idiomas elegidos (un plan de 2 idiomas a 30 USD suma 15 a cada uno); los planes o cortesías de «todos los idiomas» van en su propia fila y las suscripciones sin ningún idioma elegido, en «Sin idiomas elegidos». Un alumno con varios idiomas cuenta en cada uno, así que los suscriptores no suman el total.</p>
      </div>}
      {r && r.otroModo > 0 && <p className="muted pie-nota" style={{ margin: '-8px 0 12px' }}>{r.otroModo} suscripciones del otro modo de Stripe no cuentan en el resumen.</p>}
      <div className="filtros">
        <input placeholder="Buscar por nombre, correo, plan o cliente de Stripe…" value={q} onChange={(e) => setQ(e.target.value)} />
        <select value={estado} onChange={(e) => setEstado(e.target.value)} aria-label="Estado">{FILTROS.map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
        <select value={idioma} onChange={(e) => setIdioma(e.target.value)} aria-label="Idioma"><option value="">Todos los idiomas</option>{Object.entries(IDIOMAS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
      </div>
      {err && <p className="err">{err}</p>}
      <div className="tarjeta">
        {d && <p className="muted" style={{ marginTop: 0 }}>{d.total} suscripciones{d.total > d.filas.length ? ` (se muestran ${d.filas.length})` : ''}</p>}
        <div className="desliza"><table>
          <thead><tr><th>Alumno</th><th>Plan</th><th>Idiomas</th><th>Origen</th><th>Estado</th><th>Hasta</th><th className="num">Importe</th><th>Actualizada</th></tr></thead>
          <tbody>{d?.filas.map((f) => {
            const [clase, etq] = ESTADOS[f.estado] ?? ['', f.estado]
            return <tr key={f.usuarioId} className="click" onClick={() => abrir(f.usuarioId)}>
              <td><b>{f.nombre}</b><br /><span className="muted mono">{f.email}</span></td>
              <td>{f.planNombre}<br /><span className="muted mono">{f.planId}</span></td>
              <td>{f.todosLosIdiomas ? 'Todos' : f.idiomas.map((c) => IDIOMAS[c] ?? c).join(', ') || '—'}{f.idiomasPorElegir > 0 && <><br /><span className="muted">{f.idiomasPorElegir} por elegir</span></>}</td>
              <td>{f.origen === 'cortesia' ? <span className="pill">Cortesía</span>
                : f.origen === 'familia' ? <><span className="pill">Familia</span>{f.titularEmail && <><br /><span className="muted mono">paga {f.titularEmail}</span></>}</>
                : <>Stripe{f.modo && <span className="muted"> · {f.modo}</span>}</>}</td>
              <td><span className={`pill ${clase}`}>{etq}</span>{f.cancelaAlFinal && <><br /><span className="muted">cancela al final</span></>}</td>
              <td>{f.periodoFin ? fecha(f.periodoFin) : f.origen !== 'stripe' ? 'Sin fecha' : '—'}</td>
              <td className="num">{f.importe !== null ? `${f.importe.toFixed(2)} ${(f.moneda ?? '').toUpperCase()}${(f.meses ?? 1) > 1 && f.meses !== 12 ? ` cada ${f.meses} meses` : f.intervalo === 'anio' || f.meses === 12 ? '/año' : '/mes'}` : '—'}</td>
              <td>{hace(f.actualizadoEn)}</td>
            </tr>
          })}</tbody>
        </table></div>
        {d && d.filas.length === 0 && <p className="muted">No hay suscripciones con esos filtros.</p>}
      </div>
    </>
  )
}
