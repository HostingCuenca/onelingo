# Biblioteca editorial de ejercicios v1

## Objetivo

Separar el contenido que enseña de los bancos que practican, evalúan y comprueban retención. La ruta base no genera ejercicios mediante IA.

## Contrato propuesto

```json
{
  "schema": "exercise-library/1",
  "libraryId": "onelingo",
  "version": "2026.09.0",
  "course": "en",
  "units": {
    "en.a1.example": {
      "concepts": ["example-concept"],
      "skills": ["vocabulario", "escucha"],
      "prerequisites": [],
      "pools": {
        "teaching": ["ex.onelingo.en.example.one:v1:model"],
        "practiceGuided": ["ex.onelingo.en.example.two:v1:guided"],
        "practice": ["ex.onelingo.en.example.three:v1:practice"],
        "evaluation": ["ex.onelingo.en.example.four:v1:assessment"],
        "review": ["ex.onelingo.en.example.five:v1:review"]
      }
    }
  },
  "families": [
    {
      "id": "ex.onelingo.en.example.five",
      "revision": 1,
      "concepts": ["example-concept"],
      "skills": ["vocabulario"],
      "variants": [
        {
          "id": "ex.onelingo.en.example.five:v1:review",
          "format": "elegir",
          "prompt": {"es": "…"},
          "answer": {"index": 1},
          "choices": [{"text": "…"}, {"text": "…"}],
          "teaches": [],
          "requires": ["v-example"],
          "origin": {"kind": "editorial"},
          "contentHash": "sha256:…"
        }
      ]
    }
  ]
}
```

## IDs y versiones

- Familia: `ex.<biblioteca>.<idioma>.<concepto>.<slug>`.
- Variante: `<familia>:v<revision>:<slug>`.
- Un cambio en estímulo, respuesta o lógica de corrección crea una revisión nueva.
- Nunca se recicla un ID publicado.
- Cada intento registra `variantId`, `libraryVersion` y `selectionId` además de las claves históricas.

## Reglas anti-filtración

1. Pools: `teaching`, `practiceGuided`, `practice`, `evaluation`, `review`.
2. Una familia reservada a evaluación o repaso no aparece antes en otro pool.
3. Guiada puede tener pista; práctica independiente no.
4. Evaluación y repaso nunca exponen respuesta, pista o función de distractor.
5. Evaluación exige al menos cuatro variantes y dos formatos por clase de transferencia.
6. `teaches` declara qué introduce el ejercicio; `requires` solo usa prerrequisitos ya enseñados.
7. El validador detecta duplicados exactos y casi duplicados entre pools incompatibles.
8. Cambiar únicamente el orden de opciones no crea una variante pedagógica nueva.

## Selección determinista

1. Filtrar por idioma, unidad, pool, conceptos, habilidades, dificultad y prerrequisitos.
2. Excluir familias expuestas recientemente o reservadas para otra función.
3. Aplicar cuotas por habilidad y formato.
4. Ordenar con hash estable de versión, curso, unidad, pool, semilla, familia y variante.
5. Congelar la selección del intento con `selectionId`.

No se usa `Random()` dependiente del orden del JSON ni generación de IA.

## Corrección multiparte determinista

Para evaluar varias decisiones dentro de una misma actividad sin revelar las
respuestas por emparejamiento léxico, `completar` puede declarar este contrato:

```json
{
  "format": "completar",
  "origin": {
    "text": "Fuente global opcional.",
    "sentences": ["Primera decisión: ___", "Segunda decisión: ___"],
    "scoring": {"parts": 2, "minimumCorrect": 1, "requiredParts": [1]}
  },
  "answer": {
    "text": "respuesta uno | respuesta dos",
    "accepted": ["respuesta uno | respuesta dos"],
    "parts": [
      {"text": "respuesta uno", "accepted": ["respuesta uno"]},
      {"text": "respuesta dos", "accepted": ["respuesta dos"]}
    ]
  }
}
```

- `origin.sentences`, `answer.parts` y `origin.scoring.parts` tienen la misma longitud.
- Cada estímulo contiene al menos un `___`; cada parte se escribe y corrige por separado.
- `minimumCorrect` define el umbral real que consume la UI; sin este contrato, `completar` admite un solo blanco visible.
- `requiredParts` puede marcar índices base cero que deben acertarse además del umbral (por ejemplo, estado actual y fecha de cierre).
- `origin.text` permite mostrar una fuente común para tareas de extracción o secuencia.
- La corrección es local y determinista; no interviene ningún tutor ni servicio de IA.

`requiredParts` nunca puede contener más índices que `minimumCorrect`: de lo
contrario un umbral anunciado como 4/5 se convertiría de hecho en 5/5. Cuando
una respuesta canónica multiparte usa `|` para documentación, `accepted` debe
incluir además una formulación natural sin ese separador.

## Escritura extensa por rúbrica determinista

Una actividad `escribir` puede aceptar paráfrasis controladas sin IA mediante
un rango de palabras y grupos de evidencia:

```json
{
  "origin": {
    "scoring": {
      "wordRange": [80, 100],
      "evidenceGroups": [
        ["my goal is", "my aim is"],
        ["two weeks", "fourteen days"],
        ["dated answer sheets", "dated records"]
      ]
    }
  }
}
```

La respuesta aprueba solo si respeta `wordRange` y contiene al menos una frase
normalizada de cada grupo. Cada grupo representa un criterio curricular
obligatorio; las alternativas son equivalencias editoriales explícitas, no una
evaluación semántica abierta. Si no existen `evidenceGroups`, se conserva la
comparación exacta normalizada con `answer.accepted`.

## Migración desde esquema 2

| Paso actual | Pool inicial |
|---|---|
| explicación, ejemplos, vocabulario, patrón, tabla | `teaching` |
| práctica guiada | `practiceGuided` |
| práctica independiente | `practice` |
| situación | `practice`/`application` |
| evaluación | `evaluation` |
| nuevo contenido editorial de retención | `review` |

Los ítems importados reciben IDs `legacy.<curso>.<unidad>.<paso>.<item>` y conservan su origen. El adaptador mantiene los pasos embebidos como fallback mientras cada unidad se migra.

## Cambios de implementación previstos

- `modelos.dart`: modelos y parser retrocompatible.
- `selector.dart`: selección determinista, filtros, cuotas y snapshot.
- `integridad.dart`: validación global y anti-filtración.
- `providers.dart`: evidencia por variante y versión sin romper claves existentes.
- `migracion.dart`: aliases idempotentes de legado a IDs globales.
- `unidad_screen.dart`: consumir pools; repaso usa solo `review`.
- Pruebas: fallback, IDs, revisiones, anti-leak, determinismo, migración y widgets sin mezcla de pools.
## Apoyo visual opcional

Los ejercicios editoriales pueden declarar `origin.imageAsset` y `origin.imageAlt`. La imagen debe existir bajo `assets/img/`, usar PNG, WebP o JPEG y tener texto alternativo no vacío. El adaptador conserva ambos campos y la vista de ruta muestra el activo con semántica accesible.

Las imágenes son apoyo, no sustituto del contrato de respuesta: cada escena debe ser inequívoca, ligera y reutilizable. No debe contener texto incrustado, marcas de agua ni información irrelevante. C24–C25 inauguran la convención con `assets/img/educacion/en/`; sus cuatro activos fueron generados específicamente para OneLingo y convertidos a WebP 768×768.
