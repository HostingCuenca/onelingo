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

## Release: 20260929-edu-4-n1-runtime

Fecha: 2026-09-29 14:03 UTC
Responsable: Codex
Contenido: release web acumulativa; incorpora el alcance de `edu-3-escrituras` pendiente y conecta Inglés N1 editorial al recorrido real con 100 clases, biblioteca determinista de 1.300 ejercicios, pools separados y 100 unidades activas. Los enlaces históricos resuelven a N1. N2 C1–C15 permanece fuera del runtime y no se publica. Backend, APK y avatar sin cambios.

Commit: árbol de trabajo sobre `d4e2dcd`, rama `claude/educacion-multilenguaje`; los cambios educativos continúan sin commit. El artefacto desplegado está identificado por manifiesto completo en `backups/20260929-edu-4-n1-runtime/build-web-v2.sha256`.

Build: `flutter build web --release --no-pub --dart-define=API_URL=https://onelingo.hostingcuenca.com/api`; `main.dart.js` SHA-256 `71d06ed85241a61ff340e6b2c34ec84b3543100030f76fecb42a78ea8ad1af19`; `n1-editorial.json` `2f08ad20e29427c1de4baab04eb2d1d470234cc89a9756d90c22e958d29ac718`; biblioteca `6804db552370d12f30f293bead21800ac0c7dcb921b47024c73703a4599f3961`.

Pruebas ejecutadas: rutas 10 idiomas/0 errores; 47 pruebas Python; Flutter 155 pasan, 1 omitida; prueba focalizada posterior a la corrección 22 pasan; análisis sin errores nuevos y con 12 avisos heredados. Verificación HTTP de 100 unidades, 100 activas y 1.300 familias. Recorrido visual real: `/aprender` muestra N1 A1 completo, 0/100; C1 abre y muestra solo las 8 tarjetas editoriales de vocabulario.

Incidente contenido durante QA: el primer candidato llegó a activarse brevemente, pero la inspección visual detectó que exponía frases internas como tarjetas de vocabulario. Se restauró inmediatamente la web anterior (`main.dart.js` `b772bd8c…`), se corrigió el compilador y solo entonces se activó/vigiló la variante v2. No se declaró completada la release defectuosa.

Backup del servidor: `/var/www/onelingo/backups/20260929-edu-4-n1-runtime/web-anterior` (`main.dart.js` `b772bd8c96388c55…`), hashes del entorno y manifiestos de build.
Ruta desplegada: `/var/www/onelingo/web`, mediante staging y renombres; `/apk/` y `/avatar/` preservados por hardlinks desde la web anterior.
URL de validación: `https://onelingo.hostingcuenca.com/?release=20260929-edu-4-n1-runtime-v2#/aprender`
Health check: `/api/salud` OK; `onelingo-api` online sin reinicio; `.env` conserva SHA-256 `35a518e3…`; APK y avatar responden 200.
Resultado: OK.

Rollback disponible:
```bash
ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20260929-edu-4-n1-runtime/web-retirada-post-release && cp -al backups/20260929-edu-4-n1-runtime/web-anterior web'
```

## Release: 20260930-edu-5-n2-n3-review

Fecha: 2026-09-30 13:53 UTC
Responsable: Codex
Contenido: release web acumulativa para revisión del cliente. Mantiene N1 C1–C100 y publica N2 C1–C100 y N3 C1–C90 en el recorrido real. Total: 290 clases activas y 3.770 ejercicios deterministas, sin tutor IA en runtime. N3 C91–C100 no forma parte de esta release. Incluye soporte visible para fuentes de lectura/escucha, completar multiparte, puntuación parcial y rúbricas locales de escritura. Backend, APK y avatar sin cambios.

Commit: árbol de trabajo sobre `d4e2dcd`, rama `claude/educacion-multilenguaje`; los cambios educativos continúan sin commit por la restricción histórica sobre `.git`.

Build: `flutter build web --release --no-pub --dart-define=API_URL=https://onelingo.hostingcuenca.com/api`; `main.dart.js` SHA-256 `72e25f36798f5810b1fac9c68ec95d788729ddd9dd8d3378f7965f414b7808a6`; biblioteca `6082121eb64241c789032d5ba8d044c80759ffd93f3d6a3738f98a9081063ff2`; activación `f1effe220d28baa4377643fb3bbecdeb5dd114d58eb9e190c0388ee7358bc765`; versión de biblioteca `2026.09.30-en-n3.1`.

Pruebas ejecutadas: rutas de 10 idiomas con 0 errores; 61 pruebas Python; 169 pruebas Flutter pasan y 1 se omite; análisis focalizado sin problemas. El análisis global conserva 12 avisos heredados. Verificación del build y HTTP: 290 unidades activas, 3.770 familias, N2 C1–C100, N3 C1–C90 y ausencia de C91. Inspección visual real de `#/ruta/n2` y `#/ruta/n3` correcta.

Backup del servidor: `/var/www/onelingo/backups/20260930-edu-5-n2-n3-review/web-anterior`, `env.sha256`, `web-anterior.sha256` y `build-web.sha256`.
Ruta desplegada: `/var/www/onelingo/web`, mediante staging, copia por hardlinks de `apk/` y `avatar/`, y renombres atómicos.
URL de validación: `https://onelingo.hostingcuenca.com/?release=20260930-edu-5-n2-n3-review#/aprender`
Health check: `/api/salud` OK; `onelingo-api` online sin reinicio; `.env` conserva SHA-256 `35a518e3a6c41168b07ef38d44680a77bd23079caf169ab7231823fff62435b1`; APK y avatar responden 200.
Resultado: OK. Lock creado y liberado después de la comprobación visual.

Rollback disponible:
```bash
ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20260930-edu-5-n2-n3-review/web-retirada-post-release && cp -al backups/20260930-edu-5-n2-n3-review/web-anterior web'
```

## Release: 20260930-edu-6-pulido

