# Inventario completo de inglés: maestro 10 x 100 frente al producto

Estado: inventario editorial vivo. Fecha: 2026-09-30.

## Conclusión ejecutiva

Inglés tiene tres capas que no deben mezclarse:

1. El PDF maestro contiene **1.000 especificaciones**, cien por nivel. Su estructura está completa, pero no son clases publicables.
2. La fuente local de esquema 2 indexa **290 unidades editoriales**: N1=100, N2=100 y N3=90; conserva 7 unidades de Fundamentos (`f0`), fuera del objetivo 10 x 100. Las 29 unidades A1 heredadas siguen en disco como respaldo, pero ya no están en el índice inglés local.
3. Los mapas editoriales v2 de N2/N3 y el plan de N1 gobiernan la producción reproducible; ningún mapa por sí solo activa contenido.

La cobertura correcta es: **1.000/1.000 especificaciones estructurales**, **1.000/1.000 IDs planificados** y **290/1.000 clases editoriales integradas y publicadas**. Inglés N1 aporta 100 clases/1.300 ejercicios; N2 otras 100/1.300; N3 C1–C90 aporta 90/1.170. Los JSON de autoría N2/N3 conservan `status: shadow`, mientras el manifiesto de runtime los declara `active`. Las 29 unidades heredadas siguen como respaldo y trazabilidad; no se contabilizan como clases adicionales.

## Fuentes y autoridad

| Fuente | Qué decide | Qué no decide |
|---|---|---|
| PDF maestro | Intención del cliente, diez niveles y cien títulos/resultados generales por nivel | Secuencia final, adecuación MCER, ejercicios, respuestas, prerrequisitos o publicación |
| `assets/contenido/en/curriculo-master.json` | Transcripción del PDF, 1.000 IDs `en.nX.lYYY` y trazabilidad | Activación; los 1.000 registros siguen en `especificacion_fuente` |
| `PLAN_NIVEL1_INGLES_100.md` | Reestructuración propuesta de N1 en 20 bloques | Cuerpo completo o bancos de ejercicios |
| `assets/contenido/en/ruta/` | Fundamentos y recorrido editorial activo N1–N3 | Contenido aún no redactado de N3 C91–C100 y N4–N10 |
| `assets/contenido/en/biblioteca.json` | 116 preguntas actuales de diagnóstico/práctica | Biblioteca editorial por clase; no tiene pools separados |
| Metodología y biblioteca v1 | Contrato y puertas de calidad | No convierten una especificación en contenido |

El PDF atribuye a la IA modelado, corrección y reciclaje de debilidades. La decisión vigente lo sustituye: ruta base, evaluación y repaso son editoriales y deterministas; la conversación con IA solo puede ser opcional. El manifiesto importado elimina esas instrucciones y conserva únicamente el escenario como `practicaEditorial`; cada escenario todavía debe convertirse en ejercicios y respuestas antes de aprobar contenido.

## Mediciones comprobadas

### Maestro del cliente

- 202 páginas, 10 niveles y 100 lecciones numeradas por nivel.
- 1.000 IDs únicos, sin campos principales vacíos en la transcripción.
- 1.000 registros en estado `especificacion_fuente`.
- N1 es relativamente concreto; N2-N10 usan 18 temas x 5 clases hasta la 90 y diez cierres genéricos.
- En N2-N10 un tema alterna entre `vocabulary/grammar/listening/speaking/reading` y `writing/pronunciation/conversation/role-play/integrated skills`. Cada tema queda sin la mitad de una secuencia pedagógica completa.
- Las clases 91-100 de N2-N10 repiten categorías genéricas y necesitan alcance, textos, rúbricas y evidencias propios.

### Activos ingleses en fuente local

| Capa | Cantidad | Observación |
|---|---:|---|
| Fundamentos `f0` | 7 unidades | No cuenta en 10 x 100 |
| Nivel editorial `n1` | 100 unidades | Indexadas, activas y publicadas |
| A1 heredado `a1-1`/`a1-2` | 29 unidades | Preservadas en disco y resueltas por alias, fuera del índice local |
| N2 editorial | 100 clases | Fuente editorial `shadow`; runtime activo y publicado |
| N3 editorial | 90 clases | C1–C90 activas y publicadas; C91–C100 pendientes de autoría |
| Enseñanza en las 36 unidades | 150 pasos | Explicación, ejemplos, vocabulario, patrón o tabla |
| Interacción en las 36 unidades | 528 ítems | 139 guiados, 104 independientes, 67 de situación y 218 de evaluación |
| `biblioteca.json` | 116 preguntas | 10 por nivel salvo N5, con 26; no está vinculada a cien clases por nivel |

No se deben sumar los 150 pasos y los 528 ítems como si fueran la misma unidad de medida.

## Cobertura real N1-N10

