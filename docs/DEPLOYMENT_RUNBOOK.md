# Runbook de despliegue

El historial y los rollbacks concretos están en `docs/claude-educacion/DESPLIEGUES.md`. Este runbook evita perder activos o romper producción.

## Preparación

1. Confirmar alcance, rama, commit y árbol de trabajo.
2. Ejecutar las validaciones pertinentes.
3. Compilar web siempre con:

```bash
~/flutter/bin/flutter build web --release \
  --dart-define=API_URL=https://onelingo.org/api
```

4. Nombrar la release `YYYYMMDD-objetivo-N` y calcular hashes de los archivos relevantes.
5. Comprobar HTTPS y `/api/salud` antes de abrir SSH.

## Servidor

Desde el 29-10-2026 OneLingo tiene servidor propio: VPS Hostinger KVM 2 (Boston), `179.197.89.105`, Ubuntu 26.04, 2 vCPU, 8 GB, 100 GB. Hetzner (`167.235.20.41`) ya no atiende OneLingo: solo queda un puente temporal (ver «Corte» abajo).

```bash
ssh onelingo   # alias de ~/.ssh/config: root@179.197.89.105 con ~/.ssh/id_ed25519_onelingo (solo llave, sin contraseña)
```

Rutas y servicios:

- web: `/var/www/onelingo/web` (DocumentRoot); panel: `/var/www/onelingo/panel` (`/panel`); audios: `/var/www/onelingo/audio`
- backend: `/var/www/onelingo/backend` (`.env` 600), Node 22, PostgreSQL 18 (base y rol `onelingo`), ffmpeg 8
- todo pertenece al usuario de servicio `onelingo`; tras copiar archivos como root: `chown -R onelingo:onelingo <ruta>`
- PM2 corre como `onelingo` (servicio `pm2-onelingo`, arranca solo): `sudo -u onelingo -H pm2 restart onelingo-api`, `sudo -u onelingo -H pm2 logs onelingo-api`
- dependencias y migraciones también como `onelingo`: `cd /var/www/onelingo/backend && sudo -u onelingo -H npm ci && sudo -u onelingo -H npm run migrate`
- Apache: `sites-available/onelingo.conf` (80 → https) y `onelingo-ssl.conf` (`/api/` → `127.0.0.1:8091`); certificado propio `/etc/letsencrypt/live/onelingo.org` (onelingo.org y www, renovación automática con `certbot.timer`; el subdominio de hostingcuenca ya no se usa). En este servidor solo vive OneLingo: `systemctl reload apache2` está permitido.
- respaldos de la base: `/usr/local/bin/onelingo-respaldo-db` cada día a las 03:15 (cron `/etc/cron.d/onelingo-respaldo`) en `/var/backups/onelingo`, 14 días; además backup semanal de Hostinger
- respaldos de despliegues: `/var/www/onelingo/backups`
- seguridad: ufw (22, 80, 443), fail2ban, actualizaciones automáticas, SSH solo con llave
- lock: `/tmp/onelingo-deploy.lock`

Antes de mutar, comprobar que no exista un lock activo. Crear el lock con release, responsable y fecha. Si existe, detenerse y determinar quién despliega.

### Corte desde Hetzner (29-10-2026)

`tools/servidor/corte.sh` paró la API de Hetzner, copió la base y los audios al VPS y dejó en Hetzner el proceso PM2 `onelingo-puente` (`/var/www/onelingo/puente.mjs`) en el puerto 8091, que reenvía `/api` al VPS mientras haya caché de DNS vieja. Hetzner conserva su lock puesto: no desplegar allí. Retirar el puente y los archivos de OneLingo de Hetzner cuando su `onelingo-access.log` deje de recibir tráfico.

## Reglas de publicación

- Crear un backup verificable antes de reemplazar archivos.
- Preparar web/backend en staging, validar allí y activar mediante renombre atómico cuando sea posible.
- Conservar siempre `web/apk/`, `web/avatar/`, backend `.env`, caché de audio y datos que no pertenezcan al build.
- No usar un `rsync --delete` directo sobre producción sin exclusiones y staging.
- Si cambia backend: instalar dependencias solo en su directorio, ejecutar typecheck/migración cuando corresponda y reiniciar únicamente `sudo -u onelingo -H pm2 restart onelingo-api`.
- No reiniciar PostgreSQL ni el servidor salvo evidencia y autorización específica; para Apache basta `systemctl reload apache2`.

## Verificación posterior

- `/api/salud` responde correctamente.
- PM2 muestra `onelingo-api` estable.
- Inicio, onboarding, ruta educativa, voz y avatar cargan sin errores de consola.
- Los assets educativos nuevos responden 200.
- `web/apk/` y `web/avatar/` siguen disponibles.
- Las variables del backend no cambiaron; comparar hashes de `.env`, no su contenido.
- El lock se elimina solo después de validar.

Registrar fecha, commit, build/hash, pruebas, backup, rutas, URL, salud, resultado y comando de rollback en `docs/claude-educacion/DESPLIEGUES.md`.
