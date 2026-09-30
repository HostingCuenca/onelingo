# Metodología editorial 10 × 100

Estado: diseño para sustituir progresivamente la metodología anterior sin romper el producto publicado.

## Principio rector

La ruta base es determinista y editorial. OneLingo entrega contenido, ejercicios, evaluaciones y repasos creados, revisados y versionados por el equipo. La IA conversacional queda fuera del camino crítico y solo puede ofrecer una práctica opcional claramente identificada.

## Estructura de cada nivel

Cada nivel contiene 20 bloques de cinco clases:

1. **Entrada y vocabulario:** significado, sonido/escritura, ejemplos y reconocimiento.
2. **Patrón y gramática:** forma, uso, contraste y errores frecuentes.
3. **Comprensión:** escucha y lectura con dificultad controlada.
4. **Producción:** escritura, pronunciación y habla guiada que avanza a independiente.
5. **Transferencia:** situación real, evaluación editorial y programación del repaso.

Veinte bloques × cinco clases = cien clases. La última parte del nivel puede usar bloques de integración, proyecto y evaluación acumulativa, pero conserva el mismo contrato de evidencia.

## Separación de bancos

Una familia de ejercicio pertenece a un único propósito de exposición:

- `teach`: ejemplo interactivo o demostración; no puntúa dominio.
- `practice`: práctica con o sin ayuda; puede reciclar conceptos, no ítems reservados.
- `assessment`: ítems reservados que deciden aprobación.
- `review`: variantes editoriales no vistas que miden retención y transferencia.

No basta con cambiar el orden de opciones. Dos ítems con la misma respuesta, estructura superficial y contexto pertenecen a la misma familia y no pueden cruzar de práctica a evaluación o repaso reservado.

## Unidad mínima de biblioteca

Cada ejercicio necesita, como mínimo:

- ID global estable y versión;
- idioma meta y texto de apoyo;
- estado editorial: borrador, revisado, publicado o retirado;
- propósito/pool;
- familia y variante;
- clase, bloque, conceptos y habilidades;
- nivel interno y MCER;
- vocabulario permitido y prerrequisitos;
- formato, estímulo, respuesta, alternativas y feedback;
- dificultad y tiempo estimado;
- origen y revisión lingüística;
- reglas de incompatibilidad/exposición.

## Repaso editorial

El planificador decide cuándo repasar; la biblioteca decide qué ejercicio puede mostrar.

Selección mínima:

1. tomar conceptos vencidos según el historial;
2. excluir familias ya usadas en enseñanza, práctica o evaluación reciente;
3. elegir una variante `review` compatible con vocabulario y escritura dominados;
4. alternar reconocimiento y producción;
5. registrar familia, variante, resultado y tiempo;
6. si falla, crear estado de `refuerzo` sin borrar una aprobación histórica;
7. recomendar contenido editorial de reparación antes del siguiente intento.

La selección debe ser reproducible con una semilla derivada de alumno, fecha de sesión y concepto. No requiere IA generativa.

## Progreso por competencia

Además del estado por unidad, se registra evidencia por concepto y habilidad:

- visto;
- practicado con ayuda;
- producido sin ayuda;
- aprobado con ítem reservado;
- retenido después del intervalo;
- necesita refuerzo.

Esto impide que un diagnóstico general omita escritura, pronunciación o gramática no demostradas.

## Migración transparente

1. Congelar IDs actuales y documentar su correspondencia.
2. Crear la biblioteca nueva sin cambiar la lectura del esquema 2.
3. Importar los ítems embebidos actuales y clasificarlos por pool/familia.
4. Mantener un adaptador para unidades antiguas.
5. Poblar y validar primero Inglés Nivel 1 en paralelo a la ruta vigente.
6. Activarlo detrás de una versión curricular, nunca por reemplazo silencioso.
7. Migrar progreso por tabla explícita de equivalencias.
8. Ejecutar simulaciones de alumnos y comparación de resultados.
9. Publicar por nivel/idioma; conservar rollback a la versión anterior.
10. Retirar el adaptador solo cuando todas las unidades activas estén migradas.

## Puertas de calidad antes de publicar

- 100 clases exactas y alcanzables en el nivel.
- Ningún concepto evaluado antes de enseñarse.
- Todas las palabras usadas están expuestas cronológicamente, no solo declaradas.
- Cada habilidad declarada tiene evidencia observable.
- Evaluación y repaso usan familias reservadas.
- No hay duplicados ni casi duplicados entre pools incompatibles.
- Hay una recomendación accionable para todos los estados de alumno.
- Diagnóstico no apunta a niveles vacíos.
- Prerrequisitos de escritura se comprueban por competencia.
- El recorrido base realiza cero llamadas a tutor o generador IA.
- Las claves de progreso anteriores mantienen significado o tienen migración explícita.
- Validación automática, revisión editorial y revisión lingüística están registradas.

## Orden de trabajo

1. Inglés Nivel 1: mapa de 100 clases y correspondencia de las unidades existentes.
2. Contrato y cargador de biblioteca editorial.
3. Importador de ejercicios actuales y detector de contaminación.
4. Repaso nuevo con banco separado.
5. Simulaciones automatizadas y validadores semánticos.
6. Inglés niveles 2–10 por lotes.
7. Por cada nuevo idioma: mapa propio, F0 como prerrequisito, niveles 1–10 y revisión lingüística.

