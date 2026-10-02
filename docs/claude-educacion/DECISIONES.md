# Decisiones de arquitectura y pedagogía

## DEC-001 — Checkpoint único y Codex pausado

Fecha: 2026-09-26
Problema: el repositorio tenía un solo commit (08-09) y ~120 archivos sin commitear; Codex y Claude podían pisarse.
Decisión: Codex queda pausado. Se crea `checkpoint/onelingo-before-multilang-2026-09-26` (commit `396333b`, tag `checkpoint-2026-09-26-pre-multilang`) con todo el estado, y se trabaja en `claude/educacion-multilenguaje` en la misma carpeta.
Motivo: un único escritor evita divergencias; el checkpoint permite volver al estado exacto previo.
Alternativas descartadas: worktree desde el commit 08-09 (perdía 2,5 semanas de trabajo); dos ramas activas en paralelo.
Archivos afectados: ninguno de código.
Riesgo: el checkpoint incluye ~244 MB de modelos GLB; subirlo a GitHub sin Git LFS infla el repositorio. No se ha hecho push.

## DEC-002 — Conservar la escala interna 0–10

Fecha: 2026-09-26
Estado: reemplazada para la nueva versión curricular por DEC-020; se conserva únicamente como interpretación del progreso histórico.
Problema: se propuso reasignar niveles para que 10 = C2.
Decisión: se conserva 0 = Fundamentos, 1–2 A1, 3–4 A2, 5–6 B1, 7–8 B2, 9–10 C1 (`lib/core/diagnostico.dart:320`). C2 queda en el modelo curricular como `cefr: C2`, `estado: planificado`, `nivelInterno: null` (reservado).
Motivo: cambiar la escala exige migrar progreso, diagnóstico, exámenes, backend e interfaz.
Alternativas descartadas: reasignar 1–10 a pre-A1…C2 ahora.
Archivos afectados: esquema de contenido (campo `nivelInterno` anulable).
Riesgo: ninguno inmediato. Decisión formal pendiente sobre niveles 11–12 para C2.

## DEC-003 — Arquitectura curricular independiente del idioma

Fecha: 2026-09-26
Problema: el contenido profundo existe solo en inglés y varias pantallas dependen de él.
Decisión: la lógica (grafo, dominio, desbloqueo, repaso) vive en código común; cada idioma aporta su propio mapa y rutas en datos. No se traduce el currículo inglés.
Motivo: los sistemas lingüísticos difieren (escritura, género, casos, tonos, partículas).
Alternativas descartadas: plantilla única traducida.
Archivos afectados: por definir tras la auditoría (ver ESQUEMA_CONTENIDO.md).
Riesgo: más contenido que revisar por idioma; requiere revisión nativa.

## DEC-004 — Explicaciones en el idioma nativo del usuario

Fecha: 2026-09-26 (decidido por el usuario: opción a)
Problema: `es` es idioma meta, pero toda la interfaz y las explicaciones están en español; un no hispanohablante no entendería el curso de español.
Decisión: el contenido educativo (explicaciones, traducciones, consignas de unidad) se guarda por **idioma de apoyo** y se muestra en el idioma nativo del usuario, con respaldo en español. Esta fase publica apoyo `es` para los 9 cursos y apoyo `en` para el curso de español. La interfaz general (menús, botones) sigue en español; su traducción completa queda para una fase posterior.
Motivo: cada curso debe explicarse en un idioma que el alumno entienda.
Alternativas descartadas: (b) español solo para angloparlantes sin estructura multilingüe; (c) ocultar español como meta.
Archivos afectados: esquema de contenido (campos de texto localizados), cargador de rutas, pantalla de ruta. Ver ESQUEMA_CONTENIDO.md.
Riesgo: un nativo de un idioma sin textos de apoyo cae al respaldo en español. La interfaz de un angloparlante que estudia español seguirá mayormente en español hasta la fase de i18n.

## DEC-005 — Ruta nueva en paralelo; el contenido antiguo queda como banco

