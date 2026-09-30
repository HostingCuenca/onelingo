# Estrategia de tutor visual y conversacional

## Hechos del prototipo actual

OneLingo incluye diez tutores GLB y retratos bajo `web/avatar/`. Three.js renderiza un tutor, corrige la pose abierta de los brazos en tiempo de ejecución y añade respiración, cabeza, parpadeo y movimiento de boca. El audio procede de ElevenLabs y la boca responde a la amplitud mediante principalmente `viseme_aa`; por eso parece hablar, pero no forma consonantes y vocales de manera fiable.

Los GLB pesan aproximadamente 21–28 MB cada uno, suman cerca de 250 MB y funcionan solo en web. Se observaron alrededor de 32 morph targets; no se comprobaron 52 expresiones ARKit ni animaciones faciales incrustadas. El código lo reconoce explícitamente como aproximación por amplitud.

## Dirección recomendada

Para una experiencia tipo Praktika/Duolingo con carga rápida, crear un tutor humano 2D reutilizable en Rive:

- capas separadas de cuerpo, cabeza, ojos, cejas, boca, cabello y brazos;
- estados `idle`, `listening`, `thinking`, `speaking`, `correct`, `error`, `celebrate`;
- loops sutiles de respiración, parpadeo, mirada y cabello;
- 15–20 formas de boca reutilizables;
- selección de visemas con tiempos derivados del texto/audio por idioma;
- un runtime liviano, sin generar video durante la conversación.

Higgsfield puede producir hojas visuales coherentes del personaje, expresiones y poses de referencia. Esas referencias deben redibujarse/riggearse como un asset reutilizable; una sucesión de videos generados no resuelve una conversación en tiempo real.

## Piloto mínimo

1. Elegir una tutora y fijar estilo, vista frontal 3/4, paleta y uniforme OneLingo.
2. Generar una hoja de personaje consistente: neutra, sonrisa, escucha, duda, acierto y error; ojos abiertos/cerrados; bocas de visemas.
3. Vectorizar por capas y construir el state machine en Rive.
4. Usar texto del tutor y alineación temporal para alimentar visemas; mantener amplitud solo como respaldo.
5. Integrar en `/avatar` detrás de un flag, sin retirar el prototipo 3D.
6. Medir: peso inicial, primer render, FPS, memoria, tiempo hasta primera voz y sincronización A/V.
7. Tras validar una tutora, derivar los demás personajes e idiomas.

## Conexión pedagógica pendiente

El tutor debe iniciar la conversación y recibir una ficha breve de la actividad actual: idioma, nivel, unidad, objetivos, vocabulario introducido, gramática enseñada, situación, errores recientes y habilidad a reforzar. Debe practicar solo contenido ya enseñado o explicar antes de evaluarlo. Al cerrar, registra evidencia por habilidad y alimenta el camino/repaso.

Los metadatos `tutor` ya existen en el contenido nuevo, pero aún falta transportarlos hasta el iframe/backend. Esta conexión aporta más valor educativo que añadir más personajes visuales antes de terminar el piloto.

## Referencias técnicas

- Duolingo, visemas de personajes: <https://blog.duolingo.com/world-character-visemes/>
- Rive, llamada con Lily: <https://www.rive.app/blog/duolingo-s-ai-powered-video-call-brings-lily-to-life>
- ElevenLabs, streaming con timestamps: <https://elevenlabs.io/docs/api-reference/text-to-speech/stream-with-timestamps>

Estas referencias orientan la arquitectura; hay que validar disponibilidad, costes y compatibilidad por idioma antes de implementar.
