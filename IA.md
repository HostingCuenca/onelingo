# OneLingo · Arquitectura de IA (3 servicios)

Reparto acordado con el cliente (septiembre 2026). Las claves viven **solo** en
`backend/.env` y `tools/contenido/.env` (ignorados por git); la app nunca
llama a los proveedores directamente, siempre pasa por el backend.

| Servicio | Para qué | Dónde | Modelo por defecto |
|---|---|---|---|
| **OpenAI** | Tutor conversacional: conversa, comprende, detecta y explica errores, adapta al nivel. También transcribe la voz del alumno. | `backend/src/lib/ia_openai.ts` · `POST /chat` · `POST /transcribir` | `gpt-4.1-mini` (chat) · `gpt-4o-mini-transcribe` (voz→texto) |
| **Google Gemini** | Generación y personalización de ejercicios (vocabulario, frases, diálogos, errores típicos, examen) a partir del plan curricular. | `tools/contenido` (`npm run generar -- --proveedor gemini`) | `gemini-flash-latest` |
| **ElevenLabs** | Voz natural: tutores y narradores de lecciones/Listening. Cada frase se sintetiza **una sola vez** y se guarda. | `backend/src/lib/voz.ts` · `GET /voz` · `POST /voz/lote` | `eleven_multilingual_v2` |

Variables de entorno (backend): `IA_PROVEEDOR=openai|gemini|claude`, `OPENAI_API_KEY`,
`OPENAI_MODELO`, `OPENAI_MODELO_TRANSCRIPCION`, `GEMINI_API_KEY`, `GEMINI_MODELO`,
`ELEVENLABS_API_KEY`, `ELEVENLABS_MODELO`, `AUDIO_DIR` (carpeta de MP3, por defecto
`./audio`), `VOZ_MAX_CARACTERES` (600). Para rotar una clave basta cambiar el `.env`
y reiniciar el backend; la app no cambia.

## 1. Tutor (OpenAI)

- Mismo contrato que antes para la app: `{reply, romanizacion, traduccion, corrections[], suggestions[]}`.
- Chat Completions con **Structured Outputs** (`response_format: json_schema`, `strict: true`),
  así la respuesta siempre es JSON válido con las 5 claves.
- El *system prompt* (`ia.ts → systemPrompt`) lleva personalidad del tutor (Mia, Leo,
  Sofía, Max), perfil del nivel 1-10, situación y objetivo pedagógico.
- Reintentos con espera ante 429/5xx. Si OpenAI falla, `/chat` devuelve 502 y la app
  usa el simulador local (nunca se queda sin respuesta).
- Cada turno se guarda en la tabla `conversaciones` (modelo, tokens) → panel "Conversaciones IA".
- **Voz del alumno → texto**: `POST /transcribir` (multipart `audio` + `idioma`).
  Hoy la app usa el reconocimiento del sistema (speech_to_text); este endpoint queda
  listo para cuando se grabe audio en el dispositivo (mejor precisión en chino/japonés/coreano).

Cambiar de proveedor: `IA_PROVEEDOR=gemini` o `claude` (con `ANTHROPIC_API_KEY`).

## 2. Ejercicios (Gemini)

Pipeline en `tools/contenido` (ver `PIPELINE.md`): plan curricular de 10 niveles × 20
temas → una unidad JSON por tema (vocab 8-10, frases 6-8, diálogo 4-8, errores 2-4,
examen 3-4) → validación → empaquetado en `assets/contenido/<idioma>/nivel-N.json`.

```bash
cd tools/contenido
npm run generar -- --idioma en --nivel 1 --proveedor gemini        # un nivel
npm run generar -- --todo --proveedor gemini --concurrencia 2       # los 10 idiomas
npm run validar && npm run empaquetar
```

La cuota gratuita de Gemini es de ~20 peticiones/día; con facturación activada en el
proyecto de Google AI Studio se pueden generar las 2 000 unidades (10 idiomas × 200)
en pocas horas. Cada unidad cuesta ~2 000 tokens de entrada y ~1 700 de salida.

Personalización futura (mismo servicio): variaciones de ejercicios a partir de los
errores del alumno (`errores` en la BD) y planes de refuerzo por habilidad.

## 3. Voz (ElevenLabs)

- `GET /voz?texto=&idioma=&voz=` devuelve `audio/mpeg`. Cabeceras `X-Voz-Cache: hit|miss`
  y `X-Voz-Hash`. Acepta `?token=` para reproductores que no envían cabeceras.
- Caché: `sha256(modelo|voz_id|texto)` → `AUDIO_DIR/<hash>.mp3` + fila en `audios`
  (idioma, voz, texto, caracteres, bytes, usos). Una frase repetida por 1 000 alumnos
  consume la API **una** vez.