Fecha: 2026-09-26
Problema: reordenar los niveles 1–2 cambia los IDs `L<n>-NNN` y el progreso asociado; el cargador antiguo exige 20 unidades por nivel.
Decisión: el esquema 2 (`assets/contenido/<idioma>/ruta/`) convive con el antiguo. Los JSON `nivel-N.json`, las guías y la biblioteca no se modifican ni se borran; se migrarán nivel a nivel.
Motivo: no perder progreso ni romper pantallas publicadas.
Alternativas descartadas: reordenar y migrar IDs ahora.
Archivos afectados: `lib/core/aprendizaje/*`, `assets/contenido/*/ruta/*`.
Riesgo: dos modelos de progreso conviven hasta completar la migración.

## DEC-006 — Estados de unidad y criterio de dominio

Fecha: 2026-09-26
Problema: «completado» significaba solo participación; no existía «dominado».
Decisión: estados calculados desde `practicas`: bloqueada (visible, se puede leer) → disponible → en curso → practicada (guiada resuelta, desbloquea la siguiente) → aprobada (evaluación ≥ 80 % a la primera, en ese intento; no se revoca) → dominada (repaso acertado ≥ 1 día después de aprobar). Repaso espaciado tipo Leitner [1, 3, 7, 16, 35, 90] días; un fallo baja dos cajas y reprograma a 1 día.
Motivo: separar práctica con ayuda, comprobación y retención (auditorías C y D).
Alternativas descartadas: desbloquear solo con «dominada» (bloquearía un día entero).
Archivos afectados: `lib/core/aprendizaje/dominio.dart`, `providers.dart`.
Riesgo: umbrales (80 %, 1 día) son hipótesis; calibrar con un piloto. La evaluación reutiliza los mismos ítems al reintentar (banco de evaluación separado pendiente).

## DEC-007 — La ruta de fundamentos es el Nivel 0 en los 10 idiomas

Fecha: 2026-09-26 (decidido por el usuario)
Problema: un principiante de inglés nunca salía del nivel 0 (contaba 40 lecciones que no se pueden abrir).
Decisión: `fundamentosPendientes` termina al aprobar todas las unidades f0 del idioma (marca `ruta:<idioma>.f0:completa`) o, por compatibilidad, completando las lecciones antiguas del nivel 0. Esas lecciones quedan como «práctica extra» dentro de la ruta.
Motivo: una salida alcanzable y pedagógica del nivel 0.
Archivos afectados: `lib/core/state/providers.dart`, `lib/features/ruta/*`, `lib/features/course/levels_screen.dart`, `lib/shared/widgets/learning_path.dart`.
Riesgo: ninguno para usuarios existentes (la condición antigua sigue valiendo).

## DEC-008 — Destinos del home según idioma (solo navegación)

Fecha: 2026-09-26 (autorizado por el usuario)
Problema: «Aprende hoy» iba siempre a fundamentos de inglés; diagnóstico y biblioteca abrían siempre inglés.
Decisión: «Aprende hoy» → ruta de fundamentos si está pendiente; si no, Aprender (inglés) o la lección actual. Diagnóstico con el idioma meta. Biblioteca solo para inglés; en otros idiomas lleva a Aprender. No se cambió diseño, logo, iconos, imagen ni textos.
Archivos afectados: `lib/features/home/home_screen.dart` (10 líneas).
Riesgo: el diagnóstico de otros idiomas tiene las limitaciones documentadas en la auditoría C.

## DEC-009 — Corrección tolerante a tildes y a espacios en zh/ja

Fecha: 2026-09-26
Problema: exigir «não», «équatorienne» o pinyin con tonos frustra en teclados sin esas letras.
Decisión: una respuesta que solo difiere en tildes (y marcas de tono del pinyin) cuenta como correcta y muestra «Ojo con las tildes: …». En zh/ja se aceptan con y sin espacios. Las opciones se muestran barajadas.
Archivos afectados: `lib/core/aprendizaje/correccion.dart`, `lib/features/ruta/item_view.dart`.
Riesgo: pares donde la tilde cambia el sentido (avó/avô) se aceptan con aviso.

