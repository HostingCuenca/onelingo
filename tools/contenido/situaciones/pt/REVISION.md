# Revisión de situaciones en portugués de Brasil

- **Quién revisa:** alguien distinto del autor, con portugués de Brasil nativo y buen español e inglés.
- **Qué revisar en `lote-N.json`** (contrato en `ENCARGO.md`):
  1. **Portugués de Brasil:** correcto y natural en Brasil (você / o senhor según el contexto, colocaciones reales, ortografía posterior al Acuerdo), sin europeísmos.
  2. **Nivel:** básico simple, intermedio B1–B2, avanzado con matices. Los tramos crecen, los objetivos no se repiten entre tramos y los ids del básico conservan su intención original.
  3. **Vocabulario:** útil y propio de la situación, con artículo en los sustantivos y un `ejemplo` que contiene la palabra; sin repetidas entre tramos.
  4. **Traducciones `{es, en}`:** exactas; español neutro de América (tú) e inglés americano natural.
  5. **Adaptación cultural** a Brasil (Recife cuando hay lugar concreto), sin estereotipos, solo datos reales y sin mencionar Ecuador. Falsos amigos traducidos correctamente.
- **Cómo:** corrige directamente en el archivo y luego ejecuta `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/pt/lote-N.json` hasta tener 0 errores.
- **Entregable:** `revision-N.md` con el veredicto **GO** o **REVISE**, los cambios por tipo y 6–10 ejemplos de antes → después.
