# OneLingo · Plan de trabajo

Estado al 3 sep 2026. Orden pensado para que el cliente pueda **probar flujos
completos cuanto antes** y el desarrollo avance sin rehacer nada.

## Hecho (fase 1 · demo navegable)
- [x] Proyecto Flutter (Android/iOS/web), tema con la paleta del logo, navegación con 4 pestañas.
- [x] Modelo de datos y reglas del curso: 10 niveles × 100 lecciones, desbloqueo progresivo, examen final 65 %, programa completado.
- [x] Reproductor de lección con 8 tipos de ejercicio (flashcard, opción múltiple, hueco, ordenar, dictado, parejas, imagen, repetir).
- [x] Práctica libre: 50 situaciones con foto, conversación libre, 4 tutores, chat con IA simulada que corrige errores.
- [x] Sección de errores, perfil/progreso, prueba gratuita de 1 h medida por uso, planes $20/$30/$40.
- [x] **Login demo** con 5 usuarios de prueba (contraseña `1234`) en distintos puntos del camino.
- [x] 36 fotos CC0/CC BY (Openverse) para situaciones, unidades, tutores y ejercicios; créditos en `assets/img/fotos/CREDITOS.md`.
- [x] Currículo alineado a CEFR/Oxford (`CURRICULO.md`); Nivel 1 con contenido real.
- [x] **10 idiomas**: plan por idioma con exámenes oficiales y manuales (`CURRICULO-IDIOMAS.md`); Nivel 1 unidades 1-6 reales en los 9 idiomas restantes con romanización (pinyin, Hepburn, RR, cirílico translit.) en `lib/core/content/idiomas.dart`.
- [x] Corre en web (`build/web`) y en el simulador iOS.

## Sprint 1 · Contenido real y flujos completos (1-2 semanas)
Objetivo: que un usuario haga el Nivel 1 completo con contenido de calidad y voz.
- [x] **Pipeline de contenido** (`tools/contenido`, ver `PIPELINE.md`): plan curricular de 200 unidades (`content/plan-curricular.json`), generador con Claude (salida estructurada Zod, directo o Batches al 50 %, reanudable), validador, empaquetador y cargador en la app (`contenido_json.dart`). Semilla del Nivel 1 exportada para los 10 idiomas en el mismo formato.
- [ ] **Ejecutar la generación** (requiere `ANTHROPIC_API_KEY`): `npm run generar -- --todo --batch` → 2 000 unidades ≈ $52 por Batches con claude-opus-5; luego `validar`, muestreo humano y `empaquetar`.
- [x] `dialogo`, `errores_tipicos` y `examen` del JSON en la app: paso "Antes de empezar" (gramática + errores) en Frases, diálogo de situación en Escucha/Repaso, y el examen del nivel prioriza las preguntas generadas.
- [x] **Voz (TTS)**: `flutter_tts` con locale por idioma en flashcards, dictado y chat (`lib/core/voz.dart`).
- [x] **Reconocimiento de voz**: `speech_to_text` en "Repite en voz alta" (compara lo dicho con la frase y puntúa) y en el micrófono del chat (dicta y envía). Permisos iOS/Android añadidos. Nota: el simulador iOS no tiene entrada de audio; probar en iPhone real o Chrome.
- [x] Prueba de nivel adaptativa en el registro y en Perfil (`PRUEBA-NIVEL.md`): autoevaluación + bloques de 3 preguntas que suben/bajan de nivel, ≤ 24 preguntas; niveles inferiores convalidados.
- [ ] Examen final con 30 preguntas y cooldown configurable; pantalla "no aprobado" → repaso de errores.
- [x] **Efectos tipo Duolingo** en los ejercicios: panel de feedback que sube con rebote, icono elástico, opciones con rebote al tocar, barra de progreso animada, insignia de combo (x2, x3…), sonidos (acierto/fallo/lección completada) + vibración, confeti con la paleta del logo al terminar (`lib/core/efectos.dart`, `lib/shared/confeti.dart`).
- [ ] Ilustraciones/fotos por unidad para los 10 niveles (misma fuente Openverse + revisión manual) y avatar animado simple de los tutores.
- [ ] Recordatorio diario (notificación local) y racha.

