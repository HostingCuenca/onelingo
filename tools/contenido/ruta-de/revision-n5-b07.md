GO

# Revisión N5 B7 (de.n5.c31–c35) — revisor distinto del autor

Validador `validar_bloque.py de 5 7` (encadenado con n5-b06.json): 0 errores del bloque.

## Cambios por clase

- **c31**
  - g1: la consigna decía «supuesto» (colisiona con vermeintlich); ahora «llamado» (con ironía). Se quita la letra inicial, que ya no hacía falta.
  - e2: la letra «m» hacía trivial el ítem; ahora «presunto», femenino nominativo (lo que se evalúa es la terminación).
  - i2: se añade «sin dass» (la consigna fija «Die Sprecherin sagt,», así que había otra respuesta con dass).
  - e4: faltaba la frase de partida; ahora «Die Zahl ist hoch.» con «sin dass» y «sei angeblich hoch».
  - «nichtseriös»: el error real se mantiene (distractor de i3 y erroresFrecuentes); la explicación y el feedback dicen que lo correcto es «unseriös» o «nicht seriös» (dos palabras).
  - Tabla «Marcas de distancia»: la fila de comillas tenía las columnas descolocadas; se reordena.
  - `contexto.es` estaba en alemán; ahora en español.
- **c32**
  - La nota ⚠ de Handy se reescribe desde el español («≠ práctico»). Es el único ⚠ del bloque.
  - `contexto.es` estaba en alemán; ahora en español.
- **c33**
  - Explicación: «en una oración principal enunciativa» (V2 no es absoluto).
  - g1: `aceptadas` con el otro orden válido (objeto antes del sujeto, «den» inequívoco).
  - e4: la consigna fija «sujeto antes del objeto» (una sola respuesta).
  - i3: la consigna pide la conjunción que corrige lo negado («sino»), para excluir «aber».
  - Tabla de casos: «Das Foto zeigt die Agentur» era ambiguo y absurdo; ahora «Das Foto kritisiert der Sender.»
  - Diálogo: línea de Frau Becker sobre el portavoz sin sentido; se reescribe.
  - `contexto.es` estaba en alemán; ahora en español.
- **c34**
  - Explicación de «hingegen» corregida: posición 1 (menos frecuente), tras el sujeto en el Vorfeld, o en el Mittelfeld. Se añaden dos filas a la tabla de conectores y un ejemplo en Mittelfeld («Der Sender zeigt hingegen Bilder.»).
  - Se quita la frase que mezclaba «wohingegen» con el imperativo.
  - erroresFrecuentes 3 («aber … hingegen»): ya no se afirma que sea agramatical; se dice que es redundante.
  - e1: el feedback era falso («dagegen» también puede ir en posición 1); se corrige y la consigna fija el verbo en 2.ª posición.
  - e2: «(no während)» para evitar la respuesta alternativa.
  - e4: la consigna dice claramente que la primera frase ya está escrita y que se responde solo con la segunda.
  - `contexto.es` estaba en alemán; ahora en español.
- **c35**
  - e4: la consigna añade el participio «beschlossen».
  - erroresFrecuentes 3: «hat beschlossen worden sein» no era un error realista; ahora «…worden» (falta «sein»).
  - Texto de la tabla (decía «tres pasos» y hay cuatro filas).
  - Diálogo: «kann … abgelehnt worden sein» (modal no enseñado) pasa a «soll»; se quita «Dann machen wir das morgen».
  - `contexto.es` estaba en alemán; ahora en español.
- **Diálogos c33, c34, c35:** se fusionan los turnos consecutivos del mismo hablante. Extensión final: c31 321, c32 306, c33 311, c34 296, c35 306 palabras (mínimo con margen 292).

## Comprobaciones sin cambios
- Reciclaje de B6 (zufolge c30; «sei» c26–29; «habe» c26–29): todo está de verdad en n5-b06.json. No hay ítem que dependa de algo que B6 no enseñe. «sei … worden» (Konjunktiv I pasivo) solo aparece como ejemplo en c35, sin evaluarlo.
- Léxico de las tablas «Para leer» (Meldung, Branche, Agentur, Regierung, Sender, Medien, ablehnen): cada palabra se enseña en una tabla, vocabulario o ejemplos antes de evaluarse.
- Morfología revisada a mano en todas las respuestas, opciones y diálogos: sogenannte/mutmaßliche, Dem Faktencheck zufolge, erwies/erwiesen, den/der de c33, worden/bestätigt/überprüft, Medium-Medien, etc.
- Todas las transformaciones `escribir` traen ahora su frase de partida en la consigna.
- Sin Ecuador, sin Lumo, nombres solo de la lista permitida.

## Sin resolver
- Las pistas de letra inicial se mantienen solo donde desambiguan sinónimos (c31 s1 «v»: vermeintlich/angeblich; c34 g1 y s1 «h»: hingegen/dagegen).
- Falta la verificación de voz de-DE (Umlaut, ß, ch) antes de integrar, como indica la Calibración.
