/**
 * Volumen igual para todas las voces. ElevenLabs entrega cada voz a su propio
 * nivel: en la medición del 2026-10-26 (una frase fija por idioma, 130 voces)
 * iban de −41 LUFS (it_anna) a −12 (ru_mariia), y el alumno tenía que subir y
 * bajar el volumen según quién hablara. Todo audio nuevo se lleva a OBJETIVO.
 *
 * Usa ffmpeg (`FFMPEG` o el del PATH). Sin ffmpeg, el audio sale tal cual.
 */
import { spawn } from 'node:child_process';

export const OBJETIVO_LUFS = -18;
const FFMPEG = process.env.FFMPEG ?? 'ffmpeg';
const limitar = (db: number) => Math.max(-12, Math.min(24, db));

/** Sonoridad medida de cada voz (LUFS); el streaming no puede medir el clip antes de enviarlo. */
const LUFS_VOZ: Record<string, number> = {
  de_anna: -25.2, de_ava: -21.9, de_ben: -16.7, de_ela: -15.9, de_ela_2: -20.4, de_elias: -16.4, de_julius: -22.9, de_mila: -23.1, de_otto: -20.9,
  de_petra: -25.6, de_susi: -20.1, de_timo: -28.2, de_tristan_medersburg: -15.8, en_alexandra: -17.0, en_brittney: -22.6, en_cassidy: -20.9, en_elise: -16.8,
  en_hope: -20.5, en_joe: -24.8, en_jon: -18.9, en_liam: -21.9, en_mark: -22.6, en_matilda: -20.2, en_nichalia_schwartz: -15.5, en_peter: -21.5,
  en_young_jamal: -20.6, es_antonio: -20.2, es_daniela: -19.7, es_enrique: -15.0, es_enrique_mondragon: -15.1, es_isabel: -20.8, es_lina: -17.3,
  es_lumina: -19.4, es_marcela: -16.7, es_marlene: -18.0, es_sebastian: -15.6, es_sofia: -14.6, es_tony: -20.3, es_yuri_baldemira: -21.6, fr_adina: -18.8,
  fr_amadou: -22.8, fr_anatole: -23.3, fr_caroline: -22.2, fr_francois_louis: -18.4, fr_jeanne: -19.4, fr_lucie: -18.1, fr_marcel: -21.5, fr_marine: -25.1,
  fr_maxime: -17.9, fr_mimi: -16.1, fr_nicolas: -19.7, fr_victoria: -18.3, it_andy: -14.5, it_anna: -41.2, it_carmelo: -19.9, it_chris_basetta: -21.3,
  it_corrado_noventa: -21.2, it_giulia_pro: -17.7, it_kina: -27.4, it_linda_fiore: -17.9, it_lorenzo: -17.9, it_marcotrox: -20.3, it_mia: -32.6,
  it_sami: -22.6, it_valentina: -34.1, ja_hinata: -25.2, ja_ishibashi: -20.3, ja_kenzo: -15.3, ja_kuon: -17.2, ja_kyoko: -24.5, ja_mitsuki: -21.6,
  ja_otani: -16.9, ja_sakura: -24.3, ja_shizuka: -21.6, ja_sora: -18.7, ja_yamato: -13.3, ja_yoko_honda: -20.8, ja_yui: -15.0, ko_anna_kim: -15.0,
  ko_chris: -20.9, ko_han: -17.4, ko_hyuk: -17.0, ko_jennie: -26.1, ko_jin_geon_song: -19.6, ko_jiyoung: -28.9, ko_jy: -18.9, ko_kelee_k: -22.6,
  ko_min_joon: -18.9, ko_salang: -24.2, ko_taehyung: -15.5, ko_yohan_koo: -20.2, pt_alcione: -15.2, pt_amanda_kelly: -21.4, pt_ana_dias: -17.8,
  pt_borges: -18.8, pt_fernanda: -18.6, pt_joao_pedro: -22.8, pt_lucas: -24.6, pt_paulo: -17.4, pt_raquel: -21.5, pt_roberta: -21.6, pt_tchize: -19.7,
  pt_victor_power: -18.0, pt_yasmin_alves: -29.1, ru_andrey_permikin: -26.0, ru_artem: -19.9, ru_denophine: -12.5, ru_ekaterina: -19.6, ru_kari: -16.5,
  ru_kate: -19.8, ru_larisa: -19.9, ru_lisa: -15.5, ru_mariia: -11.6, ru_natalia: -22.3, ru_prince_nur: -18.4, ru_stanislav: -19.4, ru_vasko: -18.8,
  zh_coco_li: -34.9, zh_evan: -13.7, zh_guan_tang_bao: -26.9, zh_jason_chen: -18.0, zh_julia: -11.9, zh_karo_yang: -26.1, zh_macy: -36.9, zh_maya: -13.7,
  zh_shanshan: -33.3, zh_stacy: -18.9, zh_xinghe: -16.1, zh_yating: -13.9, zh_zhile: -20.6,
};

/** Ganancia fija de una voz (dB) para el streaming; 0 si no se midió. */
export const gananciaVoz = (clave: string) => LUFS_VOZ[clave] === undefined ? 0 : limitar(OBJETIVO_LUFS - LUFS_VOZ[clave]);

/** Volumen y limitador (sin saturar) y de vuelta a MP3 de 128 kb/s. */
const filtro = (db: number) => ['-af', `volume=${db.toFixed(1)}dB,alimiter=limit=0.89:level=false`, '-c:a', 'libmp3lame', '-b:a', '128k', '-ar', '44100', '-f', 'mp3', 'pipe:1'];

