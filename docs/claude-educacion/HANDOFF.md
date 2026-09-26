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
- Ruta f0 IMPLEMENTADA y PROBADA en los 10 idiomas (6 unidades c/u, 60 en total). 9 idiomas marcados «Versión inicial» (sin revisión nativa).
- Nivel 0 = ruta; aprobar todas sus unidades desbloquea el Nivel 1.
- Gramática inglesa: reanuda tema, marca practicados, guarda borradores.
- A1–C1 de otros idiomas: legado + niveles 3–10 con banco genérico en inglés (sin resolver, decisión del usuario: se resuelve con contenido real).

## Cinco últimos cambios
1. `607a1df` núcleo `lib/core/aprendizaje/`, pantallas `lib/features/ruta/`, contenido f0 × 10, pruebas.
2. Tolerancia a tildes y pinyin; opciones barajadas (DEC-009).
3. `CargadorRuta` lee sin la caché de `rootBundle` (evita futuros colgados en pruebas).
4. Home: 3 destinos por idioma (DEC-008), sin tocar diseño.
5. Docs de seguimiento completos en `docs/claude-educacion/`.

## Archivos principales
```
lib/core/aprendizaje/{modelos,cargador,grafo,dominio,correccion,integridad,migracion,providers}.dart
lib/features/ruta/{ruta_screen,unidad_screen,item_view}.dart
lib/shared/widgets/tarjeta_fundamentos.dart
assets/contenido/<idioma>/ruta/{curso,f0}.json
tools/validar_ruta.py
test/ruta_{contenido,dominio,recorrido}_test.dart
```

## Comandos
```bash
python3 tools/validar_ruta.py            # contenido de los 10 idiomas
~/flutter/bin/flutter analyze lib        # 7 info previos en sync.dart
~/flutter/bin/flutter test               # 129 pasan, 1 omitida
~/flutter/bin/flutter build web --release --dart-define=API_URL=https://onelingo.hostingcuenca.com/api
./tools/dev-local.sh android emulator-5554   # AVD pruebas_general
```
En pruebas de widgets: precargar la ruta con `tester.runAsync(() => cargador.cargar(...))` y sobrescribir `cargadorRutaProvider`; silenciar `Efectos.sonido` y usar un doble de audioplayers (ver `test/ruta_recorrido_test.dart`).

## Producción
Ver DESPLIEGUES.md (release, respaldo y rollback). SSH `ssh -F /dev/null root@167.235.20.41`; web en `/var/www/onelingo/web` (conservar `web/apk/`); bloqueo `/tmp/onelingo-deploy.lock` en el servidor.

## Siguiente tarea concreta
Migrar A1 de inglés (niveles 1–2) al esquema 2 empezando por los nodos `en-g-*` de A1 de la auditoría A, enlazando las guías existentes como alias. En paralelo: revisión nativa de DEC-010.

## Riesgos activos
- Contenido de 9 idiomas sin revisión nativa (DEC-010).
- Evaluación de unidad reutiliza ítems al reintentar; no hay banco separado.
- Audio TTS de pares mínimos/tonos no verificado acústicamente.
- El audio exige sesión en el backend; los usuarios demo locales no oyen audio (comportamiento previo).
- Home: la tarjeta «50 situaciones» dice «Inglés para la vida real» en todos los idiomas (texto del home, no tocado).
- Niveles 3–10 fuera de inglés siguen mostrando el banco genérico en inglés.
- El backend reemplaza el estado completo sin fusión (riesgo previo de «última escritura gana»).

## No sobrescribir
Home nuevo (`home_screen.dart`, salvo sus destinos), logo oficial, 6 iconos del home, imagen «Aprende hoy», avatares (`web/avatar`), voz, backend y su `.env`, configuración del servidor, APK publicado.
