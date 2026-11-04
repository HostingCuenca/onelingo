import type { FastifyInstance } from 'fastify';
import { randomInt } from 'node:crypto';
import { z } from 'zod';
import { query, uno } from '../lib/db.js';
import { requiereAdmin, requiereAlumno, type Sesion } from '../lib/auth.js';
import { config } from '../lib/config.js';
import { esc } from '../lib/correo.js';

/**
 * Certificado de nivel: al superar un nivel N1–N10 de la ruta (todas sus
 * clases o su prueba) el alumno recibe un certificado con su nombre y una
 * dirección pública para verificarlo, descargarlo en PDF o compartirlo.
 * El servidor solo lo emite si el progreso sincronizado lo confirma.
 */
const IDIOMAS: Record<string, { es: string; en: string }> = {
  en: { es: 'inglés', en: 'English' }, es: { es: 'español', en: 'Spanish' }, fr: { es: 'francés', en: 'French' },
  de: { es: 'alemán', en: 'German' }, pt: { es: 'portugués', en: 'Portuguese' }, it: { es: 'italiano', en: 'Italian' },
  zh: { es: 'chino mandarín', en: 'Mandarin Chinese' }, ja: { es: 'japonés', en: 'Japanese' }, ko: { es: 'coreano', en: 'Korean' }, ru: { es: 'ruso', en: 'Russian' },
};
type Lengua = 'es' | 'en';
type Via = 'clases' | 'prueba';
export type Certificado = { codigo: string; idioma: string; nivel: string; nombre: string; via: Via; lengua: Lengua; logrado_en: string | null; emitido_en: string };

const Pedido = z.object({
  idioma: z.enum(Object.keys(IDIOMAS) as [string, ...string[]]),
  nivel: z.string().regex(/^n([1-9]|10)$/),
  nombre: z.string().max(120).optional(),
  lengua: z.enum(['es', 'en']).default('es'),
});

/** Sin letras que se confunden (0/O, 1/I/L): se dicta y se copia bien. */
const ALFABETO = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
export const nuevoCodigo = () => {
  const c = Array.from({ length: 10 }, () => ALFABETO[randomInt(ALFABETO.length)]).join('');
  return `${c.slice(0, 5)}-${c.slice(5)}`;
};

/** Nombre tal como irá impreso: sin espacios de más y, si es un correo, la parte antes de la @. */
export function nombreCertificado(n: string) {
  const limpio = n.trim().replace(/\s+/g, ' ');
  return (limpio.includes('@') ? limpio.split('@')[0] : limpio).slice(0, 80);
}

/** Cómo superó el nivel según su progreso (claves de `ClaveRuta` en la app) y cuándo. */
export function nivelSuperado(practicas: Record<string, any>, idioma: string, nivel: string): { via: Via; fecha: string | null } | null {
  const completa = practicas[`ruta:${idioma}.${nivel}:completa`];
  if (completa && typeof completa === 'object') return { via: 'clases', fecha: completa.primeraFecha ?? completa.fecha ?? null };
  const prueba = practicas[`ruta:${idioma}.${nivel}:prueba`];
  if (prueba?.aprobada === true) return { via: 'prueba', fecha: prueba.aprobadaEn ?? prueba.fecha ?? null };
  return null;
}

export const urlCertificado = (codigo: string) => `${config.publicUrl}/certificado/${codigo}`;
const salida = (c: Certificado) => ({
  codigo: c.codigo, idioma: c.idioma, nivel: c.nivel, nombre: c.nombre, via: c.via, lengua: c.lengua,
  logradoEn: c.logrado_en, emitidoEn: c.emitido_en, url: urlCertificado(c.codigo),
});

const TEXTOS = {
  es: {
    titulo: 'Certificado de nivel', otorga: 'Se otorga a', fecha: 'Fecha', codigo: 'Código', verifica: 'Verificación',
    clases: (n: number, i: string) => `por completar el <b>Nivel ${n}</b> del curso de <b>${i}</b> de OneLingo.`,
    prueba: (n: number, i: string) => `por aprobar la prueba del <b>Nivel ${n}</b> del curso de <b>${i}</b> de OneLingo.`,
    aclara: 'Acredita un nivel del curso de OneLingo. No es una certificación oficial del Marco Común Europeo (MCER).',
    nota: 'Este certificado fue emitido por OneLingo y es auténtico mientras se pueda ver en esta dirección.',
    pdf: 'Descargar PDF', compartir: 'Compartir', copiado: 'Enlace copiado',
    noExiste: 'Certificado no encontrado', noExisteTexto: 'Este código no corresponde a ningún certificado de OneLingo.',
  },
  en: {
    titulo: 'Level certificate', otorga: 'Awarded to', fecha: 'Date', codigo: 'Code', verifica: 'Verify at',
    clases: (n: number, i: string) => `for completing <b>Level ${n}</b> of the OneLingo <b>${i}</b> course.`,
    prueba: (n: number, i: string) => `for passing the <b>Level ${n}</b> test of the OneLingo <b>${i}</b> course.`,
    aclara: 'Recognizes a level of the OneLingo course. It is not an official CEFR certification.',
    nota: 'This certificate was issued by OneLingo and is authentic as long as it can be viewed at this address.',
    pdf: 'Download PDF', compartir: 'Share', copiado: 'Link copied',
    noExiste: 'Certificate not found', noExisteTexto: 'This code does not match any OneLingo certificate.',
  },
};

