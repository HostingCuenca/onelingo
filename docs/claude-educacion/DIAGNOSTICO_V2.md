# Diagnóstico de ubicación v2 — Inglés N1–N10

Actualizado: 2026-09-30. Decisión: DEC-025. Sustituye al banco antiguo de 87 preguntas (escala 0–10) solo en inglés; los otros 9 idiomas siguen con el diagnóstico actual.

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
