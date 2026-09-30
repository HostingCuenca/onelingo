# Estado actual

Última actualización: 2026-09-30
Responsable: Codex
Rama o worktree: `claude/educacion-multilenguaje` en `/home/roggrt/Documents/onelingo` (sin worktree)
Fase actual: Inglés N1 y N2 completos y N3 C1–C90 publicados; N3 C91–C100 pendiente de autoría.
Porcentaje aproximado: Fundamentos en 10 idiomas · Inglés 290/1.000 clases editoriales integradas y activas · programa inglés total 29 %

## Trabajando ahora

- Continuar Inglés N3 desde C91 en bloques de cinco bajo `editorial-agent.v2`, con autoría y revisión independiente en paralelo. No ampliar el runtime de 290 a 300 hasta obtener GO longitudinal.
- Cola y protocolo de continuidad: `docs/claude-educacion/ENGLISH_EDITORIAL_PIPELINE.md`.

## Terminado recientemente

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

1. Recoger revisión del cliente sobre N2 y N3 C1–C90 ya publicados.
2. Completar Inglés N3 C91–C100 por bloques de cinco con validación longitudinal y revisión independiente; después crear el mapa v2 de N4.
3. Antes de cualquier release nueva, ejecutar el runbook desde un árbol controlado, con lock, backup, salud, consola y recorrido real.

## Bloqueos

- Revisión nativa de 9 idiomas (decisión humana).

## Producción

- Versión desplegada: `20260930-edu-5-n2-n3-review` · `main.dart.js` `72e25f36798f5810…`; backend sin cambios desde `edu-2`.
- Fecha: 2026-09-30 13:53 UTC
- URL: https://onelingo.hostingcuenca.com
- Estado de salud: `/api/salud` OK; `onelingo-api` online.
- Respaldo: `/var/www/onelingo/backups/20260930-edu-5-n2-n3-review/web-anterior`
- Rollback: ver `DESPLIEGUES.md`; restauración web completa, sin reinicio de backend.
