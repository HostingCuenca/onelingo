# Micrófono del chat: cierre por silencio

11 de septiembre de 2026.

## Causa

El chat web estaba excluido de `_puedeGrabar()` y dependía del motor SpeechRecognition. El resultado `finalResult` se enviaba inmediatamente al tutor. El plazo `listenFor=8s` era un máximo, no una garantía: el navegador podía cerrar antes de completar la frase. Aumentar `pauseFor` por sí solo no garantiza continuidad (https://pub.dev/packages/speech_to_text/example).

## Cambio

El chat autenticado usa el grabador existente también en web: WAV PCM, canal único solicitado, configuración inicial 16 kHz (el navegador puede negociar otra frecuencia; la cabecera WAV recoge la real). Se carga el archivo completo en `/transcribir`, que ya admite WAV. No se utiliza SpeechRecognition como fallback silencioso en este chat: si no puede abrirse la grabación, se muestra error.

El alumno dispone de 60 segundos máximos por turno y botón «Detener y enviar». Se vigila actividad de audio cada 200 ms, umbral conservador -50 dBFS, y se cierra tras 3 segundos sin actividad después de empezar a hablar. Dos muestras activas evitan iniciar por un único clic. El silencio inicial no finaliza el turno antes del máximo. No es un detector lingüístico de voz: ruido sostenido puede impedir el cierre automático; el botón manual sigue disponible.

El PCM puede representar silencio absoluto como -Infinity dBFS. Se considera silencio válido; NaN/+Infinity no deciden el cierre. La prueba de navegador detectó y corrigió este caso.

Al cerrar se muestra «Transcribiendo tu respuesta…». Se bloquea un segundo envío mientras se graba o transcribe. El texto completo se envía al tutor y se conserva la reproducción automática progresiva de la respuesta. Al abandonar el chat se cancelan temporizadores/captura y se ignoran transcripciones tardías. El blob temporal web se libera tras leerlo.

La pausa elegida de 3 segundos forma parte de la espera antes de transcribir. «Detener y enviar» evita esa espera. No se promete TTFA de 1–2 segundos medido desde el último sonido con esta configuración.

## Verificación

Seis tests Flutter aprobados (silencio, pausas intermedias, respuestas largas, y regresiones de voz/chat), análisis de cinco archivos sin incidencias y compilación web correcta.

Chrome con micrófono virtual: fixture de voz sintetizada «Hi», pausa intermedia de 1,5 segundos, «I am fine», silencio. Captura real por AudioWorklet y multipart WAV: 7,125 s totales, unos 3,15 s desde la última actividad hasta el cierre. Una única transcripción. También se comprobaron cierre manual y cancelación sin subida ni canales de micrófono activos. Primero se aislaron servicios con respuestas simuladas; después se comprobó STT, LLM y reproducción con APIs reales y sin deshabilitar la política de autoplay del navegador. La frase completa llegó al chat y hubo evento de reproducción de respuesta. Es una prueba con entrada virtual; no sustituye validación del micrófono físico del usuario ni prueba de todos los navegadores.

Scripts e informes de QA: `work/browser/mic-check.mjs`, `mic-fixture.mjs`, `mic-report.json`. No incluyen claves en los informes. Publicación: web, sin cambios de backend ni reinicio de otros servicios. Backup confirmado `/var/www/onelingo/backups/mic-silence-20260911`.

Producción verificada: https://onelingo.hostingcuenca.com, captura de 6,997 s y cierre 3,187 s después de la última actividad. STT real: «Hi, I am fine.»; respuesta hablada automática confirmada sin pulsar reproducción. No hubo errores de página. Los márgenes de tiempo anteriores se conservan para ejercicios nativos sin control por silencio.
