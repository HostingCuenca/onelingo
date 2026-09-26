# Práctica con tutor IA avatar — 12 septiembre 2026

Apartado web adicional en Practicar → Conocer a los tutores. Ruta `/#/avatar`.
Conserva el chat y los tutores anteriores. Android muestra un aviso de disponibilidad web.

## Implementación

- El tutor recibe el idioma meta activo de OneLingo. Chat, transcripción y voz
  utilizan ese idioma; la galería prioriza tutores recomendados para cada uno
  de los diez idiomas sin ocultar el resto de opciones.
- Los GLB conservan su rig original, pero el visor baja ambos brazos mediante
  los huesos `upperarm_l` y `upperarm_r`. Las tarjetas recortan rostro y torso,
  por lo que la pose abierta de exportación tampoco aparece en la selección.
- Diez modelos reutilizables MPFB/Blender, cinco mujeres y cinco hombres. Cada modelo se descarga al seleccionarlo, no los diez al entrar. Total biblioteca ~244 MB; el primer acceso a un modelo todavía es pesado (~20–25 MB).
- Sofía, Mei, Owen y Kenji tienen prendas con más contraste. Se conservan mangas cortas y posiciones de logos aprobadas.
- Flutter abre un iframe del mismo origen. La sesión se entrega en memoria mediante postMessage verificando origen y ventana; no se añade a URLs ni se guarda en el visor.
- Chat autenticado existente `/chat`, SSE. Rol nuevo `avatar_<id>` para no sustituir los cuatro tutores existentes. Reutiliza contexto de progreso/diagnóstico y conversaciones del backend, además del nivel, sectores y objetivos del cliente. Selector de las 50 situaciones.
- Al recibir `reply` se pide `/voz/stream` con Authorization. ElevenLabs utiliza el modelo ya configurado en el backend y su caché existente. Chrome reproduce MP3 con MediaSource conforme llegan bytes. Navegadores sin MSE MP3 descargan el archivo antes de reproducirlo.
- Web Audio analiza la amplitud del audio reproducido y mueve morphs del avatar. Es sincronización aproximada, **no alineación fonética ni Rhubarb**. Se conserva el prototipo Rhubarb independiente. No se genera un vídeo por respuesta ni se espera a analizar un audio completo.
- Micrófono MediaRecorder, manual o 3 segundos de silencio desde voz detectada; máximo 60 segundos y 15 segundos sin detectar voz. Archivo completo a `/transcribir` (OpenAI). Respuesta automática por defecto; opción para revisar antes de enviar.
- Interrumpir cancela red, audio y micrófono. Salir elimina recursos WebGL. Mensaje explícito al perder conexión. Sin simulación de respuestas cuando falla IA.
- En móvil el rostro permanece visible y el panel inferior se desplaza de forma independiente.

## Validación

- TypeScript correcto. Flutter web release compilado. 68 tests aprobados y uno omitido existente. Analyze: 9 avisos informativos preexistentes fuera de los archivos nuevos, sin errores nuevos.
- Diez tutores renderizados y una petición IA + voz real por cada uno; sin errores JS/API. Audio observado a los 2,7–5,1 s desde enviar texto (incluye la espera hasta observar 0,3 s de reproducción; no es una medición exacta de TTFA y no incluye STT).
- Micrófono con audio de prueba: transcripción íntegra «Hi, I am fine.», captura 7,684 s; audio observado a los 12,722 s desde iniciar captura. Interrupción y modo sin conexión correctos; sin desbordamiento horizontal a 390 px.
- App completa: entrada desde Practicar, sesión en iframe, situación restaurante, respuesta real con voz y cancelación.
- Informes privados de QA: work/browser/avatar-report.json, avatar-mic-report.json, avatar-app-local.json. No contienen tokens.

## Límites de esta primera integración

La animación por amplitud no distingue fonemas; falta alineación más precisa sin introducir espera. La primera descarga de los modelos requiere optimizar texturas/compresión. La sesión conserva historial mientras está abierta y el backend registra conversaciones; no añade todavía nuevas unidades completadas ni puntuaciones al progreso. La transcripción no mide pronunciación ni acredita listening. No se garantiza un TTFA de 1–2 s.

Fuentes editables, texturas y uniformes conservados en `Documents/Codex/2026-09-08/de/outputs/tutor-collection/characters`.

## Publicación verificada

Publicado en https://onelingo.hostingcuenca.com el 12 de septiembre de 2026. Respaldo: `/var/www/onelingo/backups/avatars-20260912-13`. Se actualizaron únicamente lib/ia.ts y lib/voz.ts en backend (sus partes anteriores coinciden con producción), y la web. Entorno, base de datos, panel y APK conservados.

Prueba de producción desde Practicar → tutor Kenji → restaurante: sesión correcta, respuesta «Certainly! Would you like it hot or iced?», voz reproducida e interrupción funcional. Sin errores JavaScript. SHA-256 de main.dart.js, HTML/JS del visor y diez GLB coincide con la compilación local. Informe: `work/browser/avatar-app-production.json`.

## Refinamiento de apertura y latencia — 22 septiembre 2026

- El tutor inicia la conversación al terminar de cargar y vuelve a abrir la escena cuando el alumno cambia de situación. Ya no exige un primer mensaje vacío del alumno.
- El estado visual diferencia pensamiento, preparación de voz y reproducción. Durante audio real muestra cinco barras animadas; respeta `prefers-reduced-motion`.
- El visor limita el render 3D a 30 fps para reservar CPU a red, audio y controles en equipos modestos.
- Producción conserva las mismas diez voces y MP3 progresivo, con `eleven_flash_v2_5` en lugar de `eleven_multilingual_v2`.
- A/B desde el servidor, misma voz y frase: primer byte 1.838 ms con Multilingual v2 y 166 ms con Flash v2.5. Prueba completa en producción: saludo automático, onda durante reproducción y apertura automática de la situación aprobados; primera voz no almacenada en caché observada a 2.634 ms y repetición en caché a 1.958 ms desde iniciar el turno.
- El reproductor expone `replyReadyMs` y `firstAudioMs` para QA. Respaldo: `/var/www/onelingo/backups/avatar-voice-waves16-20260922`.