## DEC-010 — Publicar 9 idiomas como «Versión inicial» (REVISIÓN NATIVA PENDIENTE)

Fecha: 2026-09-26 (decidido por el usuario)
Problema: las rutas de es, fr, de, pt, it, zh, ja, ko, ru se redactaron sin revisión de hablantes nativos.
Decisión: se publican con `revision: "inicial"` y etiqueta visible «Versión inicial». Inglés: `revisada`.
Puntos concretos a revisar (informes de los autores): fr professeure, «Comment tu t'appelles ?», «Je viens de Quito»; it «sto a casa», «Prego» = «Dígame»; pt pronunciaciones de Río/SP, «estou com fome»; de «Ich bin kein Lehrer», pregunta V1; ru convención de transliteración (х = j, о átona = a); es «Encantado» como error, yeísmo; zh 不 con tono cambiado, frases cortas en la tienda de té; ja sin kanji en f0, おくに は どこ; ko romanización sin tensificación, 친구예요; en todos, pares mínimos que dependen del TTS (avó/avô, pala/palla, tonos, 달/탈/딸).
Riesgo: errores de naturalidad; ningún error de corrección gramatical conocido.

## DEC-011 — Unidades omitibles según el diagnóstico

Fecha: 2026-09-26
Problema: con prerrequisitos entre niveles, un alumno ubicado en A1 o A2 quedaría bloqueado por unidades de Fundamentos o A1 que no necesita.
Decisión: `nivelBase = fundamentos ? 0 : nivelInicial`. Las unidades con `nivelInterno < nivelBase` no aprobadas son «omitibles»: cuentan como prerrequisito cumplido, no se recomiendan y siguen disponibles. No se marcan como aprobadas ni dominadas (no hay evidencia).
Motivo: el prompt pide distinguir unidades dominadas, a estudiar y omitibles; esto aplica la ubicación sin inventar evidencia.
Alternativas descartadas: marcar como aprobadas las unidades inferiores (falsearía el dominio); ignorar prerrequisitos entre niveles.
Archivos afectados: `lib/core/aprendizaje/dominio.dart`, `providers.dart`, pantallas de ruta.
Riesgo: el diagnóstico actual no mide por unidad; una comprobación breve de prerrequisitos (auditoría C) sigue pendiente.

## DEC-012 — Pronunciación por idioma: idioma forzado en la voz y voz nativa para sílabas sueltas

Fecha: 2026-09-26 (reportado por el usuario: «あ» no sonaba japonés)
Problema: el backend recibía `idioma` pero no lo enviaba a ElevenLabs; la voz (Alice, inglesa) adivinaba el idioma. Prueba con Whisper: sin forzar, «Привет» y «Obrigada» se detectaron como inglés; con `language_code`, ruso y portugués. Además la caché no distinguía idioma («no» es/en compartían audio) y zh/ja se leían con los espacios del contenido.
Decisión: (1) `language_code` en modelos v2.5; (2) el idioma forma parte de la clave de caché, salvo inglés, que conserva su clave (su audio ya era correcto); (3) zh/ja sin espacios antes de sintetizar; (4) textos de 1–2 caracteres en ja/zh/ko/ru → voz del sistema del dispositivo con su locale; (5) la ruta usa `Voz.hablar`, que recurre a la voz del sistema sin sesión.
Archivos afectados: `backend/src/lib/voz.ts`, `backend/src/routes/voz.ts`, `backend/test/voz-idioma.test.ts`, `lib/core/voz.dart`, `lib/features/ruta/item_view.dart`.
Riesgo: el audio de idiomas distintos del inglés se regenera la primera vez (costo de caracteres). La voz del sistema depende de que el dispositivo tenga instalada la voz del idioma. Revisar voces nativas por idioma en ElevenLabs para la fase de avatares.

## DEC-013 — Sonidos y feedback visual orientados también a niños