const fechaLarga = (iso: string, l: Lengua) =>
  new Intl.DateTimeFormat(l === 'en' ? 'en-US' : 'es', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'America/Bogota' }).format(new Date(iso));

const ESTILO = `
:root{--morado:#4519BB;--morado-suave:#EEE8FB;--amarillo:#FFD23F;--tinta:#1c1b1b;--gris:#6e6979;--fondo:#F4F1FA}
*{box-sizing:border-box}body{margin:0;background:var(--fondo);color:var(--tinta);font-family:Nunito,system-ui,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
main{max-width:980px;margin:0 auto;padding:32px 16px}
.cert{position:relative;background:#fff;border-radius:18px;padding:14px;box-shadow:0 1px 0 rgba(0,0,0,.04)}
.marco{border:2px solid var(--morado);border-radius:12px;padding:44px 52px;aspect-ratio:1.414;display:flex;flex-direction:column;position:relative;overflow:hidden}
.marco:before{content:"";position:absolute;inset:6px;border:1px solid var(--morado-suave);border-radius:8px;pointer-events:none}
.cab{display:flex;justify-content:space-between;align-items:center}
.marca{font-size:28px;font-weight:900;letter-spacing:-.5px}.marca span{color:var(--morado)}
.etiqueta{font-size:13px;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:var(--morado)}
.centro{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:10px}
.sello{width:96px;height:96px;border-radius:50%;background:var(--amarillo);display:grid;place-items:center;font-weight:900;font-size:34px;color:var(--morado);box-shadow:0 0 0 6px #fff,0 0 0 8px var(--amarillo);margin-bottom:8px}
.otorga{font-size:15px;color:var(--gris);font-weight:700;text-transform:uppercase;letter-spacing:2px}
h1{font-size:clamp(30px,6vw,54px);line-height:1.1;margin:0;font-weight:900;padding:0 0 12px;border-bottom:2px solid var(--amarillo);max-width:100%;overflow-wrap:anywhere}
.motivo{font-size:19px;line-height:1.5;max-width:620px;margin:6px 0 0}
.pie{display:grid;grid-template-columns:1fr 1fr 2fr;gap:16px;border-top:1px solid #e7e3ee;padding-top:16px;font-size:14px}
.pie div b{display:block;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:var(--gris);margin-bottom:2px}
.pie .mono{font-family:ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
.aclara{font-size:11.5px;color:var(--gris);margin:12px 0 0;text-align:center}
.acciones{display:flex;gap:10px;justify-content:center;margin:22px 0 8px;flex-wrap:wrap}
button{font:inherit;font-weight:800;font-size:16px;border-radius:12px;padding:12px 22px;cursor:pointer;border:2px solid var(--morado)}
.primario{background:var(--morado);color:#fff}.secundario{background:#fff;color:var(--morado)}
.nota{text-align:center;color:var(--gris);font-size:14px;margin:0}
@media (max-width:700px){main{padding:16px}.marco{aspect-ratio:auto;padding:28px 20px;gap:22px}.cab{flex-direction:column;gap:6px}.pie{grid-template-columns:1fr 1fr}.pie div:last-child{grid-column:1/-1}.motivo{font-size:17px}}
@page{size:A4 landscape;margin:0}
@media print{body{background:#fff}main{max-width:none;padding:0}.cert{border-radius:0;padding:8mm;height:100vh;box-shadow:none}.marco{height:100%;aspect-ratio:auto}.acciones,.nota{display:none}}`;

function pagina(titulo: string, cuerpo: string, l: Lengua, extraHead = '') {
  return `<!doctype html><html lang="${l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>${titulo}</title>${extraHead}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap" rel="stylesheet">
<style>${ESTILO}</style></head><body><main>${cuerpo}</main></body></html>`;
}

