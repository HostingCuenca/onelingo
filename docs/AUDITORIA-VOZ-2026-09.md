# Auditoría de voz, escucha y práctica oral — septiembre de 2026

## Alcance y certeza

Inspección del código local el 19 de septiembre. No se consumieron APIs ni se ejecutaron conversaciones reales. No equivale a comprobar lo desplegado en producción ni el micrófono de un dispositivo. La APK se pospone. Avatares fuera de este cambio; MakeHuman se reserva para tutor conversacional posterior.

## Arquitectura existente

Chat: grabación completa (WAV web, M4A nativo) → POST /transcribir → OpenAI (configuración predeterminada gpt-4o-mini-transcribe) → POST /chat con SSE → campo reply completo → GET /voz/stream → ElevenLabs MP3 streaming → reproductor. Existe caché de voz en servidor. El campo reply se entrega antes de terminar correcciones y traducciones; no es streaming de cada frase hacia TTS. No hay entrada de audio incremental ni WebRTC.

Referencias: lib/core/voz.dart, lib/core/api/sync.dart, backend/src/routes/chat.ts, backend/src/routes/voz.ts, backend/src/lib/ia_openai.ts, backend/src/lib/voz.ts.

El chat pide 60 segundos máximos y tres segundos de silencio; el usuario puede detener manualmente. FinPorSilencio es una puerta de amplitud (−50 dB, muestras cada 200 ms, requiere dos muestras activas), no un VAD lingüístico. Voz baja puede parecer silencio; ruido continuo puede impedir terminar hasta el límite. En modo sistema, los límites también dependen del proveedor nativo.

## Corrección conservadora de esta entrega

Los ejercicios de repetición llamaban Oido.escuchar sin configurar duración: defecto de seis segundos, ocho en grabación nube. Se propone/alinea la llamada de lesson_player_screen.dart con el chat: 60 segundos y tres de silencio. Se elimina «Pronunciación clara» y se identifica el resultado como comparación de transcripción. No se cambia core/voz.dart ni las APIs. Validar que el patch esté aplicado antes de presentar este apartado como desplegado.

Importante: en web esta configuración usa la grabadora nube y requiere sesión/micrófono; ya no depende del motor web de reconocimiento para esta actividad. Comprobar el mensaje cuando no hay sesión o permiso. El modo nativo puede seguir recurriendo al motor del sistema si la nube no está disponible.

## Hallazgos prioritarios

1. P1 — Evidencia oral mal interpretada. similitud() compara coincidencia de palabras sin orden; una negación añadida puede mantener puntuación completa. Aprobar al 60 % no demuestra pronunciación, semántica o fluidez. La etiqueta curricular Skill.pronunciacion sigue existiendo y la puntuación sigue alimentando progreso; se necesita separar la evidencia de repetición del dominio acústico. El cambio de texto es una corrección de honestidad, no una reparación del evaluador.
2. P1 — Duraciones inconsistentes entre chat y lección explicaban cortes de ejercicios. El ajuste elimina el límite de seis/ocho segundos de esa llamada, pero no demuestra que todos los cortes queden resueltos.
3. P2 — Listening marca played al iniciar reproducción, no al completar audio. played=true no equivale a escucha completa. Registrar inicio, final, cancelación, reintentos y revelado de transcripción. Un fallo de reproducción no debe contar como error del alumno.
4. P2 — Fin de turno basado en volumen requiere pruebas de voz suave, ruido y distintos dispositivos. Mantener parada manual y considerar un modo manual para personas que necesitan pausas largas. No prometer 1–2 segundos desde fin real de habla cuando el detector espera tres segundos antes de enviar audio.
5. P2 — Grabación/subida/STT siguen siendo secuenciales. La salida ya transmite audio; no atribuir toda la demora a TTS ni migrar sin medir. Instrumentar fin de voz, fin de captura, inicio/fin STT, reply disponible y primer audio audible.
6. P2 — Estados de captura y transcripción deben impedir reentradas. Probar doble pulsación, detener mientras empieza grabación, salir durante STT y cambiar de pantalla. El helper tiene identificadores de sesión, pero hace falta validar cada interfaz consumidora.
7. P2 — La memoria textual del tutor es útil para gramática y objetivos, no para certificar listening o pronunciación. El prompt backend lo reconoce; la presentación y el progreso deben respetarlo.