## Sprint 2 · Backend y cuentas (2-3 semanas)
- [x] `backend/` (Fastify + Postgres + zod, puerto 8091): registro/login, sincronización del progreso completo, errores, exámenes, eventos; endpoints de administración.
- [x] **Panel de administración** `panel/` (Vite + React, puerto 5176): resumen (KPIs, por idioma/nivel, exámenes, errores, actividad), lista de alumnos con búsqueda y detalle por alumno (progreso por nivel, errores, actividad, datos sincronizados). Login admin/1234.
- [x] La app sincroniza sola: registro/login demo crean el usuario, cada cambio de progreso se sube (offline-first, 2 s de agrupación) y se registran eventos (lección completada, examen).
- [ ] Pendiente del backend: matrículas por idioma, trial medido en servidor, catálogo de contenido servido por API, contraseñas reales.
- [x] Autenticación real: correo + contraseña (bcrypt), verificación y recuperación por correo (SMTP o bandeja local visible en el panel), Google Sign-In (backend verifica el idToken; IDs por configurar, ver `AUTENTICACION.md`). Los usuarios demo siguen disponibles en el login.
- [ ] Apple Sign-In (obligatorio en App Store si hay Google) y borrado de cuenta.
- [x] **Proveedor Gemini** añadido en backend y pipeline (`IA_PROVEEDOR=gemini`, `gemini-flash-latest`). La clave actual es de **nivel gratuito: 20 peticiones/día** (se agotó en la primera prueba de generación); para generar contenido y servir el chat hay que activar facturación en el proyecto de Google AI Studio o usar la clave de Anthropic.
- [x] **IA real**: `POST /chat` arma el prompt (tutor + perfil de nivel + situación + idioma nativo) y llama a Claude con salida estructurada `{reply, romanizacion, traduccion, corrections[], suggestions[]}`; cada turno se guarda en `conversaciones` (panel → Conversaciones IA). La app usa el servidor y cae al simulador si no hay clave. Falta: `ANTHROPIC_API_KEY` en el backend y límite de turnos/día por plan.
- [ ] Sincronización offline-first (caché local + cola de eventos).
- [ ] Panel de administración mínimo (ver usuarios, contenido, métricas) reutilizando el panel de Pollos.

## Sprint 3 · Monetización y tiendas (2 semanas)
- [ ] Pagos: Apple/Google in-app (RevenueCat o nativo) + Stripe en web. Entitlements por número de idiomas.
- [ ] Selección de idiomas dentro del plan, cambio de idioma, progreso independiente por idioma.
- [ ] Iconos, splash, política de privacidad, términos; publicación en TestFlight y Play Internal Testing.
- [ ] Analítica de producto (eventos clave: lección completada, examen, conversación, conversión trial → plan).

## Sprint 4 · Escala a 10 idiomas (continuo)
- [ ] Confirmar la lista de 10 idiomas con el cliente y generar contenido por idioma con el pipeline.
- [ ] Interfaz de la app traducida a los idiomas nativos soportados (l10n).
- [ ] Voces neuronales por idioma (ElevenLabs / Azure / Google) para los tutores.
- [ ] Certificados por nivel, ranking/liga semanal, amigos (opcional, tipo Duolingo).

## Preguntas abiertas para el cliente (bloquean sprints 2-4)
Ver `REQUERIMIENTOS.md` · "Preguntas abiertas": lista de idiomas, definición de la hora gratis, reintentos del examen, prueba de nivel vs. niveles anteriores, cambio de idiomas en el plan, pasarela de pago.

## Cómo probar hoy
```bash
cd ~/Documents/onelingo
flutter run -d chrome            # web
flutter run                      # iPhone 16 (simulador arrancado)
```
En "Ya tengo cuenta · Iniciar sesión" aparecen los 5 usuarios de prueba; toca uno y ENTRAR.


## Integración de las 3 APIs de IA (hecho, 7 sep 2026)
OpenAI = tutor y transcripción · Gemini = generación de ejercicios · ElevenLabs = voz con caché. Detalles y variables en `IA.md`.