Fecha: 2026-09-26 (pedido por el usuario; referencia Duolingo)
Decisión: efectos Kenney CC0 elegidos midiendo la forma de onda: acierto = confirmation_002 (ascendente y brillante), error = question_004 (descenso suave), completado = confirmation_001 + 002, nuevo `toque` = select_002 al elegir una opción. Opciones con pedestal (mismo lenguaje que `BotonPrincipal`), «pop» al acertar y sacudida suave al fallar, CONTINUAR verde tras acertar; todo respeta sonido/animaciones desactivados y movimiento reducido.
Archivos afectados: `assets/sfx/*`, `lib/core/efectos.dart`, `lib/features/ruta/opcion_respuesta.dart`, `item_view.dart`, `unidad_screen.dart`, `ruta_screen.dart`.
Riesgo: la elección se hizo por análisis de la señal, no de oído; validar escuchando en el dispositivo.

## DEC-014 — Un fallo en la práctica no bloquea: el ejercicio vuelve al final del bloque

Fecha: 2026-09-26 (reportado por el usuario: «al continuar se repite y no hay avance»)
Problema: en la práctica guiada, tras un error solo se ofrecía «Intentar otra vez»; quien no sabía la respuesta repetía el mismo ejercicio sin avanzar.
Decisión: tras responder siempre se puede continuar viendo la respuesta correcta; un ejercicio de práctica fallado se reinserta una vez al final de su bloque con la etiqueta «Otra vez» (patrón Duolingo). «Intentar otra vez ahora» queda como opción secundaria. La evaluación no repite (mide la primera respuesta).
Archivos afectados: `lib/features/ruta/unidad_screen.dart`, `item_view.dart`.
Riesgo: ninguno conocido; «practicada» sigue exigiendo resolver cada ejercicio guiado.

## DEC-015 — Paso «tabla» y escrituras completas por idioma

Fecha: 2026-09-26 (pedido por el usuario: en japonés solo había algunas kana)
Decisión: nuevo paso `tabla` (celdas meta con romanización, audibles) para escrituras y conjugaciones; las celdas cuentan como enseñadas. Fundamentos de cada idioma cubren la escritura/sonidos completos (ja kana completo, zh pinyin completo, ko hangul completo, ru 33 letras, alfabetos latinos) y cada idioma tiene un A1 «Primeras frases» con pronombres, verbos iniciales y tablas de conjugación.
Archivos afectados: esquema, validadores, `modelos.dart`, `tabla_ruta.dart`, contenido de los 10 idiomas.
Riesgo: las celdas de tabla amplían lo «enseñado» sin explicar cada palabra; audio de letras sueltas → voz del sistema (DEC-012).

## DEC-016 — Recompensa al completar

Fecha: 2026-09-26 (pedido por el usuario; referencia Duolingo)
Decisión: al aprobar una unidad o repaso, celebración con Lumo, confeti, fichas animadas (XP ganada, precisión, tiempo) y sonido «completado»; al completar un nivel, trofeo y fanfarria «nivel». Las lecciones antiguas usan la misma celebración (aciertos, precisión, racha). Respeta sonido/animaciones desactivados y movimiento reducido. En web se precarga la fuente de la escritura que se estudia para evitar cuadros vacíos.
Archivos afectados: `lib/features/ruta/celebracion.dart`, `unidad_screen.dart`, `lesson_result_screen.dart`, `efectos.dart`, `assets/sfx/nivel.wav`, `lib/main.dart`.
Riesgo: la XP mostrada es la ganada en la sesión (las repeticiones no suman XP).

## DEC-017 — Ruta base editorial, sin tutor IA obligatorio

