# Encargo: situaciones en alemán (DE)

- **Contrato:** `docs/claude-educacion/SITUACIONES_V2.md`, sección «Esquema genérico para idiomas nuevos». Mismo formato que `tools/contenido/situaciones/pt/lote-N.json`.
- **Partida:** el contenido inglés aprobado (`assets/contenido/en/situaciones.json`) y el catálogo (`assets/contenido/situaciones/catalogo.json`). Cada situación y tramo conserva **la misma intención comunicativa** (los mismos 3 objetivos con los mismos ids), adaptada a Alemania: euros (€), U-Bahn/S-Bahn/Deutsche Bahn, Bäckerei, Apotheke, Hausarzt, Krankenkasse, Bürgeramt (Anmeldung), EC-Karte, Pfand. **«Sie» por defecto** con desconocidos, tiendas, oficinas y trabajo; «du» entre amigos, familia o gente joven cuando el contexto lo pide.
- **Ambientación:** Alemania; cuando la situación pide un lugar concreto, ciudades reales (Berlín, Hamburgo, Múnich, Colonia…). Solo datos reales. **Nunca se menciona Ecuador** (la app es para EE. UU. y Latinoamérica en general). Sin historia continua ni personajes del curso.
- **Contenido por tramo:**
  - `objetivos`: 3, con `titulo` {es, en}, `frase` en alemán y `traduccion` {es, en};
  - `vocabulario`: 10, con `meta` en alemán (sustantivos con artículo: «die Rechnung»), `traduccion` {es, en} y `ejemplo` en alemán que contenga la palabra;
  - `frases`: 4, con `meta` y `traduccion` {es, en}.
- **Niveles:** básico A1–A2 (frases ≤ 12 palabras), intermedio B1–B2 (≤ 20), avanzado B2+–C1 (≤ 30, con matices: Konjunktiv II de cortesía, pasiva, conectores).
- **Alemán estándar de Alemania:** ß y umlauts, sustantivos con mayúscula, verbo en segunda posición y Satzklammer, orden de la subordinada; nada regional ni de Austria/Suiza. Sin palabras repetidas entre los tramos de una situación.
- **Cifras:** en las frases de partida, horas y precios como se dicen («um halb acht», «zwölf Euro fünfzig»); evita cifras de 3+ dígitos en `frase`/`meta`.
- **Falsos amigos:** cuando aparece uno (Chef, bekommen, Handy, Gift, Rezept, Kaution, Mappe…), la `traduccion` es la correcta y nunca la del falso amigo.
- **Idiomas de apoyo:** español neutro de América (tú; celular, auto, computadora, estacionar) e inglés general americano.
- **Validación:** `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/de/lote-N.json` → 0 errores.
