# Auditoría C — Habilidades y evaluación

Agente C · 2026-09-26 · rama `claude/educacion-multilenguaje` · solo lectura del código (sin build ni run).
Cifras obtenidas con scripts `python3` sobre `assets/contenido/**` y leyendo el código que genera las lecciones. Todo lo que está marcado como "propuesta" no existe en el código.

## Resumen

1. **Hay tres motores de actividad que no están conectados entre sí.** El primero es el reproductor de lecciones, que tiene 10 `StepType` y se genera por código a partir de vocabulario y frases. El segundo es el diagnóstico, con 12 `TipoDiag`. El tercero es la biblioteca inglesa (lectura, listening, gramática, situaciones y fundamentos-v1), que existe solo para `en`. El examen de nivel es un cuarto flujo: 10 preguntas de opción múltiple.
2. **Predomina el reconocimiento.** En una unidad de los niveles 1–2 hay 31 pasos. De los 24 que puntúan, el 54 % son de selección, el 17 % de ordenar, el 17 % dictado copiado y el 12 % repetición oral. No hay **ninguna producción libre puntuada** en lecciones ni en exámenes. En Fundamentos (nivel 0) el 82 % de lo puntuado es selección. El examen de ascenso es 100 % selección.
3. **Lo que no se mide:**
   - Speaking: el diagnóstico lo declara no evaluado (`diagnostico_screen.dart:463`).
   - Pronunciación: solo se compara la transcripción con el texto modelo (`voz.dart:487`).
   - Escritura: solo tiene nota en el diagnóstico y en la biblioteca inglesa, con una puntuación global de IA sin anclajes.
   - Listening: se repite sin límite y con pistas, y el dictado es de frases ya vistas en la misma unidad.
4. **Ascender de nivel no exige dominio.** Una lección cuenta como completada con cualquier porcentaje (`providers.dart:567`). El examen se desbloquea tras 100 lecciones completadas (`providers.dart:131`). El examen son 10 preguntas de opción múltiple del mismo banco que las lecciones, con aprobado al 65 %, reintentos ilimitados y se guarda la mejor nota (`exam_screen.dart:22-57`, `providers.dart:585-607`). No hay retención diferida, no hay banco separado y no hay evidencia por habilidad.
5. **Riesgos graves de contenido que afectan a la evaluación:**
   - Los niveles 3–10 se construyen para **todos los idiomas** con un banco genérico **en inglés** de 6 palabras y 3 frases por nivel (`curriculum.dart:349,453`). Un alumno de francés en nivel 3 practica y se examina con contenido inglés.
   - El diagnóstico sin servidor para idiomas ≠ `en` usa ese mismo respaldo (`diagnostico.dart:216-224`).
6. **El diagnóstico inglés está anclado al nivel declarado.** Con el recorrido fijo de 10 ítems, los ítems objetivos solo pueden mover la estimación ±1,0 nivel (`diagnostico.dart:400-411,430-438,728-735`). Nunca recomienda Fundamentos, porque las estimaciones por habilidad se recortan a ≥1.
7. **El diagnóstico de los otros idiomas pide "listening" sin audio.** `tiposPorSkill` no tiene la clave `listening` y recurre a `eleccion` (`diagnostico.dart:364-373,482`).
8. **Propuesta.** Un perfil de 7 dimensiones enlazado al grafo de unidades. Separar el banco de práctica del de evaluación. Evaluación de unidad: ≥80 % en primera respuesta y sin ayuda, con ítems nuevos, más una producción aceptable según rúbrica y una retención a ≥1 día. Si falla, se vuelve a enseñar. Tres afirmaciones separadas: dominio del curso, CEFR estimado (orientativo) y preparación para un examen concreto.

## Inventario de tipos de actividad (cifras)

### Tipos implementados

| Motor | Tipo | Qué hace el alumno | ¿Puntúa? | Evidencia |
|---|---|---|---|---|
| Lección | `flashcard` | ve palabra y traducción (con audio) | no | `lesson_player_screen.dart:344-350` |
| Lección | `multipleChoice` | elige entre 3–4 opciones | sí (exacto) | `:313-330` |
| Lección | `fillBlank` | hueco **con opciones** (es selección) | sí | `curriculum.dart:549-562` |
| Lección | `imageChoice` | elige imagen (16 palabras fijas en inglés para todos los idiomas) | sí | `curriculum.dart:577-590` |
| Lección | `matchPairs` | une 4 pares; correcto solo si no hay fallos | sí | `lesson_player_screen.dart:739` |
| Lección | `orderWords` | ordena fichas (traducción inversa) | sí (normalizado exacto) | `:317-319` |
| Lección | `listenWrite` | dictado a 0,4× de velocidad, repeticiones ilimitadas, pista con la 1.ª palabra | sí (exacto) | `:320-322`, `curriculum.dart:563-570` |
| Lección | `speak` | repetir la frase; similitud de transcripción ≥0,6 | sí, pero **se puede saltar** | `:273-276`, `:344-350` |
| Lección | `readText` | lee la regla y los errores típicos | no | `:344-350` |
| Lección | `roleplay` | escucha un diálogo réplica a réplica (no produce) | no | `:997-1030` |
| Diagnóstico | `eleccion`, `natural`, `significado`, `contexto`, `situacion`, `error`, `escucha` | selección entre 4 opciones (`escucha` = audio y opciones) | sí | `diagnostico.dart:28-41` |
| Diagnóstico | `completar`, `corta` | escribir la palabra; coincidencia con `aceptadas` | sí | `:717-720` |
| Diagnóstico | `dictado` | escribir lo oído; similitud ≥0,8 | sí | `:711-716` |
| Diagnóstico | `ordenar` | ordenar fichas | sí | `:717-720` |
| Diagnóstico | `escritura` | 3–7 frases evaluadas por IA de 1 a 10 | sí (IA) | `backend/src/routes/diagnostico.ts:34-73` |
| Biblioteca en | los mismos `TipoDiag` sobre `biblioteca.json` | práctica por habilidad | sí (`registrarPractica`) | `library_screen.dart:189,282` |
| Biblioteca en | lectura y listening por unidades | pasaje y 3 preguntas de opción múltiple | sí, marcado `comprobacion_guiada` | `learning_unit_screen.dart:105-116` |
| Biblioteca en | guías de gramática | 2 preguntas de opción múltiple más una producción "Dilo a tu manera" | opción múltiple sí; la producción **no** | `grammar_screen.dart:45-52,429` |
| Situaciones en | conversación con tutor IA (modo práctica o prueba) | producción libre, oral o escrita | **no** (solo correcciones) | `backend/src/lib/situaciones.ts:44`, `providers.dart:505-534` |
| Fundamentos-v1 en | tarjetas y comprobaciones | selección y 2 de ordenar | guiada (`conApoyo`) | `foundations_screen.dart:107-120` |
| Examen de nivel | opción múltiple | 10 preguntas | sí, aprobado al 65 % | `exam_screen.dart:22-57`, `models.dart:60` |