Fecha: 2026-09-27 (decidido por el usuario)
Problema: el currículo maestro del cliente describe «práctica con IA», pero depender de generación en tiempo de ejecución impide controlar secuencia, respuestas, dificultad, coste y reproducibilidad.
Decisión: enseñanza, práctica, evaluación y repaso de la ruta base usan contenido editorial creado, revisado y versionado por OneLingo. El tutor IA queda como práctica opcional separada y nunca es requisito para completar una clase o nivel.
Motivo: asegurar calidad pedagógica, funcionamiento offline/degradado y medición comparable.
Alternativas descartadas: generar ejercicios o repasos en tiempo de ejecución; usar el tutor como paso obligatorio.
Archivos afectados: diseño en `METODOLOGIA_EDITORIAL_10X100.md` y `BIBLIOTECA_EJERCICIOS_V1.md`; implementación pendiente.
Riesgo: aumenta el volumen editorial y exige herramientas de autoría, validación y revisión lingüística.

## DEC-018 — Diez niveles de cien clases por idioma

Fecha: 2026-09-27 (decidido por el usuario)
Problema: el PDF del cliente fija 10 × 100, mientras la ruta actual contiene 109 clases de Nivel 1–10 entre los diez idiomas y cobertura desigual.
Decisión: cada idioma tendrá exactamente cien clases en cada nivel interno 1–10. Fundamentos (`f0`) se conserva como preparación adaptativa fuera de esas 1.000 clases. Se comparte el contrato y los resultados MCER, pero no se traduce la secuencia gramatical inglesa.
Motivo: cumplir la estructura comercial sin ignorar escritura, gramática, pronunciación y registro propios de cada idioma.
Alternativas descartadas: traducir 1.000 clases inglesas; contar F0 dentro de las cien del Nivel 1; poblar solo títulos.
Archivos afectados: `INVENTARIO_10X100_IDIOMAS.md`, `PLAN_NIVEL1_INGLES_100.md` y futuros manifiestos por idioma.
Riesgo: 10.000 clases requieren producción por lotes, QA automatizado y revisión lingüística; no deben publicarse de una sola vez.

## DEC-019 — Diagnóstico acotado y alfabetización no omitible

Fecha: 2026-09-27
Problema: un diagnóstico podía apuntar por encima del último nivel publicado y dejar la ruta sin recomendación. En zh/ja/ko/ru, el mismo nivel global podía volver opcionales unidades de escritura no demostradas.
Decisión: la recomendación se acota al mayor nivel con contenido editorial cargado. Las unidades F0 de `escritura` en zh, ja, ko y ru no son omitibles por nivel global; requieren evidencia específica. Los repasos vencidos o en refuerzo tienen prioridad sobre contenido nuevo.
Motivo: siempre debe existir un siguiente paso accionable y una habilidad oral no demuestra alfabetización.
Archivos afectados: `lib/core/aprendizaje/dominio.dart`, `providers.dart`, `test/simulacion_estudiantes_test.dart`, `test/ruta_dominio_test.dart`.
Riesgo: un alumno alfabetizado puede repetir contenido hasta que el diagnóstico por competencia se implemente; es preferible a omitir una escritura desconocida.

## DEC-020 — Adoptar la escala comercial del cliente

Fecha: 2026-09-27 (decidido por el usuario)
Problema: la escala histórica repartía A1, A2, B1 y B2 entre pares de niveles internos, mientras el currículo contratado define diez niveles comerciales con cien clases cada uno. El nuevo mapa inglés de N1 concentra A1 completo y por tanto no puede convivir sin versión con N1–N2 = A1.
Decisión: la nueva versión curricular usa N1 = A1; N2 = A2; N3 = entrada B1; N4 = consolidación B1; N5 = entrada B2; N6 = consolidación B2; N7 = B2 alto; N8 = entrada C1; N9 = C1 profesional/avanzado; N10 = dominio C1. Son bandas pedagógicas internas, no acreditaciones oficiales. C2 queda fuera de la promesa de los diez niveles hasta disponer de alcance y evaluación propios.
Migración: el progreso histórico conserva su escala y valor original. La equivalencia conservadora es legado 1–2 → cliente 1, 3–4 → 2, 5–6 → 3, 7–8 → 5 y 9–10 → 8. Los niveles intermedios superiores de cada banda se obtienen con evidencia nueva, no se conceden automáticamente.
Motivo: respetar la estructura del cliente, evitar duplicar A1 y mantener resultados honestos en los niveles avanzados.
Alternativas descartadas: conservar N1–N2 = A1; llamar C2 o «bilingüe» al Nivel 10 sin evidencia suficiente; sobrescribir el nivel histórico del usuario.
Archivos afectados: diagnóstico, serialización de progreso, manifiestos curriculares, rutas inglesas y pruebas de migración.
Riesgo: la interfaz antigua que interprete `nivelInicial` sin versión debe mantenerse sobre aliases hasta completar la migración.

