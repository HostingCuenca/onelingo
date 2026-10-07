import 'modelos.dart';

final _puntuacion = RegExp(r'[.,!?¡¿;:/。、！？「」…"“”«»()—–，：；]');
final _espacios = RegExp(r'\s+');

/// Normaliza una respuesta escrita (ver ESQUEMA_CONTENIDO.md).
String normalizar(String s) => s
    .toLowerCase()
    .replaceAll('’', "'")
    .replaceAll('‘', "'")
    .replaceAll(_puntuacion, ' ')
    .replaceAll(_espacios, ' ')
    .trim();

/// Igual que [normalizar] pero sin espacios: en zh/ja se aceptan con y sin
/// separación entre palabras.
String _compacta(String s) => normalizar(s).replaceAll(' ', '');

const _tildes = {
  'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a', 'ã': 'a', 'å': 'a',
  'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
  'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
  'ó': 'o', 'ò': 'o', 'ô': 'o', 'ö': 'o', 'õ': 'o',
  'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
  'ç': 'c', 'ñ': 'n', 'œ': 'oe', 'æ': 'ae',
  // Ruso: «ё» se escribe a menudo como «е».
  'ё': 'е',
  // Marcas de tono del pinyin.
  'ā': 'a', 'ǎ': 'a', 'ē': 'e', 'ě': 'e', 'ī': 'i', 'ǐ': 'i',
  'ō': 'o', 'ǒ': 'o', 'ū': 'u', 'ǔ': 'u', 'ǖ': 'u', 'ǘ': 'u', 'ǚ': 'u',
  'ǜ': 'u',
};

/// Quita las tildes del alfabeto latino (no afecta a otras escrituras).
String sinTildes(String s) => s.split('').map((c) => _tildes[c] ?? c).join();

String _forma(String s, String idioma) => switch (idioma) {
  'zh' || 'ja' => _compacta(s),
  'en' => expandirContracciones(normalizar(s)),
  _ => normalizar(s),
};

const _contraccionesFijas = {
  "can't": 'can not',
  'cannot': 'can not',
  "won't": 'will not',
  "shan't": 'shall not',
  "i'm": 'i am',
  "let's": 'let us',
};
const _conS = {
  'he',
  'she',
  'it',
  'that',
  'what',
  'there',
  'where',
  'who',
  'here',
  'how',
};
final _conSufijo = RegExp(r"^([a-z]+)'(re|ve|ll|d|s)$");

/// Inglés: «I'm», «don't», «she's»… equivalen a su forma completa, para que
/// una respuesta con contracción no cuente como error. El genitivo sajón
/// («Tom's», «my brother's») no se toca.
String expandirContracciones(String normalizada) => normalizada
    .split(' ')
    .map((palabra) {
      final fija = _contraccionesFijas[palabra];
      if (fija != null) return fija;
      if (palabra.endsWith("n't") && palabra.length > 3) {
        return '${palabra.substring(0, palabra.length - 3)} not';
      }
      final m = _conSufijo.firstMatch(palabra);
      if (m == null) return palabra;
      final base = m.group(1)!;
      return switch (m.group(2)) {
        're' => '$base are',
        've' => '$base have',
        'll' => '$base will',
        'd' => '$base would',
        _ => _conS.contains(base) ? '$base is' : palabra,
      };
    })
    .join(' ');

/// Compara una respuesta escrita con una forma válida con las mismas reglas
/// que [respuestaEscritaCorrecta] (puntuación, tildes y contracciones).
bool mismaRespuesta(String dada, String valida, String idioma) {
  final a = sinTildes(_forma(dada, idioma));
  return a.isNotEmpty && a == sinTildes(_forma(valida, idioma));
}

bool _coincide(Item item, String respuesta, String idioma, bool tildes) {
  String f(String s) =>
      tildes ? _forma(s, idioma) : sinTildes(_forma(s, idioma));
  final dada = f(respuesta);
  if (dada.isEmpty) return false;
  return item.respuestasValidas.any((r) => f(r) == dada);
}

/// Correcta si coincide con alguna forma válida. Un error solo de tildes se
/// acepta (teclados sin esas letras) y se avisa con [soloFallanTildes].
bool respuestaEscritaCorrecta(Item item, String respuesta, String idioma) =>
    _coincide(item, respuesta, idioma, false);

bool soloFallanTildes(Item item, String respuesta, String idioma) =>
    !_coincide(item, respuesta, idioma, true) &&
    _coincide(item, respuesta, idioma, false);

int contarPalabras(String texto) =>
    normalizar(texto).split(' ').where((palabra) => palabra.isNotEmpty).length;

/// Producción abierta: basta con escribir dentro de la extensión pedida.
bool produccionAbiertaCompleta(Item item, String respuesta) =>
    contarPalabras(respuesta) >= (item.minimoPalabras ?? 1);

/// Idiomas que se escriben sin espacios entre palabras (el curso los pone,
/// pero el alumno puede no hacerlo).
bool _sinEspacios(String idioma) => idioma == 'zh' || idioma == 'ja';

final _caracterCjk = RegExp(r'[\u3040-\u30ff\u3400-\u9fff]');

/// Extensión de una respuesta para la rúbrica: palabras; en zh y ja, cada
/// carácter cuenta como una (no se puede segmentar sin diccionario) y lo
/// demás (cifras, letras) por palabras.
int _extensionRubrica(String texto, String idioma) => _sinEspacios(idioma)
    ? _caracterCjk.allMatches(texto).length +
        contarPalabras(texto.replaceAll(_caracterCjk, ' '))
    : contarPalabras(texto);

bool _cumpleRubricaEscritura(Item item, String respuesta, String idioma) {
  if (item.abierta) return produccionAbiertaCompleta(item, respuesta);
  if (item.evidenciasEscritura.isEmpty ||
      item.minimoPalabras == null ||
      item.maximoPalabras == null) {
    return respuestaEscritaCorrecta(item, respuesta, idioma);
  }
  final palabras = _extensionRubrica(respuesta, idioma);
  if (palabras < item.minimoPalabras! || palabras > item.maximoPalabras!) {
    return false;
  }
  final dada = ' ${sinTildes(_forma(respuesta, idioma))} ';
  return item.evidenciasEscritura.every(
    (grupo) => grupo.any((frase) {
      final evidencia = sinTildes(_forma(frase, idioma));
      if (evidencia.isEmpty) return false;
      // zh/ja: [_forma] quita los espacios; la evidencia se busca dentro.
      if (_sinEspacios(idioma)) return dada.contains(evidencia);
      if (dada.contains(' $evidencia ')) return true;
      // La última palabra admite flexiones regulares (complaint → complaints,
      // decide → decided): el alumno no debe fallar por el número o el tiempo.
      return idioma == 'en' &&
          RegExp(' ${RegExp.escape(evidencia)}(?:s|es|d|ed|ing) ')
              .hasMatch(dada);
    }),
  );
}

/// Corrige un ítem. [respuesta] es un índice (elegir/escuchar), una frase
/// (ordenar/completar/escribir) o `true` cuando se completó relacionar.
bool corregir(
  Item item,
  Object? respuesta,
  String idioma,
) => switch (item.formato) {
  FormatoItem.elegir ||
  FormatoItem.escuchar => respuesta == item.indiceRespuesta,
  FormatoItem.relacionar => respuesta == true,
  FormatoItem.escribir =>
    respuesta is String && _cumpleRubricaEscritura(item, respuesta, idioma),
  _ => respuesta is String && respuestaEscritaCorrecta(item, respuesta, idioma),
};
