import { useEffect, useState } from 'react'
import { api, ESTADOS, fecha, hace, num, usd } from '../api'

type Fila = {
  usuarioId: string; nombre: string; email: string; planId: string; planNombre: string; origen: 'stripe' | 'cortesia'; estado: string; acceso: boolean
  cancelaAlFinal: boolean; periodoFin: string | null; modo: string | null; importe: number | null; moneda: string | null; intervalo: string | null; nota: string; actualizadoEn: string
}
type Datos = {
  resumen: { modo: string | null; activas: number; mrr: number; otrasMonedas: number; nuevas30: number; canceladas30: number; impagos: number; cortesias: number; otroModo: number }
  filas: Fila[]; total: number
}

const FILTROS: [string, string][] = [['', 'Todos los estados'], ['con_acceso', 'Con acceso'], ['activa', 'Activas'], ['prueba_stripe', 'En prueba (Stripe)'], ['impago', 'Impago'],
  ['cancela_al_final', 'Cancelan al final del periodo'], ['cancelada', 'Canceladas'], ['vencida', 'Vencidas'], ['cortesia', 'Cortesías']]

export default function Suscripciones({ abrir }: { abrir: (id: string) => void }) {
  const [q, setQ] = useState(''); const [estado, setEstado] = useState('')
  const [d, setD] = useState<Datos | null>(null); const [err, setErr] = useState('')
  useEffect(() => {
    const t = setTimeout(() => api<Datos>(`/admin/suscripciones?${new URLSearchParams({ q, estado })}`).then((r) => { setD(r); setErr('') }).catch((e) => setErr(e.message)), 250)
    return () => clearTimeout(t)
  }, [q, estado])
  const r = d?.resumen
  return (
    <>
      <div className="cab"><h1>Suscripciones</h1>{r?.modo && <span className={`pill ${r.modo === 'live' ? 'ok' : 'trial'}`}>{r.modo === 'live' ? 'MODO REAL' : 'MODO TEST'}</span>}</div>
      {r && <div className="kpis">
        <div className="kpi"><div className="v">{num(r.activas)}</div><div className="l">Activas (Stripe)</div></div>
        <div className="kpi"><div className="v">{usd(r.mrr)}</div><div className="l">MRR (USD)</div><div className="nota">anuales ÷ 12{r.otrasMonedas ? ` · ${r.otrasMonedas} en otra moneda sin contar` : ''}</div></div>
        <div className="kpi"><div className="v">{num(r.nuevas30)}</div><div className="l">Nuevas 30 días</div></div>
        <div className="kpi"><div className="v">{num(r.canceladas30)}</div><div className="l">Canceladas 30 días</div></div>
        <div className="kpi"><div className="v" style={r.impagos ? { color: 'var(--rojo)' } : undefined}>{num(r.impagos)}</div><div className="l">Impagos</div></div>
        <div className="kpi"><div className="v">{num(r.cortesias)}</div><div className="l">Cortesías vigentes</div></div>
      </div>}
      {r && r.otroModo > 0 && <p className="muted pie-nota" style={{ margin: '-8px 0 12px' }}>{r.otroModo} suscripciones del otro modo de Stripe no cuentan en el resumen.</p>}
      <div className="filtros">
        <input placeholder="Buscar por nombre, correo, plan o cliente de Stripe…" value={q} onChange={(e) => setQ(e.target.value)} />
        <select value={estado} onChange={(e) => setEstado(e.target.value)} aria-label="Estado">{FILTROS.map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
      </div>
      {err && <p className="err">{err}</p>}
      <div className="tarjeta">
        {d && <p className="muted" style={{ marginTop: 0 }}>{d.total} suscripciones{d.total > d.filas.length ? ` (se muestran ${d.filas.length})` : ''}</p>}
        <div className="desliza"><table>
          <thead><tr><th>Alumno</th><th>Plan</th><th>Origen</th><th>Estado</th><th>Hasta</th><th className="num">Importe</th><th>Actualizada</th></tr></thead>
          <tbody>{d?.filas.map((f) => {
            const [clase, etq] = ESTADOS[f.estado] ?? ['', f.estado]
            return <tr key={f.usuarioId} className="click" onClick={() => abrir(f.usuarioId)}>
              <td><b>{f.nombre}</b><br /><span className="muted mono">{f.email}</span></td>
              <td>{f.planNombre}<br /><span className="muted mono">{f.planId}</span></td>
              <td>{f.origen === 'cortesia' ? <span className="pill">Cortesía</span> : <>Stripe{f.modo && <span className="muted"> · {f.modo}</span>}</>}</td>
              <td><span className={`pill ${clase}`}>{etq}</span>{f.cancelaAlFinal && <><br /><span className="muted">cancela al final</span></>}</td>
              <td>{f.periodoFin ? fecha(f.periodoFin) : f.origen === 'cortesia' ? 'Sin fecha' : '—'}</td>
              <td className="num">{f.importe !== null ? `${f.importe.toFixed(2)} ${(f.moneda ?? '').toUpperCase()}${f.intervalo === 'anio' ? '/año' : '/mes'}` : '—'}</td>
              <td>{hace(f.actualizadoEn)}</td>
            </tr>
          })}</tbody>
        </table></div>
        {d && d.filas.length === 0 && <p className="muted">No hay suscripciones con esos filtros.</p>}
      </div>
    </>
  )
}
