GO

# Revisión de de.n5 B6 (c26–c30)

Validador (cadena con el n5-b05.json real): `validar_bloque.py de 5 6` -> 0 errores del bloque, antes y después de las correcciones. Situaciones (palabras): c26 303, c27 299, c28 309, c29 296, c30 300 (mínimo con margen N5: 292). Sin Ecuador/Lumo; nombres (Becker, Wolf, Berger, Anna, Jonas) todos de NOMBRES_LIBRES. Alemán y morfología revisados a mano (Konjunktiv I: habe/sei/komme/könne/werde/gebe/wirke; auxiliar haben/sein; hätten/würden; zufolge y gemäß + Dat., nach Angaben + Gen.; tablas de Dat./Gen. correctas).

## Cambios

- **c26** (diálogo, Herr Wolf): «sie habe das Interview gelesen» era Konjunktiv I de pasado (contenido de c27, adelantado); ahora «sie sei mit dem Interview zufrieden» (es/en ajustados).
- **c26** (diálogo): «wann das sei» (pregunta indirecta con Konj. I, no enseñada) pasa a «wann». Dos turnos seguidos de la Moderatorin fundidos en uno y quitado el «cuando sepamos más, volveremos a hablar…», que sonaba a cierre a mitad de diálogo.
- **c27** (`v9`, «der Leiter»): quitado el ⚠. No es falso amigo (Leiter ~ líder/leader): la nota normal explica que «der Leiter» (persona) y «die Leiter» (escalera) se escriben igual y solo cambia el género; la mujer es «die Leiterin» (es/en).
- **c27** (explicación, es/en): «Ich hatte… se resumen igual» era incompleto (sin participio); ahora solo «Ich habe das Problem erkannt» y «Ich erkannte das Problem».
- **c27** (ejemplos): «Er sagte, er habe gesagt, das Problem sei wichtig» (cita dentro de cita, forzada) -> «Er sagte, er habe gestern gearbeitet.» (forma ya en la tabla p2).
- **c27** (diálogo): «Das Problem ist früh erkannt worden» (pasivo de Perfekt, no enseñado) -> «Er hat das Problem früh erkannt»; quitado «Das ist sicher»; dos turnos seguidos de Frau Becker fundidos.
- **c28** (explicación, es/en): «En singular el Konjunktiv I se ve bien» es solo cierto en 3.ª persona (ich habe = indicativo); precisado. Frase de «sein»: «seien» ya se distingue de «sind» y no necesita sustituto; «wären» queda como nota hablada sin evaluar (el nuevo texto lo dice así).
- **c28** (`v8` «die Mehrheit»): la nota sobre la «h» era ambigua («h tras vocal no suena» con «hait» escrito); ahora distingue la «h» de «Mehr» (muda, alarga) de la de «-heit» (se pronuncia).
- **c28** (diálogo): dos turnos seguidos de Herr Wolf fundidos; «Mucha gente quiere eso» -> «Muchos empleados quieren eso» (fiel al alemán).
- **c29** (diálogo, es): «Es un avance» -> «Eso está bien» (traducía de más «Das ist gut»).
- **c30** (ejemplos y diálogo, es/en): «Die Quelle wird in der Zeitung zitiert» (pasivo de presente) se presentaba como reciclaje de c23, pero B5 c23 solo enseña el pasivo en Präteritum; ahora «Die Zeitung zitiert die Quelle.» (activa).
- **c30** (diálogo): «Danke.» a mitad de diálogo quitado (el cierre «Danke für die Hilfe» queda al final); dos turnos de Herr Wolf fundidos.

## Puntos del encargo (comprobados)

- Reciclaje de B5 (c30 «doppelt so hoch», «das Vorjahr», «das Prozent», «der Anteil», «sinken/steigen», «gesunken», «Erkrankung», c29 «Medikament/Nebenwirkung/Risiko/Dosis»): todo existe en ejemplos, tablas o vocabulario del n5-b05.json real. Lo único que no estaba (pasivo de presente) ya está quitado.
- `escribir` de transformación (c26 i1/e4, c27 i1/e4, c28 i2/e4, c29 i3/e4, c30 i2/e4): todos traen la frase de partida en la consigna, el verbo/auxiliar y «sin dass» o la estructura exigida.
- ⚠ Chef (c28): correcto. Los demás ⚠ del bloque no existen: Leiter sin ⚠ (ver arriba).
- c28: la explicación es correcta (Konjunktiv II solo cuando el I coincide con el indicativo; «würden + infinitivo» por defecto; «kämen» literario; «seien» propio) y no adelanta nada (no se evalúa «seien» ni «wären»).
- `relacionar` (c26 i3, c27 i3, c29 i1, c30 i3): alemán a la izquierda, apoyo {es,en} real a la derecha, una sola pareja por forma.
- `aceptadas` de Vorfeld alternativo (c26 i1/e3, c27 g3/e3, c28 g3/i2, c29 g3/i3): gramaticales y compatibles con el «empieza con…» de la consigna.

## Sin resolver

- Corregido tras la revisión: `contexto.es` de c26, c27 y c28 estaba en alemán; ahora en español (y «presentadora» en c26, c29 y c30, fiel a «host»).
- Nada bloqueante. Pendiente general del nivel: confirmar con las voces de-DE el audio de ch, Umlaut (ä en hätten/wären/gemäß), r vocalizada y ß antes de integrar.
- Menor: formas flexionadas de los verbos separables o de ergänzen/festhalten en diálogos («ergänze», «halten … fest») no están literalmente en tablas (el validador no las marca; solo ocurren en diálogo, no en ítems).
- Menor: «Protokoll» (acta) comparte forma con «protocolo/protocol»; no se marcó ⚠ al no estar en la lista de falsos amigos del nivel.
