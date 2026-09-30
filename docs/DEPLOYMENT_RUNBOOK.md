# Runbook de despliegue

El historial y los rollbacks concretos están en `docs/claude-educacion/DESPLIEGUES.md`. Este runbook evita perder activos o afectar otros servicios del servidor compartido.

## Preparación

1. Confirmar alcance, rama, commit y árbol de trabajo.
2. Ejecutar las validaciones pertinentes.
3. Compilar web siempre con:

```bash
~/flutter/bin/flutter build web --release \
  --dart-define=API_URL=https://onelingo.hostingcuenca.com/api
```

4. Nombrar la release `YYYYMMDD-objetivo-N` y calcular hashes de los archivos relevantes.
5. Comprobar HTTPS y `/api/salud` antes de abrir SSH.

## Servidor

```bash
ssh -F /dev/null root@167.235.20.41
```

Rutas:

- web: `/var/www/onelingo/web`
- backend: `/var/www/onelingo/backend`
- backups: `/var/www/onelingo/backups`
- proceso: `onelingo-api`
- lock: `/tmp/onelingo-deploy.lock`

Antes de mutar, comprobar que no exista un lock activo. Crear el lock con release, responsable y fecha. Si existe, detenerse y determinar quién despliega.

## Reglas de publicación

- Crear un backup verificable antes de reemplazar archivos.
- Preparar web/backend en staging, validar allí y activar mediante renombre atómico cuando sea posible.
- Conservar siempre `web/apk/`, `web/avatar/`, backend `.env`, caché de audio y datos que no pertenezcan al build.
- No usar un `rsync --delete` directo sobre producción sin exclusiones y staging.
- Si cambia backend: instalar dependencias solo en su directorio, ejecutar typecheck/migración cuando corresponda y reiniciar únicamente `pm2 restart onelingo-api`.
- No reiniciar Apache, PostgreSQL, PM2 global ni procesos ajenos salvo evidencia y autorización específica.

## Verificación posterior

- `/api/salud` responde correctamente.
- PM2 muestra `onelingo-api` estable.
- Inicio, onboarding, ruta educativa, voz y avatar cargan sin errores de consola.
- Los assets educativos nuevos responden 200.
- `web/apk/` y `web/avatar/` siguen disponibles.
- Las variables del backend no cambiaron; comparar hashes de `.env`, no su contenido.
- El lock se elimina solo después de validar.

Registrar fecha, commit, build/hash, pruebas, backup, rutas, URL, salud, resultado y comando de rollback en `docs/claude-educacion/DESPLIEGUES.md`.
