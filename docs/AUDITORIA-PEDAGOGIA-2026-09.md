# Auditoría pedagógica · septiembre de 2026

## Diagnóstico del estado anterior a esta entrega

La ruta inglesa priorizaba ejercicios, no una secuencia completa de enseñanza. La biblioteca contiene 116 preguntas para diez niveles: por nivel 2 de gramática, 3 de listening, 1 de vocabulario, 2 de escritura y 2 de comprensión, salvo el nivel 5 con 18 de comprensión. Las 50 situaciones contienen cada una 3 palabras y 3 objetivos/frases. Eso es una semilla, no cobertura suficiente de un curso completo.

### Problemas comprobados en código

- `library_screen.dart`, `CaminoPersonalizado`: mostrar solo las primeras tres habilidades hacía desaparecer gramática de las recomendaciones tras responder bien. No se borraba su contenido.
- `biblioteca.dart`, `prioridades`: dos respuestas sustituyen el diagnóstico como criterio de prioridad. La recomendación debe destacarse sin ocultar acceso a materias.
- `biblioteca.dart`, `nivelSugerido`: recalcula desde el nivel inicial y solo mira primeros intentos; al repetir una pregunta su evidencia se sobrescribe y deja de entrar en esa muestra. No es un modelo acumulativo de dominio.
- `biblioteca.dart`, `seleccionar`: incluye niveles vecinos incluso si el alumno eligió nivel explícito. Separar selección fija y adaptación.
- `diagnostico.dart`, `BancoDiag.precargar`: diagnóstico inglés y práctica comparten biblioteca, con riesgo de aprendizaje de respuestas del propio test.
- `levels_screen.dart`: la ruta inglesa enlaza biblioteca, evitando explicaciones del currículo clásico.
- `curriculum.dart`: hay material enriquecido empaquetado para niveles 1 y 2. El fallback 3–10 repite el mismo banco de seis palabras y tres frases dentro de veinte unidades por nivel. No contar esas variaciones de título como lecciones diferentes.
- `situation_screen.dart`: la prueba de vocabulario escribía `habilidad`, mientras la ruta lee `skill`. Normalizar evidencia.

## Entrega de gramática

20 guías originales, dos temas por nivel, y 40 preguntas de práctica con retroalimentación. Cada guía incluye objetivo, regla en español, ejemplo bilingüe y error habitual. Son guías introductorias, no un temario exhaustivo ni una certificación. El nivel es interno de OneLingo; no se ha calibrado psicométricamente.

| Nivel interno | Temas de esta entrega |
|---|---|
| 1 | Be; sujeto-verbo-complemento y posición de adjetivos/artículos |
| 2 | Presente simple; frecuencia |
| 3 | Pasado simple; presente continuo frente a hábitos |
| 4 | Cantidades; consejos con should |
| 5 | Present perfect frente a pasado simple; relativas identificativas |
| 6 | Segundo condicional; estilo indirecto |
| 7 | Futuro perfecto frente a continuo; pasiva perfecta |
| 8 | Condicional mixto frente a tercero; inversión con had |
| 9 | Inversión negativa; matización y posibilidad |
| 10 | Concesión; hipótesis formales presentes y pasadas |

La pantalla permite revisar la explicación y los resultados sin que se oculten al terminar. Las evidencias usan `skill: gramatica`, nivel, tema e IDs estables. La comprobación es práctica guiada con respuestas deterministas: no evaluación oficial ni uso de APIs. Solo se registra una respuesta por pregunta y sesión; regresar a explicación no vuelve a otorgar actividad. La evidencia persiste en el proveedor existente; el estado visual de las respuestas es local a esta pantalla.

Las preguntas contrastan forma y significado (por ejemplo, acción futura en curso frente a terminada, condición pasada frente a consecuencia presente), pero siguen siendo reconocimiento de opciones. Falta comprobar producción espontánea, transferencia, retención y uso en contexto nuevo.

## Fuentes y criterio editorial

Consultadas el 19 de septiembre de 2026. Se usaron para contrastar estructuras y alcances, no para copiar ejercicios. Las explicaciones y preguntas de la entrega son originales.

- British Council, [condicionales tercero y mixto](https://learnenglish.britishcouncil.org/free-resources/grammar/b1-b2/conditionals-third-mixed): contraste temporal entre condición y consecuencia. El recurso los sitúa en B1–B2, lo que impide atribuir automáticamente C1 a una pregunta aislada de condicionales.
- British Council, [gramática C1](https://learnenglish.britishcouncil.org/free-resources/grammar/c1): referencia de estructuras avanzadas como inversión. Conocer una forma aislada no implica competencia C1 global.
- Council of Europe, [descriptores del CEFR](https://www.coe.int/en/web/common-european-framework-reference-languages/cefr-descriptors): evaluar capacidades comunicativas por destreza, no únicamente una lista de tiempos verbales.
- Cambridge Dictionary, [Conditionals — English Grammar Today](https://dictionary.cambridge.org/us/grammar/british-grammar/conditional-sentences): contraste del punto de vista del hablante y las condiciones posibles/imaginarias.
- British Council, [A1–A2 grammar](https://learnenglish.britishcouncil.org/free-resources/grammar/a1-a2): referencia de estructuras iniciales; introducción y práctica no son equivalentes a prueba de nivel.

## Lo que sigue pendiente

1. Ampliar cobertura: preguntas, negaciones, posesivos, comparativos, preposiciones, futuros, modales de obligación/deducción, pasados en contraste, gerundios/infinitivos, artículos, relativas no identificativas, cohesión y registro. No saltar de una guía introductoria a estructuras avanzadas sin comprobar prerrequisitos.
2. Separar bancos de práctica y comprobación independiente. Guardar primer intento, reintentos y ayudas, no solo última respuesta.
3. Añadir repaso espaciado y producción en contextos nuevos; no aprobar un nivel por repetir opciones conocidas.
4. Lectura: vocabulario previo opcional durante enseñanza, después idea general, detalles, inferencia y uso de evidencia textual. Evitar pistas en diagnóstico.
5. Listening: primera escucha para idea general, segunda para detalles, transcripción posterior y práctica de segmentación; diversidad de voces y velocidades con dificultad controlada.
6. Situaciones: más léxico, estructuras combinables, alternativas corteses y resolución de problemas, diferenciadas por nivel.
7. Revisores de contenido: comprobar respuestas alternativas válidas, distracciones, ambigüedad y adecuación al objetivo. Simular estudiante principiante, intermedio y avanzado, incluyendo errores plausibles.
8. Medición: guardar exposición, respuesta inicial, ayudas, latencia y repaso posterior. Rachas y animaciones deben premiar práctica real sin prometer dominio.

## Validación

`grammar_guides_test.dart` comprueba cobertura de diez niveles, IDs únicos, presencia de enseñanza, alternativas únicas y claves de respuesta válidas. El test no acredita calidad pedagógica: esa requiere revisión editorial y pruebas con alumnos. Los archivos Dart fueron formateados con el SDK del proyecto; ejecución de tests y prueba visual corresponden a la integración principal.


## Estado final de integración

Consultar PLAN-APRENDIZAJE-2026-09-19.md para el resultado actualizado. La entrega pasó de 20 a 43 temas de gramática y amplió las 50 situaciones a 550 entradas. Se corrigieron transcripción de apoyo persistente entre unidades, orden de opciones léxicas, nivel fijo en agrupación de lecturas, acceso permanente a las cinco áreas y preferencia de animaciones/texto grande en racha. Estos documentos conservan hallazgos de la revisión inicial; no todos siguen pendientes.
