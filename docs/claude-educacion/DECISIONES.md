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
