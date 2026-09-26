# Despliegues

Bloqueo operativo: `/tmp/onelingo-deploy.lock` **en el servidor**. Crear antes de desplegar (contenido: release, responsable, fecha); borrar al terminar la validación.
SSH: `ssh -F /dev/null root@167.235.20.41`. Web: `/var/www/onelingo/web`. Backend: `/var/www/onelingo/backend` (PM2 `onelingo-api`). APK: `/var/www/onelingo/web/apk/` (conservar siempre).

## Release de referencia (anterior a esta fase)

Fecha: 2026-09-25 19:35 UTC
Responsable: Codex
Contenido: home-layout17-assets (nuevo home, logo oficial, iconos, imagen «Aprende hoy»)
Build: `main.dart.js` sha256 `caa2e8a452cf3de8…`
Backup del servidor: `/var/www/onelingo/backups/home-layout17-assets-20260925T193557Z`
Resultado: en producción al iniciar esta fase.

<!-- Plantilla
## Release: YYYYMMDD-edu-N-objetivo

Fecha:
Responsable:
Contenido:
Commit:
Build:
Pruebas ejecutadas:
Backup del servidor:
Ruta desplegada:
URL de validación:
Health check:
Resultado:
Rollback disponible:
-->
