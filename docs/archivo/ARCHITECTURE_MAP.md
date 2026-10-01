# Mapa técnico rápido

| Área | Tecnología | Archivos principales |
|---|---|---|
| App | Flutter, Riverpod, GoRouter | `lib/main.dart`, `lib/app/`, `lib/features/`, `lib/shared/` |
| Estado/sync | Riverpod, SharedPreferences, HTTP | `lib/core/state/providers.dart`, `lib/core/api/sync.dart` |
| Currículo nuevo | JSON esquema 2 + dominio Dart | `lib/core/aprendizaje/`, `assets/contenido/*/ruta/` |
| Contenido legado | JSON y catálogos Dart | `lib/core/content/`, `assets/contenido/*/nivel-*.json` |
| Diagnóstico | motor local + API | `lib/core/diagnostico.dart`, `lib/features/onboarding/diagnostico_screen.dart`, `backend/src/routes/diagnostico.ts` |
| Tutor de texto | Flutter + backend IA | `lib/features/chat/chat_screen.dart`, `backend/src/routes/chat.ts`, `backend/src/lib/ia*.ts` |
| Voz | captura Flutter/web + OpenAI STT + ElevenLabs TTS | `lib/core/voz.dart`, `lib/core/api/sync.dart`, `backend/src/routes/voz.ts`, `backend/src/lib/voz.ts` |
| Tutor 3D web | iframe, Three.js, GLB | `lib/features/avatar/avatar_screen_web.dart`, `web/avatar/` |
| Tutor Android | pantalla de reserva | `lib/features/avatar/avatar_screen_stub.dart` |
| Backend | Node.js, TypeScript, Fastify, PostgreSQL | `backend/src/app.ts`, `backend/src/routes/`, `backend/src/lib/` |
| Panel | frontend administrativo separado | `panel/` |
| Herramientas de contenido | Node/TypeScript + Gemini/OpenAI | `tools/contenido/` |
| Validación educativa | Python + Flutter tests | `tools/validar_ruta.py`, `test/ruta_*` |

## Flujo de voz del avatar actual

```text
getUserMedia
→ MediaRecorder (WebM/Opus, M4A o WebM)
→ VAD local por amplitud y 3 s de silencio
→ archivo completo multipart POST /transcribir
→ OpenAI gpt-4o-mini-transcribe
→ POST /chat
→ OpenAI gpt-4.1-mini con tokens en streaming
→ reply temprano
→ GET /voz/stream
→ ElevenLabs eleven_flash_v2_5 MP3 streaming
→ elemento HTMLAudioElement
→ analyser de amplitud
→ morph targets aproximados en Three.js
```

La transcripción espera al archivo completo. El LLM y el TTS sí tienen rutas de streaming. El movimiento de boca no conoce los fonemas.

## Rutas de producto clave

- `/bienvenida`, `/onboarding`, `/diagnostico`, `/inicio`
- `/aprender`, `/fundamentos`, `/ruta/:nivel`, `/gramatica`, `/biblioteca`
- `/practicar`, `/situacion/:id`, `/chat`, `/avatar`, `/tutores`
- `/perfil`, `/errores`, `/planes`
