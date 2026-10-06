# Encargo: ruta de alemán N1–N10 para hispanohablantes, 50 clases por nivel en 10 bloques

Equivale a `ENCARGO_RUTA_PT.md` para el alemán, con el **método ligero** de `PLAN_ALEMAN.md`: **sin reparto, sin cronología, sin MAPA ni canon**. Cada clase es una situación concreta y autónoma. El alumno es **hispanohablante** (apoyo en español; inglés americano como segundo apoyo).

Lee antes:
- tu **paquete de contexto** (`python3 tools/curriculo/paquete.py de N B`): tus 5 fichas de `curriculo/de/nX.json`, la nota del nivel y una clase modelo. Escribe exactamente lo que dicen las fichas: la gramática nueva es solo la de su `introduce`; lo ya visto va como repaso (`recicla`). Los ejercicios siguen su plan (`ejercicios`): mismo formato, misma clave, misma cosa evaluada. Puedes pulir la redacción y completar `aceptadas`, pistas y feedback;
- `PLAN_ALEMAN.md` §2 (variedad) y §4 (retos) y `ESQUEMA_CONTENIDO.md` (esquema 2).

## Por nivel

| Nivel | cefr | nivelInterno | Duración | Sonido del día | Lectura en la situación |
|---|---|---|---|---|---|
| N1 | A1 | 1 | 10–12 min | sí (`sonido` de la ficha) | diálogo de 3–6 líneas |
| N2 | A2 | 2 | 12–15 min | no; nota de pronunciación si hace falta | 60–160 palabras |
| N3–N4 | B1 | 3–4 | 15 min | no | 130–300 palabras |
| N5–N7 | B2 | 5–7 | 15–20 min | no | 270–560 palabras |
| N8–N10 | C1 | 8–10 | 20 min | no | 360–770 palabras |

La c50 de cada nivel imita el formato Goethe-Zertifikat del MCER (Start Deutsch 1 en N1; C1 en N8–N10). Desde N9, cada clase incrusta el punto gramatical de su `gramatica`.

## Archivo por bloque

`tools/contenido/ruta-de/nX-bYY.json` con `{"modulo": "de.nX-bYY", "unidades": [5 unidades]}`. La revisión va en `revision-nX-bYY.md`.

- **Ids:** `de.nX.c01` … `de.nX.c50`. **Orden:** 100·X + n. **Prerrequisitos:** N1 c01 → `de.f0.vorstellen`; c01 de los demás niveles → la c50 del nivel anterior; cada clase → la anterior.
- **Textos de apoyo:** todos `{"es": …, "en": …}`: español latinoamericano neutro con tú e inglés americano. Las consignas se escriben desde el español; la versión inglesa compara con el inglés cuando ayuda (cognados, V2).
- **Guías de pronunciación** (coherentes con el Nivel 0):
  - ES: «ü» = «i» con los labios de «u»; «ö» = «e» con los labios de «o»; «ä» ≈ «e» abierta; «ei» = «ai», «ie» = «i» larga, «eu/äu» = «oi»; «ch» tras e/i suave como silbido (ich), tras a/o/u como la «j» española (ach); «sch» = «sh»; «sp/st» al inicio = «shp/sht»; «z» = «ts»; «w» = «v» labiodental; «v» = «f» (Vater); «j» = «y»; «h» tras vocal no suena y alarga; «-er» final ≈ «a» («besser» ≈ «bessa»); b/d/g finales suenan p/t/k (Tag ≈ «tak»); la «e» final átona es una vocal débil, nunca muda.
  - EN: «ü» like «ee» with rounded lips; «ö» like «ay» with rounded lips; «ch» in «ich» like the «h» in «huge», in «ach» like Scottish «loch»; «w» like English «v»; «v» like «f»; «z» like «ts»; «ei» like «eye»; «ie» like «ee».
  - Nunca se promete un sonido igual al español: se avisa de la diferencia (longitud vocálica, Umlaut, r vocalizada).

## Cada clase

En orden: `explicacion` (en N1 abre con el sonido del día), `ejemplos` (5–8 con audio), `vocabulario` (6–12 palabras de la ficha; **sustantivos con artículo y plural**: «der Tisch, -e»), `patron` o `tabla` (conjugación completa ich/du/er-sie-es/wir/ihr/sie-Sie; **tablas de caso completas** cuando la clase trate artículos, pronombres o adjetivos), `practica_guiada` (3–5 con `pista`), `practica_independiente` (3–4), `situacion` (contexto, diálogo o texto, 1–2 preguntas), `evaluacion` (≥ 4 ítems puntuables y ≥ 2 formatos; los `escribir` abiertos no cuentan). Además: `erroresFrecuentes` ≥ 1, **típicos de hispanohablantes** («*Ich habe 27 Jahre», «*Heute ich gehe», «*weil ich habe keine Zeit», «*Ich helfe dich», «*mit der Freund», «*Ich bin gegangen nach Hause» [Satzklammer], «*das Tisch», «*Ich habe gegangen»), `recicla` ≥ 30 % del vocabulario anterior y los seis formatos a lo largo del bloque.

