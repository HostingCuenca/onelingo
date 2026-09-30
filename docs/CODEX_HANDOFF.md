# Handoff maestro de OneLingo

Actualizado: 2026-09-30. Este archivo permite continuar en otra cuenta de Codex sin reconstruir toda la historia de conversación.

## Punto de partida comprobado

- Proyecto: `/home/roggrt/Documents/onelingo`
- Rama: `claude/educacion-multilenguaje`
- Commit base al crear este handoff: `d4e2dcd`.
- Árbol de trabajo: deliberadamente sucio, con cambios de producto, contenido, pruebas y documentos sin commit. No descartarlo ni asumir que los archivos sin seguimiento son solo transferencia.
- Producción: <https://onelingo.hostingcuenca.com>
- Backend público: `https://onelingo.hostingcuenca.com/api`; salud: `/api/salud`.
- Producción documentada: `20260930-edu-5-n2-n3-review`; N1 y N2 completos y N3 C1–C90 activos, backend sin cambios desde `20260926-edu-2-a1-voz`.
- El alcance de `20260926-edu-3-escrituras` quedó absorbido por `20260929-edu-4-n1-runtime`; ya no debe desplegarse por separado. Consultar `docs/claude-educacion/DESPLIEGUES.md`.

## Producto actual

OneLingo es una app Flutter web/Android de aprendizaje personalizado. Incluye onboarding, diagnóstico adaptativo, camino educativo, gramática, vocabulario, situaciones, práctica, tutor conversacional, voz, progreso y panel administrativo. La experiencia se centra primero en inglés, con una arquitectura preparada para diez idiomas.

Idiomas activos: inglés, español, francés, alemán, portugués, italiano, chino, japonés, coreano y ruso. La escala histórica interna 0–10 se conserva sin sobrescritura. El currículo nuevo usa `client-10-levels-v1`: N1=A1 completo, N2=A2, N3–N4=B1, N5–N7=B2 y N8–N10=C1; Fundamentos sigue separado como nivel 0.

## Estado educativo

- Núcleo del esquema 2 en `lib/core/aprendizaje/`.
- Contenido en `assets/contenido/<idioma>/ruta/`.
- Fundamentos completos en los diez idiomas: seis unidades por idioma.
- La ruta inglesa local ya no indexa las 29 unidades A1 heredadas: publica el nivel editorial `n1` con 100 clases. Los archivos heredados siguen preservados como respaldo y fuente de trazabilidad.
- Escrituras y sonidos de Fundamentos, más A1 «Primeras frases», presentes en los diez idiomas: 204 unidades documentadas.
- Práctica con repetición de fallos al final, celebración, tablas de escritura/conjugación y pronunciación por idioma.
- Nueve idiomas continúan como «versión inicial» sin revisión nativa.
- N2 de inglés está completo y activo en producción. N3 C1–C90 está activo; C91–C100 está pendiente de autoría. N4–N10 y la profundización del resto siguen pendientes; niveles altos fuera de inglés aún dependen de contenido legado/genérico.
- El PDF maestro inglés ya está transcrito en `assets/contenido/en/curriculo-master.json`: 10 niveles y 1.000 especificaciones. No son todavía 1.000 clases publicables.
- M1 editorial tiene dry-run reproducible en `docs/claude-educacion/reportes/import-en-inicial/`: 36 unidades y 528 variantes, 0 errores, sin aplicar ni activar.
- La decisión de escala quedó resuelta en DEC-020 y tiene migración conservadora de diagnóstico/progreso.
- Los mapas editoriales cubren N1–N10 con 1.000 IDs planificados. No equivalen a clases publicables.
- Inglés N1 1–100 está redactado, integrado y publicado: 100 clases, 1.300 ejercicios y pools separados de guiada, práctica, evaluación y repaso. La pantalla de unidad consume `exercise-library.json`, registra `variantId`, versión y selección y no depende del tutor IA.
- Inglés N2 tiene mapa editorial v2 y C1–C100 completas: 100 clases y 1.300 ejercicios, cierres acumulativos cada cinco clases, revisión cruzada y validación longitudinal. Está indexado y activo en la release `20260930-edu-5-n2-n3-review`.
- Inglés N3 tiene mapa editorial v2 completo. C1–C90 están integradas y activas con 1.170 ejercicios y GO independiente. C91–C100 no tiene artefactos integrados y es el siguiente trabajo.
- Respaldo recomendado anterior a DEC-020: `backups/education-pre-client-scale-20260927T193146-clean.tar.gz`, SHA-256 `6ed6a436e33f9078dac0ae36ba85da5f6851811a93e058d080eb5fdbbf7b75c8`.

Lee, en este orden, solo si trabajas en educación:

1. `docs/claude-educacion/HANDOFF.md`
2. `docs/claude-educacion/PROGRESO.md`
3. la sección pertinente de `docs/claude-educacion/CHECKLIST.md`
4. `docs/claude-educacion/ESQUEMA_CONTENIDO.md`
5. `docs/claude-educacion/MAPA_CURRICULAR.md` y las auditorías cuando el cambio sea curricular.

