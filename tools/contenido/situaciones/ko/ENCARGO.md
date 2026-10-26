# Encargo: situaciones en coreano (KO)

- **Contrato:** `docs/claude-educacion/SITUACIONES_V2.md`, sección «Esquema genérico para idiomas nuevos». Mismo formato que `tools/contenido/situaciones/pt/lote-N.json` (modelo de una situación en el paquete: `modelo-pt-s1.json`).
- **Partida:** el contenido inglés aprobado (en el paquete, `en-lote-N.json`, 10 situaciones con su nombre). Cada situación y tramo conserva **la misma intención comunicativa** (los mismos 3 objetivos con los mismos ids), adaptada al país del idioma: no se traduce palabra por palabra.
- **Ficha del idioma:** `tools/ia/idiomas/ko.md` es la autoridad en variedad, tratamiento, nombres y lugares (lista cerrada, sin datos verificables: ni líneas de metro, direcciones, precios reales ni comercios reales), ortografía y romanización.
- **Nunca se menciona Ecuador** (ni Quito, Guayaquil, Cuenca ni «ecuatoriano»), en ningún campo: la app es para EE. UU. y Latinoamérica en general. Sin historia continua ni personajes del curso.
- **Contenido por tramo:**
  - `objetivos`: 3, con `titulo` {es, en} (infinitivo, ≤ 60 caracteres), `frase` en coreano y `traduccion` {es, en};
  - `vocabulario`: 10, con `meta` en coreano (verbos y adjetivos en forma de diccionario -다), `traduccion` {es, en} y `ejemplo` en coreano que contenga la palabra;
  - `frases`: 4, con `meta` y `traduccion` {es, en}.
- **Niveles:** básico A1–A2 (frases ≤ 12 palabras), intermedio B1–B2 (≤ 20), avanzado B2+–C1 (≤ 30, con matices: 합쇼체 de servicio, conectores, -(으)ㄹ 텐데요). Sin palabras repetidas entre los tramos de una situación.
- **Situación 50 («Conversación libre»):** básico = presentarse y hablar de gustos; intermedio = dar y defender opiniones; avanzado = debatir y matizar.
- **Idiomas de apoyo:** español neutro de América (tú; celular, auto, computadora, departamento, boleto) e inglés general americano. Con un falso amigo, la `traduccion` es la correcta.
- **Validación:** `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/ko/lote-N.json` → 0 errores (también acepta un archivo con una lista de una sola situación).
- **Ambientación:** Corea del Sur, con ciudades de la lista cerrada de la ficha (서울, 부산, 인천…). Wones (원), 지하철, 교통카드, 편의점, 약국, 병원, 건강보험. **해요체 por defecto** en todo el contenido; 합니다체 solo en fórmulas fijas de servicio (감사합니다, 어서 오세요, 안내해 드리겠습니다).
- **Coreano estándar:** hangul con espacios según la norma (partículas pegadas al sustantivo); números sino-coreanos o nativos según el uso real; nada de cifras arábigas en `meta`/`frase` del básico.

## Romanización (obligatoria, la comprueba el validador)

Igual que en el curso (romanización en los ejercicios hasta N4; después, solo en el vocabulario):

| Tramo | Lleva romanización |
|---|---|
| básico | `fraseRom` en cada objetivo; `metaRom` y `ejemploRom` en cada palabra; `metaRom` en cada frase |
| intermedio y avanzado | solo `metaRom` en cada palabra del vocabulario (ningún otro campo `…Rom`) |

El sistema es el de la sección de romanización de la ficha (Romanización Revisada oficial (2000), con los cambios fonéticos reales: 감사합니다 → gamsahamnida, 실례 → sillye). En minúsculas (mayúscula solo en nombres propios de la ficha), un grupo por eojeol con las partículas pegadas, misma puntuación que el hangul.

```json
{"id": "s1-b-v1", "meta": "메뉴", "metaRom": "menyu", "traduccion": {"es": "el menú", "en": "the menu"},
 "ejemplo": "메뉴 좀 주세요.", "ejemploRom": "menyu jom juseyo."}
```
