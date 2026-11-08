/**
 * Videollamada con explicaciones en el idioma del alumno: el tutor escribe esas
 * partes entre corchetes («[Como fue ayer, se dice «行きました».] 言ってみて？»).
 * Aquí se separan por idioma para la voz (cada parte con su pronunciación) y se
 * quitan los corchetes de lo que ve el alumno.
 */
export type Explica = 'nativo' | 'meta';
export type Parte = { texto: string; nativo: boolean };

/** Escrituras propias de los idiomas meta que no usan el alfabeto latino. */
const ESCRITURA: Record<string, RegExp> = {
  ja: /[぀-ヿ一-鿿]/gu, zh: /[一-鿿]/gu, ko: /[가-힯ᄀ-ᇿ]/gu, ru: /[Ѐ-ӿ]/gu,
};

/** Sin corchetes ni espacios dobles: lo que se ve y lo que se guarda. */
export const sinCorchetes = (t: string) => t.replace(/[[\]]/g, '').replace(/\s{2,}/g, ' ').replace(/\s+([.,!?…。！？])/g, '$1').trim();

/**
 * Red de seguridad si el tutor olvida los corchetes: en un idioma meta de otra
 * escritura, una parte sin esa escritura y con palabras latinas es del alumno.
 */
function pareceNativo(texto: string, meta: string) {
  const re = ESCRITURA[meta];
  if (!re) return false;
  const propias = texto.match(re)?.length ?? 0, letras = texto.match(/\p{Script=Latin}/gu)?.length ?? 0;
  const palabras = texto.match(/\p{Script=Latin}+/gu)?.length ?? 0;
  return palabras >= 2 && propias * 2 < letras;
}

/** Al revés: el tutor puso entre corchetes una frase en la escritura del idioma meta. */
function pareceMeta(texto: string, meta: string) {
  const re = ESCRITURA[meta];
  if (!re) return false;
  const propias = texto.match(re)?.length ?? 0, letras = texto.match(/\p{Script=Latin}/gu)?.length ?? 0;
  return propias > 0 && letras * 3 < propias;
}

/**
 * Separador con estado: recibe las frases en orden (una explicación puede
 * abrir el corchete en una frase y cerrarlo en la siguiente) y devuelve sus
 * partes con el idioma de cada una.
 */
export function separadorDeLenguas(meta: string) {
  let dentro = false;
  return (frase: string): Parte[] => {
    const partes: Parte[] = [];
    let actual = '';
    const cerrar = () => {
      const texto = sinCorchetes(actual);
      if (/[\p{L}\p{N}]/u.test(texto)) partes.push({ texto, nativo: dentro ? !pareceMeta(texto, meta) : pareceNativo(texto, meta) });
      actual = '';
    };
    for (const c of frase) {
      if (c === '[' && !dentro) { cerrar(); dentro = true; }
      else if (c === ']' && dentro) { cerrar(); dentro = false; }
      else actual += c;
    }
    cerrar();
    return partes;
  };
}