## Reglas (las comprueba `validar_ruta.py de`; con `reglasAutoria` también la extensión de la lectura)

- **Nada sin enseñar.** Cada palabra alemana de respuestas, opciones, audios, diálogos y ordenar aparece antes en un paso de enseñanza (`ejemplos`, `vocabulario`, `patron`, `tabla`) de esta clase o de una anterior, incluidos Fundamentos (`de.f0.*`). Los cognados con el inglés (Haus, Wasser) **también se enseñan**. Mientras el validador no tenga morfología alemana, **toda forma flexionada** (plural, caso, terminación del adjetivo, persona del verbo, participio, verbo separable partido) debe aparecer tal cual en una `tabla` o en `ejemplos`.
- **Alemán estándar de Alemania**, ortografía de 2006 con ß. Léxico: Tschüss, Brötchen, Januar, Samstag, Sahne, Kartoffel. Austria y Suiza solo como comprensión en N8, nunca como respuesta esperada.
- **Mayúsculas:** todo sustantivo y el Sie de cortesía con mayúscula en enunciados, respuestas y `aceptadas`. No añadas variantes en minúscula a `aceptadas`: la tolerancia (con aviso) es cosa de la app.
- **Sie / du:** la ficha fija cuál. Sie por defecto con adultos desconocidos y en el trabajo.
- **Falsos amigos (obligatorio, ⚠ con contraste):** Chef (jefe), Termin (cita), Gymnasium (instituto), eventuell (quizá), Karte (tarjeta/mapa) ≠ carta (Brief), also (entonces), bekommen (recibir), Rente (jubilación), Gift (veneno), Rat (consejo), aktuell (actual), spenden (donar), Präservativ, Konkurrenz (competencia), sensibel. Los nuevos que uses van en el informe. Ningún `relacionar` ni ítem de falsos amigos tiene una opción también defendible.
- **Una sola respuesta** por ítem. Variantes igualmente correctas van en `aceptadas`: otro **Vorfeld** en `ordenar` («Heute gehe ich ins Kino» / «Ich gehe heute ins Kino»), contracciones (in dem / im), **ae/oe/ue/ss** por ä/ö/ü/ß. No evalúes solo por el Umlaut, salvo en clases de ortografía.
- **Hablantes:** nombres alemanes genéricos (Anna, Jonas, Lena, Paul, Frau Becker, Herr Wolf…) o el papel en alemán («Kellnerin», «Arzt», «Verkäufer», «Mitarbeiterin»). Nunca el papel en español. El nombre no se arrastra a otras clases: no hay reparto.
- **Lugares:** genéricos («der Bahnhof», «die Apotheke») o ciudades grandes sin datos verificables (Berlin, Hamburg, München, Köln). Sin líneas, direcciones ni precios «reales». **Nunca Ecuador, Quito, Guayaquil, Cuenca ni «ecuatoriano»**; otros países latinoamericanos, España y EE. UU. sí.
- **Lumo:** nunca en la misma escena que otro personaje; nunca en pruebas de ubicación.
- **Opciones de comprensión** en alemán desde N3 (en N1–N2 pueden ir en español). No se pasan al español para esquivar palabras: se enseña la palabra o se reformula.
- **Tablas de lectura** («Zum Lesen: …»): como máximo 15 filas, palabra + sentido + frase; los nombres propios no llevan fila.
- **Un solo hueco** por `completar`; la pista nombra el caso o la persona («Dat., fem.»).
- **Producción abierta:** en un `escribir` con `abierta: true`, el modelo tiene al menos `minimoPalabras` palabras.
- **Audio:** frases naturales; sin «_», «→», «/», «€» ni «%» (escribe «Euro», «Prozent»); números y horas en palabras cuando el audio deba leerlos («halb acht»). Comillas alemanas „…“ solo en texto, no en respuestas.

## Validación

```bash
python3 tools/curriculo/validar_plan.py de              # fichas (0 errores)
python3 tools/curriculo/validar_plan_detallado.py de    # plan de ejercicios (0 errores; requiere la adaptación de PLAN_ALEMAN §7.2)
python3 tools/curriculo/validar_bloque.py de N B        # tu bloque, encadenado con los borradores previos no integrados
```

