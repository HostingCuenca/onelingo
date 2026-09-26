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

## Release: 20260926-edu-1-fundamentos

Fecha: 2026-09-26 18:56 UTC
Responsable: Claude (Claude Code)
Contenido: ruta de Fundamentos (6 unidades) en los 10 idiomas con esquema 2; Nivel 0 = ruta (DEC-007); destinos del home por idioma (DEC-008); gramática que reanuda y marca lo practicado; corrección tolerante a tildes (DEC-009); 9 idiomas con «Versión inicial» (DEC-010). Solo web; backend sin cambios.
Commit: `c4e1ade` (código en `607a1df`), rama `claude/educacion-multilenguaje`
Build: `flutter build web --release --dart-define=API_URL=https://onelingo.hostingcuenca.com/api` · `main.dart.js` sha256 `ffefcc975f280e73…`
Pruebas ejecutadas: `python3 tools/validar_ruta.py` (10 idiomas, 0 errores); `flutter analyze lib` (0 errores, 7 info previos); `flutter test` (129 pasan, 1 omitida, 0 fallos); recorrido web local (inglés), emulador Android (japonés) y producción (francés).
Backup del servidor: `/var/www/onelingo/backups/20260926-edu-1-fundamentos/web-anterior` (release `home-layout17-assets`, `main.dart.js` `caa2e8a452cf3de8…`) + `env.sha256`
Ruta desplegada: `/var/www/onelingo/web` (staging por rsync con hardlinks; `apk/` conservado con `cp -al`; avatares intactos)
URL de validación: https://onelingo.hostingcuenca.com/?release=20260926-edu-1-fundamentos (`#/fundamentos`)
Health check: `/api/salud` OK; `onelingo-api` online; 10 `ruta/f0.json`, `home-aprende-hoy.webp`, `apk/onelingo-prueba.apk` y `avatar/index.html` responden 200; `.env` sin cambios (sha256).
Resultado: OK. Bloqueo `/tmp/onelingo-deploy.lock` creado y liberado.
Rollback disponible:
```bash
ssh -F /dev/null root@167.235.20.41 'cd /var/www/onelingo && mv web staging/20260926-edu-1-fundamentos/web-retirada && mv backups/20260926-edu-1-fundamentos/web-anterior web'
```

## Release: 20260926-edu-2-a1-voz

Fecha: 2026-09-26 20:08 UTC
Responsable: Claude (Claude Code)
Contenido: A1 de inglés en esquema 2 (29 unidades, niveles 1–2, rutas `/ruta/a1-1` y `/ruta/a1-2`); unidades omitibles según diagnóstico (DEC-011); pronunciación por idioma (DEC-012: `language_code`, caché por idioma, zh/ja sin espacios, voz del sistema para sílabas sueltas); sonidos revisados y opciones/botones con el estilo de `BotonPrincipal` (DEC-013). Web + backend (`src/lib/voz.ts`, `src/routes/voz.ts`).
Commit: `f0a6451` (A1 en `913a4e3`), rama `claude/educacion-multilenguaje`
Build: `main.dart.js` sha256 `b772bd8c96388c55…`; backend `voz.ts` `fe3852934581990a…`, `routes/voz.ts` `33f2fb41a7ca99c0…`
Pruebas ejecutadas: `tools/validar_ruta.py` (10 idiomas, 0 errores, regla estricta de distractores); `flutter analyze lib` (7 info previos); `flutter test` 133 pasan, 1 omitida; backend `tsx --test` 11 pasan; `tsc` en staging del servidor; comparación Whisper con/sin `language_code` (ru y pt pasan de «inglés» a su idioma); verificación visual web del ejercicio (opciones con pedestal, COMPROBAR/CONTINUAR).
Backup del servidor: `/var/www/onelingo/backups/20260926-edu-2-a1-voz/` (`web-anterior` = release edu-1, `backend-src/lib-voz.ts`, `backend-src/routes-voz.ts`, `env.sha256`). Los archivos de backend reemplazados eran idénticos al checkpoint.
Ruta desplegada: `/var/www/onelingo/web` (apk conservado) y 2 archivos en `/var/www/onelingo/backend/src`; `pm2 restart onelingo-api`.
URL de validación: https://onelingo.hostingcuenca.com/?release=20260926-edu-2-a1-voz (`#/ruta/a1-1`)
Health check: `/api/salud` OK; `/api/voz/estado` `eleven_flash_v2_5`; `onelingo-api` online y estable; assets A1, `ja/ruta/f0.json`, `sfx/toque.wav`, APK y avatar responden; `.env` sin cambios.
Resultado: OK. Bloqueo creado y liberado.
Rollback disponible:
```bash
ssh -F /dev/null root@167.235.20.41 'cd /var/www/onelingo && B=backups/20260926-edu-2-a1-voz && cp $B/backend-src/lib-voz.ts backend/src/lib/voz.ts && cp $B/backend-src/routes-voz.ts backend/src/routes/voz.ts && pm2 restart onelingo-api && mv web staging/20260926-edu-2-a1-voz/web-retirada && mv $B/web-anterior web'
```
Nota: el audio de idiomas distintos del inglés se regenera en el primer uso (clave de caché nueva).

## 20260926-edu-3-escrituras — PENDIENTE
Fecha: 2026-09-26 · Responsable: Claude (Claude Code)
Contenido: escrituras completas en f0 (kana, hangul, pinyin, cirílico, alfabetos), A1 «Primeras frases» ×10 idiomas (204 unidades), paso `tabla`, repetición de fallos al final del bloque, celebración con XP/precisión/tiempo, `sfx/nivel.wav`, precarga de fuentes en web. Solo web (backend sin cambios desde edu-2).
Commit: `15e02e8` · Build: `main.dart.js` sha256 `181298a30c436abf…` (API_URL prod) en `build/web`.
Estado: NO desplegado. El puerto 22 de 167.235.20.41 no responde desde la IP 128.201.160.43 (30 reintentos en 30 min); HTTPS y `/api/salud` OK. Probable bloqueo de fail2ban. No se creó bloqueo ni se tocó el servidor.
