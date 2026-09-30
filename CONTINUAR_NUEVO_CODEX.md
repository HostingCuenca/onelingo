# OneLingo — punto único para continuar en otra cuenta de Codex

**Ruta absoluta de este proyecto:** `/home/roggrt/Documents/onelingo`

Este documento es la entrada maestra. La nueva instancia debe leerlo completo antes de revisar archivos o hacer cambios.

## Prompt exacto para pegar en la nueva cuenta

```text
Continúa el proyecto OneLingo existente en esta computadora y dirige la producción editorial restante de Inglés con agentes en paralelo. Abre `/home/roggrt/Documents/onelingo` y lee completo `/home/roggrt/Documents/onelingo/CONTINUAR_NUEVO_CODEX.md`; úsalo como fuente maestra y no hagas un barrido general del repositorio. Primero congela el estado: verifica rama/commit, árbol, release de producción, hashes, salud, conteos del runtime y diferencias materiales sin modificar el producto. Confirma que producción contiene N1 C1–C100, N2 C1–C100 y N3 C1–C90, y que N3 C91–C100 no está activo. Después reanuda en N3 C91–C95 y C96–C100 usando roles separados de autor, validador mecánico, auditor pedagógico/adversarial, simulador de estudiantes e integrador; ningún agente puede aprobar su propio contenido. Mantén 100 % de validación automática y usa muestreo pedagógico determinista orientado al riesgo para evitar revisar manualmente cada ejercicio: escala a revisión completa si aparece cualquier P1, dos P2 o un fallo sistémico. Integra únicamente bloques con expediente GO y hashes reproducibles. Al terminar N3, ejecuta auditoría longitudinal de las 100 clases y solo entonces amplía conscientemente el corte del compilador/runtime. Antes de N4, crea y aprueba un mapa editorial v2 propio; no autorices N4–N10 a partir de los mapas legacy. Conserva activos, APK, avatar, backend, `.env` y cachés. Para cada release sigue lock → backup → staging → validación → activación atómica → verificación visual/HTTP → rollback documentado. Informa avances por bloque, incidencias y puertas GO/NO-GO; no te detengas entre bloques aprobados salvo que exista un bloqueo real, riesgo de producción o decisión material que requiera al usuario.
```

## Instrucciones para la nueva instancia

Estás retomando un proyecto activo con bastante trabajo previo. No reconstruyas la historia desde cero. Usa este archivo y la documentación enlazada para cargar contexto por área.

1. Abre `/home/roggrt/Documents/onelingo` como proyecto local existente.
2. Lee `AGENTS.md` y `docs/CODEX_HANDOFF.md`.
3. Ejecuta:

   ```bash
   git status --short --branch
   git log --oneline -5
   ```

4. El punto base esperado es la rama `claude/educacion-multilenguaje`, commit `d4e2dcd`. El árbol está deliberadamente sucio: contiene cambios de producto, contenido editorial, pruebas y documentos sin commit. No lo limpies, descartes ni sobrescribas; verifica primero diferencias materiales y propiedad de cada cambio.
5. No hagas un análisis completo de todos los archivos. Lee únicamente la documentación correspondiente a la tarea.
6. Verifica conectores y servicios sin mostrar secretos.
7. Informa las diferencias materiales. Si el usuario pegó el prompt anterior, continúa con el primer lote pendiente siguiendo las puertas de este documento; no regeneres bloques ya aprobados.

## Estado resumido