### Cantidades por nivel e idioma (lecciones generadas por código)

Los niveles 1–2 de los 10 idiomas tienen JSON con 20 unidades por nivel. Cada nivel suma 160 palabras, 120 frases, 80–82 líneas de diálogo y 60 preguntas de examen. La composición es idéntica en todos los idiomas. Cada unidad genera 5 lecciones con un patrón fijo (`curriculum.dart:616-627`):

| Pasos por unidad (niveles 1–2) | flash | MC | fillBlank | image | match | order | listenWrite | speak | readText | roleplay | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| en, es, fr, de, pt, it, ko, ru | 4 | 6 | 3 | 1 | 3 | 4 | 4 | 3 | 1 | 2 | **31** |
| zh, ja (1 ordenar pasa a MC) | 4 | 7 | 3 | 1 | 3 | 3 | 4 | 3 | 1 | 2 | 31 |

Esto da 620 pasos por nivel. Etiquetas de habilidad por unidad: vocabulario 14, frases 4, gramática 4, listening 4, pronunciación 3 y conversación 2. **Lectura y escritura: 0**. `Skill.lectura` no se usa en el código y `Skill.escritura` solo aparece en los scripts de Fundamentos.

**Niveles 3–10 (todos los idiomas):** 28 pasos por unidad (sin `readText` ni `roleplay`), 560 por nivel, construidos con **6 palabras y 3 frases inglesas por nivel** repetidas en 20 unidades (`curriculum.dart:349-412,453`). No son evaluables como nivel real.

**Fundamentos (nivel 0)** (`fundamentos.dart:100-205`, 8 unidades por idioma):

| Idioma | Lecciones | flashcard | MC | matchPairs | speak | Puntúan como selección |
|---|---|---|---|---|---|---|
| en / es / fr / pt / it / ru | 40 | 89–95 | 173–174 | 48 | 48 | 221 de 269 (82 %) |
| de / ko | 42 | 95 / 100 | 179 / 180 | 50 | 50 | 82 % |
| zh | 44 | 102 | 187 | 52 | 52 | 82 % |
| ja | 48 | 119 | 205 | 56 | 56 | 82 % |

En Fundamentos no hay listening sin texto, ni discriminación de sonidos o tonos, ni trazado o escritura del sistema gráfico, ni dictado.

### Bancos de inglés (biblioteca y diagnóstico)

| Banco | Ítems | Por tipo | Por nivel |
|---|---|---|---|
| `en/biblioteca.json` (**lo usa el diagnóstico en inglés** y también la práctica) | 116 | contexto 36 · escucha 30 · escritura 20 · completar 10 · ordenar 10 · significado 10 | 10 por nivel en 1–10 (26 en el nivel 5); **sin nivel 0** |
| `en/diagnostico.json` | 87 | elección 19, completar/natural/significado/contexto 9 cada uno, escucha 8, situación 8, error 6, dictado 5, escritura 5 | 0–10. **No se carga en tiempo de ejecución:** `precargar` lee `biblioteca.json` para `en` (`diagnostico.dart:203`). Los otros 9 idiomas no tienen `diagnostico.json`. |
| `reading_units.json` | 20 unidades / 60 MC | pasaje de 42–45 palabras (nivel 1) a 132–141 (nivel 10) | 2 unidades por nivel |
| `listening_units.json` | 20 unidades / 60 MC | pasaje de 39–41 palabras (nivel 1) a 117–122 (nivel 10) | 2 unidades por nivel |
| `grammar_guides.dart` | 43 guías / 86 MC y 43 consignas de producción sin nota | niveles 1:5, 2:6, 3:4, 4:5, 5:5, 6:5, 7:4, 8:4, 9:3, 10:2 | — |
| `situaciones.json` | 50 situaciones / 150 objetivos | conversación con IA | — |
| `foundations.dart` (v1) | 6 unidades · 14 tarjetas · 13 comprobaciones (2 de ordenar) | guiado | — |

### Selección frente a producción (sobre ítems que puntúan)

| Flujo | Selección (MC, hueco con opciones, imagen, parejas) | Ordenar | Producción controlada (dictado, completar, repetir) | Producción libre puntuada |
|---|---|---|---|---|
| Lección niveles 1–2 (24 puntuables por unidad) | 13 (54 %) | 4 (17 %) | 7 (29 %) | **0** |
| Fundamentos | 82 % | 0 | 18 % (repetir, opcional) | 0 |
| Diagnóstico en (recorrido de 10) | 6 (60 %) | 1 | 1 (completar) | 2 escrituras (20 %; pesan el 35 % de la nota final) |
| Banco `biblioteca.json` | 76 (66 %) | 10 (9 %) | 10 (9 %) | 20 (17 %) |
| Examen de ascenso | 10 (100 %) | 0 | 0 | 0 |

## Auditoría por habilidad (con evidencia)

| Habilidad | Se enseña | Se practica | Se evalúa | No se puede medir hoy |
|---|---|---|---|---|
| **Vocabulario** | tarjetas (`curriculum.dart:515`), guías de situación | MC, parejas, imagen | MC en lección y examen; `significado` en el diagnóstico | recuperación activa (escribir la palabra a partir del significado), uso en contexto nuevo, retención diferida |
| **Gramática** | `readText` con la regla de la unidad (`curriculum.dart:595-603`); 43 guías (solo en) | hueco **con opciones**, ordenar | MC del examen (`exam_screen.dart:34-45`); `completar` y `ordenar` en el diagnóstico | transformación, corrección de errores producida, uso en producción libre (la consigna existe pero no se puntúa: `grammar_screen.dart:429`) |
| **Lectura** | estrategia y vocabulario previo en `reading_units` (solo en) | 60 MC con texto visible, marcadas `conApoyo` (`learning_unit_screen.dart:114`) | `contexto` en el diagnóstico (2 ítems en el recorrido en) | lectura extensa (≥C1 son 132–141 palabras), inferencia y organización del texto, lectura en otros 9 idiomas (no hay banco) |
| **Listening** | `listening_units` (en), audio lento hasta nivel 3 (`diagnostico_screen.dart:333`) | dictado de la frase ya vista con pista (`curriculum.dart:563-570`); 60 MC en `listening_units` | 3 `escucha` en el recorrido en; en otros idiomas el "listening" se genera como `eleccion` sin audio (`diagnostico.dart:482`) | escucha independiente (repeticiones ilimitadas y contadas, pero no limitan: `diagnostico_screen.dart:373`); si terminó el audio (`played` = inició); textos largos, acentos, velocidad natural |
| **Speaking** | diálogo modelo (`roleplay` solo escucha) | chat con tutor IA en 50 situaciones; repetición | **nada puntúa**; el diagnóstico lo excluye (`diagnostico_screen.dart:316,463`) | fluidez, interacción, adecuación, alcance, coherencia; tampoco hay rúbrica ni grabación conservada como evidencia |
| **Escritura** | solo scripts no latinos en Fundamentos; consignas de gramática | consigna libre sin nota (guías) | IA 1–10 en diagnóstico y biblioteca (`diagnostico.ts:40-73`) con subnotas que el cliente **descarta** (solo usa `puntuacion`) | rúbrica por criterio con anclas por nivel, cumplimiento de tarea medido, fiabilidad (sin doble evaluación ni muestras ancla), escritura en lección y examen |
| **Pronunciación** | audio TTS | `speak`: STT → `similitud` de Levenshtein por palabra (o carácter en zh/ja) ≥0,6 (`voz.dart:487-594`) | la misma similitud, y pesa en `aciertos` de la lección | segmentos (pares mínimos), tonos (zh), acento y entonación, inteligibilidad. El STT corrige hacia palabras reales y **oculta errores fonéticos**. Una frase bien pronunciada puede fallar por error de STT, y viceversa. |

