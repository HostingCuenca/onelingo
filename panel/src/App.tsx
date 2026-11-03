import { useEffect, useState } from 'react'
import { api, guardarToken, token, SESION_CADUCADA } from './api'
import Resumen from './paginas/Resumen'
import Usuarios from './paginas/Usuarios'
import UsuarioDetalle from './paginas/UsuarioDetalle'
import Correos from './paginas/Correos'
import Conversaciones from './paginas/Conversaciones'
import Audios from './paginas/Audios'
import Conexiones from './paginas/Conexiones'
import Planes from './paginas/Planes'
import Suscripciones from './paginas/Suscripciones'
import Cotizaciones from './paginas/Cotizaciones'
import ReportesIA from './paginas/ReportesIA'
import TutorIA from './paginas/TutorIA'

const LOGO = `${import.meta.env.BASE_URL}logo-panel.webp`

type Ruta = { p: 'resumen' } | { p: 'usuarios' } | { p: 'usuario'; id: string; desde?: 'usuarios' | 'suscripciones' | 'reportes' } | { p: 'correos' } | { p: 'conversaciones' } | { p: 'audios' } | { p: 'conexiones' } | { p: 'planes' } | { p: 'suscripciones' } | { p: 'cotizaciones' } | { p: 'reportes' } | { p: 'tutor' }

const TITULOS: Record<Ruta['p'], string> = {
  resumen: 'Resumen', usuarios: 'Alumnos', usuario: 'Alumno', planes: 'Planes', suscripciones: 'Suscripciones', cotizaciones: 'Cotizaciones', reportes: 'Reportes IA', tutor: 'Tutor IA',
  conversaciones: 'Conversaciones IA', audios: 'Voz y audios', conexiones: 'Conexiones', correos: 'Correos',
}

function Login({ onOk, aviso }: { onOk: () => void; aviso?: string }) {
  const [usuario, setUsuario] = useState('admin'); const [pin, setPin] = useState(''); const [err, setErr] = useState(''); const [ocupado, setOcupado] = useState(false)
  const entrar = async (e: React.FormEvent) => {
    e.preventDefault(); setErr(''); setOcupado(true)
    try { const r = await api<{ token: string }>('/admin/login', { metodo: 'POST', cuerpo: { usuario: usuario.trim(), pin: pin.trim() } }); guardarToken(r.token); onOk() }
    catch (x: any) { setErr(x.message) } finally { setOcupado(false) }
  }
  return (
    <form className="login" onSubmit={entrar}>
      <img className="logo-login" src={LOGO} alt="OneLingo" width={77} height={72} />
      <h1>One<span style={{ color: 'var(--morado)' }}>Lingo</span> · Panel</h1>
      <p className="muted">Administración de alumnos y progreso</p>
      {aviso && !err && <div className="aviso-login">{aviso}</div>}
      <input value={usuario} onChange={(e) => setUsuario(e.target.value)} placeholder="Usuario" aria-label="Usuario" autoComplete="username" autoCapitalize="none" autoCorrect="off" spellCheck={false} />
      <input value={pin} onChange={(e) => setPin(e.target.value)} placeholder="PIN" aria-label="PIN" type="password" autoComplete="current-password" />
      {err && <div className="err">{err}</div>}
      <button disabled={ocupado}>{ocupado ? 'Entrando…' : 'Entrar'}</button>
    </form>
  )
}

