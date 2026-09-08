import { useEffect, useState } from 'react'
import { api, guardarToken, token } from './api'
import Resumen from './paginas/Resumen'
import Usuarios from './paginas/Usuarios'
import UsuarioDetalle from './paginas/UsuarioDetalle'
import Correos from './paginas/Correos'
import Conversaciones from './paginas/Conversaciones'
import Audios from './paginas/Audios'

type Ruta = { p: 'resumen' } | { p: 'usuarios' } | { p: 'usuario'; id: string } | { p: 'correos' } | { p: 'conversaciones' } | { p: 'audios' }

function Login({ onOk }: { onOk: () => void }) {
  const [usuario, setUsuario] = useState('admin'); const [pin, setPin] = useState('1234'); const [err, setErr] = useState('')
  const entrar = async (e: React.FormEvent) => {
    e.preventDefault()
    try { const r = await api<{ token: string }>('/admin/login', { metodo: 'POST', cuerpo: { usuario, pin } }); guardarToken(r.token); onOk() }
    catch (x: any) { setErr(x.message) }
  }
  return (
    <form className="login" onSubmit={entrar}>
      <h1>One<span style={{ color: 'var(--morado)' }}>Lingo</span> · Panel</h1>
      <p className="muted">Administración de alumnos y progreso</p>
      <input value={usuario} onChange={(e) => setUsuario(e.target.value)} placeholder="Usuario" />
      <input value={pin} onChange={(e) => setPin(e.target.value)} placeholder="PIN" type="password" />
      {err && <div className="err">{err}</div>}
      <button>Entrar</button>
      <p className="muted" style={{ fontSize: 12 }}>Demo: admin / 1234 (se cambia en .env del backend)</p>
    </form>
  )
}

export default function App() {
  const [sesion, setSesion] = useState(!!token())
  const [ruta, setRuta] = useState<Ruta>({ p: 'resumen' })
  useEffect(() => {
    const onErr = (e: PromiseRejectionEvent) => { if (e.reason?.status === 401) { guardarToken(null); setSesion(false) } }
    window.addEventListener('unhandledrejection', onErr); return () => window.removeEventListener('unhandledrejection', onErr)
  }, [])
  if (!sesion) return <Login onOk={() => setSesion(true)} />
  return (
    <div className="app">
      <aside>
        <div className="marca">One<b>Lingo</b> · Panel</div>
        <a className={ruta.p === 'resumen' ? 'activo' : ''} onClick={() => setRuta({ p: 'resumen' })}>Resumen</a>
        <a className={ruta.p === 'usuarios' || ruta.p === 'usuario' ? 'activo' : ''} onClick={() => setRuta({ p: 'usuarios' })}>Alumnos</a>
        <a className={ruta.p === 'conversaciones' ? 'activo' : ''} onClick={() => setRuta({ p: 'conversaciones' })}>Conversaciones IA</a>
        <a className={ruta.p === 'audios' ? 'activo' : ''} onClick={() => setRuta({ p: 'audios' })}>Voz y audios</a>
        <a className={ruta.p === 'correos' ? 'activo' : ''} onClick={() => setRuta({ p: 'correos' })}>Correos</a>
        <div className="pie">API: {import.meta.env.DEV ? 'localhost:8091' : 'misma raíz'}<br /><button className="sec" onClick={() => { guardarToken(null); setSesion(false) }}>Salir</button></div>
      </aside>
      <main>
        {ruta.p === 'resumen' && <Resumen />}
        {ruta.p === 'usuarios' && <Usuarios abrir={(id) => setRuta({ p: 'usuario', id })} />}
        {ruta.p === 'usuario' && <UsuarioDetalle id={ruta.id} volver={() => setRuta({ p: 'usuarios' })} />}
        {ruta.p === 'correos' && <Correos />}
        {ruta.p === 'conversaciones' && <Conversaciones />}
        {ruta.p === 'audios' && <Audios />}
      </main>
    </div>
  )
}