Fecha: 2026-09-30 16:30 UTC · Responsable: Claude (Claude Code)
Contenido: pulido de N1–N3 C1–C90 (auditoría 2026-09-30): 290/290 clases enriquecidas (explicación, patrón, tabla, errores reales, situación con diálogo e ítem propio, ejemplos reales), 668 pistas de «completar», ~200 ejercicios corregidos y 429 ítems con tercera opción; app: fichas desordenadas, contracciones, umbral redondeado, repaso sin bucle, audio en ordenar/completar, nivel elegido en el diagnóstico, MCER por nivel, hash web, producción abierta (216 variantes), JSON compactos. Solo web; backend sin cambios.
Commit: `d60f7a4` (contenido `bf0d57b`), rama `claude/educacion-multilenguaje`.
Build: `main.dart.js` sha256 `e6eca1c7da207a9c…`; biblioteca `c5039f628c87e5b4…` versión `2026.09.30-en-pulido.1`.
Pruebas: 176 Flutter (1 omitida), 61 herramientas, validar_ruta 10 idiomas 0 errores, validar_enriquecimiento 0 errores; recorrido visual en local y en producción (N2 C50).
Backup: `/var/www/onelingo/backups/20260930-edu-6-pulido/` (`web-anterior` = edu-5, `env.sha256`, `apache-onelingo-le-ssl.conf.bak`); staging `staging/20260930-edu-6-pulido/` (`build-web.sha256`, `web-retirada`).
Ruta desplegada: `/var/www/onelingo/web` (apk y avatar por hardlink desde la release anterior, renombre atómico).
Servidor: `AddOutputFilterByType DEFLATE application/json` en el vhost 443 de onelingo; `apache2ctl configtest` OK y `systemctl reload apache2` (recarga suave). Biblioteca 3,6 MB → 589 KB y N3 1,5 MB → 325 KB transferidos.
Health check: `/api/salud` OK; `onelingo-api` online sin reinicio; `.env` igual; APK, avatar y assets 200; dlex responde.
Resultado: OK. Lock creado y liberado.
Rollback:
```bash
ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; B=backups/20260930-edu-6-pulido; mv web staging/20260930-edu-6-pulido/web-retirada-post && cp -al $B/web-anterior web'
# gzip: cp $B/apache-onelingo-le-ssl.conf.bak "$(readlink -f /etc/apache2/sites-enabled/onelingo.hostingcuenca.com-le-ssl.conf)" && apache2ctl configtest && systemctl reload apache2
```

## Release: 20260930-edu-7-n3-n4

Fecha: 2026-09-30 · Responsable: Claude (Claude Code)
Contenido: N3 completo (C91–C100, autoría compacta con GO independiente) y N4 completo (100 clases, B1 consolidación, mapa v2 revisado; autor y revisor distintos, constructor con control real de léxico). Total publicado: N1–N4, 400 clases y 5.200 ejercicios. Solo assets web (app sin cambios de código).
Commit: `842b72b` · Build: `main.dart.js` `e6eca1c7…` (igual que edu-6); biblioteca `d24eda6b…`.
Pruebas: 176 Flutter (1 omitida), validar_ruta 10 idiomas 0 errores, construir_bloque OK en los 20 bloques de N4.
Backup: `/var/www/onelingo/backups/20260930-edu-7-n3-n4/web-anterior` (= edu-6), `env.sha256`.
Health: `/api/salud` 200, `onelingo-api` online sin reinicio, `.env` igual, APK/avatar 200, `n4-editorial.json` servido con gzip. Lock creado y liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20260930-edu-7-n3-n4/web-retirada-post && cp -al backups/20260930-edu-7-n3-n4/web-anterior web'`

## Release: 20260930-edu-8-n5-n6

Fecha: 2026-09-30 · Responsable: Claude (Claude Code)
Contenido: N5 (B2 entrada) y N6 (B2 consolidación) completos, 100 clases cada uno, autoría compacta con revisión independiente GO. Total publicado N1–N6: 600 clases. App: rúbricas de escritura con flexión de la última palabra; validadores con números con símbolo y variantes UK/US.
Commit: `c774806` (+ `cdb57b7`) · Build: `main.dart.js` `2d5759d1…`; biblioteca `4b4fd601…`.
Pruebas: 177 Flutter (1 omitida), validar_ruta 0 errores, construir_bloque OK en N5 y N6.
Backup: `/var/www/onelingo/backups/20260930-edu-8-n5-n6/web-anterior` (= edu-7). Health: salud, APK, avatar y `n6-editorial.json` 200; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20260930-edu-8-n5-n6/web-retirada-post && cp -al backups/20260930-edu-8-n5-n6/web-anterior web'`

## Release: 20260930-edu-9-n7-n9

Fecha: 2026-09-30 · Responsable: Claude (Claude Code)
Contenido: N7 (B2 dominio), N8 (C1 inicial) y N9 (C1 profesional) completos, 100 clases cada uno, autoría compacta con revisión independiente GO. Total publicado N1–N9: 900 clases. Palabras libres nuevas: ah, Naples.
Commit: `978dddd` (+ `fa195b1`) · Build: `main.dart.js` `2d5759d1…` (sin cambios de código); biblioteca `348268a8…`.
Pruebas: 177 Flutter (1 omitida), validar_ruta 0 errores, construir_bloque OK en N8 y N9.
Backup: `/var/www/onelingo/backups/20260930-edu-9-n7-n9/web-anterior` (= edu-8). Health: salud, APK, avatar y `n9-editorial.json` 200; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20260930-edu-9-n7-n9/web-retirada-post && cp -al backups/20260930-edu-9-n7-n9/web-anterior web'`

## Release: 20260930-edu-10-n10-ingles-completo

Fecha: 2026-09-30 · Responsable: Claude (Claude Code)
Contenido: N10 (C1 dominio) completo, 100 clases con revisión independiente GO. **Inglés N1–N10 completo: 1.000 clases, 13.002 variantes, 1.000 activas.** `validar_ruta.py` recorre los prerrequisitos de forma iterativa (la cadena de ~1.000 unidades superaba el límite de recursión).
Commit: `d6502aa` · Build: `main.dart.js` `2d5759d1…` (sin cambios de código); biblioteca `e1bca6ef…` (servida igual; 2,5 MB con gzip).
Pruebas: 177 Flutter (1 omitida), validar_ruta 0 errores en 10 idiomas, construir_bloque OK en los 20 bloques de N10, 1.000/1.000 clases enriquecidas con GO.
Backup: `/var/www/onelingo/backups/20260930-edu-10-n10-ingles-completo/web-anterior` (= edu-9). Health: salud, APK, avatar, `n10-editorial.json` y biblioteca 200; `curso.json` sirve n8–n10 «publicado»; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20260930-edu-10-n10-ingles-completo/web-retirada-post && cp -al backups/20260930-edu-10-n10-ingles-completo/web-anterior web'`

## Release: 20260930-edu-11-c1-dificultad

Fecha: 2026-09-30 · Responsable: Claude (Claude Code)
Contenido: pase de dificultad C1 en N8–N10 (60 bloques, 300 clases) con puerta medible en el constructor (`"pase": "c1"`) y revisión independiente GO por bloque. Estímulos de ~15 → 40–46 palabras; vocabulario 8,5 → 12 entradas por clase; frases de enseñanza 12 → 20–23 palabras; la correcta es la única opción más larga en 13–14 % (antes 42–51 %). Español neutro (municipio, auto, boleto, celular…). App: opciones y bancos de palabras siempre barajados (y nunca en el orden correcto) en lecciones antiguas y en el diagnóstico.
Commit: `5422ab3` · Build: `main.dart.js` `8c57e0a0…`; biblioteca `0d281c1b…` (servida igual).
Pruebas: 178 Flutter (1 omitida), validar_ruta 0 errores en 10 idiomas, 1.000/1.000 clases con GO, 60/60 bloques C1 con GO y construcción en orden.
Backup: `/var/www/onelingo/backups/20260930-edu-11-c1-dificultad/web-anterior` (= edu-10). Health: salud, APK, avatar y `n10-editorial.json` 200; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20260930-edu-11-c1-dificultad/web-retirada-post && cp -al backups/20260930-edu-11-c1-dificultad/web-anterior web'`