- Producción: <https://onelingo.hostingcuenca.com>
- API: `https://onelingo.hostingcuenca.com/api`
- Salud: `https://onelingo.hostingcuenca.com/api/salud`
- Producción documentada: `20260930-edu-5-n2-n3-review`; N1 y N2 completos y N3 C1–C90 están activos. El backend no cambió desde `20260926-edu-2-a1-voz`.
- El alcance de `20260926-edu-3-escrituras` quedó absorbido por la release vigente; no debe desplegarse por separado.
- App Flutter para web y Android; backend Node.js/TypeScript, Fastify y PostgreSQL.
- Diez idiomas: en, es, fr, de, pt, it, zh, ja, ko y ru.
- Fundamentos completos en diez idiomas, inglés A1 completo y 204 unidades documentadas entre escrituras y primeras frases.
- Nueve idiomas siguen como versión inicial sin revisión nativa.
- Inglés integrado y publicado: 290/1.000 clases y 3.770 ejercicios: N1 C1–C100, N2 C1–C100 y N3 C1–C90. Los JSON editoriales conservan `status: shadow` como etapa de autoría, pero el manifiesto runtime los declara `active` y `curso.json` publica N1–N3.
- Inglés pendiente comprobado: N3 C91–C100 no tiene artefactos integrados; N4–N10 requieren primero mapas editoriales v2 propios y después 700 clases/9.100 ejercicios.

## Inglés: inventario operativo y dónde ver lo pendiente

| Nivel | Clases | Ejercicios | Estado editorial | Runtime/producción | Próxima acción |
| --- | ---: | ---: | --- | --- | --- |
| N1 · A1 | 100/100 | 1.300 | completo | `active`, publicado | mantenimiento |
| N2 · A2 | 100/100 | 1.300 | completo | `active`, publicado | revisión del cliente |
| N3 · B1 inicial | 90/100 | 1.170 | C1–C90 completas | `active`, C1–C90 publicado | producir C91–C100 |
| N4–N10 | 0/700 | 0/9.100 | no iniciados | no activos | crear mapa v2 de cada nivel antes de autoría |

Totales: **290/1.000 clases y 3.770/13.000 ejercicios publicados**. Pendientes: **710 clases y 9.230 ejercicios**.

Fuentes de verdad, en este orden:

1. Estado operativo y siguiente lote: `docs/ACTIVE_CHECKLIST.md`.
2. Cola y reglas: `docs/claude-educacion/ENGLISH_EDITORIAL_PIPELINE.md`.
3. Registro cronológico: `docs/claude-educacion/PROGRESO.md`.
4. Mapa vigente N3: `assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json`.
5. Clases aprobadas: `assets/contenido/en/editorial/n1/`, `n2/` y `n3/`.
6. Runtime compilado: `assets/contenido/en/ruta/curso.json`, `n1-editorial.json`, `n2-editorial.json`, `n3-editorial.json`, `exercise-library.json` y `exercise-activation.json`.
7. Release y rollback: `docs/claude-educacion/DESPLIEGUES.md`.

Notas para no contar mal:

- N1 C1–C5 viven dentro de `pilot-classes-01-05.json`; contar solo `class-*.json` devuelve falsamente 95.
- El nombre `tools/contenido/generar_runtime_n1.py` es histórico: ahora compila el corte explícito N1=100, N2=100 y N3=90 declarado en `LEVELS`.
- `status: shadow` describe la etapa editorial del JSON fuente; la activación visible se decide en `exercise-activation.json`.
- `work/` y `build/` son staging/evidencia, no autoridad de publicación.

Pendiente concreto inmediato:

- N3 C91–C95: bloque `community-project`, con C95 como transferencia acumulativa.
- N3 C96–C100: bloque `b1-entry-capstone`; debe revisarse completo por ser cierre de nivel.
- C99: borrador/revisión de 100–130 palabras, checklist de cuatro criterios y tres cambios sustantivos.
- C100: 100–140 palabras, cinco conceptos y evidencia de cronología, opciones/condición, fuentes, coordinación y revisión.
- Después: auditoría longitudinal N3 C1–C100, integración, recompilación consciente del corte a 300 clases, pruebas y release.
- N4 es **NO-GO para autoría** hasta producir y auditar `mapa-n4-editorial-v2.json`. Lo mismo aplica sucesivamente a N5–N10.

## Ejecución continua con agentes

Usar tantos agentes en paralelo como permita la sesión, pero asignarles archivos y decisiones no solapados. Con cuatro plazas, el agente principal coordina e integra y tres agentes trabajan en paralelo. Ningún agente aprueba su propio contenido.