Notas transversales:
- `porHabilidad` cuenta **pasos vistos**, no aciertos (`providers.dart:169-178`). La barra de habilidades mide exposición.
- Las `vidas` bajan pero no detienen la lección (`lesson_player_screen.dart:58`).
- `registrarPractica` guarda `primeraCorrecta`/`primeraFecha` (`providers.dart:457-499`). Es la única pieza que sirve para evidencia independiente, pero solo la usan la biblioteca y las situaciones inglesas. El reproductor de lecciones no la usa: guarda `puntuaciones` como máximo histórico (`:576-580`).
- `PRUEBA-NIVEL.md` describe el algoritmo por bloques de `PruebaNivel`. En tiempo de ejecución solo se usa `PruebaNivel.bancoNivel` como banco de respaldo (`diagnostico.dart:222`). **Lo documentado no está activo.**
- `docs/COMPETENCIAS-ASCENSO-PROPUESTA.json` declara `automaticPromotionEnabled: false` y un umbral del 80 %. El código sigue ascendiendo con el examen de 10 MC al 65 %. **Es una propuesta que no está implementada.**

## Progresión por habilidad y nivel

Los descriptores están redactados por OneLingo a partir de las capacidades del CEFR Companion Volume (2020): niveles Pre-A1…C2, escalas de recepción, producción, interacción, mediación y control fonológico. No son texto oficial. D = corrección determinista; IA = requiere modelo (con rúbrica y revisión); H = revisión humana recomendada para calibrar.

### Catálogo de tareas

| Tarea | Habilidad principal | Niveles | Corrección | En el código |
|---|---|---|---|---|
| Ordenar palabras | gramática / sintaxis | 0–4 | D | sí |
| Completar (con opciones) | gramática / vocabulario | 0–6 | D | sí (`fillBlank`) |
| Completar (abierto, lista de aceptadas) | gramática | 1–8 | D (lista) / IA (variantes) | solo en el diagnóstico |
| Relacionar | vocabulario / escritura | 0–4 | D | sí |
| Dictado | listening y ortografía | 1–8 | D (distancia de edición) | sí (con ayudas) |
| Discriminación de sonidos / pares mínimos / tonos | pronunciación (percepción) | 0–4 | D | **no** |
| Respuesta corta | lectura / listening | 1–8 | D (aceptadas) + IA opcional | solo en el diagnóstico |
| Transformación (reescribir con palabra clave) | gramática | 4–10 | D (aceptadas) + IA | **no** |
| Lectura con varias preguntas | lectura | 1–10 | D | sí (en, 3 preguntas) |
| Escucha con varias preguntas | listening | 1–10 | D | sí (en, 3 preguntas) |
| Descripción de imagen | speaking / escritura | 1–8 | IA + rúbrica | **no** |
| Conversación con objetivo | interacción oral | 1–10 | IA + rúbrica (y H para calibrar) | parcial (no puntúa) |
| Escritura guiada a libre | escritura | 1–10 | IA + rúbrica (y H) | parcial (diagnóstico y biblioteca en) |
| Corrección de errores (producida) | gramática / edición | 3–10 | D (aceptadas) + IA | solo detectar (`error`, MC) |
| Producción libre (exposición, argumentación) | speaking / escritura | 5–10 | IA + rúbrica + H | **no** |
| Repetir / leer en voz alta | pronunciación | 0–6 | hoy: STT (D aproximado); válido: evaluación acústica | sí (limitado) |

### Lectura

| Nivel | Capacidad observable | Tareas | Corrección |
|---|---|---|---|
| 0 Fundamentos | reconocer letras o caracteres y palabras aisladas apoyadas en imagen | relacionar grafía con imagen o sonido | D |
| A1 (1–2) | extraer nombres, números, horas y lugares de avisos y mensajes muy breves | lectura de 40–60 palabras con 3–5 preguntas; respuesta corta | D |
| A2 (3–4) | localizar información en textos cotidianos (horarios, correos) y entender la secuencia | varias preguntas, relacionar textos con personas | D |
| B1 (5–6) | seguir la idea principal y detalles de textos sobre temas conocidos; reconocer opinión | 250–400 palabras, MC y respuesta corta, texto con huecos de oraciones | D |
| B2 (7–8) | comprender argumentos, postura del autor y detalle en textos extensos | textos largos, relacionar párrafos, inferencia | D |
| C1 (9–10) | captar implicaciones, matiz, registro y organización en textos complejos | textos largos y densos, texto con párrafos retirados, síntesis breve | D + IA (síntesis) |
| C2 (plan.) | leer críticamente casi cualquier texto, incluso abstracto o literario | comparar textos, síntesis y evaluación | IA + H |

### Listening

| Nivel | Capacidad observable | Tareas | Corrección |
|---|---|---|---|
| 0 | distinguir sonidos, sílabas o tonos y reconocer palabras oídas | pares mínimos, elegir la palabra oída, tono (zh) | D |
| A1 | captar números, precios, horas y peticiones simples dichas despacio | escucha con 3–5 preguntas, dictado corto sin pista | D |
| A2 | entender lo esencial de anuncios y conversaciones rutinarias | varias preguntas, completar una nota con lo oído | D |
| B1 | seguir ideas principales de charlas y conversaciones sobre temas familiares, a velocidad normal | monólogo o diálogo de 1–3 min, MC y completar | D |
| B2 | seguir argumentación, actitud y detalle en discurso extenso | entrevista, relacionar hablantes con opiniones | D |
| C1 | comprender discurso no estructurado, implícitos y registro variado | conferencias, varios hablantes, respuesta corta | D + IA |
| C2 | seguir cualquier discurso nativo rápido, con acento o jerga | tareas integradas (escuchar y escribir) | IA + H |