let hayFfmpeg: Promise<boolean> | undefined;
export const ffmpegDisponible = () => hayFfmpeg ??= new Promise<boolean>((ok) => {
  const p = spawn(FFMPEG, ['-version'], { stdio: 'ignore' });
  p.on('error', () => ok(false)); p.on('exit', (c) => ok(c === 0));
}).then((hay) => {
  // Un fallo pasajero (EAGAIN con carga) no deja la voz sin normalizar hasta reiniciar.
  if (!hay) setTimeout(() => { hayFfmpeg = undefined; }, 60_000).unref();
  return hay;
});

function ffmpeg(args: string[], entrada: Buffer): Promise<{ salida: Buffer; log: string }> {
  return new Promise((ok, mal) => {
    const p = spawn(FFMPEG, ['-hide_banner', '-nostats', '-f', 'mp3', '-i', 'pipe:0', ...args]);
    const salida: Buffer[] = []; let log = '';
    p.stdout.on('data', (d: Buffer) => salida.push(d));
    p.stderr.on('data', (d: Buffer) => { log += d; });
    p.on('error', mal);
    // «close» y no «exit»: con «exit» aún pueden quedar datos de stdout por llegar (MP3 cortado al final).
    p.on('close', (c) => c === 0 ? ok({ salida: Buffer.concat(salida), log }) : mal(new Error(`ffmpeg ${c}: ${log.slice(-200)}`)));
    p.stdin.on('error', () => {});
    p.stdin.end(entrada);
  });
}

/** Sonoridad integrada (LUFS) de un MP3; null si es silencio o no se pudo medir. */
export async function medirLufs(mp3: Buffer): Promise<number | null> {
  const { log } = await ffmpeg(['-af', 'ebur128', '-f', 'null', '-'], mp3);
  const v = Number(log.match(/I:\s+(-?[\d.]+) LUFS(?![\s\S]*I:\s+-?[\d.]+ LUFS)/)?.[1]);
  return Number.isFinite(v) && v > -70 ? v : null;
}

/**
 * El clip a OBJETIVO_LUFS. Si no se puede medir (clip muy corto), usa la
 * ganancia de la voz. Ante cualquier fallo devuelve el audio original.
 * `rapido` (videollamada) no mide: usa la ganancia de la voz en una sola
 * pasada. Medir costaba ~75 ms por frase en el VPS, casi lo que tarda ElevenLabs.
 */
export async function normalizarVolumen(mp3: Buffer, voz?: string, rapido = false): Promise<Buffer> {
  if (!(await ffmpegDisponible())) return mp3;
  try {
    const lufs = rapido && LUFS_VOZ[voz ?? ''] !== undefined ? null : await medirLufs(mp3);
    const db = lufs === null ? gananciaVoz(voz ?? '') : limitar(OBJETIVO_LUFS - lufs);
    if (Math.abs(db) < 1) return mp3;
    const { salida } = await ffmpeg(filtro(db), mp3);
    return salida.length ? salida : mp3;
  } catch { return mp3; }
}

/**
 * Streaming con la ganancia de la voz: los trozos MP3 entran a ffmpeg y salen
 * a medida que se codifican. Sin ffmpeg o con ganancia ~0, pasan tal cual.
 */
export async function* conGananciaVoz(fuente: AsyncIterable<Buffer>, voz: string): AsyncGenerator<Buffer> {
  const db = gananciaVoz(voz);
  if (Math.abs(db) < 1 || !(await ffmpegDisponible())) { yield* fuente; return; }
  // Solo si de verdad llega MP3 (cabecera ID3 o sincronía de trama): con otra
  // cosa ffmpeg esperaría al final y el alumno no oiría nada hasta entonces.
  const it = fuente[Symbol.asyncIterator]();
  const primero = await it.next();
  if (primero.done) return;
  const resto = { [Symbol.asyncIterator]: () => it };
  const b = primero.value;
  if (!(b.subarray(0, 3).toString('latin1') === 'ID3' || (b[0] === 0xff && (b[1] & 0xe0) === 0xe0))) {
    yield b; yield* resto; return;
  }
  async function* trozos() { yield b; yield* resto; }
  const p = spawn(FFMPEG, ['-hide_banner', '-loglevel', 'error', '-fflags', 'nobuffer', '-probesize', '32', '-analyzeduration', '0',
    '-f', 'mp3', '-i', 'pipe:0', '-flush_packets', '1', ...filtro(db)]);
  let fallo: unknown;
  const crudo: Buffer[] = [];
  p.stdin.on('error', () => {});
  p.on('error', () => {});
  const entrada = (async () => {
    try {
      for await (const t of trozos()) {
        if (p.stdin.destroyed) break;
        crudo.push(t);
        if (!p.stdin.write(t)) await new Promise((r) => { p.stdin.once('drain', r); p.stdin.once('close', r); });
      }
    } catch (e) { fallo = e; }
    finally { p.stdin.end(); }
  })();
  let salio = false;
  try {
    for await (const d of p.stdout) { salio = true; yield d as Buffer; }
    await entrada;
  } finally {
    // Si el alumno cortó la reproducción, no se espera a la entrada: quien la
    // produce la cancela al cerrar; ffmpeg se detiene aquí.
    if (p.exitCode === null) p.kill();
  }
  if (fallo) throw fallo;
  // ffmpeg no pudo con lo que llegó: mejor el audio sin ajustar que nada.
  if (!salio) yield* crudo;
}
