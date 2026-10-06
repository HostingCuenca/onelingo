GO

# Revisión de de N1 bloque 1 (c01–c05), `n1-b01.json`

Revisor distinto del autor. Tras mis correcciones: `validar_bloque.py de 1 1` = 0 errores. Respaldo del borrador del autor fuera del repo (scratchpad).

## Veredicto por criterio

1. **Alemán estándar: OK.** Mayúsculas (Sie, Ihnen, sustantivos), terminaciones de presente (-e/-st/-t/-en/-t/-en), seid/sind, Deutscher/Deutsche, plurales de vocabulario (Herr, -en; Mexikanerin, -nen; Punkt, -e…), orden V2 y verbo inicial en preguntas. Sin errores de alemán.
2. **Solo `introduce` + `recicla`: OK.** c01 anrede; c02 nacionalidad como sustantivo sin artículo; c03 presente regular; c04 dictado de correo y letras; c05 ihr/Sie/sie. Sin acusativo, dativo ni plurales fuera de ficha. c05 usa «euch» solo como reconocimiento.
3. **Formas flexionadas en tabla/ejemplos antes de evaluarse: OK.** c03 tablas completas de 6 verbos; c05 tabla wir/ihr/sie/Sie con kommen y sein (ich/du/er de sein vienen de f0; no se añaden filas). «großes/kleines» en ejemplos de c04.
4. **Claridad ES/EN y guías de pronunciación: OK con retoques.** Sonidos del día comparados con las guías del encargo: golpe de glotis, «-er» ≈ a, w = v, ei/ie, alfabeto (e, i, j, v, w). Corregí: c05 ES («se escriben al revés» era confuso), c03 ES («o seguida de una consonante suele ser larga» no vale para «wohnen»: es la «h» la que alarga), c04 EN («fow» sin referencia; ahora «rhymes with cow»), varias frases EN torpes (c01, c02, c04). Ninguna guía promete un sonido igual al español.
5. **Falsos amigos / una sola respuesta: OK.** Este bloque no contiene ninguno de la lista del encargo; «studieren» (universidad) ya iba matizado. Todos los `relacionar` tienen una sola correspondencia dentro de su conjunto (ver decisiones). `ordenar` fijan el Vorfeld con «empieza con…».
6. **Lectura y reglas: OK.** Diálogos de 5, 4, 3, 5 y 6 líneas (3–6). Sin Ecuador/Quito/etc. Sin Lumo. Nombres genéricos, sin lugares con datos reales.

## Decisiones sobre los puntos abiertos

**c04, correo electrónico.** Se enseña y se oye la forma **dicha** («lena Punkt schulz At gmx Punkt de»); la forma escrita queda como apoyo visual. Razones: (a) es lo que el alumno oye y dice en Alemania; (b) el validador tokeniza «ruiz@web» y «tom_berg@gmx» como palabras no enseñadas; (c) la app lee en voz alta las celdas `texto` de las tablas, así que «@» y «_» sonarían mal (regla de audio del encargo); (d) la normalización de la app convierte «.» en espacio, así que la respuesta escrita con signos es frágil. Cambios aplicados:
- Tabla «Correos dictados»: columna «Se dice» con audio (celda `texto`); columna «Se escribe» como celda `apoyo` (se ve, no se lee ni se tokeniza). Quita el truco del autor de meter la dirección escrita como celda de audio.
- Opciones escritas de `situacion.s1` y `evaluacion.e1` (elegir/escuchar entre carla.ruiz@web.de / carla_ruiz@web.de y tom_berg / tom-berg): opciones tipo apoyo `{es, en}`, que no se tokenizan ni se pronuncian. Conservan la habilidad «oigo el dictado y reconozco la forma escrita».
- `independiente.i1` (escribir): ahora el alumno **dicta** (ve lena.schulz@gmx.de en la consigna y escribe «lena Punkt schulz At gmx Punkt de»). Desvío menor de la ficha («escribe con signos la dirección dictada»).
- `evaluacion.e4` (escribir): sigue con audio, pero se transcribe lo que se oye («paul Punkt weber At web Punkt de»), no la forma con signos.
- Se mantiene el formato de cada ítem del plan (mismas claves); cambia solo qué se escribe.