## Release: 20260930-edu-12-prueba-nivel-v2

Fecha: 2026-09-30 · Responsable: Claude (Claude Code)
Contenido: prueba de nivel v2 de inglés (DEC-025, `DIAGNOSTICO_V2.md`): ~8 min, adaptativa bayesiana por habilidad (escucha, lectura, gramática, vocabulario; escritura omitible), «empiezo de cero» sin examen, resultado por habilidad y elección N−1/N/N+1. Banco de 180 ítems (18 por nivel) con revisión independiente GO. El registro guarda el nivel en la escala del curso. Los demás idiomas siguen con el diagnóstico anterior.
Commit: `8b93e3f` · Build: `main.dart.js` `7593f3ad…`; banco `diagnostico-v2.json` `16c0c6a5…` (servidos iguales).
Pruebas: 186 Flutter (1 omitida), validar_ruta 0 errores, validar_diagnostico 10/10 OK con GO. Navegador (build local): alumno N5 simulado → «N5 · B2» en 19 preguntas; respuestas al azar → «Empiezas desde cero». Se detectó y corrigió en esa prueba que los `completar` con opciones se corregían siempre como error.
Backup: `/var/www/onelingo/backups/20260930-edu-12-prueba-nivel-v2/web-anterior` (= edu-11). Health: salud, APK, avatar y banco 200; `.env` igual; lock liberado. Producción muestra la nueva pantalla en `/#/prueba-nivel`.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20260930-edu-12-prueba-nivel-v2/web-retirada-post && cp -al backups/20260930-edu-12-prueba-nivel-v2/web-anterior web'`

## Release: 20260930-edu-13-lumo-feedback

Fecha: 2026-09-30 · Responsable: Claude (Claude Code)
Contenido: Lumo reacciona al responder. Panel inferior al estilo Duolingo (sube por encima de la barra de navegación) con Lumo, ✓/✗, título, explicación con scroll propio y **SIGUIENTE** siempre visible: verde con Lumo feliz (celebra/anima alternados) al acertar; rojo con Lumo triste amable (error-amable) al fallar, con «Intentar otra vez» en práctica. Aplica a la ruta, la prueba de nivel y las lecciones antiguas; el resto de pantallas usa el mismo componente con Lumo y colores nuevos. Lumo pensando en las pistas y sorprendido al completar unidad. 6 poses nuevas del cliente optimizadas (5,3 MB → 149 KB, WebP 360 px); fuentes en `output/imagegen/mascotas/fuente/`.
Commit: `469c40b` · Build: `main.dart.js` `6e0d55f7…`.
Pruebas: 189 Flutter (1 omitida); navegador (build local, móvil): acierto y error verificados visualmente.
Backup: `/var/www/onelingo/backups/20260930-edu-13-lumo-feedback/web-anterior` (= edu-12). Health: salud, APK, avatar y poses 200; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20260930-edu-13-lumo-feedback/web-retirada-post && cp -al backups/20260930-edu-13-lumo-feedback/web-anterior web'`

## Release: 20260930-edu-14-lumo-animado

Fecha: 2026-09-30 · Responsable: Claude (Claude Code)
Contenido: Lumo animado y siempre visible. Causa de «a veces no se ve»: en web cada imagen se descarga la primera vez que se dibuja y el panel aparecía antes. Arreglo: las 7 imágenes fijas se precargan al abrir la app y las animaciones (6 del cliente, optimizadas 6,6 → 2,7 MB: 216 px, 8 fps) en segundo plano; mientras la animación no está lista se ve la fija (mismo encuadre = sin salto). Reglas del cliente: sin rebote en el panel, nunca dos personajes a la vez (Lumo escucha solo antes de responder; feedback inline sin Lumo), prueba de nivel sin Lumo.
Commit: `787b65d` · Build: `main.dart.js` `7e121796…`.
Pruebas: 190 Flutter (1 omitida); navegador (build local, móvil): fijas precargadas al inicio y animaciones descargadas en segundo plano; prueba de nivel sin Lumo.
Backup: `/var/www/onelingo/backups/20260930-edu-14-lumo-animado/web-anterior` (= edu-13). Health: salud, APK, avatar y poses 200; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20260930-edu-14-lumo-animado/web-retirada-post && cp -al backups/20260930-edu-14-lumo-animado/web-anterior web'`

## Release: 20260930-edu-15-lumo-escucha

Fecha: 2026-09-30 · Responsable: Claude (Claude Code)
Contenido: Lumo escucha (pata en la oreja, animado) en todos los ejercicios de audio: elegir/escuchar, escucha y ordena/completa, dictado y «escucha y escribe» de las lecciones antiguas; también en el coach de las pantallas de listening (Práctica, Fundamentos, unidades de escucha), donde antes salía Nara. Se oculta al abrir el panel de resultado (nunca dos personajes) y no aparece en la prueba de nivel.
Commit: `acd6e77` · Build: `main.dart.js` `eb9bdc46…`.
Pruebas: 192 Flutter (1 omitida), incluida `lumo_escucha_test.dart`; navegador (build local): coach de Práctica con Lumo escucha.
Backup: `/var/www/onelingo/backups/20260930-edu-15-lumo-escucha/web-anterior` (= edu-14). Health 200; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20260930-edu-15-lumo-escucha/web-retirada-post && cp -al backups/20260930-edu-15-lumo-escucha/web-anterior web'`

## Releases 20260930-edu-16 a edu-19 — Tutor con IA fluido e integrado

Fecha: 2026-09-30 · Responsable: Claude (Claude Code). Detalle y plan: `TUTOR_AVATAR_V2.md`.
- **edu-16-tutor-fluido** (`e56d3b7`): modelos 3D 24 → 4–5 MB (texturas 1024 WebP, visemas intactos), saludo en paralelo a la carga, fin de turno por 1,2 s de silencio (avatar y chat), boca por bandas de frecuencia, estados pensando/escuchando; Nara vuelve al coach de escucha.
- **edu-17-avatar-ligero** (`258148a`): geometría y formas de la cara con meshopt → modelos 1,5–2,1 MB (antes 22–28 MB); decodificador meshoptimizer 0.25 (MIT). Medido en producción: GLB de Amara 2,1 MB en ~3 s.
- **edu-18-tutores-integrados** (`468ae63`): visor en tema claro de la app, brazos con caída natural, plano de videollamada, retratos regenerados desde el 3D (WebP ~20 KB).
- **edu-19-tutores-ia** (`002774c`, `main.dart.js` `a03d7333…`): pantalla nativa única «Tutores con IA» (/tutores) con videollamada 3D y chat de voz/texto; /avatar/:id abre la videollamada integrada con la cabecera y las pestañas de la app.
Pruebas: 194 Flutter (1 omitida); navegador (build local y producción): galería, videollamada integrada, carga del modelo, boca con audio.
Backups: `/var/www/onelingo/backups/20260930-edu-1{6,7,8,9}-*/web-anterior` (cada uno = el anterior). Health 200 en todos; `.env` igual; lock liberado.
Rollback (a edu-15): `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20260930-edu-16-tutor-fluido/web-retirada-post && cp -al backups/20260930-edu-16-tutor-fluido/web-anterior web'`

