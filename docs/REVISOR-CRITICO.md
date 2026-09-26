# Revisión crítica independiente de integración

Fecha: 2026-09-19. Método: inspección de código, simulaciones mentales de flujos y lectura editorial de 120 preguntas. **No son pruebas humanas ni pruebas de escucha de audio real.** Archivos pueden seguir cambiando durante la integración; verificar cada observación contra su versión final.

## Hallazgos accionables

### P1 · La práctica apoyada puede aumentar el nivel sugerido

`lib/core/biblioteca.dart`, `nivelSugerido`, filtra habilidad/idioma/primer intento pero no `tipo` ni `conApoyo`. Las nuevas guías registran `practica_guiada`; lectura/listening registran `comprobacion_guiada`. Cuatro aciertos viendo una regla o después de leer el guion pueden subir el nivel sugerido.

Simulación: alumno A1 copia estructura de la explicación en las cuatro comprobaciones del nivel 1 → cuatro primeros aciertos → ascenso de recomendación, aunque no se ha comprobado transferencia.

Corrección: usar estas respuestas para actividad y refuerzo, excluirlas del ascenso; crear comprobaciones sin apoyo y con material diferente. La lectura puede legítimamente consultar su texto: el criterio no es ocultarlo, sino distinguir práctica enseñada de evaluación independiente.

### P1 · La marca de apoyo de transcripción se puede borrar

`learning_unit_screen.dart:88` registra el valor actual de `transcript`. Abrir, leer y volver a ocultar produce `conApoyo:false`. Cambiar de unidad y volver reinicia esa bandera aunque el alumno ya conoce el texto.

Corrección: mantener `transcriptSeen` por unidad/intento, acumulativo; no depender de si el panel está abierto. Registrar también vocabulario, repeticiones y evidencias reveladas como apoyo. Nunca anunciar “sin apoyo” solo porque la transcripción está oculta.

### P2 · Vocabulario registra comprensión y duplica evidencia

La pantalla admite `widget.skill == vocabulario`, pero carga reading y registra `skill:comprension`; el ID usa `learn-vocabulario`, distinto de `learn-comprension` para la misma pregunta. Esto puede contar dos veces la misma evidencia de comprensión y no mejora vocabulario.

Corrección: entrada de vocabulario como preparación léxica claramente etiquetada, sin comprobación de lectura duplicada; o crear preguntas léxicas dedicadas y registrar `skill:vocabulario`. Mantener identificador canónico por pregunta si se muestra desde varias rutas.

### P2 · Material de listening revela respuestas por escrito antes de escuchar

Dataset revisado `/tmp/onelingo-listening/listening_units.json`: **80/80 ejemplos de vocabulario son fragmentos literales del pasaje**. En el café se lee el pedido del té/sándwich y la petición de agua antes de las preguntas del audio. El dataset de lectura tiene 0/80 ejemplos copiados del pasaje.

Corrección: ejemplos nuevos en contextos distintos, manteniendo el mismo significado léxico. Tratar toda la unidad como práctica guiada. No usar este resultado como listening independiente.

### P2 · Iniciar audio no equivale a haberlo escuchado

`VozNube.reproducir` retorna después de `_player.play`, no al terminar. `LearningUnitScreen.listen` establece `heard=true` inmediatamente y habilita responder. El registro se llama honestamente `audioIniciado`, pero la interfaz puede parecer que exige escucha completa cuando no lo hace.

Corrección: si se necesita comprobar escucha, medir tiempo y finalización mediante eventos reales del reproductor. Para práctica libre permitir responder temprano, pero no atribuir escucha completa. Mostrar pausa/parada sería útil para pasajes largos; actualmente el botón solo reinicia el audio.

### P2 · Preferencia de animaciones y texto grande en rachas

`streak_card.dart` comprueba `MediaQuery.disableAnimationsOf` pero no el ajuste propio `Efectos.animaciones`. Las fechas usan círculos de 30 px con texto escalable de 11 px: a escala 3, el glifo y altura de línea exceden el contenedor. Esto es un riesgo encontrado por geometría, no una captura visual probatoria.

Corrección: respetar ambas preferencias de animación; adaptar el numeral con `FittedBox` o tamaño de círculo y distribución responsiva. Mantener semántica completa del día fuera de cualquier adaptación visual.

### P2 · Dificultad avanzada todavía poco discriminante

No encontré claves de respuesta claramente falsas ni dos respuestas correctas inequívocas en las 120 preguntas leídas. Sin embargo, varios distractores avanzados contienen absolutos extremos (all, every, never) y la correcta siempre expresa cautela equilibrada. Un alumno puede aprender esa estrategia superficial sin dominar el texto.

Corrección editorial: añadir distractores plausibles con alcance temporal, causal o modal incorrecto, no simplemente absurdos. Incluir actitudes, referentes, orden del discurso y distintos géneros. Los temas avanzados de archivos, encuestas y eficiencia también se repiten entre lectura y listening: útiles para transferencia, no evidencia independiente de cobertura amplia.

## Comprobaciones editoriales reproducibles

