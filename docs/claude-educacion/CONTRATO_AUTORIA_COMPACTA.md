# Contrato de autoría compacta — Inglés N3 C91 → N10 C100

Actualizado: 2026-09-30. Sustituye a los generadores Python por bloque. Objetivo: **cero retrabajo** — cada clase nace con enseñanza, práctica, evaluación, situación y pistas, y la herramienta rechaza lo que no cumple antes de la revisión.

## Flujo

1. El autor escribe `assets/contenido/en/editorial/<nivel>/autor/bloque-<ini>-<fin>.json` (5 clases; números con dos cifras: `bloque-91-95.json`, `bloque-01-05.json`).
2. Ejecuta `python3 tools/contenido/construir_bloque.py <archivo> --solo-validar` y corrige hasta `OK`. Después, sin `--solo-validar`, genera `class-NN.json`, `bundle-…json` y `enriquecimiento-…json`.
3. Un revisor distinto revisa el bloque y añade `"review": {"status": "GO", …}` al archivo de autor y vuelve a ejecutar el constructor (propaga el GO al enriquecimiento).
4. El coordinador amplía `LEVELS` en `tools/contenido/generar_runtime_n1.py` y compila.

La fuente curricular es `assets/contenido/en/plan-editorial/mapa-n<N>-editorial-v2.json`: cada clase toma de allí `concepts`, `phase`, `title`, `languageFocus`, `canDo` y `assessment.taskEs`.

## Formato

```json
{
  "schema": "onelingo.editorial.compact-block.v1",
  "level": "n3",
  "range": {"start": 91, "end": 95},
  "classes": [
    {
      "n": 91,
      "objetivo": "Leer un encargo de proyecto y localizar objetivo, plazo y responsables.",
      "habilidades": ["gramática", "lectura", "escucha", "escritura"],
      "vocabulario": [{"en": "brief", "es": "encargo"}, … 6–12 entradas],
      "ensenanza": [{"en": "The brief says the garden must be ready by May.", "es": "El encargo dice que el jardín debe estar listo para mayo.", "nota": "Must + verbo base marca un requisito."}, … 4–6],
      "explicacion": {"titulo": "…", "texto": "Regla en español, 250–550 caracteres."},
      "patron": {"texto": "…:", "formula": [{"texto": "The brief", "nota": "…"}, … 2–5]},
      "tabla": {"columnas": ["…", "…"], "filas": [[{"texto": "…"}, {"texto": "…"}]]},
      "erroresFrecuentes": [{"incorrecto": "…", "correcto": "…", "explicacion": "…"}, {…}],
      "situacion": {"contexto": "…", "dialogo": [{"hablante": "Ana", "texto": "…", "traduccion": "…"}, … 3–6],
                     "item": {"formato": "elegir", "consigna": "Según el diálogo, …", "opciones": [{"es": "…"}, {"es": "…"}, {"es": "…"}], "respuesta": 0, "feedback": "…"}},
      "ejercicios": {
        "guiada":     [3 ítems, cada uno con "pista"],
        "practica":   [3 ítems],
        "evaluacion": [4 ítems, ≥2 formatos],
        "repaso":     [3 ítems]
      }
    }
  ]
}
```

`tabla` es opcional. `titulo` es opcional (por defecto, el del mapa).

### Ítems

Campos comunes: `formato`, `consigna` (español, ≤ 90 caracteres, **única** en el bloque, concreta: nada de «Elige la opción correcta»), `feedback` (español, explica por qué, **único** en el bloque, nunca menciona la posición «la primera opción»), `pista` (solo guiada).

| formato | campos |
|---|---|
| `elegir` | `opciones` (3–4, inglés), `respuesta` (índice). Opcional `texto` (lectura breve que se muestra). |
| `escuchar` | `audio` (inglés, lo lee la voz), `opciones`, `respuesta`. La respuesta **no** debe poder deducirse sin escuchar. |
| `completar` | `texto` (frase inglesa con **un** `___`), `respuesta`, `aceptadas` (todas las correctas). La `consigna` incluye la traducción completa: `Completa: «Vivo en Lima.»`. Multiparte: `frases` (≥2 con `___`), `partes` [{`respuesta`, `aceptadas`}], `minimo`, `texto` opcional. |
| `ordenar` | `respuesta` (frase; las fichas salen de sus palabras). 4–12 palabras. |
| `escribir` | `texto` (estímulo o datos, puede ser español), `respuesta` (modelo), `aceptadas` (≥1 variante distinta). Para respuestas > 12 palabras, **obligatoria** `rubrica`: `{"palabras": [min, max], "evidencias": [[frases válidas], [..], [..]]}` (≥3 grupos; cada grupo aparece en el modelo). Sin rúbrica, un texto largo no puntúa. |
| `relacionar` | `pares` [[inglés, español]] 3–5, sin pares de relleno. |

## Reglas que la herramienta comprueba