## IA y voz actuales

- Backend: Node.js/TypeScript, Fastify 5 y PostgreSQL.
- Tutor: OpenAI `gpt-4.1-mini` por defecto, Chat Completions con JSON Schema y streaming de tokens en el flujo del avatar.
- STT: OpenAI `gpt-4o-mini-transcribe`, mediante archivo WebM/Opus o M4A completo enviado a `POST /transcribir` después de terminar la grabación.
- TTS: ElevenLabs `eleven_flash_v2_5`; `GET /voz/stream` transmite MP3 y conserva en caché solo audio completo.
- Diagnóstico: Gemini Flash primero y OpenAI como respaldo; en producción se documentó un 403 de Gemini, por lo que debe verificarse antes de depender de él.
- Todas las APIs externas pasan por el backend. Las claves están en archivos `.env` ignorados por Git.
- El tutor web detecta voz con umbral local y finaliza tras 3 segundos de silencio, 15 segundos sin empezar o 60 segundos totales. La transcripción no es streaming.

Documentación: `IA.md`, `docs/voz/latencia-streaming.md`, `docs/voz/microfono-silencio.md`, `docs/CONNECTORS_AND_SERVICES.md`.

## Avatares

- Entrada Flutter: `/avatar`.
- Web: iframe a `web/avatar/index.html`; Android usa actualmente `avatar_screen_stub.dart` y no muestra el tutor 3D.
- Diez tutores GLB en `web/avatar/models/`, de 21–28 MB cada uno, cerca de 250 MB en total.
- Three.js carga el GLB, baja los brazos en tiempo de ejecución y anima idle, parpadeo y boca por amplitud.
- Los modelos contienen aproximadamente 32 morph targets, pero no animaciones incrustadas ni un rig facial comprobado de 52 ARKit. El labial actual no usa fonemas/visemas temporizados.
- El tutor recibe idioma, nivel, sectores, objetivos, diagnóstico, refuerzos e historial. Aún no recibe de forma completa la unidad/lección activa aunque el esquema educativo ya guarda metadatos `tutor`.
- Decisión recomendada para la experiencia principal: tutor humano 2D reutilizable con Rive, estados y visemas; conservar el 3D como laboratorio hasta resolver peso, Android y sincronización facial.

Lee `docs/AVATAR_STRATEGY.md` antes de cambiar esta área.

## Home y visuales que se conservan

El home vigente integra el logo oficial, seis iconos propios, la imagen «Aprende hoy», mascota, racha, accesos educativos y banner de avatares. No sustituirlos por iconos genéricos ni volver a layouts anteriores sin petición explícita. Los assets están bajo `assets/img/` y `assets/img/home-icons/`.

## Android/APK

- `pubspec.yaml`: versión `0.1.0+1` al crear este handoff.
- APK debug reciente: `build/app/outputs/flutter-apk/app-debug.apk`, ~120 MB, 2026-09-26.
- APK release existente: ~62 MB, 2026-09-08; no asumir que representa el código actual.
- El release Android aún usa la clave de depuración. Antes de distribución real hacen falta keystore de producción, aumento de versión, política de actualización y prueba en dispositivo.
- APK publicados documentados: `/apk/onelingo-prueba.apk` y `/apk/onelingo-abierto.apk`. No sobrescribirlos durante un deploy web.
- Una app instalada no incorpora automáticamente cambios Flutter web. Para actualizaciones sin reinstalar hace falta decidir entre publicación normal en tienda o un contenedor web/PWA controlado; no se ha implementado esa migración.

## Infraestructura

- Servidor documentado: Hetzner, Ubuntu 22.04, IP `167.235.20.41`.
- SSH: `ssh -F /dev/null root@167.235.20.41`.
- Web: `/var/www/onelingo/web`; backend: `/var/www/onelingo/backend`; proceso PM2: `onelingo-api`.
- Lock obligatorio de despliegue: `/tmp/onelingo-deploy.lock` en el servidor.
- Compartido con otros servicios: no reiniciar ni modificar recursos ajenos.
- La release web más reciente se publicó por staging y renombre atómico; SSH, HTTPS, salud, PM2, APK y avatar quedaron verificados.

Usa `docs/DEPLOYMENT_RUNBOOK.md` y el historial `docs/claude-educacion/DESPLIEGUES.md`.

## Prioridad al retomar

1. Verificar rama, commit, árbol y estado real de producción; no volver a auditar todo.
2. Producir N3 C91–C95 y C96–C100 con autoría, auditoría y GO independientes; después auditar N3 C1–C100.
3. Ampliar el runtime de 290 a 300 clases solo tras GO y una decisión consciente de release.
4. Crear y aprobar el mapa editorial v2 de N4 antes de autorizar su contenido; repetir por nivel.
5. Mantener la ruta base sin tutor IA obligatorio y separar práctica, evaluación y repaso editorial por unidad.
6. Tratar Rive, avatar 3D, latencia de voz y Android como líneas separadas del currículo.

El checklist vivo está en `docs/ACTIVE_CHECKLIST.md`.