Condiciones de evidencia para listening: texto oculto, número de reproducciones limitado y registrado (1–2 en evaluación), audio completado (no solo iniciado), transcripción revelada = práctica asistida.

### Speaking (producción e interacción)

| Nivel | Capacidad observable | Tareas | Corrección |
|---|---|---|---|
| 0 | decir palabras y saludos modelados de forma inteligible | repetir, responder "¿cómo te llamas?" | D (aprox.) + escucha propia |
| A1 | presentarse, pedir y dar datos personales con frases memorizadas | responder 5 preguntas personales, pedir algo en una situación | IA con rúbrica breve |
| A2 | describir rutinas y personas, y hacer transacciones sencillas | describir una imagen, juego de rol transaccional | IA |
| B1 | narrar experiencias, dar opinión con razones y mantener conversación sobre temas conocidos | contar una historia, discusión breve, 1 min de monólogo | IA + H (calibración) |
| B2 | argumentar, comparar opciones, interactuar con naturalidad y reparar malentendidos | discusión colaborativa, comparar fotos, 2 min de monólogo | IA + H |
| C1 | exponer de forma estructurada y fluida y adaptar el registro | presentación, entrevista con preguntas de seguimiento | IA + H |
| C2 | expresarse con precisión y matiz sin esfuerzo aparente | debate, mediación de un texto | H |

### Escritura

| Nivel | Capacidad observable | Tareas | Corrección |
|---|---|---|---|
| 0 | escribir letras o caracteres y palabras copiadas o dictadas | trazado, copia, dictado de palabra | D |
| A1 | escribir frases sobre sí mismo y rellenar formularios | completar un formulario, 3–5 frases guiadas | D + IA |
| A2 | notas y mensajes breves conectados con *y, pero, porque* | mensaje de 25–50 palabras con 3 puntos obligatorios | IA con rúbrica |
| B1 | correos y relatos cohesionados sobre temas conocidos | correo de ~100 palabras, historia | IA |
| B2 | ensayo o artículo que argumenta y compara | 140–190 palabras, dos tareas | IA + H |
| C1 | textos claros y bien organizados en registro adecuado (informe, propuesta) | 220–260 palabras | IA + H |
| C2 | reformular, sintetizar y evaluar fuentes con estilo apropiado | ensayo de síntesis | H |

### Pronunciación (control fonológico)

| Nivel | Capacidad observable | Tareas | Corrección |
|---|---|---|---|
| 0 | percibir y producir los sonidos y tonos contrastivos del idioma | pares mínimos (percepción), repetir sílabas | D (percepción); acústica (producción) |
| A1–A2 | inteligible con esfuerzo del oyente; acento L1 evidente | leer en voz alta, repetir frases | evaluación acústica (fonema/tono), no STT |
| B1 | generalmente inteligible, con errores que ocasionalmente dificultan | monólogo breve | IA acústica + H |
| B2–C1 | inteligible, con acento y entonación que apoyan el significado | monólogo y conversación | IA acústica + H |
| C2 | varía la entonación y el énfasis para matizar | — | H |

**Decisión técnica:** mientras solo haya STT, la actividad debe llamarse "Repetición (comprobación de palabras reconocidas)". No debe alimentar "pronunciación" ni el dominio.

### Gramática y vocabulario (conocimiento lingüístico)

Progresión: reconocer en contexto (MC) → recuperar (completar abierto) → producir de forma controlada (transformación, ordenar, corregir) → usar libremente (escritura o speaking con rúbrica). Un objetivo gramatical solo cuenta como dominado cuando hay evidencia en al menos dos de estos escalones, con al menos uno de producción.

## Diagnóstico: estado actual y diseño conectado al grafo

### Lógica real

| Aspecto | Inglés (`personalizado = idiomaContenido=='en'`, `diagnostico_screen.dart:107`) | Otros 9 idiomas |
|---|---|---|
| Inicio | nivel declarado 0–10 (autoevaluación y control deslizante) | igual |
| Recorrido | fijo de 10 ítems: comprensión×2, listening×3, gramática×2 (completar, ordenar), vocabulario×1, escritura×2 (`diagnostico.dart:400-411`) | adaptativo de 10–25 ítems: habilidad menos medida entre 8 y tipo menos usado (`:465-499`) |
| Fuente de ítems | `biblioteca.json` a ±1 nivel, y la IA si falta (`:531-556`) | IA si hay servidor; si no, banco de respaldo (`:571`), que en niveles ≥3 **es inglés** |
| Actualización | por habilidad: declarado ±0,5 por respuesta, recortado a [1,10]; media de 4 habilidades (`:430-438,728-735`) | ±0,5 (±0,75 si el ítem está alejado); −0,25 si el fallo se concentra en una habilidad (`:736-752`) |
| Detención | tras 10 ítems | ≥10 ítems, estable (rango ≤0,5 en las últimas 4) y escritura hecha, o 25 ítems (`:465-467,691-695`) |
| Nivel final | 0,65·objetivo + 0,35·escritura IA, redondeado a 0,5 (`:814-818`) | igual |
| Perfil por habilidad | estimación por habilidad | nivel medio de los ítems + (precisión − 0,5)·3, con 1–3 ítems (`:833-840`) |
| Confianza | 0,4 + 0,03·n + … (heurística, no psicométrica) (`:865-867`) | igual |
| Plan | IA con actividades de `BancoDiag.de('en')` **incluso para otros idiomas** (`diagnostico_screen.dart:299`) | `planDe`: busca palabras del tema en títulos de unidad (`:896-933`) |
| Aplicación | `guardarDiagnostico` → `nivelInicial` clamp 1–10 y `fundamentos = nivel==0` (`providers.dart:445-455`); el alumno puede elegir el nivel recomendado, uno menos o 0 (`diagnostico_screen.dart:1298-1310`) | igual |

### Defectos

