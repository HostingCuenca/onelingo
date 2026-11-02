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

## Release: 20261002-edu-40-frances-n4-n5

Fecha: 2026-10-02 · Responsable: Claude (Claude Code). Solo web (contenido); backend sin cambios y sin reinicios.
Contenido: francés N4 (B1 consolidado) y N5 (B2 de entrada) completos, 100 clases escritas desde fichas con plan de ejercicios y revisadas bloque a bloque (GO); bancos de ubicación N3 y N4 compilados (72 ítems, N1–N4); vocabulario estricto; mínimos de producción abierta ajustados.
Commit: `a779bdc` · Build: `main.dart.js` sin cambios de lógica (solo tests).
Pruebas: Flutter 242 (1 omitida); `validar_ruta.py` y `validar_plan.py fr` 0 errores.
Backup: `/var/www/onelingo/backups/20261002-edu-40-frances-n4-n5/web-anterior` (= edu-39). Salud 200; `.env` igual; APK servido; `n5-b10.json` servido; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261002-edu-40-frances-n4-n5/web-retirada-post2 && cp -al backups/20261002-edu-40-frances-n4-n5/web-anterior web'`

## Release: 20261002-edu-41-frances-n6-n7

Fecha: 2026-10-02 · Responsable: Claude (Claude Code). Solo web (contenido); backend sin cambios y sin reinicios.
Contenido: francés N6 y N7 (B2) completos, 100 clases escritas desde fichas con plan de ejercicios y revisadas bloque a bloque (GO); bancos de ubicación N5 y N6 compilados (108 ítems, N1–N6).
Commit: `3002f02` (build) + `e825e52` (solo palabrasLibres/fichas) · Build: `main.dart.js` sin cambios de lógica.
Pruebas: Flutter 242 (1 omitida); `validar_ruta.py` y `validar_plan.py fr` 0 errores.
Backup: `/var/www/onelingo/backups/20261002-edu-41-frances-n6-n7/web-anterior` (= edu-40). Salud 200; `.env` igual; APK servido; `n7-b10.json` servido; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261002-edu-41-frances-n6-n7/web-retirada-post2 && cp -al backups/20261002-edu-41-frances-n6-n7/web-anterior web'`

## Release: 20261002-edu-42-frances-n8

Fecha: 2026-10-02 · Responsable: Claude (Claude Code). Solo web (contenido); backend sin cambios y sin reinicios.
Contenido: francés N8 (C1) completo, 50 clases escritas desde fichas y revisadas bloque a bloque (GO); bancos de ubicación N7 y N8 compilados (144 ítems, N1–N8).
Commit: `3f46557` · Build: `main.dart.js` sha256 `2bae06ec939a9206…` (API_URL prod).
Pruebas: Flutter 242 (1 omitida); `validar_ruta.py`, `validar_plan.py fr` y `validar_diagnostico.py --idioma fr` 0 errores.
Backup: `/var/www/onelingo/backups/20261002-edu-42-frances-n8/web-anterior` (= edu-41). Salud 200; `.env` igual; APK servido; `n8-b10.json` y `diagnostico-v2.json` servidos; lock liberado. (El primer intento falló antes del intercambio porque faltaba la carpeta de staging; se creó y se completó con el mismo respaldo.)
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261002-edu-42-frances-n8/web-retirada-post2 && cp -al backups/20261002-edu-42-frances-n8/web-anterior web'`

## Release: 20261002-edu-43-frances-n9-n10

Fecha: 2026-10-02 · Responsable: Claude (Claude Code). Solo web (contenido); backend sin cambios y sin reinicios.
Contenido: francés N9 y N10 (C1) completos. Son 100 clases escritas desde fichas y revisadas bloque a bloque (GO); con esto el francés N1–N10 queda completo (500 clases). Bancos de ubicación N9 y N10 compilados (180 ítems, N1–N10).
Commits: `f35290d` (N9), `6d5ceba` (N10), `cf2bb28` (bancos) · Build: `main.dart.js` sha256 `2bae06ec939a9206…` (API_URL prod), igual al servido.
Pruebas: Flutter 242 (1 omitida) con N9–N10; pruebas de ubicación/diagnóstico 40 tras compilar los bancos; `validar_ruta.py`, `validar_plan.py fr` y `validar_diagnostico.py --idioma fr` con 0 errores.
Backup: `/var/www/onelingo/backups/20261002-edu-43-frances-n9-n10/web-anterior` (= edu-42). Verificado:
- salud 200;
- `.env` sin cambios;
- APK, `n9-b01.json`, `n10-b10.json` y `diagnostico-v2.json` servidos;
- `curso.json` con f0, N1–N10 y c2;
- lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261002-edu-43-frances-n9-n10/web-retirada-post2 && cp -al backups/20261002-edu-43-frances-n9-n10/web-anterior web'`

## Release: 20261002-edu-44-frances-tipografia

Fecha: 2026-10-02 · Responsable: Claude (Claude Code). Solo web (contenido); backend sin cambios y sin reinicios.
Contenido: tipografía francesa normalizada en N1–N10, con U+202F antes de ? ! : ; y dentro de « » (184 cadenas publicadas; `tools/contenido/tipografia_fr.py`).
Commit: `4baa44d`. Pruebas: `ruta_contenido_test` 18/18; `validar_ruta.py fr` 0 errores.
Backup: `/var/www/onelingo/backups/20261002-edu-44-frances-tipografia/web-anterior` (= edu-43). Verificado:
- salud 200;
- `.env` sin cambios;
- APK servido;
- `n7-b05.json` servido idéntico al local;
- lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261002-edu-44-frances-tipografia/web-retirada-post2 && cp -al backups/20261002-edu-44-frances-tipografia/web-anterior web'`

## Release: 20261005-edu-45-espanol

Fecha: 2026-10-05 · Responsable: Claude (Claude Code). Web + backend (2 archivos); reinicio de `onelingo-api` autorizado por el cliente para esta release.
Contenido: curso de español para angloparlantes completo (DEC-034): ruta N1–N10 (500 clases, bloques con GO), prueba de ubicación v2 (180 ítems), 50 situaciones × 3 tramos, Nivel 0 «Leer y pronunciar» (5 unidades, 18 lecciones), «Mis verbos» (124), voz del dispositivo es-MX; apoyo solo en inglés (`localizarApoyo` acepta `{en}`).
Commit: `2a79a1c` (build desde worktree limpio de HEAD) · `main.dart.js` sha256 `10edb5126ecadeb8…` (API_URL prod).
Backend: `src/lib/situaciones.ts` (apoyo `{en}`) y `src/content/situaciones-es.json` copiados archivo por archivo; `config.ts` de prod intacto.
Pruebas: Flutter 248 en HEAD limpio («All tests passed!»); backend tsc + 10/10.
Backup: `/var/www/onelingo/backups/20261005-edu-45-espanol/{web-anterior,backend-anterior}` (= edu-44). Verificado:
- `/api/salud` 200 y `onelingo-api` online tras el reinicio;
- `situacionesDe('es')` = 50 en prod;
- `n10-b10.json`, `diagnostico-v2.json`, `situaciones.json`, `nivel0.json` y `verbos.json` del español servidos; APK conservado;
- lock liberado.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261005-edu-45-espanol/web-retirada-post && cp -al backups/20261005-edu-45-espanol/web-anterior web'`
Rollback backend: `ssh -F /dev/null root@167.235.20.41 'cd /var/www/onelingo; cp backups/20261005-edu-45-espanol/backend-anterior/situaciones.ts backend/src/lib/ && rm backend/src/content/situaciones-es.json && pm2 restart onelingo-api'`

## Release: 20261006-edu-46-portugues

Fecha: 2026-10-06 · Responsable: Claude (Claude Code). Web + backend (1 archivo nuevo); sin reinicio de `onelingo-api`.
Contenido: curso de portugués de Brasil completo (DEC-035): ruta N1–N10 (500 clases, bloques con GO, pasada de canon), prueba de ubicación v2 (180 ítems), 50 situaciones × 3 tramos, Nivel 0, «Mis verbos»; `idiomasConRuta` incluye `pt`; apoyo es/en.
Commit: `1d2dfc8` (build desde worktree limpio de HEAD) · `main.dart.js` sha256 `d7b02de9409d106c…` (API_URL prod).
Backend: `src/content/situaciones-pt.json` añadido; `src/lib/situaciones.ts` idéntico al de prod (sin cambios); `config.ts` de prod intacto.
Pruebas: Flutter 258 + 1 omitida en HEAD limpio («All tests passed!»); `validar_ruta.py` 0 errores en todos los idiomas.
Backup: `/var/www/onelingo/backups/20261006-edu-46-portugues/{web-anterior,backend-anterior}` (= edu-45). Verificado:
- `/api/salud` 200;
- `situaciones-pt.json` = 50 situaciones (lectura en node); el proceso carga el archivo de forma perezosa por idioma (si ya había cacheado `pt` vacío antes del despliegue, haría falta reiniciar `onelingo-api`);
- `n10-b10.json`, `diagnostico-v2.json`, `verbos.json` y `situaciones.json` del portugués servidos; APK conservado;
- lock liberado.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261006-edu-46-portugues/web-retirada-post && cp -al backups/20261006-edu-46-portugues/web-anterior web'`
Rollback backend: `ssh -F /dev/null root@167.235.20.41 'rm /var/www/onelingo/backend/src/content/situaciones-pt.json'`

## Release: 20261006-edu-47-aleman

Fecha: 2026-10-06 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat. Web + backend (1 archivo cambiado, 2 nuevos); con reinicio de `onelingo-api`.
Contenido: curso de alemán completo (método ligero, sin historia): ruta N1–N10 (500 clases, 100 bloques con GO), prueba de ubicación v2, 50 situaciones × 3 tramos, Nivel 0, «Mis verbos»; `idiomasConRuta` incluye `de`; apoyo es/en; contenido heredado sin Ecuador.
Commits: `ec8330e`, `ebcb5c0`, `eaa07cd` (build desde worktree limpio de `eaa07cd`) · `main.dart.js` sha256 `698b7838ab045863…` (API_URL prod).
Backend: `src/lib/voz.ts` (voces Petra/Julius para `de` y cifras en palabras), `src/lib/numeros_de.ts` y `src/content/situaciones-de.json` añadidos; `tsc --noEmit` en staging OK; `config.ts` de prod intacto; `.env` sin cambios (hash igual).
Pruebas: Flutter 272 y backend 23/23 en HEAD; validadores 0 errores.
Backup: `/var/www/onelingo/backups/20261006-edu-47-aleman/{web-anterior,backend-anterior}` (= edu-46). Verificado:
- `/api/salud` 200 tras el reinicio; sin errores nuevos en el log;
- staging: «§ 437 … 1921» → «Paragraf vierhundertsiebenunddreißig … neunzehnhunderteinundzwanzig»; `situacionesDe('de')` = 50;
- `curso.json`, `n5-b03.json`, `n10-b10.json` y `situaciones.json` del alemán servidos con el mismo sha256 que el repo; APK conservado;
- lock liberado. La web anterior queda también en `/var/www/onelingo/web-saliente-20261006-edu-47-aleman` (enlaces duros; se puede borrar).
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261006-edu-47-aleman/web-retirada-post && cp -al backups/20261006-edu-47-aleman/web-anterior web'`
Rollback backend: `ssh -F /dev/null root@167.235.20.41 'cd /var/www/onelingo; cp backups/20261006-edu-47-aleman/backend-anterior/voz.ts backend/src/lib/ && rm backend/src/lib/numeros_de.ts backend/src/content/situaciones-de.json && pm2 restart onelingo-api'`

## Release: 20261007-edu-48-chip-idioma

Fecha: 2026-10-07 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat (plan de la semana). Solo web; sin cambios de backend ni reinicio.
Contenido: chip de idioma legible en el registro (antes blanco sobre blanco); contenido viejo retirado de it/ja/ko/ru/zh (`nivel-0/1/2.json`, `ruta/a1-1.json`, `f0` antiguo) y tarjeta «En preparación» mientras esos idiomas no tienen ruta; `vocabularioEstricto` para ru/ko/ja/zh.
Commit: `3bae9e8` (build desde worktree limpio) · `main.dart.js` sha256 `189c6219747b4c49…` (API_URL prod).
Pruebas: Flutter en el worktree, todas en verde salvo `ruta_recorrido_test` «N1 activo entra al recorrido editorial», que falló por tiempo con la máquina cargada y pasa al correrlo solo (5/5); `validar_ruta.py` 10 idiomas, 0 errores.
Backup: `/var/www/onelingo/backups/20261007-edu-48-chip-idioma/web-anterior` (= edu-47). Verificado: `/`, `/api/salud` y `main.dart.js` 200 con el sha256 del build; `it/nivel-1.json` ya no se sirve (404); lock liberado. La web anterior queda también en `/var/www/onelingo/web-saliente-20261007-edu-48-chip-idioma` (enlaces duros; se puede borrar, igual que `web-saliente-20261006-edu-47-aleman`).
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261007-edu-48-chip-idioma/web-retirada-post && cp -al backups/20261007-edu-48-chip-idioma/web-anterior web'`

## Release: 20261007-edu-49-italiano

