import { useEffect, useState } from 'react'
import { api, fecha, IDIOMAS, token } from '../api'

const kb = (b: number) => b < 1024 * 1024 ? `${Math.round(b / 1024)} KB` : `${(b / 1024 / 1024).toFixed(1)} MB`

export default function Audios() {
  const [d, setD] = useState<any>(null)
  const [texto, setTexto] = useState('Buongiorno! Vorrei un caffè, per favore.')
  const [idioma, setIdioma] = useState('it')
  const [voz, setVoz] = useState('narradora')
  const [res, setRes] = useState<any>(null)
  const [ocupado, setOcupado] = useState(false)
  const cargar = () => api('/admin/audios').then(setD)
  useEffect(() => { cargar() }, [])
  const probar = async (e: React.FormEvent) => {
    e.preventDefault(); setOcupado(true); setRes(null)
    try { const r = await api('/admin/audios/probar', { metodo: 'POST', cuerpo: { texto, idioma, voz } }); setRes(r); cargar() }
    catch (x: any) { setRes({ error: x.message }) } finally { setOcupado(false) }
  }
  if (!d) return <p className="muted">Cargando…</p>
  const src = (hash: string) => `${import.meta.env.DEV ? '/api' : ''}/admin/audios/${hash}?token=${token()}`
  const pct = d.cuota ? Math.round((d.cuota.usados / d.cuota.limite) * 100) : 0
  return (
    <>
      <div className="cab"><h1>Voz y audios</h1><span className="muted">ElevenLabs · {d.modelo}</span></div>
      <div className="kpis">
        <div className="kpi"><div className="v">{d.audios}</div><div className="l">Audios guardados</div></div>
        <div className="kpi"><div className="v">{d.reproducciones}</div><div className="l">Reproducciones</div></div>
        <div className="kpi"><div className="v">{d.caracteres}</div><div className="l">Caracteres sintetizados</div></div>
        <div className="kpi"><div className="v">{kb(d.bytes)}</div><div className="l">Espacio en disco</div></div>
        {d.cuota && <div className="kpi"><div className="v">{pct} %</div><div className="l">Cuota mensual ({d.cuota.usados} / {d.cuota.limite}, plan {d.cuota.plan})</div></div>}
      </div>
      <div className="grid2">
        <div className="tarjeta"><h2>Probar una voz</h2>
          <form onSubmit={probar} style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            <input value={texto} onChange={(e) => setTexto(e.target.value)} placeholder="Texto a decir" />
            <div style={{ display: 'flex', gap: 10 }}>
              <select value={idioma} onChange={(e) => setIdioma(e.target.value)}>{Object.entries(IDIOMAS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
              <select value={voz} onChange={(e) => setVoz(e.target.value)}>{Object.entries(d.voces).map(([k, v]: any) => <option key={k} value={k}>{k} · {v.nombre}</option>)}</select>
              <button disabled={ocupado}>{ocupado ? 'Generando…' : 'Escuchar'}</button>
            </div>
          </form>
          {res?.error && <p className="err">{res.error}</p>}
          {res?.hash && <p className="muted" style={{ marginTop: 10 }}>{res.cache ? 'Ya existía: salió de la caché sin gastar cuota.' : `Generado ahora (${res.caracteres} caracteres).`}<br /><audio controls autoPlay src={src(res.hash)} style={{ width: '100%', marginTop: 6 }} /></p>}
          <p className="muted" style={{ fontSize: 12, marginTop: 10 }}>Cada frase se sintetiza una sola vez y se guarda; la app y el Listening reutilizan el mismo archivo.</p>
        </div>
        <div className="tarjeta"><h2>Voces por rol</h2>
          <table><tbody>{Object.entries(d.voces).map(([k, v]: any) => <tr key={k}><td><b>{k}</b></td><td>{v.nombre}</td><td className="muted">{v.descripcion}</td><td style={{ textAlign: 'right' }}>{d.porVoz.find((x: any) => x.voz === k)?.audios ?? 0}</td></tr>)}</tbody></table>
          <h2 style={{ marginTop: 14 }}>Por idioma</h2>
          <table><tbody>{d.porIdioma.map((r: any) => <tr key={r.idioma}><td>{IDIOMAS[r.idioma] ?? r.idioma}</td><td style={{ textAlign: 'right' }}><b>{r.audios}</b> audios · {r.caracteres} car.</td></tr>)}</tbody></table>
          {d.porIdioma.length === 0 && <p className="muted">Todavía no hay audios.</p>}
        </div>
      </div>
      <div className="tarjeta"><h2>Últimos audios</h2>
        <table><thead><tr><th>Fecha</th><th>Idioma</th><th>Voz</th><th>Texto</th><th>Usos</th><th></th></tr></thead>
          <tbody>{d.ultimos.map((a: any) => <tr key={a.hash}><td>{fecha(a.creado_en)}</td><td>{IDIOMAS[a.idioma] ?? a.idioma}</td><td><span className="pill">{a.voz}</span></td><td>{a.texto}</td><td>{a.usos}</td><td><audio controls preload="none" src={src(a.hash)} style={{ height: 30 }} /></td></tr>)}</tbody></table>
        {d.ultimos.length === 0 && <p className="muted">Sin audios todavía.</p>}
      </div>
    </>
  )
}
