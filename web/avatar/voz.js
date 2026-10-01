// Envolvente de la voz para mover la boca sin pasar el audio por WebAudio.
// Antes la voz sonaba a través de un AudioContext (para leer un analizador);
// en iPhone, al abrir el micrófono ese contexto cambia de frecuencia de
// muestreo y la voz se entrecortaba. Ahora la voz suena por un <audio> normal
// y la boca sigue esta envolvente, calculada al descargar cada frase.
export const FPS = 50;
// Reparto típico de la energía por bandas con estos filtros (medido con las
// voces de los tutores). Cada banda se compara con su valor típico.
export const BANDAS_TIPICAS = { graves: 0.78, medios: 0.143, agudos: 0.029, sibilantes: 0.011 };

let decodificador = null;
function contexto() {
  const Offline = window.OfflineAudioContext || window.webkitOfflineAudioContext;
  if (!decodificador && Offline) decodificador = new Offline(1, 1, 44100);
  return decodificador;
}

/** Envolvente por cuadros de 20 ms: amplitud (0–1) y energía por bandas. */
export async function envolvente(bytes) {
  const ac = contexto();
  if (!ac) return null;
  const buffer = await ac.decodeAudioData(bytes.slice(0));
  const x = buffer.getChannelData(0), sr = buffer.sampleRate, salto = Math.round(sr / FPS);
  const k = fc => Math.exp(-2 * Math.PI * fc / sr);
  const a6 = k(600), a20 = k(2000), a50 = k(5000);
  let l6 = 0, l20 = 0, l50 = 0;
  const cuadros = [];
  for (let i = 0; i < x.length; i += salto) {
    let total = 0, graves = 0, medios = 0, agudos = 0, sibilantes = 0;
    const fin = Math.min(x.length, i + salto);
    for (let j = i; j < fin; j++) {
      const v = x[j];
      l6 = (1 - a6) * v + a6 * l6; l20 = (1 - a20) * v + a20 * l20; l50 = (1 - a50) * v + a50 * l50;
      total += v * v; graves += l6 * l6;
      const m = l20 - l6, h = l50 - l20, s = v - l50;
      medios += m * m; agudos += h * h; sibilantes += s * s;
    }
    const n = fin - i || 1;
    cuadros.push({ amplitud: Math.min(1, Math.sqrt(total / n) * 5), graves, medios, agudos, sibilantes });
  }
  return { cuadros, duracion: buffer.duration };
}

/** Muestra de la envolvente en el instante actual del <audio>. */
export function muestraEn(env, segundos) {
  if (!env) return null;
  return env.cuadros[Math.min(env.cuadros.length - 1, Math.max(0, Math.floor(segundos * FPS)))];
}

/** Bandas relativas a su peso típico, normalizadas (suman 1). */
export function repartir(m) {
  const n = {
    graves: m.graves / BANDAS_TIPICAS.graves, medios: m.medios / BANDAS_TIPICAS.medios,
    agudos: m.agudos / BANDAS_TIPICAS.agudos, sibilantes: m.sibilantes / BANDAS_TIPICAS.sibilantes,
  };
  const total = n.graves + n.medios + n.agudos + n.sibilantes || 1;
  return { graves: n.graves / total, medios: n.medios / total, agudos: n.agudos / total, sibilantes: n.sibilantes / total };
}
