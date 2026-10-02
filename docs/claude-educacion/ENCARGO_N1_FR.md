# Encargo: N1 francés (FR-5c), 50 clases en 10 bloques

Lee antes:
- **tus 5 fichas** en `curriculo/fr/n1.json` (`PLAN_CLASES.md`): escribe exactamente lo que dicen. No introduzcas gramática que no esté en su `introduce` ni en clases anteriores; lo que ya se vio va como repaso;
- `PLAN_PRODUCCION.md` §2 (mapa de bloques y tema de cada clase);
- `PLAN_FRANCES.md` §3–§4 (pistas y anatomía de clase);
- `ESQUEMA_CONTENIDO.md` (esquema 2: unidad, pasos, ítems y reglas);
- `assets/contenido/fr/ruta/a1-1.json` como modelo de estilo. Sus 9 unidades pueden reutilizarse en B1–B3.

## Archivo por bloque

`tools/contenido/ruta-fr/n1-bXX.json` con `{"modulo": "fr.n1-bXX", "unidades": [5 unidades]}`.

- **Ids:** `fr.n1.c01` … `fr.n1.c50`.
- **Orden:** `orden` = 100 + n en el borrador; el integrador lo renumera a continuación de Fundamentos.
- **Nivel:** `cefr: "A1"`, `nivelInterno: 1`.
- **Prerrequisitos:** c01 → `fr.f0.se-presenter`; cada clase siguiente → la anterior.
- **Concepto:** un id neutral (`saludos`, `presente-er`, `numeros-0-20`…).
- **Textos de apoyo:** todos `{"es": …, "en": …}` (español neutro de América con tú; inglés americano). La versión inglesa compara con el inglés cuando ayuda.

## Cada clase (≈ 10–12 minutos)

En orden:
1. `explicacion`: corta y concreta. La primera abre con el **sonido del día**, un recordatorio de una grafía del Nivel 0 relacionada con las palabras de la clase.
2. `ejemplos`: 5–8, con audio.
3. `vocabulario`: 6–10 vocablos con artículo en los sustantivos.
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
