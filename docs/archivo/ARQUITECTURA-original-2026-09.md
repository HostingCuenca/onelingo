# OneLingo · Arquitectura y análisis técnico

Cómo se traduce `REQUERIMIENTOS.md` a software. Decisiones tomadas y por qué.

## 0. Stack
- **App**: Flutter 3.47 / Dart 3.13 (Android, iOS y **web**). Misma base que Pollos
  San Carlos: Riverpod, go_router, dio. La web sirve para que el cliente pruebe la
  app desde una URL sin instalar nada.
- **Backend**: Node 20 + Fastify + PostgreSQL + zod (mismo patrón que
  `pollos-san-carlos-backend`). Carpeta hermana `backend/` (fase 2).
- **IA**: API de Claude para conversación, corrección y generación de contenido;
  STT/TTS del dispositivo (`speech_to_text`, `flutter_tts`) en fase 1, voces
  neuronales en servidor más adelante.

## 1. La idea central: el contenido es DATOS, no pantallas
10 idiomas × 10 niveles × 100 lecciones = **10 000 lecciones**. Es imposible (y
absurdo) diseñarlas a mano una por una. Por eso:

1. Existen **~10 tipos de ejercicio** implementados una sola vez en la app
   (el "reproductor de lección").
2. Cada lección es un **JSON** con una lista de pasos (`steps`), cada paso usa uno
   de esos tipos. Lo que se muestra en el diseño de Figma (ordena la frase, escucha
   y escribe, une parejas, elige la respuesta, flashcard, rol con IA…) son
   exactamente estos tipos.
3. Las lecciones se **generan con IA a partir de un plan curricular** (el temario
   de cada nivel en `REQUERIMIENTOS.md`), se revisan y se guardan en la base de
   datos. La app solo las descarga.

### Tipos de ejercicio (`ExerciseType`)
| Tipo | Pantalla de referencia en Figma | Qué evalúa |
|---|---|---|
| `flashcard` | Práctica de Vocabulario: Flashcards | vocabulario |
| `multipleChoice` | Ejercicio: Pedir en el restaurante | comprensión / gramática |
| `fillBlank` | Examen de Gramática, Pedir direcciones | gramática |
| `orderWords` | Ejercicio: Ordena la frase | formación de frases |
| `listenWrite` | Ejercicio: Escucha y escribe | listening / escritura |
| `matchPairs` | Ejercicio: Une los síntomas | vocabulario |
| `imageChoice` | Ejercicio: En la oficina | vocabulario |
| `speak` | Conversación con IA (repite la frase) | pronunciación |
| `roleplay` | Caso: En el restaurante, Rol: en la consulta | conversación |
| `readText` | (lectura corta + preguntas) | lectura |

Cada paso declara qué **habilidad** mide (`vocabulario, gramatica, conjugacion,
listening, pronunciacion, frases, lectura, escritura, conversacion`) → alimenta
las barras del perfil de progreso y la clasificación de errores.

## 2. Modelo de datos (entidades principales)
```
Language        code, nombre, nativo (bool), disponible
Level           languageCode, numero 1..10, nombre, descripcion, temario[]
Lesson          levelId, numero 1..100, titulo, unidad (agrupa ~5 lecciones),
                skills[], steps[] (JSON), xp
Exam            levelId, preguntas (banco), minimoAprobacion = 65
Situation       id 1..50, nombre, icono, descripcionPorNivel{1..10}
Tutor           id, nombre, personalidad (amigable|motivador|profesional|directo), voz

User            id, email, idiomaNativo, plan, trialStartedAt, trialSecondsUsed
Enrollment      userId, languageCode, nivelActual, leccionActual (1..100)
LessonProgress  enrollmentId, lessonId, completadaAt, puntuacion, intentos
ExamAttempt     enrollmentId, levelId, puntuacion, aprobado, fecha
Mistake         userId, languageCode, tipo, original, correccion, explicacion,
                practicada (bool), origen (lessonId | situationId | free)
Conversation    userId, tipo (lesson|situation|free), situationId?, nivel,
                tutorId, mensajes[]
Stats           userId, languageCode, xp, racha, ultimoDia, segundosEstudio,
                vocabAprendido, porHabilidad{...}
```

## 3. Desbloqueo progresivo (regla única)
```
lecciónDesbloqueada(n) = n == 1 || completada(n-1)
examenDesbloqueado(nivel) = completadas(nivel) == 100
nivelDesbloqueado(k) = k == 1 || aprobado(examen(k-1)) || nivelInicialPorPrueba >= k
```
Se calcula en el servidor y la app solo pinta el estado (`bloqueada / actual /
completada`). Las pantallas "Unidad: …" del diseño ya muestran los tres estados.

## 4. Examen final
- 30 preguntas muestreadas del banco del nivel, mezclando todos los tipos y
  habilidades (parámetro configurable).
- ≥ 65 % aprueba → `Enrollment.nivelActual += 1`, `leccionActual = 1`.
- < 65 % → se registran los fallos como `Mistake` y se muestra "Repasa tus
  errores"; reintento permitido (política de espera pendiente con el cliente).