Fecha: 2026-10-07 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat (plan de la semana: publicar cada idioma al 100 %). Solo web; sin cambios de backend ni reinicio.
Contenido: italiano esencial, Fundamentos (f0) + N1–N4 (200 clases), prueba de ubicación N1–N4 y Nivel 0. N5–N10 aparecen como «Próximamente».
Commit: `fd2cc6e` (incluye `bee468b`; build desde worktree limpio) · `main.dart.js` sha256 `951aab309ecfa276…` (API_URL prod).
Pruebas: Flutter completo en el worktree, 328 en verde. `ruta_recorrido_test` «N1 activo entra al recorrido editorial» falló por tiempo con la máquina cargada; ya fallaba igual en `3bae9e8`, y al repetirlo pasa el archivo entero. `validar_ruta.py`: 10 idiomas, 0 errores.
Pendiente: las voces nativas Luna/Carmelo (`backend/src/lib/voz.ts`, en `bee468b`) no están desplegadas porque requieren reiniciar PM2 con autorización. Mientras tanto, el italiano usa la voz por defecto.
Backup: `/var/www/onelingo/backups/20261007-edu-49-italiano/web-anterior` (= edu-48). Verificado: `/`, `/api/salud`, `main.dart.js` (sha256 del build), `it/ruta/curso.json`, `it/ruta/n4-b10.json` y `it/diagnostico-v2.json` responden 200; lock liberado. La web anterior queda en `/var/www/onelingo/web-saliente-20261007-edu-49-italiano`.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261007-edu-49-italiano/web-retirada-post && cp -al backups/20261007-edu-49-italiano/web-anterior web'`

## Release: 20261007-edu-50-chino

Fecha: 2026-10-07 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat (plan de la semana). Solo web; sin cambios de backend ni reinicio.
Contenido: chino mandarín esencial, con Fundamentos (f0) + N1–N2 (100 clases, pinyin con sandhi), prueba de ubicación N1–N2 y Nivel 0. N3–N10 aparecen como «Próximamente». La rúbrica de escritura para zh/ja ahora busca evidencias sin espacios y mide en caracteres.
Commit: `cc57f11` (build desde worktree limpio) · `main.dart.js` sha256 `772c58d4d466eac0…` (API_URL prod).
Pruebas: Flutter completo en el worktree, 342 en verde. `ruta_recorrido_test` falló por tiempo (inestable, ya conocido) y pasa al repetirlo (5/5). `validar_ruta.py`: 10 idiomas, 0 errores.
Pendiente: voces nativas Shan Shan/Evan (`voz.ts`), que necesitan reiniciar PM2 con autorización. Aún no está desplegado el arreglo del paso `deletreo` del Nivel 0 (`626c969`).
Backup: `/var/www/onelingo/backups/20261007-edu-50-chino/web-anterior` (= edu-49). Verificado: `/`, `/api/salud`, `main.dart.js` (sha256 del build), `zh/ruta/curso.json`, `zh/ruta/n2-b10.json`, `zh/diagnostico-v2.json` e `it/ruta/n4-b10.json` responden 200; lock liberado. La web anterior queda en `/var/www/onelingo/web-saliente-20261007-edu-50-chino`.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261007-edu-50-chino/web-retirada-post && cp -al backups/20261007-edu-50-chino/web-anterior web'`

## Release: 20261007-edu-51-japones

Fecha: 2026-10-07 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat (plan de la semana). Solo web; sin cambios de backend ni reinicio.
Contenido: japonés esencial, con Fundamentos (f0) + N1–N2 (100 clases, kana con rom Hepburn), prueba de ubicación N1–N2 y Nivel 0. N3–N10 aparecen como «Próximamente». También va el arreglo del Nivel 0 (`626c969`): el paso `deletreo` con letras en orden (pt, de, it, ru, ko, ja) ahora es un ejercicio de ordenar con audio, y no un «elegir» roto.
Commit: `ea734ff` (incluye `626c969`; build desde worktree limpio) · `main.dart.js` sha256 `25a55251afbcad74…` (API_URL prod).
Pruebas: Flutter completo en el worktree, 366 en verde. `ruta_recorrido_test` falló por tiempo (inestable, ya conocido) y pasa al repetirlo (5/5). `validar_ruta.py`: 10 idiomas, 0 errores.
Pendiente: voces nativas Kyoko/Hinata (`voz.ts`), que necesitan reiniciar PM2 con autorización.
Backup: `/var/www/onelingo/backups/20261007-edu-51-japones/web-anterior` (= edu-50). Verificado: `/`, `/api/salud`, `main.dart.js` (sha256 del build), `ja/ruta/curso.json`, `ja/ruta/n2-b10.json`, `ja/diagnostico-v2.json`, `zh/ruta/n2-b10.json` e `it/ruta/n4-b10.json` responden 200; lock liberado. La web anterior queda en `/var/www/onelingo/web-saliente-20261007-edu-51-japones`.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261007-edu-51-japones/web-retirada-post && cp -al backups/20261007-edu-51-japones/web-anterior web'`

## Release: 20261007-edu-52-ruso

Fecha: 2026-10-07 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat (plan de la semana). Solo web; sin cambios de backend ni reinicio.
Contenido: ruso esencial, con Fundamentos (f0) + N1–N2 (100 clases, cirílico con rom letra a letra y acento), prueba de ubicación N1–N2 y Nivel 0 corregido (rom de rótulos, acentos, deRom/aRom/letraRom). N3–N10 aparecen como «Próximamente».
Commit: `2c316b3` (build desde worktree limpio) · `main.dart.js` sha256 `dbdbd1266b4ee1ed…` (API_URL prod).
Pruebas: Flutter completo en el worktree, 382 en verde. `ruta_recorrido_test` falló por tiempo (inestable, ya conocido) y pasa al repetirlo (5/5). `validar_ruta.py`: 10 idiomas, 0 errores.
Pendiente: voces nativas Mariia/Stanislav (`voz.ts`), que necesitan reiniciar PM2 con autorización.
Backup: `/var/www/onelingo/backups/20261007-edu-52-ruso/web-anterior` (= edu-51). Verificado: `/`, `/api/salud`, `main.dart.js` (sha256 del build), `ru/ruta/curso.json`, `ru/ruta/n2-b10.json`, `ru/diagnostico-v2.json`, y los `n*-b10` de ja, zh e it responden 200; lock liberado. La web anterior queda en `/var/www/onelingo/web-saliente-20261007-edu-52-ruso`.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261007-edu-52-ruso/web-retirada-post && cp -al backups/20261007-edu-52-ruso/web-anterior web'`

## Release: 20261007-edu-53-coreano

Fecha: 2026-10-07 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat (plan de la semana). Solo web; sin cambios de backend ni reinicio.
Contenido: coreano esencial, con Fundamentos (f0) + N1–N2 (100 clases, hangul con rom RR), prueba de ubicación N1–N2 y Nivel 0. N3–N10 aparecen como «Próximamente». Con esto ya no queda ningún idioma «En preparación».
Commit: `ae209d5` (build desde worktree limpio) · `main.dart.js` sha256 `e43669b7fab657cc…` (API_URL prod).
Pruebas: Flutter completo en el worktree, 398 en verde. `ruta_recorrido_test` falló por tiempo (inestable, ya conocido) y pasa al repetirlo (5/5). `validar_ruta.py`: 10 idiomas, 0 errores.
Pendiente: voces nativas Jiyoung/Chris (`voz.ts`), que necesitan reiniciar PM2 con autorización.
Backup: `/var/www/onelingo/backups/20261007-edu-53-coreano/web-anterior` (= edu-52). Verificado: `/`, `/api/salud`, `main.dart.js` (sha256 del build), `ko/ruta/curso.json`, `ko/ruta/n2-b10.json`, `ko/diagnostico-v2.json`, y los `n*-b10` de ru, ja, zh e it responden 200; lock liberado. La web anterior queda en `/var/www/onelingo/web-saliente-20261007-edu-53-coreano`.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261007-edu-53-coreano/web-retirada-post && cp -al backups/20261007-edu-53-coreano/web-anterior web'`

## Release: 20261013-edu-54-ola2-voces

Fecha: 2026-10-13 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat («mandemos a producción todo lo que tenemos»). Web + backend (2 archivos cambiados, 1 nuevo) + caché de audio; con reinicio de `onelingo-api`.
Contenido (ola 2, cada idioma completo y probado): italiano N5–N6 (`9272689`), ruso N3–N4 (`b1c84b3`), coreano N3–N4 (`95f70fa`), japonés N3–N4 (`0a08e52`), chino N3–N4 (`53554fc`), con ubicación hasta el último nivel publicado. Los niveles siguientes aparecen como «Próximamente».
Voces (`c554e4c`, `07d3014`): las letras ya no van a la voz del dispositivo (decía «A mayúscula»); el servidor lee su nombre por idioma (`modo=letra`) y no lee la notación de la vista (`voz_texto.ts`). Voces nativas nuevas: es Isabel/Enrique (latino neutro), pt Fernanda/Paulo (Brasil), en Matilda/Chris (americano, antes Alice/George británicos); quedan activas las de it, ru, ko, ja y zh (Luna/Carmelo, Mariia/Stanislav, Jiyoung/Chris, Kyoko/Hinata, Shan Shan/Evan).
Audio pregenerado: 1544 audios cortos (letras, vocales, sílabas, palabras de 1–2 letras) con `tools/voz/pregenerar_cortos.py`, verificados por transcripción (1077 verificados; el resto, sobre todo hanzi sueltos, sin verificación posible pero sin ruido ni tono de pregunta), copiados a `/var/www/onelingo/audio` (425 → 1996; ninguno reemplazado). Quedan 27 tomas sobrantes de la primera pasada, para textos que la app no lee.
Commit: `07d3014` (build desde worktree limpio) · `main.dart.js` sha256 `2106c611fdd5f41c…` (API_URL prod).
Pruebas: Flutter completo en el worktree, 408 en verde (1 omitido); backend 27/27; `tsc --noEmit` en staging OK; `config.ts` de prod intacto.
Backup: `/var/www/onelingo/backups/20261013-edu-54-ola2-voces/{web-anterior,backend-anterior}`. Verificado: `/`, `/api/salud`, `main.dart.js` (sha256), los `n*-b10` nuevos de it, ru, ko, ja y zh y `zh/diagnostico-v2.json` responden 200; `/api/voz/estado` lista las voces nuevas; PM2 `online`; lock liberado. La web anterior queda en `/var/www/onelingo/web-saliente-20261013-edu-54-ola2-voces`.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261013-edu-54-ola2-voces/web-retirada-post && cp -al backups/20261013-edu-54-ola2-voces/web-anterior web'`
Rollback backend: `ssh -F /dev/null root@167.235.20.41 'cd /var/www/onelingo; cp backups/20261013-edu-54-ola2-voces/backend-anterior/voz.ts backend/src/lib/ && cp backups/20261013-edu-54-ola2-voces/backend-anterior/routes-voz.ts backend/src/routes/voz.ts && rm backend/src/lib/voz_texto.ts && pm2 restart onelingo-api'`

## Release: 20261013-edu-55-italiano

Fecha: 2026-10-13 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat («ok despleguemos y los exámenes más exigentes»). Solo web; sin cambios de backend ni reinicio.
Contenido: italiano COMPLETO, con Fundamentos (f0) y N1–N10 (500 clases); N7–N10 son nuevos (`ea7c50f`). La prueba de ubicación llega hasta N10 (diagnóstico v2 con 180 ítems). También va la prueba de nivel más exigente (`89f597a`): 30 preguntas, hay que acertar 27 (90 %) con escuchar, escribir y gramática, y tras suspender se espera 12 h. Vale para todos los idiomas.
Audio: 22 audios cortos nuevos de it y ru, pregenerados con `tools/voz/pregenerar_cortos.py` y verificados por transcripción. Las abreviaturas de ru N8 (→, ≠, ↑, ↓, т. к., см.) se oyen como su lectura («к», «а не», «больше», «меньше», «так как», «смотри»). Se añadieron con `--ignore-existing` a `/var/www/onelingo/audio` (1980 → 2002); no se reemplazó ninguno. Quedan sin pregenerar «тя» y «po’» porque ninguna toma salía bien.
Commit: `ea7c50f` (build desde worktree limpio) · `main.dart.js` sha256 `e48aeaec1e93a6f8…` (API_URL prod).
Pruebas: Flutter completo en el worktree, 409 en verde (1 omitido). `validar_ruta.py`: 10 idiomas, 0 errores.
Backup: `/var/www/onelingo/backups/20261013-edu-55-italiano/web-anterior` (= edu-54). Verificado:
- responden 200: `/`, `/api/salud`, `it/ruta/curso.json`, `it/ruta/n10-b10.json`, `it/diagnostico-v2.json` y los `n4-b10` de ru y zh;
- curso it con N1–N10 publicados;
- lock liberado.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261013-edu-55-italiano/web-retirada-post && cp -al backups/20261013-edu-55-italiano/web-anterior web'`

## Release: 20261013-edu-56-ruso

Fecha: 2026-10-13 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat. Solo web; sin cambios de backend ni reinicio.
Contenido:
- Ruso COMPLETO, con Fundamentos (f0) y N1–N10 (500 clases); N5–N10 son nuevos (`4630bdc`). La prueba de ubicación llega hasta N10 (diagnóstico v2 con 180 ítems).
- Acentos del rom corregidos en N1–N4 ya publicado (`629976d`): sléduyushchaya, yáytsa, právilo, zapólnite, rúki, délala/délayete, otprávlyu, dnevniké, poberézh'ye, znála, rasskazála y -nibud' átono.
- Los puntos de la auditoría que ya eran correctos se dejaron como estaban.
- Incluye todo lo de edu-55.
Commit: `629976d` (build desde worktree limpio) · `main.dart.js` sha256 `e48aeaec1e93a6f8…` (el código Dart es el mismo que en edu-55; cambian los assets).
Pruebas: Flutter completo en el worktree, 411 en verde (1 omitido). `validar_ruta.py`: 10 idiomas, 0 errores. `validar_diagnostico.py --idioma ru`: n1–n10 OK.
Backup: `/var/www/onelingo/backups/20261013-edu-56-ruso/web-anterior` (= edu-55). Verificado:
- responden 200: `/`, `/api/salud`, `ru/ruta/n5-b01.json`, `ru/ruta/n10-b10.json`, `ru/diagnostico-v2.json`, `it/ruta/n10-b10.json` y `ko/ruta/n4-b10.json`;
- curso ru con N1–N10 publicados;
- `n1-b10` lleva «znála»;
- lock liberado.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261013-edu-56-ruso/web-retirada-post && cp -al backups/20261013-edu-56-ruso/web-anterior web'`
Limpieza (autorizada por el usuario):
- Se borraron los 8 `web-saliente-*` de edu-47 a edu-54 y los de edu-55 y edu-56. Eran enlaces duros a `backups/*/web-anterior`, así que solo liberan ~2 MB.
- Las 27 tomas de audio sobrantes de edu-54 se movieron a `backups/20261013-audio-sobrante/`.
- El espacio real lo ocupan `backups/` (14 GB) y `staging/` (4,8 GB). Siguen intactos a la espera de que el usuario decida.