1. **Anclaje en inglés.** Con 8 ítems objetivos repartidos en 4 habilidades, la estimación objetiva solo puede variar **±1,0** respecto al nivel declarado. Quien declara 1 y tiene un C1 real acaba en torno a 4,5–5 aunque su escritura obtenga 9. Además, nunca se recomienda el nivel 0 por la propia prueba.
2. **Listening sin audio en los otros idiomas.** `tiposPorSkill` no tiene `listening` y cae en `eleccion` (`:482`).
3. **Ítems de IA sin calibrar.** Los descriptores de nivel de la IA son gramaticales y anglocéntricos, por ejemplo verbos compuestos o inversiones (`diag_ia.ts:57-71`), y se aplican a zh, ja, ko y ru. Ningún ítem generado se revisa antes de puntuarlo.
4. **Banco compartido.** El diagnóstico inglés y la práctica de biblioteca usan los mismos 116 ítems. Repetir el diagnóstico tras practicar mide memoria de ítems.
5. **Sin speaking ni pronunciación.** Tampoco hay ítems de nivel 0 en el banco inglés.
6. **El perfil por habilidad no cambia la ruta.** Solo cambia el nivel global. El perfil se usa en la biblioteca inglesa (`biblioteca.dart:13-52`), pero **no** para omitir o asignar unidades.
7. **Evaluación de escritura de un solo intento.** La IA devuelve subnotas (gramática, vocabulario, coherencia, naturalidad) que el cliente descarta. `evaluarLocal` existe pero no se usa en pantalla.

### Diseño propuesto: diagnóstico conectado al grafo de unidades

**Perfil (7 dimensiones).** Cada una tiene estado, nivel estimado (0–10 más C2 reservado), número de ítems y confianza. Las dimensiones son gramática, vocabulario, lectura, listening, speaking, escritura y pronunciación. Una dimensión sin evidencia queda `sin_evidencia`, **nunca 0**.

**Estados por unidad del grafo** (DEC-003: la lógica es común y los datos van por idioma):

| Estado | Regla |
|---|---|
| `dominada` | comprobación breve (3–4 ítems nuevos de la unidad) ≥80 % en primera respuesta, con sus prerrequisitos `dominada`; sigue pendiente de retención (se programa un repaso a ≥1 día) |
| `omitible` | su nivel está ≥1 por debajo del nivel estimado y la dimensión principal tiene confianza alta. Puede omitirse sin comprobación **solo** si no es prerrequisito de una unidad aún no comprobada; en ese caso es obligatoria una comprobación breve |
| `a_estudiar` | falló la comprobación, o es prerrequisito de algo fallado |
| `sin_evidencia` | no se comprobó (p. ej. speaking sin micrófono); se recomienda, pero no bloquea otras rutas |

**Reglas adaptativas:**
1. Arranque en el nivel declarado, con un primer ítem **un nivel por debajo** para asentar la confianza. La autoevaluación solo elige el punto de partida; no fija límites.
2. Escalada: bloques de 5–8 ítems por nivel candidato, con al menos 2 de listening con audio y 1 de producción (completar abierto u ordenar). Se sube si hay ≥75 % en primera respuesta; se baja si hay ≤40 %. Entre ambos valores se añade un bloque de desempate.
3. Detención: dos bloques consecutivos que acotan (aprueba N y falla N+1), o 30 ítems objetivos, o 20 minutos.
4. Se comprueban los prerrequisitos del nivel resultante: por cada unidad raíz del nivel N, 1–2 ítems. Si domina, la unidad queda `dominada` o `omitible`. Si falla, la unidad pasa a `a_estudiar` y **recibe enseñanza**; no se le dan más preguntas.
5. **No ubicar por encima de habilidades no dominadas.** Nivel de ruta = min(nivel de gramática+vocabulario, nivel de lectura, nivel de listening) + 0,5 como máximo si la producción lo avala. Speaking y pronunciación sin evidencia no suben ni bajan el nivel, y se marcan explícitamente.
6. Peso real propuesto para el nivel CEFR estimado (no para la ruta): lectura 20 %, listening 20 %, gramática y vocabulario 20 %, escritura 20 %, speaking 20 %. Si falta speaking, se informa "estimación parcial (4/5 habilidades)" en lugar de repartir su peso.
7. Producción: 1 escritura siempre (desde A1) y 1 tarea oral opcional pero recomendada. Ambas con rúbrica por criterios (cumplimiento, alcance, corrección y coherencia, más pronunciación e interacción en la oral), con anclas por nivel y marcas de "revisión humana" si la IA duda.
8. Ítems: el banco de evaluación de diagnóstico va separado del de práctica y está versionado por idioma. Los ítems de IA solo entran en el banco tras revisión (estado `revisado`). En vivo solo se usan ítems revisados.

**Resultado (esquema orientativo):**
```json
{"idioma":"fr","version":"diag-v4","nivelRuta":3,"cefrEstimado":"A2 (orientativo)",
 "perfil":{"gramatica":{"nivel":3.5,"n":7,"conf":"media"},"listening":{"nivel":2.5,"n":6,"conf":"media"},
           "speaking":{"estado":"sin_evidencia"}},
 "unidades":{"fr.A1.u04":"dominada","fr.A1.u07":"a_estudiar","fr.A1.u02":"omitible"},
 "plan":[{"unidad":"fr.A1.u07","motivo":"falló comprobación: artículos partitivos"}]}
```

## Modelo de evaluación y criterios de ascenso

### Cuatro tipos de evaluación

| Tipo | Cuándo | Banco | Qué decide | Estado hoy |
|---|---|---|---|---|
| Diagnóstica | inicio o cambio de idioma | evaluación (diagnóstico) | punto de entrada y unidades `omitible`/`a_estudiar` | existe, con defectos (sección anterior) |
| Formativa | dentro de cada lección | práctica (con ayudas) | feedback inmediato y repaso; **nunca** dominio | existe (lecciones, biblioteca), pero se confunde con dominio |
| Acumulativa (unidad y módulo) | fin de unidad; fin de módulo (4–5 unidades) | evaluación, ítems nuevos | `dominada` y desbloqueo por grafo | **no existe** |
| Ascenso de nivel | tras dominar las unidades del nivel | evaluación, por habilidad, con producción | subir de nivel interno | examen de 10 MC al 65 % (inválido como evidencia) |

### Evidencia independiente (reglas)

Un ítem cuenta para el dominio solo si se cumplen todas estas condiciones:
- Es **la primera respuesta** a un ítem **nuevo** para ese alumno. Se excluyen la misma familia de ítem y los cambios cosméticos.
- Se respondió **sin ayuda**: sin transcripción, sin pista, sin traducción visible y con reproducciones dentro del límite.
- No hubo **fallo técnico**: si el audio no terminó o el micrófono falló, cuenta como "sin evidencia", no como error.
- Se evalúa **con clave oculta** hasta cerrar el bloque.

La **retención** se mide con una nueva comprobación, con ítems distintos, a ≥1 día (piloto: 1 y 7 días). Cada evento guarda: `itemId@version`, `banco` (practica o evaluacion), `modo`, `primeraRespuesta`, `ayudas[]`, `reproducciones`, `audioCompleto`, `rubricaVersion` y `evaluador` (D, IA o H).