Roles:

1. **Planificador/coordinador:** congela mapa, alcance, prerequisitos y digest; mantiene el ledger y decide el orden.
2. **Autor:** produce solo en staging un generador reproducible, cinco clases, bundle, informe y manifiesto; entrega `DRAFT`.
3. **Validador mecánico/simulador:** ejecuta contratos, idempotencia, cinco perfiles de estudiante y pruebas de runtime; no juzga su propia autoría.
4. **Auditor pedagógico/adversarial:** busca ambigüedad, fuga de respuestas, distractores débiles, fuentes invisibles, remediación incompleta y progresión artificial; emite `GO`, `REVISE` o `REJECT`.
5. **Integrador:** promueve únicamente expedientes `GO` con hashes coincidentes, actualiza pruebas longitudinales y recompila el runtime solo cuando el alcance esté explícitamente aprobado.

Cadencia recomendada:

- Ola 1: autor C91–C95; autor C96–C100; validador prepara/ejecuta controles acumulativos C1–C90.
- Ola 2: los autores corrigen hallazgos cruzados; el auditor revisa C91–C95 por muestra y C96–C100 completo.
- Ola 3: integrador promueve ambos bloques; validador ejecuta N3 C1–C100 y luego las pruebas globales.
- Ola 4: solo tras GO del nivel, actualizar `LEVELS` de 90 a 100, regenerar runtime y preparar release.

No esperar a que termine toda una ola para comunicar un fallo reproducible: el revisor debe devolverlo al autor inmediatamente. Sí esperar al expediente GO completo antes de integrar.

## Cómo revisar a grandes rasgos sin inspeccionar uno por uno

La calidad escalable combina **100 % de control automático** con **muestreo pedagógico determinista basado en riesgo**. Nunca se sustituye la validación total por una mirada rápida.

| Puerta | Cobertura | Condición de avance |
| --- | ---: | --- |
| G0 mapa | 100 % | 20 bloques, fases, IDs, prerequisitos, tareas y digest congelados |
| G1 reproducibilidad | 100 % | doble generación idéntica, seeds estables y manifiesto válido |
| G2 contrato editorial | 100 % | 13 ejercicios por clase, pools separados, hashes y remediación válidos |
| G3 runtime | 100 % | todos los formatos se muestran y puntúan realmente en Flutter |
| G4 simulación | 5 perfiles × 100 % de clases | principiante, carga alta, fallo total, acierto total y reingreso pasan |
| G5 muestra pedagógica | 25–40 % por bloque | naturalidad, ambigüedad, evidencia, distractores y feedback correctos |
| G6 longitudinal | cada 20 y 100 clases | progresión, reutilización, variedad, cierres y transición válidos |
| G7 integración | solo tras GO | autor, revisor e integrador distintos; hashes coinciden |

Muestra normal de un bloque de cinco:

- clase `transfer` completa;
- `t06`, `e04` y `r03` de `production`;
- una clase entre `input/form/comprehension`, elegida por hash: `e04`, `r03`, dos distractores y la remediación de `e04`;
- todos los ítems con audio nuevo, escritura libre, completar multiparte, puntuación parcial o formato nuevo.

Escalar automáticamente a revisión completa cuando ocurra cualquiera de estos casos:

- un P0: `REJECT` inmediato;
- un P1: `REVISE` y revisión completa del bloque;
- dos P2 o el mismo P2 repetido;
- el mismo fallo en dos bloques: escaneo del nivel y pausa de la cola;
- fallo de un generador compartido: regenerar y validar todos sus bloques;
- primer o último bloque de nivel, primera herramienta nueva o bloque posterior a un fallo sistémico.

Para N3: C91–C95 usa la muestra normal más revisión completa de C95 y la escritura de C94; C96–C100 se revisa al 100 % y C100 se contrasta transversalmente con todo N3.

