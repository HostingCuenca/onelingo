# Encargo: situaciones en italiano (IT)

- **Contrato:** `docs/claude-educacion/SITUACIONES_V2.md`, sección «Esquema genérico para idiomas nuevos». Mismo formato que `tools/contenido/situaciones/pt/lote-N.json` (modelo de una situación en el paquete: `modelo-pt-s1.json`).
- **Partida:** el contenido inglés aprobado (en el paquete, `en-lote-N.json`, 10 situaciones con su nombre). Cada situación y tramo conserva **la misma intención comunicativa** (los mismos 3 objetivos con los mismos ids), adaptada al país del idioma: no se traduce palabra por palabra.
- **Ficha del idioma:** `tools/ia/idiomas/it.md` es la autoridad en variedad, tratamiento, nombres y lugares (lista cerrada, sin datos verificables: ni líneas de metro, direcciones, precios reales ni comercios reales), ortografía.
- **Nunca se menciona Ecuador** (ni Quito, Guayaquil, Cuenca ni «ecuatoriano»), en ningún campo: la app es para EE. UU. y Latinoamérica en general. Sin historia continua ni personajes del curso.
- **Contenido por tramo:**
  - `objetivos`: 3, con `titulo` {es, en} (infinitivo, ≤ 60 caracteres), `frase` en italiano y `traduccion` {es, en};
  - `vocabulario`: 10, con `meta` en italiano (sustantivos con artículo: «il conto», «la ricevuta»), `traduccion` {es, en} y `ejemplo` en italiano que contenga la palabra;
  - `frases`: 4, con `meta` y `traduccion` {es, en}.
- **Niveles:** básico A1–A2 (frases ≤ 12 palabras), intermedio B1–B2 (≤ 20), avanzado B2+–C1 (≤ 30, con matices: condizionale de cortesía, congiuntivo, conectores). Sin palabras repetidas entre los tramos de una situación.
- **Situación 50 («Conversación libre»):** básico = presentarse y hablar de gustos; intermedio = dar y defender opiniones; avanzado = debatir y matizar.
- **Idiomas de apoyo:** español neutro de América (tú; celular, auto, computadora, departamento, boleto) e inglés general americano. Con un falso amigo, la `traduccion` es la correcta.
- **Validación:** `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/it/lote-N.json` → 0 errores (también acepta un archivo con una lista de una sola situación).
- **Ambientación:** Italia, con ciudades de la lista cerrada de la ficha (Roma, Milano, Napoli, Firenze, Bologna…). Euros (€), Trenitalia/regionale, autobus, farmacia, medico di base, tessera sanitaria, codice fiscale, bar (caffè al banco), scontrino. **«Lei» por defecto** con desconocidos, tiendas, oficinas y trabajo; «tu» entre amigos, familia o gente joven.
- **Italiano estándar:** acentos gráficos correctos (è/e, perché, città, più, già), preposiciones articuladas (nel, al, dal, sul), elisión con apóstrofo (l’albergo, un’ora); sin regionalismos.
- **Cifras:** horas y precios como se dicen («alle otto e mezza», «dodici euro e cinquanta»); evita cifras de 3+ dígitos en `frase`/`meta`.