### Separación de bancos

| Banco | Contenido | Uso |
|---|---|---|
| Enseñanza | ejemplos, explicaciones, modelos | nunca se evalúa |
| Práctica | ítems generados o con plantilla; se pueden repetir | formativa, repaso espaciado |
| Evaluación | ítems revisados por humano, versionados, ≥3 formas paralelas por unidad, no mostrados en práctica | acumulativa, ascenso, diagnóstico |
| Anclas de producción | respuestas de muestra puntuadas por humanos por nivel y criterio | calibrar la IA de escritura y speaking |

### Criterios observables para ascender de nivel interno (propuesta de piloto)

1. Todas las unidades del nivel están `dominada`, con retención comprobada en ≥1 día para al menos el 80 % de ellas.
2. Prueba de ascenso por habilidad, con ítems nuevos:

| Habilidad | Umbral |
|---|---|
| Lectura | ≥75 % |
| Listening | ≥75 % (máx. 2 reproducciones) |
| Gramática y vocabulario | ≥80 % |
| Escritura | rúbrica ≥ "adecuado" en los 4 criterios del nivel |
| Speaking | rúbrica ≥ "adecuado" si hay evidencia; si no la hay, se asciende con la etiqueta "oral sin evaluar" |

3. Ninguna habilidad objetiva puede quedar por debajo del 60 %: una media alta no compensa una habilidad débil.
4. Si no aprueba, no hay reintento inmediato con el mismo banco. Primero la ruta de refuerzo; después, otra forma paralela.

Los umbrales son hipótesis de producto sin validar (coinciden con `COMPETENCIAS-ASCENSO-PROPUESTA.json`). Requieren un piloto.

### Tres afirmaciones que deben mostrarse por separado

| Afirmación | Significado | Evidencia mínima | Texto sugerido para la interfaz |
|---|---|---|---|
| **Dominio del curso** | domina las unidades de OneLingo | reglas anteriores | "Has dominado 18/20 unidades del Nivel 3" |
| **Equivalencia CEFR estimada** | nuestra mejor estimación orientativa | diagnóstico y pruebas de ascenso con las 4–5 habilidades; sin estudio de vinculación | "Estimación orientativa: A2 (lectura B1, oral sin evaluar). No es un certificado." |
| **Preparación para certificación** | práctica del formato de un examen y una edición concretos | ruta específica, simulacros cronometrados, rúbricas del constructo; predicción solo con datos externos | "Has practicado todas las partes del formato B1 Preliminary. No predecimos tu resultado." |

## Certificaciones (tabla) — dominio vs CEFR vs certificación

Las tareas están descritas con palabras propias. No se reproducen ítems. Las equivalencias CEFR son las que publica cada organismo, si las publica.

| Examen (idioma) | Habilidades evaluadas | Tipos de tarea (resumen) | CEFR | Qué necesitaría OneLingo para una ruta de preparación |
|---|---|---|---|---|
| **A2 Key** (en) | lectura y escritura (7 partes, 60 min), listening (5 partes, ~30 min), speaking en parejas (2 partes) | avisos breves, textos con MC, cloze, mensaje corto e historia con imágenes; listening de detalles; entrevista e intercambio | A2 | listening de varias preguntas con 2 reproducciones, escritura guiada de 25–35 palabras con rúbrica, speaking en pareja simulada con IA |
| **B1 Preliminary** (en) | lectura (6 partes, 45 min), escritura (2 tareas de ~100 palabras), listening (4 partes, se oye 2 veces), speaking (4 partes) | relacionar descripciones, cloze léxico y abierto, correo más artículo o historia, descripción de foto, discusión | B1 | cloze abierto, correo con puntos obligatorios, descripción de foto oral, discusión con IA con rúbrica |
| **B2 First** (en) | lectura y uso del inglés (7 partes, 1 h 15), escritura (2 partes, 1 h 20), listening (4 partes), speaking (4 partes, 14 min en pareja) | cloze MC y abierto, formación de palabras, **transformación con palabra clave**, texto con huecos, ensayo de opinión, completar oraciones al escuchar, comparar fotos | B2 | tipo "transformación" y "formación de palabras" (hoy no existen), ensayo de 140–190 palabras con IA y anclas, monólogo oral de 1 min |
| **C1 Advanced** (en) | lectura y uso (8 partes, 56 preguntas, 90 min), escritura (2 textos, 90 min), listening (4 partes, 30 preguntas), speaking (4 partes, 15 min) | lo anterior con textos académicos y profesionales; ensayo obligatorio y propuesta, informe o reseña | C1 | textos largos (hoy C1 = 132–141 palabras), escritura de registro, resolución colaborativa oral |
| **C2 Proficiency** (en) | lectura y uso (7 partes, 53 preguntas), escritura (ensayo de síntesis de 240–280 más otro de 280–320), listening (4 partes), speaking (3 partes, 16 min) | síntesis de dos textos, discurso extenso, matiz | C2 | nivel C2 inexistente (DEC-002); requiere niveles 11–12 o una ruta aparte |
| **IELTS Academic / GT** (en) | listening (4 partes, 40 preguntas, ~30 min), lectura (3 textos, 40 preguntas, 60 min), escritura (T1 describir un gráfico de 150 palabras y T2 argumentar 250; GT difiere en T1), speaking (3 partes, 11–14 min) | completar notas, tablas y formularios, emparejar, verdadero/falso/no dado, entrevista, monólogo con tarjeta, discusión | bandas 0–9 (no son niveles) | escritura sobre datos visuales, monólogo de 2 min con preparación, criterios de banda propios. **No** mostrar bandas estimadas sin estudio de equivalencia |
| **TOEFL iBT** (formato desde 21-01-2026) (en) | lectura (50 ítems, 30 min), listening (47, 29 min), escritura (12, 23 min), speaking (11, 8 min); escala 1–6 más 0–120 de transición | completar palabras, textos cotidianos y académicos, elegir respuesta, anuncio, clase; construir oración, correo, discusión académica; **escuchar y repetir**, entrevista | escala propia (ETS publica una relación con CEFR) | "construir oración" y "completar palabras" (fáciles, D), correo, foro académico con IA, repetición con evaluación **acústica** (la de hoy por STT no sirve) |
| **DELF / DALF** (fr) | comprensión oral y escrita, producción escrita y oral (4 × 25 puntos; ≥50/100 y ≥5/25 por prueba) | MC en comprensión, cartas, artículos y síntesis (C1–C2), exposición oral | A1–B2 (DELF), C1–C2 (DALF) | banco francés propio (hoy no existe más allá de A1 genérico); producción con rúbrica por prueba; regla de mínimo por habilidad |
| **Goethe-Zertifikat** (de) | Hören, Lesen, Schreiben, Sprechen; de B1 a C2 por módulos; ≥60/100 por módulo | anuncios y diálogos, textos, correos y opiniones, presentación y planificación en pareja | A1–C2 | módulos por habilidad (encaja con el perfil de 7 dimensiones); tareas de planificación conjunta oral |
| **CELI** (Perugia) / **CILS** (Siena) (it) | escucha, lectura, estructuras (análisis de la lengua en CILS), escritura y oral | comprensión, ejercicios estructurales, textos y conversación | CELI 1–5 = A2–C2 (más CELI Impatto A1); CILS A1–QUATTRO-C2 | tareas de "estructuras" (completar y transformar), producción con rúbrica |
| **CELPE-Bras** (pt-BR) | integradas: parte colectiva (4 tareas que combinan comprensión y escritura) y parte individual oral | escribir un texto con propósito a partir de un vídeo, un audio o un texto; entrevista | **no usa CEFR**: Intermedio, Intermedio Superior, Avanzado y Avanzado Superior; sin media entre partes | tareas **integradas** (escuchar o leer y escribir) con género textual y destinatario; es el cambio de diseño más grande |
| **DELE / SIELE** (es) | DELE: 2 grupos (lectura y escritura; audición y oral), apto si ≥30/50 en cada uno; C2 en 3 pruebas integradas. SIELE: 4 pruebas, 0–1000, multinivel A1–C1 | comprensión, expresión e interacción escrita y oral, tareas integradas en C2 | A1–C2 (DELE); A1–C1 (SIELE) | depende de DEC-004 (el curso de español para no hispanohablantes); contenido de español como lengua extranjera propio |
| **HSK / HSKK** (zh) | HSK 2.0: 6 niveles (listening y lectura; escritura desde HSK 3); HSKK oral aparte. HSK 3.0: "3 etapas, 9 niveles" (escuchar, hablar, leer, escribir, traducir), **en fase piloto** | elegir según audio o imagen, ordenar, escribir caracteres, traducción (niveles 7–9) | **el organizador no publica una alineación oficial con CEFR** en las páginas consultadas; no afirmarla | escritura de caracteres (D), tonos (percepción D; producción acústica), listas de caracteres y palabras por nivel. Hay que decidir si se apunta a HSK 2.0 o 3.0 |
| **JLPT** (ja) | conocimiento de la lengua (vocabulario y gramática), lectura y listening; **no evalúa producción** | MC en todas las secciones | desde diciembre de 2025 el informe añade un **CEFR de referencia** según la puntuación (N5→A1 … N1→B2/C1), limitado a recepción | ruta D pura (MC y listening); no confundir con un CEFR global: faltan producción e interacción |
| **TOPIK** (ko) | TOPIK I (niveles 1–2): listening y lectura; TOPIK II (3–6): más escritura; prueba de speaking aparte | MC, escritura de frase y de texto argumentativo corto; formato digital (IBT) en transición | niveles 1–6 propios; no usar como CEFR oficial | escritura en hangul con IA, formato digital; confirmar la edición vigente antes de diseñar |
| **ТРКИ / TORFL** (ru) | lectura, escritura, vocabulario y gramática, listening, oral; ≥66 % **por subprueba** | MC de léxico y gramática, textos, escritura con propósito, diálogos | ТЭУ A1, ТБУ A2, ТРКИ-I…IV = B1–C2 | subprueba de léxico y gramática (encaja con el perfil), mínimo por subprueba, casos y aspecto en ítems D |