export function htmlCertificado(c: Certificado) {
  const l = c.lengua, t = TEXTOS[l], n = Number(c.nivel.slice(1)), idioma = IDIOMAS[c.idioma]?.[l] ?? c.idioma, url = urlCertificado(c.codigo);
  const titulo = `${t.titulo} · ${esc(c.nombre)} · OneLingo`;
  const og = `<meta property="og:title" content="${titulo}"><meta property="og:description" content="${esc((c.via === 'prueba' ? t.prueba : t.clases)(n, idioma).replace(/<\/?b>/g, ''))}">`;
  return pagina(titulo, `
<section class="cert"><div class="marco">
  <div class="cab"><div class="marca">One<span>Lingo</span></div><div class="etiqueta">${t.titulo}</div></div>
  <div class="centro">
    <div class="sello">N${n}</div>
    <div class="otorga">${t.otorga}</div>
    <h1>${esc(c.nombre)}</h1>
    <p class="motivo">${(c.via === 'prueba' ? t.prueba : t.clases)(n, esc(idioma))}</p>
  </div>
  <div class="pie">
    <div><b>${t.fecha}</b>${fechaLarga(c.logrado_en ?? c.emitido_en, l)}</div>
    <div><b>${t.codigo}</b><span class="mono">${c.codigo}</span></div>
    <div><b>${t.verifica}</b><span class="mono">${esc(url.replace(/^https?:\/\//, ''))}</span></div>
  </div>
  <p class="aclara">${t.aclara}</p>
</div></section>
<div class="acciones"><button class="primario" onclick="print()">${t.pdf}</button><button class="secundario" id="compartir">${t.compartir}</button></div>
<p class="nota">${t.nota}</p>
<script>document.getElementById('compartir').onclick=async e=>{const u=${JSON.stringify(url)};try{if(navigator.share){await navigator.share({title:document.title,url:u});return}await navigator.clipboard.writeText(u);e.target.textContent=${JSON.stringify(t.copiado)}}catch(_){}}</script>`, l, og);
}

export default async function rutas(app: FastifyInstance) {
  /** Emite (o devuelve) el certificado de un nivel superado. Con `nombre` corrige el impreso. */
  app.post('/certificados', { preHandler: requiereAlumno }, async (req, reply) => {
    const s = req.user as Sesion;
    const d = Pedido.parse(req.body);
    const [usuario, progreso] = await Promise.all([
      uno<{ nombre: string }>('SELECT nombre FROM usuarios WHERE id = $1', [s.sub]),
      uno<{ estado: any }>('SELECT estado FROM progreso WHERE usuario_id = $1', [s.sub]),
    ]);
    if (!usuario) return reply.code(404).send({ error: 'usuario_no_existe' });
    const logro = nivelSuperado(progreso?.estado?.practicas ?? {}, d.idioma, d.nivel);
    if (!logro) return reply.code(409).send({ error: 'nivel_no_superado' });
    const nombre = nombreCertificado(d.nombre ?? '') || nombreCertificado(usuario.nombre) || 'OneLingo';
    // El código y la fecha del logro no cambian al corregir el nombre o la lengua.
    for (let i = 0; i < 3; i++) {
      try {
        const c = await uno<Certificado>(`INSERT INTO certificados (codigo, usuario_id, idioma, nivel, nombre, via, lengua, logrado_en)
          VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
          ON CONFLICT (usuario_id, idioma, nivel) DO UPDATE SET nombre = CASE WHEN $9 THEN EXCLUDED.nombre ELSE certificados.nombre END, lengua = EXCLUDED.lengua
          RETURNING *`, [nuevoCodigo(), s.sub, d.idioma, d.nivel, nombre, logro.via, d.lengua, logro.fecha, d.nombre != null && nombreCertificado(d.nombre) !== '']);
        return salida(c!);
      } catch (e: any) {
        if (e?.code !== '23505' || i === 2) throw e; // choque de código: otro intento
      }
    }
  });

  app.get('/certificados/me', { preHandler: requiereAlumno }, async (req) => {
    const s = req.user as Sesion;
    const filas = await query<Certificado>('SELECT * FROM certificados WHERE usuario_id = $1 ORDER BY idioma, emitido_en', [s.sub]);
    return { certificados: filas.map(salida) };
  });

  app.get('/admin/usuarios/:id/certificados', { preHandler: requiereAdmin }, async (req) => {
    const { id } = z.object({ id: z.string().uuid() }).parse(req.params);
    const filas = await query<Certificado>('SELECT * FROM certificados WHERE usuario_id = $1 ORDER BY idioma, emitido_en', [id]);
    return { certificados: filas.map(salida) };
  });

  /** Página pública: verificación, PDF (imprimir) y compartir. */
  app.get('/certificado/:codigo', async (req, reply) => {
    const { codigo } = z.object({ codigo: z.string().max(20) }).parse(req.params);
    const c = await uno<Certificado>('SELECT * FROM certificados WHERE codigo = $1', [codigo.toUpperCase()]);
    reply.type('text/html; charset=utf-8');
    if (!c) {
      const t = TEXTOS.es;
      return reply.code(404).send(pagina(t.noExiste, `<section class="cert"><div class="marco" style="aspect-ratio:auto;align-items:center;text-align:center;gap:10px">
        <div class="marca">One<span>Lingo</span></div><h1 style="font-size:28px;border:0">${t.noExiste}</h1><p class="motivo">${t.noExisteTexto}</p></div></section>`, 'es'));
    }
    return htmlCertificado(c);
  });
}