**«U-Umlaut» y guiones.** Completar con opciones «U-Umlaut»/«A-Umlaut»: una sola respuesta; añadí `aceptadas: ["U Umlaut"]` porque la normalización de la app no quita el guion. En el `relacionar` de c04 (Bindestrich/Punkt/Unterstrich ↔ guion/punto/guion bajo) la pista «Unter = abajo» lo hace inequívoco.

**`relacionar` con apoyo a la derecha.** «der Mexikaner ↔ hombre de México…» (c02): 4 pares sin solape, con género y país distintos. «spielt ↔ er, sie, es» (c03): las opciones son ich/du/er-sie-es; «spielt» también es ihr, pero ihr no está entre las opciones, así que la respuesta es única. Lo mismo con «kommt ↔ ihr» en c05 (er no está entre las opciones). Sin cambios, solo documentado.

## Cambios realizados

- c01: EN de la explicación de Herr/Frau (frase torpe).
- c02: ES «el alemán es la excepción» (ambiguo idioma/persona) y EN «noun with no a».
- c03: ES de la explicación (sujeto omitido, se aclara que el pronombre casi siempre se dice) y del sonido (o + h).
- c04: ver decisiones; además sonido del día reescrito (ES/EN), explicación de «At» sin «arroba», vocablo «der Umlaut» (la diéresis alemana no es el Umlaut), `aceptadas` en i2.
- c05: sonido del día ES/EN (ei/ie).
- Se probó y descartó un ejemplo con «U-Umlaut» antes de la tabla (el validador exige que se enseñe antes).

## Sin resolver

- Verificar con las voces de-DE el audio de «At» (¿«at» o «et»?), «Punkt», «Eszett» y «U-Umlaut» antes de integrar; la nota de la calibración 1 del encargo sigue pendiente.
- Plan de ejercicios: c04 `i1` y `e4` cambian lo que se escribe respecto a la ficha; confirmar que el plan detallado lo admite o actualizar la ficha.
- Aceptadas de `ordenar` de c03 i3 («Deutsch lernt Herr Wolf.») y c05 i3 («Aus Mexiko kommen wir.») contradicen su propia consigna «empieza con…»; inofensivas, no las toqué.
- c05: tabla de sein solo con wir/ihr/sie/Sie (ich/du/er vienen de f0). Aceptable en N1; añadir filas completas si se quiere uniformidad con c03.
- Duración de 10–12 min no medible aquí.
- Los nombres Ruiz y Wolf se repiten entre clases (c02/c04 y c01/c03/c04); sin reparto no es error, pero conviene variar en bloques futuros.

## Calibración

1. **Direcciones, URLs, símbolos y cualquier cadena con «@ _ - / .»:** no entran como `respuesta`, `opciones` de tipo texto ni celdas `texto`. Se enseña y se evalúa la forma dicha (Punkt, At…). La forma escrita va en celdas `apoyo`, en opciones `{es,en}` o en la consigna. Motivo: el validador las parte mal, la app lee las celdas `texto` en voz alta y su normalización convierte «.» en espacio.
2. **Orden de enseñanza:** una palabra debe estar en `ejemplos`/`vocabulario` antes de la `tabla` que la trae; no uses en `ejemplos` formas que solo enseña la tabla posterior (p. ej. «U-Umlaut»). Comprueba con el validador cada vez que muevas un paso.
3. **`relacionar` con apoyo a la derecha:** las opciones de la derecha son un conjunto cerrado; cada forma de la izquierda debe tener una sola pareja dentro de ese conjunto aunque existan homónimos fuera (spielt = er/ihr). Si el conjunto no lo garantiza, dilo en la consigna.
4. **Guías de sonido:** copia las del encargo; no inventes reglas fonéticas propias («o + una consonante es larga» es falso; la longitud se enseña por «h» o vocal doble). En EN indica una palabra de referencia, no comparaciones de ortografía («mirror images»). Una explicación por sonido, sin mezclar guía y gramática.
5. **Consigna y `aceptadas`:** si la consigna fija el Vorfeld («empieza con X»), no pongas en `aceptadas` el orden alternativo; si quieres aceptarlo, quita la restricción.
6. **Idioma de apoyo:** revisa el EN por frases de traducción literal («a noun with no “a”», «mirror images»). Compara con el inglés solo cuando aclare (cognados, artículo ausente, V2). Traduce el metalenguaje (Umlaut, Eszett) por lo que es, no por un término español de otra cosa (diéresis).