- La app (`lib/core/voz.dart → VozNube`) guarda además cada MP3 en la carpeta temporal
  del dispositivo y, al abrir una lección, **precarga** todas sus frases en segundo plano.
- Si no hay sesión, el servidor falla o el texto supera `VOZ_MAX_CARACTERES`, la app cae
  a la voz del sistema (flutter_tts) sin interrumpir la lección.
- Velocidad lenta (botón "despacio" de Listening): reproducción a 0.8× en el dispositivo,
  sin generar un segundo audio.

Voces por rol (`voz.ts → VOCES`):

| Rol | Voz ElevenLabs | Uso |
|---|---|---|
| `mia` | Sarah (cálida) | tutora amigable |
| `leo` | Liam (enérgico) | tutor motivador |
| `sofia` | Matilda (profesional) | tutora profesional |
| `max` | Adam (firme) | tutor directo |
| `narradora` | Alice (educadora) | lecciones, flashcards, Listening |
| `narrador` | George (narrador) | segunda voz en diálogos |

`eleven_multilingual_v2` detecta el idioma por el texto (probado con italiano, coreano y
japonés). Para los diálogos, las réplicas pares suenan con `narrador` y las impares con
`narradora`, así el alumno distingue a los dos hablantes.

Panel → **Voz y audios**: audios guardados, reproducciones, caracteres, cuota mensual
del plan de ElevenLabs, prueba de cualquier voz e idioma, y reproducción de los últimos
audios. Plan actual: Starter, 40 000 caracteres/mes (≈ 800 frases nuevas; las repetidas
no cuentan).

## Costes orientativos

| Acción | Servicio | Coste aprox. |
|---|---|---|
| Un turno de chat (nivel 1-5) | OpenAI gpt-4.1-mini | ≈ 0,0005 USD |
| Una unidad de contenido | Gemini Flash | ≈ 0,001 USD |
| Una frase nueva de 50 caracteres | ElevenLabs | 50 caracteres de cuota; después gratis |

## Pendiente

- (Hecho) La app graba audio con el paquete `record` (AAC 16 kHz mono) y lo envía a
  `/transcribir`; en web o sin sesión usa el reconocimiento del sistema (`Oido.nube`).
  El modo activo se muestra en la interfaz ('Grabando…' frente a 'Escuchando…').
- Pregenerar en lote los audios de todo un nivel (`POST /voz/lote`) al empaquetar contenido.
- Límite de turnos de IA por plan y por hora de prueba (contador ya en `conversaciones`).


## Diagnóstico adaptativo (nivel real por competencias)

`lib/core/diagnostico.dart` + `lib/features/onboarding/diagnostico_screen.dart`. Parte del nivel declarado,
una pregunta por turno, mide la competencia menos observada a la dificultad estimada, sube/baja como máximo
un nivel por respuesta, no hunde el nivel global si los fallos se concentran en una competencia, incluye una
producción escrita (evaluada por OpenAI vía `POST /diagnostico/escritura`, con respaldo local) y termina entre
10 y 25 preguntas cuando la estimación se estabiliza. Devuelve nivel (medios puntos), MCER, puntuación por
competencia, fortalezas, debilidades, errores recurrentes, temas a reforzar, nivel recomendado (0 = Fundamentos)
y plan inicial (unidades concretas). El resultado se guarda en el estado del alumno (`diagnostico`), se muestra
en Inicio ("Tu plan de refuerzo") y en el panel (detalle del alumno).


### Preguntas generadas por la IA (Gemini, con OpenAI de respaldo)

Desde el 8 sep 2026 el diagnóstico pide cada pregunta a `POST /diagnostico/pregunta`
(`backend/src/lib/diag_ia.ts`): el motor de la app decide nivel (0-10), competencia y tipo
(rotando formatos: elegir, natural, significado, contexto, situación, error, completar, corta,
escucha, dictado, escritura) y la IA la redacta con salida JSON estructurada, en el idioma meta y con
ejercicios propios de ese idioma (partículas, casos, tonos, formas corteses). Gemini responde primero
(`GEMINI_TIMEOUT_MS`, 12 s); si tarda o falla, OpenAI. Mientras el alumno lee el feedback ya se pide la
siguiente (prefetch). Sin conexión se usa el banco sembrado (`semilla/<idioma>-diagnostico.txt`).
Al terminar, `POST /diagnostico/perfil` redacta el resumen del profesor, recomendaciones y un plan
de dos semanas que se guarda con el diagnóstico. Coste aproximado por diagnóstico completo: 15-25
preguntas × Gemini Flash + 1 evaluación de escritura (gpt-4.1) + 1 perfil ≈ 0,02-0,05 USD.
