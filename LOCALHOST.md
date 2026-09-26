# OneLingo: desarrollo local

Preparado el 8 de septiembre de 2026 en `/home/roggrt/Documents/onelingo`.

| Servicio | Dirección |
|---|---|
| App Flutter web | http://127.0.0.1:8087 |
| Panel React | http://127.0.0.1:5176/panel/ |
| Backend Fastify | http://127.0.0.1:8091 |
| Salud API | http://127.0.0.1:8091/salud |
| PostgreSQL 17, base onelingo | 127.0.0.1:55432 |

La BD usa contenedor `onelingo-local-db` y volumen `onelingo-local-pgdata`. Es independiente de `jr-pg` y de producción. Las credenciales están en `work/local/db.env`, ignorado por Git; el backend tiene actualizada su DATABASE_URL en `.env`. Los proveedores de IA conservan las claves existentes: el servidor de aplicación y los datos son locales, las llamadas de IA y voz siguen siendo externas y consumen la cuenta configurada.

Para arrancar cada parte, desde la raíz del proyecto, en terminales separadas:

```bash
./tools/dev-local.sh db
./tools/dev-local.sh backend
./tools/dev-local.sh panel
./tools/dev-local.sh web
```

El backend aplica automáticamente las migraciones pendientes. El panel reenvía `/api` al puerto 8091. Backend y panel tienen recarga durante el desarrollo. En la terminal Flutter, `r` recarga y `R` reinicia.

Para comprobar los servicios:

```bash
./tools/dev-local.sh check
```

## Android — pospuesto por decisión del usuario

Flutter está en `/home/roggrt/flutter`; SDK Android en `/home/roggrt/Android/Sdk`. Emuladores existentes: `cliente_avd` y `restaurante_avd`. Se eligió `cliente_avd`.

La compilación debug x86_64 pasó y está en `build/app/outputs/flutter-apk/app-debug.apk`, configurada con `API_URL=http://10.0.2.2:8091`. Esta dirección representa el localhost del equipo desde el emulador Android estándar.

Por ahora el trabajo y las pruebas se harán en la versión web. Android no bloquea esta fase.

El entorno aislado de ejecución no expone `/dev/kvm`. El arranque por software llegó a ADB, pero Android no llegó a habilitar el servicio de paquetes durante el intento; se detuvo esa instancia. Abrir `cliente_avd` desde Android Studio y, una vez que Android esté listo:

```bash
adb devices -l
# Sustituir por el identificador mostrado arriba:
./tools/dev-local.sh android emulator-5554
```

Para instalar la APK ya compilada, sin recompilar:

```bash
adb -s emulator-5554 install -r build/app/outputs/flutter-apk/app-debug.apk
adb -s emulator-5554 shell am start -n com.torisoftt.onelingo/.MainActivity
```

Cambiar el identificador si ADB muestra otro. Si aparece `INSTALL_FAILED_UPDATE_INCOMPATIBLE`, no desinstalar una versión anterior sin revisar primero sus datos; instalar un applicationId de desarrollo diferente o acordar el borrado del estado demo.

## Adaptaciones realizadas

- Dependencias Node reinstaladas desde lockfiles para Linux en backend y panel.
- `pubspec.yaml` admite Dart desde 3.13.0, la versión instalada con Flutter 3.47.0; no se cambiaron versiones de paquetes Dart.
- `android/local.properties` regenerado con las rutas Linux.
- Flutter agregó exclusiones de plataformas al análisis.
- Directorio `/work/` ignorado por Git para archivos locales y credenciales.
- Script `tools/dev-local.sh` con comandos por servicio y estrategia Kotlin in-process para evitar depender de su daemon global en entornos aislados.

Verificación: Flutter analyze sin incidencias; 23 tests aprobados y uno omitido por ser exportación opcional; APK debug compilada; panel build correcto; API y proxy del panel responden a salud; bienvenida web verificada visualmente.

No se ha desplegado ningún cambio en el servidor. El servidor actual se usará para pruebas cuando los cambios locales estén listos; no se considera el destino definitivo de la app.


## Diagnóstico personalizado (8 de septiembre de 2026)

La versión de trabajo actual usa http://127.0.0.1:8088 con backend local en 8091. El servidor de 8087 corresponde a la sesión anterior. `tools/dev-local.sh web` usa ahora 8088; se puede cambiar con `ONELINGO_WEB_PORT`.

El registro incluye ocho sectores y ocho objetivos de selección múltiple. El diagnóstico de inglés tiene diez actividades generadas y revisadas: lectura (2), listening con ElevenLabs (3), gramática (2, completar y ordenar), vocabulario (1) y escritura (2). Hay feedback después de cada respuesta, perfil orientativo por competencia y acceso permanente en Inicio. Los borradores se guardan localmente por usuario; el resultado completo y el perfil se sincronizan al servidor al finalizar.

Gemini es principal y OpenAI respaldo. Durante la comprobación Gemini devolvió HTTP 429 de cuota; OpenAI y ElevenLabs respondieron correctamente. No se cambiaron claves ni facturación.

La puntuación sigue siendo orientativa y se calcula en el cliente. Antes de un lanzamiento público, trasladar la autoridad de los intentos y la corrección objetiva al backend, calibrar las rúbricas y resolver los problemas de autenticación demo descritos en AUDITORIA.md.

Se corrigió también CORS para permitir PUT desde la web. La comprobación final en PostgreSQL confirmó que el usuario demo guardó sus sectores, objetivos y las diez respuestas del diagnóstico.
