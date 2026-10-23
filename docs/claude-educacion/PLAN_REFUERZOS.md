# Plan: 100 clases por nivel con clases de refuerzo (DEC-036)

## Objetivo

Los 9 idiomas distintos del inglés tienen 50 clases por nivel (`cNN`, plan DEC-034). El cliente quiere ver 100 por nivel. Por cada clase `cNN` se suma una **clase de refuerzo `rNN`**, un poco más exigente, armada con el material del bloque que ya está revisado. No se escriben clases nuevas. El inglés ya tiene 100 por nivel y no se toca.

Al terminar: 9 idiomas × 10 niveles × 50 refuerzos = **4.500 clases nuevas**, y cada idioma queda con 1.000.

## Método de bajo consumo (probado en fr N1, 22-10-2026)

Herramientas en `tools/contenido/refuerzo/`:

| Paso | Comando | Costo |
|---|---|---|
| 1. Paquete del nivel | `construir.py <idioma> N todo --paquete` | 0 tokens |
| 2. Variación ligera | un agente sonnet por nivel con `ENCARGO_VARIACION.md` (máx. 3 llamadas) | ~160 k tokens en fr N1 |
| 3. Construir y validar | `construir.py <idioma> N todo`: control automático y `validar_ruta.py` | 0 tokens |
| 4. Revisión | `revision.py <idioma> N salida.html`: tabla original → variante | lectura humana o de Claude |
| 5. Correcciones | editar `<idioma>/nN.variantes.json`, quitar la clave o corregirla, y volver al paso 3 | mínimo |

**Cómo es una clase de refuerzo:**
- repaso breve con el error típico, los ejemplos, el vocabulario y la tabla de la clase original;
- los ejercicios de la clase original en versión más difícil: elegir pasa a escribir, escuchar pasa a dictado y completar va sin opciones;
- dos ejercicios de otras clases del bloque, una frase combinada y un relacionar mezclado;
- la situación invertida, donde el alumno hace la parte de un personaje;
- nota mínima de 0,9 y sin pistas fuera de la práctica guiada.

**Variación con IA:** cambia un solo elemento por frase. Las variantes van solo en ejercicios escritos. Los dictados y los diálogos usan las frases originales, que ya tienen el audio en caché, así que no gastan créditos nuevos de ElevenLabs.

**Control automático de cada variante:**
- solo palabras ya enseñadas hasta su bloque;
- de 1 a 3 palabras cambiadas;
- conserva la palabra del hueco;
- no repite otra frase del bloque;
- no menciona Ecuador;
- trae las traducciones.

Si una variante falla, queda la frase original: no hay reintentos ni revisor por bloque.

## Resultado del piloto (fr N1)

- 50 refuerzos, entre 11 y 17 ejercicios cada uno, con al menos el 91 % de producción. `validar_ruta.py` da 0 errores y pasan las pruebas de contenido de Flutter.
- 324 de 348 frases variadas (93 %). En la revisión a ojo se corrigieron 4: Cuenca en lugar de un lugar francés, «Bonjour, à demain», «les cafés» y una traducción.
- Consumo: **161 k tokens y 4 minutos** para el nivel, frente a ~3,6 M por nivel al escribir clases.
- Probado en la app local: el repaso, escribir sin opciones, completar variado y el dictado funcionan, y el nivel cuenta 100 unidades.

## Orden de trabajo

| # | Idioma | Estado | Nota |
|---|---|---|---|
| 1 | Francés (fr) | **completo** N1–N10 (22-10), sin desplegar | piloto; ~2,3 M tokens; 2 errores de las originales corregidos |
| 2 | Alemán (de) | **completo** N1–N10 (22-10), sin desplegar | ~2 M tokens; 3.309 variantes de los agentes, 44 descartadas en revisión (registro du/Sie, hechos, colocaciones) |
| 3 | Portugués (pt) | **completo** N1–N10 (22-10), sin desplegar | ~2,3 M tokens; curso con historia (Camila en Recife): los agentes cambiaban nombres, ciudades y cifras, así que se sumaron las reglas 6d/6e y un filtro automático; quedan 2.402 variantes tras quitar ~20 % en filtro y revisión |
| 4 | Italiano (it) | **completo** N1–N10 (22-10), sin desplegar | ~1,8 M tokens; con las reglas 6d/6e los agentes casi no tocaron la historia: 1.816 variantes, 6 % quitadas en filtro y revisión |
| 5 | Español (es) | **completo** N1–N10 (22-10), sin desplegar | ~2 M tokens; apoyo solo en inglés (el constructor copia `en` a `es` mientras arma y lo quita al escribir); historia en Quito: los agentes omiten esas frases; 2.292 variantes, ~35 quitadas en revisión |
| 6 | Ruso (ru) | **completo** N1–N10 (22-10), sin desplegar | 1.439 variantes, 18 quitadas en revisión; constructor adaptado a `*Rom`: `textoRom` y `tokensRom` se arman con la romanización de ejemplos, diálogo y vocabulario; las variantes traen su `rom` (regla 8b); si no cuadra palabra por palabra, el ejercicio queda sin romanización |
| 7 | Chino (zh) | **completo** N1–N10 (22-10), sin desplegar | 2.048 variantes, 17 quitadas en revisión; `*Rom` (pinyin). El texto del curso ya viene separado por palabras, así que «ordenar» funciona igual |
| 8 | Japonés (ja) | **completo** N1–N10 (22-10), sin desplegar | 1.964 variantes, 15 quitadas en revisión; `*Rom` (romaji). «ordenar» igual que en chino |
| 9 | Coreano (ko) | **completo** N1–N10 (22-10), sin desplegar | 1.717 variantes, 24 quitadas en revisión; `*Rom`. El validador ko rechaza conjugaciones válidas, así que quedarán más frases originales (Kiwi queda para después) |

**Por idioma:**
1. Los 10 niveles, de 3 en 3 agentes en paralelo.
2. Revisión de cada tabla.
3. Conectar el constructor al `ruta-<idioma>/integrar.py`.
4. `flutter test`.
5. **Un commit por idioma, sin push.**
6. Despliegue a producción solo con el idioma al 100 % y con autorización expresa, un despliegue por idioma (`DEPLOYMENT_RUNBOOK.md`).

**Estimación:** 2,5–3 M tokens de agentes por idioma (los niveles altos tienen frases y vocabulario más largos), unos 25 M en total.

## Cuidados

- `ruta-<idioma>/integrar.py` reescribe los bloques sin refuerzos. Tras integrar, vuelve a correr `construir.py <idioma> N todo`: es determinista y reaplica las variantes guardadas.
- Quien ya iba avanzado en un nivel verá la clase siguiente bloqueada hasta hacer los refuerzos del bloque. Antes del lanzamiento no importa.
- Las correcciones a mano en `nN-bYY.variantes.json` mandan sobre `nN.variantes.json`.
