# Encargo: situaciones en ruso (RU)

- **Contrato:** `docs/claude-educacion/SITUACIONES_V2.md`, sección «Esquema genérico para idiomas nuevos». Mismo formato que `tools/contenido/situaciones/pt/lote-N.json` (modelo de una situación en el paquete: `modelo-pt-s1.json`).
- **Partida:** el contenido inglés aprobado (en el paquete, `en-lote-N.json`, 10 situaciones con su nombre). Cada situación y tramo conserva **la misma intención comunicativa** (los mismos 3 objetivos con los mismos ids), adaptada al país del idioma: no se traduce palabra por palabra.
- **Ficha del idioma:** `tools/ia/idiomas/ru.md` es la autoridad en variedad, tratamiento, nombres y lugares (lista cerrada, sin datos verificables: ni líneas de metro, direcciones, precios reales ni comercios reales), ortografía y romanización.
- **Nunca se menciona Ecuador** (ni Quito, Guayaquil, Cuenca ni «ecuatoriano»), en ningún campo: la app es para EE. UU. y Latinoamérica en general. Sin historia continua ni personajes del curso.
- **Contenido por tramo:**
  - `objetivos`: 3, con `titulo` {es, en} (infinitivo, ≤ 60 caracteres), `frase` en ruso y `traduccion` {es, en};
  - `vocabulario`: 10, con `meta` en ruso (sustantivos en nominativo singular, verbos en infinitivo; sin artículos), `traduccion` {es, en} y `ejemplo` en ruso que contenga la palabra;
  - `frases`: 4, con `meta` y `traduccion` {es, en}.
- **Niveles:** básico A1–A2 (frases ≤ 12 palabras), intermedio B1–B2 (≤ 20), avanzado B2+–C1 (≤ 30, con matices: condicional con бы, aspecto, participios y conectores). Sin palabras repetidas entre los tramos de una situación.
- **Situación 50 («Conversación libre»):** básico = presentarse y hablar de gustos; intermedio = dar y defender opiniones; avanzado = debatir y matizar.
- **Idiomas de apoyo:** español neutro de América (tú; celular, auto, computadora, departamento, boleto) e inglés general americano. Con un falso amigo, la `traduccion` es la correcta.
- **Validación:** `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/ru/lote-N.json` → 0 errores (también acepta un archivo con una lista de una sola situación).
- **Ambientación:** Rusia, con ciudades de la lista cerrada de la ficha (Москва, Санкт-Петербург, Казань…). Rublos (рубль), метро, электричка, аптека, поликлиника, полис ОМС, паспорт. **«Вы» por defecto** con desconocidos, tiendas, oficinas y trabajo; «ты» entre amigos, familia o gente joven.
- **Ruso estándar:** el cirílico **nunca** lleva marca de acento; «ё» se escribe siempre como ё. Cifras: horas y precios en letras en `frase`/`meta`/`ejemplo` («в восемь часов», «двести рублей»).

## Romanización (obligatoria, la comprueba el validador)

Igual que en el curso (romanización en los ejercicios hasta N4; después, solo en el vocabulario):

| Tramo | Lleva romanización |
|---|---|
| básico | `fraseRom` en cada objetivo; `metaRom` y `ejemploRom` en cada palabra; `metaRom` en cada frase |
| intermedio y avanzado | solo `metaRom` en cada palabra del vocabulario (ningún otro campo `…Rom`) |

El sistema es el de la sección de romanización de la ficha (transliteración neutra letra a letra, con tilde en la vocal tónica de toda palabra de 2+ sílabas). Una palabra rusa = un grupo de la romanización; el validador comprueba letra por letra y que haya una tilde por palabra de 2+ sílabas.

```json
{"id": "s1-b-v1", "meta": "меню", "metaRom": "menyú", "traduccion": {"es": "el menú", "en": "the menu"},
 "ejemplo": "Можно меню, пожалуйста?", "ejemploRom": "Mózhno menyú, pozháluysta?"}
```
