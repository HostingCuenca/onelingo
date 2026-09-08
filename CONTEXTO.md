# OneLingo · Contexto del proyecto

App de aprendizaje de idiomas con IA, tipo Duolingo pero con curso estructurado
completo (10 niveles × 100 lecciones por idioma) + práctica libre con IA (50
situaciones + conversación libre). Cliente externo; Torisoftt (Roger) desarrolla.

- **Requerimientos del cliente**: `REQUERIMIENTOS.md` (canónico).
- **Arquitectura y decisiones**: `ARQUITECTURA.md`.
- **Diseño**: Figma "Untitled" → página "OneLingo · UI", 8 secciones, 36 pantallas.
  https://www.figma.com/design/9L8blJJ22vtVLKDQUMJVWs/
  Logo exportado en `design/logo/onelingo-logo-704.png`.

## Stack
Flutter 3.47 / Dart 3.13 · Riverpod · go_router · dio (fase 2) · Material 3.
Plataformas: Android, iOS, **web** (demo para el cliente en una URL).
Backend (fase 2): Node 20 + Fastify + PostgreSQL + zod en `backend`.

## Paleta (colores del logo)
| Token | Hex | Uso |
|---|---|---|
| `morado` | #4519BB | primario (botones, "Lingo", progreso) |
| `moradoClaro` | #E6DEFF | fondos suaves, chips |
| `naranja` | #F7941D | CTA de onboarding, XP, racha |
| `azul` | #2E78D1 | flujo "ciudad", listening |
| `rojo` | #E03349 | flujo "médico", errores, corazones |
| `verde` | #40A652 | aciertos, completado |
| `amarillo` | #FFD23F | logros |
| `fondo` | #FCF9F8 | fondo de pantallas |
| `texto` | #1C1B1B / gris #79758A | texto principal / secundario |

Sin emojis en la interfaz: iconos vectoriales (Material Icons) e ilustraciones.

## Usuarios de prueba (login demo, contraseña `1234`)
`lib/core/content/demo_users.dart` — aparecen en "Ya tengo cuenta · Iniciar sesión":
ana (nueva) · bryan (Nivel 1, 12 lecciones, errores) · carla (Nivel 3 completo, examen
listo, plan 2 idiomas) · diego (hora gratis agotada) · lucia (Nivel 10, examen de Dominio).

## Fotos
`assets/img/fotos/` — 36 fotos CC0/CC BY bajadas de Openverse (créditos en
`CREDITOS.md`). Mapeo en `lib/core/content/fotos.dart` (situaciones, unidades del
Nivel 1, tutores, actividades, ejercicio "elige la imagen").

## Simulador iOS
El conector nativo del simulador falla con un error falso de `xcode-select`; se usa
`flutter build ios --simulator --debug` + `xcrun simctl install/launch` y capturas con
`xcrun simctl io booted screenshot`. Para tocar la pantalla desde scripts: `cliclick`
sobre la ventana del Simulator (posición con `osascript`).

## Idiomas y voz
`idiomaContenido` (curriculum.dart) lo fija el estado de progreso; `unidadesDe/leccionesDe`
cachean por idioma. Bancos por idioma en `idiomas.dart` (texto nativo + romanización en el
mismo campo). Voz: `Voz.instancia.hablar(texto, idioma)` quita la romanización antes de hablar.
Escucha: `Oido.instancia.escuchar(idioma, onTexto, onFin:)` (speech_to_text) y `similitud()` para
puntuar la pronunciación. El simulador iOS no tiene micrófono (log: "Could not find default
device for dIn"): probar STT en dispositivo real o en Chrome.

## Contenido generado
`tools/contenido` (Node/TS, @anthropic-ai/sdk 0.90, Zod). `content/plan-curricular.json` = 10 niveles ×
20 temas. Unidades en `content/<idioma>/nivel-N/unidad-NN.json`; `npm run empaquetar` las deja en
`assets/contenido/<idioma>/nivel-N.json`, que `ContenidoJson.precargar(idioma)` carga al iniciar y
al cambiar de idioma; `unidadesDe` prefiere ese JSON sobre los bancos manuales. Semilla del Nivel 1
exportable con `EXPORTAR=1 flutter test test/exportar_semilla_test.dart`.

## Backend y panel
`~/Documents/onelingo/backend` (Fastify+Postgres, `npm run dev`, puerto **8091**; el 8090 lo usa un
PocketBase de otro proyecto). BD `onelingo` local; tablas usuarios, progreso (estado jsonb), errores,
examenes, eventos. Admin: admin/1234 (.env). `~/Documents/onelingo/panel` (Vite+React, puerto 5176,
proxy /api→8091). En la app, `lib/core/api/sync.dart` (`Sync.instancia`) hace registro/login/subida;
URL con `--dart-define=API_URL=`. Ambos están en `.claude/launch.json` (onelingo-api, onelingo-panel).

## Autenticación e IA
Rutas `/auth/*` (registro, login, google, verificar, recuperar, restablecer) y `/chat` en el backend;
correos vía nodemailer (sin SMTP → tabla `correos`, visible en el panel). IA en `src/lib/ia.ts`
(claude-opus-5 por defecto, salida estructurada Zod v4). Guía completa en `AUTENTICACION.md`.
En la app: `Sync.instancia.{registrarConPassword,loginConPassword,loginConGoogle,recuperarPassword,chat}`.

## Gemini
Proveedor de IA activo: Gemini (`gemini-flash-latest`, clave de Roger en `backend/.env` y
`tools/contenido/.env`). El backend y el pipeline reintentan ante 503/429. Claude sigue disponible
con ANTHROPIC_API_KEY (`IA_PROVEEDOR=claude`).

## Estado actual
Fase 1 lista (demo navegable con datos locales, web + iOS). Plan de trabajo en
`PLAN.md`; currículo CEFR/Oxford en `CURRICULO.md`.

## Comandos
```bash
flutter run -d chrome          # demo web
flutter run                    # dispositivo/simulador
flutter build web --release    # publicar carpeta build/web en una URL
flutter analyze
```
