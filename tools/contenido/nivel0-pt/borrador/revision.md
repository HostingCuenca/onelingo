# Revisión editorial · Nivel 0 portugués

Fecha: 2026-10-03  
Variante pedagógica: portugués de Brasil  
Código técnico: `pt`  
Estado: **GO editorial para staging · NO-GO técnico para activación**

## Artefactos revisados

- `sonidos.json`: 12 IDs vocálicos/grupos nasales congelados.
- `parte-p1-p5.json`: 5 unidades, 20 lecciones y 180 pasos.
- `parte-p6-p10.json`: 5 unidades, 20 lecciones y 182 pasos.
- `nivel0.json`: integración mecánica de las dos partes; 10 unidades, 40 lecciones y 362 pasos.

Cada lección tiene 9–10 pasos. Todos los apoyos editoriales están en español e inglés y todos los tipos de ejercicio existen en la pantalla actual.

## Qué se corrigió antes del GO

- ejemplos inexistentes, ambiguos o mal marcados (`nõo`, `pê`, `sôfá`, `sim`, `nome`, `sem`);
- representación coherente de `ão`, `ãe` y `õe` como pistas visuales apoyadas por audio;
- consonantes `nh`, `lh`, `ch`, `ss`, `ti` y `di` separadas de los IDs vocálicos;
- formulaciones regionales no absolutas para vocales finales, `t/d+i`, `r/rr`, `s` y `l` finales;
- 40 lecciones de 9–10 pasos, sin placeholders ni relleno mecánico;
- P10 como batería global: 10 audios, 5 contrastes, 8 palabras reales, 2 pseudopalabras, deletreo, respuesta funcional y umbral declarado de 80 %;
- metadatos `categoria`, `evaluacion` y `refuerzo` para una recomendación determinista futura.

La revisión independiente final dio **GO editorial**. El validador de Nivel 0 devuelve **0 errores** con `--bilingue` sobre el archivo integrado.

## Bloqueos antes de mover a `assets/`

1. Elegir y probar dos voces nativas brasileñas; registrarlas en `backend/src/lib/voz.ts` y cubrirlas con prueba.
2. Añadir `pt` a `idiomasConNivel0` solo cuando toda la integración esté lista.
3. Hacer que el runtime lea `evaluacion`, `categoria` y `refuerzo`.
4. Exigir 80 % en la batería P10: un intento fallido no puede registrar el Nivel 0 como aprobado.
5. Mostrar las unidades P3–P9 recomendadas según las categorías falladas.
6. Descargar desde Noto los 10 emoji todavía ausentes o sustituirlos por activos Noto existentes, manteniendo créditos: `1f1e7_1f1f7`, `1f331`, `1f347`, `1f44c`, `1f44d`, `1f475`, `1f4d6`, `2e`, `31`, `40`.
7. Repetir `python3 tools/contenido/validar_nivel0.py pt --bilingue`, pruebas Flutter de Nivel 0 y una prueba visual ES/EN.

No activar portugués ni copiar este borrador a `assets/contenido/pt/nivel0/` hasta cerrar todos esos puntos.

## Integración P0 (2026-10-05)

- Emoji: los códigos mal elegidos se corrigieron — `40` (arroba) → `1f4e7` 📧, `2e` (ponto) → `26ab` ⚫, `31` (bom) → `1f44c` 👌 (el mismo ancla que la o nasal de *bom*), `31` (u nasal de *um*) → `0031_20e3` 1️⃣. La bandera `1f1e7_1f1f7` no está en `2D/png/128` de Noto: se sustituyó por `1f30e` 🌎. Los que faltaban se descargaron de Noto con `descargar_emoji.py` (sin generar imágenes); `validar_nivel0.py pt --bilingue`: 0 errores y ningún emoji ausente.
- Copiado a `assets/contenido/pt/nivel0/`; `pt` añadido a `idiomasConNivel0` y a `ProgressState.nivel0Pendiente`; `pubspec.yaml` declara la carpeta.
- Siguen pendientes los puntos 1 y 3–5 (voces pt-BR en `backend/src/lib/voz.ts`, lectura de `evaluacion`/`categoria`/`refuerzo` en el runtime, umbral del 80 % en P10 y recomendación P3–P9).
