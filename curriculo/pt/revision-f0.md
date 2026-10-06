# Revisión del plan de Fundamentos portugués

Fecha: 2026-10-03  
Alcance: `curriculo/pt/f0.json`  
Resultado: **GO de planificación; contenido de la ruta todavía no escrito ni activado**.

## Inventario validado

- 8 unidades Pre-A1, de `pt.f0.primeiro-contato` a `pt.f0.apresentar-se`.
- 24 claves nuevas, sin duplicados y con prerrequisitos ordenados.
- 102 entradas de vocabulario con ids únicos. La conversión ejecutable detectó y formalizó dos apoyos ya usados por las fichas: `muito` en F1 y `também` en F5.
- Por unidad: 3 ejercicios guiados, 3 independientes, 2 preguntas de situación y 5 de evaluación.
- Evaluación de todas las claves introducidas y al menos tres formatos por unidad.
- Apoyo bilingüe español/inglés y variante productiva pt-BR.
- Sin tutor IA para explicar, corregir ni aprobar.

## Proceso editorial

Los primeros borradores parciales fueron descartados porque contenían plantillas y no alcanzaban el detalle requerido. F1–F4 y F5–F8 se reescribieron por separado, se unieron mecánicamente y un revisor distinto auditó las ocho unidades completas.

La revisión inicial pidió una corrección en F6: el contraste de entonación interrogativa debía especificar audios comparables y controles verificables. El plan final usa dos grabaciones con la misma voz y velocidad, referencias distintas y revisión auditiva humana obligatoria antes de publicar.

También se aclaró que las fórmulas de F2 con `estar` se aprenden como bloques; la conjugación se analiza recién en F3.

Durante la conversión a esquema ejecutable, la revisión cruzada detectó dos apoyos que ya aparecían en los ejercicios o diálogos pero no en el inventario: `muito` y `também`. Se añadieron a la fuente canónica en vez de ocultarlos en la ruta. También se retiró de los borradores ejecutables el campo editorial `introduce`; las 24 claves permanecen en este plan y se proyectan en `gramatica` sin crear una segunda fuente paralela.

## Evidencia automática

```text
python3 tools/curriculo/validar_fundamentos.py pt
0 errores, 0 avisos · 8 unidades · 24 claves · 102 vocablos
```

## Pendientes de producción

1. Escribir la ruta nueva de Fundamentos a partir de estas fichas, sin recuperar el f0 legado.
2. Producir y revisar los dos audios comparables de F6.
3. Validar el contenido con el validador de ruta y revisión separada ES/EN.
4. Mantener portugués inactivo hasta completar los requisitos técnicos del Nivel 0, Fundamentos y N1.
