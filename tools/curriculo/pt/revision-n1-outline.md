# Revisión del outline portugués N1

Fecha: 2026-10-03  
Artefacto: `n1-outline.json`  
Estado: **GO de esqueleto pedagógico; todavía no es el plan canónico con ejercicios**.

## Inventario

- 40 prerrequisitos exactos: 16 salidas de Nivel 0 y 24 de Fundamentos.
- 50 clases A1, 5 por bloque, alineadas con `curriculo/marco.json`.
- 49 claves nuevas únicas; C50 no introduce gramática.
- 6–12 vocablos específicos por clase; el outline actual usa 8.
- Objetivo, tarea y sonido concretos en cada clase.
- Repaso de cada clave con reaparición inmediata, +2/+3 y aproximadamente +7 cuando hay espacio; las claves tardías cierran en C50.

## Ciclo de revisión

El primer borrador fue rechazado aunque cumplía los conteos: repetía el mismo vocabulario en las cinco clases de cada bloque, usaba objetivos/tareas genéricos y creaba claves artificiales de integración.

El segundo borrador recibió REVISE por duplicar salidas de Fundamentos, clasificar `viver` como verbo `-ir`, omitir el imperativo del bloque 9, usar focos fonéticos falsos (`ônibus` como nasal, `r` en `cidade`) y no demostrar repaso espaciado.

Tras esas correcciones, dos revisores distintos emitieron un primer GO:

- auditoría gramatical: pt-BR productivo, límites A1, claves y progresión correctos;
- simulación de estudiante ES/EN: carga, utilidad, interferencia, repaso y salida C50 coherentes.

La población piloto C01–C05 y C46–C50 reabrió la auditoría semántica. Se detectaron y corrigieron:

- el título duplicado de C04 y tareas que no medían todos los elementos declarados;
- 22 objetivos en inglés que repetían la tarea en lugar de traducir el objetivo español;
- cobertura explícita de pregunta/respuesta de hora en C26, `devo/deve` en C38, las cuatro formas regulares de C47 y producción de irregulares en C48;
- `nationality-gender` como reciclaje declarado en C02.

La revisión final comparó una por una las 50 parejas ES/EN de objetivo y tarea y emitió **GO sin regresiones**. No se cambiaron las 49 claves nuevas ni la progresión gramatical.

## Límites

Este archivo no lleva planes de ejercicios y usa `estado: "esqueleto"`; por eso no se copia todavía a `curriculo/pt/n1.json` ni autoriza escribir clases. El siguiente paso es convertir cada ficha en `planificado` con práctica guiada, independiente, situación y evaluación determinista, manteniendo exactamente esta progresión.

## Validación

```bash
python3 tools/curriculo/validar_outline_n1.py pt
```
