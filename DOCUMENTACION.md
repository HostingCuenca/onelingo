# OneLingo · Documentación completa del proyecto

Estado al 8 de septiembre de 2026. Este documento resume **todo** lo que hay en el
repositorio: qué es, cómo está organizado, cómo se ejecuta cada parte, qué variables
de entorno necesita, cómo está desplegado en el servidor y qué queda pendiente. Los
demás archivos `.md` amplían cada tema; aquí están los enlaces.

---

## 1. Qué es OneLingo

App de aprendizaje de idiomas con IA, tipo Duolingo pero con un curso estructurado
completo: **10 idiomas × 10 niveles × 100 lecciones** (20 unidades por nivel, 5
lecciones por unidad), más un **Nivel 0 (Fundamentos)** para quien empieza desde
cero (alfabeto o silabario, sonidos, números, colores, vocabulario básico, verbos),
práctica libre con IA (50 situaciones + conversación libre con 4 tutores),
diagnóstico adaptativo de nivel, sección de errores, progreso, prueba gratuita de
1 hora y planes de pago.

Cliente externo. Desarrolla Torisoftt (Roger Rojas, Cuenca, Ecuador). Los
requerimientos del cliente están en `REQUERIMIENTOS.md` (documento canónico).

Idiomas: inglés (en), español (es), francés (fr), italiano (it), portugués (pt),
alemán (de), chino (zh), japonés (ja), coreano (ko), ruso (ru). En zh/ja/ko/ru el
contenido lleva romanización (pinyin con tonos, Hepburn, romanización revisada,
transliteración del cirílico).

---

## 2. Estructura del repositorio

```
onelingo/                      ← este repositorio (monorepo)
├── lib/                       App Flutter (Android, iOS y web)
├── test/                      Pruebas de la app (flutter test)
├── assets/                    Imágenes, sonidos, contenido empaquetado (assets/contenido)
├── content/                   Contenido en JSON, una carpeta por idioma (fuente de assets/contenido)
├── android/ ios/ web/         Proyectos nativos generados por Flutter
├── design/                    Logo y material de diseño
├── tools/contenido/           Pipeline de contenido (Node + TypeScript): semillas → JSON → assets
│   └── semilla/               Contenido escrito a mano (Nivel 0, 1 y 2 de los 10 idiomas, diagnóstico)
├── backend/                   API (Node 20 + Fastify 5 + PostgreSQL + zod)
│   ├── src/                   app.ts, server.ts, routes/, lib/
│   ├── sql/                   Migraciones 001_inicial, 002_auth, 003_audios
│   ├── .env                   Claves y configuración (NO se sube a git)
│   └── .env.ejemplo           Plantilla con los nombres de las variables
├── panel/                     Panel de administración (Vite + React + TypeScript)
└── *.md                       Documentación (ver sección 12)
```

Los tres proyectos vivían antes en carpetas hermanas (`onelingo-backend`,
`onelingo-panel`). En la máquina de desarrollo quedan enlaces simbólicos con esos
nombres para que los comandos antiguos sigan funcionando.

---

## 3. Stack