export default function App() {
  const [sesion, setSesion] = useState(!!token())
  const [ruta, setRutaBase] = useState<Ruta>({ p: 'resumen' })
  const [menu, setMenu] = useState(false)
  const setRuta = (r: Ruta) => { setRutaBase(r); setMenu(false); window.scrollTo(0, 0) }
  useEffect(() => {
    if (!menu) return
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setMenu(false) }
    window.addEventListener('keydown', onKey); document.body.classList.add('sin-scroll')
    return () => { window.removeEventListener('keydown', onKey); document.body.classList.remove('sin-scroll') }
  }, [menu])
  const [aviso, setAviso] = useState('')
  useEffect(() => {
    // Cualquier 401 de la API (token caducado o inválido) devuelve al login, sin dejar al usuario atascado.
    const caducada = () => { setSesion(false); setMenu(false); setAviso('Tu sesión expiró. Vuelve a entrar.') }
    window.addEventListener(SESION_CADUCADA, caducada); return () => window.removeEventListener(SESION_CADUCADA, caducada)
  }, [])
  if (!sesion) return <Login aviso={aviso} onOk={() => { setAviso(''); setRutaBase({ p: 'resumen' }); setSesion(true) }} />
  const titulo = TITULOS[ruta.p]
  return (
    <div className={menu ? 'app menu-abierto' : 'app'}>
      <header className="barra-movil">
        <button className="hamburguesa" aria-label={menu ? 'Cerrar menú' : 'Abrir menú'} aria-expanded={menu} aria-controls="menu-lateral" onClick={() => setMenu(!menu)}>
          <span /><span /><span />
        </button>
        <img src={LOGO} alt="" width={28} height={26} />
        <span className="titulo-movil">{titulo}</span>
      </header>
      <div className="velo" onClick={() => setMenu(false)} />
      <aside id="menu-lateral">
        <div className="marca"><img src={LOGO} alt="" width={34} height={32} /><span>One<b>Lingo</b> · Panel</span><button className="cerrar-menu" aria-label="Cerrar menú" onClick={() => setMenu(false)}>×</button></div>
        <a className={ruta.p === 'resumen' ? 'activo' : ''} onClick={() => setRuta({ p: 'resumen' })}>Resumen</a>
        <a className={ruta.p === 'usuarios' || ruta.p === 'usuario' ? 'activo' : ''} onClick={() => setRuta({ p: 'usuarios' })}>Alumnos</a>
        <a className={ruta.p === 'planes' ? 'activo' : ''} onClick={() => setRuta({ p: 'planes' })}>Planes</a>
        <a className={ruta.p === 'suscripciones' ? 'activo' : ''} onClick={() => setRuta({ p: 'suscripciones' })}>Suscripciones</a>
        <a className={ruta.p === 'cotizaciones' ? 'activo' : ''} onClick={() => setRuta({ p: 'cotizaciones' })}>Cotizaciones</a>
        <a className={ruta.p === 'tutor' ? 'activo' : ''} onClick={() => setRuta({ p: 'tutor' })}>Tutor IA</a>
        <a className={ruta.p === 'conversaciones' ? 'activo' : ''} onClick={() => setRuta({ p: 'conversaciones' })}>Conversaciones IA</a>
        <a className={ruta.p === 'reportes' ? 'activo' : ''} onClick={() => setRuta({ p: 'reportes' })}>Reportes IA</a>
        <a className={ruta.p === 'audios' ? 'activo' : ''} onClick={() => setRuta({ p: 'audios' })}>Voz y audios</a>
        <a className={ruta.p === 'conexiones' ? 'activo' : ''} onClick={() => setRuta({ p: 'conexiones' })}>Conexiones</a>
        <a className={ruta.p === 'correos' ? 'activo' : ''} onClick={() => setRuta({ p: 'correos' })}>Correos</a>
        <div className="pie"><span className="api">API: {import.meta.env.DEV ? 'localhost:8091' : 'misma raíz'}<br /></span><button className="sec" onClick={() => { guardarToken(null); setAviso(''); setMenu(false); setSesion(false) }}>Salir</button></div>
      </aside>
      <main>
        {ruta.p === 'resumen' && <Resumen />}
        {ruta.p === 'usuarios' && <Usuarios abrir={(id) => setRuta({ p: 'usuario', id })} />}
        {ruta.p === 'usuario' && <UsuarioDetalle id={ruta.id} desde={ruta.desde ?? 'usuarios'} volver={() => setRuta({ p: ruta.desde ?? 'usuarios' })} />}
        {ruta.p === 'planes' && <Planes />}
        {ruta.p === 'suscripciones' && <Suscripciones abrir={(id) => setRuta({ p: 'usuario', id, desde: 'suscripciones' })} />}
        {ruta.p === 'cotizaciones' && <Cotizaciones />}
        {ruta.p === 'correos' && <Correos />}
        {ruta.p === 'conversaciones' && <Conversaciones />}
        {ruta.p === 'tutor' && <TutorIA />}
        {ruta.p === 'reportes' && <ReportesIA abrirAlumno={(id) => setRuta({ p: 'usuario', id, desde: 'reportes' })} />}
        {ruta.p === 'audios' && <Audios />}
        {ruta.p === 'conexiones' && <Conexiones />}
      </main>
    </div>
  )
}
