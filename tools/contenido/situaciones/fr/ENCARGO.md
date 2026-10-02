# Encargo: situaciones en francés (FR-4)

- **Contrato:** `docs/claude-educacion/SITUACIONES_V2.md`, sección «Esquema genérico para idiomas nuevos».
- **Partida:** el contenido inglés aprobado (`assets/contenido/en/situaciones.json`) y el catálogo (`assets/contenido/situaciones/catalogo.json`). Cada situación y tramo conserva **la misma intención comunicativa** (los mismos 3 objetivos con los mismos ids), adaptada a Francia: euros, métro, SNCF, boulangerie, pharmacie, carte Vitale, tutoiement / vouvoiement según el contexto.
- **Contenido por tramo:**
  - `objetivos`: 3, con `titulo` {es, en}, `frase` en francés y `traduccion` {es, en};
  - `vocabulario`: 10, con `meta` en francés (artículo en los sustantivos), `traduccion` {es, en} y `ejemplo` en francés que contenga la palabra;
  - `frases`: 4, con `meta` y `traduccion` {es, en}.
- **Niveles:** básico A1–A2 (frases ≤ 12 palabras), intermedio B1–B2 (≤ 20), avanzado B2+–C1 (≤ 30, con matices, condicional de cortesía y subjuntivo cuando toque).
- **Francés de Francia:** espacio fina U+202F antes de ? ! : ; y apóstrofo ’. Sin palabras repetidas entre los tramos de una situación.
- **Idiomas de apoyo:** español neutro de América (tú) e inglés general americano.
- **Validación:** `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/fr/lote-N.json` → 0 errores.
