# QA incremental de inglés N1, clases 1–10

Fecha: 2026-09-27. Estado: **apto como patrón editorial; no activado**.

## Resultado estable

- Artefacto: `assets/contenido/en/editorial/n1/pilot-classes-01-05.json`.
- SHA-256 del archivo validado: `66db0bd7d7ad0bb764552719faac262709499dfa99271e95799c70e1b9089206`.
- Cobertura: 5 clases, 65 ejercicios; por clase, 3 guiados, 3 de práctica, 4 de evaluación y 3 de repaso.
- Escala: `client-10-levels-v1`; estado `shadow`; `runtimeAi: false`.
- Enseñanza autocontenida, prerrequisitos de clase, feedback en todos los pools, pistas solo en práctica guiada, accesibilidad, recuperación por error, evidencia de reingreso y evaluación acumulativa en la clase 5.
- La activación permanece vacía: ninguna clase nueva sustituye la ruta publicada.

## Validaciones

- `python3 tools/contenido/pilot_validate_en_n1.py`: correcto.
- Generador de refuerzo ejecutado dos veces con el mismo SHA-256: idempotente.
- Revisión adversarial de respuestas, conceptos y prerrequisitos: sin bloqueantes.
- Simulación de principiante absoluto, carga alta, fallo total, acierto total y reingreso: `GO` para redactar los siguientes lotes.
- El `remediationMap` comparte el tercer ítem de repaso para dos fallos de la clase 5; es una mejora futura no bloqueante.

## Intentos paralelos posteriores

- Clases 6–9: se redactaron una por una, con corrección inmediata tras cada revisión técnica y simulación estudiantil. Quedaron integradas individualmente en `shadow`; no están activas.
- Clase 10: cierre acumulativo del bloque 6–10. Pasó doble revisión independiente, los validadores estructural y cronológico y la simulación longitudinal. SHA-256 `cf1e9f04527ae1e727553f255601d0b0edf546e1b97ae7b3a9aee09df9e1d14b`.
- Resultado longitudinal 1–10: 10 clases y 130 ejercicios válidos. La suite focalizada del contrato editorial y cronología ejecutó 16 pruebas, todas correctas.
- Resultado longitudinal 1–15: 15 clases y 195 ejercicios válidos. La suite focalizada aumentó a 24 pruebas y añadió detección de evidencia repetida entre formatos, manteniendo reciclaje legítimo entre clases.
- Resultado longitudinal 1–17: 17 clases y 221 ejercicios válidos. C16 y C17 pasaron correcciones iterativas, revisión técnica y simulación estudiantil. La suite focalizada suma 28 pruebas e incorpora el modo opt-in `vocabularyDeclarations: exhaustive` para detectar vocabulario usado pero no declarado y declaraciones ociosas.
- Resultado longitudinal 1–18: 18 clases y 234 ejercicios válidos. C18 conserva sus prerrequisitos originales y añade únicamente los patrones de apoyo usados. El modo exhaustivo acepta ahora declaraciones compuestas como `have got` sin forzar `got` como palabra independiente; la suite suma 30 pruebas.
- Resultado longitudinal 1–20: 20 clases y 260 ejercicios válidos. C19 enseña `have got/has got` con artículos y concordancia; C20 cierra acumulativamente posesivos adjetivales, `'s`, posesión y familia/rasgos. C6, C9 y C10 recibieron saneamiento cronológico y estudiantil; C1–C5 continúa NO-GO hasta corregir sus remediaciones y secuencia.
- Resultado longitudinal 1–21: 21 clases y 273 ejercicios válidos. C21 enseña habitaciones y muebles sin adelantar `there is/there are`, preguntas, negaciones ni preposiciones; pasó tres ciclos de autoría/corrección, validación estructural, cronología exhaustiva y simulación estudiantil. La suite focalizada suma 38 pruebas.
- Resultado longitudinal 1–22: 22 clases y 286 ejercicios válidos. C22 limita `there is/there are` a afirmaciones singulares/plurales, sin adelantar preguntas, negaciones, `any` ni preposiciones; pasó corrección de respuestas, remediaciones, vocabulario exhaustivo y simulación estudiantil. La suite focalizada suma 39 pruebas.
- Resultado longitudinal 1–85: 85 clases y 1.105 ejercicios válidos. C36–C40 introducen presente simple; C41–C45 cubren tercera persona; C46–C50 incorporan negación y preguntas; C51–C55 añaden preguntas WH y agendas; C56–C60 desarrollan frecuencia y tiempo; C61–C65 integran rutinas; C66–C70 cubren capacidad y preferencias; C71–C75 incorporan pronombres objeto y posesión; C76–C80 trabajan cantidades; C81–C85 desarrollan peticiones corteses y restaurante. C85 aporta evidencia de evaluación para las cinco habilidades del bloque; la suite focalizada suma 40 pruebas.
- Simulación C76–C85: `GO` para principiante absoluto, carga alta/dislexia, fallo total, acierto total y reingreso. Todas las clases ofrecen enseñanza previa, consignas breves —máximo observado de 13 palabras—, remediación 4/4, evaluaciones sin pistas y selección determinista con progreso preservado.
- La simulación longitudinal descubrió deuda previa que los validadores legacy no bloqueaban: remediaciones desalineadas en C1/C3/C4/C5, fugas de respuestas en C1–C5 y los tokens no declarados `of`, `it` y `see` en C5/C6/C9–C10. Debe sanearse antes de activar el bloque; no invalida el avance editorial en `shadow`.
- Lote 11–15: rechazado antes de integrar. Aunque cumplía conteos y hashes, sus consignas eran genéricas y repetía estímulos entre práctica, evaluación y repaso. Permanece fuera del repositorio del producto, en un directorio de trabajo temporal.
- Lote 16–20: el agente se detuvo sin crear contenido al no poder garantizar calidad editorial.
- Estos resultados confirman que pasar el validador estructural no basta. Cada lote necesita una simulación pedagógica adversarial antes de incorporarse siquiera en `shadow`.

El flujo posterior mantiene una clase por vez: autor → validador → simulador → corrección → integración. La clase siguiente no comienza antes del `GO` de la anterior.

## Pendiente antes de producción

Convertir el bundle piloto al contrato runtime `exercise-library/1`, probar selección/evidencia/reanudación en el recorrido real, realizar revisión humana lingüística y pedagógica, y activar por unidad con rollback. No se desplegó nada.
