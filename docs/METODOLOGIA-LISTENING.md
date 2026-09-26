# Listening inglés: unidades originales y límites de evaluación

Fecha: 19-09-2026. Contenido original OneLingo; no se copiaron preguntas ni guiones de exámenes. No se generó audio ni se llamó a APIs de pago.

## Entregable y alcance

`listening_units.json`: esquema version 1, 20 unidades, dos por cada uno de los diez niveles internos, 60 preguntas y 80 entradas de vocabulario. Cada unidad contiene objetivo, cuatro palabras del guion, ejemplos nuevos en otros contextos, estrategia de escucha, monólogo TTS y tres preguntas. Las preguntas combinan idea principal, detalle e intención/inferencia según dificultad. Cada corrección incluye evidencia literal y explicación en español. Las opciones correctas están repartidas entre las cuatro posiciones; conservar el vínculo con answerIndex al barajarlas.

Niveles 1–3: guiones de 39–55 palabras sobre acciones cotidianas. Nivel 4: transición de 62–64 palabras con alternativas e instrucciones. Niveles 5–10: 80–122 palabras con contraste, condiciones, cautela, intención, límites de evidencia y supuestos. Estos números son decisiones de diseño de OneLingo, no límites oficiales de CEFR. Tampoco existe calibración estadística que permita equiparar los diez niveles a certificaciones.

## Fundamentos consultados

British Council distingue predicción, comprensión global, detalles, marcadores del discurso e inferencia. La propuesta toma esas habilidades como objetivos distintos: una pregunta de detalle correcta no demuestra comprensión de todo el mensaje. [Five essential listening skills](https://www.britishcouncil.org/voices-magazine/five-essential-listening-skills-english-learners).

El catálogo A2 de British Council combina preparación, grabación y actividades de comprensión. Aquí se adopta esa separación funcional: preparar vocabulario, escuchar y comprobar; no se importan textos ni preguntas. [A2 listening](https://learnenglish.britishcouncil.org/free-resources/listening/a2).

La evaluación debe distinguir lo que hace el oyente al comprender de la tarea elegida para observarlo. No se puede identificar una habilidad completa con una única respuesta de opción múltiple. [British Council: Assessing Listening](https://www.britishcouncil.org/exam/english/aptis/research/projects/assessment-literacy/listening).

Los descriptores del Consejo de Europa sirven como referencia de competencias comunicativas. Los niveles internos de este banco son una secuencia editorial, no una conversión validada al marco. [CEFR descriptors](https://www.coe.int/en/web/common-european-framework-reference-languages/cefr-descriptors).

## Secuencia pedagógica y evidencia

1. Preparación: objetivo en español, cuatro palabras con traducción y ejemplos que no reproducen respuestas del guion, estrategia breve.
2. Primera escucha: guion oculto; centrarse en el mensaje general. Ofrecer repetición y modo lento como apoyo, registrando su uso.
3. Comprobación guiada: preguntas, explicación tras contestar y evidencia literal. El guion completo puede verse después como material de aprendizaje. El acceso a soluciones antes de acabar las otras preguntas hace que estas también sean asistidas.
4. Repaso: escuchar otra vez siguiendo el texto, identificar qué parte no se reconoció y practicar. No acumular dominio por repetir las mismas tres respuestas.
5. Transferencia futura: una unidad nueva, no previamente enseñada, y reglas explícitas de ayuda. Solo con ítems nuevos y varias evidencias tendría sentido una prueba independiente.

**Estas unidades se registrarán como `comprobacion_guiada` y se excluirán del ascenso de nivel**, incluso si el guion permaneció oculto: se han enseñado vocabulario/contexto y los ítems no están calibrados. Nunca llamar a estos resultados prueba certificada. El ocultamiento debe aplicarse también a semántica/accesibilidad para no exponer el guion a lectores de pantalla antes de responder, manteniendo alternativas accesibles honestamente etiquetadas como lectura asistida.

## Voz sintética, acento y velocidad

Todos los guiones están escritos para una sola voz, como mensaje, aviso o exposición; no simulan turnos entre varias personas. Usar el runtime y caché ElevenLabs existente. No se prepararon audios aquí y no se ha verificado su duración, pronunciación ni prosodia.

La voz sintética puede ser excesivamente clara, regular o pausada. Comprenderla no garantiza entender conversación espontánea con reducciones, solapamientos o ruido. Los guiones avanzados evalúan razonamiento verbal limitado; no sustituyen discursos largos o interacción real. La voz, el acento y la velocidad pueden alterar la dificultad sin cambiar el texto.

En aprendizaje: repetición libre y velocidad lenta opcional. En futura evaluación: fijar versión del guion, voz/modelo, velocidad y política de repeticiones; registrar cambios. No asignar acentos por apariencia o etnia del tutor. No aumentar velocidad y complejidad a la vez. Validar primero con voces claras y después variar acentos reales declarados por el proveedor, revisando los audios. Una ralentización mecánica no equivale automáticamente a habla naturalmente más lenta.

## QA ejecutado

`validate.py` comprueba esquema, veinte unidades, dos por nivel, sesenta preguntas, IDs únicos, rangos de extensión, cuatro opciones diferentes, índices válidos, evidencia literal y presencia de cada palabra en el guion. Verifica que los ejemplos no estén copiados del pasaje. Resultado: `qa-result.json`, PASS. Se corrigió una evidencia después de ajustar un guion; se volvió a validar.

La revisión editorial comprobó las claves contra el guion. El validador no demuestra ausencia de ambigüedad, calidad del audio o idoneidad CEFR; requiere revisión de docente humano y prueba con alumnos antes de usarlo para decisiones de nivel. Algunos distractores iniciales son deliberadamente sencillos; no sirven para discriminar niveles superiores.

## Perfiles simulados y pruebas propuestas (no participantes reales)

Estos perfiles son casos de prueba de producto; **no se ha ejecutado un estudio con seres humanos ni se reportan resultados inventados**.

- Principiante que sabe leer las palabras pero necesita audio lento: comprobar que puede repetir sin recibir una falsa etiqueta de bajo dominio por usar apoyos.
- Alumno intermedio con buena idea global y fallos de detalles: respuestas guionizadas aciertan pregunta global y fallan hora/condición; comprobar feedback diferenciado, sin ascenso automático.
- Alumno avanzado que detecta matiz pero desconoce una palabra: no penalizar todo el pasaje por un fallo; mostrar evidencia local tras respuesta y conservar resultado por objetivo.
- Alumno que memoriza el banco: repetir respuestas exactas no genera nueva evidencia de dominio ni ascenso.
- Alumno con discapacidad auditiva o sonido no disponible: permitir alternativa textual identificada como lectura asistida, no etiquetarla listening independiente.
- Usuario interrumpido: salir durante descarga, cambiar unidad y volver no reproduce un audio anterior; errores de red no suman fallos lingüísticos.

Pruebas humanas posteriores: revisar pronunciación TTS de vocabulario y números, comprobar que ninguna entonación revela artificialmente la respuesta, preguntar por ambigüedades, registrar tiempos y ayudas, y analizar qué distractores nunca se eligen. Con pocos casos solo se detectan problemas de usabilidad; no se proclama calibración psicométrica.
