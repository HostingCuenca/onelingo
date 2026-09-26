# Diseño vigente de OneLingo

Decisiones del usuario, 8 de septiembre de 2026. Aplicar al continuar el diseño de la app.

- Las acciones principales ocupan el ancho disponible. Evitar botones pequeños aislados con espacio vacío a su lado; usar una fila equilibrada o botones completos apilados.
- Seis actividades diarias se presentan en tres columnas y dos filas. Mantener lectura multilínea y objetivos táctiles cómodos.
- Tarjetas de situaciones más grandes, con fotografías más altas. Conservar sus fotografías originales.
- Las ilustraciones complementan las situaciones y lecturas: estilo editorial pintado, textura fina de papel, luz cálida, lavanda/índigo/menta/melocotón, personajes adultos. No sustituir las fotos de las cards.
- Biblioteca de dos ilustraciones horizontales por cada una de las 50 situaciones, sin texto incrustado; escenas diferentes con continuidad visual.
- Iconos propios de navegación y habilidades, vectoriales para mantener nitidez.
- Evitar huecos accidentales. Conservar separación necesaria para legibilidad: no llenar cada espacio con decoración.
- Sin conexión con el servidor: avisar claramente, conservar el texto y permitir reintentar. No simular respuestas de IA ni atribuir puntuaciones inventadas.
- La práctica automática usa biblioteca y la escritura usa evaluación con IA. El modo sin conexión completo queda para una fase futura.
- Diez niveles internos: 1–2 A1, 3–4 A2, 5–6 B1, 7–8 B2, 9–10 C1; nivel 0 Fundamentos. Equivalencia curricular orientativa, no certificación.

## Feedback durante la práctica

- Feedback consistente entre biblioteca, diagnóstico y lecciones: sello animado y explicación visibles después de responder.
- Acierto: confirmación breve. Error: señal suave y «Vamos a repasarlo», sin castigos visuales. Finalización: celebración de la práctica realizada; no implica dominio perfecto.
- Tres efectos de Kenney Interface Sounds (CC0), empaquetados y reutilizados; no generar efectos con ElevenLabs ni hacer llamadas de IA para sonidos.
- Volumen moderado, sin música de fondo ni sonidos al cargar páginas. Al reproducir voz se detienen los efectos; al confirmar una respuesta se detiene la voz antes del efecto.
- Silenciador a mano y preferencias persistentes de sonidos, animaciones y vibración en Perfil. Movimiento reducido del sistema desactiva los nuevos efectos visuales y el confeti.
- La explicación textual y los controles funcionan incluso si el navegador bloquea el sonido o si se desactivan efectos.

### Movimiento y carga de actividades · septiembre 2026
- Carga: iconos de lectura, escucha, conversación y escritura en órbita, con bloques provisionales que anticipan la estructura de la pregunta. No retrasar contenido para completar una animación.
- Revisión escrita: versión compacta del mismo indicador. Conservar respuestas y mensajes de error/reintento.
- Acierto: destello breve de estrellas verdes alrededor del sello; finalización en morado. No cubrir el texto ni bloquear Continuar.
- Precargar y reutilizar los tres efectos; no solicitar un seek antes de cada reproducción, ya que ReleaseMode.stop devuelve el audio al inicio. Mantener cancelación de voz pendiente para no solapar listening.
- Respetar sonidos desactivados y movimiento reducido del sistema/app; detener el controlador al salir.

### Correcciones verificadas en producción
- Diagnóstico: el feedback no debe quedar al final de la lista de preguntas. Usar FeedbackDock encima de Continuar/Siguiente, con desplazamiento propio para correcciones extensas.
- Aplicar el mismo panel a biblioteca y lecciones; comprobar a 390 × 640 y con texto grande.
- La carga incluye un libro-personaje que se balancea y parpadea, iconos coloreados con órbita y rebote. La prueba debe verificar cambio de posición entre fotogramas, no solo la existencia de un controlador activo.

## Gramática y temarios: reducir carga visual (19 septiembre 2026)

Mostrar una actividad y un tema a la vez. El catálogo completo se consulta desde «Temario», en una hoja con selección de nivel y solo sus temas. Evitar abrir con una lista de los 43 temas, un gran encabezado decorativo y toda la lección desplegada.

Secuencia de gramática: Aprende → Crea → Prueba. La idea clave y ejemplos bilingües ocupan el primer paso; consejos adicionales son desplegables. La producción escrita y comprobación tienen pantallas de contenido separadas. En pruebas se muestra una pregunta, su retroalimentación y luego la siguiente; consultar la explicación conserva las respuestas y el borrador de sesión. Conservar colores OneLingo, botones amplios y navegación con texto escalado. Las transiciones suaves respetan reducción de movimiento.
