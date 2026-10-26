# Encargo: situaciones en japonés (JA)

- **Contrato:** `docs/claude-educacion/SITUACIONES_V2.md`, sección «Esquema genérico para idiomas nuevos». Mismo formato que `tools/contenido/situaciones/pt/lote-N.json` (modelo de una situación en el paquete: `modelo-pt-s1.json`).
- **Partida:** el contenido inglés aprobado (en el paquete, `en-lote-N.json`, 10 situaciones con su nombre). Cada situación y tramo conserva **la misma intención comunicativa** (los mismos 3 objetivos con los mismos ids), adaptada al país del idioma: no se traduce palabra por palabra.
- **Ficha del idioma:** `tools/ia/idiomas/ja.md` es la autoridad en variedad, tratamiento, nombres y lugares (lista cerrada, sin datos verificables: ni líneas de metro, direcciones, precios reales ni comercios reales), ortografía, escritura por nivel y romanización.
- **Nunca se menciona Ecuador** (ni Quito, Guayaquil, Cuenca ni «ecuatoriano»), en ningún campo: la app es para EE. UU. y Latinoamérica en general. Sin historia continua ni personajes del curso.
- **Contenido por tramo:**
  - `objetivos`: 3, con `titulo` {es, en} (infinitivo, ≤ 60 caracteres), `frase` en japonés y `traduccion` {es, en};
  - `vocabulario`: 10, con `meta` en japonés (verbos en forma de diccionario; una palabra con kanji lleva además `lectura`, su lectura en kana), `traduccion` {es, en} y `ejemplo` en japonés que contenga la palabra;
  - `frases`: 4, con `meta` y `traduccion` {es, en}.
- **Niveles:** básico A1–A2 (frases ≤ 12 palabras), intermedio B1–B2 (≤ 20), avanzado B2+–C1 (≤ 30, con matices: keigo de servicio (お願いいたします, いらっしゃいませ), conectores). Sin palabras repetidas entre los tramos de una situación.
- **Situación 50 («Conversación libre»):** básico = presentarse y hablar de gustos; intermedio = dar y defender opiniones; avanzado = debatir y matizar.
- **Idiomas de apoyo:** español neutro de América (tú; celular, auto, computadora, departamento, boleto) e inglés general americano. Con un falso amigo, la `traduccion` es la correcta.
- **Validación:** `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/ja/lote-N.json` → 0 errores (también acepta un archivo con una lista de una sola situación).
- **Ambientación:** Japón, con ciudades de la lista cerrada de la ficha (とうきょう, おおさか, きょうと…). Yenes (円), でんしゃ, ICカード, コンビニ, やっきょく, びょういん, ほけんしょう. **Registro です/ます siempre**; el personal de servicio puede usar keigo fijo (いらっしゃいませ, かしこまりました).
- **Escritura por tramo:** básico en hiragana y katakana, con kanji solo en 日本, 人, 私, 先生, 学生, 円, 水, 駅, 何, 今 (lo comprueba el validador); intermedio con kanji frecuentes del JLPT N5–N4; avanzado con la escritura normal. **Toda palabra del vocabulario con kanji lleva `lectura` en kana** (la voz lee la lectura; sin kanji, no lleva `lectura`).
- **Separación de palabras (como en todo el curso):** un espacio entre palabras y las partículas aparte («えき は どこ です か？»); puntuación japonesa 。、？！ pegada a la palabra anterior y seguida de espacio; nunca puntuación ASCII ni espacio de ancho completo. Números en kana o kanji, no cifras arábigas.

## Romanización (obligatoria, la comprueba el validador)

Igual que en el curso (romanización en los ejercicios hasta N4; después, solo en el vocabulario):

| Tramo | Lleva romanización |
|---|---|
| básico | `fraseRom` en cada objetivo; `metaRom` y `ejemploRom` en cada palabra; `metaRom` en cada frase |
| intermedio y avanzado | solo `metaRom` en cada palabra del vocabulario (ningún otro campo `…Rom`) |

El sistema es el de la sección de romanización de la ficha (rōmaji Hepburn modificado: ō ū ē ā con macrón, は wa, を o, へ e como partículas, ん + vocal con apóstrofo). Un grupo de rōmaji por cada palabra separada por espacio. Mayúscula al inicio de frase y en nombres propios. El validador calcula el rōmaji exacto de todo texto en kana.

```json
{"id": "s1-b-v1", "meta": "メニュー", "metaRom": "menyū", "traduccion": {"es": "el menú", "en": "the menu"},
 "ejemplo": "メニュー を ください。", "ejemploRom": "Menyū o kudasai."}
{"id": "s1-i-v1", "meta": "予約", "lectura": "よやく", "metaRom": "yoyaku", "traduccion": {"es": "la reserva", "en": "the reservation"},
 "ejemplo": "七時 に 予約 を お願い します。"}
```
