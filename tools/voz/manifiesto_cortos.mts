/**
 * Manifiesto de audios cortos para pregenerar y verificar (tools/voz/pregenerar_cortos.py).
 * Una letra o sílaba suelta sale muda o mal en la voz (auditoría 2026-10-13), así que
 * se generan aparte, se transcriben de vuelta y la toma buena queda en la caché del
 * servidor con la misma clave que usaría `/voz` (texto normalizado + voz + modelo + idioma).
 *
 *   cd backend && npx tsx ../tools/voz/manifiesto_cortos.mts [modelo] > /tmp/manifiesto.json
 */
import { readFileSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { hashAudio, rolDeVoz, textoParaVoz, VOCES } from '../../backend/src/lib/voz.ts';
import { nombreLetra } from '../../backend/src/lib/voz_texto.ts';

const RAIZ = path.resolve(import.meta.dirname, '../../assets/contenido');
const MODELO = process.argv[2] ?? 'eleven_flash_v2_5';
const IDIOMAS = ['en', 'es', 'fr', 'de', 'pt', 'it', 'ru', 'ko', 'ja', 'zh'];
/** Campos que la app lee en voz alta (en el Nivel 0, las fichas, grafías y sonidos no se oyen). */
const VOZ = new Set(['texto', 'audio', 'pregunta', 'opciones', 'respuesta', 'tokens', 'correcto', 'aceptadas', 'frases', 'vocab']);
const VOZ_N0 = new Set(['m', 'texto', 'audio', 'palabra', 'palabras', 'de', 'a', 'ancla', 'ejemplos', 't']);
/** Pasos del Nivel 0 cuyas opciones se oyen al tocarlas (en los demás son letras o piezas mudas). */
const OPCIONES_CON_VOZ = new Set(['escucha_elige', 'toca_sonido', 'lee', 'elige_significado']);
const LETRAS_N0 = new Set(['letras', 'letra']);
const CJK = /[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Hangul}]/u;

type Caso = { idioma: string; texto: string; modo?: string; normalizado: string; esperado: string[]; rol: string; voz_id: string; hash: string };

function archivos(dir: string): string[] {
  return readdirSync(dir).flatMap((f) => {
    const p = path.join(dir, f);
    return statSync(p).isDirectory() ? archivos(p) : p.endsWith('.json') ? [p] : [];
  });
}

/** Marcado del Nivel 0 a texto plano: «(sh:ʃ)ip» → «ship», «_» muda, «=» dígrafo. */
const plano = (s: string) => s.replace(/\(([^:()]*):[^()]*\)/g, '$1').replace(/[_=*]/g, '');

const soloLetras = (t: string) => {
  const piezas = t.split(/[\s,\-–]+/).filter(Boolean);
  return piezas.length > 0 && piezas.every((p) => [...p].length === 1 && /\p{L}/u.test(p));
};

const casos = new Map<string, Caso>();
function anotar(idioma: string, texto: string, voz: string, modo?: string) {
  const normalizado = textoParaVoz(texto, idioma, modo);
  const letras = normalizado.replace(/[\s\p{P}]/gu, '');
  // Sílaba suelta (kana, hangul, hanzi) o palabra de hasta dos letras.
  if (!letras || (!modo && [...letras].length > (CJK.test(letras) ? 1 : 2))) return;
  if (modo && [...texto.replace(/[\s\p{P}]/gu, '')].length > 1) return; // secuencias: se oyen bien
  const rol = rolDeVoz(voz, idioma);
  const v = VOCES[rol];
  const hash = hashAudio(normalizado, v.id, MODELO, idioma);
  if (casos.has(hash)) return;
  const base = texto.replace(/[\s\p{P}]/gu, '');
  const esperado = modo ? [base, nombreLetra(base, idioma), normalizado.replace(/[.。]$/u, '')] : [letras];
  casos.set(hash, { idioma, texto, ...(modo ? { modo } : {}), normalizado, esperado: [...new Set(esperado.map((e) => e.toLowerCase()))], rol, voz_id: v.id, hash });
}

for (const idioma of IDIOMAS) {
  const dir = path.join(RAIZ, idioma);
  const n0 = JSON.parse(readFileSync(path.join(dir, 'nivel0', 'nivel0.json'), 'utf8'));
  const vozN0: string = n0.voz ?? 'sofia';
  for (const f of archivos(dir)) {
    const enN0 = f.includes(`${path.sep}nivel0${path.sep}`);
    const voz = enN0 ? vozN0 : 'narradora';
    const recorrer = (x: unknown, clave = ''): void => {
      if (Array.isArray(x)) return x.forEach((v) => recorrer(v, clave));
      if (x && typeof x === 'object') {
        const o = x as Record<string, unknown>;
        if (enN0 && o.tipo === 'deletreo' && typeof o.palabra === 'string') for (const l of o.palabra) anotar(idioma, l, voz, 'letra');
        if (enN0 && OPCIONES_CON_VOZ.has(String(o.tipo)) && Array.isArray(o.opciones)) {
          for (const op of o.opciones) {
            const t = typeof op === 'string' ? op : (op as { m?: string })?.m;
            if (t) anotar(idioma, plano(t), voz, soloLetras(plano(t)) ? 'letra' : undefined);
          }
        }
        for (const [k, v] of Object.entries(o)) {
          if (k === 'es' || k === 'en' || k.endsWith('Rom')) continue;
          // Las claves que no se leen se recorren igual: pueden contener pasos o ítems.
          recorrer(v, typeof v === 'string' || (Array.isArray(v) && v.every((e) => typeof e === 'string')) ? k : '');
        }
        return;
      }
      if (typeof x !== 'string' || !x.trim()) return;
      if (enN0 && LETRAS_N0.has(clave)) return anotar(idioma, x, voz, 'letra');
      // Como `decir` (palabra_color.dart): solo letras sueltas → por su nombre.
      if (enN0 && soloLetras(plano(x))) return anotar(idioma, plano(x), voz, 'letra');
      if ((enN0 ? VOZ_N0 : VOZ).has(clave)) anotar(idioma, enN0 ? plano(x) : x, voz);
    };
    recorrer(JSON.parse(readFileSync(f, 'utf8')));
  }
}
console.log(JSON.stringify([...casos.values()], null, 1));
