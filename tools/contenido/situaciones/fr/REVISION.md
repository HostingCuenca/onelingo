# Revisión de situaciones en francés

- **Quién revisa:** alguien distinto del autor, con francés de Francia nativo y buen español e inglés.
- **Qué revisar en `lote-N.json`** (contrato en `ENCARGO.md`):
  1. **Francés:** correcto y natural en Francia (registro tu/vous según el contexto, colocaciones reales); tipografía con U+202F antes de ? ! : ; y el apóstrofo ’.
  2. **Nivel:** básico simple, intermedio B1–B2, avanzado con matices. Los tramos crecen, los objetivos no se repiten entre tramos y los ids del básico conservan su intención original.
  3. **Vocabulario:** útil y propio de la situación, con artículo en los sustantivos y un `ejemplo` que contiene la palabra; sin repetidas entre tramos.
  4. **Traducciones `{es, en}`:** exactas; español neutro de América (tú) e inglés americano natural.
  5. **Adaptación cultural** a Francia, sin estereotipos.
- **Cómo:** corrige directamente en el archivo y luego ejecuta `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/fr/lote-N.json` hasta tener 0 errores.
- **Entregable:** `revision-N.md` con el veredicto **GO** o **REVISE**, los cambios por tipo y 6–10 ejemplos de antes → después.
