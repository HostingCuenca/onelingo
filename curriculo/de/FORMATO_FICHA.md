# Ficha ligera de alemán (`curriculo/de/nX.json`)

Método ligero (PLAN_ALEMAN.md §1): **sin** `personajes`, `hechosDelReparto`, `MAPA.md` ni cronología. Cada clase es una situación autónoma con nombres genéricos (Anna, Jonas, Frau Becker, Herr Wolf…) que no se arrastran a la clase siguiente. Modelo completo: `curriculo/de/n1.json`, clases c01–c10.

## Raíz del archivo

`idioma`, `nivel`, `cefr`, `examen`, `nota` (copiada del outline), `previos` (idénticos al outline) y `clases` (las 50). No hay más campos.

## Cada ficha

1. **Campos congelados**: todos los del outline `tools/curriculo/de/nX-outline.json` (`id`, `bloque`, `titulo`, `objetivo`, `gramatica`, `introduce`, `recicla`, `vocabulario`, `sonido`, `situacion` [id 1…50 del marco], `tarea`), copiados **tal cual**. Solo cambia `estado`: `esqueleto` → `planificado`.
2. **`ejercicios`**, el único campo que se escribe:
   - `guiada`: 3 ítems · `independiente`: 3 · `situacion`: `{texto, preguntas[1–2]}` · `evaluacion`: 5–8 con ≥ 3 formatos, cubriendo cada clave de `introduce`.
   - Ítem: `{formato, clave, consigna, ejemplo}`. `clave` ∈ `introduce` ∪ `recicla`. `consigna` en español, sin exponer la clave interna. `ejemplo` = «estímulo → respuesta».
   - `situacion.texto`: **solo en alemán**, ≥ 24 palabras, con diálogo (líneas «—») o datos concretos; sin palabras españolas («el», «la», «que», «pero», «con»…).
   - Formatos: `completar` (un solo `___`), `elegir`/`escuchar` (`A) … / B) …`, la respuesta es una opción; `escuchar` lleva `Audio:`), `ordenar` (`[tok / tok]`, la solución es una permutación exacta), `relacionar` (3–5 pares `a↔b;` mezclados → pares correctos, consigna ≥ 5 palabras), `escribir` (el estímulo no contiene la respuesta).
   - Sin repetir `ejemplo` en todo el nivel; sin plantillas («respuesta exacta», «Frase: ___», «Caso 1»…).
   - Alemán: sustantivos con mayúscula, Sie de cortesía con mayúscula; una sola respuesta defendible; nada de Ecuador.
3. La **c50** de cada nivel es la prueba: `introduce` vacío y evaluación de ≥ 6 ítems sobre ≥ 5 claves del nivel.

## Ejemplo (de.n1.c01, abreviado)

```json
{
 "id": "de.n1.c01", "bloque": 1, "…": "campos del outline sin tocar",
 "estado": "planificado",
 "ejercicios": {
  "guiada": [
   {"formato": "completar", "clave": "anrede-herr-frau", "consigna": "Completa el saludo formal a un señor que se apellida Wolf.", "ejemplo": "Guten Tag, ___ Wolf! → Herr"},
   {"formato": "ordenar", "clave": "anrede-herr-frau", "consigna": "Ordena el saludo a la señora Berger en la recepción.", "ejemplo": "[Berger / Tag / Frau / Guten] → Guten Tag, Frau Berger!"},
   {"formato": "elegir", "clave": "greetings", "consigna": "Elige la despedida formal al salir de una oficina.", "ejemplo": "A) Auf Wiedersehen, Herr Wolf. / B) Guten Tag, Herr Wolf. → Auf Wiedersehen, Herr Wolf."}
  ],
  "independiente": ["… 3 ítems …"],
  "situacion": {
   "texto": "Am Empfang einer Firma in Köln.\n—Guten Tag, Frau Berger!\n—Guten Tag, Herr Wolf! Wie geht es Ihnen?\n—Danke, gut. Und Ihnen?\n—Danke, gut. Auf Wiedersehen, Frau Berger!\n—Auf Wiedersehen!",
   "preguntas": [{"formato": "completar", "clave": "greetings", "consigna": "Completa la respuesta de Frau Berger a la pregunta de Herr Wolf.", "ejemplo": "Danke, ___. Und Ihnen? → gut"}]
  },
  "evaluacion": ["… 5–8 ítems, ≥ 3 formatos, cubre anrede-herr-frau …"]
 }
}
```

## Validar

```bash
python3 tools/curriculo/validar_plan_detallado.py de curriculo/de/nX.json --parcial   # mientras haya fichas en esqueleto
python3 tools/curriculo/validar_plan_detallado.py de curriculo/de/nX.json             # nivel completo (50 planificadas)
python3 tools/curriculo/validar_plan.py de
```
