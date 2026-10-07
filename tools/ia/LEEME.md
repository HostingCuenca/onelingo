# tools/ia: producción de cursos con la API de OpenAI

El plan y las puertas de calidad están en `docs/claude-educacion/PLAN_ITALIANO.md`.

- `idiomas/<idioma>.md`: ficha del idioma (variedad, nombres, pronunciación, errores típicos, falsos amigos). Es la única parte que cambia de un idioma a otro.
- `prompts/*.md`: instrucciones de cada etapa. Llevan `{FICHA_IDIOMA}` e `{IDIOMA_NOMBRE}`.
- `esquemas.py`: lo que el modelo puede devolver (JSON estricto). Lo mecánico no está en el esquema: lo pone el programa.
- `openai_contenido.py`: ejecuta las etapas, valida, repara y registra el coste.
- `chequeos.py`: los fallos recurrentes de revisión convertidos en reglas automáticas.
- `registro/`: costes y salidas en bruto del modelo. No se commitea.

```bash
python3 tools/ia/openai_contenido.py mapa    it 2
python3 tools/ia/openai_contenido.py outline it 2
python3 tools/ia/openai_contenido.py fichas  it 2
python3 tools/ia/openai_contenido.py clases  it 2 1
python3 tools/ia/openai_contenido.py revisar it 2 1
python3 tools/ia/openai_contenido.py costos
```

**Modelos:** se eligen con `--modelo` o con las variables `IA_MODELO_AUTOR`, `IA_MODELO_REVISOR` e `IA_MODELO_PLAN`. Por defecto: `gpt-5.4-mini`, `gpt-6-sol` y `gpt-6-sol`. La clave se toma de `OPENAI_API_KEY` o de `backend/.env`, y nunca se imprime.

**Reglas:**
- Si un fallo aparece dos veces en revisión, pasa a la ficha del idioma, a un prompt o a `chequeos.py`.
- No se edita a mano lo que el programa monta (ids, `recicla`, prerrequisitos).
