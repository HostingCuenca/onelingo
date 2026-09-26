# Voz progresiva: primera fase, 10 septiembre 2026

Publicado en https://onelingo.hostingcuenca.com. Respaldo servidor: /var/www/onelingo/backups/voice-stream-20260910.

## Implementación

- POST /chat negocia SSE con Accept: text/event-stream; conserva JSON para clientes anteriores.
- Una llamada a gpt-4.1-mini con Structured Outputs y stream:true. Emite `reply` cuando se completa la primera propiedad JSON, antes de traducción, correcciones y sugerencias. No transmite palabras sueltas al sintetizador.
- El cliente inicia la voz una sola vez al recibir `reply`; al recibir `final` completa la interfaz. No hay segunda llamada de evaluación.
- GET /voz/stream consume el endpoint HTTP /stream de ElevenLabs y entrega MP3 incremental mediante Readable. Conserva eleven_multilingual_v2 y las voces existentes.
- Caché compartida por modelo/voz/texto, deduplicación de generaciones simultáneas y escritura temporal con rename únicamente al completar el audio. Un stream interrumpido no publica una entrada incompleta.
- El chat usa UrlSource también en nativo: ya no necesita descargar a un archivo antes de reproducir esta ruta. La biblioteca y otras actividades mantienen su mecanismo anterior.
- Timeout y cancelación del stream OpenAI al salir del chat, protección contra reproducciones pendientes al detener voz. No constituye todavía conversación full-duplex con interrupción automática por voz.
- Historial enviado limitado a los últimos 30 mensajes para respetar el límite existente del backend.
- Métricas backend: chat_reply_ready, chat_complete, voz_first_chunk. No contienen el texto del usuario.

## Verificación

- TypeScript: typecheck correcto.
- Flutter: análisis de voz, pantalla chat y prueba de streaming sin incidencias; sync.dart mantiene avisos de estilo de llaves.
- Backend: 4 pruebas (JSON escapado/incompleto, SSE fragmentado/cortado, audio incremental/caché/corte, entrega HTTP temprana y compatibilidad/autenticación).
- Flutter: prueba SSE incremental y seis pruebas de sincronización/feedback correctas.
- Build web release correcto. Avisos existentes de flutter_tts en ensayo Wasm; artefacto publicado JavaScript.
- Chrome headless contra producción con usuario QA, sin errores de página y una sola reproducción de respuesta.

Tiempos de UN turno real, desde pulsar enviar texto:

| Evento | ms |
|---|---:|
| POST /chat iniciado | 207 |
| GET /voz/stream iniciado | 2555 |
| POST /chat terminado | 3682 |
| Evento playing del navegador | 3785 |
| Descarga /voz/stream terminada | 3870 |

La síntesis se inició 1127 ms antes de terminar el JSON. La reproducción comenzó antes de terminar la transferencia. No es una comparación A/B ni una medición desde el último sonido del alumno. El evento playing confirma inicio del reproductor; no mide la salida acústica física del dispositivo.

## Pendiente y límites

Aún se espera la propiedad reply completa; no se sintetiza desde su primera frase/token. Web Speech, sus pausas y el temporizador de grabación Android no se modificaron. No se activó STT realtime ni WebSocket TTS ni Flash. Android comparte el código modificado, pero no se compiló/publicó APK ni se verificó en un dispositivo en esta fase. El objetivo 1–2 s no se ha alcanzado en la muestra. Próximas decisiones deben apoyarse en más muestras y separación de fin de voz, primer texto y primer audio.

# Segunda fase: módulos de audio, 11 septiembre 2026

Publicada la web; respaldo `/var/www/onelingo/backups/voice-modules-20260911`. No cambió el backend, los proveedores ni las voces.

- Voz y VozNube usan reproducción progresiva por defecto: listening del diagnóstico, biblioteca/práctica personalizada, lecciones, diálogos, frases y reproducción manual del tutor.
- Los archivos locales ya existentes se consultan antes de abrir una URL; la caché compartida del servidor sigue evitando regeneraciones.
- Cancelar una reproducción pendiente devuelve false: no debe acreditarse como una escucha válida. La biblioteca comprueba también que el resultado corresponda a la misma pregunta.
- Al desmontar una actividad de lección se detienen voz y micrófono. Se cancela una grabación abandonada sin iniciar su transcripción; los resultados tardíos de sesiones anteriores se descartan.
- Los callbacks de reproducción automática verifican que el ejercicio siga montado.

Validación: análisis Flutter sin incidencias en archivos modificados; 26 pruebas de voz, chat, diagnóstico y biblioteca correctas. Build web release correcto. Navegador Chrome contra la compilación local y después contra producción: biblioteca, diagnóstico (primera pregunta y siguiente listening) y lección reproducen por `/voz/stream`, sin errores de página ni peticiones a la antigua ruta `/voz` en esos recorridos.

Muestras puntuales en producción desde activar Escuchar hasta evento `playing`: biblioteca 364 ms y diagnóstico 1747 ms. La reproducción automática de la lección también fue verificada, sin medir un tiempo comparable desde clic. Estas cifras pueden incluir caché y no representan promedios ni la latencia de una conversación completa. No se modificaron VAD, tiempos de silencio, STT ni se publicó APK.
