// Gráficos mínimos en SVG propio (sin librerías).

type Serie = { nombre: string; clave: string; color: string }

const diaCorto = (d: string) => { const [, m, dd] = d.split('-'); return `${Number(dd)}/${Number(m)}` }

/** Líneas por día: una o varias series sobre el mismo eje. */
export function LineasDias({ datos, series, alto = 150 }: { datos: Record<string, any>[]; series: Serie[]; alto?: number }) {
  const ancho = 600, izq = 28, abajo = 18, arriba = 8
  const max = Math.max(1, ...datos.flatMap((d) => series.map((s) => Number(d[s.clave] ?? 0))))
  const n = Math.max(1, datos.length - 1)
  const x = (i: number) => izq + (i / n) * (ancho - izq - 6)
  const y = (v: number) => arriba + (1 - v / max) * (alto - arriba - abajo)
  const marcas = [0, Math.round(max / 2), max].filter((v, i, a) => a.indexOf(v) === i)
  return (
    <div className="grafico">
      <svg viewBox={`0 0 ${ancho} ${alto}`} role="img" aria-label={series.map((s) => s.nombre).join(', ')}>
        {marcas.map((m) => <g key={m}><line x1={izq} x2={ancho} y1={y(m)} y2={y(m)} className="eje" /><text x={izq - 4} y={y(m) + 3} textAnchor="end" className="etq">{m}</text></g>)}
        {series.map((s) => (
          <g key={s.clave}>
            <polyline fill="none" stroke={s.color} strokeWidth={2} points={datos.map((d, i) => `${x(i)},${y(Number(d[s.clave] ?? 0))}`).join(' ')} />
            {datos.map((d, i) => <circle key={i} cx={x(i)} cy={y(Number(d[s.clave] ?? 0))} r={Number(d[s.clave]) > 0 ? 2.5 : 0} fill={s.color}><title>{`${d.dia}: ${d[s.clave]} ${s.nombre.toLowerCase()}`}</title></circle>)}
          </g>
        ))}
        {datos.length > 0 && <>
          <text x={x(0)} y={alto - 4} className="etq">{diaCorto(datos[0].dia)}</text>
          <text x={x(Math.floor(n / 2))} y={alto - 4} textAnchor="middle" className="etq">{diaCorto(datos[Math.floor(n / 2)].dia)}</text>
          <text x={x(n)} y={alto - 4} textAnchor="end" className="etq">{diaCorto(datos[n].dia)}</text>
        </>}
      </svg>
      <div className="leyenda">{series.map((s) => <span key={s.clave}><i style={{ background: s.color }} />{s.nombre}: <b>{datos.reduce((a, d) => a + Number(d[s.clave] ?? 0), 0)}</b> en {datos.length} días</span>)}</div>
    </div>
  )
}

/** Barras horizontales con valor y porcentaje opcional. */
export function BarrasH({ filas, max }: { filas: { etiqueta: string; valor: number; nota?: string }[]; max?: number }) {
  const tope = Math.max(1, max ?? Math.max(0, ...filas.map((f) => f.valor)))
  return (
    <div className="barrash">
      {filas.map((f) => (
        <div key={f.etiqueta} className="fila">
          <span className="et">{f.etiqueta}</span>
          <div className="barra"><i style={{ width: `${(f.valor / tope) * 100}%` }} /></div>
          <span className="val"><b>{f.valor}</b>{f.nota && <span className="muted"> {f.nota}</span>}</span>
        </div>
      ))}
    </div>
  )
}