| Parte | Tecnología |
|---|---|
| App | Flutter 3.47 / Dart 3.13, Riverpod (StateNotifier), go_router, Material 3, flutter_tts, speech_to_text, audioplayers, record, path_provider, crypto, http |
| Backend | Node 20, Fastify 5, PostgreSQL 17, zod, nodemailer, pm2 en producción |
| Panel | Vite 6, React 18, TypeScript |
| Pipeline | Node 20, TypeScript (tsx), Zod, SDKs de Gemini / Anthropic |
| IA | OpenAI (tutor, transcripción, evaluación de escritura), Google Gemini (preguntas del diagnóstico y generación de ejercicios), ElevenLabs (voz) |
| Servidor | Ubuntu 22.04, Apache 2.4 (proxy inverso), certbot (Let's Encrypt), PostgreSQL 17, pm2 |

Paleta y reglas visuales en `CONTEXTO.md` (sin emojis en la interfaz: iconos vectoriales).

---

## 4. Cómo ejecutar en local

### 4.1 Base de datos
```bash
createdb onelingo
cd backend && npm install && npm run migrate      # aplica sql/001..003
```

### 4.2 Backend (puerto 8091)
```bash
cd backend
cp .env.ejemplo .env      # rellenar valores (sección 5)
npm run dev               # tsx watch src/server.ts
```
Comprobar: `curl http://localhost:8091/salud`.

### 4.3 Panel (puerto 5176, proxy /api → 8091)
```bash
cd panel && npm install && npm run dev
```
Usuario `admin`, PIN el de `ADMIN_PIN` en el `.env` del backend.

### 4.4 App
```bash
flutter pub get
flutter run -d chrome --dart-define=API_URL=http://localhost:8091
flutter run                                  # dispositivo o simulador
flutter test                                 # 23 pruebas
```
Parámetros `--dart-define`:
- `API_URL` URL del backend (sin barra final). En producción `https://onelingo.hostingcuenca.com/api`.
- `DESBLOQUEAR_TODO=true` desbloquea todos los niveles y lecciones (solo para probar).

### 4.5 Pipeline de contenido
```bash
cd tools/contenido && npm install
npm run importar          # semilla/*.txt → content/<idioma>/...json
npm run validar           # esquema, romanización, duplicados
npm run empaquetar        # → assets/contenido/<idioma>/{nivel-0,nivel-1,nivel-2,diagnostico}.json
```
Después de empaquetar hay que recompilar la app (el contenido va dentro del binario).

---

## 5. Variables de entorno

Archivo `backend/.env` (plantilla en `backend/.env.ejemplo`). **Nunca se sube a git.**
Para desarrollo local se comparte por un canal privado.

| Variable | Para qué |
|---|---|
| `PORT` | Puerto del backend (8091) |
| `DATABASE_URL` | `postgres://usuario:clave@host:5432/onelingo` |
| `JWT_SECRET` | Firma de los tokens de sesión |
| `ADMIN_USUARIO`, `ADMIN_PIN` | Acceso al panel de administración |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM` | Correos de verificación y recuperación. Sin SMTP los correos se guardan en la tabla `correos` y se ven en el panel |
| `PUBLIC_URL` | URL pública del backend (enlaces en correos, audios) |
| `GOOGLE_CLIENT_IDS` | IDs de cliente OAuth (iOS, Android, web) separados por coma |
| `IA_PROVEEDOR` | `openai` (actual), `gemini` o `claude` para el tutor conversacional |
| `OPENAI_API_KEY`, `OPENAI_API_KEY_ALT` | Clave de OpenAI (la alterna es de reserva) |
| `OPENAI_MODELO` | Modelo del tutor (`gpt-4.1-mini`) |
| `OPENAI_MODELO_EVALUACION` | Modelo que evalúa la escritura del diagnóstico (`gpt-4.1`) |
| `OPENAI_MODELO_TRANSCRIPCION` | Voz a texto (`gpt-4o-mini-transcribe`) |
| `GEMINI_API_KEY`, `GEMINI_MODELO` | Google Gemini (`gemini-flash-latest`) |
| `GEMINI_TIMEOUT_MS` | Espera máxima a Gemini antes de pasar a OpenAI (12000) |
| `ANTHROPIC_API_KEY`, `IA_MODELO` | Claude, solo si `IA_PROVEEDOR=claude` |
| `ELEVENLABS_API_KEY`, `ELEVENLABS_MODELO` | Voz natural (`eleven_multilingual_v2`) |
| `AUDIO_DIR` | Carpeta donde se guardan los MP3 generados (`./audio` en local, `/var/www/onelingo/audio` en producción) |
| `VOZ_MAX_CARACTERES` | Texto máximo por audio (600) |

Archivo `tools/contenido/.env`: solo `GEMINI_API_KEY` (la misma), para generar contenido con IA.

En producción el `.env` está en `/var/www/onelingo/backend/.env` y difiere del local en
`DATABASE_URL` (base local del servidor), `PUBLIC_URL`, `AUDIO_DIR` y `ADMIN_PIN`.

Las claves de OpenAI, Gemini y ElevenLabs las entregó el cliente y se van a rotar; para
cambiarlas basta editar el `.env` y reiniciar el backend (`pm2 restart onelingo-api`).

---

## 6. La app (Flutter)

Carpetas de `lib/`:

- `app/` router (go_router) y tema.
- `core/models/` modelos (usuario, progreso, lección, ejercicio…).
- `core/state/providers.dart` estado global con Riverpod: sesión, progreso por idioma, `fundamentos`, `diagnostico`, plan, hora gratis. `nombreLimpio` evita mostrar el correo como nombre.
- `core/content/` currículo (`curriculum.dart`), carga del JSON empaquetado (`contenido_json.dart`), Nivel 0 (`fundamentos.dart`), bancos por idioma (`idiomas.dart`), fotos, usuarios demo.
- `core/diagnostico.dart` motor del diagnóstico adaptativo (sección 8).
- `core/placement.dart` prueba de nivel por bloques (versión anterior, sigue disponible en Perfil).
- `core/voz.dart` voz (`Voz` → ElevenLabs vía backend con caché en el dispositivo, respaldo flutter_tts) y escucha (`Oido` → graba AAC y transcribe en el backend, respaldo speech_to_text).
- `core/api/sync.dart` cliente HTTP del backend: registro, login, Google, subida del progreso, chat, transcribir, voz, diagnóstico.
- `core/efectos.dart` sonidos, vibración y animaciones tipo Duolingo.
- `features/` pantallas: onboarding (bienvenida, login, registro, diagnóstico), home, course (niveles y unidades), lesson (reproductor de 8 tipos de ejercicio y resultado), exam, practice y chat con IA, mistakes, progress, plans y tutores.

Flujo del alumno: bienvenida → registro o login → elige idioma y nivel declarado →
diagnóstico adaptativo (opcional) → Inicio con plan de refuerzo → lecciones → examen
del nivel (65 % para aprobar) → siguiente nivel. Detalles en `FLUJOS.md`.

Usuarios demo (contraseña `1234`): ana, bryan, carla, diego, lucia (`demo_users.dart`).

---

## 7. Contenido

### 7.1 Formato de semillas (escritas a mano)
Todo el contenido actual está escrito a mano en `tools/contenido/semilla/` y se convierte
a JSON con `npm run importar`. Formatos completos en `PIPELINE.md`. Resumen:

- `<idioma>-nivel-N.txt` (N ≥ 1): cabecera `# n | Título | Objetivo | Gramática`, líneas
  `V` vocabulario, `F` frases, `D` diálogo, `E` errores típicos, `X` examen. Opciones del
  examen separadas por `;` (no usar `;` dentro de una opción).
- `<idioma>-nivel-0.txt`: unidades de `escritura` (símbolos con sonido, nota y ejemplo)
  y de `vocabulario`.
- `<idioma>-diagnostico.txt`: banco de preguntas `Q nivel | skill | tipo | tema | instrucción | texto | opciones | correcta | explicación`.

### 7.2 Estado del contenido
| Nivel | Idiomas | Unidades |
|---|---|---|
| 0 Fundamentos | 10 | 10 × 8 |
| 1 | 10 | 10 × 20 |
| 2 | 10 | 10 × 20 |
| 3-10 | – | Usan los bancos genéricos de la app hasta sembrarlos (o generarlos con Gemini) |
| Diagnóstico sembrado | inglés | 87 preguntas (respaldo sin conexión; en línea la IA redacta las preguntas) |

### 7.3 Generación con IA
`npm run generar -- --idioma en --nivel 3 --proveedor gemini` produce el mismo JSON que las
semillas. Decisión actual: sembrar a mano lo posible para abaratar y reservar Gemini
para lo dinámico (diagnóstico, personalización). Costes en `PIPELINE.md`.

---

## 8. Inteligencia artificial (3 servicios)

Reparto acordado con el cliente. Detalle en `IA.md`.

| Servicio | Uso | Dónde |
|---|---|---|
| **OpenAI** | Tutor conversacional (`POST /chat`, salida JSON estricta), transcripción de voz (`POST /transcribir`), evaluación de la escritura del diagnóstico (`POST /diagnostico/escritura`, gpt-4.1) y respaldo de Gemini | `backend/src/lib/ia_openai.ts`, `ia.ts` |
| **Gemini** | Redacta cada pregunta del diagnóstico (`POST /diagnostico/pregunta`) y el perfil final del profesor (`POST /diagnostico/perfil`); generación de ejercicios en el pipeline | `backend/src/lib/diag_ia.ts`, `ia_gemini.ts`, `tools/contenido` |
| **ElevenLabs** | Voz de tutores y narradores. Cada frase se sintetiza una vez: caché `sha256` en disco (`AUDIO_DIR`) + tabla `audios`; la app guarda además el MP3 en el dispositivo y precarga las frases de cada lección | `backend/src/lib/voz.ts`, rutas `/voz`, `/voz/lote`, `/voz/audio/:hash` |

Voces: mia = Sarah, leo = Liam, sofia = Matilda, max = Adam, narradora = Alice,
narrador = George. La app nunca llama a los proveedores; siempre pasa por el backend.

### Diagnóstico adaptativo
- Empieza en el nivel que declara el alumno (0-10), una pregunta por turno, mide la
  competencia menos observada (comprensión, vocabulario, gramática, tiempos,
  expresiones, contexto, cotidiano, escritura), sube o baja como máximo un nivel
  por respuesta, termina entre 10 y 25 preguntas cuando la estimación se estabiliza.
- Tipos de pregunta: elegir, la más natural, significado, comprensión de texto,
  situación, detectar el error, completar, respuesta corta, **escucha** y **dictado**
  (con voz del servidor), y **escritura libre** evaluada por la IA (35 % del nivel final).
- Cada pregunta la redacta Gemini (OpenAI si tarda más de 12 s); se envía la lista de
  preguntas ya hechas para no repetir; la siguiente se pide mientras se lee el feedback.
- Resultado: nivel con medios puntos, MCER, puntuación por competencia, fortalezas,
  debilidades, errores recurrentes, temas a reforzar, nivel recomendado (0 =
  Fundamentos), plan de dos semanas y resumen del profesor de IA. Se guarda en el
  progreso del alumno y se ve en Inicio y en el panel.
- `GET /diagnostico/estado` indica qué proveedor está activo.

---

## 9. Backend (API)

Rutas (todas bajo `/api/` en producción):

| Ruta | Descripción |
|---|---|
| `GET /salud` | Estado del servicio y de la base |
| `POST /auth/registro`, `/auth/login`, `/auth/google`, `/auth/verificar`, `/auth/recuperar`, `/auth/restablecer` | Autenticación (JWT). Detalle en `AUTENTICACION.md` |
| `GET/PUT /usuarios/estado` | Sincronización del progreso completo (JSON), incluye `fundamentos` y `diagnostico` |
| `POST /errores`, `/examenes`, `/eventos` | Registro de errores, exámenes y eventos de uso |
| `POST /chat` | Tutor con IA (guarda cada turno en `conversaciones`) |
| `POST /transcribir` | Audio (multipart) → texto |
| `GET /voz`, `POST /voz/lote`, `GET /voz/audio/:hash` | Voz con caché |
| `POST /diagnostico/pregunta`, `/diagnostico/escritura`, `/diagnostico/perfil`, `GET /diagnostico/estado` | Diagnóstico adaptativo |
| `/admin/*` | Resumen, usuarios, detalle, conversaciones, correos, audios (`/admin/audios/probar`) |

Tablas: `usuarios`, `progreso` (estado jsonb), `errores`, `examenes`, `eventos`,
`conversaciones`, `correos`, `audios`. Migraciones en `backend/sql/`, se aplican con
`npm run migrate`.

---

## 10. Panel de administración

`panel/` (Vite + React). Páginas: Resumen (KPIs, por idioma y nivel, exámenes,
errores, actividad), Usuarios y detalle (progreso, diagnóstico, plan), Conversaciones
IA, Correos, Voz y audios (audios guardados, cuota de ElevenLabs, prueba de voces).
En producción se sirve en `/panel` (build con `npm run build`, base `/panel/`,
API en `/api`).

---

## 11. Producción

Servidor: `167.235.20.41` (Hetzner, Ubuntu 22.04), dominio
`onelingo.hostingcuenca.com`. Acceso por SSH con clave (`root`). Comparte máquina con
otros servicios (Apache en 80/443, otros pm2). Todo lo de OneLingo vive en
`/var/www/onelingo/`:

```
/var/www/onelingo/backend   código del backend + .env de producción (pm2 "onelingo-api", puerto 8091)
/var/www/onelingo/panel     build del panel (Apache Alias /panel)
/var/www/onelingo/web       build web de Flutter (DocumentRoot) + /apk/ con las APK
/var/www/onelingo/audio     MP3 generados por ElevenLabs
```

- Apache: vhost `onelingo.hostingcuenca.com` (+ `-le-ssl` con certificado Let's Encrypt).
  `/api/` → `http://127.0.0.1:8091/`, `/panel` → carpeta del panel, `/` → web. Cabecera
  `Cache-Control: no-cache` en los archivos de arranque de Flutter para que cada
  despliegue se vea al recargar.
- Base de datos `onelingo` en el PostgreSQL 17 del servidor (rol `onelingo`).
- pm2: `pm2 restart onelingo-api`, `pm2 logs onelingo-api`.

URLs:
- Web: https://onelingo.hostingcuenca.com
- Panel: https://onelingo.hostingcuenca.com/panel (admin + PIN)
- API: https://onelingo.hostingcuenca.com/api/salud
- APK de prueba: https://onelingo.hostingcuenca.com/apk/onelingo-prueba.apk
- APK con todo desbloqueado: https://onelingo.hostingcuenca.com/apk/onelingo-abierto.apk

### Desplegar cambios
```bash
# Backend
rsync -az --delete --exclude node_modules --exclude .env --exclude audio backend/ root@167.235.20.41:/var/www/onelingo/backend/
ssh root@167.235.20.41 "cd /var/www/onelingo/backend && npm ci && npm run migrate && pm2 restart onelingo-api"

# Panel
cd panel && npm run build && rsync -az --delete dist/ root@167.235.20.41:/var/www/onelingo/panel/

# Web (ojo: --exclude apk para no borrar las APK publicadas)
flutter build web --release --dart-define=API_URL=https://onelingo.hostingcuenca.com/api
rsync -az --delete --exclude apk build/web/ root@167.235.20.41:/var/www/onelingo/web/

# APK
flutter build apk --release --dart-define=API_URL=https://onelingo.hostingcuenca.com/api
flutter build apk --release --dart-define=API_URL=https://onelingo.hostingcuenca.com/api --dart-define=DESBLOQUEAR_TODO=true
scp build/app/outputs/flutter-apk/app-release.apk root@167.235.20.41:/var/www/onelingo/web/apk/onelingo-prueba.apk
```

---

## 12. Documentos del repositorio

| Archivo | Contenido |
|---|---|
| `REQUERIMIENTOS.md` | Especificación del cliente (canónica) |
| `ARQUITECTURA.md` | Decisiones técnicas y estructura de la app |
| `CONTEXTO.md` | Contexto rápido: stack, paleta, usuarios demo, comandos |
| `FLUJOS.md` | Flujos de pantallas |
| `CURRICULO.md`, `CURRICULO-IDIOMAS.md` | Currículo CEFR/Oxford y plan por idioma |
| `PIPELINE.md` | Pipeline de contenido y formatos de semillas |
| `IA.md` | Arquitectura de IA (OpenAI, Gemini, ElevenLabs) y diagnóstico |
| `AUTENTICACION.md` | Registro, login, Google, correos |
| `PRUEBA-NIVEL.md` | Prueba de nivel por bloques (versión anterior del diagnóstico) |
| `PLAN.md` | Plan de trabajo y estado por sprint |

---

## 13. Pendiente

- Rotar las claves de OpenAI, Gemini y ElevenLabs (las actuales son provisionales) y
  cambiar la contraseña de root del servidor (el acceso por clave SSH ya está).
- Sembrar los bancos de diagnóstico de los otros 9 idiomas (hoy la IA los redacta en
  línea; la semilla es el respaldo sin conexión).
- Semillas de los niveles 3-10 (mismo formato) o generación con Gemini y revisión humana.
- Examen final con 30 preguntas y cooldown configurable.
- Google OAuth (IDs de cliente), SMTP real, Apple Sign-In, pagos, notificaciones, l10n.
- Pregenerar en lote los audios de cada nivel al empaquetar (`POST /voz/lote`).
- Límite de turnos de IA por plan y por hora de prueba.