## Enseñar, practicar y evaluar por separado

### Enseñar a escuchar

Presentar vocabulario esencial y contexto; ofrecer audio lento, repetición y transcripción opcional. Registrar estas ayudas sin penalizar al alumno. Explicar la evidencia de la respuesta, sonidos reducidos y expresiones cuando corresponda.

### Práctica de listening

Texto oculto inicialmente, preguntas de significado, detalle e intención; no solo dictado. Repeticiones libres y feedback inmediato. Variar ejemplo y voz sin cambiar simultáneamente todos los factores de dificultad. Una respuesta correcta con transcripción es práctica asistida, no prueba independiente de escucha.

### Test de listening

Ítems nuevos y sin solución previa; reglas visibles para repeticiones y ayudas. Separar problemas técnicos de errores lingüísticos. No atribuir nivel por una única frase. Comparar varias evidencias por subcompetencia y nivel.

### Speaking

Repetición guiada puede comprobar palabras reconocidas; producción libre necesita valorar tarea comunicativa, gramática y vocabulario. Pronunciación/entonación requieren evidencia acústica y criterios propios. La transcripción por sí sola no permite esas conclusiones. No subir el nivel por conversar sin recibir correcciones.

## Estado de lectura y cobertura

La secuencia curricular sí contempla vocabulario → frases → escucha → práctica → repaso. No obstante, los huecos gramaticales se generan eliminando la palabra central de una frase (curriculum.dart), lo que no garantiza medir el objetivo gramatical de la unidad.

Biblioteca inglesa inspeccionada: 116 preguntas, con 36 de lectura (18 pasajes), 30 de listening, 20 de gramática, 20 de escritura y 10 de vocabulario. Por nivel son solo tres listening, dos gramática, dos escritura y un vocabulario. Lectura tiene dos por nivel excepto nivel cinco con 18. Este banco es una base de práctica, no una calibración suficiente de dominio o equivalencia MCER. Ampliar variantes y verificar cobertura antes de endurecer progresión o recomendar certificaciones.

## Criterios de aceptación

- Chat y lección permiten una intervención de 15–25 segundos sin corte a los seis/ocho segundos.
- Pausas de 0,5, 1,5 y 2,8 segundos conservan un turno; más de tres segundos termina conforme a la configuración y muestra procesamiento.
- Probar voz suave, ventilador, auriculares y altavoz en Android físico y navegador. Documentar dispositivo/navegador y resultado.
- Parada manual produce un solo envío. Cancelar/salir descarta resultado tardío y no reproduce audio de la sesión anterior.
- Sin permiso/sesión/red se informa causa y se permite continuar/reintentar sin atribuir error lingüístico.
- Negación añadida, orden invertido y omisión importante no se presentan como buena pronunciación. El evaluador actual todavía necesita una corrección adicional para no premiar coincidencia engañosa.
- No contabilizar audio cancelado/fallido como escucha completa; diferenciar ayudas de evaluación independiente.
- Para lectura/listening, evaluar con un texto o audio nuevo después de enseñar; el mismo ítem repetido no demuestra transferencia.
- Registrar percentiles de latencia con timestamps reales; los tests simulados de audio no validan micrófonos, permisos, eco ni primer audio audible.

## Pruebas existentes y límites

 test/silencio_test.dart cubre lógica de pausa; test/voice_modules_test.dart usa un plugin de audio simulado para streaming y cancelación al preparar. Son útiles pero no sustituyen pruebas físicas. No se realizaron llamadas pagadas en esta auditoría.