0 errores del bloque. Si un borrador anterior ya está en `assets/contenido/de/ruta/`, quítalo de la cadena. El revisor (distinto del autor) deja `revision-nX-bYY.md` con **GO** o **REVISE** y «## Sin resolver», y comprueba:
1. corrección del alemán estándar (casos, género, plural, terminaciones, orden V2/verbo final, Perfekt con haben/sein, separables, mayúsculas);
2. que cada clase enseña solo su `introduce` y recicla lo previsto;
3. formas flexionadas presentes en tablas o ejemplos antes de evaluarse;
4. claridad en español **y** en inglés; guías de pronunciación correctas;
5. falsos amigos marcados; una sola respuesta defendible por ítem; variantes de orden en `aceptadas`;
6. extensión de la lectura según la tabla; sin Ecuador; Lumo solo.

## Calibración (piloto N1 b01 y N6 b01, 06-10)

Antes de integrar: confirmar con las voces de-DE que Umlaut, ch (ich/ach), r vocalizada, longitud vocálica, «At», «Eszett» y «U-Umlaut» suenan según las guías.

**Trabajo en scratch:** usa solo tu carpeta `/tmp/claude-1000/-var-www-html/13f9b56f-c5b2-4793-9806-086c8576ca42/scratchpad/de/bloques/nX-bYY/` para scripts y borradores (hay autores en paralelo; nada de `build.py` o `lib.py` sueltos).

Reglas del piloto N1 b01:
1. **Direcciones, URLs, símbolos y cualquier cadena con «@ _ - / .»:** no entran como `respuesta`, `opciones` de tipo texto ni celdas `texto`. Se enseña y se evalúa la forma dicha (Punkt, At…). La forma escrita va en celdas `apoyo`, en opciones `{es,en}` o en la consigna. Motivo: el validador las parte mal, la app lee las celdas `texto` en voz alta y su normalización convierte «.» en espacio.
2. **Orden de enseñanza:** una palabra debe estar en `ejemplos`/`vocabulario` antes de la `tabla` que la trae; no uses en `ejemplos` formas que solo enseña la tabla posterior (p. ej. «U-Umlaut»). Comprueba con el validador cada vez que muevas un paso.
3. **`relacionar` con apoyo a la derecha:** las opciones de la derecha son un conjunto cerrado; cada forma de la izquierda debe tener una sola pareja dentro de ese conjunto aunque existan homónimos fuera (spielt = er/ihr). Si el conjunto no lo garantiza, dilo en la consigna.
4. **Guías de sonido:** copia las del encargo; no inventes reglas fonéticas propias («o + una consonante es larga» es falso; la longitud se enseña por «h» o vocal doble). En EN indica una palabra de referencia, no comparaciones de ortografía («mirror images»). Una explicación por sonido, sin mezclar guía y gramática.
5. **Consigna y `aceptadas`:** si la consigna fija el Vorfeld («empieza con X»), no pongas en `aceptadas` el orden alternativo; si quieres aceptarlo, quita la restricción.
6. **Idioma de apoyo:** revisa el EN por frases de traducción literal («a noun with no “a”», «mirror images»). Compara con el inglés solo cuando aclare (cognados, artículo ausente, V2). Traduce el metalenguaje (Umlaut, Eszett) por lo que es, no por un término español de otra cosa (diéresis).

Reglas del piloto N6 b01 (niveles B2–C1, situaciones largas):
1. **La situación se escribe a partir de la ficha pero no debe introducir verbos fuera de la clase en las preguntas/escribir.** Los ítems evaluables solo usan formas que aparezcan literalmente en `ejemplos` o `tabla` de la clase (aquí falló `rief … an` y `Stunde`); el autor debe grep-ear cada respuesta y cada `aceptadas` contra `ejemplos`/`tabla` antes de entregar.
2. **Todo `escribir` cerrado nombra en la consigna el tiempo verbal y las formas clave** («en Präteritum, con «war» y «begann»»). Sin eso hay tres respuestas defendibles (Präsens/Präteritum/Perfekt) y sinónimos (Oma/Großmutter).
3. **Las notas ⚠ de falso amigo se escriben desde el español**: «bekommen ≠ volverse», no «become». El inglés va solo en el campo `en`.
4. **Las explicaciones es y en deben ser equivalentes**: no añadir en español una frase extra (ej. «Ich bin der Meinung» en c04) ni dejar analogías en español que no se entienden; si una analogía no ayuda, se quita.
5. **Posición verbal en la explicación/feedback**: tras un bloque preposicional o subordinada en Vorfeld, nombrar «posición 1 / verbo en posición 2» (o «verbo en 1.ª posición» solo tras una subordinada completa). El piloto confundió ambas.
6. **Revisar `sonido` de la ficha contra el alemán real** antes de copiarlo (ER-ach-tens es erróneo) y reflejar el sonido de cada clase en una nota de `vocabulario` (el bloque lo hizo en todas; mantenerlo).

Nota de herramientas: el validador trata las palabras con guion como una sola («E-Mail», «U-Bahn»): enséñalas en `vocabulario` y úsalas con normalidad. El `relacionar` lleva alemán a la izquierda y apoyo {es,en} a la derecha.