## Release: 20261001-edu-20-tutores-v2

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). Autorizado por el cliente: cambio de servidor y reinicio del backend. Detalle: `TUTOR_AVATAR_V2.md` (Fase 2).
Contenido:
- **Lumo que habla** (2D, base sin boca + 6 bocas de `assets/img/mascotas/lumo-habla`, regeneradas a 720 px desde las maestras; ~80 KB): tutor destacado en «Tutores con IA», voz Jessica (ElevenLabs), boca por energía de bandas normalizada (A/E/O/U/M), inclinación leve al pensar, sin rebotes.
- **Voz frase a frase**: el backend emite `frase` por cada frase terminada; el visor reproduce la primera en streaming y precarga las siguientes. Medido con el proveedor real: primera frase 0,76–1,5 s frente a respuesta completa 1,0–1,8 s.
- **Pedagogía**: personalidades distintas para los 10 tutores 3D + Lumo; prompt en tres capas (personaje · diseño pedagógico · alumno) con reglas de videollamada (reacción breve primero, corrección por reformulación natural, 2–3 frases); tarjetas de corrección, ideas para responder, traducción a demanda; «Terminar llamada» → resumen (logros, a mejorar, vocabulario, siguiente paso) guardado como `eventos.resumen_tutor` y usado al abrir la siguiente llamada («hechos del alumno»). Nuevo endpoint `POST /chat/resumen`; evento SSE `frase` (Flutter lo ignora: compatible).
- **Modelos 3D** 1,6–2,2 → 1,1–1,4 MB (0,75–1,0 MB con gzip), mismas 32 expresiones; mirada (arriba al pensar), encuadre con la cabeza completa, boca 3D con bandas normalizadas.
- **Arreglos**: «Enviar mensaje» quedaba desactivado (un comentario se tragaba `stage.dataset.loaded`); sin sesión la videollamada pide iniciarla.
- **Servidor (Apache, vhost OneLingo)**: compresión para JS, WASM, GLB, fuentes, SVG y JSON (el `AddOutputFilterByType` del vhost anulaba el global); tipo `image/webp`; caché: modelos/retratos/Lumo versionados 1 año `immutable`, vendor 30 días, imágenes y fuentes 1 día, JSON y JS del visor `no-cache`. `main.dart.js` 4,16 → 1,22 MB en la red; GLB de Amara 2,2 → 0,99 MB; three.js 603 → 118 KB. `configtest` OK y `reload` (sin reinicio).
Commits: `2f16716`, `0ed0ee3` · Build: `main.dart.js` `05ef68d8…`.
Pruebas: 194 Flutter (1 omitida); backend 15 (`tutor-frases.test.ts` nuevo) + `tsc` en staging del servidor; navegador (build local): Lumo carga y cambia de boca con audio (A 32 %, E 27 %, M 25 %, O 10 %, U 6 %; ~7,6 cambios/s), flujo simulado completo (frases en cola, tarjetas, ideas, resumen), Amara con modelo comprimido = mismo encuadre que el original; producción: cabeceras de compresión/caché, galería con Lumo, visor sin sesión; proveedor real en el servidor: frases, correcciones, voz de Lumo y resumen.
Backups: `/var/www/onelingo/backups/20261001-edu-20-tutores-v2/` (`web-anterior` = edu-19, `backend-src` = 5 archivos previos, `apache-onelingo-le-ssl.conf`). Backend reiniciado 2 veces (`pm2 restart onelingo-api`; la 2.ª para el ajuste de correcciones); salud OK; `.env` igual; lock liberado.
Rollback:
```
ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; B=backups/20261001-edu-20-tutores-v2; mv web staging/20261001-edu-20-tutores-v2/web-retirada-post && cp -al $B/web-anterior web; cp -a $B/backend-src/backend/src/. backend/src/ && pm2 restart onelingo-api; R=$(readlink -f /etc/apache2/sites-enabled/onelingo.hostingcuenca.com-le-ssl.conf); cp -a $B/apache-onelingo-le-ssl.conf "$R" && apache2ctl configtest && systemctl reload apache2'
```

## Release: 20261001-edu-21-llamada

Fecha: 2026-10-01 · Responsable: Claude (Claude Code).
Causa del «Cargando Lumo…» infinito (iPhone, iOS 18.7, visto en el log de Apache: cargaba el visor pero nunca pedía las imágenes ni `/api/chat`): el visor esperaba `AudioContext.resume()`, que en iOS (y en navegadores con autoplay bloqueado) no se resuelve sin un toque dentro del propio iframe; el toque en la tarjeta de Flutter no cuenta. Afectaba también a los tutores 3D.
Contenido: la carga ya no espera al audio; botón «Llamar a <tutor>» (el toque desbloquea audio, `<audio>` con un WAV silencioso y micrófono); el personaje y el saludo (texto + voz por frases) se preparan antes y contesta al instante; manos libres como Duolingo Video Call / modo voz de ChatGPT: micrófono abierto toda la llamada, escucha al terminar el tutor, pausa de 1,2 s = enviar, 15 s sin hablar = deja de escuchar; tocar al tutor lo interrumpe; silenciar y colgar (resumen); la galería oculta ya no se dibuja en modo integrado. Solo web (backend y Apache sin cambios).
Commit: `41ab9b9` · Build: `main.dart.js` `731da52f…`.
Pruebas: navegador (build local) con `resume()` bloqueado hasta el toque (simulación de iOS) y micrófono simulado: Lumo carga y el saludo queda precargado sin sonar; al tocar «Llamar» habla al instante; escucha sola; habla + pausa → transcribe, envía y Lumo responde; tocar interrumpe; colgar muestra el resumen. `flutter analyze` sin incidencias.
Backup: `/var/www/onelingo/backups/20261001-edu-21-llamada/web-anterior` (= edu-20). Health 200; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261001-edu-21-llamada/web-retirada-post && cp -al backups/20261001-edu-21-llamada/web-anterior web'`

## Release: 20261001-edu-22-llamada-entrante

