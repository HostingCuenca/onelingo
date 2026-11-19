# Compilar OneLingo para iOS en la Mac

Guía para la sesión que trabaje en la Mac. Revisada el 19-11-2026 sobre la 0.5.9+2015 (la que está en Google Play).

## Rama y versión

- Repo: `https://github.com/HostingCuenca/onelingo` (público: nunca subir `.env`, llaves, certificados ni perfiles).
- **Trabajar en `claude/educacion-multilenguaje`.** `main` está cientos de commits atrás y no sirve.
- Flutter **3.47.0** stable (el mismo con el que se compila Android). Xcode reciente + CocoaPods.

```bash
git clone -b claude/educacion-multilenguaje https://github.com/HostingCuenca/onelingo.git
cd onelingo
flutter pub get
cd ios && pod install && cd ..
```

Todos los assets de `pubspec.yaml` están en git; no hace falta copiar nada desde la PC Linux. Para compilar la app no se necesita ningún secreto: el backend vive en el servidor.

## Lo que ya está configurado

- Bundle ID `com.torisoftt.onelingo` (igual que Android), iOS mínimo 15.0, firma automática.
- `Info.plist`: nombre «Onelingo», permisos de micrófono y de reconocimiento de voz.
- Ícono: `ios/Runner/Assets.xcassets/AppIcon.appiconset`, generado con `python3 tools/imagenes/iconos_app.py --solo-ios` (hasta el 19-11-2026 tenía el ícono por defecto de Flutter; las compilaciones 201502–201504 salieron con ese ícono).

## Lo que falta en la Mac

1. **Equipo de firma.** `DEVELOPMENT_TEAM` no está en el proyecto. En Xcode → Runner → Signing & Capabilities → Team, elegir la cuenta de Apple Developer de Torisoftt (Bryan Fonseca Segura, equipo `V82AC4GTUM`; cuenta infoonelingo@gmail.com). Xcode lo guarda en `project.pbxproj`; ese cambio sí se puede commitear.
2. ~~App en App Store Connect~~: hecho el 19-11-2026 (App ID `com.torisoftt.onelingo` registrado y app «OneLingo» creada, idioma principal español de México, SKU `onelingo-ios`).

## Compilar en la nube (sin Mac)

`.github/workflows/ios-testflight.yml` compila en una Mac de GitHub (gratis: el repo es público), firma con la firma en la nube de Apple y sube a TestFlight.

Una sola vez, el dueño de la cuenta de Apple:

1. App Store Connect → Usuarios y acceso → Integraciones → App Store Connect API → claves de equipo → generar una clave con rol **Admin** (con menos permisos no puede crear el certificado de distribución). Anotar el **Issuer ID** y el **Key ID**, descargar `AuthKey_XXXX.p8` (solo se puede bajar una vez).
2. Cargar los secretos desde la PC con `gh` (la clave nunca pasa por el chat ni por el código):

```bash
gh secret set ASC_KEY_ID --repo HostingCuenca/onelingo
gh secret set ASC_ISSUER_ID --repo HostingCuenca/onelingo
gh secret set ASC_KEY_P8 --repo HostingCuenca/onelingo < ~/Descargas/AuthKey_XXXX.p8
```

Cada compilación:

```bash
gh workflow run ios-testflight.yml --repo HostingCuenca/onelingo --ref claude/educacion-multilenguaje
```

Número de compilación = build de `pubspec.yaml` × 100 + número de corrida (p. ej. 2015 → 201501), así nunca se repite entre subidas. La versión sale de `pubspec.yaml`. `Info.plist` declara `ITSAppUsesNonExemptEncryption = false` (solo HTTPS), así TestFlight no pregunta por cifrado en cada subida.

El archivo de Xcode se genera sin firmar (con firma automática Xcode exigiría un iPhone registrado para el perfil de desarrollo); la exportación lo firma con el certificado de distribución que Apple administra en la nube.

## Compilar en una Mac

