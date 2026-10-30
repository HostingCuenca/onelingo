import nodemailer from 'nodemailer';
import { config } from './config.js';
import { query } from './db.js';

// El correo sale por el Postfix del propio servidor (127.0.0.1:25, sin usuario
// ni TLS) o por un SMTP externo con usuario y contraseña.
const local = ['127.0.0.1', 'localhost'].includes(config.smtp.host);
const transporte = config.smtp.host
  ? nodemailer.createTransport({
    host: config.smtp.host, port: config.smtp.port, secure: config.smtp.port === 465, ignoreTLS: local,
    ...(config.smtp.user ? { auth: { user: config.smtp.user, pass: config.smtp.pass } } : {}),
  })
  : null;

/** Envía un correo; sin SMTP configurado lo deja en la bandeja `correos` (visible en el panel). */
export async function enviarCorreo(para: string, asunto: string, html: string) {
  let enviado = false, detalle = '';
  if (transporte) {
    try { const r = await transporte.sendMail({ from: config.smtp.from, to: para, subject: asunto, html }); enviado = true; detalle = r.messageId ?? ''; }
    catch (e) { detalle = String(e); }
  } else {
    detalle = 'SMTP no configurado: correo guardado solo en la bandeja del panel';
  }
  await query('INSERT INTO correos (para, asunto, cuerpo, enviado, detalle) VALUES ($1,$2,$3,$4,$5)', [para, asunto, html, enviado, detalle]);
  return enviado;
}

/** Escapa texto del usuario (nombres) antes de meterlo en el HTML. */
export const esc = (t: string) =>
  t.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);

export const plantilla = (titulo: string, cuerpo: string, boton?: { texto: string; url: string }) => `
<div style="font-family:Arial,sans-serif;max-width:520px;margin:0 auto;padding:24px;color:#1c1b1b">
  <div style="font-size:22px;font-weight:800;margin-bottom:12px">One<span style="color:#4519BB">Lingo</span></div>
  <h2 style="font-size:18px;margin:0 0 10px">${titulo}</h2>
  <p style="line-height:1.5">${cuerpo}</p>
  ${boton ? `<p style="margin:22px 0"><a href="${boton.url}" style="background:#4519BB;color:#fff;text-decoration:none;padding:12px 20px;border-radius:10px;font-weight:700">${boton.texto}</a></p><p style="font-size:12px;color:#6e6979">Si el botón no funciona, copia este enlace: ${boton.url}</p>` : ''}
</div>`;

/** Correo con un código de un solo uso, grande y fácil de copiar. */
export const plantillaCodigo = (titulo: string, cuerpo: string, codigo: string, idioma: 'es' | 'en' = 'es') => plantilla(titulo, `${cuerpo}</p>
  <p style="font-size:34px;font-weight:800;letter-spacing:10px;color:#4519BB;margin:18px 0">${codigo}</p>
  <p style="font-size:13px;color:#6e6979">${idioma === 'en'
    ? 'It is valid for 10 minutes. If this wasn\'t you, ignore this email: no one can get in without the code.'
    : 'Vale 10 minutos. Si no fuiste tú, ignora este correo: nadie puede entrar sin el código.'}`);