Fecha: 2026-10-01 · Responsable: Claude (Claude Code).
Causa de «Conectando…» que a veces no conectaba (confirmado: ninguna petición `/api/chat` llegó al backend desde el iPhone): carrera en el visor. Avisaba a la app antes de cargar `topics.json`; si el `init` llegaba antes (habitual en móvil), `requestTutor` leía `units` sin inicializar, lanzaba un error fuera del `try` y dejaba `busy=true`: el saludo nunca se pedía y la llamada esperaba para siempre.
Contenido: roster y temas se cargan antes de avisar; `requestTutor` nunca deja `busy` colgado; el tutor empieza a hablar solo si el navegador permite audio sin toque (escritorio, Android) y, si no (iPhone), pantalla de llamada entrante «<Tutor> te está llamando · Contestar» (en lugar de «está listo» + silencio); vigilante: a los 7 s sin voz cancela y reintenta (2 veces) y luego avisa con «Volver a llamar»; carga de Lumo con `load` + `decode()` con límite (en segundo plano `decode()` podía no resolverse). Solo web.
Commit: `625c83f` · Build: `main.dart.js` `9e2c1d21…`.
Pruebas (navegador, build local con servidor simulado): iPhone simulado (audio bloqueado sin toque) → llamada entrante, al contestar habla al instante; audio permitido → empieza a hablar solo (1,6 s); saludo colgado → reintento a los 7 s y habla (8,9 s); pestaña oculta → Lumo carga.
Backup: `/var/www/onelingo/backups/20261001-edu-22-llamada-entrante/web-anterior` (= edu-21). Health 200; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261001-edu-22-llamada-entrante/web-retirada-post && cp -al backups/20261001-edu-22-llamada-entrante/web-anterior web'`

## Release: 20261001-edu-23-llamada-v3

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). Reinicio de `onelingo-api` autorizado por el cliente en esta sesión.
Datos que motivaron el cambio (logs de prod): turno de voz = transcripción 1,1–2,7 s + primera frase IA ~1,1 s + voz 0,2–0,3 s + 1,2 s de silencio de espera; tras «I like to read books» el backend registró `Respuesta rechazada` (fallo pasajero, no reproducible 4/4) y el visor se quedó esperando sin aviso.
Contenido:
- Web: pantalla de llamada a pantalla completa (tutor centrado, cabecera con nombre y duración, tema en botón con hoja de temas, subtítulos con traducción a demanda y «Repetir», corrección en una línea y conversación/resumen en hoja inferior); **mantener pulsado para hablar** como WhatsApp (desliza a la izquierda para cancelar; teclado opcional); la voz suena por `<audio>` sin WebAudio y la boca sigue una envolvente precalculada (`web/avatar/voz.js`, calibrada con 6 voces) — en iPhone el micrófono cambiaba la frecuencia del AudioContext y entrecortaba la voz; errores visibles con «Reintentar» (reenvía el audio si no se transcribió); Flutter sin cabecera propia en la llamada (la flecha está en el visor). Si el backend no tiene `/chat/voz` (404), transcribe y responde en dos pasos.
- Backend (`ia.ts`, `ia_openai.ts`, `routes/chat.ts`): `POST /chat/voz` (audio → evento `transcripcion` → frases, en una petición); reintento único si el proveedor falla antes de emitir nada; `suggestions` sin mínimo (un turno fallaba tras hablar si la IA daba una sola idea); Lumo conversador con vida propia (reacciona, comparte y pregunta sobre lo mismo); detalle del rechazo en el log.
Commit: `5f15691` · Build: `main.dart.js` `a0ea11d1…`.
Pruebas: backend 17 (nuevas `chat-voz.test.ts`: transcripción→respuesta y reintento) + `tsc` en staging; Flutter 194 (1 omitida); navegador con servidor y micrófono simulados (390×700): llamada entrante sin subtítulos previos, contestar → habla en 40 ms con bocas M/E/A/U, mantener/soltar → transcripción y respuesta, deslizar cancela sin petición, fallo → Reintentar, temas, teclado, colgar → resumen, tutor 3D con la nueva fuente, respaldo 404 → /transcribir + /chat.
Backup: `/var/www/onelingo/backups/20261001-edu-23-llamada-v3/` (`web-anterior` = edu-22, `backend-src` = 3 archivos previos). Salud OK; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; B=backups/20261001-edu-23-llamada-v3; mv web staging/20261001-edu-23-llamada-v3/web-retirada-post && cp -al $B/web-anterior web; cp -a $B/backend-src/backend/src/. backend/src/ && pm2 restart onelingo-api'`

## Release: 20261001-edu-24-lecciones-ia

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). Reinicio de `onelingo-api` autorizado por el cliente.
Contenido:
- **Escritura revisada por IA** (`POST /ejercicios/revisar`, `revisarEscritura` en `ia.ts`): si la frase no coincide exactamente con una respuesta aceptada, o es producción abierta (antes solo contaba palabras), la IA decide por significado y corrección, exige la estructura practicada (p. ej. present perfect) y explica qué cambiar; el panel muestra «Corrección»/«Más natural», la explicación y «Otra forma» (el modelo). Coincidencia exacta = sin IA. Sin sesión/conexión = corrección local. La prueba de nivel no la usa. Probado con el proveedor real: acepta sinónimos y otro orden, rechaza pasado simple cuando se pide present perfect, «has repair», respuesta incompleta y tiempos mezclados (1–2 s).
- **Botones fijos**: COMPROBAR/SIGUIENTE quedan abajo y siempre visibles; el ejercicio se desplaza.
- **Lecciones más dinámicas** (clases N1–N10): «Une las parejas» con el vocabulario de la clase y «Escribe en inglés» con un ejemplo de la clase cuando el bloque no los tiene; formatos alternados. En las 1.000 clases: unir ≈7 → 14 %, escribir ≈9 → 13 %, elegir ≈34 → 29 %; mismo tipo seguido 7 %. Fundamentos conserva su secuencia.
- **Llamada**: zona inferior de alto fijo; el tutor y el micrófono no se mueven con subtítulos largos (el texto se desplaza dentro).
Commit: `31b1cf6` · Build: `main.dart.js` `9aa5892f…`.
Pruebas: backend 18 (nueva `revisar-escritura.test.ts`) + `tsc` en staging; Flutter 197 (1 omitida; nuevas `ejercicios_dinamicos_test.dart`: variedad en todas las clases, IA acepta otra forma, sin IA si coincide); navegador: tutor y micrófono a la misma altura con texto corto y largo.
Backup: `/var/www/onelingo/backups/20261001-edu-24-lecciones-ia/` (`web-anterior` = edu-23, `backend-src` = app.ts e ia.ts previos). Salud OK; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; B=backups/20261001-edu-24-lecciones-ia; mv web staging/20261001-edu-24-lecciones-ia/web-retirada-post && cp -al $B/web-anterior web; cp -a $B/backend-src/backend/src/. backend/src/ && rm -f backend/src/routes/ejercicios.ts && pm2 restart onelingo-api'`

