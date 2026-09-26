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
