# Estado actual

Última actualización: 2026-10-01
Responsable: Claude (Claude Code)
Rama o worktree: `claude/educacion-multilenguaje` en `/home/roggrt/Documents/onelingo` (sin worktree)
Fase actual: **Inglés N1–N10 completo y publicado (1.000 clases)**; siguiente fase: revisión del cliente y calidad C1.
Porcentaje aproximado: Fundamentos en 10 idiomas · Inglés 1.000/1.000 clases editoriales integradas y activas · programa inglés total 100 %

## Trabajando ahora

- Hoja de ruta acordada el 2026-10-01: A limpieza → B ubicación y prueba de nivel → C situaciones por tramo → D léxico único y «Mis palabras» → E francés (`docs/ARQUITECTURA_VIGENTE.md`, sección 6).
- **E, francés (en curso):** ver la hoja de ruta FR-1…FR-8 en `PLAN_FRANCES.md` §9. FR-1 y FR-2 hechos y bilingües; siguen FR-3 (verbos), FR-4 (situaciones) y FR-5 (N1).

## Terminado recientemente

- **I2 y francés FR-1/FR-2 (2026-10-01, DEC-032):**
  - Contenido bilingüe con `localizarApoyo`.
  - Nivel 0 francés F1–F10 completo (40 lecciones, bilingüe, revisión GO con 67 correcciones).
  - Ruta francesa f0 + a1-1 con inglés (revisión GO).
  - Selector de idioma de la app en la bienvenida, el registro y Perfil.

- **I1, interfaz en inglés (2026-10-01, DEC-031):**
  - 939 textos con `tr()` en unos 70 archivos (6 agentes por grupos de archivos).
  - `en.json` traducido y revisado (GO, 44 correcciones).
  - Selector de idioma en Perfil; primera visita en el idioma del dispositivo.
  - Reglas vigiladas por pruebas.

- **Fase E, primera entrega de francés (2026-10-01, DEC-030):**
  - Voces Hélène y Nicolas.
  - Nivel 0 multilingüe: el contenido trae su idioma, voz y textos.
  - Francés F1–F5: 20 lecciones, mapa de 15 sonidos y 70 emoji Noto nuevos.
  - Validador `validar_nivel0.py` y descargador de emoji.

- **Fase D, léxico (2026-10-01, DEC-029):**
  - Índice único de más de 4.000 palabras calculado desde ruta, situaciones y Nivel 0.
  - «Mis palabras» con repaso espaciado por palabra, agrupadas por nivel o situación, con búsqueda.
  - «Mis verbos»: 174 verbos con 5 tablas y audio, más práctica de irregulares.
  - Perfil cuenta Mis palabras. Biblioteca enlaza ambas pantallas.

- **Fase C, situaciones v2 (2026-10-01, DEC-028):**
  - Las 50 situaciones × 3 tramos: 450 objetivos, 1.500 palabras y 600 frases, con autoría y revisión independiente GO por lote.
  - Pantalla nueva con selector de tramo, avance, objetivos (chat y videollamada), palabras, frases y la prueba de 10 preguntas.
  - Las tarjetas de Practicar muestran el avance.
  - Fuente única con generador; el servidor responde con el tramo del alumno.

- **Fases A y B (2026-10-01, DEC-026/027):**
  - Estética unificada: tema para `FilledButton`; `BotonPrincipal` fijo, `OpcionRespuesta` y `FeedbackDock` en lecturas, escuchas, gramática, lecciones, examen y prueba antigua.
  - Retirados la biblioteca de práctica antigua, LearningPath, LearningPrimer y foundations. La Biblioteca nueva tiene Lecturas, Escuchas, Guías y Mapa de sonidos.
  - Sin selectores de nivel ni jerga.
  - Ubicación a prueba de azar: techo bayesiano en la prueba antigua, prueba obligatoria en el registro de todos los idiomas y sin opción N+1.
  - Prueba para subir de nivel (20 preguntas, 16 para aprobar) y niveles con estado en Aprender.
  - Documentación consolidada: `ARQUITECTURA_VIGENTE.md`, nuevo `AGENTS.md` y `docs/archivo/`. Reglas vigiladas por `test/arquitectura_test.dart`. 213 pruebas Flutter.

