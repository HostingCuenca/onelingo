# QA de integración runtime — Inglés N1

Fecha: 2026-09-28  
Alcance: fuente local y build web; no producción.

## Resultado

Inglés N1 quedó conectado al recorrido real local con 100 unidades (`en.n1.class-01` a `en.n1.class-100`) y 1.300 variantes editoriales. La pantalla de unidad obtiene de la biblioteca los pools `guided`, `practice`, `evaluation` y `review`; el modo repaso consume exclusivamente `review`. No existe generación de ejercicios por IA en ejecución.

La activación fuente es `active` para las 100 unidades. Si una unidad activa no puede cargar o validar su biblioteca, muestra error explícito y no cae silenciosamente al contenido embebido. Los enlaces históricos `/ruta/a1-1` y `/ruta/a1-2` resuelven a `n1` bajo la escala `client-10-levels-v1`.

## Evidencia automatizada

- `python3 tools/contenido/generar_runtime_n1.py`: 100 unidades, 1.300 variantes, 100 activas; segunda ejecución sin cambios de hash.
- `python3 tools/validar_ruta.py`: 10 idiomas, 0 errores.
- `python3 -m unittest discover -s test_tools`: 40 pruebas correctas.
- `flutter test --no-pub`: 155 correctas, 1 omitida, 0 fallos.
- `flutter analyze --no-pub lib test`: sin errores nuevos; 12 avisos/información heredados.
- `flutter build web --release --no-pub --dart-define=API_URL=https://onelingo.hostingcuenca.com/api`: correcto.

## Integridad del build

- `build/web/main.dart.js`: `71d06ed85241a61ff340e6b2c34ec84b3543100030f76fecb42a78ea8ad1af19`
- `assets/contenido/en/exercise-library.json`: `6804db552370d12f30f293bead21800ac0c7dcb921b47024c73703a4599f3961`
- `assets/contenido/en/ruta/n1-editorial.json`: `c86c9ff8cf427889cf847610c62ea562ba27a0bf8261df12082ca8938f72f2da`

El build contiene `exercise-activation.json`, `exercise-library.json`, `curso.json` y `n1-editorial.json`. La inspección visual confirmó carga del build y onboarding con la escala de diez niveles. La entrada de N1/C1 está cubierta además por prueba de widget sobre el recorrido real.

## Límites y rollback

No se desplegó: el árbol contiene cambios previos y archivos sin seguimiento, y el runbook exige release desde un estado identificable, backup y lock. Como la migración cambia el índice inglés de 29 a 100 unidades, el rollback seguro de esta release es restaurar el build web anterior completo. Cambiar solo una unidad a `legacy` no restaura el índice anterior.

Antes de producción: registrar revisión humana, confirmar árbol/commit, crear backup remoto, adquirir lock, desplegar, validar `/api/salud`, consola, onboarding, N1/C1, repaso y progreso; documentar hashes y ruta de restauración.
