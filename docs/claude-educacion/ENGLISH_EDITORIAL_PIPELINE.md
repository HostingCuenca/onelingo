# Cadena continua de producción editorial — Inglés

Actualizado: 2026-09-30

## Objetivo

Completar Inglés N1–N10, 100 clases por nivel, sin depender del tutor ni de generación IA en runtime. El trabajo se realiza en bloques de cinco clases y mantiene separadas autoría, auditoría, corrección e integración.

## Estado de la cola

| Alcance | Estado | Siguiente puerta |
| --- | --- | --- |
| N1 C1–C100 | `active`, producción | mantenimiento |
| N2 C1–C100 | fuente editorial `shadow`; runtime `active`, producción | revisión del cliente |
| N3 C1–C90 | fuente editorial `shadow`; runtime `active`, producción | revisión del cliente |
| Enriquecimiento N1–N3 (290 clases) | completo: 290/290 GO; pistas de completar y correcciones de ítems GO | despliegue `edu-6-pulido` |
| N3 C91–C100 | pendiente, después del enriquecimiento | autoría con el contrato enriquecido |
| N4–N10 | NO-GO para autoría | mapa v2 propio antes de autoría |

## Flujo obligatorio por bloque

1. **Autoría:** un agente genera cinco clases, 65 ejercicios, bundle, informe y manifiesto reproducible solo en `work/`.
2. **Validación mecánica:** el autor ejecuta el validador del bundle, pruebas focalizadas e idempotencia. El resultado sigue siendo DRAFT.
3. **Auditoría independiente:** otro agente revisa mapa, progresión, originalidad, distractores, remediaciones, variantes, metadatos y escenarios de transferencia. Solo este rol emite `GO` o `REVISE`.
4. **Corrección:** ante `REVISE`, el autor corrige exactamente los hallazgos y regenera; no se rebaja ningún requisito para obtener aprobación.
5. **Integración:** tras `GO`, se promueve el generador reproducible y sus cinco clases a `assets/contenido/en/editorial/`; se amplían pruebas longitudinales y se registra el hito.
6. **Continuidad:** mientras un bloque se audita, los autores trabajan en los dos bloques siguientes. Ningún agente aprueba su propio contenido.

## Contrato de calidad

- Fuente curricular: mapa editorial v2 del nivel correspondiente.
- Ciclo fijo por bloque: `input → form → comprehension → production → transfer`.
- 13 ejercicios por clase: guiada, práctica, evaluación y repaso separados.
- `status: shadow`, `runtimeAi: false`, selección y remediación deterministas.
- Enseñar antes de evaluar; no copiar evidencia ni respuestas entre enseñanza, evaluación y repaso.
- Cierre cada cinco clases con evidencia acumulativa y tres escenarios realmente distintos.
- Registrar `variantId`, `libraryVersion` y `selectionId` en cada intento.
- La activación de runtime es una decisión explícita separada del `status` editorial. La release `20260930-edu-5-n2-n3-review` activó N2 completo y N3 C1–C90 para revisión del cliente; no ampliar este corte por el solo hecho de integrar nuevos JSON.

## Protocolo de reanudación

Al retomar el trabajo, leer primero este archivo y `PROGRESO.md`, comprobar la fila más avanzada y reanudar el primer bloque que no tenga `GO`. No volver a generar bloques integrados ni ampliar producción como parte automática de la población editorial. El enriquecimiento de las 290 clases está completo. El primer lote pendiente es N3 C91–C95, que debe incluir desde la autoría la capa del CONTRATO_ENRIQUECIMIENTO.md.

Validaciones mínimas antes de cerrar un hito:

```bash
python3 tools/contenido/validar_bundle_editorial.py --file <bundle> --start <inicio> --end <fin> --level <nivel>
python3 -m unittest discover -s test_tools -p 'test_*.py'
python3 tools/validar_ruta.py
```
