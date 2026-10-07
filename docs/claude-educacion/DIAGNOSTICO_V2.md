# Diagnóstico de ubicación v2 — Inglés N1–N10

Actualizado: 2026-09-30. Decisión: DEC-025. Sustituye al banco antiguo de 87 preguntas (escala 0–10) en inglés y, desde FR-6, en cada idioma con ruta que tenga su banco (sección «Otros idiomas»); el resto sigue con el diagnóstico anterior.

## Principios (acordados con el cliente)

- **Corto e inteligente, no un examen**: ~8 minutos, 16–22 preguntas. Se sube la dificultad mientras el alumno acierta y cada habilidad se detiene cuando empieza a fallar. Un alumno A1 casi nunca ve preguntas de B2.
- **Por habilidad**: escucha, lectura, gramática y vocabulario se ubican por separado; la escritura (1–3 frases, rúbrica determinista) cierra y se puede omitir.
- **Desde cero sin examen**: la primera pantalla pregunta cuánto inglés sabe; «Nada, empiezo de cero» empieza en el principio sin preguntas. Si falla las primeras preguntas básicas, el resultado lo dice con naturalidad.
- **Sin micrófono ni IA en tiempo de ejecución**: determinista, como el curso.

## Flujo

1. Autodeclaración: nada (sin examen, nivel 0) · poco (empieza en N1) · me defiendo (N3) · bastante (N5) · avanzado (N7).
2. Estimación bayesiana por habilidad, en rotación (escucha → lectura → gramática → vocabulario). La escalera simple se descartó: en simulación solo ubicaba el 78 % a ±1 nivel por el acierto al azar (1/3).
   - Probabilidad de acertar un ítem de nivel L con nivel real T: 0,92 si L ≤ T; 0,45 si L = T+1; azar (1/nº de opciones) si más arriba.
   - Prior centrado en la autodeclaración (σ = 3); las respuestas de las otras habilidades cuentan con peso 0,4.
   - Cada pregunta se pide en el nivel mediano de la habilidad; se cierra con ±1 nivel al 85 % (mín. 3 preguntas) o tras 6; tope 22 preguntas.
   - Si la estimación conjunta da P(nivel 0) ≥ 85 % tras 3 preguntas, termina: «empiezas desde cero».
3. Escritura en el nivel estimado (omitible).
4. Resultado: nivel por habilidad (moda, 0–10), nivel de inicio = media de las cuatro objetivas redondeada hacia abajo, sin superar la más débil en más de 2. Niveles anteriores desbloqueados y omitibles. Nivel 0 = empezar desde cero.

## Banco

Fuente: `assets/contenido/en/plan-editorial/diagnostico/n<N>.json` (una por nivel). Compilado: `assets/contenido/en/diagnostico-v2.json`. Validador: `python3 tools/contenido/validar_diagnostico.py`.

Por nivel: 4 ítems de cada habilidad (`escucha`, `lectura`, `gramatica`, `vocabulario`) + 2 de `escritura` = 18 ítems; 180 en total. Cada ítem de nivel N debe poder resolverlo quien terminó N y **no** quien solo terminó N−1: se toma del núcleo del mapa v2 del nivel (principio, mitad y final del nivel).

Formato de ítem (el mismo JSON de ítem que la ruta, más `nivel` y `habilidad`):

```json
{"id": "dx.en.n4.lectura.2", "nivel": 4, "habilidad": "lectura", "formato": "elegir",
 "consigna": {"es": "Lee el aviso y elige qué debe hacer Tom."},
 "texto": "…pasaje en inglés…", "opciones": ["…", "…", "…"], "respuesta": 1,
 "feedback": {"es": "…"}}
```

| habilidad | formato | reglas |
|---|---|---|
| escucha | `escuchar` | `audio` (inglés, lo lee la voz) con opciones parafraseadas; no se resuelve sin oír |
| lectura | `elegir` | `texto` = pasaje del nivel; pregunta de detalle (N1–N4) o de inferencia/propósito/actitud (N5–N10) |
| gramatica | `elegir` o `completar` (con `opciones`) | una frase o dos de contexto; prueba la estructura del nivel |
| vocabulario | `elegir` o `completar` (con `opciones`) | palabra o colocación del nivel en contexto |
| escritura | `escribir` | `respuesta` modelo, `aceptadas` ≥1, `evidenciasEscritura` ≥3 grupos de frases, `minimoPalabras`/`maximoPalabras` |