| Nivel | Nombre del PDF | Especificaciones | Ruta activa | Mapa editorial | Clases nuevas activables | Hueco principal |
|---|---|---:|---:|---|---:|---|
| N1 | Beginner Foundations | 100 | 100 producción | Sí, 100 | 100 `active` | Revisión humana continua |
| N2 | Elementary Communication | 100 | 100 producción | Sí, 100 (v2) | 100 `active` | Revisión del cliente |
| N3 | Pre-Intermediate Communication | 100 | 90 producción | Sí, 100 (v2) | 90 `active` | Producir C91–C100 y revisar |
| N4 | Intermediate Communication | 100 | 0 | No | 0 | Mapa, prerrequisitos y contenido |
| N5 | Upper-Intermediate Communication | 100 | 0 | No | 0 | Mapa, calibración y contenido |
| N6 | Advanced Communication | 100 | 0 | No | 0 | Mapa, calibración y contenido |
| N7 | Advanced Plus | 100 | 0 | No | 0 | Diferenciar avance frente a N6/N8 |
| N8 | Near-Fluent Communication | 100 | 0 | No | 0 | Cambiar etiquetas de fluidez por resultados observables |
| N9 | Professional Fluency | 100 | 0 | No | 0 | Equilibrar inglés general, académico y profesional |
| N10 | Mastery and Bilingual Communication | 100 | 0 | No | 0 | Retirar promesas `native-like/bilingual`; mantener C1 |

«Ruta activa» es contenido utilizable hoy. «Activable» exige biblioteca editorial, evaluación reservada, repaso nuevo, revisión y simulación.

## Escala resuelta

Se adoptó la escala del cliente (DEC-020): N1 cubre A1 completo y los niveles siguientes progresan hasta C1 avanzado en N10. El valor histórico nunca se sobrescribe; se añade escala/versionado y una equivalencia conservadora. Las 29 unidades activas de `a1-1` y `a1-2` son fuente para N1, pero sus IDs y evidencias antiguas se conservan mediante aliases.

## Mapa por nivel y tratamiento

| Nivel | Núcleo del PDF, clases 1-90 | Tratamiento editorial |
|---|---|---|
| N1 | Identidad, casa, rutina, comida, compras, comunidad, salud y trabajo; después continuo, pasado, futuro y simulaciones | Usar el plan N1 corregido; mover pasado completo, futuro y problemas complejos |
| N2 | Presente, pasado, futuro, present perfect inicial, comparación, cantidad y modales; viaje, trabajo, salud y tecnología | Reconstruir 20 bloques completos y evitar repetir A1 absorbido por N1 |
| N3 | Present perfect, narración, futuros, condicionales, gerundio/infinitivo, relativas, pasiva y reported speech | Calibrar A2/B1 según la escala; concretar léxico y corpus |
| N4 | Past perfect, tiempos narrativos, condicionales, deducción, pasiva, registro y colocaciones | Eliminar solapamientos con N3 y fijar transferencia |
| N5 | Elección temporal, perfect forms, mixed conditionals, especulación, causativas, idioms y lenguaje académico | Convertir etiquetas gramaticales en objetivos comunicativos |
| N6 | Precisión narrativa, inversión, modales, nominalización, diplomacia, retórica y cohesión | Delimitar nivel y crear rúbricas de producción extendida |
| N7 | Registro, cronología, contrafactuales, lenguaje epistémico, cohesión y argumentación | Reducir repetición de liderazgo/negociación y probar avance |
| N8 | Comprensión rápida, inferencia, retórica, registro, metáfora y variación regional; medios y academia | Sustituir `near-fluent`; planificar audio auténtico licenciado |
| N9 | Comunicación ejecutiva, riesgo/política, diplomacia, datos, informes y propuestas | Mantener una vía general además de la profesional |
| N10 | Humor, ironía, cultura, debate, diplomacia, academia, paneles, investigación y escucha avanzada | Presentarlo como C1 avanzado, no como bilingüismo garantizado |

Las clases 91-100 de N2-N10 comparten el mismo cierre genérico: repaso, medio/canción, proyecto narrativo, simulación, lectura, escritura, speaking, práctica integrada y evaluación. Cada nivel debe recibir materiales y criterios propios.

## Auditoría del plan N1

El plan tiene exactamente 100 entradas y 20 bloques. Distribución:

| Acción | Clases | Lectura correcta |
|---|---:|---|
| `C` conservar | 9 | Base cercana; aún requiere pools y revisión |
| `D` dividir | 51 | Una unidad alimenta varias clases; no son 51 clases escritas |
| `R` reescribir | 16 | Reutilización parcial |
| `N` crear | 24 | Sin base suficiente |

Fortalezas: mantiene F0 separado; ordena entrada, patrón, comprensión, producción y transferencia; retira exceso de pasado/futuro; excluye al tutor IA obligatorio.