El coordinador puede declarar “está bien” a grandes rasgos únicamente si el tablero muestra: conteos exactos, cero huecos/duplicados, todos los manifiestos válidos, G0–G7 en verde, cero P0/P1 abiertos, P2 corregidos o justificados, simulaciones completas y muestra independiente aprobada. No necesita leer manualmente los 1.300 ejercicios si esas evidencias existen.

## Validaciones editoriales y de release

Por bloque:

```bash
python3 tools/contenido/validar_bundle_editorial.py \
  --file <bundle> --start <inicio> --end <fin> --level <nivel>
sha256sum -c <MANIFEST.sha256>
python3 -m unittest discover -s test_tools
```

Antes de integrar o publicar:

```bash
cd /home/roggrt/Documents/onelingo
python3 tools/contenido/generar_runtime_n1.py
python3 tools/validar_ruta.py
python3 -m unittest discover -s test_tools
~/flutter/bin/flutter analyze --no-pub lib/core/aprendizaje lib/features/ruta
~/flutter/bin/flutter test --no-pub
~/flutter/bin/flutter build web --release --no-pub \
  --dart-define=API_URL=https://onelingo.hostingcuenca.com/api
```

Estado de referencia de `20260930-edu-5-n2-n3-review`: 10 idiomas/0 errores de ruta; 61 pruebas Python; 169 pruebas Flutter pasan y 1 se omite; análisis focalizado sin problemas. El análisis global conserva 12 avisos heredados.

## IA y voz

- Tutor: OpenAI `gpt-4.1-mini` por defecto.
- STT: OpenAI `gpt-4o-mini-transcribe`.
- TTS: ElevenLabs `eleven_flash_v2_5` con MP3 streaming y caché.
- Diagnóstico: Gemini Flash con respaldo OpenAI; se documentó un 403 de Gemini en producción y debe verificarse.
- El audio web se graba completo con `MediaRecorder`; se corta tras 3 segundos de silencio y luego se envía a `/transcribir`. STT no es streaming.
- El LLM y TTS tienen rutas de streaming.
- Variables y claves viven en `.env` ignorados por Git. No leer, copiar ni imprimir sus valores.

Archivos principales:

- `backend/src/lib/config.ts`
- `backend/src/lib/ia_openai.ts`
- `backend/src/lib/voz.ts`
- `backend/src/routes/chat.ts`
- `backend/src/routes/voz.ts`
- `web/avatar/practice.js`
- `IA.md`
- `docs/voz/latencia-streaming.md`
- `docs/voz/microfono-silencio.md`

## Avatares

- Ruta de producto: `/avatar`.
- Flutter web inserta `web/avatar/index.html`; Android muestra actualmente una pantalla de reserva.
- Hay diez GLB en `web/avatar/models/`, de 21–28 MB cada uno.
- Three.js anima idle, parpadeo y boca según amplitud del audio.
- No existe lip-sync fonético fiable: usa principalmente `viseme_aa` y amplitud.
- Los GLB tienen alrededor de 32 morph targets, sin 52 ARKit ni animaciones faciales comprobadas.
- El tutor recibe perfil, nivel, idioma, objetivos e historial, pero aún no integra completamente la unidad educativa activa.
- Dirección recomendada: un tutor humano 2D reutilizable con Rive, state machine y 15–20 visemas; conservar el 3D como laboratorio.

Leer antes de trabajar aquí:

- `docs/AVATAR_STRATEGY.md`
- `docs/CONNECTORS_AND_SERVICES.md`
- `docs/avatar-ia.md`

## Higgsfield, Meshy y Blender

