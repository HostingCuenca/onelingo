# HANDOFF — educación multilingüe

Leer esto primero. Después PROGRESO.md y la sección relevante de CHECKLIST.md.

## Objetivo actual
Estructura educativa multilingüe: cada idioma con su propio mapa y una ruta de Fundamentos (nivel 0) real, que enseña antes de evaluar. Inglés es la referencia. Después: migrar A1 (niveles 1–2) al mismo esquema, idioma por idioma.

## Arquitectura adoptada
- **Datos por idioma** en `assets/contenido/<idioma>/ruta/curso.json` + `f0.json` (esquema 2, contrato en ESQUEMA_CONTENIDO.md). La lógica no conoce ningún idioma.
- **Jerarquía**: idioma → nivel → módulo → unidad → pasos (explicación, ejemplos, vocabulario, patrón → práctica guiada → práctica independiente → situación → evaluación).
- **Textos de apoyo** `{es, en}` resueltos con nativo → predeterminado del curso → es (DEC-004). Curso `es` explicado en inglés.
- **Progreso** en `ProgressState.practicas` con claves `ruta:<unidad>:<paso>:<item>`, `:visto`, `:evaluacion`, `:repaso`, y `ruta:<idioma>.f0:completa`. Estados calculados, nunca guardados (DEC-006).
- **Escala** 0–10 intacta; C2 `planificado` sin nivel interno (DEC-002).
- El contenido antiguo (`nivel-N.json`, guías, biblioteca) convive como banco (DEC-005).

## Estado
- Ruta f0 IMPLEMENTADA y en PRODUCCIÓN en los 10 idiomas (6 unidades c/u). 9 idiomas «Versión inicial» (sin revisión nativa).
- **A1 de inglés en PRODUCCIÓN**: 29 unidades (niveles `a1-1`, `a1-2`, 3 módulos) según PLAN_A1_INGLES.md; `/ruta/:nivel`.
- Nivel 0 = ruta; unidades de niveles inferiores al diagnóstico son «omitibles» (DEC-011).
- Voz: idioma forzado en ElevenLabs y caché por idioma (DEC-012). Sonidos y botones con estilo de la app (DEC-013).
- **Escrituras completas** en f0 (kana, hangul, pinyin, cirílico, alfabetos) y **A1 «Primeras frases»** en los 10 idiomas (204 unidades). Paso `tabla`.
- Fallo en práctica → se continúa y se repite al final del bloque. Celebración al completar.
- A2–C1 inglés y a1-2+ del resto: legado; niveles 3–10 fuera de inglés con banco genérico en inglés.

## Cinco últimos cambios
1. `bf11441`/`58d2b73` escrituras completas + A1 ×10 idiomas, precarga de fuentes; `33fef8f` celebración, repetición de fallos, `tabla`.
1. `f0a6451` pronunciación por idioma (backend `voz.ts`), sonidos Kenney revisados, `OpcionRespuesta` con pedestal y `BotonPrincipal` en la ruta.
2. `913a4e3` A1 de inglés (29 unidades), rutas por nivel, omitibles, validador estricto de distractores.
3. `607a1df` núcleo `lib/core/aprendizaje/` + rutas f0 × 10 idiomas.
4. Releases `20260926-edu-1-fundamentos` y `20260926-edu-2-a1-voz` en producción.
5. Docs de seguimiento, `tools/generar_mapa_curricular.py`.

## Archivos principales
```
lib/core/aprendizaje/{modelos,cargador,grafo,dominio,correccion,integridad,migracion,providers}.dart
lib/features/ruta/{ruta_screen,unidad_screen,item_view}.dart
lib/shared/widgets/tarjeta_fundamentos.dart
assets/contenido/<idioma>/ruta/{curso,f0}.json  (+ en: a1-1, a1-2-presente, a1-2-comunicar)
lib/features/ruta/opcion_respuesta.dart · backend/src/lib/voz.ts
tools/validar_ruta.py
test/ruta_{contenido,dominio,recorrido}_test.dart
```

## Comandos
```bash
python3 tools/validar_ruta.py            # contenido de los 10 idiomas
~/flutter/bin/flutter analyze lib        # 7 info previos en sync.dart
~/flutter/bin/flutter test               # 133 pasan, 1 omitida
cd backend && npx tsx --test test/*.test.ts   # 11 pasan
python3 tools/generar_mapa_curricular.py
~/flutter/bin/flutter build web --release --dart-define=API_URL=https://onelingo.hostingcuenca.com/api
./tools/dev-local.sh android emulator-5554   # AVD pruebas_general
```
En pruebas de widgets: precargar la ruta con `tester.runAsync(() => cargador.cargar(...))` y sobrescribir `cargadorRutaProvider`; silenciar `Efectos.sonido` y usar un doble de audioplayers (ver `test/ruta_recorrido_test.dart`).

## Producción
Ver DESPLIEGUES.md (release, respaldo y rollback). SSH `ssh -F /dev/null root@167.235.20.41`; web en `/var/www/onelingo/web` (conservar `web/apk/`); bloqueo `/tmp/onelingo-deploy.lock` en el servidor.

## Siguiente tarea concreta
Desplegar `20260926-edu-3-escrituras` (build en `build/web`, `main.dart.js` 181298a3…) cuando SSH responda. Después: A2 de inglés (niveles 3–4): esqueleto contractual desde la auditoría A §A2 (como PLAN_A1_INGLES.md) y 3 agentes de contenido con un archivo cada uno. Después, A1 de otro idioma. En paralelo: revisión nativa (DEC-010) y escucha real de sonidos/voces (DEC-012, DEC-013).

## Riesgos activos
- Contenido de 9 idiomas sin revisión nativa (DEC-010).
- Sonidos elegidos por análisis de señal, no de oído; voces del sistema dependen del dispositivo.
- Gemini devuelve 403 («project denied access») en producción; el diagnóstico recurre a OpenAI.
- Evaluación de unidad reutiliza ítems al reintentar; no hay banco separado.
- Home: la tarjeta «50 situaciones» dice «Inglés para la vida real» en todos los idiomas.
- Niveles 3–10 fuera de inglés siguen mostrando el banco genérico en inglés.
- El backend reemplaza el estado completo sin fusión («última escritura gana»).

## No sobrescribir
Home nuevo (`home_screen.dart`, salvo sus destinos), logo oficial, 6 iconos del home, imagen «Aprende hoy», avatares (`web/avatar`), voz, backend y su `.env`, configuración del servidor, APK publicado.