## Release: 20261001-edu-25-nivel0

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). Decisiones del cliente: Nivel 0 nuevo (no se toca Fundamentos), Mapa de Sonidos propio, emoji y Lumo como guía, imágenes buscadas en internet (no generadas).
Contenido: **Nivel 0 · Leer y pronunciar** (inglés general americano, voz Matilda `sofia`), pista propia antes de Fundamentos que no altera la ruta ni sus reglas de léxico.
- Contenido: `assets/contenido/en/nivel0/` → `sonidos.json` (19 sonidos de vocal con imagen ancla y color; marcas de muda, dígrafo y e mágica) y `nivel0.json` con las unidades 1–3 (12 lecciones): Hello! de oído y «una letra, varios sonidos»; el abecedario y deletrear; primeros sonidos s a t i p n m d con frases decodificables.
- App: lector de lecciones (`lib/features/nivel0/`) con pasos escuchar, mirar, juntar sonidos (letras que se iluminan, lento → rápido), toca el sonido, pares mínimos, significado, letras, deletreo, construir con fichas, cambiar una letra, repetir con micrófono (IA compara) y leer frases tocables; panel de resultado con Lumo; botón tortuga; progreso por lección (`nivel0:en:<id>`) y desbloqueo en orden; Mapa de Sonidos; tarjeta en Aprender (inglés) y el botón de Inicio lleva al Nivel 0 a quien empezó de cero (`nivel0Pendiente`).
- Imágenes: 44 emoji Noto (Google, Apache 2.0) en WebP, créditos en `assets/img/emoji/CREDITOS.md`.
- Pendiente: unidades 4–14 y prueba final; audio de sonidos puros (por ahora se enseña con palabras clave y versión lenta).
Commit: `c26422d` · Build: `main.dart.js` `3985f80e…`.
Pruebas: Flutter 202 (1 omitida) + `nivel0_test.dart` (marcado, coherencia del contenido: sonidos, imágenes, respuestas, fichas y cambios de letra; lección completa con progreso); navegador (390×760): portada del Nivel 0, colores de apple/cake/car/about, botones Escuchar/Lento, juntar sonidos, sat/sit con panel, tarjeta en Aprender. Arreglos durante la prueba: botón Lento invisible (ancho infinito del tema en una fila), doble toque en COMPROBAR abría dos paneles y saltaba un paso, imágenes que tardaban (precarga por lección).
Backup: `/var/www/onelingo/backups/20261001-edu-25-nivel0/web-anterior` (= edu-24). Health 200; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261001-edu-25-nivel0/web-retirada-post && cp -al backups/20261001-edu-25-nivel0/web-anterior web'`

## Release: 20261001-edu-26-limpieza-prueba-nivel

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). Solo web; backend sin cambios y sin reinicios.
Contenido: fases A y B de la hoja de ruta (DEC-026, DEC-027, `docs/ARQUITECTURA_VIGENTE.md`).
- Estética única: `BotonPrincipal` fijo, `OpcionRespuesta` y `FeedbackDock` en lecturas, escuchas, gramática, lecciones y examen de otros idiomas y en la prueba antigua; el tema estiliza `FilledButton`.
- Sin selectores de nivel («Nivel interno», «Nivel de práctica», «Explorar nivel») y sin jerga interna.
- Retirada la biblioteca de práctica antigua. La Biblioteca nueva tiene Lecturas, Escuchas, Guías de gramática y Mapa de sonidos.
- Ubicación a prueba de azar: techo bayesiano en la prueba antigua; prueba obligatoria en el registro de todos los idiomas; no se puede empezar por encima del resultado.
- Prueba para subir de nivel: 20 preguntas y 16 para aprobar. Aprender muestra cada nivel como superado, en curso, opcional o bloqueado.
Commit: `20b3feb` · Build: `main.dart.js` `c5d0454a…` (servido igual).
Pruebas: Flutter 213; análisis sin errores ni avisos. Nuevas: `arquitectura_test`, `prueba_nivel_test`, azar en `diagnostico_test`, `lectura_escucha_test`, `guias_gramatica_test`. Navegador (400×820): niveles con estado, tarjeta y prueba del nivel con botón fijo, Biblioteca → Lecturas en el nivel del alumno.
Backup: `/var/www/onelingo/backups/20261001-edu-26-limpieza-prueba-nivel/web-anterior` (= edu-25). Salud 200; `.env` igual; APK, avatar y Nivel 0 servidos; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261001-edu-26-limpieza-prueba-nivel/web-retirada-post2 && cp -al backups/20261001-edu-26-limpieza-prueba-nivel/web-anterior web'`

## Release: 20261001-edu-27-situaciones-tramos

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). El cliente autorizó el reinicio de `onelingo-api` de esta release.
Contenido: fase C (DEC-028, `SITUACIONES_V2.md`).
- Las 50 situaciones en 3 tramos: Básico N1–3, Intermedio N4–6 y Avanzado N7–10.
- Pantalla nueva: selector de tramo según el nivel del alumno, avance, objetivos con chat o videollamada, palabras, frases y prueba de 10 preguntas con nota.
- La videollamada se abre en el tema y objetivo elegidos.
- Fuente única con copias generadas.
- Servidor: `situaciones.ts`, `chat.ts` y `situaciones-en.json` nuevos, con objetivos de los tres tramos y material del tramo; retirado `situational-vocabulary-en.json`. Se desplegaron solo esos archivos; el `config.ts` de producción no se toca.
Commit: `b5dfe8a` · Build: `main.dart.js` `043f7b0e…`.
Pruebas:
- Flutter 216 (1 omitida); backend 19.
- `tsc` en staging con el backend de producción.
- Navegador (400×820): situación 1 en nivel 5, con Intermedio como «Tu nivel», Avanzado bloqueado y la prueba con su panel de respuesta.
- En producción: `objetivoValido('en',1,'s1-i1')` y `('en',1,'s1-a2')` dan true; `('en',2,'s1-i1')` da false.
Backup: `/var/www/onelingo/backups/20261001-edu-27-situaciones-tramos/` (`web-anterior` = edu-26; `backend-src` con los 4 archivos previos). Salud 200; `.env` igual; APK servido; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; B=backups/20261001-edu-27-situaciones-tramos; mv web staging/20261001-edu-27-situaciones-tramos/web-retirada-post2 && cp -al $B/web-anterior web; cp -a $B/backend-src/backend/src/. backend/src/ && pm2 restart onelingo-api'`

## Release: 20261001-edu-28-palabras-verbos

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). Solo web; backend sin cambios y sin reinicios.
Contenido: fase D (DEC-029).
- Léxico único calculado desde ruta, situaciones y Nivel 0.
- «Mis palabras»: repaso espaciado por palabra y sesiones de 10, agrupadas por nivel o situación.
- «Mis verbos»: 174 verbos con 5 tablas, audio por persona y práctica de irregulares.
- Biblioteca y Perfil enlazados.
Commit: `913346c` · Build: `main.dart.js` `0b1d1590…`.
Pruebas: Flutter 221 (1 omitida), con la nueva `lexico_test.dart`. Navegador (400×820): Mis palabras con 20 palabras de dos situaciones, sesión de repaso y tabla de «go».
Backup: `/var/www/onelingo/backups/20261001-edu-28-palabras-verbos/web-anterior` (= edu-27). Salud 200; `.env` igual; APK y `verbos.json` servidos; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261001-edu-28-palabras-verbos/web-retirada-post2 && cp -al backups/20261001-edu-28-palabras-verbos/web-anterior web'`

