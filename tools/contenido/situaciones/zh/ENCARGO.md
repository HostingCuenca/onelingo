# Encargo: situaciones en chino mandarín (ZH)

- **Contrato:** `docs/claude-educacion/SITUACIONES_V2.md`, sección «Esquema genérico para idiomas nuevos». Mismo formato que `tools/contenido/situaciones/pt/lote-N.json` (modelo de una situación en el paquete: `modelo-pt-s1.json`).
- **Partida:** el contenido inglés aprobado (en el paquete, `en-lote-N.json`, 10 situaciones con su nombre). Cada situación y tramo conserva **la misma intención comunicativa** (los mismos 3 objetivos con los mismos ids), adaptada al país del idioma: no se traduce palabra por palabra.
- **Ficha del idioma:** `tools/ia/idiomas/zh.md` es la autoridad en variedad, tratamiento, nombres y lugares (lista cerrada, sin datos verificables: ni líneas de metro, direcciones, precios reales ni comercios reales), ortografía, segmentación y pinyin.
- **Nunca se menciona Ecuador** (ni Quito, Guayaquil, Cuenca ni «ecuatoriano»), en ningún campo: la app es para EE. UU. y Latinoamérica en general. Sin historia continua ni personajes del curso.
- **Contenido por tramo:**
  - `objetivos`: 3, con `titulo` {es, en} (infinitivo, ≤ 60 caracteres), `frase` en chino y `traduccion` {es, en};
  - `vocabulario`: 10, con `meta` en chino, `traduccion` {es, en} y `ejemplo` en chino que contenga la palabra;
  - `frases`: 4, con `meta` y `traduccion` {es, en}.
- **Niveles:** básico A1–A2 (frases ≤ 12 palabras), intermedio B1–B2 (≤ 20), avanzado B2+–C1 (≤ 30, con matices: 能不能…, 麻烦您…, conectores 虽然…但是…, 既然). Sin palabras repetidas entre los tramos de una situación.
- **Situación 50 («Conversación libre»):** básico = presentarse y hablar de gustos; intermedio = dar y defender opiniones; avanzado = debatir y matizar.
- **Idiomas de apoyo:** español neutro de América (tú; celular, auto, computadora, departamento, boleto) e inglés general americano. Con un falso amigo, la `traduccion` es la correcta.
- **Validación:** `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/zh/lote-N.json` → 0 errores (también acepta un archivo con una lista de una sola situación).
- **Ambientación:** China continental, con ciudades de la lista cerrada de la ficha (北京, 上海, 广州…). Yuanes (块/元), 地铁, 高铁, 微信支付 o 支付宝 (como forma de pago genérica), 药店, 医院, 挂号. **您** con clientes, mayores y desconocidos en contexto formal; **你** con amigos y gente joven.
- **Chino estándar en simplificados** (nunca tradicionales). **Espacios entre palabras** con la granularidad de la ficha («我 想 要 一 杯 咖啡。»); puntuación china 。，？！、 pegada a la palabra anterior y sin espacio después; números siempre en caracteres (nunca cifras: «三十五 块»).

## Romanización (obligatoria, la comprueba el validador)

Igual que en el curso (romanización en los ejercicios hasta N4; después, solo en el vocabulario):

| Tramo | Lleva romanización |
|---|---|
| básico | `fraseRom` en cada objetivo; `metaRom` y `ejemploRom` en cada palabra; `metaRom` en cada frase |
| intermedio y avanzado | solo `metaRom` en cada palabra del vocabulario (ningún otro campo `…Rom`) |

El sistema es el de la sección de romanización de la ficha (pinyin con marcas de tono (nunca números), sandhi de 3.º + 3.º, 不 y 一 escritos según el tono real). Un grupo de pinyin por cada palabra china separada por espacio, sílabas de una palabra juntas (xuésheng), sin «v» (usa ü).

```json
{"id": "s1-b-v1", "meta": "菜单", "metaRom": "càidān", "traduccion": {"es": "el menú", "en": "the menu"},
 "ejemplo": "请 给 我 菜单。", "ejemploRom": "qíng géi wǒ càidān."}
```
