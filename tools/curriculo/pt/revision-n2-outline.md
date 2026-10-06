# Revisión final del outline N2 · portugués de Brasil

Fecha: 2026-10-03  
Estado: **GO editorial en staging**  
Alcance: mapa de 50 clases; todavía no contiene ejercicios y no activa portugués.

## Resultado verificable

- 50 clases ordenadas, `pt.n2.c01`–`pt.n2.c50`, cinco por bloque.
- 48 claves nuevas únicas; C49 es proyecto y C50 prueba, ambos sin gramática nueva.
- 89 claves previas disponibles desde Nivel 0, Fundamentos y N1.
- Objetivos ES/EN específicos, observables y sin la plantilla genérica usada en el primer borrador.
- Vocabulario de 6–12 entradas por clase y tareas comunicativas delimitadas a A2.
- Validación: `0 errores · 50 clases · 48 claves nuevas · 89 previos`.

Comando:

```bash
python3 tools/curriculo/validar_outline_nivel.py pt 2 tools/curriculo/pt/n2-outline.json
```

## Correcciones exigidas antes del GO

1. C01 dejó de repetir `sou/tenho/venho` como contenido nuevo y amplía el presente con `faço/faz` y `digo/diz`.
2. C06–C09 distingue la expansión del pretérito de N1; C09 enseña y evalúa `disse`, `pôs`, `veio`, `quis` y `pôde`.
3. C13 fija el objeto indirecto con `para ele/ela`, sin adelantar `lhe`.
4. C14 incorpora `ficar sem` para expresar la consecuencia de un problema doméstico.
5. C23 eliminó `melhor/pior`, que no estaban explicados por el patrón regular de superlativo.
6. C25 modela el uso brasileño: `me/te` proclíticos, `ele/ela` como objeto tónico coloquial y objeto nulo cuando el referente es claro; no enseña enclisis europea.
7. C28 limita las fórmulas con `se` a reconocimiento en un rótulo formal y no enseña pasiva ni concordancia.
8. C31 usa participios coherentes con equipaje: perdido, encontrado y danificado.
9. C39 separa recomendaciones generales seguras de cualquier diagnóstico o tratamiento.
10. C46 explicita el contraste inicial imperfeito/perfeito y el plan con `ir + infinitivo`; C47–C50 tienen productos distintos y reciclaje representativo del nivel.

## Auditorías independientes

Tres revisiones separadas volvieron a ejecutarse después de las correcciones:

- **Alineación introduce/gramática/vocabulario/tarea: GO.** Revisó las 50 clases y, de forma reforzada, C13, C23, C25, C28, C31, C39 y C46–C50.
- **Gramática y límites pt-BR/A2: GO.** Confirmó perfecto, futuro, objetos de uso brasileño, `se`, salud, `por/para`, equivalencia ES/EN y ausencia de plantillas genéricas.
- **Auditoría independiente longitudinal: GO.** Confirmó prerrequisitos de N1, 48 claves únicas, progresión espiral y reserva de contenidos avanzados para N3.

## Decisión de publicación

Este GO autoriza la autoría de fichas y ejercicios N2 por lotes revisables. No autoriza copiar contenido a `assets/`, habilitar portugués, compilar el diagnóstico ni desplegar.

Hitos posteriores: C01–C05 y C06–C10 ya se produjeron con 130 ejercicios deterministas. Ambos lotes obtuvieron GO técnico, revisión pt-BR y simulación de estudiante después de corregir fuentes insuficientes, secuencias agramaticales y una escena contaminada. El siguiente lote permitido es C11–C15.
