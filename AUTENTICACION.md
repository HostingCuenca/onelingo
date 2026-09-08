# OneLingo · Autenticación, correo e IA (configuración)

## Qué hay implementado
| Función | Backend | App |
|---|---|---|
| Registro con correo + contraseña | `POST /auth/registro` (bcrypt, envía correo de verificación) | Paso 1 del registro; si falla (correo repetido, red) muestra el error |
| Inicio de sesión | `POST /auth/login` → devuelve el progreso guardado | Pantalla "Iniciar sesión"; restaura el progreso del servidor en un dispositivo nuevo |
| Verificar correo | `GET /auth/verificar?token=` (página HTML) | Enlace en el correo |
| Recuperar contraseña | `POST /auth/recuperar` → correo con enlace; `GET/POST /auth/restablecer` | Botón "Olvidé mi contraseña" |
| Google Sign-In | `POST /auth/google` (verifica el idToken con `GOOGLE_CLIENT_IDS`) | Botón "Google" (`google_sign_in` 7) |
| IA del tutor | `POST /chat` → Claude con tutor + perfil de nivel + situación; guarda cada turno | El chat usa el servidor y, si no hay IA, el simulador local |
| Usuarios demo | `POST /usuarios/registro|login` (sin contraseña, marcados `es_demo`) | Tarjetas de la pantalla de login |

## 1. Correo (SMTP)
Sin configurar, **los correos no se envían**: quedan en la tabla `correos` y se ven en el panel
(pestaña *Correos*, con el enlace de verificación o de restablecimiento para probar el flujo).
Para enviarlos de verdad, en `backend/.env`:
```
SMTP_HOST=smtp.gmail.com     # o Brevo, Resend, Mailgun, SES…
SMTP_PORT=587
SMTP_USER=tu-cuenta@gmail.com
SMTP_PASS=contraseña-de-aplicación
SMTP_FROM=OneLingo <no-reply@tudominio.com>
PUBLIC_URL=https://api.tudominio.com   # base de los enlaces de los correos
```
Con Gmail hay que crear una *contraseña de aplicación* (cuenta con verificación en dos pasos).
Para producción recomiendo un servicio transaccional (Brevo o Resend tienen plan gratuito).

## 2. Google Sign-In
### Crear las credenciales (enlaces)
1. Crea o elige un proyecto: https://console.cloud.google.com/projectcreate
2. Pantalla de consentimiento OAuth (nombre "OneLingo", correo de soporte, logo):
   https://console.cloud.google.com/auth/branding
3. Crea **tres** IDs de cliente OAuth en https://console.cloud.google.com/apis/credentials
   → "Crear credenciales" → "ID de cliente de OAuth":
   - **iOS**: ID del paquete `com.torisoftt.onelingo`. Te da un *Client ID* y un
     *iOS URL scheme* (`com.googleusercontent.apps.…`).
   - **Android**: paquete `com.torisoftt.onelingo` + huella **SHA-1** del certificado
     (`cd android && ./gradlew signingReport`, o `keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android`).
   - **Web**: tipo "Aplicación web". Orígenes autorizados: `http://localhost:8088`,
     `http://localhost:8087` y el dominio final.

### Dónde va cada ID
- **Backend** `backend/.env`: `GOOGLE_CLIENT_IDS=<ios>,<android>,<web>` (separados por coma;
  el servidor acepta tokens emitidos para cualquiera de ellos).
- **iOS** `ios/Runner/Info.plist`: sustituye los dos valores `REEMPLAZAR…` de `GIDClientID` y del
  `CFBundleURLSchemes` por el Client ID de iOS y su URL scheme invertido.
- **Android**: no necesita fichero; basta el SHA-1 registrado y pasar el **client ID web** como
  `serverClientId` (ya se hace con `--dart-define=GOOGLE_CLIENT_ID_WEB=…`).
- **Web y Android**: compila con `flutter build web --dart-define=GOOGLE_CLIENT_ID_WEB=<web>`
  (y lo mismo en `flutter run`).

Sin estos valores el botón "Google" muestra un aviso y el resto de la app sigue funcionando.

## 3. IA del tutor (Gemini o Claude)
El backend admite dos proveedores; se elige con `IA_PROVEEDOR=gemini|claude` (si solo hay clave de
Gemini, la usa automáticamente).

**Gemini (Google AI Studio)** — activo ahora con tu clave: `GEMINI_API_KEY=…` y `GEMINI_MODELO=gemini-flash-latest`
(el único nombre habilitado para la clave; los `gemini-2.5-*` devuelven 404 para cuentas nuevas). Gemini
devuelve JSON con `responseSchema`; ante 503 "alta demanda" o 429 el backend reintenta con espera.
Crear/rotar claves: https://aistudio.google.com/app/apikey · Cuotas y facturación: https://ai.google.dev/gemini-api/docs/rate-limits

**Nota de seguridad**: la clave que pegaste en el chat conviene rotarla en AI Studio cuando termines de probar;
está guardada solo en `backend/.env` y `tools/contenido/.env` (ambos ignorados por git).

**Claude (Anthropic)**: `ANTHROPIC_API_KEY=sk-ant-…` y opcionalmente `IA_MODELO`
(`claude-opus-5` por defecto; `claude-sonnet-5` es ~2,5× más barato). Crear la clave:
https://console.anthropic.com/settings/keys

Cada turno guarda en `conversaciones` el mensaje, la respuesta, las correcciones y los tokens
(pestaña *Conversaciones IA* del panel). Coste orientativo por turno con Opus 5: ~1 500 tokens de
entrada (el prompt de sistema se cachea) y ~150 de salida ≈ $0,01; con Sonnet 5 ≈ $0,004.
Recomendación para el plan de negocio: límite de turnos por día según plan (ya previsto en PLAN.md).

## 4. Variables de la app
| Variable (`--dart-define`) | Uso |
|---|---|
| `API_URL` | URL del backend (por defecto `http://localhost:8091`; Android emulador `10.0.2.2`) |
| `GOOGLE_CLIENT_ID_WEB` | Client ID web para Google en web/Android |

## 5. Seguridad pendiente para producción
HTTPS obligatorio, `JWT_SECRET` largo y secreto, expiración y renovación de tokens, límite de
intentos en `/auth/login`, borrado de cuenta (requisito de las tiendas) y política de privacidad.


> La configuración de IA (OpenAI, Gemini, ElevenLabs) se movió a `IA.md`.