- Plugin Higgsfield: `app-6a3293e129088191abf0875820e839da@openai-curated-remote`.
- Versión local encontrada: `2.1.0`.
- Referencia original de Mia: `7deb8fa0-fcbe-46b0-80a0-ce3c4838d416`.
- Video previo: `https://d8j0ntlcm91z4.cloudfront.net/user_3GYKg4yT6z80ijaVCbuhm6zNW5Y/hf_20260911_210525_43aea2a0-aa25-46c6-a889-5538cae9f1e9.mp4`.
- La nueva cuenta debe comprobar si Higgsfield está instalado y autenticado. La caché local no garantiza OAuth activo.
- Enumerar las herramientas MCP realmente disponibles antes de afirmar que existe `generate_3d`.
- En una sesión anterior, el modelo image-to-3D pidió `generate_3d`, pero esa herramienta no estaba expuesta y no se obtuvo GLB por ese flujo.
- Meshy fue considerado, pero no hay un conector Meshy confirmado.
- Blender existe en `/snap/bin/blender`; anteriormente el entorno Codex encontró un problema de scope/DBus. No hay fuentes `.blend` versionadas.
- Higgsfield debe servir para referencias, hojas de personaje, expresiones y movimiento. No generar un video por cada respuesta del tutor.

## Arquitectura educativa

- Núcleo: `lib/core/aprendizaje/`.
- Contenido nuevo: `assets/contenido/<idioma>/ruta/`.
- Pantallas: `lib/features/ruta/`.
- Validador: `python3 tools/validar_ruta.py`.
- Fuente operativa pedagógica: `docs/ACTIVE_CHECKLIST.md` y `docs/claude-educacion/ENGLISH_EDITORIAL_PIPELINE.md`. `docs/claude-educacion/HANDOFF.md` es histórico y solo sirve para trazabilidad.
- Luego leer, según la tarea:
  - `docs/claude-educacion/PROGRESO.md`
  - `docs/claude-educacion/CHECKLIST.md`
  - `docs/claude-educacion/ESQUEMA_CONTENIDO.md`
  - `docs/claude-educacion/MAPA_CURRICULAR.md`
  - auditorías dentro de `docs/claude-educacion/auditoria/`

No evaluar contenido que aún no se ha enseñado. Cada unidad debe introducir vocabulario, patrón/gramática y ejemplos antes de práctica guiada, independiente, situación y evaluación.

## Home e interfaz que se conservan

No sustituir ni eliminar sin instrucción explícita:

- logo oficial;
- seis iconos propios del home;
- imagen `home-aprende-hoy.webp`;
- mascota y animaciones sutiles;
- racha y feedback de acierto/error;
- banner de tutores/avatar;
- `web/avatar/` y retratos existentes.

Evitar volver a iconos genéricos o a layouts anteriores.

## Android/APK

- Versión actual documentada: `0.1.0+1`.
- APK debug reciente: ~120 MB, 2026-09-26.
- APK release existente: ~62 MB, 2026-09-08 y posiblemente desactualizada.
- La release Android usa todavía firma debug.
- El avatar 3D no funciona aún en Android nativo.
- Antes de publicar: firma propia, incremento de versión, compilación release y prueba en dispositivo.
- APK publicados que deben conservarse:
  - `https://onelingo.hostingcuenca.com/apk/onelingo-prueba.apk`
  - `https://onelingo.hostingcuenca.com/apk/onelingo-abierto.apk`
- Una app Flutter instalada no recibe automáticamente cambios web. Elegir posteriormente publicación normal o contenedor web/PWA controlado.

## Servidor y producción

- Servidor: `167.235.20.41`, Hetzner/Ubuntu 22.04.
- SSH: `ssh -F /dev/null root@167.235.20.41`.
- Web: `/var/www/onelingo/web`.
- Backend: `/var/www/onelingo/backend`.
- Proceso: PM2 `onelingo-api`.
- Lock obligatorio: `/tmp/onelingo-deploy.lock`.
- Es un servidor compartido; no reiniciar servicios ajenos.
- Conservar siempre `web/apk/`, `web/avatar/`, `.env`, caché de audio y configuración existente.
- Seguir `docs/DEPLOYMENT_RUNBOOK.md` y registrar releases en `docs/claude-educacion/DESPLIEGUES.md`.

Release verificada el 2026-09-30:

