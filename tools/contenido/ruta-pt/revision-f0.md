# Revisión de la ruta portuguesa de Fundamentos

Fecha: 2026-10-03  
Artefacto: `borrador-f0.json`  
Estado: **GO** (editorial; bloqueo de F6 resuelto el 2026-10-05, ver abajo).

## Resultado

- 8 unidades ejecutables, orden 0–7 y cadena continua de prerrequisitos.
- 102 vocablos visibles, idénticos al inventario canónico de `curriculo/pt/f0.json`.
- 104 ejercicios: por unidad, 3 guiados, 3 independientes, 2 de situación y 5 evaluativos.
- 24 claves pedagógicas proyectadas en `gramatica` y cubiertas por los ejercicios.
- Apoyo ES/EN, portugués de Brasil y corrección determinista; no depende del tutor IA.
- Enseñanza visible antes de usar vocabulario, respuestas u opciones.
- Validador de esquema 2 en modo estricto: 0 errores y 0 advertencias.

## Revisión cruzada

Los lotes F1–F4 y F5–F8 tuvieron autores separados y se unieron de forma mecánica. El revisor independiente devolvió REVISE por dos problemas de trazabilidad:

1. F1–F4 conservaban `introduce`, un campo editorial ajeno al esquema ejecutable. Se retiró; la fuente de esas claves sigue siendo `curriculo/pt/f0.json`.
2. La ruta enseñaba `muito` y `também`, ya utilizados por las fichas, pero el inventario canónico no los incluía. Se añadieron al plan con apoyo ES/EN.

Tras ambas correcciones, el revisor emitió **GO editorial para staging**.

## Adaptaciones necesarias al runtime

- Un ejercicio de puntuación se volvió selección para que el normalizador no elimine la diferencia evaluada.
- Los correos de F7 se evalúan por selección inequívoca: el normalizador elimina puntos y no debe aceptar direcciones diferentes.
- El ejercicio `relacionar` de F8 usa tres pares, mínimo admitido por el componente.

## Bloqueo de publicación (resuelto 2026-10-05, fase P0)

El único bloqueo era `pt.f0.perguntar-reparar` · `p11` · `e2`: distinguir «Você é Ana.» de «Você é Ana?» solo por entonación (A→B), que el TTS no garantiza. Se sustituyó por un ítem textual equivalente con el mismo id (`e2`) y la misma clave (`intonation-q`): formato `elegir`, el alumno quiere confirmar si la persona es Ana y elige la frase escrita como pregunta entre «Você é Ana.», «Você é Ana?» y «Você não é Ana.» (respuesta 1); el feedback explica que el orden no cambia y que al hablar la voz sube al final. Se retiró el metadato `produccionAudio`; `validar.py` ahora exige que no quede ninguno. La evaluación de F6 mantiene 4 formatos. El borrador se integra en `assets/contenido/pt/ruta/` con `integrar.py` (solo Fundamentos; portugués sigue fuera de `idiomasConRuta`).

## Reproducir la validación

```bash
python3 tools/curriculo/validar_fundamentos.py pt
python3 tools/contenido/ruta-pt/validar.py
```