## Release: 20261001-edu-29-frances-nivel0

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). El cliente autorizó el reinicio de `onelingo-api` de esta release.
Contenido: primera entrega de francés (DEC-030).
- Voces nativas: Hélène narra y Nicolas dialoga; solo cambia `voz.ts` en el servidor.
- Nivel 0 multilingüe y francés F1–F5 (20 lecciones, mapa de 15 sonidos, 70 emoji Noto).
Commit: `3ad21f7` · Build: `main.dart.js` `ecfd5f3c…`.
Pruebas: Flutter 222 (1 omitida); backend 20; `tsc` en staging. Navegador: Nivel 0 francés (portada, lección 1 «papa» con la a roja). En producción, `rolDeVoz(narradora, fr)` = Hélène.
Backup: `/var/www/onelingo/backups/20261001-edu-29-frances-nivel0/` (`web-anterior` = edu-28; `backend-src` con el `voz.ts` previo). Salud 200; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; B=backups/20261001-edu-29-frances-nivel0; mv web staging/20261001-edu-29-frances-nivel0/web-retirada-post2 && cp -al $B/web-anterior web; cp -a $B/backend-src/backend/src/. backend/src/ && pm2 restart onelingo-api'`

## Release: 20261001-edu-30-interfaz-ingles

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). Solo web; backend sin cambios y sin reinicios. Publicada por indicación del cliente tras pasar las pruebas.
Contenido: I1 (DEC-031).
- Interfaz en inglés: 939 textos.
- Selector «Idioma de la app» en Perfil.
- Primera visita en el idioma del dispositivo; la interfaz cambia al elegir el idioma nativo en el registro.
- Nombres de situaciones, idiomas y niveles traducidos.
Commit: `d95262f` · Build: `main.dart.js` `815cf48f…`.
Pruebas: Flutter 226 (1 omitida), con `i18n_test` y la nueva regla de `arquitectura_test`. Navegador (400×820): alumno nativo de inglés que aprende francés, con Home, Learn, Practice y Profile en inglés.
Backup: `/var/www/onelingo/backups/20261001-edu-30-interfaz-ingles/web-anterior` (= edu-29). Salud 200; `.env` igual; APK y `en.json` servidos; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261001-edu-30-interfaz-ingles/web-retirada-post2 && cp -al backups/20261001-edu-30-interfaz-ingles/web-anterior web'`

## Release: 20261001-edu-31-frances-bilingue

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). Solo web; backend sin cambios y sin reinicios.
Contenido: I2 y francés FR-1/FR-2 (DEC-032).
- Nivel 0 francés completo y bilingüe: F1–F10, 40 lecciones.
- Ruta francesa con apoyo en inglés.
- Selector de idioma de la app en la bienvenida, el registro y Perfil.
- `localizarApoyo` para el contenido bilingüe.
Commit: `adbc8f5` · Build: `main.dart.js` `4d499782…`.
Pruebas: Flutter 227 (1 omitida); `validar_nivel0.py fr --bilingue` 0 errores; `validar_ruta.py` 0 errores. Navegador (400×820): alumno nativo de inglés en francés, con el Nivel 0 en inglés (40 lecciones, «Continue: The o and the é»).
Backup: `/var/www/onelingo/backups/20261001-edu-31-frances-bilingue/web-anterior` (= edu-30). Salud 200; `.env` igual; APK servido; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261001-edu-31-frances-bilingue/web-retirada-post2 && cp -al backups/20261001-edu-31-frances-bilingue/web-anterior web'`

## Release: 20261001-edu-32-frances-verbos-situaciones

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). El cliente autorizó el reinicio de `onelingo-api` de esta release.
Contenido: francés FR-3, FR-4 y FR-5b.
- Mis verbos en francés: 120 verbos × 5 tiempos.
- 50 situaciones en francés × 3 tramos, bilingües.
- Aprender e Inicio con niveles de ruta en francés.
- Servidor: `situaciones.ts` (textos de apoyo `{es, en}`) y `situaciones-fr.json`.
Commit: `63c47a1` · Build: `main.dart.js` `9e624c56…`.
Pruebas: Flutter 230 (1 omitida); backend 21; `tsc` en staging. En producción: `situacionesDe('fr')` = 50, `situacionesDe('en')` = 50 y `objetivoValido('fr', 1, 's1-a1')` = true.
Backup: `/var/www/onelingo/backups/20261001-edu-32-frances-verbos-situaciones/` (`web-anterior` = edu-31; `backend-src` con el `situaciones.ts` previo). Salud 200; `.env` igual; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; B=backups/20261001-edu-32-frances-verbos-situaciones; mv web staging/20261001-edu-32-frances-verbos-situaciones/web-retirada-post2 && cp -al $B/web-anterior web; cp -a $B/backend-src/backend/src/. backend/src/ && rm -f backend/src/content/situaciones-fr.json && pm2 restart onelingo-api'`

## Release: 20261001-edu-33-frances-n1-b1-b4

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). Solo web; backend sin cambios y sin reinicios.
Contenido: francés FR-5c, primera tanda del Nivel 1 y plan de clases (DEC-034).
- N1 francés B1–B4: clases 1–20, revisadas con GO y bilingües, con el reparto de personajes coherente.
- Ruta: número de clase dentro del nivel; los niveles futuros muestran el MCER de la escala del cliente.
- Plan de clases: marco común y fichas del francés N1–N2 (no van en la app).
Commit: `436ae3b` · Build: `main.dart.js` `a3944073…`.
Pruebas: Flutter 230 (1 omitida); `validar_ruta.py` 0 errores; `validar_plan.py fr` 0 errores. Navegador: Aprender en francés (Nivel 1 · A1 con 20 clases numeradas 1…20; N2 · A2, N3 · B1), clase 18 con la interfaz en español y clase 8 en inglés.
Lock: había quedado un lock vacío de edu-32 (creado 03:24 UTC, un minuto después de su cambio; producción seguía en el build de edu-32); se retiró antes de tomar el nuevo.
Backup: `/var/www/onelingo/backups/20261001-edu-33-frances-n1-b1-b4/web-anterior` (= edu-32). Salud 200; `.env` igual; APK servido; `n1-b04.json` servido; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261001-edu-33-frances-n1-b1-b4/web-retirada-post2 && cp -al backups/20261001-edu-33-frances-n1-b1-b4/web-anterior web'`

## Release: 20261001-edu-34-frances-n1-b5-b7

