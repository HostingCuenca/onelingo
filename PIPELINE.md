# OneLingo · Pipeline de contenido

Convierte el plan curricular en las **2 000 unidades** (10 idiomas × 10 niveles × 20 unidades)
que alimentan las 10 000 lecciones de la app. Cada unidad genera sus 5 lecciones, el
diálogo de situación y el banco de preguntas del examen final.

```
content/plan-curricular.json   ← 200 temas (nivel × unidad) + gramática y MCER por nivel
        │  tools/contenido (Claude, salida estructurada validada con Zod)
        ▼
content/<idioma>/nivel-N/unidad-NN.json   ← 1 fichero por unidad (revisable, versionado)
        │  npm run empaquetar
        ▼
assets/contenido/<idioma>/nivel-N.json    ← lo que carga la app (lib/core/content/contenido_json.dart)
```

## Qué contiene cada unidad
`titulo`, `objetivo` (can-do MCER), `gramatica` (explicación en español), `vocab` 8-10 (palabra,
romanización, traducción, ejemplo), `frases` 6-8, `dialogo` 4-8 réplicas de situación real,
`errores_tipicos` 2-4 (interferencia del español) y `examen` 3-4 preguntas. Esquema en
`tools/contenido/src/esquema.ts`. La app deriva de ahí: flashcards, elegir, huecos, ordenar,
dictado, parejas, repetir, el rol de la lección y las preguntas del examen del nivel.

## Reglas pedagógicas (en el prompt de sistema, cacheado)
Nivel MCER estricto · español neutro para explicaciones · romanización obligatoria en zh/ja/ko/ru
(pinyin con tonos, Hepburn, RR, cirílico transliterado) · chino y japonés con espacios entre
palabras en niveles 1-3 · errores típicos de hispanohablantes · sin emojis.

## Ejecutar
```bash
cd tools/contenido && npm install
# Proveedor: Gemini (clave en tools/contenido/.env → GEMINI_API_KEY) o Claude (ANTHROPIC_API_KEY)
set -a; . ./.env; set +a                 # carga GEMINI_API_KEY
npm run generar -- --idioma en --nivel 1 --proveedor gemini --concurrencia 2

npm run plan                             # revisar los 200 temas
npm run generar -- --todo --dry-run      # 2 000 unidades · coste estimado
npm run generar -- --idioma en --nivel 1 # prueba: 20 unidades en directo (~$1)
npm run generar -- --todo --batch        # todo por Batches (50 % de coste, < 24 h)
npm run generar -- --recoger msgbatch_…  # descargar resultados cuando termine
npm run validar                          # esquema, romanización, duplicados, cobertura
npm run empaquetar                       # assets/contenido/<idioma>/nivel-N.json
cd ../.. && flutter build web --release  # la app ya lee el contenido nuevo
```
Es **reanudable**: las unidades ya existentes se saltan (`--forzar` para regenerar). Los fallos
quedan en `content/.estado/errores.log`.

## Coste y tiempo (estimación con `claude-opus-5`, ~1 900 tokens de entrada y ~1 700 de salida por unidad)
| Alcance | Unidades | Directo | Batch (50 %) |
|---|---|---|---|
| 1 idioma · Nivel 1 | 20 | ≈ $1 | ≈ $0,5 |
| 1 idioma · 10 niveles | 200 | ≈ $10 | ≈ $5 |
| 10 idiomas · 10 niveles | 2 000 | ≈ $104 | ≈ $52 |

El prompt de sistema se cachea (lectura a ~10 % del precio), por lo que el coste real de entrada
baja. Tiempo: en directo con 4 en paralelo, ~25 s/unidad → un idioma completo en ~20 min; por
Batch, todo en unas horas (máximo 24). Con `--modelo claude-sonnet-5` el coste baja a ~40 %;
la calidad lingüística en idiomas asiáticos y ruso justifica Opus para la versión final.

## Control de calidad
1. `npm run validar` (automático): esquema, romanización presente/ausente según idioma,
   vocabulario sin repetir, opciones de examen distintas.