## DEC-021 — Pulir las 290 clases publicadas antes de producir más
Fecha: 2026-09-30 · Responsable: Claude
Decisión: detener N3 C91–C100 y N4 hasta corregir lo publicado. La auditoría del 2026-09-30 mostró práctica sin enseñanza, situaciones y errores de relleno, fichas ya ordenadas y controles neutralizados por el compilador.
Motivo: producir 710 clases más con el mismo molde multiplicaría el defecto.
Archivos: `auditoria/AUDITORIA_2026-09-30.md`.

## DEC-022 — Capas editoriales sobre la fuente aprobada
Fecha: 2026-09-30 · Responsable: Claude
Decisión: las mejoras se aplican como capas revisables sobre los JSON editoriales, sin regenerar las clases: `enriquecimiento-*.json` (explicación, patrón, tabla, 2 errores reales, situación con diálogo e ítem propio, ejemplos corregidos), `correcciones-completar.json` (frase con hueco + traducción como pista + respuestas aceptadas) y `correcciones-items.json` (campos corregidos de ejercicios defectuosos y tercera opción). El compilador solo fusiona archivos con revisión independiente `GO` y que pasan la validación automática.
Motivo: trazabilidad por bloque, autor y revisor distintos, y reversibilidad (quitar la capa restaura la versión anterior).
Riesgo: dos fuentes para un mismo ítem; se mitiga con una sola función de fusión (`normalized_exercise`) común a biblioteca y ruta.

## DEC-023 — Producción abierta para escritura larga sin rúbrica
Fecha: 2026-09-30 · Responsable: Claude
Decisión: un «escribir» de más de 12 palabras sin `evidenceGroups` se marca `openProduction`: el alumno escribe dentro de un rango de palabras, compara con el modelo y el ítem no puntúa (216 variantes).
Motivo: sin IA en runtime, comparar un párrafo con una o dos soluciones exactas rechaza respuestas correctas y bloquea aprobaciones.
Alternativa futura: corrección por el tutor IA con rúbrica, cuando se conecte con la unidad.

## DEC-024 — Aprobación con redondeo hacia abajo
Fecha: 2026-09-30 · Responsable: Claude
Decisión: `aciertosNecesarios = floor(total × umbral)` (mínimo 1; con 1–2 ítems, todos). Con 0,8: 3/4 y 2/3 aprueban.
Motivo: con 4 ítems de evaluación, 0,8 exigía el 100 %.

## DEC-025 — Prueba de nivel v2 de inglés (adaptativa por habilidad)

Fecha: 2026-09-30. Acordado con el cliente: diagnóstico corto (~8 min) e inteligente, que sube la dificultad mientras el alumno acierta y se detiene al empezar a fallar; ubicación por habilidad (escucha, lectura, gramática, vocabulario; escritura omitible); «empiezo de cero» sin examen; sin micrófono ni IA en tiempo de ejecución.
Decisión: estimación bayesiana por habilidad sobre N0–N10 (prior centrado en la autodeclaración, otras habilidades con peso 0,4, pregunta en el nivel mediano, cierre con ±1 nivel al 85 % o 6 preguntas, parada temprana si P(N0) ≥ 85 %). Banco de 180 ítems (18 por nivel) con revisión independiente GO. Inicio = media redondeada hacia abajo, sin superar en 2 a la habilidad más débil; el alumno puede elegir un nivel arriba o abajo.
Evidencia: simulación (3.000 alumnos): 92 % de habilidades y 95 % de inicios a ±1 nivel, 1–2 % sobreubicación, ~18 preguntas; sin conocimientos: ~6,5 preguntas. Detalle: `DIAGNOSTICO_V2.md`. Los otros 9 idiomas mantienen el diagnóstico anterior.