Fecha: 2026-10-01 · Responsable: Claude (Claude Code). Solo web (contenido); backend sin cambios y sin reinicios.
Contenido: francés FR-5c, segunda tanda del Nivel 1.
- N1 francés B5–B7: clases 21–35 (café y compras, gustos y rutina, describir y ubicarse), escritas desde sus fichas y revisadas con GO.
- Guías de pronunciación de B1–B4 alineadas con el Nivel 0 (j = «sh», in/un = «en»).
Commit: `80f7188` · Build: `main.dart.js` `a3944073…` (sin cambios de código respecto a edu-33).
Pruebas: Flutter 230 (1 omitida); `validar_ruta.py` 0 errores; `validar_plan.py fr` 0 errores. Navegador: clase 25 con la interfaz en inglés y clase 33 en español.
Backup: `/var/www/onelingo/backups/20261001-edu-34-frances-n1-b5-b7/web-anterior` (= edu-33). Salud 200; `.env` igual; APK servido; `n1-b07.json` servido; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261001-edu-34-frances-n1-b5-b7/web-retirada-post2 && cp -al backups/20261001-edu-34-frances-n1-b5-b7/web-anterior web'`

## Release: 20261002-edu-35-frances-n1-completo

Fecha: 2026-10-02 · Responsable: Claude (Claude Code). Solo web (contenido); backend sin cambios y sin reinicios.
Contenido: francés FR-5c terminado, Nivel 1 completo (50 clases).
- N1 francés B8–B10: clases 36–50 (verbos frecuentes y comida, moverse y planes, fin de semana con passé composé), la prueba tipo DELF A1 (c49) y el proyecto «Ma vie en français» (c50). Escritas desde sus fichas y revisadas con GO.
Commit: `34736b3` · Build: `main.dart.js` `a3944073…` (sin cambios de código).
Pruebas: Flutter 230 (1 omitida); `validar_ruta.py` 0 errores; `validar_plan.py fr` 0 errores. Navegador: prueba del Nivel 1 en francés (20 preguntas, primera «Ordena: ¡Chao, hasta mañana!»).
Backup: `/var/www/onelingo/backups/20261002-edu-35-frances-n1-completo/web-anterior` (= edu-34). Salud 200; `.env` igual; APK servido; `n1-b10.json` servido; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261002-edu-35-frances-n1-completo/web-retirada-post2 && cp -al backups/20261002-edu-35-frances-n1-completo/web-anterior web'`

## Release: 20261002-edu-36-frances-ubicacion-n2

Fecha: 2026-10-02 · Responsable: Claude (Claude Code). Solo web; backend sin cambios y sin reinicios.
Contenido: francés FR-6 y primera tanda de FR-7.
- Prueba de ubicación v2 por idioma: el francés la usa con su banco N1 (18 ítems, GO). Nunca ubica por encima de lo publicado; los alumnos ubicados antes por encima quedan topados sin borrar su diagnóstico; Perfil muestra ese nivel.
- N2 francés B1–B3: clases 1–15 de A2, revisadas con GO.
Commits: `7c33982` (FR-6), `b53e2fb` (N2) · Build: `main.dart.js` `a052b5bf…`.
Pruebas: Flutter 242 (1 omitida), con `ubicacion_idiomas_test` (azar en francés → «desde cero» ≥ 90 %); `validar_diagnostico.py --compilar` inglés sin cambios; `validar_ruta.py` y `validar_plan.py fr` 0 errores. Navegador: prueba de ubicación en francés con la interfaz en inglés («How much French do you know?», dos opciones, escucha con «7 h 45 / 8 h 45 / 8 h 15»).
Backup: `/var/www/onelingo/backups/20261002-edu-36-frances-ubicacion-n2/web-anterior` (= edu-35). Salud 200; `.env` igual; APK servido; `diagnostico-v2.json` (fr) y `n2-b03.json` servidos; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261002-edu-36-frances-ubicacion-n2/web-retirada-post2 && cp -al backups/20261002-edu-36-frances-ubicacion-n2/web-anterior web'`

## Release: 20261002-edu-37-frances-n2-b4-b6

Fecha: 2026-10-02 · Responsable: Claude (Claude Code). Solo web (contenido); backend sin cambios y sin reinicios.
Contenido: francés FR-7, segunda tanda del Nivel 2.
- N2 francés B4–B6: clases 16–30 (planes y predicciones, comparar y elegir productos, restaurante y cocina), escritas desde sus fichas y revisadas con GO.
Commit: `0b579f4` · Build: `main.dart.js` `a052b5bf…` (sin cambios de código respecto a edu-36).
Pruebas: Flutter 242 (1 omitida); `validar_ruta.py` y `validar_plan.py fr` 0 errores. Navegador: N2 clase 28 con la interfaz en español.
Backup: `/var/www/onelingo/backups/20261002-edu-37-frances-n2-b4-b6/web-anterior` (= edu-36). Salud 200; `.env` igual; APK servido; `n2-b06.json` servido; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261002-edu-37-frances-n2-b4-b6/web-retirada-post2 && cp -al backups/20261002-edu-37-frances-n2-b4-b6/web-anterior web'`

## Release: 20261002-edu-38-frances-n2-completo

Fecha: 2026-10-02 · Responsable: Claude (Claude Code). Solo web (contenido); backend sin cambios y sin reinicios.
Contenido: francés FR-7 terminado, Nivel 2 completo (50 clases).
- N2 francés B7–B10: clases 31–50 (viajes y transporte, salud, favores y normas, prueba tipo DELF A2 y proyecto «Un an à Paris»), escritas desde sus fichas y revisadas con GO.
- Banco de ubicación francés N2 (18 ítems, GO): la prueba v2 ubica en francés hasta N2 (36 ítems).
Commits: `d126a88` (N2), `9505cdd` (banco) · Build: `main.dart.js` `a052b5bf…` (sin cambios de código).
Pruebas: Flutter 242 (1 omitida); `validar_ruta.py`, `validar_plan.py fr` y `validar_diagnostico.py --idioma fr` 0 errores. Navegador: prueba de ubicación en francés (dos puntos de partida; sube de N1 a N2 si acierta).
Backup: `/var/www/onelingo/backups/20261002-edu-38-frances-n2-completo/web-anterior` (= edu-37). Salud 200; `.env` igual; APK servido; `n2-b10.json` y el banco (36 ítems) servidos; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261002-edu-38-frances-n2-completo/web-retirada-post2 && cp -al backups/20261002-edu-38-frances-n2-completo/web-anterior web'`

## Release: 20261002-edu-39-frances-n3

Fecha: 2026-10-02 · Responsable: Claude (Claude Code). Solo web (contenido); backend sin cambios y sin reinicios.
Contenido: francés N3 completo (B1 de entrada, 50 clases), escrito desde fichas con plan de ejercicios y revisado bloque a bloque (GO).
Commit: `bc220eb` · Build: `main.dart.js` sin cambios de código.
Pruebas: Flutter 242 (1 omitida); `validar_ruta.py` y `validar_plan.py fr` 0 errores.
Backup: `/var/www/onelingo/backups/20261002-edu-39-frances-n3/web-anterior` (= edu-38). Salud 200; `.env` igual; APK servido; `n3-b10.json` servido; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261002-edu-39-frances-n3/web-retirada-post2 && cp -al backups/20261002-edu-39-frances-n3/web-anterior web'`