- Reading: 20 unidades, 60 preguntas, 2 unidades por nivel 1–10.
- Listening: 20 unidades, 60 preguntas, 2 unidades por nivel 1–10.
- Las 120 citas `evidence` son substrings literales de sus pasajes.
- Claves reading: 15 por cada posición 0–3.
- Claves listening: 14,14,16,16; sin sesgo grave de posición.
- Máximo pasaje listening observado: 789 caracteres.
- Ejemplos de vocabulario copiados literalmente: reading 0/80, listening 80/80.
- Estas verificaciones no certifican CEFR, adecuación acústica, pronunciación TTS, ausencia total de ambigüedad ni resultados con alumnos.

## Simulaciones de recorrido

### Alumno inicial que falla

La enseñanza continúa accesible tras la respuesta; esto corrige la experiencia de “la materia desaparece”. La retroalimentación de cada pregunta identifica evidencia. Pendiente: una respuesta incorrecta no ofrece una segunda variante del mismo objetivo; solo explica y pasa a otra pregunta. Añadir recuperación guiada con ejemplo nuevo, sin borrar el fallo inicial.

### Alumno intermedio que repite

El proveedor conserva primera respuesta y primera fecha; repetir ya no reemplaza ese dato. XP solo en primer registro por ID; la racha puede crecer con práctica repetida, razonable para constancia. La muestra sigue anclada al diagnóstico y no tiene dominio acumulativo por objetivo: no vender el recorrido como adaptación ilimitada todavía.

### Alumno con fuente grande

Las preguntas y explicaciones nuevas están en ListView, sin dock inferior fijo, lo cual reduce cortes. Persisten riesgos en números de calendario. Debe validarse interfaz real a 320 px y escala 2–3, especialmente cabeceras, dos botones en Row y calendario semanal.

## Recomendación de salida

Integrar como **módulos introductorios de aprendizaje guiado**, con gramática siempre visible, sin prometer curso completo ni nivel certificado. Resolver antes los P1 y la duplicación de vocabulario. Mantener pendientes explícitos: producción libre, separación test/práctica, repaso espaciado, cobertura amplia, revisión humana y calibración con alumnado.

## Seguimiento tras correcciones del integrador

Releída la versión posterior: `nivelSugerido` excluye `practica_guiada`, `comprobacion_guiada` y `conApoyo:true`. La contaminación directa del ascenso queda corregida. La pantalla genera ahora preguntas propias de vocabulario y registra su habilidad correcta, con lo que ya no duplica preguntas de comprensión bajo otra habilidad. Las 80 palabras de lectura aparecen en su pasaje; no hay traducciones duplicadas dentro de una unidad.

`transcriptSeen` ya conserva la exposición al cerrar el panel. Queda una precisión de metadatos: cambiar de unidad lo reinicia; ver A → ir a B → volver a A olvida exposición previa. Un conjunto de IDs de unidades vistas evitaría ese caso.

Las nuevas cuatro preguntas léxicas usan el mismo orden de significados que la enseñanza y respuestas A/B/C/D en secuencia. Recomiendo permutación estable de alternativas por pregunta para que el orden no resuelva el ejercicio.

Revisión adicional de las 40 preguntas de gramática: no se detectó una clave inequívocamente incorrecta ni dos alternativas válidas. Las reglas son introductorias y las preguntas no miden producción. Condicionales mixtos aparecen en la referencia B1–B2 de British Council: presentarlos como nivel interno 8 no acredita C1. Permanecen importantes los prerrequisitos que esta entrega todavía no desarrolla (tercer condicional completo antes del mixto, paradigma de participios antes de formas perfectas, contraste de pasados y modales básicos).

## Revisión de los bancos finales y prueba automatizada preparada

Se releyeron las preguntas avanzadas revisadas de niveles 7–10 de ambos bancos. Los distractores ahora plantean interpretaciones plausibles, alcances o causas no justificadas, en vez de depender sistemáticamente de absolutos. No se encontraron claves incorrectas en esta nueva revisión. La dificultad sigue siendo estimación editorial, no calibración CEFR.

Verificado en `/tmp/onelingo-listening/listening_units.json` y en el JSON integrado: **0/80 ejemplos léxicos son ahora fragmentos literales del audio**, corrigiendo el hallazgo anterior de 80/80. Lectura permanece en 0/80. Este criterio mecánico no demuestra por sí solo ausencia de cualquier pista semántica, pero elimina la fuga literal detectada.

Prueba widget creada en `/tmp/onelingo-learner-flow-test.dart`: escenarios con texto a escala 1 y 2, pantalla móvil, consulta de regla, respuesta equivocada, revisión de feedback, regreso a explicación y reentrada conservando resultado. También comprueba que visitar otra vez el resultado no repite XP ni intentos.

Se intentó ejecutar desde el proyecto con `flutter test --no-pub /tmp/onelingo-learner-flow-test.dart`. El comando no llegó al runner por bloqueo del sandbox de este agente al escribir `flutter/bin/cache/engine.stamp.tmp` y `engine.realm`. El integrador puede ejecutarlo con los permisos ya concedidos. **No se atribuye resultado aprobado hasta disponer de la ejecución.**


## Estado final de integración

Consultar PLAN-APRENDIZAJE-2026-09-19.md para el resultado actualizado. La entrega pasó de 20 a 43 temas de gramática y amplió las 50 situaciones a 550 entradas. Se corrigieron transcripción de apoyo persistente entre unidades, orden de opciones léxicas, nivel fijo en agrupación de lecturas, acceso permanente a las cinco áreas y preferencia de animaciones/texto grande en racha. Estos documentos conservan hallazgos de la revisión inicial; no todos siguen pendientes.
