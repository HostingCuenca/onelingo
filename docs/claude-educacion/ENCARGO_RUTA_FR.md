# Encargo: ruta francesa N1–N10, 50 clases por nivel en 10 bloques

Se escribió para N1 (FR-5c, publicado) y vale para todos los niveles: donde dice N1, aplica la tabla «Por nivel».

Lee antes:
- **tus 5 fichas** en `curriculo/fr/nX.json` (`PLAN_CLASES.md`), con `personajes` / `hechosDelReparto` de `n1.json` y la `nota` del nivel: escribe exactamente lo que dicen. No introduzcas gramática que no esté en su `introduce` ni en clases anteriores; lo que ya se vio va como repaso. Escribe los ejercicios de su **plan de ejercicios** (`ejercicios`) en ese formato y sobre esa clave; puedes pulir la redacción y completar `aceptadas`, pistas y feedback;
- `PLAN_FRANCES.md` §3–§4 (pistas y anatomía de clase);
- `ESQUEMA_CONTENIDO.md` (esquema 2: unidad, pasos, ítems y reglas);
- como modelo de estilo, las clases publicadas del nivel anterior (`assets/contenido/fr/ruta/`) y sus `revision-*.md`.

## Por nivel

| Nivel | cefr | nivelInterno | Duración de la clase | Sonido del día | Lectura en la situación |
|---|---|---|---|---|---|
| N1 | A1 | 1 | 10–12 min | sí, una grafía del Nivel 0 | diálogo de 3–6 líneas |
| N2 | A2 | 2 | 12–15 min | no; una nota de pronunciación cuando la clase la necesite | diálogo o texto de 6–10 líneas (≈ 80–120 palabras) |
| N3–N4 | B1 | 3–4 | 15 min | no | texto de 150–250 palabras |
| N5–N7 | B2 | 5–7 | 15–20 min | no | texto de 300–500 palabras |
| N8–N10 | C1 | 8–10 | 20 min | no | texto de 400–700 palabras |

Desde N2 las explicaciones pueden ser más densas, pero siguen siendo cortas y con ejemplos. La evaluación sigue pidiendo ≥ 4 ítems y ≥ 2 formatos; los `escribir` abiertos (`abierta: true`) no puntúan y se suman a esos 4.

## Archivo por bloque

`tools/contenido/ruta-fr/nX-bYY.json` con `{"modulo": "fr.nX-bYY", "unidades": [5 unidades]}`; la revisión va en `revision-nX-bYY.md` (N1 usó `revision-bYY.md`).

- **Ids:** `fr.nX.c01` … `fr.nX.c50`.
- **Orden:** `orden` = 100·X + n en el borrador; el integrador lo renumera.
- **Nivel:** `cefr` y `nivelInterno` del nivel (tabla «Por nivel»).
- **Prerrequisitos:** c01 → la última clase del nivel anterior (N1: `fr.f0.se-presenter`); cada clase siguiente → la anterior. El integrador los reescribe.
- **Concepto:** un id neutral (`saludos`, `presente-er`, `numeros-0-20`…).
- **Textos de apoyo:** todos `{"es": …, "en": …}` (español neutro de América con tú; inglés americano). La versión inglesa compara con el inglés cuando ayuda.

## Cada clase (≈ 10–12 minutos)

En orden:
1. `explicacion`: corta y concreta. La primera abre con el **sonido del día**, un recordatorio de una grafía del Nivel 0 relacionada con las palabras de la clase.
2. `ejemplos`: 5–8, con audio.
3. `vocabulario`: las palabras de la ficha (6–12), con artículo en los sustantivos. Si la gramática de la ficha necesita otra palabra, enséñala y dilo en el informe.
4. `patron` o `tabla`: conjugaciones con la tabla completa.
5. `practica_guiada`: 3–5 ítems con `pista`.
6. `practica_independiente`: 3–4 ítems.
7. `situacion`: contexto + diálogo de 3–6 líneas, que funciona como mini lectura, + 1–2 ítems de comprensión.
8. `evaluacion`: ≥ 4 ítems y ≥ 2 formatos.

Además:
- `erroresFrecuentes` ≥ 1, típicos de hispanohablantes o anglohablantes.
- Recicla ≥ 30 % del vocabulario de clases anteriores.
- Usa todos los formatos a lo largo del bloque: elegir, escuchar, ordenar, completar, escribir, relacionar.

## Reglas del validador (las más estrictas)

