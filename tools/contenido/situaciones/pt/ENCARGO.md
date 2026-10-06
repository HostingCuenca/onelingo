# Encargo: situaciones en portugués de Brasil (PT-7)

- **Contrato:** `docs/claude-educacion/SITUACIONES_V2.md`, sección «Esquema genérico para idiomas nuevos». Mismo formato que `tools/contenido/situaciones/fr/lote-N.json`.
- **Partida:** el contenido inglés aprobado (`assets/contenido/en/situaciones.json`) y el catálogo (`assets/contenido/situaciones/catalogo.json`). Cada situación y tramo conserva **la misma intención comunicativa** (los mismos 3 objetivos con los mismos ids), adaptada a Brasil: reais (R$), metrô/ônibus, Pix, padaria, farmácia, UBS/SUS, CPF, "você" por defecto y "o senhor / a senhora" cuando el contexto es formal.
- **Ambientación:** Brasil, con preferencia por Recife cuando la situación pide un lugar concreto (Boa Viagem, Marco Zero, rio Capibaribe, Olinda al lado). Solo datos reales. **Nunca se menciona Ecuador** (ni Quito ni otras ciudades ecuatorianas): la app es para EE. UU. y Latinoamérica en general.
- **Contenido por tramo:**
  - `objetivos`: 3, con `titulo` {es, en}, `frase` en portugués y `traduccion` {es, en};
  - `vocabulario`: 10, con `meta` en portugués (artículo en los sustantivos), `traduccion` {es, en} y `ejemplo` en portugués que contenga la palabra;
  - `frases`: 4, con `meta` y `traduccion` {es, en}.
- **Niveles:** básico A1–A2 (frases ≤ 12 palabras), intermedio B1–B2 (≤ 20), avanzado B2+–C1 (≤ 30, con matices, futuro do pretérito de cortesía y subjuntivo cuando toque).
- **Portugués de Brasil:** ortografía posterior al Acuerdo (ideia, voo, para), "você", "a gente" en lo coloquial, colocación pronominal brasileña natural (próclisis en el habla: "me chamo", "te ligo"). Sin europeísmos (autocarro, comboio, telemóvel, pequeno-almoço, rapariga, "tu" con verbo en 2.ª persona como norma). Sin palabras repetidas entre los tramos de una situación.
- **Falsos amigos:** cuando aparece uno (esquisito, polvo, grávida/embaraçada, oficina, apelido, ninguém, borracha, exquisito…), la `traduccion` es la correcta y nunca la del falso amigo.
- **Idiomas de apoyo:** español neutro de América (tú) e inglés general americano.
- **Validación:** `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/pt/lote-N.json` → 0 errores.