- **Inglés N3 C91 → N10 C100 (2026-09-30):** 710 clases por autoría compacta (`CONTRATO_AUTORIA_COMPACTA.md`, `construir_bloque.py`), mapas v2 N4–N10 validados, cada bloque con autor y revisor independientes (GO). Releases edu-7 (N3–N4), edu-8 (N5–N6), edu-9 (N7–N9) y edu-10 (N10). Los revisores corrigieron claves erróneas (P0) en N9 C33/C35/C38/C40, fugas de respuesta, rúbricas laxas y español peninsular. P2 abierto: dificultad léxica de N8–N10 algo baja para C1 (el control «nada sin enseñar» limita el léxico); modelos de escritura larga al 55–75 % del rango del mapa.

- **Pulido de contenido N1–N3 (2026-09-30):** 290/290 clases enriquecidas (explicación en español, patrón, tabla, 2 errores reales, situación con diálogo e ítem propio, ejemplos reales); 668 «completar» con pista de traducción; ~200 ejercicios defectuosos y 429 ítems de dos opciones corregidos. Todo con autor y revisor independientes (`GO`) y validación automática obligatoria en el compilador. Biblioteca `2026.09.30-en-pulido.1`. 176 pruebas Flutter, 61 de herramientas, 10 idiomas sin errores.

- Pulido de la app (2026-09-30, local, sin desplegar): fichas de ordenar desordenadas, contracciones aceptadas, umbral redondeado (3/4), repaso sin bucle, audio en escucha-ordenar/completar, nivel elegido en el diagnóstico, MCER por nivel, hash web, JSON compactos (12,4 → 7,3 MB), escritura larga sin rúbrica como producción abierta (216 ítems), situación con diálogo visible. Commits `d31dce7`…`5f8ce57`. 175 pruebas Flutter, 61 de herramientas, 10 idiomas sin errores.

- Inglés N1 editorial completo y conectado localmente: 100 clases, 1.300 ejercicios, cronología 1–100 válida, manifiesto `active`, repaso aislado y selección trazable. 155 pruebas Flutter pasan, 1 omitida; 40 pruebas de herramientas pasan; 10 idiomas con 0 errores de ruta. Build web local verificado; sin despliegue. 2026-09-28.
- Inglés N2: mapa editorial v2 de 100 clases congelado; C1–C15 redactadas con 195 ejercicios, 75 piezas de enseñanza, 134 entradas de vocabulario y cierres acumulativos C5/C10/C15. Validación individual 15/15, tres bundles correctos y 47 pruebas de herramientas. Permanece en `shadow`, sin alterar el runtime. 2026-09-29.
- Inglés N2 C16–C30: 15 clases, 195 ejercicios, 75 piezas de enseñanza y 117 entradas de vocabulario observable. Primer lote bajo `editorial-agent.v2`; los tres bloques fueron corregidos tras revisión independiente y recibieron `GO`. Validación longitudinal C1–C30: 390 ejercicios; 51 pruebas de herramientas; 10 idiomas con 0 errores. Permanece en `shadow`, sin alterar el runtime. 2026-09-29.
- Inglés N2 C31–C45: 15 clases, 195 ejercicios, 63 piezas de enseñanza y 90 entradas de vocabulario. Los tres bloques recibieron `REVISE/REJECT`, fueron corregidos y cerraron en `GO` independiente. Validación longitudinal C1–C45: 585 ejercicios; 52 pruebas de herramientas; 10 idiomas con 0 errores. El validador rechaza ahora variantes de escritura que solo cambian puntuación. Permanece en `shadow`, sin alterar el runtime. 2026-09-29.
- Inglés N2 C46–C100: 55 clases y 715 ejercicios producidos por bloques, corregidos tras revisión independiente e integrados en `shadow`. Validación longitudinal N2 C1–C100: 100 clases y 1.300 ejercicios; 57 pruebas de herramientas; 10 idiomas con 0 errores de ruta. N2 queda editorialmente completo sin activar el runtime. 2026-09-29.
- Inglés N3: mapa editorial v2 completo de 100 clases y 20 ciclos validado; C1–C90 integradas con 1.170 ejercicios y GO independiente. C81–C85 añadió rúbricas locales por rango y evidencia para aceptar paráfrasis controladas sin IA; C86–C90 reforzó umbrales reales, pasiva-condicional y acuerdos comunitarios medibles. C91–C100 está pendiente de autoría; no hay artefactos integrados. 2026-09-30.
- Release web `20260929-edu-4-n1-runtime` publicada y verificada: N1 100 clases/1.300 ejercicios, vocabulario visible saneado, APK/avatar/backend preservados. 2026-09-29.
- Release web `20260930-edu-5-n2-n3-review` publicada y verificada: N1 C1–C100, N2 C1–C100 y N3 C1–C90 activos, 290 clases/3.770 ejercicios; rutas de 10 idiomas sin errores, 61 pruebas Python, 169 Flutter pasan y 1 omitida. N3 C91–C100 queda expresamente fuera. Backend, `.env`, APK y avatar preservados. 2026-09-30.
- Escrituras/sonidos completos y A1 «Primeras frases» en 10 idiomas (204 unidades), paso `tabla` (DEC-015). 2026-09-26.
- Fallo en práctica ya no bloquea: repetición al final del bloque (DEC-014). 2026-09-26.
- Celebración al completar unidad/nivel y precarga de fuentes CJK en web (DEC-016). 2026-09-26.

