# Comparación conservadora de transcripción

Aplicar similarity.patch a lib/core/voz.dart y copiar transcription_similarity_test.dart a test/. El patch reemplaza únicamente similitud y su comentario; no toca captura, red, TTS ni estados.

- Normaliza puntuación y contracciones inglesas no ambiguas; mantiene 's y 'd sin expandir.
- Usa distancia de edición de secuencias, respetando repeticiones y orden. Texto sin espacios se compara por puntos de código.
- Cambios de negadores textuales y permutaciones de las mismas palabras quedan por debajo del umbral actual .6 (tope .49).
- No es un evaluador semántico ni acústico. Un sustantivo, número o verbo sustituido dentro de una frase larga aún puede obtener un resultado alto. La función es coincidencia de transcripción, no dominio ni pronunciación.
- La lista de contracciones y negadores cubre inglés y el token no; no constituye evaluación lingüística multilingüe. Ausencia de apóstrofos en un STT puede seguir causando falsos negativos. No expandir 's o 'd automáticamente porque sería ambiguo.

Verificación realizada: smoke.dart ejecutado con el SDK Dart del equipo, PASS 17 comparaciones. El archivo de nueve tests Flutter está preparado pero no ejecutado contra el proyecto, porque todavía requiere aplicar el patch. No se llamó a APIs ni se editó el proyecto directamente.
