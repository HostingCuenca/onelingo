# Interfaz, navegación y revisión por perfiles

Tres agentes revisaron código con perspectiva A0/A1, A2/B1 y B2/C1; sus conclusiones no constituyen pruebas realizadas por estudiantes humanos. La integración se verificó con tests Flutter y navegación real en localhost.

## Corregido

- Las pantallas de aprendizaje, diagnósticos, práctica, chat y perfil viven dentro del shell de cuatro pestañas. Bienvenida, registro y login siguen como entrada independiente.
- Cambiar pestaña cancela captura y audio. Respuestas de tutor que llegan a una pestaña oculta no arrancan TTS automático.
- Mayor tipografía base, etiquetas de navegación14, instrucciones16; ajustes explícitos en Inicio, camino, biblioteca, gramática y práctica.
- Tarjeta compartida con radio22, borde2 y base4; usada en camino y mascotas y ya por muchas tarjetas de contenido.
- Mascotas transparentes en Inicio, Aprender, Practicar, Perfil, fundamentos, gramática y unidades de lectura/listening.
- Situaciones: tarjetas con altura por contenido, nombres completos, chips sin altura rígida, una columna para texto grande/pantalla estrecha.
- Camino y práctica muestran nivel vigente; mantienen evidencias del diagnóstico para refuerzo.
- Gramática y unidades permiten reintentar errores; primera respuesta e XP conservan comportamiento anterior.
- Entrada a Fundamentos indica siguiente paso y progreso guiado; no lo equipara a dominio.

## Validación

Tests navegación niveles1,5,9 (nivel9 con texto2x), recorrido fundamentos, aprendizaje/errores/reintentos de gramática, tarjetas y accesibilidad de mascotas. Inspección de Inicio, Gramática nivel5 y cambio de pestañas hacia Practicar en navegador.

## Pendiente pedagógico/funcional identificado

- Reanudar unidad/pregunta exacta tras cerrar la app; la navegación entre pestañas conserva el estado de las ramas, pero no sustituye persistencia de ubicación.
- Controles de pausa/velocidad en listening y una pregunta por pantalla en lectura/listening.
- Compositor de tutor multilínea y revisión específica del teclado con las pestañas.
- Pruebas con estudiantes reales y evaluación de retención/transferencia.
- Revisión exhaustiva de cada pantalla secundaria a todas las escalas; esta entrega no afirma haber cubierto toda combinación de dispositivo/idioma.

Disponible localmente; sin despliegue nuevo a producción en esta entrega.