- **Nada sin enseñar.** Cada palabra francesa de respuestas, opciones, audios, diálogos y ordenar debe aparecer antes en un paso de enseñanza (`ejemplos`, `vocabulario`, `patron`, `tabla`) de esta clase o de una anterior (incluidos Fundamentos, `fr.f0.*`). Declararla en `vocabulario` de la unidad no basta: tiene que estar en un paso.
- **Francés de Francia:** U+202F antes de ? ! : ; y apóstrofo ’ (el validador lo normaliza).
- **Hablantes de los diálogos:** el nombre del personaje (`personajes` del plan) o su papel en francés («Le serveur», «La secrétaire»), nunca en español: se muestra igual con la interfaz en inglés.
- **Respuestas alternativas:** las formas válidas van en `aceptadas` (con y sin elisión, femenino y masculino cuando aplique).

## Validación

```bash
python3 tools/validar_ruta.py fr --borrador tools/contenido/ruta-fr/n1-b01.json [n1-b02.json …]
```

Valida junto con todos los bloques anteriores del borrador. Debe dar 0 errores.

## Revisión

- Un revisor distinto deja `tools/contenido/ruta-fr/revision-bXX.md` con GO o REVISE.
- Revisa la corrección del francés, la progresión, la claridad de las explicaciones en los dos idiomas y que los ítems sean válidos (una sola respuesta defendible).

## Calibración (revisión de B1, 2026-10-01)

1. `ordenar`: incluye en `aceptadas` **todos** los órdenes naturales (adverbios, «Et vous ?» al inicio o al final…).
2. Una `pista` ayuda a resolver **ese** ítem. Los pares de `relacionar` tienen glosas claramente distintas.
3. Guías de sonido exactas: cuidado con las consonantes finales (CaReFuL: la r de «bonjour» sí suena). Define ü/ö la primera vez que aparezcan.
4. Los diálogos modelan el objetivo de la clase y la cortesía francesa («Et vous ?», «Enchanté(e)»).
5. Personajes coherentes en todo el bloque (nombre, edad, ciudad): cada pregunta de comprensión con una sola respuesta. Formas femeninas para personajes femeninos.
6. **Guías de pronunciación en español** (las mismas del Nivel 0):
   - j y g suave (ge, gi) se escriben «sh» («bonjour» = «bon-shur»). Nunca «y» ni «j», que en español suenan distinto.
   - Las nasales in / ain / un se escriben «en» («vingt» = «ven», «lundi» = «len-di»); an / en, «an»; on, «on».
   - ü para la u francesa, ö para eu / e; se definen la primera vez que aparecen en un bloque.
   - En inglés: «zh» para j («bon-zhoor»); la nasal se aproxima avisando que la n no suena («vingt» = “van”, sin cerrar la boca en la n).


## Calibración (revisiones de N2, 2026-10-02)

7. **Español neutro de América e inglés americano.** Sí: departamento, celular, boleto, mesero, papas fritas, jugo, computadora, estacionar, ustedes. No: piso (vivienda), móvil, billete, camarero, patatas, zumo, ordenador, aparcar, vosotros. Inglés: apartment, cell phone, check, fries, store, subway, sneakers; los pisos franceses con su equivalente de EE. UU. (1er étage = second floor).
8. **La historia no se contradice.** Lee `personajes` y `hechosDelReparto` de los niveles anteriores y del tuyo, y la `nota` del nivel. En tu informe lista los hechos nuevos que inventes (una línea `- es / en` cada uno); el revisor los confirma en «Hechos del reparto confirmados».
9. **Una sola respuesta.** Si dos formas serían válidas (futur proche y futur simple, on y nous, con y sin elisión), la consigna fija cuál se pide o `aceptadas` incluye todas. Los `escribir` abiertos (`abierta: true`) no cuentan entre los ítems puntuables de la evaluación.
10. **Validación con borradores.** Valida tu bloque encadenado con los borradores anteriores del mismo nivel que aún no estén integrados (`--borrador nX-b01.json … nX-bYY.json`). Si uno ya está en `assets/contenido/fr/ruta/`, quítalo de la lista: daría «id duplicado».
11. **Vocabulario estricto** (`curso.json` → `vocabularioEstricto`). Solo cuenta como enseñado lo que se muestra: tarjetas del paso `vocabulario` (`refs`), ejemplos, patrones y tablas. Un vocablo declarado en `vocabulario` pero oculto no basta: si una palabra nueva aparece en la situación o en un ítem, enséñala en una tarjeta, un ejemplo o una tabla «Para leer…».