`API_URL` es obligatorio. Sin él la app apunta a `localhost:8091` y no conecta con nada.

```bash
flutter build ipa --release --dart-define=API_URL=https://onelingo.org/api
```

El `.ipa` queda en `build/ios/ipa/`. Se sube con Transporter o con `xcrun altool`/Xcode Organizer.

Con parches de Shorebird también en iOS (requiere `shorebird login` en la Mac; app_id en `shorebird.yaml`):

```bash
shorebird release ios -- --dart-define=API_URL=https://onelingo.org/api
```

Versión y build salen de `pubspec.yaml` (`version: 0.5.9+2015`). En iOS el número de build puede ir independiente del de Android, pero no puede repetirse entre subidas.

Para probar en el simulador contra el backend real:

```bash
flutter run -d "iPhone 16" --dart-define=API_URL=https://onelingo.org/api
```

## Avisos antes de publicar en el App Store

- **Pagos.** La compra dentro de la app solo existe en Android (`lib/core/pagos/google_play.dart`, `pagoEnAppProvider` es falso fuera de Android). Para TestFlight da igual. Para el App Store, Apple exige In-App Purchase (StoreKit) en suscripciones digitales y rechaza enlaces a otros medios de pago (guía 3.1.1). Antes de enviar a revisión: implementar `in_app_purchase` para iOS y la verificación de recibos de Apple en el backend, o publicar sin venta dentro de la app.
- **Google Sign-In.** `ios/Runner/Info.plist` tiene marcadores `REEMPLAZAR-CON-EL-CLIENT-ID-DE-IOS` en `GIDClientID` y en `CFBundleURLSchemes`. Además el servidor tiene `GOOGLE_CLIENT_IDS` vacío, así que hoy el login con Google responde 503 en todas las plataformas y se entra con correo. Para activarlo en iOS: crear un cliente OAuth tipo iOS en Google Cloud con el bundle `com.torisoftt.onelingo`, poner su ID en los dos lugares del `Info.plist` y añadirlo a `GOOGLE_CLIENT_IDS` del backend (cambio en el servidor, con autorización).
- **Revisor de Apple.** Igual que en Play, hará falta una cuenta de prueba para la revisión. La clave de la revisora de Play no va en el repo ni en el chat.

## No hacer

- No commitear `ios/Pods`, `Flutter/Generated.xcconfig`, `.ipa`, certificados `.p12`, llaves `.p8` ni perfiles `.mobileprovision`.
- No tocar el backend ni el servidor desde la Mac: los despliegues siguen el flujo de `docs/claude-educacion/DESPLIEGUES.md`.

## Ficha de App Store (19-11-2026)

Llenada en es-MX y en-US con los textos de `docs/appstore/textos.json` y las capturas de `docs/appstore/capturas/` (1206×2622, generadas con `python3 tools/appstore/capturas_ios.py` a partir de las de Play). La app es solo iPhone (`TARGETED_DEVICE_FAMILY = 1`), así no se piden capturas de iPad.

- Información de la app: nombre «OneLingo: idiomas con IA» / «OneLingo: AI Language Tutor», categoría Educación, derechos de contenido de terceros «Sí», clasificación 13+ (los términos piden 13 años).
- Privacidad: 8 tipos de datos (nombre, correo, teléfono, audio, otro contenido, ID de usuario, compras, interacción), todos vinculados, ninguno para seguimiento. Falta pulsar **Publicar** (declaración del dueño de la cuenta).
- Precio: gratis; disponible en 174 países (sin China continental, que exige declaración de IA).
- Revisión: usuario `ana@onelingo.org` (la clave está en `~/.config/onelingo/ana-revisores.txt`, la pone el dueño) y notas en inglés; contacto Bryan Fonseca Segura, falta el teléfono.
- La versión de la ficha dice 1.0 y la compilación 0.5.9: hay que igualarlas para asociar la compilación.
- URL de soporte provisional: `/privacidad/` (tiene el correo de contacto); conviene una página `/soporte/`.