2. Muestreo humano: 2 unidades por nivel e idioma revisadas por un hablante nativo o profesor
   (20 % del coste de generación en horas de revisión es una buena referencia).
3. Regenerar solo las unidades con incidencias (`--idioma ja --nivel 4 --unidad 7 --forzar`).
4. El examen final del nivel se compone muestreando `examen[]` de sus 20 unidades.

## Orden recomendado
1. Inglés completo (validar el pipeline con el idioma de referencia).
2. Español, francés, italiano, portugués, alemán.
3. Chino, japonés, coreano, ruso (revisar romanización con especial cuidado).
4. Segunda pasada con `--forzar` para las unidades marcadas en la revisión humana.

## Semilla actual
Mientras no haya clave, `assets/contenido/*/nivel-1.json` se exporta desde los bancos escritos a
mano en la app (`flutter test test/exportar_semilla_test.dart` con `EXPORTAR=1`), para que el
cargador JSON quede probado de punta a punta con el mismo formato que producirá el pipeline.

## Contenido escrito a mano (semillas)

Además del generador con IA, el contenido puede escribirse a mano en un formato
compacto de texto (una línea por elemento) y convertirse al mismo JSON:

```
tools/contenido/semilla/<idioma>-nivel-<N>.txt   →  npm run importar  →  content/<idioma>/nivel-N/unidad-NN.json
                                                    npm run empaquetar →  assets/contenido/<idioma>/nivel-N.json
```

Formato (campos separados por ` | `; la romanización solo en zh/ja/ko/ru):

```
# 3 | Título | Objetivo | Gramática                       ← cabecera de la unidad 3
V palabra | [romanización |] traducción | ejemplo         ← vocabulario (8-10)
F texto | [romanización |] traducción                     ← frases (6-8)
D quién | texto | [romanización |] traducción             ← diálogo (4-8)
E incorrecto | correcto | explicación                     ← errores típicos (2-4)
X pregunta | op1 ; op2 ; op3 ; op4 | índice | explicación ← examen (3-4)
```

Estado (7 sep 2026): **Nivel 1 completo (20 unidades) en los 10 idiomas**, escrito a
mano y validado con el esquema (`semilla/*-nivel-1.txt`, 200 unidades). Los niveles
2-10 siguen usando los bancos genéricos de la app hasta que se escriban sus semillas o
se generen con Gemini (`npm run generar -- --proveedor gemini`), que produce exactamente
el mismo JSON y convive con las semillas sin cambios en la app.

Reglas de estilo de las semillas: temas según `content/plan-curricular.json`; frases
de 3-8 palabras en Nivel 1; en chino y japonés las palabras van separadas por espacios
(la app las usa para ordenar); explicaciones en español pensadas para hispanohablantes;
sin emojis.


## Diagnóstico adaptativo (semillas)

Banco de preguntas por idioma en `semilla/<idioma>-diagnostico.txt`, una por línea:

```
Q nivel | skill | tipo | tema | instrucción | texto | opciones (a ; b ; c ; d) o - | correcta (índice) o respuestas aceptadas (x ; y) o - | explicación
```

- `skill`: comprension, vocabulario, gramatica, tiempos, expresiones, contexto, cotidiano, escritura.
- `tipo`: eleccion, natural, significado, contexto, situacion, error, completar, corta, escucha, dictado, escritura.
- En `escucha` y `dictado` el texto se reproduce con la voz del servidor y no se muestra hasta responder;
  en `dictado` con correcta `-` se acepta el propio texto (tolerancia del 80 %).
- `escritura`: consigna de producción libre que evalúa la IA (`POST /diagnostico/escritura`); la explicación es la rúbrica.
- `tema` alimenta el plan de refuerzo: usa nombres de temas que aparezcan en los títulos de las unidades.

Recomendación: 6-9 preguntas por nivel (0-10) alternando competencias y tipos, más una de escritura cada dos niveles.
Estado (8 sep 2026): inglés completo (87 preguntas). Los demás idiomas usan el banco de respaldo (opción múltiple de las lecciones) hasta que se siembren.
