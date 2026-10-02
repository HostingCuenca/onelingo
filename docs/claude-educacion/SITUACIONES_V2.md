# Situaciones v2: las mismas 50, en tres tramos

Estado: **hecho (fase C, DEC-028)** · Fecha: 2026-10-01 · Acordado con el cliente.

## Idea

Las 50 situaciones (restaurante, aeropuerto, médico…) se mantienen, pero cada una tiene **tres tramos** que crecen con el alumno. El alumno reconoce la situación y ve que la maneja cada vez mejor.

| Tramo | Niveles | MCER | Qué hace el alumno (ejemplo: restaurante) |
|---|---|---|---|
| Básico | N1–N3 | A1–B1 inicial | pide una mesa, pide un plato, paga |
| Intermedio | N4–N6 | B1–B2 | reclama un error, pide recomendaciones, explica una alergia |
| Avanzado | N7–N10 | B2 alto–C1 | negocia una reserva de grupo, resuelve un conflicto con tacto, da una opinión matizada |

- El tramo del alumno sale de su nivel. Nunca se le pide elegirlo.
- Los tramos inferiores quedan abiertos para repasar; los superiores se ven bloqueados con el nivel en que se abren.
- Cada tramo tiene:
  - 3 objetivos comunicativos, cada uno con una frase modelo y su traducción;
  - 10 palabras o colocaciones con ejemplo;
  - 4 frases útiles;
  - una prueba con final y nota.
- La práctica es con el tutor IA, por chat o por videollamada, ya situada en la situación, el tramo y el objetivo.

## Fuente única

| Archivo | Qué contiene | Quién lo edita |
|---|---|---|
| `assets/contenido/situaciones/catalogo.json` | las 50: `id`, `nombre` (es), `categoria`, `icono`, `color`; independiente del idioma | a mano (raro) |
| `assets/contenido/<idioma>/situaciones.json` | contenido por idioma y tramo (esquema abajo) | autoría + revisión GO |
| `lib/core/content/catalogo_situaciones.g.dart`, `web/avatar/topics.json`, `backend/src/content/situaciones-<idioma>.json` | **generados** con `python3 tools/contenido/generar_situaciones.py`; no editar | el generador |

`test/situaciones_v2_test.dart` falla si un generado no coincide con la fuente o si el contenido rompe el esquema.

## Esquema de `assets/contenido/<idioma>/situaciones.json`

```json
{
  "version": "2026.10.01",
  "idioma": "en",
  "situaciones": [
    {
      "id": 1,
      "tramos": {
        "basico": {
          "objetivos": [
            {"id": "s1-o1", "titulo": "Pedir una mesa", "frase": "Could we have a table for two?", "traduccion": "¿Podríamos tener una mesa para dos?"}
          ],
          "vocabulario": [
            {"id": "s1-b-v1", "en": "menu", "es": "menú", "ejemplo": "Could I see the menu, please?"}
          ],
          "frases": [
            {"id": "s1-b-f1", "en": "Could I have the soup, please?", "es": "¿Me trae la sopa, por favor?"}
          ]
        },
        "intermedio": {"objetivos": [], "vocabulario": [], "frases": []},
        "avanzado": {"objetivos": [], "vocabulario": [], "frases": []}
      }
    }
  ]
}
```

Reglas:
- **Identificadores:** `s<id>-o1..o3` (básico; se conservan los ids de siempre por el progreso y el servidor), `s<id>-i1..i3` (intermedio) y `s<id>-a1..a3` (avanzado). Vocabulario `s<id>-<b|i|a>-v<n>` y frases `s<id>-<b|i|a>-f<n>`.
- **Por tramo:** exactamente 3 objetivos, 10 entradas de vocabulario y 4 frases.
- **Sin repeticiones:** ninguna palabra (`en`, sin mayúsculas) se repite entre los tramos de una misma situación.
- **Objetivos:**
  - el título va en español, en infinitivo y corto (≤ 60 caracteres);
  - la frase es inglés natural del tramo (básico ≤ 12 palabras, intermedio ≤ 20, avanzado ≤ 30);
  - la traducción va en español neutro.
- **Vocabulario:**
  - `en` es una palabra o colocación (≤ 5 palabras) del tramo; `es` es su traducción breve;
  - `ejemplo` es una frase inglesa natural de la situación que contiene `en`.
- **Frases:** completas y reutilizables en la situación, con su traducción.
- **Inglés general americano**, como el Nivel 0: ortografía y léxico de EE. UU. (favorite, center, gas station, apartment, check, line, cell phone).
- **Español neutro de América:** tú; auto, boleto, celular, computadora, departamento.
- **La situación 50 («Conversación libre»):** básico = presentarse y hablar de gustos; intermedio = dar y defender opiniones; avanzado = debatir y matizar.

## Progreso (claves en `practicas`)

- `situacion:<idioma>:<id>:<tramo>:prueba`: `{aciertos, total, aprobada, fecha}`. Se aprueba con el 80 %.
- Turnos de práctica: `situacion-<idioma>-<id>-<objetivoId>` (ya existían).
- **Tramo completado:** prueba aprobada y al menos un objetivo practicado con el tutor.

## Producción del contenido (2026-10-01)

- **Autoría:** 5 lotes de 10 situaciones (`tools/contenido/situaciones/borrador/lote-N.json`) partiendo del básico existente (`actual.json`).
- **Revisión:** cada lote tuvo una revisión independiente con veredicto GO (`revision-N.md`). En total, unos 1.060 cambios: inglés americano, naturalidad, español neutro, vocabulario y progresión.
- **Integración:** `python3 tools/contenido/situaciones/integrar_lotes.py`. Solo integra lotes con GO y 0 errores, y después regenera las copias.
- **Para cambiar el contenido:** edita `assets/contenido/en/situaciones.json` y ejecuta `validar_situaciones.py` y `generar_situaciones.py`.

## Esquema genérico para idiomas nuevos (francés en adelante)

Inglés conserva sus claves (`en` = palabra meta, `es` = traducción). Los idiomas nuevos usan claves neutras y apoyo bilingüe:

```json
{"id": 1, "tramos": {"basico": {
  "objetivos": [{"id": "s1-o1", "titulo": {"es": "Pedir una mesa", "en": "Ask for a table"},
                 "frase": "Une table pour deux, s’il vous plaît.",
                 "traduccion": {"es": "Una mesa para dos, por favor.", "en": "A table for two, please."}}],
  "vocabulario": [{"id": "s1-b-v1", "meta": "la carte", "traduccion": {"es": "la carta, el menú", "en": "the menu"},
                   "ejemplo": "Je peux voir la carte ?"}],
  "frases": [{"id": "s1-b-f1", "meta": "L’addition, s’il vous plaît.", "traduccion": {"es": "La cuenta, por favor.", "en": "The check, please."}}]
}}}
```

- **`meta`:** el texto en el idioma que se aprende (con artículo en los sustantivos).
- **`traduccion` y `titulo`:** `{es, en}`, resueltos con `localizarApoyo`.
- **Ids:** los mismos de siempre (`s<id>-o1`… básico, `s<id>-i*` intermedio, `s<id>-a*` avanzado).