- Palabras: toda palabra inglesa de ejercicios, patrón, errores (forma correcta) y diálogo debe estar enseñada o practicada en clases anteriores, o aparecer en el `vocabulario` o la `ensenanza` de la propia clase. Se aceptan flexiones regulares y nombres propios con mayúscula. **No inventar faltas de ortografía** como distractor («studys»): usar errores gramaticales con palabras reales.
- Cada frase de `ensenanza` contiene al menos una palabra del `vocabulario` de una sola palabra, y es una frase inglesa real (no instrucciones ni metalenguaje), con traducción fiel y nota en español.
- Cada entrada de `vocabulario` aparece en la enseñanza o en algún ejercicio.
- ≥ 4 formatos por clase; evaluación con ≥ 2 formatos. Si `habilidades` incluye `escucha`, hay un `escuchar` en evaluación o repaso; si incluye `escritura`, hay un `escribir`.
- Fases `production` y `transfer`: un `escribir` en evaluación o repaso con modelo de ≥ 8 palabras y ≥ 2 respuestas aceptadas distintas.
- Sin reutilizar respuestas ni estímulos entre práctica (guiada + práctica) y evaluación/repaso.
- Clase de cierre (múltiplo de 5): la evaluación mezcla lo del bloque (la herramienta asigna los conceptos).
- Enriquecimiento: mismas reglas que `CONTRATO_ENRIQUECIMIENTO.md` (explicación ≥ 80 caracteres, 2 errores, diálogo 3–6 líneas con 2 personajes, ítem de 3 opciones que se responde leyendo el diálogo).

## Trucos (del piloto N3 C91–95)

- Un `texto` en español (datos para escribir) lleva `"textoIdioma": "es"`; si no, se revisa como inglés.
- Cada frase de `ensenanza` debe contener una entrada del vocabulario **exactamente** (el plural «volunteers» no cuenta para «volunteer»): incluye la forma que usas.
- No repitas en `relacionar` una respuesta ya usada en otro ítem de la misma sección.
- Un `escuchar` no debe tener como respuesta la misma frase del audio copiada literal: pregunta por el sentido (quién, cuándo, por qué).

- (Revisión del piloto) Las opciones de `escuchar` son **paráfrasis** del audio, no copias literales.
- Ningún `texto` o `audio` de un ítem revela la respuesta de otro ítem de la clase.
- Rúbricas de escritura flexibles: cada grupo de evidencias con variantes (cifras en número y letra, fechas en varios formatos, sinónimos) y respuestas aceptadas con esas variantes.
- Tratamiento de «tú» en español neutro (no «vosotros»); fechas como «para el 14 de junio» cuando es «by».

## Reglas de calidad para el autor (el revisor las verifica)

- Una sola respuesta defendible por ítem; distractores plausibles y claramente incorrectos.
- La respuesta no aparece en la consigna, la pista ni el audio de otra pregunta.
- Los datos necesarios están en el ítem (`texto`, `audio`) o en la enseñanza de la clase: nada de «según el registro F18» sin mostrarlo.
- Temas cotidianos y variados; personajes del curso (Ana, Leo, Mia, Tom, Carlos, Sara, Rex…).
- Dificultad según el MCER del nivel; progresión entrada → consolidación → salida.

## Pase de dificultad C1 (N8–N10) — `"pase": "c1"`

Actualizado: 2026-09-30. Motivo: las métricas de N8–N10 eran iguales a las de N4–N7 (estímulos de ~15 palabras, ~8 entradas de vocabulario casi todas ya conocidas; la correcta era la única opción más larga en el 42–51 % de los ítems). Con `"pase": "c1"` en el archivo de autor, el constructor exige por clase:

| Meta | N8 | N9 | N10 |
|---|---|---|---|
| Entradas de vocabulario (máx. 12) | ≥ 10 | ≥ 11 | 12 |
| Entradas nuevas en el curso (palabra desconocida o colocación nunca enseñada como entrada) | ≥ 4 | ≥ 5 | ≥ 6 |
| Media de palabras por frase de enseñanza | ≥ 12 | ≥ 13 | ≥ 14 |
| Al menos un `texto`/`audio` inglés de … palabras | 60 | 75 | 90 |
| Textos/audios en evaluación + repaso (2 como mínimo) de … palabras | 30 | 40 | 50 |
| Media de palabras de los estímulos (ítems con `texto`/`audio`) | ≥ 16 | ≥ 20 | ≥ 24 |
| Escritura larga (clases con `wordRange` en el mapa): modelo ≥ 70 % del mínimo | ✓ | ✓ | ✓ |

Y por bloque: la correcta es la única opción más larga en ≤ 40 % de los ítems de elegir/escuchar.

Criterios de calidad C1 (los comprueba el revisor):

- **Léxico C1**: colocaciones (reach a verdict, draw a distinction), verbos frasales en su registro, matices de cautela y actitud, vocabulario académico/profesional del tema. No palabras raras gratuitas.
- **Textos con propósito**: correos, informes, fragmentos de pódcast o reunión narrados, artículos de opinión; sin etiquetas de hablante en `audio` (la voz TTS las leería): monólogo o diálogo contado.
- **Preguntas de comprensión profunda**: al menos 2 ítems de evaluación + repaso preguntan por implicación, actitud, propósito, postura o inferencia, no por un dato literal.
- **Distractores cercanos**: misma longitud y registro; parcialmente ciertos, ciertos pero no dichos, generalizaciones excesivas o postura invertida. La correcta suele ser una paráfrasis. Nada absurdo.
- **Completar con contexto**: huecos que prueban colocación, registro o precisión, dentro de 1–3 frases de contexto; `aceptadas` con todas las respuestas defendibles.
- **Continuidad**: no se eliminan entradas de `vocabulario` existentes (otras clases pueden depender de ellas); se pueden añadir y se pueden reescribir los ejercicios.
