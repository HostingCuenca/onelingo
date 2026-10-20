import { useEffect, useState } from 'react'
import { api, guardarToken, token } from './api'
import Resumen from './paginas/Resumen'
import Usuarios from './paginas/Usuarios'
import UsuarioDetalle from './paginas/UsuarioDetalle'
import Correos from './paginas/Correos'
import Conversaciones from './paginas/Conversaciones'
import Audios from './paginas/Audios'
import Conexiones from './paginas/Conexiones'
import Planes from './paginas/Planes'
import Suscripciones from './paginas/Suscripciones'

const LOGO = `${import.meta.env.BASE_URL}logo-panel.webp`

type Ruta = { p: 'resumen' } | { p: 'usuarios' } | { p: 'usuario'; id: string; desde?: 'usuarios' | 'suscripciones' } | { p: 'correos' } | { p: 'conversaciones' } | { p: 'audios' } | { p: 'conexiones' } | { p: 'planes' } | { p: 'suscripciones' }

function Login({ onOk }: { onOk: () => void }) {
  const [usuario, setUsuario] = useState('admin'); const [pin, setPin] = useState(''); const [err, setErr] = useState('')
  const entrar = async (e: React.FormEvent) => {
    e.preventDefault()
    try { const r = await api<{ token: string }>('/admin/login', { metodo: 'POST', cuerpo: { usuario, pin } }); guardarToken(r.token); onOk() }
    catch (x: any) { setErr(x.message) }
  }
  return (
    <form className="login" onSubmit={entrar}>
      <img className="logo-login" src={LOGO} alt="OneLingo" width={77} height={72} />
      <h1>One<span style={{ color: 'var(--morado)' }}>Lingo</span> · Panel</h1>
      <p className="muted">Administración de alumnos y progreso</p>
      <input value={usuario} onChange={(e) => setUsuario(e.target.value)} placeholder="Usuario" />
      <input value={pin} onChange={(e) => setPin(e.target.value)} placeholder="PIN" type="password" />
      {err && <div className="err">{err}</div>}
      <button>Entrar</button>
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
        <div className="marca"><img src={LOGO} alt="" width={34} height={32} /><span>One<b>Lingo</b> · Panel</span></div>
        <a className={ruta.p === 'resumen' ? 'activo' : ''} onClick={() => setRuta({ p: 'resumen' })}>Resumen</a>
        <a className={ruta.p === 'usuarios' || ruta.p === 'usuario' ? 'activo' : ''} onClick={() => setRuta({ p: 'usuarios' })}>Alumnos</a>
        <a className={ruta.p === 'planes' ? 'activo' : ''} onClick={() => setRuta({ p: 'planes' })}>Planes</a>
        <a className={ruta.p === 'suscripciones' ? 'activo' : ''} onClick={() => setRuta({ p: 'suscripciones' })}>Suscripciones</a>
        <a className={ruta.p === 'conversaciones' ? 'activo' : ''} onClick={() => setRuta({ p: 'conversaciones' })}>Conversaciones IA</a>
        <a className={ruta.p === 'audios' ? 'activo' : ''} onClick={() => setRuta({ p: 'audios' })}>Voz y audios</a>
        <a className={ruta.p === 'conexiones' ? 'activo' : ''} onClick={() => setRuta({ p: 'conexiones' })}>Conexiones</a>
        <a className={ruta.p === 'correos' ? 'activo' : ''} onClick={() => setRuta({ p: 'correos' })}>Correos</a>
        <div className="pie"><span className="api">API: {import.meta.env.DEV ? 'localhost:8091' : 'misma raíz'}<br /></span><button className="sec" onClick={() => { guardarToken(null); setSesion(false) }}>Salir</button></div>
      </aside>
      <main>
        {ruta.p === 'resumen' && <Resumen />}
        {ruta.p === 'usuarios' && <Usuarios abrir={(id) => setRuta({ p: 'usuario', id })} />}
        {ruta.p === 'usuario' && <UsuarioDetalle id={ruta.id} desde={ruta.desde ?? 'usuarios'} volver={() => setRuta({ p: ruta.desde ?? 'usuarios' })} />}
        {ruta.p === 'planes' && <Planes />}
        {ruta.p === 'suscripciones' && <Suscripciones abrir={(id) => setRuta({ p: 'usuario', id, desde: 'suscripciones' })} />}
        {ruta.p === 'correos' && <Correos />}
        {ruta.p === 'conversaciones' && <Conversaciones />}
        {ruta.p === 'audios' && <Audios />}
        {ruta.p === 'conexiones' && <Conexiones />}
      </main>
    </div>
  )
}
