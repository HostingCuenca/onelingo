# Contrato de producción por clase — Inglés 10 × 100

Estado: obligatorio para todo contenido nuevo. El piloto N1 1–5 es la referencia, pero cada clase debe pasar este contrato por sí misma.

Desde Inglés N2 C16 también es obligatorio `PROTOCOLO_AGENTES_CONTENIDO.md` y la política verificable `editorial-agent.v2`.

## Flujo incremental

1. El autor redacta **una clase**, nunca un lote completo sin revisión intermedia.
2. El validador estructural y semántico se ejecuta sobre esa clase.
3. Un agente distinto simula cinco perfiles: principiante absoluto, carga alta/dislexia, fallo total, acierto total y reingreso.
4. El autor corrige la misma clase hasta recibir `GO`.
5. Solo entonces se inicia la clase siguiente.
6. Cada quinta clase añade evaluación acumulativa del bloque y se prueba también como recorrido longitudinal.

Un JSON válido no implica contenido aprobado. Los borradores rechazados se conservan fuera del repositorio del producto y nunca se activan.

## Contrato mínimo por clase

- ID estable `en.nX.class-YYY`, escala `client-10-levels-v1`, `status: shadow` y `runtimeAi: false`.
- Prerrequisito por ID de clase, no por una etiqueta ambigua.
- Conceptos locales y requisitos que solo usan conceptos ya enseñados.
- 6–12 entradas de vocabulario correctamente traducidas.
- 4–6 piezas de enseñanza autocontenidas, con explicación en español, segmentación y fuente TTS inglesa.
- 3 ejercicios guiados, 3 independientes, 4 de evaluación en al menos dos formatos y 3 de repaso.
- Feedback específico en todos los ejercicios; pistas únicamente en práctica guiada.
- `remediationMap` para cada ítem de evaluación, enlazado a una enseñanza y a una variante de repaso válidas.
- Accesibilidad: instrucciones breves, velocidad de audio, repetición, segmentación y variantes aceptadas razonables.
- Evidencia determinista y selección congelada al reingresar.

## Criterios semánticos no negociables

- La consigna contiene toda la información necesaria. Se prohíben textos como «Resuelve la actividad», «Escribe la frase indicada» o «Elige el significado indicado» sin mostrar el objetivo.
- Un ítem `completar` guarda únicamente el fragmento ausente. Por ejemplo, `He is ___ teacher` acepta `a`, no `a teacher`.
- Los distractores deben ser plausibles pero inequívocamente incorrectos para lo enseñado.
- La producción independiente solo evalúa patrones enseñados y practicados previamente.
- Evaluación y repaso usan estímulos inéditos. No se acepta copiar la misma frase, pares o respuesta contextualizada desde enseñanza o práctica.
- Un cambio de puntuación, mayúsculas u orden de opciones no crea una variante pedagógica nueva.
- La clase de cierre de cada bloque de cinco declara `cumulativeEvaluation` y aporta evidencia real de todos los conceptos del bloque.
- Ningún ejercicio depende de un tutor o generador IA en ejecución.

## Puerta de integración

Una clase puede incorporarse al directorio editorial del producto solo con:

- validador común aprobado;
- revisión adversarial sin P0/P1;
- simulación estudiantil con `GO`;
- hashes reproducibles;
- ausencia de activación del runtime;
- registro del resultado en el informe de QA.

La activación `shadow → active` es una fase posterior y requiere integración con `exercise-library/1`, prueba de recorrido real, revisión humana y rollback comprobado.