**Conclusión:** ninguna ruta de certificación es viable antes de tener:
1. Evaluación de producción con rúbrica calibrada.
2. Listening independiente.
3. Contenido real por idioma por encima del nivel 2.
4. Tipos de tarea ausentes: transformación, texto integrado, monólogo cronometrado y pares mínimos.

Las rutas de preparación deben versionarse por examen y edición (p. ej. `toefl_ibt@2026-01-21`). No deben ofrecer puntuaciones ni probabilidades de aprobar sin un estudio con resultados externos.

## Evaluación de unidad para rutas iniciales

Aplica a las unidades de Fundamentos y A1 inicial (U0–U5 del plan) de cualquier idioma. La lógica es común y los ítems son datos del idioma.

### Estructura (unos 12–15 min, 16–20 ítems, sin feedback hasta el final del bloque)

| Bloque | Ítems | Contenido | Corrección | Adaptación por idioma |
|---|---|---|---|---|
| A. Sonidos y escritura | 4 | 2 pares mínimos o tonos (audio → elegir), 2 relacionar grafía y sonido | D | zh: tonos y pinyin; ja: kana; ko: hangul (composición de sílaba); ru: letras "falsas amigas"; latinos: letras y sonidos que no existen en español |
| B. Vocabulario | 4 | 2 reconocer (imagen o audio → palabra), 2 recuperar (significado → **escribir** o componer la palabra) | D | en escrituras no latinas se permite teclado en pantalla con fichas de caracteres o kana |
| C. Estructura | 3 | 1 ordenar, 1 completar **abierto**, 1 elegir la frase correcta | D | ordenar con fichas aunque el idioma no use espacios |
| D. Listening | 3 | 2 de escuchar y elegir (máx. 2 reproducciones, texto oculto), 1 dictado de palabra o frase corta **nueva** | D | velocidad lenta permitida en Fundamentos; queda registrada |
| E. Lectura | 2 | mini texto (3–4 frases) con 2 preguntas | D | en ja y zh con apoyo de lectura (furigana o pinyin) configurable y registrado como ayuda |
| F. Producción | 2 | 1 escrita guiada (3 frases sobre sí mismo con palabras de la unidad), 1 oral (responder 2 preguntas o presentarse) | IA con rúbrica de 3 criterios: cumple la tarea, usa el objetivo de la unidad, es comprensible | la oral es opcional si no hay micrófono → "sin evidencia", no cero |

Todos los ítems objetivos provienen del **banco de evaluación**, con ≥2 formas paralelas por unidad, y nunca se han mostrado en práctica.

### Criterio de dominio de la unidad

1. **≥80 % en primera respuesta y sin ayuda** en los bloques A–E, con **≥2/3 en cada bloque que tenga ≥3 ítems**. Así, un bloque débil no queda oculto por la media.
2. **Producción aceptable:** la escrita cumple los 3 criterios de la rúbrica. La oral también, si hubo evidencia. Si la IA marca baja confianza, el resultado queda "pendiente de revisión" y no bloquea.
3. **Retención:** una comprobación breve (5–6 ítems nuevos de A–D) a **≥1 día** con ≥80 %. Hasta entonces la unidad es `aprobada_pendiente_retencion`. Desbloquea la siguiente unidad del grafo, pero no cuenta para el ascenso de nivel.

