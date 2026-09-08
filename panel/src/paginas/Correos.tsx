import { useEffect, useState } from 'react'
import { api, fecha } from '../api'

export default function Correos() {
  const [lista, setLista] = useState<any[]>([]); const [abierto, setAbierto] = useState<any>(null); const [estado, setEstado] = useState<any>(null)
  useEffect(() => { api('/admin/correos').then(setLista); api('/admin/estado-ia').then(setEstado) }, [])
  return (
    <>
      <div className="cab"><h1>Correos</h1>{estado && <span className={`pill ${estado.smtp ? 'ok' : 'trial'}`}>{estado.smtp ? 'SMTP configurado' : 'Sin SMTP: bandeja local'}</span>}</div>
      <p className="muted">Verificación de cuenta y recuperación de contraseña. Sin SMTP configurado en el backend, los correos quedan aquí para poder probar el flujo (abre uno y usa su enlace).</p>
      <div className="grid2">
        <div className="tarjeta"><table><thead><tr><th>Para</th><th>Asunto</th><th>Estado</th><th>Fecha</th></tr></thead><tbody>
          {lista.map((c) => <tr key={c.id} className="click" onClick={() => setAbierto(c)}><td className="mono">{c.para}</td><td>{c.asunto}</td><td>{c.enviado ? <span className="pill ok">enviado</span> : <span className="pill trial">en bandeja</span>}</td><td>{fecha(c.fecha)}</td></tr>)}
        </tbody></table>{lista.length === 0 && <p className="muted">Todavía no se ha generado ningún correo.</p>}</div>
        <div className="tarjeta"><h2>{abierto ? abierto.asunto : 'Vista previa'}</h2>
          {abierto ? <div style={{ border: '1px solid var(--linea)', borderRadius: 10, padding: 8, background: '#fff' }} dangerouslySetInnerHTML={{ __html: abierto.cuerpo }} /> : <p className="muted">Selecciona un correo para verlo.</p>}
          {abierto && <p className="muted mono" style={{ fontSize: 11 }}>{abierto.detalle}</p>}
        </div>
      </div>
    </>
  )
}