## Limpieza del servidor (2026-10-13, autorizada por el usuario)

Se borraron las 52 versiones antiguas de la web (edu-1 a edu-53). Cada una tenía dos copias que compartían archivos (enlaces duros): `backups/<T>/web-anterior` y `staging/<T>/web-retirada`. Hubo que borrar las dos para liberar espacio. Se conservan las de edu-54, edu-55 y edu-56, así que los rollbacks de esas tres siguen valiendo.
Antes de borrar se comprobó que nada las usa: Apache sirve `/var/www/onelingo/web` y `/panel`, PM2 corre desde `backend/` y no hay enlaces simbólicos hacia `backups/`.
Después de borrar, `main.dart.js` tiene el mismo sha256 (`e48aeaec…`) y `web/` los mismos 1348 archivos. Responden 200 `/`, `/api/salud` y los cursos.
Disco: 90 % → 65 % (de 3,9 GB a 13 GB libres). Solo se tocó `/var/www/onelingo/`.
Siguen ahí, sin decidir: 18 copias de pruebas de diseño de septiembre (avatares, home, mascotas, voz), en `backups/` y `staging/`.

## Release: 20261013-edu-57-sin-etiqueta

Fecha: 2026-10-13 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat («sí, quitemos»). Solo web; sin cambios de backend ni reinicio.
Contenido: se quita la etiqueta «Versión inicial» de la pantalla de los cursos en todos los idiomas. El campo `revision` sigue en `curso.json` como dato interno.
Commit: `5c01fd3` (build desde worktree limpio) · `main.dart.js` sha256 `df3682c977f9fb5d…` (API_URL prod; no contiene «Versión inicial»).
Pruebas: Flutter completo en el worktree, 411 en verde (1 omitido).
Backup: `/var/www/onelingo/backups/20261013-edu-57-sin-etiqueta/web-anterior` (= edu-56). Verificado: `/`, `/api/salud` y los `n10-b10` de it y ru responden 200; lock liberado. El `web-saliente` se borró porque es un enlace duro al backup.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261013-edu-57-sin-etiqueta/web-retirada-post && cp -al backups/20261013-edu-57-sin-etiqueta/web-anterior web'`

## Release: 20261016-edu-58-coreano

Fecha: 2026-10-16 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat («terminemos y publiquemos el coreano»). Solo web y audios cortos; sin cambios de backend ni reinicio.
Contenido: coreano COMPLETO, con Fundamentos (f0) y N1–N10 (500 clases); N5–N10 son nuevos (`aee54c1`). Desde N5 la romanización va solo en el vocabulario. La prueba de ubicación llega hasta N10 (diagnóstico v2 con 180 ítems).
Audio: 39 audios cortos de ko pregenerados; se subieron solo los 26 verificados por transcripción, con `--ignore-existing` (2002 → 2028). Los 13 sin verificar (리, 긴, 바, 여, 녀, 걔, 팬, -적, V-되, V-(으)며, N 및 N, y los vocablos 덤/넉 con formas entre paréntesis) siguen generándose al vuelo con `/voz`.
Commit: `aee54c1` (build desde worktree limpio) · `main.dart.js` sha256 `df3682c977f9fb5d…` (el código Dart es el mismo que en edu-57; cambian los assets).
Pruebas: Flutter completo, 413 en verde (1 omitido) y 0 fallos, corrido en el árbol principal con el mismo contenido que `aee54c1`. `validar_ruta.py`: 10 idiomas, 0 errores. `validar_diagnostico.py --idioma ko`: n1–n10 OK.
Backup: `/var/www/onelingo/backups/20261016-edu-58-coreano/web-anterior` (= edu-57). Verificado:
- responden 200: `/`, `/api/salud`, `ko/ruta/curso.json`, `ko/ruta/n5-b01.json`, `ko/ruta/n10-b10.json`, `ko/diagnostico-v2.json` y los `n10-b10` de ru e it;
- curso ko con f0 y N1–N10 publicados (c2 planificado);
- PM2 `onelingo-api` online;
- lock liberado.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261016-edu-58-coreano/web-retirada-post && cp -al backups/20261016-edu-58-coreano/web-anterior web'`
Pendiente (para después de terminar todos los idiomas): barrido de naturalidad de ko con Kiwi (el validador solo acepta la palabra exacta o palabra + partícula de una lista, lo que deja diálogos rígidos en N5–N10).

## Release: 20261019-edu-59-voz-francesa (hotfix de backend)

Fecha: 2026-10-19 · Responsable: Claude (Claude Code), con autorización del usuario para reiniciar la API por el trabajo de voces («si es necesario reiniciar el servidor de la api procedamos»).
Motivo: la dueña de la voz Hélène (`imRmmzTqlLHt9Do1HufF`), narradora francesa, la desactivó en ElevenLabs. Comprobado por API el 19-10: Hélène responde `403 voice_disabled` y Caroline (`kwhMCf63M8O3rCfnQ3oQ`) responde 200. Por eso fallaba todo audio francés que no estuviera en caché.
Cambio: `backend/src/lib/voz.ts` añade `caroline` y pasa `fr.narradora` de `helene` a `caroline`; el test `voz-idioma` se actualiza. Se desplegó solo ese archivo (el `config.ts` de prod es distinto); antes del cambio el `voz.ts` de prod era idéntico al local.
Pruebas: `tsc --noEmit` limpio; `voz-idioma`, `voice-stream` y `chat-voz`: 16/16 en verde.
Backup: `/var/www/onelingo/backups/20261019-100210/voz.ts`. Se reinició solo `onelingo-api` (online) y `/api/salud` responde 200.
Rollback: `ssh -F /dev/null root@167.235.20.41 'cp -a /var/www/onelingo/backups/20261019-100210/voz.ts /var/www/onelingo/backend/src/lib/voz.ts && pm2 restart onelingo-api'`. No sirve de nada mientras Hélène siga desactivada.
Efecto: los audios franceses de narradora ya en caché siguen con la voz de Hélène; los nuevos salen con Caroline.

## Release: 20261019-edu-60-voces

Fecha: 2026-10-19 · Responsable: Claude (Claude Code), autorizado por el usuario en el chat («que este pulido bien lo de las voces si es necesario reiniciar el servidor de la api procedamos»). Backend (dos archivos) + web.
Contenido: voces nativas por rol (cinco por idioma: narradora, narrador, mujer_b, hombre_b, lumo); tutores, avatares y Lumo con voz nativa del idioma practicado; elenco por idioma (`assets/contenido/<idioma>/elenco.json`) para que cada personaje del diálogo tenga su voz; ajustes (style 0) en el hash con respaldo a la clave antigua; textos largos por frase; `previous_text` en la videollamada (`practice.js?v=29`). Sin pregeneración masiva: el audio se genera al usarse y queda en caché.
Commit: `0fd0575` (build desde worktree limpio) · `main.dart.js` sha256 `fa472738c58bd50b…`.
Pruebas: backend `tsc --noEmit` limpio y 32/32 en verde; Flutter: suite de voz y pantallas de clase 91/91 en verde y `flutter analyze` sin errores ni avisos (la suite completa de contenido no se repitió: el contenido no cambia en este commit; el agente de implementación la pasó con 418 en verde).
Backend: copia en `/var/www/onelingo/backups/20261019-112334/{lib-voz.ts,routes-voz.ts}`; antes del cambio prod era idéntico a `d64a715` (todo `src/` igual salvo `config.ts`). Se reinició solo `onelingo-api` (online); `/api/salud` 200; `/api/voz/estado` muestra los cinco roles por idioma.
Web: backup `/var/www/onelingo/backups/20261019-edu-60-voces/web-anterior` (= edu-58). Responden 200: `/`, `/api/salud`, `fr/elenco.json`, `ko/ruta/n10-b10.json`, `avatar/index.html`. Lock liberado.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261019-edu-60-voces/web-retirada-post && cp -al backups/20261019-edu-60-voces/web-anterior web'`
Rollback backend: `ssh -F /dev/null root@167.235.20.41 'cd /var/www/onelingo && cp -a backups/20261019-112334/lib-voz.ts backend/src/lib/voz.ts && cp -a backups/20261019-112334/routes-voz.ts backend/src/routes/voz.ts && pm2 restart onelingo-api'`
Audios cortos (mismo día, tras edu-60): faltaban 321 cortos con las voces nuevas (fr Caroline 212, it Sami 95, ko 13, ru 1). Se pregeneraron con `tools/voz/pregenerar_cortos.py` y se subieron 264 con `--ignore-existing` (2035 → 2299): 194 verificados por transcripción y 70 aceptados a mano porque la transcripción era correcta pero no literal (cifras dichas como palabra, «Deuxième», «10 %», «Trois heures», homófonos «Ça»/«Si»/«Du»/«Se», «E» → «Euh», «n°» → «Numéro»). Se descartaron los demás (letras y sílabas sueltas mal dichas, y «74», «94», «71», «79» oídos como otra cifra): esos se generan al vuelo.

## Release: 20261019-edu-61-chino

Fecha: 2026-10-19 · Responsable: Claude (Claude Code), dentro del encargo del usuario en el chat («continuemos con japonés y chino, terminemos todas las clases»), con el flujo de un despliegue por idioma completo. Solo web y audios cortos; sin cambios de backend ni reinicio.
Contenido: chino COMPLETO, con Fundamentos (f0) y N1–N10 (500 clases); N5–N10 son nuevos (`6d1b086`), cada nivel con corrección por parejas de bloques y pasada final. Desde N5 el pinyin va solo en el vocabulario. La prueba de ubicación llega hasta N10 (diagnóstico v2 con 180 ítems). El validador (Python y Dart) acepta numerales chinos compuestos de caracteres enseñados.
Audio: 190 cortos de zh pendientes (caracteres sueltos de N5–N10); se subieron solo los 92 verificados por transcripción, con `--ignore-existing` (2299 → 2391). Los 98 sin verificar (oídos como otra sílaba o tono: 其→起, 向→想, 教→叫…) se generan al vuelo con `/voz`.
Commit: `6d1b086` (build desde worktree limpio) · `main.dart.js` sha256 `fa472738c58bd50b…` (igual que edu-60: solo cambian los assets).
Pruebas: Flutter completo, 420 en verde (1 omitido) y 0 fallos, con el mismo contenido que `6d1b086`. `validar_ruta.py`: 10 idiomas, 0 errores. `validar_diagnostico.py --idioma zh`: n1–n10 OK.
Backup: `/var/www/onelingo/backups/20261019-edu-61-chino/web-anterior` (= edu-60). Verificado:
- responden 200: `/`, `/api/salud`, `zh/ruta/curso.json`, `zh/ruta/n5-b01.json`, `zh/ruta/n10-b10.json`, `zh/diagnostico-v2.json` y `ko/ruta/n10-b10.json`;
- curso zh con f0 y N1–N10 publicados (c2 planificado);
- PM2 `onelingo-api` online;
- lock liberado.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261019-edu-61-chino/web-retirada-post && cp -al backups/20261019-edu-61-chino/web-anterior web'`
Pendiente (barrido): ordinales 第五+ separados por el validador; compuestos verbo+resultado (说完, 做好) separados; palabras básicas sin entrada (放心, 到底, 规则…); `elenco.json` de zh por regenerar con los personajes de N5–N10.

## Release: 20261019-edu-62-japones

Fecha: 2026-10-19 · Responsable: Claude (Claude Code), dentro del encargo del usuario en el chat («continuemos con japonés y chino, terminemos todas las clases»), con el flujo de un despliegue por idioma completo. Solo web y audios cortos; sin cambios de backend ni reinicio.
Contenido: japonés COMPLETO, con Fundamentos (f0) y N1–N10 (500 clases); N5–N10 son nuevos (`3ec5720`), cada nivel con corrección por parejas de bloques y pasada final. Desde N5 el rōmaji va solo en el vocabulario. La prueba de ubicación llega hasta N10 (diagnóstico v2 con 180 ítems). `elenco.json` añade ななこさん; los apellidos sin género usan el respaldo por orden (el test de elenco ya no los cuenta).
Audio: 218 cortos de ja pendientes; se subieron solo los 141 verificados por transcripción, con `--ignore-existing` (2391 → 2532). Los 77 sin verificar se generan al vuelo con `/voz`.
Commit: `3ec5720` (build desde worktree limpio) · `main.dart.js` sha256 `fa472738c58bd50b…` (igual que edu-61: solo cambian los assets).
Pruebas: Flutter completo, 422 en verde (1 omitido) y 0 fallos, con el mismo contenido que `3ec5720`. `validar_ruta.py`: 10 idiomas, 0 errores. `validar_diagnostico.py --idioma ja`: n1–n10 OK.
Backup: `/var/www/onelingo/backups/20261019-edu-62-japones/web-anterior` (= edu-61). Verificado:
- responden 200: `/`, `/main.dart.js`, `/api/salud`, `ja/ruta/n10-b10.json`, `ja/diagnostico-v2.json` y `zh/ruta/n10-b10.json`;
- curso ja en prod con 101 módulos;
- PM2 `onelingo-api` online y las demás apps intactas;
- lock liberado.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261019-edu-62-japones/web-retirada-post && cp -al backups/20261019-edu-62-japones/web-anterior web'`
Pendiente (barrido): el validador rechaza formas conjugadas con kanji (来ました, 食べても…) y obliga a escribirlas en kana; «は pegada» en los bancos (では, ずには); partículas を/に en N10 c26–c34; c31–c35 de N10 algo mecánicas; elenco ja por regenerar.