### Si falla: volver a enseñar, no solo más preguntas

| Resultado | Acción |
|---|---|
| Falla un bloque concreto (p. ej. D. Listening) | microlección de ese objetivo: explicación en el idioma de apoyo (DEC-004), ejemplo modelado, práctica guiada con ayudas, y después **otra forma** del bloque |
| <60 % global | repetir la secuencia de enseñanza de la unidad (no solo su práctica) y revisar los prerrequisitos del grafo. Si falla un prerrequisito, se vuelve a esa unidad |
| Producción no aceptable | feedback con la versión corregida y el error típico, un modelo nuevo y una nueva consigna distinta; no se repite la misma consigna |
| Retención fallida | la unidad vuelve a `a_repasar`, con repaso espaciado y nueva comprobación a 1–3 días; no pierde su historial |
| 2 fallos seguidos en la misma forma de evaluación | ofrecer ayuda de tutor IA o humano y bajar un escalón del grafo; se registra para revisar la calidad del ítem |

XP, racha y "completar" siguen premiando la constancia, pero **no** cambian el estado de dominio.

## Decisiones que requieren revisión humana

1. **Niveles 3–10 para idiomas ≠ en.** Hoy muestran inglés genérico. Hay dos opciones: ocultarlos o bloquearlos hasta que haya contenido, o mantenerlos. Recomendación: ocultarlos.
2. **Retirar o reconvertir el examen de 10 MC al 65 %** como mecanismo de ascenso. ¿Se desactiva el ascenso automático (como propone el JSON de competencias) mientras no exista la evaluación acumulativa?
3. **Umbrales:** 80 % por unidad, 75/80 % por habilidad en el ascenso, mínimo del 60 % y retención a 1 y 7 días. Son hipótesis que requieren un piloto.
4. **Speaking y pronunciación.** Opciones: invertir en evaluación acústica (fonema o tono) o renombrar la actividad a "repetición" y declarar pronunciación como `sin_evidencia`.
5. **Rúbricas de escritura y speaking** por nivel y criterio, y un corpus de anclas puntuadas por docentes, por idioma. ¿Quién lo produce y lo revisa?
6. **Pesos del CEFR estimado** (20 % por habilidad) y si se muestra con una habilidad sin evidencia.
7. **Diagnóstico en inglés:** sustituir el recorrido fijo de 10 ítems (anclado ±1) por un algoritmo de bloques con banco de evaluación separado.
8. **C2:** crear niveles 11–12 o una ruta aparte (DEC-002).
9. **Certificaciones:** qué examen se prioriza por idioma, con qué edición (HSK 2.0 o 3.0, TOPIK en papel o IBT) y qué lenguaje legal se usa ("preparación", no "equivalencia").
10. **Revisión nativa** de los ítems de evaluación por idioma antes de que decidan un dominio.
11. **Documentación desactualizada:** `PRUEBA-NIVEL.md` (algoritmo no activo) y `en/diagnostico.json` (no se carga). ¿Se archivan o se reactivan?

## Fuentes consultadas (URL y fecha de consulta 2026-09-26)

- Consejo de Europa, CEFR Companion Volume (2020): https://rm.coe.int/cefr-companion-volume-with-new-descriptors-2020/16809ea0d4
- Consejo de Europa, competencia fonológica: https://www.coe.int/en/web/common-european-framework-reference-languages/phonological-competence
- Consejo de Europa, vincular exámenes al CEFR: https://www.coe.int/en/web/common-european-framework-reference-languages/relating-examinations-to-the-cefr
- Cambridge, catálogo de exámenes: https://www.cambridgeenglish.org/exams-and-tests/qualifications/
- Cambridge A2 Key, formato: https://www.cambridgeenglish.org/exams-and-tests/qualifications/key/format/
- Cambridge B1 Preliminary, formato: https://www.cambridgeenglish.org/exams-and-tests/qualifications/preliminary/format/
- Cambridge B2 First, formato: https://www.cambridgeenglish.org/exams-and-tests/qualifications/first/format/
- Cambridge C1 Advanced, formato: https://www.cambridgeenglish.org/exams-and-tests/qualifications/advanced/format/
- Cambridge C2 Proficiency, formato: https://www.cambridgeenglish.org/exams-and-tests/qualifications/proficiency/format/
- IELTS Academic: https://ielts.org/take-a-test/test-types/ielts-academic-test
- IELTS, formato de Listening: https://ielts.org/take-a-test/test-types/ielts-academic-test/ielts-academic-format-listening
- IELTS, formato de Speaking: https://ielts.org/take-a-test/test-types/ielts-academic-test/ielts-academic-format-speaking
- ETS TOEFL iBT, contenido (formato desde el 21-01-2026): https://www.ets.org/toefl/test-takers/ibt/about/content.html
- ETS TOEFL iBT, puntuaciones: https://www.ets.org/toefl/test-takers/ibt/scores/understand-scores.html
- France Éducation international, DELF/DALF: https://www.france-education-international.fr/diplome/delf-tout-public/niveau-b1 y https://www.france-education-international.fr/document/manuel-candidat-delf-a2
- Goethe-Institut, exámenes A1–C2: https://www.goethe.de/de/spr/prf.html
- CVCL Perugia, CELI: https://cvcl.unistrapg.it/pagine/esami-celi-generici
- Università per Stranieri di Siena, CILS: https://cils.unistrasi.it/79/87/Spendibilit%C3%A0_del_Livello_CILS_A1.htm
- Inep, Celpe-Bras: https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/celpe-bras
- Instituto Cervantes, DELE: https://examenes.cervantes.es/es/dele/como · SIELE: https://examenes.cervantes.es/es/siele/como
- Chinese Testing International, HSK y HSK 3.0: https://www.chinesetest.cn/hsk · https://www.chinesetest.cn/syllabus · https://www.chinesetest.cn/HSKK
- JLPT, resumen de niveles: https://www.jlpt.jp/e/about/levelsummary.html · CEFR de referencia: https://www.jlpt.jp/e/about/cefr_reference.html
- TOPIK (NIIED): https://www.topik.go.kr/TWGUID/TWGUID0110.do · https://new.topik.go.kr/main.do
- ТРКИ, Instituto Pushkin: https://www.pushkin.institute/certificates/trki/ · Universidad Estatal de San Petersburgo: https://testingcenter.spbu.ru/ru/ekzameny/russia/trki.html

Nota: no se copiaron ítems ni textos de examen, y los PDF de `work/research/english-curriculum` no se redistribuyen. Revisa formatos y ediciones antes de diseñar cada ruta de certificación, porque TOPIK IBT y HSK 3.0 están en transición.