- ID: `20260930-edu-5-n2-n3-review`.
- `main.dart.js`: `72e25f36798f5810b1fac9c68ec95d788729ddd9dd8d3378f7965f414b7808a6`.
- Biblioteca: versión `2026.09.30-en-n3.1`, 290 unidades y 3.770 familias.
- Activación: 290 unidades `active`.
- N2: 100 unidades; N3: 90 unidades; C91 ausente.
- API sana; PM2 `onelingo-api` online y no reiniciado.
- Hash de `.env` preservado; APK y avatar responden 200.
- Backup: `/var/www/onelingo/backups/20260930-edu-5-n2-n3-review/web-anterior`.

Rollback de esta release:

```bash
ssh -F /dev/null root@167.235.20.41 \
  'set -e; cd /var/www/onelingo; mv web staging/20260930-edu-5-n2-n3-review/web-retirada-post-release && cp -al backups/20260930-edu-5-n2-n3-review/web-anterior web'
```

Secuencia obligatoria de despliegue: preflight HTTPS/SSH → confirmar lock libre → crear lock → backup verificable → subir a staging → conservar APK/avatar → validar hashes/conteos → renombres atómicos → verificar HTTP, recorrido visual, PM2 y `.env` → documentar → liberar lock. Si cambia solo web, no reiniciar backend.

## Comandos de comprobación

```bash
cd /home/roggrt/Documents/onelingo
python3 tools/validar_ruta.py
python3 -m unittest discover -s test_tools
~/flutter/bin/flutter analyze --no-pub lib
~/flutter/bin/flutter test --no-pub
cd backend && npx tsx --test test/*.test.ts
```

No ejecutes todas las pruebas para una simple lectura. Usa las pertinentes y ejecuta el conjunto completo antes de una release transversal.

## Prioridades vigentes

1. Recoger la revisión del cliente de la release N1+N2+N3 C1–C90 sin confundirla con aprobación editorial definitiva.
2. Producir y aprobar N3 C91–C95 y C96–C100 con agentes independientes y las puertas G0–G7.
3. Ejecutar auditoría longitudinal N3 C1–C100 y ampliar conscientemente el runtime de 290 a 300 clases.
4. Crear, auditar y congelar el mapa editorial v2 de N4 antes de autorizar su contenido; repetir por nivel hasta N10.
5. Separar evaluación de práctica y conectar vocabulario/situaciones/progreso.
6. Integrar metadatos de unidad y errores del usuario en el tutor IA.
7. Crear un piloto 2D Rive, medir latencias de voz y definir la estrategia Android como líneas separadas del currículo.

Checklist detallado: `docs/ACTIVE_CHECKLIST.md`.
Cadena de producción inglesa: `docs/claude-educacion/ENGLISH_EDITORIAL_PIPELINE.md`.

## Restricciones de seguridad y continuidad

- No copiar `~/.codex` entre cuentas.
- No copiar tokens, cookies, `.env`, claves SSH o credenciales.
- No mostrar secretos en terminal, logs o respuestas.
- No desplegar desde un árbol con cambios ajenos sin aislarlos.
- No afirmar que un conector o rig funciona sin comprobarlo.
- No borrar ni regenerar activos costosos si ya existen.
- Antes de producción: backup, lock, staging, validación y rollback documentado.

## Respuesta esperada al terminar de leer

La nueva instancia debe responder con un máximo de 12 puntos:

1. rama y commit;
2. estado del árbol;
3. producción confirmada o no;
4. release pendiente;
5. estado educativo;
6. estado de voz;
7. estado de avatares;
8. estado Android/APK;
9. Higgsfield conectado o acción requerida;
10. tres riesgos principales;
11. diferencias frente a este documento;
12. siguiente acción recomendada.

Si la instancia fue iniciada con el prompt exacto de este documento, después de informar estos puntos debe comenzar por N3 C91–C95 con el protocolo de agentes. Si solo recibió una petición de lectura o diagnóstico, debe esperar la instrucción del usuario antes de modificar el producto.
