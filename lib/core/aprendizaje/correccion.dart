import 'modelos.dart';

final _puntuacion = RegExp(r'[.,!?¡¿;:。、！？「」…"“”«»()—–，：；]');
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
String sinTildes(String s) =>
    s.split('').map((c) => _tildes[c] ?? c).join();

String _forma(String s, String idioma) =>
    idioma == 'zh' || idioma == 'ja' ? _compacta(s) : normalizar(s);

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

/// Corrige un ítem. [respuesta] es un índice (elegir/escuchar), una frase
/// (ordenar/completar/escribir) o `true` cuando se completó relacionar.
bool corregir(Item item, Object? respuesta, String idioma) =>
    switch (item.formato) {
      FormatoItem.elegir ||
      FormatoItem.escuchar => respuesta == item.indiceRespuesta,
      FormatoItem.relacionar => respuesta == true,
      _ => respuesta is String && respuestaEscritaCorrecta(item, respuesta, idioma),
    };
