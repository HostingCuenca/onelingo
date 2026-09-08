# OneLingo · Prueba de nivel (posicionamiento)

## Para qué
Que una persona que ya sabe algo del idioma **no empiece desde el Nivel 1**: la prueba la
coloca en uno de los 10 niveles, los niveles inferiores quedan **convalidados** (abiertos para
repasar, no obligatorios) y el camino, la lección diaria y la IA arrancan en su nivel.

## Cómo lo hacen los exámenes de referencia
| Prueba | Formato | Duración / preguntas | Resultado |
|---|---|---|---|
| Oxford Online Placement Test | Adaptativo por ordenador: cada pregunta se elige según la anterior | 30-40 min | Pre-A1 a C2 |
| Cambridge Placement Test | Autoevaluación inicial → bloques por nivel; sube, baja o se queda; termina cuando se estabiliza | ~25 preguntas | Examen Cambridge recomendado |
| EF SET | Adaptativo, lectura + escucha | 50 min | A1-C2 con certificado |
| DIALANG | Test de vocabulario + autoevaluación para elegir el nivel del test; modelo IRT/Rasch | variable | A1-C2 por destreza |

Lección aprendida: el modelo eficaz es **arranque por autoevaluación + bloques cortos adaptativos +
parada al estabilizarse**, con 10-25 preguntas. Los motores estadísticos (IRT) llegan al nivel
correcto ~65 % de las veces y fallan por medio nivel; para OneLingo basta un algoritmo de
búsqueda por bloques, transparente y rápido.

## Algoritmo de OneLingo (`lib/core/placement.dart`)
1. **Autoevaluación** (5 opciones) → nivel de arranque 1 / 2 / 4 / 6 / 8.
2. **Bloque de 3 preguntas** del nivel actual (preguntas del examen generado de sus unidades;
   si no hay, ejercicios de opción de las lecciones). ≥ 2 aciertos = aprueba el bloque.
3. Si aprueba sube; si falla baja. Mientras no haya cota en ese sentido salta **de dos en dos**
   (búsqueda binaria), luego de uno en uno.
4. **Termina** cuando aprobó N y falló N+1, al tocar los extremos (falla el 1 o aprueba el 10) o
   a los 8 bloques (24 preguntas). Resultado = nivel más alto aprobado (mínimo 1).
5. Pantalla de resultado: nivel, precisión, qué queda convalidado; el alumno puede aceptar o
   **empezar un nivel más abajo** (nunca más arriba).
6. Se registra el evento `prueba_nivel` (nivel recomendado, elegido, preguntas, precisión) y se
   ve en el panel.

Simulación en `test/placement_test.dart`: un alumno de nivel real 1, 3, 5, 7 o 10 queda bien
posicionado desde cualquier autoevaluación, en ≤ 24 preguntas.

## Dónde está en la app
- Registro → paso 4 "¿Cuál es tu nivel?" → tarjeta *Hacer la prueba de nivel (recomendado)*.
- Perfil → *Prueba de nivel* (repetirla y ajustar el punto de partida).
- Ruta `/prueba-nivel?idioma=xx`.

## Convalidación
`nivelInicial` = nivel elegido. Los niveles < nivelInicial se muestran como **Convalidado** en el
perfil, están desbloqueados para repasar y no bloquean el avance. Esto resuelve la pregunta
abierta n.º 3 de REQUERIMIENTOS.md (a confirmar con el cliente).

## Mejoras previstas
- Añadir un ítem de **escucha** y uno de **producción** (repetir frase con el micrófono) por bloque
  cuando el contenido generado incluya audio y diálogos en todos los niveles.
- Calibrar la dificultad real de cada pregunta con los datos de `eventos` (respuestas de alumnos)
  y pasar a un modelo IRT ligero cuando haya volumen.
- Certificado de nivel al aprobar el examen final de cada nivel.

## Fuentes
- [Oxford Placement Test (Wikipedia)](https://en.wikipedia.org/wiki/Oxford_Placement_Test) ·
  [Oxford Online Placement Test](https://elt.oup.com/feature/global/oxford-online-placement/)
- [Cambridge placement test (EF)](https://www.ef.com/wwen/english-tests/cambridge-exams/placement-test/)
- [EF SET explained](https://www.ef.com/wwen/english-tests/efset/) · [Why an adaptive test is the only answer (ClarityEnglish)](https://blog.clarityenglish.com/adaptive-test-answer/)
- [Understanding CEFR adaptive test scores (Equip)](https://help.equip.co/en/article/understanding-cefr-adaptive-test-scores-uj8zx9/)
- [DIALANG (Wikipedia)](https://en.wikipedia.org/wiki/DIALANG)