## DEC-026 — Nadie elige su nivel; se sube demostrándolo
Fecha: 2026-10-01 · Acordado con el cliente («personas al azar quedaban en niveles altos»).
Decisión:
- El nivel elegido en el registro solo es el punto de partida; la prueba de ubicación decide en todos los idiomas (antes, fuera de inglés, el alumno se ubicaba a mano).
- El resultado permite empezar un nivel más abajo, nunca más arriba.
- La prueba antigua (idiomas sin v2) lleva un techo bayesiano con prior uniforme, el percentil 20 de lo que demuestran las respuestas. Además sigue preguntando hasta confirmar la estimación.
- Para subir: terminar las clases del nivel o aprobar la **prueba del nivel**: 20 preguntas de evaluación, una por tramo de 5 clases, al azar en cada intento, formatos autocorregibles y 16 aciertos para aprobar. Aprobada, el nivel cuenta como superado (`ruta:<idioma>.<nivel>:prueba`) y sus clases quedan abiertas para repasar.
- Ningún desplegable de nivel en pantallas del alumno.
Evidencia: con la prueba antigua, quien respondía al azar desde el nivel 8 terminaba de media en 4,8 (≥5 en el 56 %). Con el techo, `diagnostico_test` comprueba 120 recorridos al azar desde 4, 7 y 10, todos en ≤2. La prueba v2 al azar sale «desde cero» en el 69–99 % según la autodeclaración.

## DEC-027 — Limpieza de la generación antigua de pantallas (fase A)
Fecha: 2026-10-01 · Acordado con el cliente (flujo A → E: limpieza, prueba de nivel, situaciones por tramo, léxico único, francés).
Decisión:
- Se retiran la biblioteca de práctica antigua (`library_screen`, banco por habilidad con selector de nivel), `LearningPath`, `LearningPrimer` y `foundations_screen`.
- «Biblioteca» pasa a ser consulta y práctica libre del nivel del alumno: Lecturas, Escuchas, Guías de gramática y Mapa de sonidos.
- Toda pantalla de ejercicios usa `BotonPrincipal` fijo, `OpcionRespuesta` y `FeedbackDock`, y no muestra jerga interna.
- `test/arquitectura_test.dart` vigila estas reglas.
Referencia: `docs/ARQUITECTURA_VIGENTE.md`.

## DEC-028 — Situaciones v2: las mismas 50 en tres tramos
Fecha: 2026-10-01 · Acordado con el cliente («vocabulario por nivel y vinculado a las situaciones»).
Decisión:
- Cada situación tiene **tres tramos**: Básico (N1–3), Intermedio (N4–6) y Avanzado (N7–10). Cada uno con 3 objetivos, 10 palabras con ejemplo, 4 frases útiles y una prueba de 10 preguntas (80 % para aprobar).
- El tramo sale del nivel del alumno (`nivelAlumnoProvider`). Los inferiores quedan abiertos y los superiores, bloqueados.
- **Completado** = prueba aprobada + al menos un objetivo practicado con el tutor.
- Cada objetivo se practica por chat o en videollamada (Lumo), ya situado en su tema y objetivo.
- Fuente única con copias generadas; inglés general americano.
- Los objetivos del básico conservan sus ids (`s<id>-o1..o3`). Los nuevos son `s<id>-i*` y `s<id>-a*`.
Motivo: antes la situación era igual en N1 y en N10, no tenía progreso, la prueba no terminaba y la lista existía en cuatro copias a mano.