Longitud en palabras de `texto` (lectura) y `audio` (escucha) por nivel:

| N | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| lectura | 15–35 | 25–45 | 35–60 | 45–70 | 55–85 | 65–95 | 75–110 | 85–120 | 95–130 | 105–150 |
| escucha | 5–15 | 8–20 | 12–25 | 15–30 | 20–40 | 25–45 | 30–55 | 35–60 | 40–70 | 45–80 |

Reglas comunes: 3–4 opciones distintas y plausibles, una sola defendible; la correcta no es la única más larga en más del 35 % de los ítems del nivel; consigna en español ≤ 90 caracteres y única; toda palabra inglesa (salvo `aceptadas` y evidencias) enseñada hasta el final del nivel N; español neutro (tú); temas variados, personajes del curso.

## Implementación

- Motor: `lib/core/aprendizaje/ubicacion.dart` · pantalla: `lib/features/onboarding/ubicacion_screen.dart` (`/prueba-nivel` en inglés; los demás idiomas siguen con `diagnostico_screen.dart`).
- Compilación: `python3 tools/contenido/validar_diagnostico.py --compilar` (exige GO en los 10 niveles; exporta la respuesta de `completar` como texto, que es como corrige la vista de ítems).
- Pruebas: `test/ubicacion_test.dart` (simulación) y `test/ubicacion_banco_test.dart` (banco real: cobertura, corrección de cada ítem, simulación y pantalla).
- Verificado en navegador (build local): un alumno N5 simulado sale «N5 · B2» en 19 preguntas; uno que responde al azar sale «Empiezas desde cero».

## Otros idiomas (FR-6)

La misma prueba sirve para cualquier idioma de `idiomasConRuta` (`lib/core/aprendizaje/providers.dart`) que tenga banco. El francés es el primero.

- **Banco:** fuentes `assets/contenido/<idioma>/plan-editorial/diagnostico/nN.json`; compilado `assets/contenido/<idioma>/diagnostico-v2.json` (`{"schema": "onelingo.diagnostico.v2", "idioma": "<idioma>", "items": […]}`).
- **Validar y compilar:** `python3 tools/contenido/validar_diagnostico.py --idioma fr [--compilar]`. Sin `--idioma` sigue siendo el inglés, con la misma salida.
  - Se compilan solo los niveles presentes con revisión `GO`, consecutivos desde N1 (hoy N1; luego N2…). Un nivel sin GO se informa y no se compila. No se exigen los 10.
  - Mismo formato, ids (`dx.<idioma>.nN.<habilidad>.<k>`), reparto (4 × 4 + 2 de escritura) y longitudes que en inglés.
  - Textos de apoyo (`consigna`, `feedback`, `pista`, `preguntaApoyo`) **bilingües** `{"es", "en"}`, sin vacíos; `consigna.es` ≤ 90 caracteres y `consigna.en` ≤ 110. El feedback no cita posiciones («primera opción», «first option»).
  - Léxico: cada palabra del estímulo, de la opción correcta y de la respuesta modelo debe estar enseñada en la ruta publicada hasta el final de N (vocabulario y tablas de las unidades de f0 a N, más `palabrasLibres`, con el mismo criterio que `tools/validar_ruta.py`); los distractores pueden usar además las formas de `erroresFrecuentes`. Cifras y símbolos (`2,50 €`) no cuentan.
  - Sin la regla de ortografía británica/estadounidense del inglés. La tipografía francesa (espacio fino U+202F antes de `? ! : ;`, comillas « ») se admite: cuenta como espacio y puntuación.
  - Rúbrica de escritura comprobada como la corrige la app para ese idioma (sin contracciones inglesas ni flexiones -s/-ed/-ing; tildes opcionales).
