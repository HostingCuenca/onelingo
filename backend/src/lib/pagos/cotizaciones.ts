/**
 * Plan Empresarial: solicitudes de cotización (tabla `cotizaciones`). La app
 * las envía con o sin sesión; el administrador las atiende desde el panel.
 */
import { z } from 'zod';
import { query, uno } from '../db.js';
import { enviarCorreo, esc, plantilla } from '../correo.js';
import { CODIGOS_IDIOMA } from './suscripciones.js';

export const ESTADOS_COTIZACION = ['nueva', 'contactada', 'cerrada'] as const;
export const CotizacionEntrada = z.object({
  empresa: z.string().trim().min(1, 'Escribe el nombre de la empresa').max(160),
  empleados: z.number().int().min(1, 'Indica cuántos empleados').max(1_000_000),
  idiomas: z.array(z.enum(CODIGOS_IDIOMA)).min(1, 'Elige al menos un idioma').max(10),
  mensaje: z.string().trim().max(2000).default(''),
  nombre: z.string().trim().max(120).default(''),
  email: z.string().trim().toLowerCase().email('Correo no válido').max(200),
  telefono: z.string().trim().max(40).default(''),
});
export const CotizacionCambios = z.object({ estado: z.enum(ESTADOS_COTIZACION).optional(), nota: z.string().max(2000).optional() });

/** Guarda la solicitud y confirma al solicitante por correo (si falla el correo, la solicitud queda igual). */
export async function crearCotizacion(d: z.infer<typeof CotizacionEntrada>, usuarioId: string | null) {
  const f = await uno<{ id: string }>(`INSERT INTO cotizaciones (empresa, empleados, idiomas, mensaje, nombre, email, telefono, usuario_id)
    VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id`, [d.empresa, d.empleados, [...new Set(d.idiomas)], d.mensaje, d.nombre, d.email, d.telefono, usuarioId]);
  await enviarCorreo(d.email, 'Recibimos tu solicitud de OneLingo para empresas', plantilla('Gracias por tu interés',
    `Recibimos la solicitud de cotización para <b>${esc(d.empresa)}</b> (${d.empleados} ${d.empleados === 1 ? 'persona' : 'personas'}). Te escribiremos a este correo con una propuesta.`))
    .catch(() => false);
  return { id: Number(f!.id) };
}

export async function listarCotizaciones(estado = '') {
  const filas = await query(`SELECT * FROM cotizaciones WHERE ($1 = '' OR estado = $1) ORDER BY creado_en DESC LIMIT 500`, [estado]);
  const [n] = await query<{ nuevas: number }>(`SELECT count(*) FILTER (WHERE estado = 'nueva')::int AS nuevas FROM cotizaciones`);
  return {
    nuevas: n?.nuevas ?? 0,
    cotizaciones: filas.map((f) => ({
      id: Number(f.id), empresa: f.empresa, empleados: f.empleados, idiomas: f.idiomas, mensaje: f.mensaje, nombre: f.nombre, email: f.email,
      telefono: f.telefono, usuarioId: f.usuario_id, estado: f.estado, nota: f.nota, creadoEn: f.creado_en, actualizadoEn: f.actualizado_en,
    })),
  };
}

export async function actualizarCotizacion(id: number, d: z.infer<typeof CotizacionCambios>) {
  return uno(`UPDATE cotizaciones SET estado = coalesce($2, estado), nota = coalesce($3, nota), actualizado_en = now() WHERE id = $1 RETURNING id`,
    [id, d.estado ?? null, d.nota ?? null]);
}
