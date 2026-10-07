# Romanización (`rom`) en ru, ko, ja y zh

Fecha: 07-10-2026. Solo para idiomas sin alfabeto latino (ru, ko, ja, zh). En it, de, fr, pt, es y en no hay ningún campo de romanización.

## Convención: sufijo «Rom» paralelo al campo

| Dónde | Campo | Romanización |
|---|---|---|
| Vocablo, ejemplo, línea de diálogo, celda de tabla | `texto` | `rom` |
| Nivel 0: palabra o paso con marcado | `m` | `rom` |
| Ítem de ejercicio | `texto` / `pregunta` | `textoRom` / `preguntaRom` |
| Ítem de ejercicio | `opciones`, `tokens` | `opcionesRom`, `tokensRom` (listas paralelas) |
| Ítem `relacionar` | izquierda de cada par | `paresRom` (lista paralela a `pares`) |
| Nivel 0 | `opciones`, `fichas`, `letra`, `de`, `a` | `opcionesRom`, `fichasRom`, `letraRom`, `deRom`, `aRom` |
| Nivel 0 (sonidos.json) | `ancla`, `ejemplos` | `anclaRom`, `ejemplosRom` |
| Opcionales (ru) | `hablante`, `incorrecto`, `correcto` | `hablanteRom`, `incorrectoRom`, `correctoRom` |

- Las listas paralelas tienen la misma longitud que su campo. Una posición que no está en la escritura del idioma (por ejemplo, una opción en español) va como `""`.
- Si las opciones son de apoyo `{es, en}`, no hay `opcionesRom`.
- **`audio`, `respuesta` y `aceptadas` nunca llevan romanización:** el alumno escucha o escribe en el idioma.
- El hueco `___` se copia tal cual en `textoRom`.
- Claves retiradas: `rom` suelto en un ítem, `romOpciones`, `romFichas`, `romDe` y `romA`.

## Regla didáctica (app)

- **N1–N2, Fundamentos y Nivel 0:** la romanización se ve en gris, pequeña, bajo el texto, cada opción, ficha, token y par.
- **Desde N3:** va oculta. El botón «Ver romanización» la abre para toda la clase. Está en `ItemView` y en los pasos de enseñanza de `unidad_screen.dart`, y la prueba de nivel también lo tiene.
- **Ejercicios de escucha:** la romanización de las opciones se muestra al corregir, nunca antes, porque delataría lo que se oye. En la ruta afecta a `escuchar`; en el Nivel 0, a `escucha_elige`, `toca_sonido`, `escucha_letra`, `deletreo`, `construye` y `cambia`. El panel de resultado enseña la romanización de la respuesta correcta.

## Dónde se aplica

- **App:**
  - modelos: `Item`, `Frase.hablanteRom` y `Celda` en `lib/core/aprendizaje/modelos.dart`; `Palabra.rom`, `PasoN0` y `SonidoVocal` en `lib/core/nivel0/nivel0.dart`;
  - widget: `TextoRom` en `lib/shared/widgets/romanizacion.dart`.
- **Validación:**
  - `tools/contenido/rom_items.py` (ítems), usado por `tools/contenido/ruta-{ru,ko,ja,zh}/validar.py`.
- **Autoría:**
  - `tools/ia/esquemas.py`: `clase(idi)` y `revision(idi)` añaden los cuatro campos a los ítems solo en ru, ko, ja y zh;
  - bloque `<!-- rom-items -->` de `tools/ia/prompts/clase_autor_ligera.md`, que `prompt()` quita para la escritura latina.
- **Nivel 0:** `tools/contenido/nivel0-{ru,ko,ja,zh}/generar.py`.
