# Encargo: situaciones en español para anglohablantes (ES-4)

- **Contrato:** `docs/claude-educacion/SITUACIONES_V2.md`, sección «Esquema genérico para idiomas nuevos», con una diferencia: el apoyo es **solo inglés** (`{"en": …}`, sin clave `es`), como la ruta del español (`idiomasApoyo: ["en"]`).
- **Partida:** el contenido inglés aprobado (`assets/contenido/en/situaciones.json`), el francés como modelo de formato (`tools/contenido/situaciones/fr/lote-N.json`) y el catálogo (`assets/contenido/situaciones/catalogo.json`). Cada situación y tramo conserva **la misma intención comunicativa** (los mismos 3 objetivos con los mismos ids), adaptada a América Latina con Quito como base: dólares, bus/Ecovía/metro de Quito, la tienda del barrio, farmacia, cédula, el IESS o el seguro privado, tú entre amigos y usted con mayores, en trámites y con desconocidos.
- **Contenido por tramo:**
  - `objetivos`: 3, con `titulo` {en}, `frase` en español y `traduccion` {en};
  - `vocabulario`: 10, con `meta` en español (artículo en los sustantivos: el, la, los, las), `traduccion` {en} y `ejemplo` en español que contenga la palabra;
  - `frases`: 4, con `meta` y `traduccion` {en}.
- **Niveles:** básico A1–A2 (frases ≤ 12 palabras), intermedio B1–B2 (≤ 20), avanzado B2+–C1 (≤ 30, con matices, condicional de cortesía y subjuntivo cuando toque).
- **Español latinoamericano neutro:** carro, celular, computadora, departamento, jugo, boleto, mesero, manejar, estacionar, el vuelto, ustedes. Nunca vosotros, coche, ordenador, móvil, zumo, piso (vivienda), vale, billete (de transporte), gafas, conducir. Ortografía completa (¿…? ¡…! y tildes). Sin palabras repetidas entre los tramos de una situación.
- **Inglés de apoyo:** inglés general americano, natural y exacto.
- **Validación:** `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/es/lote-N.json` → 0 errores.
