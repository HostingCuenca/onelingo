# Auditoría 2026-09-30 — Inglés N1–N3 publicado (290 clases)

Responsable: Claude (coordinador) con dos auditores independientes (pedagogía; código y pruebas). Base: release `20260930-edu-5-n2-n3-review`, checkpoint `d50723d`.

## Veredicto

La producción masiva de N1–N3 tiene buena cobertura del temario y progresión de longitud, pero la experiencia del alumno era **práctica sin enseñanza**. Los controles automáticos pasaban porque el compilador neutralizaba sus reglas. Se decide **pulir las 290 clases antes de producir N3 C91–C100 y N4**.

## Hallazgos y estado

| # | Sev. | Hallazgo | Estado |
|---|---|---|---|
| 1 | P0 | «Ordenar»: las fichas llegaban en el orden de la respuesta (484 ítems) | Corregido `d31dce7`: se desordenan y nunca coinciden con la respuesta |
| 2 | P0 | Contracciones rechazadas («I'm» ≠ «I am», 76/86 ítems) | Corregido `d31dce7`: equivalencia en inglés, también en multiparte |
| 3 | P1 | Umbral 0,8 con 4 ítems exigía el 100 % | Corregido: se redondea hacia abajo (3/4, 2/3 aprueban) |
| 4 | P1 | Repaso fallido se volvía a recomendar en el acto (bucle) | Corregido: vence al día siguiente |
| 5 | P1 | «Escucha y ordena/completa» sin botón de audio (8 ítems) | Corregido |
| 6 | P1 | El diagnóstico guardaba el nivel recomendado, no el elegido; sobrescribía `escala` | Corregido |
| 7 | P0 | Gramática sin explicar: explicación = objetivo en una línea | Corregido: 290/290 clases con explicación y patrón (GO independiente) |
| 8 | P1 | Situación falsa en 290 clases (contexto genérico + copia de práctica) | Corregido: 290 situaciones con diálogo e ítem propio |
| 9 | P1 | `erroresFrecuentes` falsos («frase + ?») | Corregido: 580 errores reales |
| 10 | P0/P1 | 161 ejemplos de enseñanza son metalenguaje en inglés; notas en inglés; traducciones-resumen | Corregido en el enriquecimiento |
| 11 | P1 | Escritura larga corregida por coincidencia exacta (159 respuestas > 12 palabras, 3 con rúbrica) | Corregido: producción abierta no puntuable (216 variantes, DEC-023) |
| 12 | P1 | 345/401 ítems de elegir de N1 con 2 opciones | Corregido: tercera opción en 429 ítems de N1–N2 |
| 13 | P1 | Respuesta visible en consigna/pista (91 ítems); pistas genéricas repetidas | Corregido en correcciones-items / pistas |
| 14 | P0 | N1 C86–88: 15 «completar» sin frase inglesa; opciones con errores | Corregido (pistas + correcciones de ítems) |
| 15 | P1 | Vocabulario inflado con «expresión del curso» (81–89 %): anula el control «nada sin enseñar» | Pendiente: separar léxico de validación del vocabulario enseñado |
| 16 | P2 | 12,4 MB de JSON sin compresión en el servidor | Parcial: JSON compactos (7,3 MB). Falta activar `DEFLATE` para `application/json` (config del servidor, requiere aprobación) |
| 17 | P2 | Hash de selección distinto en web (precisión > 2^53) | Corregido |
| 18 | P2 | Niveles mostraban MCER de la escala antigua | Corregido |
| 19 | P1 | Progreso A1 antiguo (`en.a1.*`) sin equivalencia en N1 | Mitigado: enlace al nivel nuevo; solo afecta a usuarios de prueba |
| 20 | P2 | Temas de N2–N3 dominados por oficina/trámites; sin imágenes en N2–N3; sin personajes fijos | Situaciones del enriquecimiento cotidianas y aptas para niños; resto pendiente |
| 21 | P2 | Cobertura: N1 sin was/were ni going to; N3 sin used to, modales de deducción, question tags | Pendiente: mapas v2 y N3 C91–C100 / N4 |

## Métricas de referencia

- Formatos N1: 394 elegir, 277 completar, 270 ordenar, 91 escuchar, 35 escribir, 33 relacionar.
- Palabras por ejemplo: N1 4,8 · N2 9,0 · N3 12,4.
- Pruebas tras la fase 1: 174 Flutter, 1 omitida; 61 de herramientas; 10 idiomas sin errores.

## Actualización (cierre de la fase de pulido)

- 668 «completar» sin pista recibieron traducción completa como guía y respuestas aceptadas (`correcciones-completar.json`, GO por nivel).
- ~200 ejercicios del registro `EJERCICIOS_DEFECTUOSOS.md` y 429 ítems de dos opciones corregidos (`correcciones-items.json`, GO por nivel).
- Queda pendiente: #15 (vocabulario inflado: el control «nada sin enseñar» sigue siendo laxo; las pistas destaparon 57 palabras no enseñadas en N2–N3), #16 (gzip en el servidor), #20 (imágenes y personajes fijos), #21 (cobertura MCER).