- A1 de inglés: 29 unidades en 3 módulos (plan en PLAN_A1_INGLES.md), rutas por nivel, unidades omitibles según diagnóstico. 2026-09-26.
- Pronunciación por idioma corregida (DEC-012) y sonidos/feedback visual al estilo de la app (DEC-013). 2026-09-26.
- Release `20260926-edu-2-a1-voz` en producción. 2026-09-26.

- Auditoría con 4 agentes (A currículo, B vocabulario/situaciones, C habilidades/evaluación, D arquitectura/recorridos): `auditoria/`. 2026-09-26.
- Núcleo `lib/core/aprendizaje/` (esquema 2, estados, repaso, migración) y pantallas `lib/features/ruta/`. Pruebas `test/ruta_*`. 2026-09-26.
- Ruta f0 de 6 unidades en en, es, fr, de, pt, it, zh, ja, ko, ru (60 unidades, 75–93 vocablos y 72–93 ítems por idioma). 2026-09-26.
- Gramática inglesa: reanuda tema, marca practicados, guarda borradores. 2026-09-26.
- Release `20260926-edu-1-fundamentos` en producción. 2026-09-26.

## Siguiente paso

1. Recoger revisión del cliente sobre N1–N10 publicados.
2. Recoger datos reales de la prueba de nivel v2 para recalibrar umbrales (eventos `diagnostico` versión 4).
3. Auditoría #15 (léxico de validación separado del vocabulario enseñado), imágenes y personajes fijos (#20).

## Bloqueos

- Revisión nativa de 9 idiomas (decisión humana).

## Producción

- Versión desplegada: `20261001-edu-25-nivel0` · `main.dart.js` `3985f80e…` (Nivel 0 inglés, unidades 1–3); backend con `/chat/voz` y `/ejercicios/revisar`; backend: 5 archivos del tutor (`ia.ts`, `ia_openai.ts`, `situaciones.ts`, `voz.ts`, `routes/chat.ts`); Apache con compresión y caché (vhost de OneLingo).
- Fecha: 2026-10-01
- URL: https://onelingo.hostingcuenca.com
- Estado de salud: `/api/salud` OK.
- Respaldo: `/var/www/onelingo/backups/20261001-edu-20-tutores-v2/` (`web-anterior`, `backend-src`, `apache-onelingo-le-ssl.conf`).
- Rollback: ver `DESPLIEGUES.md` (web, backend con `pm2 restart` y vhost con `reload`).