## Release: 20261019-edu-63-voces-cifras

Fecha: 2026-10-19 · Responsable: Claude (Claude Code), dentro del barrido de voces que pidió el usuario («que esté pulido bien lo de las voces; si es necesario reiniciar el servidor de la API, procedamos»). Backend (archivo por archivo) + web + audios cortos; PM2 `onelingo-api` reiniciado (solo esa app).
Contenido:
- Cifras a palabras antes de la voz en fr, es, pt, it y ru (`numeros_{comun,fr,es,pt,it,ru}.ts`; antes solo de). Sonda con Flash v2.5 + transcripción, 86 frases: antes fr «74»→64, ru 1147→1947 y 1911→1919, «Статья 2»→«да», pt «4,8»→«quatro do oito», es «60»→160; después, bien (fr «soixante-quatorze», ru «в тысяча девятьсот одиннадцатом году»). Muestras en el scratchpad `barrido-voz/sonda1` y `sonda2`.
- Patrones «N1 は N2 に» se leen «AはBに» (antes «1は2に»); V1/Adj… no dejan cifras.
- ja: kanji suelto o jukujikun → lectura en kana del curso (`lecturas_ja.json`, 195 entradas; 星 salía «ほしい»).
- Voz por clase (`assets/contenido/<idioma>/elenco_clases.json`, `tools/voz/elenco_clases.py`): apellidos y oficios sin género global reciben voz según la clase. Líneas sin voz asignada: ja 23,8 % → 5,4 %, es 5,2 → 3,4 %, pt 2,8 → 0,5 %, it/en → 0.
Audio: 5 cortos ja nuevos verificados (い, き, ち, ひ, ま) subidos con `--ignore-existing` (2532 → 2537). Los textos con cifras o kanji suelto cambian de clave y se regeneran al vuelo.
Commit: `64c00ad` (build desde worktree limpio) · `main.dart.js` sha256 `7f6884135924d362…`.
Pruebas: backend 44/44 (`npx tsx --test test/*.test.ts`), `tsc --noEmit` limpio; Flutter completo 425 en verde (1 omitido); `validar_ruta.py` 0 errores. En prod, `textoParaVoz` comprobado: «74»(fr) → «soixante-quatorze.», «星»(ja) → «ほし。».
Backup: web en `backups/20261019-edu-63-voces-cifras/web-anterior` (= edu-62); `voz.ts` y `voz_texto.ts` anteriores en `backups/20261019-edu-63-voces-cifras/backend-lib/`. Verificado: `/`, `/main.dart.js`, `/api/salud`, `/api/voz/estado`, `ja/elenco_clases.json` responden 200; PM2 `onelingo-api` online y las demás apps intactas; lock liberado.
Rollback: web `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261019-edu-63-voces-cifras/web-retirada-post && cp -al backups/20261019-edu-63-voces-cifras/web-anterior web'`; backend: copiar `backend-lib/voz.ts` y `voz_texto.ts` a `backend/src/lib/` y `pm2 restart onelingo-api` (los numeros_*.ts y lecturas_ja.json nuevos quedan sin uso).
Visto en el log de errores de la API (anterior a esta release): Gemini responde 403 «project has been denied access» y el diagnóstico cae a OpenAI.

## Release: 20261020-edu-64-panel

Fecha: 2026-10-19 (noche) · Responsable: Claude (Claude Code), por pedido del usuario («panel de administrador … usuarios registrados, clases, analíticas»). Backend archivo por archivo + panel; PM2 `onelingo-api` reiniciado (solo esa app).
Contenido: panel `/panel` con analíticas (DAU/WAU/MAU, registros y activos 30 días, embudo, retención D1/D7/D30, clases por idioma × nivel, abandono, prueba de ubicación, coste estimado de IA y voz), alumnos con filtros/orden/CSV y detalle con progreso real por idioma (ids `ja.n3.c06`; antes contaba `L1-`). `/admin/usuarios/:id` ya no envía `password_hash` ni tokens. Migración `004_indices_panel.sql` (solo índices) aplicada al arrancar. Detalle en `docs/PANEL_ADMIN.md`.
Commit: `fd6d2b5`. Pruebas: backend 54/54, `tsc` limpio, `npm run build` del panel OK; prueba manual del agente en local (escritorio y 375 px).
Backup: `backups/20261020-edu-64-panel/` (`backend/admin.ts` anterior y `panel-anterior`). Verificado: `/api/salud` 200, `/panel/` 200, `/api/admin/resumen` 401 sin sesión; log «Migración aplicada: 004_indices_panel.sql»; PM2 online; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; cp backups/20261020-edu-64-panel/backend/admin.ts backend/src/routes/admin.ts; mv panel staging/20261020-edu-64-panel/panel-retirado && cp -al backups/20261020-edu-64-panel/panel-anterior panel; pm2 restart onelingo-api'` (analitica.ts e índices quedan sin uso).
Visto: ufw permite 5432/tcp (Postgres) desde cualquier IP → avisado al usuario, sin tocar.

## Release: 20261020-edu-65-app-020

Fecha: 2026-10-20 · Responsable: Claude (Claude Code), por pedido del usuario («compila la app, lanza emuladores, revisa errores y sube una versión al login como descarga»). Solo web + APK; sin backend.
Contenido: app 0.2.0+2 (`2ee2e53`): registro con el idioma meta real (objetivos, niveles sin gramática del inglés, prueba gratuita con 50 clases por nivel fuera de en y el 90 % real de la prueba de nivel), perfil con nivel y clase de la ruta (antes «Lección 100»), y bloque «Descarga la app para Android» en bienvenida y login (solo web).
APK: firmado con la llave propia (`~/.config/onelingo-firma/onelingo-release.jks`, SHA-1 `E3:C8:F4:AD:95:1D:BF:62:4D:97:CC:4D:C1:4E:25:96:D1:11:03:DC`), `--split-per-abi`: `/descargas/onelingo.apk` (arm64-v8a, 97 MB) y `/descargas/onelingo-armv7.apk`; `/descargas/version.json`. API_URL de prod (`onelingo.hostingcuenca.com/api`).
Pruebas: Flutter completo 433 en verde (1 omitido); emuladores Pixel 7/Pixel 6 (API 34): APK de publicación arranca sin errores contra prod; recorrido completo (registro → prueba de ubicación → inicio → ruta → clase con audio → práctica → perfil) con un APK de depuración contra el backend local.
Backup: `backups/20261020-edu-65-app-020/web-anterior`. Verificado: `/`, `/main.dart.js` (sha `58981f2368e8c7bb…`), `/descargas/version.json`, `/descargas/onelingo.apk` (application/vnd.android.package-archive) responden; en el navegador la bienvenida muestra «Descarga la app para Android · Versión 0.2.0 · 97 MB».
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261020-edu-65-app-020/web-retirada-post && cp -al backups/20261020-edu-65-app-020/web-anterior web'`
Pendiente: dominio onelingo.org (DNS lo cambia el usuario en Porkbun), login con Google (cliente: orígenes y SHA-1 en Google Cloud), bloque «DEMO · usuarios de prueba» visible en el login de producción (decisión del usuario).

## Release: 20261020-edu-66-dominio

Fecha: 2026-10-20 · Responsable: Claude (Claude Code), por pedido del usuario («configura los DNS para empezar a usar el dominio de producción»; certificado autorizado con «dale, instala el certificado»). Solo infraestructura + web + APK; sin backend.
Dominio: en Porkbun (cuenta del cliente) `onelingo.org` pasó de ALIAS a parking a A 167.235.20.41 y el comodín `*` CNAME pixie.porkbun.com pasó a `www` A 167.235.20.41. Apache: `ServerAlias onelingo.org www.onelingo.org` en los dos vhosts (OJO: `sites-enabled/onelingo.hostingcuenca.com-le-ssl.conf` es un archivo propio, no un enlace). Certificado Let's Encrypt `onelingo.hostingcuenca.com` ampliado con `certbot --expand` a los 3 nombres (vence 2027-01-18). Respaldos de la configuración en `/root/respaldos-apache/20261020-115934/`.
Incidente: durante la recarga de certbot Apache quedó caído unos minutos (systemd mató procesos y el reinicio vio «httpd already running»). `systemctl start apache2` lo levantó; todos los sitios verificados después.
App: web y APK 0.2.0+2 recompilados con `API_URL=https://onelingo.org/api` desde `49d44e1` (árbol limpio). APK x86_64 probado en el emulador: arranca y llama a `/api/salud` 200. `main.dart.js` sha256 `2b14f4d7ac843775…`; `/descargas/onelingo.apk` sha256 `7808a63692ecc15a…`.
Backup: `backups/20261020-edu-66-dominio/web-anterior`. Verificado: `https://onelingo.org/`, `/main.dart.js`, `/api/salud`, `/panel/`, `/descargas/version.json`, `https://www.onelingo.org/` y `https://onelingo.hostingcuenca.com/` responden 200; PM2 intacto; lock liberado.
Rollback web: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; mv web staging/20261020-edu-66-dominio/web-retirada-post && cp -al backups/20261020-edu-66-dominio/web-anterior web'`
Pendiente: `http://onelingo.org` responde 200 sin redirigir a https (la regla de reescritura del vhost :80 solo cubre onelingo.hostingcuenca.com; el cambio fue bloqueado y queda para el usuario). Las APK 0.2.0 ya instaladas siguen usando onelingo.hostingcuenca.com, que se mantiene.

## Release: 20261020-edu-67-panel-pin

Fecha: 2026-10-20 · Responsable: Claude (Claude Code), por pedido del usuario («ponle un PIN genérico básico, 2345; cuando pasemos a producción blindamos todo»). `.env` del backend en prod: `ADMIN_PIN` cambiado a un PIN genérico temporal (respaldo del `.env` anterior en `/root/respaldos-apache/20261020-115934/backend-env-antes-pin`); PM2 `onelingo-api` reiniciado con `--update-env` (solo esa app). Panel (`0ef0712`): el login ya no precarga «1234» ni muestra la pista «Demo: admin / 1234».
Verificado: `POST /api/admin/login` con el PIN nuevo 200 y con 1234 401; `/panel/` 200 y el Resumen carga datos reales en el navegador; PM2 online; lock liberado.
Backup panel: `backups/20261020-edu-67-panel-pin/panel-anterior`.
Pendiente al salir a producción: cuentas de administrador por persona, contraseña fuerte y límite de intentos en `/admin/login` (hoy no hay).

## Release: 20261020-edu-68-conexiones

Fecha: 2026-10-20 · Responsable: Claude (Claude Code), por pedido del usuario («que desde el panel configure las conexiones, vea consumos, las API keys… y que se verifique», «el logo en el sidebar»). Backend archivo por archivo + panel; PM2 `onelingo-api` reiniciado (solo esa app).
Contenido (`538b820`): página «Conexiones» del panel para ElevenLabs, OpenAI y Gemini: clave y modelos editables, verificación de formato (rechaza la clave de otro proveedor) y con el proveedor (llamadas de lectura sin coste) antes de guardar, guardado cifrado AES-256-GCM en la tabla `conexiones` con prioridad sobre el `.env` y aplicado en caliente, «Volver a la configuración del servidor», consumo (ElevenLabs real; OpenAI estimado o real con Admin key; Gemini enlace) e instrucciones para obtener cada clave. Logo en la barra lateral, el login y el favicon del panel. Archivos: `sql/005_conexiones.sql`, `src/lib/conexiones.ts`, `src/routes/conexiones.ts`, `src/app.ts`, `src/server.ts` (los dos últimos eran iguales a HEAD en prod). `config.ts` de prod sin tocar.
Pruebas: backend 70/70, `tsc` limpio, build del panel OK. En prod: migración 005 aplicada; las tres claves actuales «Clave válida»; una clave `sk-proj-…` en ElevenLabs → «Esta clave es de OpenAI, no de ElevenLabs»; consumo ElevenLabs 16 988/58 388 (renueva 07-11); la página carga con el logo; sin sesión 401.
Backup: `backups/20261020-edu-68-conexiones/` (`backend/app.ts`, `backend/server.ts`, `panel-anterior`).
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; cp backups/20261020-edu-68-conexiones/backend/app.ts backups/20261020-edu-68-conexiones/backend/server.ts backend/src/; mv panel staging/20261020-edu-68-conexiones/panel-retirado-post && cp -al backups/20261020-edu-68-conexiones/panel-anterior panel; pm2 restart onelingo-api'` (la tabla `conexiones` queda sin uso).
Notas: `IA_PROVEEDOR` se decide al arrancar; si se añade desde el panel la clave de un proveedor que no estaba, el tutor no cambia de proveedor hasta reiniciar. Si cambia `JWT_SECRET`, las claves guardadas en el panel no se descifran y se usa el `.env` (la página lo avisa).

## Release: 20261020-edu-69-pagos