- **Español (ES-8, 2026-10-05):** banco N1–N10 (180 ítems, 10 GO). Como la ruta del español, el apoyo es **solo inglés** `{"en"}` (`APOYO_SOLO_EN` en el validador: `consigna.en` ≤ 110 caracteres, sin clave `es`); `localizarApoyo` cae al inglés también con la interfaz en español.
- **Portugués de Brasil (06-10):** banco N1–N10 (180 ítems, 10 GO), apoyo bilingüe `{es, en}` como el francés. El léxico se comprueba con la morfología pt de la ruta (`conocida_pt`: flexiones, conjugaciones y ênclise de lo enseñado).
- **Alemán (06-10):** banco N1–N10 (180 ítems, 10 GO), apoyo `{es, en}`; léxico comprobado con `conocida_de` (flexiones de lo enseñado) contra la ruta integrada.
- **Italiano, versión esencial (07-10):** banco N1–N4 (72 ítems, 4 GO), apoyo `{es, en}`, léxico con `conocida_it`. Solo hay clases hasta N4: la prueba nunca ubica por encima de N4 (`test/ubicacion_it_test.dart`). Al publicar N5–N10 se añaden sus `nN.json` y se recompila.
- **Chino mandarín, versión esencial (07-10):** banco N1–N2 (36 ítems, 2 GO), apoyo `{es, en}`, léxico con `conocida_cjk` (cada palabra separada por espacios, enseñada tal cual). Cada texto y opción en chino lleva pinyin (`textoRom`, `opcionesRom`; ROMANIZACION.md); el validador comprueba además, con las reglas de `tools/contenido/ruta-zh/validar.py`, el sandhi escrito, los espacios entre palabras y la puntuación de ancho completo. Escritura: en zh y ja la extensión (`minimoPalabras`/`maximoPalabras`) se mide en caracteres y las evidencias se buscan sin espacios, igual en la app (`correccion.dart`) y en el validador. Nunca ubica por encima de N2 (`test/ubicacion_zh_test.dart`).
- **Japonés, versión esencial (07-10):** banco N1–N2 (36 ítems, 2 GO), apoyo `{es, en}`, léxico con `conocida_cjk` (cada palabra, escrita en kana y separada por espacios, enseñada tal cual; sin kanji ni cifras). Cada texto y opción en japonés lleva rōmaji (`textoRom`, `opcionesRom`); el validador comprueba el Hepburn modificado de `tools/ia/idiomas/ja.md` con `tools/contenido/hepburn_ja.py` (macrones, n', wa/e/o, mayúscula solo al inicio de frase y en nombres propios, «-san» con guion) y las reglas de `tools/contenido/ruta-ja/validar.py` (puntuación de ancho completo, partículas aparte). Escritura medida en caracteres, igual que el chino. Nunca ubica por encima de N2 (`test/ubicacion_ja_test.dart`).
- **Ruso, versión esencial (07-10):** banco N1–N2 (36 ítems, 2 GO), apoyo `{es, en}`, léxico con `conocida_ru` (cada forma enseñada tal cual, con ё ≡ e y sin acento gráfico; las flexiones van entre paréntesis en el vocablo de la clase). Cirílico sin marca de acento; cada texto y opción en ruso lleva `textoRom`/`opcionesRom` letra a letra con la tilde aguda solo en el rom (palabras copiadas de las clases; una tilde por palabra de 2+ sílabas, ninguna en los monosílabos). El validador comprueba el rom con `tools/contenido/ruta-ru/validar.py` (`errores_ruso`) y normaliza ё → е como `sinTildes` de la app. Escritura medida en palabras, evidencias de 2+ palabras. Nunca ubica por encima de N2 (`test/ubicacion_ru_test.dart`).
- **App:** `/prueba-nivel` abre `UbicacionScreen(idioma)` si el idioma tiene ruta y banco (`bancoUbicacionProvider`); si no, el diagnóstico anterior.
  - Textos de apoyo con `localizarApoyo` en el idioma de la interfaz; voz y corrección en el idioma evaluado.
  - **Tope:** la prueba solo pregunta y ubica hasta el nivel más alto con ítems en el banco **y** unidades publicadas (`ruta.delNivel('nX').isNotEmpty`). Con solo N1, el resultado es 0 (Nivel 0 / Fundamentos) o 1, y la primera pantalla solo ofrece «Nada» y «Un poco».
  - El alumno ya ubicado por encima de lo publicado (p. ej. N4 con el diagnóstico antiguo) conserva su diagnóstico, pero su nivel efectivo (`nivelUbicacionRuta`, `nivelAlumnoProvider`) se limita al último nivel publicado; al publicarse más niveles, se aplica.
- **Pruebas:** `test/ubicacion_idiomas_test.dart` (azar en francés → «desde cero», nunca por encima de N1; tope; pantalla; nivel efectivo de alumnos antiguos). Con el banco francés compilado se activa también la simulación sobre el banco real.
