/** Error al cargar una página, siempre con salida: reintentar. */
export default function ErrorCarga({ msg, reintentar }: { msg: string; reintentar: () => void }) {
  return <div className="tarjeta carga-err"><p className="err">{msg}</p><button className="sec" onClick={reintentar}>Reintentar</button></div>
}