- Nivel 10 aprobado → pantalla "Programa completado" + certificado.

## 5. IA adaptada al nivel (cómo se hace de verdad)
No hay 10 "IAs" distintas: hay **un perfil por nivel** que se inyecta en el
prompt del sistema:
```
LevelProfile {
  nivel, nombre,
  vocabularioMax   (p. ej. 500 palabras en N1, sin límite en N10),
  tiemposPermitidos ["presente"] … ["todos"],
  longitudFrase    "5-8 palabras" … "sin límite",
  velocidadHabla   0.7x … 1.0x,
  correccion       "solo errores graves, explicar en idioma nativo" …
                   "todos los errores, explicar en idioma meta",
  temasPermitidos  [...]
}
```
Prompt final = **tutor** (personalidad) + **perfil de nivel** + **situación**
(descripción para ese nivel) + **idioma nativo del alumno** + historial.
Así "Restaurante" en N1 y en N10 es el mismo `Situation` con distinto perfil.
Las 50 situaciones × 10 niveles no son 500 textos: son 50 descripciones base +
10 perfiles; la descripción por nivel se genera una vez y se guarda.

Cada respuesta de la IA devuelve JSON estructurado:
`{ reply, corrections[{original, corrected, type, explanation}], suggestions[] }`
→ las correcciones se guardan como `Mistake` y aparecen en la sección de errores
con su explicación y botón "Practicar" (regenera un ejercicio de ese error).

## 6. Prueba gratuita y planes
- **Trial**: 60 min de **uso real** medidos en servidor (heartbeats cada 30 s
  mientras la app está en primer plano). Al agotarse → pantalla de planes. Evita
  que el usuario pierda la hora por registrarse y cerrar la app.
- **Planes** = `maxIdiomas` (1/2/3) a $20/$30/$40. El usuario elige qué idiomas
  activar dentro de su cupo; el resto queda visible pero bloqueado (upsell).
- Pagos por tienda (Apple/Google) en móvil y Stripe en web; el backend valida y
  guarda `Subscription {plan, estado, renovacion}`.

## 7. Onboarding
Registro → idioma nativo (define idioma de la interfaz y de las explicaciones) →
idioma a aprender → **prueba de nivel** (20 preguntas adaptativas, o "empiezo de
cero") → inicia trial → tour de 3 pantallas → Lección 1.

## 8. Estructura de la app (Flutter)
```
lib/
  main.dart                 ProviderScope + MaterialApp.router
  app/theme.dart            paleta OneLingo (colores del logo) + Material 3
  app/router.dart           go_router: shell 4 pestañas (Inicio, Aprender,
                            Practicar, Perfil) + rutas de lección/examen/chat
  core/models/              Language, Level, Lesson, Step, Situation, Tutor,
                            Enrollment, Progress, Mistake…
  core/content/             curriculum.dart (temarios), situations.dart (50),
                            level_profiles.dart (10), seed_lessons.dart (demo)
  core/state/               providers Riverpod (sesión, matrícula, progreso)
  core/api/                 api_client.dart (dio) — fase 2
  features/onboarding       bienvenida, registro, idioma nativo, idioma meta,
                            prueba de nivel, trial
  features/home             dashboard (camino de aprendizaje, lección diaria)
  features/course           mapa de niveles, unidad, lista de lecciones
  features/lesson           reproductor de lección (10 tipos de paso) + resultado
  features/exam             examen final + aprobado/no aprobado + programa completado
  features/practice         50 situaciones, conversación libre, tutores
  features/chat             conversación con IA (texto/voz), correcciones
  features/mistakes         sección de errores
  features/progress         perfil y estadísticas
  features/plans            prueba gratuita, planes, pago
  shared/widgets/           Tarjeta, Chip, BarraProgreso, AnilloProgreso, Boton…
```

## 9. Fases
1. **Fase 1 · Demo navegable (web + móvil)**: onboarding completo, dashboard,
   Nivel 1 con lecciones de muestra, reproductor con los 10 tipos, desbloqueo,
   resultado de lección, práctica libre con situaciones y chat de texto con IA,
   errores, progreso y planes. Datos locales (sin backend) para que el cliente
   pruebe en una URL.
2. **Fase 2 · Backend real**: cuentas, progreso en servidor, generación y carga de
   las 1 000 lecciones del primer idioma, exámenes, trial y pagos.
3. **Fase 3 · Escala**: 10 idiomas, voz neuronal, tutores con avatar, notificaciones,
   panel de administración de contenido.

## 10. Riesgos que hay que tener claros
- **Costo de IA**: cada mensaje de conversación consume tokens (y voz). Con $20/mes
  hay que limitar minutos de conversación por día o usar modelos más baratos para
  niveles bajos. Se mide desde la fase 1.
- **Volumen de contenido**: generar 1 000 lecciones de calidad por idioma requiere
  un pipeline (plan curricular → generación → revisión → publicación), no se hace
  "a mano". Es un proyecto en sí mismo.
- **Web y voz**: el reconocimiento de voz en navegador depende del Web Speech API
  (Chrome sí, Safari parcial). En la demo web la conversación es por texto con
  botón de voz "cuando esté disponible".
