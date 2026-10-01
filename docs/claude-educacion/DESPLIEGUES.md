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