N1 ya tiene vocabulario cronológico, textos, audio TTS editorial, ejercicios y evaluaciones hasta C100, y está publicado. N2 completo y N3 C1–C90 también están publicados para revisión del cliente. Siguen siendo necesarias revisión lingüística/pedagógica continua y comprobación de licencias para cualquier medio futuro. La escala, los 1.000 IDs y prerrequisitos de planificación están versionados.

## Especificación frente a contenido publicable

| Componente | Maestro | Publicable |
|---|---|---|
| Tema/resultado | General | Conducta observable y criterio de éxito |
| Vocabulario | Concreto sobre todo en N1 | Lista versionada, sentido, pronunciación y exposición |
| Gramática | Etiqueta/intención | Regla, contraste, ejemplos, errores y prerrequisitos |
| Enseñanza | Descripción | Texto, ejemplos y medios finales |
| Práctica | Consigna atribuida a IA | Familias con respuestas, distractores y feedback |
| Evaluación | Intención | Pool reservado, al menos 4 variantes y 2 formatos en transferencia |
| Repaso | «Recycle weak points» | Pool `review` inédito y determinista |
| Corrección | IA | Claves, aceptadas, rúbrica o revisión humana definida |
| Progreso/QA | Ausente | Evidencia versionada, validación y simulación |

## Volumen editorial pendiente

Rango de planificación por clase, a calibrar en el piloto:

- 3-6 piezas de enseñanza;
- 3-5 variantes guiadas;
- 3-5 de práctica/aplicación;
- al menos 4 de evaluación en clases de transferencia;
- 3-5 variantes inéditas de repaso;
- metadatos, respuestas, feedback, distractores, prerrequisitos y revisión.

Son aproximadamente **16-25 piezas o variantes por clase**: 1.600-2.500 por nivel y 16.000-25.000 para los diez. Es capacidad editorial, no cuota que sustituya calidad.

Reutilización: 29 unidades activas, 528 ítems interactivos que deben clasificarse, 116 preguntas como semilla y cien especificaciones N1. En el plan N1, 76 clases declaran relación con activos (`C`, `D` o `R`) y 24 son nuevas. Nada de esto crea el pool `review` automáticamente.

## Orden de lotes

### Fase 0

1. Aplicar DEC-020 y verificar equivalencia/versionado de progreso.
2. Congelar mapa N1, IDs, conceptos, prerrequisitos y resultados.
3. Importar en seco las 36 unidades y clasificar 528 ítems.
4. Definir corpus, audio, licencias, rúbricas y responsables.

### N1: veinte lotes secuenciales

| Orden | Clases | Alcance |
|---:|---:|---|
| 1 | 1-5 | Piloto: identidad y objetos |
| 2-5 | 6-25 | Artículos/plural, descripción, posesión y casa |
| 6-7 | 26-35 | Ubicación, órdenes e integración inicial |
| 8-10 | 36-50 | Presente simple, tercera persona, negación y preguntas |
| 11-13 | 51-65 | WH, frecuencia, tiempo e integración de rutina |
| 14-15 | 66-75 | Capacidad, gustos, pronombres y posesión |
| 16-17 | 76-85 | Cantidad y peticiones corteses |
| 18-19 | 86-95 | Continuo, conectores e integración final |
| 20 | 96-100 | Repaso, evaluación, conversación por tarjetas y proyecto |

Cada lote avanza `legacy -> shadow -> active`. Auditorías acumulativas en 25, 50, 75 y 100 clases.

### N2-N10

N2 está completo. Para N3 faltan C91–C100 y la auditoría longitudinal C1–C100. Para N4–N10: crear y aprobar primero un mapa editorial v2 propio, contrastar solapamientos, producir veinte lotes de cinco y cerrar cada nivel con simulación longitudinal. No redactar un nivel avanzado desde su mapa legacy ni antes de fijar su grafo.

## Puerta de publicación

Cada lote exige cinco clases alcanzables; enseñanza previa; pools separados; cero familia compartida con evaluación/repaso; estímulos de repaso inéditos; corrección no ambigua; licencias; revisión curricular, estructural, pedagógica y lingüística; simulaciones; cero IA obligatoria; manifiesto, impacto de progreso y rollback comprobados.

## Siguiente ejecución

Producción `20260930-edu-5-n2-n3-review` contiene N1 C1–C100, N2 C1–C100 y N3 C1–C90: 290 clases y 3.770 ejercicios. La siguiente ejecución es N3 C91–C95 y C96–C100 con agentes independientes, seguida de auditoría longitudinal N3 C1–C100. Solo tras GO debe ampliarse el runtime a 300 clases. N4 permanece NO-GO hasta aprobar su mapa editorial v2.
