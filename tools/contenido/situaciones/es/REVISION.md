# Revisión de situaciones en español

- **Quién revisa:** alguien distinto del autor, con español latinoamericano nativo e inglés americano.
- **Qué revisar en `lote-N.json`** (contrato en `ENCARGO.md`):
  1. **Español:** correcto y natural en América Latina (Quito como base), registro tú/usted según el contexto, colocaciones reales; nada peninsular; ¿…? ¡…! y tildes.
  2. **Nivel:** básico simple, intermedio B1–B2, avanzado con matices. Los tramos crecen, los objetivos no se repiten entre tramos y los ids conservan la intención del inglés.
  3. **Vocabulario:** útil y propio de la situación, con artículo en los sustantivos y un `ejemplo` que contiene la palabra; sin repetidas entre tramos.
  4. **Traducciones `{en}`:** exactas y en inglés americano natural; sin clave `es`.
  5. **Adaptación cultural** a Ecuador/América Latina, sin estereotipos.
- **Cómo:** corrige directamente en el archivo y luego ejecuta `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/es/lote-N.json` hasta tener 0 errores.
- **Entregable:** `revision-N.md` con el veredicto **GO** o **REVISE**, los cambios por tipo y 6–10 ejemplos de antes → después.
