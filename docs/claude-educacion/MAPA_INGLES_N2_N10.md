# Mapa editorial de inglés N1–N10

Estado: **planificado**. Este documento y sus JSON son una fuente editorial estática de respaldo; no activan contenido y no declaran clases publicables.

Actualización 2026-09-30: N2 tiene un mapa de autoridad editorial v2 en `assets/contenido/en/plan-editorial/mapa-n2-editorial-v2.json` y sus C1–C100 están redactadas en `assets/contenido/en/editorial/n2/`: 100 clases y 1.300 ejercicios en `shadow`. N3 tiene su mapa de autoridad en `assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json`; C1–C90 ya están integradas en `shadow` y C91 en adelante se producen por bloques con revisión independiente. Ambos mapas usan ciclos `input → form → comprehension → production → transfer`. Los mapas originales se conservan como trazabilidad del PDF, no como autoridad de producción para N2/N3.

La escala adoptada es la del cliente: N1 contiene A1 completo. Continúa con N2=A2, N3=B1 entrada, N4=B1 consolidado, N5=B2 entrada, N6=B2 consolidado, N7=B2 alto, N8=C1 entrada, N9=C1 profesional y N10=C1 avanzado. Cada nivel contiene 100 clases organizadas en 20 bloques de 5 (1.000 clases / 200 bloques en total).

## Archivos

- `assets/contenido/en/plan-editorial/mapa-ingles-n1-n10.json`: índice completo de 1.000 clases.
- `assets/contenido/en/plan-editorial/mapa-n1.json`: N1 derivado del mapa editorial corregido.
- `assets/contenido/en/plan-editorial/mapa-ingles-n2-n10.json`: índice de respaldo de las 900 clases N2-N10.
- `assets/contenido/en/plan-editorial/mapa-n2.json` … `mapa-n10.json`: respaldo por nivel.
- `assets/contenido/en/plan-editorial/mapa-n2-editorial-v2.json`: autoridad editorial vigente de N2.
- `assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json`: autoridad editorial vigente de N3.

Cada clase usa un ID estable `en.nX.lYYY`, título y tema derivados del currículo fuente, resultado fuente, tratamiento editorial, skills, prerrequisitos y estado `planificado`. Los prerrequisitos encadenan las clases dentro del nivel y conectan el primer bloque con el cierre del nivel anterior, evitando solapamientos de escala.

## Límites

El mapa no redacta ejercicios, textos, audio, bancos de ítems ni criterios de publicación. Antes de cualquier activación se requiere revisión pedagógica, producción de contenido, QA lingüístico, accesibilidad y validación de la ruta.