Fecha: 2026-10-21 · Responsable: Claude (Claude Code), por pedido del usuario («que el admin configure los planes y suscripciones y vincule Stripe desde el panel», «con modo test»; despliegue autorizado con «si continúa»). Backend archivo por archivo + panel + web + APK 0.3.0; PM2 `onelingo-api` reiniciado (solo esa app).
Contenido (`6da9458`, `6a88569`): planes en el servidor (`GET /planes`), Stripe por claves en Conexiones (webhook, Customer Portal con cambio de plan y sincronización de productos/precios automáticos; modo test/real según la clave), Checkout + confirmación al volver + webhook firmado e idempotente, suscripciones con idiomas elegidos (regla de cambio `uno_por_periodo` por defecto, editable), cortesía del administrador, páginas Planes y Suscripciones del panel, el servidor es la autoridad del plan (el PUT de progreso ignora `planId`; la prueba no baja). App 0.3.0+3: planes del servidor, selector de idiomas al suscribirse, «Gestionar suscripción», vuelta `#/pago`, aviso de idioma no pagado, «Idioma que estudias» en Perfil.
Migraciones aplicadas al arrancar: 006_pagos, 007_pagos_portal, 008_pagos_idiomas. Archivos backend: `sql/006–008`, `src/lib/pagos/*`, `src/routes/pagos.ts`, `src/routes/planes.ts`, y modificados `src/lib/conexiones.ts`, `src/lib/analitica.ts`, `src/routes/admin.ts`, `src/routes/auth.ts`, `src/routes/usuarios.ts`, `src/app.ts` (los 6 eran iguales a `4015cef` en prod antes del cambio).
Pruebas: backend 96/96, `tsc` limpio, panel build OK, Flutter 466 en verde (1 omitido); integración local contra el servidor real (sin plan, 503 sin Stripe, cortesía con idiomas por elegir, completar, cambio permitido y segundo cambio 403 con fecha, acceso por idioma). Stripe real sin probar: falta clave de test.
Datos: el único alumno con plan elegido en la app (p3, sin pago) se conservó como cortesía p3 con `en` (2 idiomas por elegir), nota en la suscripción.
Backup: `backups/20261020-edu-69-pagos/` (backend modificado, `web-anterior`, `panel-anterior`). Verificado: `/api/salud`, `/`, `/panel/` 200; `GET /planes` con p1–p3 y `pagos.disponible=false`; `/descargas/version.json` 0.3.0 y APK con sha igual al local; PM2 intacto; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; K=backups/20261020-edu-69-pagos; cp $K/backend/src/lib/*.ts backend/src/lib/; cp $K/backend/src/routes/*.ts backend/src/routes/; cp $K/backend/src/app.ts backend/src/; mv web staging/20261020-edu-69-pagos/web-retirada-post && cp -al $K/web-anterior web; mv panel staging/20261020-edu-69-pagos/panel-retirado-post && cp -al $K/panel-anterior panel; pm2 restart onelingo-api'` (las tablas nuevas quedan sin uso; los archivos `lib/pagos` y `routes/pagos|planes.ts` quedan sin registrar).
Pendiente: vincular Stripe en modo test (el usuario pega la clave en Panel → Conexiones; en «URL de la app» usar https://onelingo.org) y probar una compra con la tarjeta 4242.

## Release: 20261022-edu-70-tutores-vivo (registro reconstruido)

Desplegada el 2026-10-22 (15:36–23:53, hora de Ecuador) por otra sesión de Claude Code, que el usuario interrumpió antes de cerrarla: no se registró aquí y el lock quedó puesto. Lo que se ve en el servidor: web y APK 0.4.0+4 (tutores en vivo, Ana incluida), backend de tutores (`personajes.ts`, `ia.ts`, `voz.ts`, `llamada.ts`…) igual a HEAD salvo `config.ts` (propio de prod) y `routes/admin.ts` (sin el cambio del panel `b2ba68f`). Backup: `backups/20261022-edu-70-tutores-vivo/`. El lock huérfano se guardó en `backups/20261023-edu-71-100-clases/lock-huerfano-edu-70.txt`.
Complemento de la sesión que lo desplegó: build desde `git archive 56eebb0` (sin el francés `965b5af`), `API_URL=https://onelingo.org/api`, APK firmado (SHA-1 `e3c8f4ad…`). Backend: `app.ts`, `lib/ia.ts`, `lib/situaciones.ts`, `lib/voz.ts`, `routes/voz.ts` reemplazados (iguales a `44b0ac4` antes) y `lib/personajes.ts`, `routes/llamada.ts` nuevos; `tsc --noEmit` limpio en prod antes de `pm2 restart onelingo-api`; `.env` sin cambios (sha). Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; K=backups/20261022-edu-70-tutores-vivo; cp $K/backend/src/app.ts backend/src/; cp $K/backend/src/lib/*.ts backend/src/lib/; cp $K/backend/src/routes/voz.ts backend/src/routes/; pm2 restart onelingo-api'` (la web la reemplazó edu-71).

## Release: 20261023-edu-71-100-clases

Fecha: 2026-10-23 · Responsable: Claude (Claude Code), por pedido del usuario («cuando ya tengas todo haz pruebas aleatorias y despliega en produccion»; «cuando terminemos todas las 100 clases igual subimos a produccion», incluidos los tutores en vivo y Ana). Web + panel + APK 0.5.0+5 + `backend/src/routes/admin.ts`; PM2 `onelingo-api` reiniciado (solo esa app).
Contenido (`e32b522`): los 10 idiomas con 100 clases por nivel (DEC-036: un refuerzo rNN por cada cNN; fr, de, pt, it, es, ru, zh, ja, ko nuevos; en ya los tenía). Romanización de ru/zh/ja/ko en los ejercicios de N1–N4 y solo en el vocabulario desde N5. Elenco por clase regenerado (los refuerzos heredan las voces de su clase). Panel con menú móvil y sesión de 30 días (`b2ba68f`, `d4ac027`); login del panel sin distinguir mayúsculas en el usuario.
Pruebas: Flutter 466 en verde (1 omitido), `validar_ruta.py` 10 idiomas 0 errores, backend 108/108, `tsc` limpio, panel build OK. Recorrido local en web y en el emulador (pruebas_general, APK contra el backend local): los 10 idiomas muestran N1–N10 «0/100» en el perfil; un refuerzo de francés abre y corre.
APK: firmado con la llave propia (SHA-1 `E3:C8:F4:AD…`), `--split-per-abi`: `/descargas/onelingo.apk` (arm64-v8a, 129 MB, sha256 `79672be3cf0d660e…`) y `/descargas/onelingo-armv7.apk` (sha256 `8f2cb25b607b68af…`); `/descargas/version.json` 0.5.0. `main.dart.js` sha256 `8ebcfaf6ea119b37…` (igual al de edu-70: solo cambian assets y versión).
Backup: `backups/20261023-edu-71-100-clases/` (`web-anterior`, `panel-anterior`, `backend/admin.ts`, `env.sha`). Staging subido con `rsync --checksum --link-dest` sobre la web anterior; contenido comprobado en staging (10 idiomas × N1–N10 = 100) antes del renombre.
Verificado: `/`, `/main.dart.js`, `/version.json`, `/api/salud`, `/panel/`, `/descargas/version.json`, `/avatar/index.html`, `ja/ruta/n1-b01.json`, `ko/ruta/n10-b10.json` responden 200; APK servido con sha igual al local; en el navegador la bienvenida muestra «Versión 0.5.0 · 129 MB» sin errores de consola; `.env` sin cambios (sha); PM2 online; lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; K=backups/20261023-edu-71-100-clases; S=staging/20261023-edu-71-100-clases; mv web $S/web-retirada-post && cp -al $K/web-anterior web; mv panel $S/panel-retirado-post && cp -al $K/panel-anterior panel; cp $K/backend/admin.ts backend/src/routes/admin.ts; pm2 restart onelingo-api'`

## Release: 20261024-edu-72-imagenes-vocab

Fecha: 2026-10-24 · Responsable: Claude (Claude Code), por pedido del usuario («dale despliega»). Web + APK 0.5.1+6; backend sin cambios (no se reinició PM2).
Contenido (`1b74f28`, `89b97b0`): 895 ilustraciones de vocabulario (`assets/img/vocab/`, 448 px webp) y `assets/contenido/<idioma>/imagenes.json` en los 10 idiomas. Las imágenes aparecen en la tarjeta del paso de vocabulario, en «Mis palabras», en la retroalimentación del repaso y en la nueva forma «Escucha y elige la imagen».
Pruebas: Flutter 471 en verde (1 omitido), `mapear.py --comprobar` OK, `validar_ruta.py` 10 idiomas 0 errores. Recorrido local en web: miniaturas en «Mis palabras», imagen en la retroalimentación del repaso, tarjetas con imagen en fr.n2.c16.
APK: build desde un árbol limpio de `89b97b0` con `API_URL=https://onelingo.org/api`, firmado con la llave propia (SHA-1 `e3c8f4ad…`), `--split-per-abi`: `/descargas/onelingo.apk` (arm64-v8a, 146 MB, sha256 `7b3b4f5a11aa71f8…`) y `/descargas/onelingo-armv7.apk` (sha256 `9cecc147544b2eee…`); `/descargas/version.json` 0.5.1.
Backup: `backups/20261024-edu-72-imagenes-vocab/` (`web-anterior`, `env.sha`). Staging armado con `cp -al` de la web viva y `rsync --checksum` encima (sin tocar `avatar/`, idéntico al local; `descargas/` con archivos nuevos, inodos distintos de los vivos). En staging: 895 imágenes y 10 mapas antes del renombre.
Verificado: `/`, `/main.dart.js`, `/version.json`, `/descargas/version.json`, `/api/salud`, `/avatar/index.html`, `/panel/`, `img/vocab/action-buy.webp` y `fr/imagenes.json` responden 200. El APK servido tiene el mismo sha que el local. En el navegador la app abre en `#/bienvenida` con `version.json` 0.5.1 y sin errores de consola. `.env` sin cambios (sha), las 5 apps de PM2 online, lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; K=backups/20261024-edu-72-imagenes-vocab; S=staging/20261024-edu-72-imagenes-vocab; mv web $S/web-retirada-post && cp -al $K/web-anterior web'`

## Release: 20261025-edu-73-correcciones

Fecha: 2026-10-25 · Responsable: Claude (Claude Code), por pedido del usuario («dale, despliega todo con las correcciones»). Web + APK 0.5.2+7 + 9 archivos del backend + `web/avatar/practice.js` y `vivo.js`; PM2 `onelingo-api` reiniciado (solo esa app).
Contenido: `5fdeb5f` (tutores en vivo corrigen y explican mejor), `a7fa16f` (seguridad: el registro ya no reclama cuentas antiguas sin contraseña; nombres escapados en los correos; token de `/auth/restablecer` validado, cierra el XSS), `2d793a1` (fallos hallados probando como alumno en el emulador: tarea abierta que se repetía en la evaluación, reanudar en la evaluación, perfil por idioma y por habilidad, XP real del examen, consignas en inglés, chat por objetivos que no dice la frase del alumno, corrección en segunda persona) y `4cc0dfa` (versión).
Backend: `lib/correo.ts`, `lib/ia.ts`, `lib/ia_openai.ts`, `lib/personajes.ts`, `lib/situaciones.ts`, `routes/auth.ts`, `routes/chat.ts`, `routes/diagnostico.ts`, `routes/usuarios.ts` (prod era igual a `a27cd8f` salvo `config.ts`, que no se tocó). Sin migraciones. `tsc --noEmit` limpio en prod antes del reinicio.
Pruebas: Flutter 474 en verde (1 omitido), backend 109/109, `tsc` limpio. Recorrido en el emulador con 4 cuentas locales (en, fr desde cero, es con interfaz en inglés, ja a 360 dp).
APK: build desde un árbol limpio de `4cc0dfa` con `API_URL=https://onelingo.org/api`, firmado con la llave propia (SHA-1 `e3c8f4ad…`), `--split-per-abi`: `/descargas/onelingo.apk` (arm64-v8a, 146 MB, sha256 `79491925e11c00c5…`) y `/descargas/onelingo-armv7.apk` (sha256 `caecadc52625b8f0…`); `/descargas/version.json` 0.5.2.
Backup: `backups/20261025-edu-73-correcciones/` (`web-anterior`, `backend/lib`, `backend/routes`, `env.sha`).
Verificado: `/`, `/main.dart.js`, `/version.json` (0.5.2), `/descargas/version.json`, `/api/salud`, `/api/planes`, `/avatar/index.html`, `/avatar/vivo.js`, `/panel/` y una imagen de vocabulario responden 200. El APK servido tiene el mismo sha que el local. `/auth/restablecer?token="><script>` responde «Enlace no válido» sin el script. En el navegador la app abre en `#/bienvenida` sin 404 de producción. `.env` sin cambios (sha), las 5 apps de PM2 online, lock liberado.
Rollback: `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; K=backups/20261025-edu-73-correcciones; S=staging/20261025-edu-73-correcciones; mv web $S/web-retirada-post && cp -al $K/web-anterior web; cp $K/backend/lib/*.ts backend/src/lib/; cp $K/backend/routes/*.ts backend/src/routes/; pm2 restart onelingo-api'`

## Release: 20261026-edu-74-situaciones

Fecha: 2026-10-26 · Responsable: Claude (Claude Code), por pedido del usuario («dale, despliega y pon la apk accesible facilmente»). Web + APK 0.5.3+8 + 19 archivos del backend (1 migración) + `web/avatar/practice.js`; ffmpeg instalado en el servidor; caché de voz normalizada; PM2 `onelingo-api` reiniciado (solo esa app).

**Contenido:**
- `8c7f33a`: corrector de tutores aparte (gpt-5.6-luna), límites y reintentos de red.
- `63dff7c`: mismo volumen en todas las voces (−18 LUFS) y lecturas ja/ru.
- `a93d0c1`: un ejercicio fallado vuelve como mucho dos veces.
- `27f3f09`: situaciones en it, ru, ja, ko y zh con romanización; respuestas en letras latinas aceptadas.
- `1ba5432`: el servidor bloquea al tutor con la prueba agotada (402); interruptor de usuarios demo.
- `ed22679` y `30604eb`: app 0.5.3+8 y página de descarga.

**APK fácil:**
- **https://onelingo.org/descargar/:** página con botón, versión, enlace armv7, pasos de instalación y QR.
- **https://onelingo.org/apk:** atajo que lleva a esa página.
- **Logo:** va en `/descargar/icono.png`, porque Apache reserva `/icons/` con su alias por defecto. Por eso tampoco se sirven los íconos del manifiesto PWA; es un fallo previo, sin tocar.

**Backend:**
- **Archivos modificados:** `package.json` (script `normalizar-audios`), `content/situaciones-en.json`, `lib/ia.ts`, `lib/ia_openai.ts`, `lib/pagos/planes.ts`, `lib/pagos/suscripciones.ts`, `lib/voz.ts`, `lib/voz_texto.ts`, `routes/chat.ts`, `routes/llamada.ts`, `routes/usuarios.ts`.
- **Archivos nuevos:** `lib/volumen.ts`, `normalizar-audios.ts`, `content/situaciones-{it,ru,ja,ko,zh}.json`, `sql/009_modo_demo.sql`.
- **Estado previo:** prod era igual a `0b4a679` (sha por archivo), salvo `config.ts`, que no se tocó.
- **Comprobación:** `tsc --noEmit` limpio en una copia de prod con su `config.ts` antes de copiar.
- **Migración:** «Migración aplicada: 009_modo_demo.sql». `GET /planes` devuelve `demoActivo: true`; el demo queda activo y hay que apagarlo al lanzar (Panel → Planes).

**ffmpeg y audios:**
- **ffmpeg:** 4.4.2 por apt. Probado en el servidor: −36,2 y −16,2 LUFS → −18,5.
- **Normalización:** `npm run normalizar-audios` corrido como root, porque `backend/` es 700 root. Luego `chown -R webdev:webdev audio`. Resultado: 2.172 ajustados, 435 ya estaban bien, 0 con error, de 2.607 MP3; lock liberado al terminar.
- **Respaldo de la caché:** `backups/.../audios-antes`, con enlaces duros de los 2.655 archivos.

**Pruebas:** Flutter 482 en verde (1 omitido), backend 117/117, `tsc` limpio. `mapear.py` regenerado para las situaciones nuevas.

**APK:**
- **Build:** desde un árbol limpio de `ed22679` con `API_URL=https://onelingo.org/api`, firmado con la llave propia (SHA-1 `e3c8f4ad…`), versionCode 2008.
- **`/descargas/onelingo.apk`:** arm64-v8a, 147 MB, sha256 `eedc952b77cd9011…`.
- **`/descargas/onelingo-armv7.apk`:** sha256 `4e8a568837a93104…`.
- **Versión publicada:** `/descargas/version.json` 0.5.3. `main.dart.js` sha256 `d4adae063adb9f8b…`.

**Backup:** `backups/20261026-edu-74-situaciones/` (`web-anterior`, `backend/` con los 11 archivos previos, `backend-nuevos.txt`, `audios-antes`, `env.sha`).

**Verificado:**
- **Responden 200:** `/`, `/main.dart.js`, `/version.json` (0.5.3+8), `/descargar/`, `/apk/`, `/descargas/version.json`, `/avatar/index.html`, `/avatar/practice.js` (con `bloqueoTutor`), `/panel/`, `/api/salud`, `/api/planes`, las situaciones de zh e it y una imagen de vocabulario.
- **APK:** el servido tiene el mismo sha que el local y `content-type` `application/vnd.android.package-archive`.
- **Navegador:** la app abre en `#/bienvenida`; `/descargar/` a 375 px sin desplazamiento lateral.
- **Servidor:** las 5 apps de PM2 en línea y `.env` sin cambios.

**Rollback:** `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; K=backups/20261026-edu-74-situaciones; S=staging/20261026-edu-74-situaciones; mv web $S/web-retirada-post && cp -al $K/web-anterior web; cp -r $K/backend/. backend/; (cd backend && xargs rm -f < ../$K/backend-nuevos.txt); pm2 restart onelingo-api'`. La columna `demo_activo` se puede quedar, porque es inocua. Los audios se restauran con `cp -al $K/audios-antes/. audio/` solo si hiciera falta.

## Release: 20261029-edu-75-pagos

Fecha: 2026-10-29 · Responsable: Claude (Claude Code), por pedido del usuario («dale, despliega»). Web 0.5.4 + panel + 9 archivos del backend (2 migraciones) + APK 0.5.4+2010 con Shorebird; PM2 `onelingo-api` reiniciado (solo esa app).

**Contenido:**
- `48da744`: cobro dentro de la app Android con Google Play Billing (`/pagos/google/verificar`, `/pagos/google/rtdn`), planes con duraciones 1/3/6/12 meses y plan Familiar; panel de suscripciones con origen Google Play.
- `9606ed7`: Shorebird (app `fdede793…`); la APK recibe parches de código sin reinstalar.
- `3341c65`: íconos nuevos de OneLingo (Android adaptativo, web, favicon, descarga), permiso del micrófono obligatorio para entrar al tutor, recuadro «Tutores en vivo», tutores 3D ocultos, solo las demos Ana y Bryan, errores de micrófono explicados con reintento.

**Backend:**
- **Modificados:** `lib/pagos/planes.ts`, `lib/pagos/proveedor.ts`, `lib/pagos/stripe.ts`, `lib/pagos/suscripciones.ts`, `routes/pagos.ts`, `routes/planes.ts`.
- **Nuevos:** `lib/pagos/cotizaciones.ts`, `lib/pagos/familia.ts`, `lib/pagos/google.ts`, `sql/010_planes_duraciones_familia.sql`, `sql/011_google_play.sql`.
- **Migraciones:** 010 y 011 aplicadas con `npm run migrate`. `config.ts` de prod sin tocar. Google Play queda apagado hasta configurar `GOOGLE_PLAY_*` en `.env` (`google.disponible: false`).

**Cuentas:** Ana y Bryan con cortesía p3 «todos» hasta 2026-10-30T19:34Z (la prueba de prod sigue en 1 minuto).

**APK:**
- **Build:** `shorebird release android --artifact apk --target-platform android-arm,android-arm64 --build-number=2010` desde un árbol limpio de `3341c65` con `API_URL=https://onelingo.org/api`. La release 0.5.4+2009 quedó registrada a medias en Shorebird por una corrida interrumpida; por eso se publicó la 2010.
- **`/descargas/onelingo.apk` y `/descargas/onelingo-armv7.apk`:** la misma APK universal (arm + arm64), 163 MB, sha256 `b890ccc08deeeef1…`; `/descargas/version.json` 0.5.4. Se escribieron con nombre temporal y `mv`, para no tocar los enlaces duros de los respaldos.

**Backup:** `backups/20261029-edu-75-pagos/` (`web-anterior`, `panel-anterior`, `backend/` con los 6 archivos previos, `backend-nuevos.txt`, `onelingo-antes.dump`, `env.sha`).

**Verificado:** `/api/planes` devuelve p1, p2, p3 y familiar con productos de Google; `/version.json` 0.5.4; el APK servido tiene el mismo sha que el local y `content-type` `application/vnd.android.package-archive`; las 5 apps de PM2 en línea; `.env` sin cambios (sha); lock liberado.

**Rollback:** `ssh -F /dev/null root@167.235.20.41 'set -e; cd /var/www/onelingo; K=backups/20261029-edu-75-pagos; S=staging/20261029-edu-75-pagos; mv web $S/web-retirada-post && cp -al $K/web-anterior web; mv panel $S/panel-retirado-post && cp -a $K/panel-anterior panel; cp -r $K/backend/. backend/; (cd backend && xargs rm -f < ../$K/backend-nuevos.txt); pm2 restart onelingo-api'`. Las tablas y columnas de 010/011 se pueden quedar; si hiciera falta, la base se restaura con `pg_restore` desde `onelingo-antes.dump`.

## Release: 20261029-migracion-vps

Fecha: 2026-10-29 · Responsable: Claude (Claude Code), por pedido del usuario («ya migrar todo al servidor de produccion completamente … incluido los dns»). OneLingo pasa de Hetzner (`167.235.20.41`, compartido) al VPS Hostinger KVM 2 `179.197.89.105` (`ssh onelingo`). Detalle del servidor en `docs/DEPLOYMENT_RUNBOOK.md`.

**Preparación:** Ubuntu 26.04 con Apache 2.4.66, PostgreSQL 18, Node 22, ffmpeg 8, PM2 6 (usuario de servicio `onelingo`, servicio `pm2-onelingo`), certbot, ufw, fail2ban, actualizaciones automáticas, swap de 2 GB y SSH solo con llave. Web, panel, audios y backend (con `.env`, copiado de servidor a servidor sin leerlo) copiados por `tar`; `npm ci` y `tsc --noEmit` limpios. Certificado de `onelingo.hostingcuenca.com` (incluye onelingo.org y www, vence 2027-01-18) copiado. Vhost nuevo: http redirige a https para todos los nombres. Respaldo diario de la base a las 03:15 (14 días).

**Corte (16:36–16:38 hora de Ecuador, unos 2 minutos sin API):** `tools/servidor/corte.sh` comprobó que web, panel y backend fueran idénticos en los dos lados (huella sha256), paró `onelingo-api` en Hetzner, copió la base (`pg_dump -Fc` → `/var/backups/onelingo/hetzner-corte.dump` → `pg_restore`) y los audios (`rsync`). Conteos iguales: usuarios 25, progreso 23, suscripciones 3, eventos 265, conversaciones 179, errores 40, audios 527, migraciones 11. En Hetzner quedó `onelingo-puente` (PM2, `puente.mjs`) en el puerto 8091 reenviando al VPS; probado con GET y POST.

**DNS:** Porkbun, registros A de `onelingo.org` y `www` → `179.197.89.105` (TTL 600); Cloudflare y Google ya lo resolvían así minutos después. Certificado propio emitido en el VPS para `onelingo.org` y `www` (vence 2027-01-27, `certbot renew --dry-run` correcto); el subdominio `onelingo.hostingcuenca.com` se retiró del vhost y su certificado copiado se borró.

**Verificado:** `/`, `/main.dart.js`, `/version.json`, `/descargas/version.json`, `/descargar/`, `/api/salud`, `/api/planes`, `/avatar/index.html`, `/panel/`, `/iconos/Icon-192.png` y `/manifest.json` responden 200 desde el VPS; el APK con `content-type` de Android; `http://` responde 301 a https.

**Limpieza de Hetzner (mismo día, 17:10):** sin tráfico por Hetzner desde el corte, se retiraron el puente, `onelingo-api`, los vhosts (incluida una copia real del vhost SSL en `sites-enabled` que habría roto la siguiente recarga de Apache), el certificado, la base y el rol `onelingo` y `/var/www/onelingo` (18 GB: 12 GB de respaldos de releases y 4,8 GB de staging). Disco de Hetzner del 85 % al 37 %; `apache2ctl configtest` correcto y los demás sitios responden 200. Respaldo esencial previo en el VPS y en local (ver `docs/DEPLOYMENT_RUNBOOK.md`).

**Pendiente:** copia de los respaldos fuera del VPS.

**Rollback:** ya no hay OneLingo en Hetzner; ante una caída del VPS se reconstruye desde el repo, el respaldo esencial y los volcados diarios.

## Release: 20261030-edu-76-tutores

Fecha: 2026-10-30 · Responsable: Claude (Claude Code), por pedido del usuario («dale despliega»). Primer despliegue en el VPS `onelingo` (179.197.89.105): 2 archivos del backend + página del avatar; PM2 `onelingo-api` reiniciado (solo esa app). Sin APK: la app carga `/avatar` desde onelingo.org con `Cache-Control: no-cache`.

**Contenido (`bf5efd2`):** el avatar corrige en voz alta al estilo Praktika (reacción, forma correcta y siempre pide repetir; en niveles 1-2 sin reglas), pistas habladas (botón «Pista» y avisos de silencio a los 9 s y 12 s más, `aviso: silencio|pista` en `/chat`), rellenos hablados si la primera frase tarda, avatar en una card con insignia de estado.

**Archivos:** `backend/src/lib/ia.ts`, `backend/src/routes/chat.ts`, `web/avatar/index.html`, `web/avatar/practice.js`. Antes de copiar, los de prod coincidían con `bf5efd2~1` (sha). Sin migraciones; `.env` sin tocar.

**Probado antes:** backend 134/134 y typecheck; local con `/chat` (fr/en, niveles 1, 2 y 5); emulador Android (`pruebas_general`, APK debug contra el backend local): saludo, silencio, pista, corrección hablada con petición de repetir, resumen al colgar, sin errores en logcat.

**Backup:** `backups/20261030-edu-76-tutores/antes.tar.gz` (los 4 archivos previos).

**Verificado:** `tsc` en el servidor OK; `onelingo-api` en línea; `/api/salud` ok; `/avatar/index.html` con `pedirPista` y `practice.js?v=53` (200); lock liberado.

**Rollback:** `ssh onelingo 'cd /var/www/onelingo && tar xzf backups/20261030-edu-76-tutores/antes.tar.gz && chown onelingo:onelingo backend/src/lib/ia.ts backend/src/routes/chat.ts web/avatar/index.html web/avatar/practice.js && sudo -u onelingo -H pm2 restart onelingo-api'`.

## Release: 20261030-edu-77-registro

Fecha: 2026-10-30 · Responsable: Claude (Claude Code), por pedido del usuario («Todo junto»). Backend (5 archivos modificados, 2 nuevos, migración 012) + `.env` (correo) + panel + web 0.5.5 + APK 0.5.5+2011 con Shorebird; PM2 `onelingo-api` reiniciado (solo esa app).

**Contenido:**
- `e280889`: registro con código de 6 dígitos por correo (nombre, apellido, correo, teléfono), «olvidé mi contraseña» con código, Google pide el teléfono si falta, mensajes del servidor en es/en (`x-idioma`); panel con apellido, teléfono y correo verificado.
- `7d3418f`: versión de la app al pie de Perfil.
- `dca9284`: una cuenta demo con cortesía vigente sigue entrando con el modo demo apagado (Ana).
- `47077a2`: permiso `MODIFY_AUDIO_SETTINGS`: sin él, el WebView de la videollamada no abría el micrófono (`NotReadableError`, «Otra app está usando el micrófono») y caía al modo de mantener pulsado. Exige reinstalar la APK.
- `b69058f`: el panel muestra los minutos de prueba restantes según el ajuste vigente.

**Backend:**
- **Modificados:** `lib/correo.ts`, `lib/pagos/suscripciones.ts`, `routes/admin.ts`, `routes/auth.ts`, `routes/usuarios.ts`.
- **Nuevos:** `lib/codigos.ts`, `sql/012_registro_codigo.sql`.
- **Migración:** 012 aplicada con `npm run migrate`.
- **`.env`:** `SMTP_HOST=127.0.0.1`, `SMTP_PORT=25`, `SMTP_FROM=OneLingo <no-reply@onelingo.org>`, `PUBLIC_URL=https://onelingo.org/api` (Postfix + DKIM del propio VPS, ver runbook). Copia anterior en el backup (`env.anterior`, 600).

**Cuentas:** Ana (`ana@onelingo.demo`) con cortesía p3 «todos» sin vencimiento (antes vencía 2026-10-30 14:34). Bryan sin cambios (su cortesía venció).

**APK:**
- **Build:** `shorebird release android --artifact apk --target-platform android-arm,android-arm64 --build-number=2011 -- --dart-define=API_URL=https://onelingo.org/api` desde un worktree limpio de `b69058f`; Shorebird publicó la release 0.5.5+2011. Comprobado con `aapt2`: versionCode 2011, permisos RECORD_AUDIO y MODIFY_AUDIO_SETTINGS; `libapp.so` con `https://onelingo.org/api`.
- **`/descargas/onelingo.apk` y `/descargas/onelingo-armv7.apk`:** 163 MB, sha256 `b88e160b682a391a…`; `/descargas/version.json` 0.5.5. Escritas con nombre temporal y `mv`.
- Probado antes en el emulador (build debug contra producción, cuenta Ana): sin el permiso, `getUserMedia` daba `NotReadableError` y logcat «Requires MODIFY_AUDIO_SETTINGS and RECORD_AUDIO»; con el permiso, la llamada abre «Micrófono abierto» y pide `/llamada/token`.

**Backup:** `backups/20261030-edu-77-registro/` (`web-anterior`, `panel-anterior`, `backend/` con los 5 archivos previos, `backend-nuevos.txt`, `env.anterior`, `env.sha`, `onelingo-antes.dump`). Retirados en `staging/20261030-edu-77-registro/` (`web-retirada`, `panel-retirado`).

**Verificado:** `/api/salud` 200; `/auth/registro/codigo` responde con validación en español; entrada demo de Ana 200; `nodemailer.verify()` contra 127.0.0.1:25 correcto; panel, web, `/avatar/index.html` y la APK responden; `/version.json` 0.5.5; PM2 `onelingo-api` en línea sin errores; lock liberado.

**Rollback:** `ssh onelingo 'set -e; cd /var/www/onelingo; K=backups/20261030-edu-77-registro; S=staging/20261030-edu-77-registro; mv web $S/web-retirada-post && mv $S/web-retirada web; mv panel $S/panel-retirado-post && mv $S/panel-retirado panel; cp -r $K/backend/. backend/; (cd backend && xargs rm -f < ../$K/backend-nuevos.txt); install -m 600 -o onelingo -g onelingo $K/env.anterior backend/.env; sudo -u onelingo -H pm2 restart onelingo-api'`. Las columnas y la tabla de 012 pueden quedarse. La APK 0.5.4 anterior sigue en `web-anterior/descargas` (enlace duro).

## Release: 20261030-edu-78-llamada

Fecha: 2026-10-30 · Responsable: Claude (Claude Code), por pedido del usuario («sube el apk actualizado … mandas a producción»). Backend (3 archivos) + web 0.5.6 (incluye `web/avatar`) + APK 0.5.6+2012 con Shorebird; PM2 `onelingo-api` reiniciado (solo esa app). Sin migraciones ni cambios de `.env` (hash igual antes y después).

**Contenido:**
- `cc242eb`: `/chat?voz=1` manda la voz de cada frase en el mismo stream (evento `voz`, MP3 + tiempos de letras). En la llamada no se mide la sonoridad (ganancia fija de la voz, una pasada de ffmpeg) y guardar en disco/`audios` ya no retrasa la entrega. Medido en el VPS: ElevenLabs 0,25 s; medir+recodificar costaba ~0,2 s extra por frase.
- `8334bd5`: turnos de la videollamada. El tutor no arranca mientras el micrófono capta voz del alumno (tope 2,5 s); si el alumno sigue antes de oír al tutor, se une lo dicho y se borra la respuesta que no sonó; espera tras cerrar la frase 450 ms (1,7 s si queda colgando) + 250 ms en niveles 1–2; corte de frase de Scribe a 0,5 s. Halo/borde/«Te escucho» al ritmo de la voz, anillo mientras piensa, cursor en la transcripción, subtítulos que se desplazan en lugar de cortarse. Arreglo: `vivo.js` `nivel()` lanzaba siempre `ReferenceError` (analizador dentro del `try`): ningún efecto por energía funcionaba.
- `382fd1e`: `tools/pruebas/llamada_simulada.py` (alumno IA contra el tutor real en el emulador).
- `76e8a98`: app 0.5.6+2012.

**Pruebas:** backend 140/140 (`npx tsx --test test/*.test.ts`), `tsc` y typecheck en el VPS. Flutter 498 pruebas en verde (una primera corrida con el emulador encendido se cortó por tiempo, sin fallos de lógica). Simulación de 6 turnos en el emulador contra el backend local (alumno con pausas de 300–900 ms): 0 veces el tutor encima del alumno, una burbuja por turno, respuesta en 1,95–3,7 s (antes 2,7–4,4 s; el emulador suma 0,5–1,4 s al arrancar el audio porque dibuja el avatar por software). Producción, desde que llega el mensaje: primera frase 0,68–1,03 s, voz de esa frase +0,25–0,33 s.

**APK:** `shorebird release android --artifact apk --target-platform android-arm,android-arm64 --build-number=2012 -- --dart-define=API_URL=https://onelingo.org/api` desde un worktree limpio de `76e8a98`; Shorebird publicó la release 0.5.6+2012. `aapt2`: versionCode 2012, RECORD_AUDIO y MODIFY_AUDIO_SETTINGS; `libapp.so` con `https://onelingo.org/api`; firma igual a la 0.5.5 (se instala encima). `/descargas/onelingo.apk` y `onelingo-armv7.apk` (enlace duro): 171 MB, sha256 `a61c4dce7e21d24b…`; `/descargas/version.json` 0.5.6. Escritas con nombre temporal y `mv`. La página de la llamada no exige reinstalar: `index.html` va con `Cache-Control: no-cache` y la app 0.5.5 ya carga la nueva.

**Verificado:** `/api/salud` 200; `/version.json` 0.5.6; `/avatar/index.html` con `practice.js?v=61`; `/chat?voz=1` con Ana en producción manda `voz_activa`, `frase` y `voz`; PM2 `onelingo-api` en línea sin errores; `.env` sin cambios; lock liberado.

**Nota:** `/llamada/token` admite 30 tokens por alumno y hora (en memoria). Si el teléfono reconecta la transcripción cada ~20 s, se agota en ~10 min: pendiente la telemetría de cierres del WebSocket.

**Backup:** `backups/20261030-edu-78-llamada/` (`web-anterior` con enlaces duros, `backend/src/{lib/volumen.ts,lib/voz.ts,routes/chat.ts}` previos, `env.sha`, `onelingo-antes.dump`). Web retirada en `staging/20261030-edu-78-llamada/web-retirada`.

**Rollback:** `ssh onelingo 'set -e; cd /var/www/onelingo; K=backups/20261030-edu-78-llamada; S=staging/20261030-edu-78-llamada; mv web $S/web-retirada-post && mv $S/web-retirada web; cp -p $K/backend/src/lib/volumen.ts $K/backend/src/lib/voz.ts backend/src/lib/; cp -p $K/backend/src/routes/chat.ts backend/src/routes/; chown onelingo:onelingo backend/src/lib/volumen.ts backend/src/lib/voz.ts backend/src/routes/chat.ts; sudo -u onelingo -H pm2 restart onelingo-api'`. La APK 0.5.5 anterior queda en `web-anterior/descargas` (enlace duro).

## Release: 20261031-edu-79-auditoria

Fecha: 2026-10-31 · Responsable: Claude (Claude Code), por pedido del usuario («si despliega todo y sube el apk»). Backend (5 archivos) + web 0.5.7 (incluye `web/avatar`) + APK 0.5.7+2013 con Shorebird; PM2 `onelingo-api` reiniciado (solo esa app). Sin migraciones ni cambios de `.env` (hash igual antes y después).

**Contenido (auditoría de la videollamada con 4 agentes):**
- `4e662be`: backend. Tope de 10 s y 3 intentos con espera a cada llamada a ElevenLabs (antes podía colgarse minutos); caché de voz escrita con temporal + `rename` (no sirve MP3 vacíos ni a medias); ffmpeg resuelve en `close`; el stream de voz rechaza si el cliente corta; tope de 8 s por voz en `/chat?voz=1`; límites de longitud en `idiomaMeta`, `idiomaNativo` y `tutorId`; cortes de frase CJK con comillas de cierre. `/llamada/token` guarda en `eventos.datos` el motivo (`inicio|reconexion|visible`) y cómo se cerró la sesión anterior (`cierre`: código, razón, segundos, estado del audio, último aviso de Scribe); devuelve el cupo si ElevenLabs falla y manda `Retry-After` en el 429.
- `0b73e9e`: página de la llamada (`practice.js?v=62`, `vivo.js?v=5`). Reconexión acotada (1, 2 y 4 s, 3 intentos; antes pedía un token nuevo en cada corte y agotaba los 30/hora en ~10 min, visto en producción el 24-10 y el 30-10); una sola escucha abierta a la vez; la muletilla ya no anula la espera del turno; el filtro de eco no se come respuestas cortas («Yes», «Tea»); «Te escucho» no se queda pegado; «Repetir» sin carreras; la llamada se pausa al ocultarse y mantiene la pantalla encendida (Wake Lock).
- `5803536`: app. La llamada se pausa fuera de pantalla (otra pestaña o segundo plano) y reanuda al volver; `wakelock_plus`; reintento si la página no carga; el WebView solo navega dentro del visor; «Iniciar sesión» va al login; el permiso del micrófono no se vuelve a pedir al volver.
- `b9f9755`: app 0.5.7+2013.

**Pruebas:** backend 141/141 (`npx tsx --test test/*.test.ts`), typecheck en el VPS. Flutter 498 en verde. Emulador (APK debug contra el backend local): simulación de 6 turnos sin el tutor encima del alumno ni cortes del WebSocket; cambio de pestaña y HOME sueltan el micrófono y al volver se reabre (`motivo: visible`); cierre forzado del WebSocket reconecta y queda `{codigo:1006, segundos:5, audio:running}` con `motivo: reconexion`. Producción tras desplegar: `/chat?voz=1` con Ana en los 10 idiomas, todas las frases con voz y sin errores; `/llamada/token` guarda la telemetría (un evento de prueba con razón `prueba-despliegue`).

**APK:** `shorebird release android --artifact apk --target-platform android-arm,android-arm64 --build-number=2013 -- --dart-define=API_URL=https://onelingo.org/api` desde un worktree limpio de `b9f9755`; Shorebird publicó la release 0.5.7+2013. `aapt2`: versionCode 2013, RECORD_AUDIO y MODIFY_AUDIO_SETTINGS; `libapp.so` con `https://onelingo.org/api`; firma igual a la 0.5.6 (se instala encima). `/descargas/onelingo.apk` y `onelingo-armv7.apk` (enlace duro): 172 MB, sha256 `27090ae16697af94…`; `/descargas/version.json` 0.5.7. Escritas con nombre temporal y `mv`. La pausa al cambiar de pestaña y la pantalla encendida exigen esta APK (plugin nativo nuevo); el resto llega a la 0.5.6 por la web.

**Verificado:** `/api/salud` 200; `/version.json` 0.5.7; `/avatar/index.html` con `practice.js?v=62`; PM2 `onelingo-api` en línea sin errores; `.env` sin cambios; lock liberado.

**Backup:** `backups/20261031-edu-79-auditoria/` (`web-anterior` con enlaces duros, `backend/src/{lib/ia_openai.ts,lib/volumen.ts,lib/voz.ts,routes/chat.ts,routes/llamada.ts}` previos, `env.sha`, `onelingo-antes.dump`). Web retirada en `staging/20261031-edu-79-auditoria/web-retirada`.

**Rollback:** `ssh onelingo 'set -e; cd /var/www/onelingo; K=backups/20261031-edu-79-auditoria; S=staging/20261031-edu-79-auditoria; mv web $S/web-retirada-post && mv $S/web-retirada web; cp -p $K/backend/src/lib/*.ts backend/src/lib/; cp -p $K/backend/src/routes/*.ts backend/src/routes/; chown onelingo:onelingo backend/src/lib/ia_openai.ts backend/src/lib/volumen.ts backend/src/lib/voz.ts backend/src/routes/chat.ts backend/src/routes/llamada.ts; sudo -u onelingo -H pm2 restart onelingo-api'`. La APK 0.5.6 anterior queda en `web-anterior/descargas` (enlace duro).

**Pendiente:** leer `eventos` (`tipo='llamada_token'`, `datos->'cierre'`) tras unas llamadas reales en el teléfono para saber por qué Scribe se cortaba cada ~20 s.

## Release: 20261031-edu-80-play

Fecha: 2026-10-31 · Responsable: Claude (Claude Code), por pedido del usuario («si crea y sube todo»). Backend (6 archivos modificados, 2 nuevos, migración 013) + panel + web 0.5.8 + APK 0.5.8+2014 con Shorebird (y AAB para Google Play); PM2 `onelingo-api` reiniciado (solo esa app). Sin cambios de `.env` (hash igual antes y después).

**Contenido:**
- `a35e5c3`: tutor que decide como un profesor (jugadas A–F: autocorrección, repetición, error ya corregido, error importante, error menor, frase correcta), longitud por nivel, `estadoTurno()` (repite, segundo intento, respuestas muy cortas), corrector con tope de 8 s; modelo del tutor `OPENAI_MODELO_TUTOR` (por defecto `gpt-5.6-luna`, esfuerzo `none`). Evaluación en `docs/claude-educacion/auditoria/eval-tutor-2026-10-31.md` (2,89 → 3,62).
- `8a2ba0a`: Google Play. `/privacidad/`, `/terminos/`, `/eliminar-cuenta/` (es + en); `DELETE /usuarios/me` (las demo responden 403 `cuenta_demo`; cancela Stripe antes); `POST /reportes-ia` y panel «Reportes IA»; en la app: Perfil → Eliminar cuenta, enlaces legales, «Reportar respuesta» en el chat. Migración `013_cuenta_reportes_ia.sql` (`reportes_ia`, `cuentas_eliminadas`).
- `4749eb8`: la videollamada sale en inglés si la app está en inglés (`textos.js`, `practice.js?v=64`); las pestañas se traducen al momento.
- `b14c71e`: `docs/play/` (textos, gráficos, capturas, formularios). `f3e70c6`: app 0.5.8+2014.

**Nota:** en producción `config.ts` tenía `elevenModelo` por defecto `eleven_multilingual_v2` (el repo dice `eleven_flash_v2_5`); se conservó el de producción en el archivo desplegado. No cambia nada: `.env` fija `ELEVENLABS_MODELO`.

**APK/AAB:** `shorebird release android --artifact apk --target-platform android-arm,android-arm64,android-x64 --build-number=2014 -- --dart-define=API_URL=https://onelingo.org/api` desde un worktree limpio de `f3e70c6`; Shorebird publicó la release 0.5.8+2014. Incluye x86_64 (las anteriores no, y fallaban en emuladores x86_64). `aapt2`: versionCode 2014, RECORD_AUDIO y MODIFY_AUDIO_SETTINGS; `libapp.so` con `https://onelingo.org/api`. `/descargas/onelingo.apk` y `onelingo-armv7.apk` (enlace duro): 188 MB, sha256 `bc2c55c66693ca6b…`; `/descargas/version.json` 0.5.8. AAB 175 MB para Play (`build/app/outputs/bundle/release/app-release.aab` del worktree).

**Verificado:** `/api/salud` 200; `/version.json` 0.5.8; `/privacidad/`, `/terminos/`, `/eliminar-cuenta/` y `/panel/` 200; `/avatar/index.html` con `practice.js?v=64`; con Ana: `DELETE /usuarios/me` 403 `cuenta_demo`, `/chat` 200 (recast «I go → I went» y pregunta de seguimiento), `/reportes-ia` sin datos 400; tablas `reportes_ia` y `cuentas_eliminadas` creadas; PM2 en línea sin errores; `.env` sin cambios; lock liberado.

**Backup:** `backups/20261031-edu-80-play/` (`web-anterior` y `panel-anterior` con enlaces duros, `backend/src/...` previos, `backend-nuevos.txt`, `env.sha`, `onelingo-antes.dump`). Retirados en `staging/20261031-edu-80-play/{web-retirada,panel-retirado}`.

**Rollback:** `ssh onelingo 'set -e; cd /var/www/onelingo; K=backups/20261031-edu-80-play; S=staging/20261031-edu-80-play; mv web $S/web-post && mv $S/web-retirada web; mv panel $S/panel-post && mv $S/panel-retirado panel; for f in src/app.ts src/lib/config.ts src/lib/ia.ts src/lib/ia_openai.ts src/lib/pagos/proveedor.ts src/routes/usuarios.ts; do cp -p $K/backend/$f backend/$f; done; rm backend/src/lib/cuenta.ts backend/src/routes/reportes.ts; sudo -u onelingo -H pm2 restart onelingo-api'`. Las tablas de la 013 pueden quedarse (nadie las usa sin el código). La APK 0.5.7 queda en `web-anterior/descargas`.

## Release: 20261101-edu-81-parche-llamada-situada

Fecha: 2026-11-01 · Responsable: Claude (Claude Code), por pedido del usuario («dale, sube el parche cuando terminen»). Solo parche Shorebird de Android (Patch 1 sobre 0.5.8+2014, canal stable). Sin cambios en el servidor, la web ni el panel.

**Contenido:**
- `c9c13f4`: en Android, la «Videollamada» de un objetivo de situación ya no avisa «solo en la versión web». Abre `/tutores?tema=&objetivo=` con el nombre y el icono de la situación arriba. La llamada con el tutor elegido (en vivo o Lumo) y el «Hablar con mi tutor» empiezan en esa situación y ese objetivo.
- `b6cc28b`: el aviso usa el icono de la situación. Un icono nuevo cambiaba `MaterialIcons-Regular.otf` (asset), y los parches no llevan assets.
- Sin textos nuevos: los parches no llevan `assets/i18n`.

**Build:** `shorebird patch android --release-version=0.5.8+2014 --no-confirm -- --dart-define=API_URL=https://onelingo.org/api` desde un worktree limpio de `b6cc28b`, con `key.properties` y el wrapper de Gradle copiados del worktree de la release. Los parches van firmados con la llave que administra Shorebird, la misma que la release. arm32 440 KB, arm64 375 KB, x86_64 420 KB. Pruebas antes: `flutter test` completo (504 en verde) y `extraer.py --comprobar` (0 errores).

**Alcance:** el AAB de Google Play es la misma release de Shorebird (`libapp.so` y `libflutter.so` idénticos a la APK 2014). El parche llega a la app de Play y a la APK de onelingo.org al abrirla, y se aplica en el siguiente arranque. La web (Flutter web) sigue sin desplegar: allí la llamada situada abre directamente con Lumo hasta el próximo despliegue web.

**Rollback:** `shorebird patches rollback --release-version=0.5.8+2014` (vuelta atrás con `patches rollforward`). Las apps vuelven al código de la release en el siguiente arranque.

## Release: 20261101-edu-81-web

Fecha: 2026-11-01 · Responsable: Claude (Claude Code), por pedido del usuario («si despliega también la web y habilitemos ana torres como si tuviera el plan de 20»). Web 0.5.8 con `c9c13f4` y `b6cc28b` (lo mismo del parche 1 de Android) + cambio de plan de Ana. Sin cambios en el backend, `.env` ni PM2.

**Web:** `flutter build web --release --dart-define=API_URL=https://onelingo.org/api` desde un worktree limpio de `1e48776`. Staging con enlaces duros de `web/` y `rsync -rlc` encima (3 archivos cambiados; `descargas/` intacta). Cambio atómico con `mv`. Ahora, en la web, la videollamada de una situación también abre la galería de tutores y empieza en la situación elegida.

**Ana (`ana@onelingo.demo`):** pasa de cortesía `p3` con todos los idiomas a cortesía `p1` (un idioma, el plan de 20 USD) con inglés, sin vencimiento, vía `darCortesia()`. Sigue siendo `es_demo` y entra por el panel demo.

**Verificado:** `/`, `/main.dart.js` (con `/tutores?tema=` y sin el aviso «disponible en la versión web»), `/avatar/index.html`, `/descargas/version.json`, `/privacidad/` y `/api/salud` en 200. Ana: `usuarios.plan_id = p1`, cortesía activa, `idiomas = {en}`, sin `periodo_fin`.

**Backup:** `backups/20261101-edu-81-web/web-anterior` (enlaces duros) y `backups/20261101-ana-p1/ana-suscripcion-antes.csv`. Web retirada en `staging/20261101-edu-81-web/web-retirada`.

**Rollback:**
- **Web:** `ssh onelingo 'set -e; cd /var/www/onelingo; S=staging/20261101-edu-81-web; mv web $S/web-post && mv $S/web-retirada web'`.
- **Ana:** volver a darle cortesía `p3` con `idiomas: 'todos'`, sin fecha, desde Panel → Suscripciones o con `darCortesia()`.

**Ajuste de Ana (mismo día, por pedido del usuario: «demos acceso para probar todos los idiomas, y cambia de demo a usuario con suscripción»):**
- Cortesía `p1` con `todos_idiomas = true`: los 10 idiomas abiertos, sin vencimiento.
- `usuarios.es_demo = false`: cuenta como usuaria normal en las analíticas y en el panel.
- Sigue entrando por el panel DEMO, porque `/usuarios/login` mira el dominio `@onelingo.demo` y no `es_demo`. Con la cortesía vigente también entra con el modo demo cerrado, y sigue sin poder borrarse por el dominio.
- Verificado por la API: login demo correcto, `GET /usuarios/me/suscripcion` devuelve `p1`, `cortesia`, `activa` y 10 de 10 idiomas abiertos.
- Respaldos: `backups/20261101-ana-p1/ana-suscripcion-antes-todos.csv` y `ana-es-demo-antes.txt`.

## Release: 20261101-edu-82-correccion-voz

Fecha: 2026-11-01 · Responsable: Claude (Claude Code), por pedido del usuario («si publica»). Backend (2 archivos) + web 0.5.8 (incluye `web/avatar`) + parche 2 de Shorebird. PM2 `onelingo-api` reiniciado (solo esa app). Sin migraciones ni cambios de `.env` (hash igual antes y después).

**Contenido:**
- `ee8019d`: videollamada. El tutor corrige en voz alta, explica el porqué (en N1–N2 con un contraste, p. ej. «Today I go, yesterday I went») y pide repetir; como máximo dos intentos por error. Un revisor rápido (`veredictoRapido`, `gpt-5.6-luna` sin razonamiento, tope 1,5 s) corre en paralelo con el tutor. Si encuentra un error que el tutor no corrigió en voz alta, se descarta el borrador y el tutor responde con el veredicto en la nota de estado. En la página (`practice.js?v=65`): tarjeta «original → correcto» bajo los subtítulos; el turno del tutor entra al historial con el texto completo (antes esperaba al corrector, hasta 8 s, y si el alumno contestaba antes se perdían la petición de repetir, la tarjeta y el turno guardado); la repetición de la frase modelo ya no se descarta como eco. Evaluación en `docs/claude-educacion/auditoria/eval-tutor-2026-10-31.md` («Veredicto antes de hablar»).
- `07541ee`: «Escucha y repite». El fin por silencio se mide contra el pico de la voz (con ganancia automática el ruido quedaba sobre -50 dBFS y la grabación de un «hello» seguía abierta), medidor de voz y aviso «Transcribiendo tu respuesta…».

**Pruebas:** backend 153/153 y typecheck en el VPS; Flutter 507 en verde; eval v5 con los 16 turnos con error corregidos en voz alta.

**Verificado en producción** (Ana, `avatar_chloe`, inglés N2, `/chat` con SSE):
- «Yesterday I go to the park…»: dice la forma correcta, da el contraste y pide repetirlo; tarjeta `I go → I went`; primera frase en 1,17 s.
- Frase correcta: no corrige; 1,20 s.
- Repetición correcta: lo celebra y sigue; 0,98 s.
- `/`, `/main.dart.js`, `/avatar/index.html` (`practice.js?v=65`), `/descargas/version.json`, `/privacidad/` y `/api/salud` en 200. PM2 en línea. `.env` sin cambios. Lock liberado.

**Web:** `flutter build web --release --dart-define=API_URL=https://onelingo.org/api` desde un worktree limpio de `ee8019d`. Staging con enlaces duros y `rsync -rlc` encima (5 archivos; `descargas/` intacta). Cambio con `mv`. Android carga la llamada desde `onelingo.org/avatar`, así que el arreglo de la llamada le llega sin parche.

**Backup:** `backups/20261101-edu-82-correccion-voz/` (`web-anterior` con enlaces duros, `backend/src/lib/{ia.ts,ia_openai.ts}` previos, `env.sha`). Web retirada en `staging/20261101-edu-82-correccion-voz/web-retirada`.

**Rollback:**
- **Backend y web:** `ssh onelingo 'set -e; cd /var/www/onelingo; K=backups/20261101-edu-82-correccion-voz; S=staging/20261101-edu-82-correccion-voz; mv web $S/web-post && mv $S/web-retirada web; cp -p $K/backend/src/lib/*.ts backend/src/lib/; sudo -u onelingo -H pm2 restart onelingo-api'`.
- **Android:** `shorebird patches rollback --release-version=0.5.8+2014` vuelve al parche 1 (vuelta atrás con `patches rollforward`).

**Parche 2 de Android** (sobre 0.5.8+2014, canal stable): lleva «Escucha y repite» (`07541ee`) a la app de Play y a la APK. Sin assets nuevos: «Transcribiendo tu respuesta…» ya estaba en `assets/i18n` de la release. Comando: `shorebird patch android --release-version=0.5.8+2014 --no-confirm -- --dart-define=API_URL=https://onelingo.org/api`, lanzado desde un worktree limpio de `ee8019d` en `~/.cache/onelingo-build/edu82`. Allí se copiaron `key.properties` y el wrapper de Gradle. El primer intento falló en `/tmp`: el tmpfs se quedó sin espacio. Por eso el build va en el disco principal, con `TMPDIR` y `java.io.tmpdir` ahí. Tamaño: arm32 888 KB, arm64 871 KB, x86_64 862 KB. Se aplica al abrir la app y cobra efecto en el siguiente arranque.