## DEC-029 — Léxico único, «Mis palabras» y «Mis verbos»
Fecha: 2026-10-01 · Acordado con el cliente (fase D; «Mis verbos» confirmado).
Decisión:
- **El léxico es un índice calculado**, no otra fuente. Reúne las palabras que enseñan la ruta (pasos de vocabulario), las situaciones (por tramo) y el Nivel 0. La clave es la palabra normalizada; para cada una se guardan su nivel mínimo y sus orígenes.
- **«Mis palabras»** son las de las clases practicadas, los tramos de situación empezados y las lecciones del Nivel 0 completas. Se calculan; no se guardan.
- **El repaso es por palabra**, en cajas con intervalos de 1, 3, 7, 16, 35 y 90 días. Un fallo devuelve la palabra a la caja 0 y la repasa mañana. Solo se guardan `[caja, fecha]` por palabra en `lexico:<idioma>`.
- **Una sesión de repaso** tiene 10 palabras: primero las vencidas y luego las nuevas. Las formas se alternan (significado, cómo se dice y escucha), y las falladas vuelven al final.
- **«Mis verbos»** sale de una fuente revisada de 174 verbos (108 irregulares), de la que se generan las tablas: presente, pasado, futuro con will, presente perfecto y presente continuo, con audio.
  - El nivel de cada verbo se toma de la ruta.
  - La práctica usa 10 preguntas, sobre todo irregulares, con errores típicos como distractores (goed, went/gone, falta de -s).
  - El esquema sirve para francés, que tendrá personas y tiempos propios.

## DEC-030 — Francés: voces nativas y Nivel 0 de lectura
Fecha: 2026-10-01 · Acordado con el cliente (francés de Francia, Hélène y Nicolas).
Decisión:
- **Voces nativas:** los roles neutros usan la voz nativa del idioma (`NATIVAS`): en francés, Hélène narra y Nicolas dialoga.
- **Nivel 0 multilingüe:** el contenido trae su idioma, voz y textos de interfaz (`idiomasConNivel0`).
- **Francés F1–F5 (20 lecciones):**
  - el mapa de sonidos tiene 15 sonidos de vocal con imagen y color;
  - la marca `‿` sirve para el enlace;
  - autoría en dos lotes y revisión independiente GO con 24 correcciones.
- **El registro y Aprender** recomiendan el Nivel 0 a quien empieza de cero también en francés.
- **Versión inicial:** el contenido se publica con revisión independiente por IA; queda pendiente la de un nativo.

## DEC-031 — Interfaz multilingüe con el español como clave
Fecha: 2026-10-01 · Acordado con el cliente: la app también es para nativos de inglés (y otros), sin reescribir todo, y la interfaz se elige en Perfil.
Decisión:
- **Clave en español:** `tr('texto en español')` con diccionarios `assets/i18n/<idioma>.json`. Si falta una traducción se ve el español.
- **Herramientas:** `tools/i18n/extraer.py` comprueba que nada quede sin traducir, y `arquitectura_test` impide textos visibles sin `tr()`.
- **Idioma de la interfaz:** el elegido en Perfil o, si no hay elección, el nativo, y si no está disponible, inglés. La primera visita usa el idioma del dispositivo.
- **Textos de apoyo del contenido:** siguen el idioma de la interfaz.
- **Alternativa descartada:** las ARB de Flutter. Obligaban a inventar unas 940 claves y a reescribir cada llamada.

## DEC-032 — Contenido bilingüe e idioma de la app en el registro
Fecha: 2026-10-01 · Acordado con el cliente («al registrarse, que puedan elegir el idioma de la interfaz»).
Decisión:
- **Textos de apoyo:** cualquiera puede ser `{"es": …, "en": …}`. `localizarApoyo` lo resuelve al idioma de la interfaz al cargar (Nivel 0, situaciones…); la ruta ya usaba `TextoApoyo`.
- **Contenido nuevo:** nace bilingüe. `validar_nivel0.py --bilingue` y `nivel0_test` lo exigen en francés.
- **Francés hecho bilingüe:** Nivel 0 F1–F10 (40 lecciones) y la ruta f0 + a1-1 (2.233 textos), con revisión independiente GO.
- **Selector de idioma de la app:** en la bienvenida, en el paso del idioma nativo y en Perfil. Al cambiarlo se conserva el borrador del registro.
