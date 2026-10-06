# Revisión de situaciones en alemán

- **Quién revisa:** alguien distinto del autor, con alemán estándar nativo y buen español e inglés.
- **Qué revisar en `lote-N.json`** (contrato en `ENCARGO.md`):
  1. **Alemán:** correcto y natural en Alemania (Sie/du según el contexto, género y caso, verbo en segunda posición, Satzklammer, colocaciones reales), sin regionalismos.
  2. **Nivel:** básico simple, intermedio B1–B2, avanzado con matices. Los tramos crecen, los objetivos no se repiten entre tramos y los ids del básico conservan su intención original.
  3. **Vocabulario:** útil y propio de la situación, sustantivos con artículo y un `ejemplo` que contiene la palabra (forma flexionada aceptable); sin repetidas entre tramos.
  4. **Traducciones `{es, en}`:** exactas; español neutro de América (tú) e inglés americano natural.
  5. **Adaptación cultural** a Alemania, sin estereotipos, solo datos reales y sin mencionar Ecuador. Falsos amigos traducidos correctamente.
- **Cómo:** corrige directamente en el archivo y luego ejecuta `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/de/lote-N.json` hasta tener 0 errores.
- **Entregable:** `revision-N.md` con el veredicto **GO** o **REVISE** en la primera línea, los cambios por tipo y 6–10 ejemplos de antes → después.
