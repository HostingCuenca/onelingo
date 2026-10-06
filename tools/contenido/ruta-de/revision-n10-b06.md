GO

# Revisión N10 B6 (de.n10.c26–c30)

Validador: `validar_bloque.py de 10 6` = 0 errores (cadena con el n10-b05 real). Situaciones: c26 416, c27 402, c28 399, c29 396, c30 397 palabras (mínimo con margen 390).

## Cambios por clase
- Reciclaje de B5: comprobado por script contra el n10-b05.json real. Ninguna palabra de B6 depende solo de B5 salvo «liefert» (c26, diálogo de Frau Berger); se reformuló a «…die großen Firmen auch am selben Tag liefern?» (forma ya enseñada en la tabla de lectura de la propia clase). Sin otras referencias a clases de B5.
- c26: diálogo reordenado (las dos preguntas seguidas de Frau Berger fundidas en un turno; «Vielen Dank für Ihre Zeit» pasó del medio al cierre de Jonas, antes de la despedida). Consigna s2 «vive» -> «está». Quitada de `aceptadas` la variante con cifra «50 Prozent» (e6 pide la cifra en palabras).
- c27: título en palabras («fünfzigtausend»). e5 (Futur I) ahora trae la frase de partida «Die Rendite wächst im dritten Jahr.» (faltaba). e1: las dos opciones llevan «das Geschäft» (antes «um zu skalieren» sin objeto). ES: «les digo» (Wolf habla a los dos).
- c28: «Und wenn wir ein Auto brauchen…» no coincidía con la traducción (dinero) -> «Geld brauchen». Quitado el doble matiz «Im Zweifel … notfalls». «der Partner springt ab» (abspringen, no enseñado) -> «der Partner fällt aus». ES: «por la noche», «¿Cuánto tardan…?».
- c29: «Ich habe die Idee gehabt» -> «Ich hatte die Idee». «gemeinsame Entscheidung» -> «es, gemeinsam zu entscheiden». «Alle Entscheidungen fallen gemeinsam» -> «Alle entscheiden gemeinsam». ES/EN de Frau Schmidt alineados con el alemán (no «contrato de socios»). Título EN «Shares and a say». Añadida una frase en el cierre de Anna.
- c30: «Tabelle 2» -> «Tabelle zwei» en todo el alemán (ejemplos, e6). Quitados «vorlesen» y «mitschreiben» (separables no enseñados) y «unseres Vertrags» -> «des Vertrags». Añadido turno de Frau Berger entre dos turnos seguidos de Herr Wolf. e1: el distractor «Der Vertrag in Kraft am ersten Mai tritt» era absurdo -> «Der Vertrag treten am ersten Mai in Kraft» (error real de conjugación). Error frecuente «tritt in Kraft am ersten März» (defendible en alemán) -> «*am erste März» (terminación del ordinal).

## Verificado sin cambios
- Puntos del autor: cifras y fechas en palabras (fünfzigtausend, zweihunderttausend, «am ersten März», «fünfzig zu fünfzig», Tabelle zwei); sin dígitos en ningún texto alemán. Cita c28 «Laut Weber … zehn Prozent» sin año. `escuchar` c28–c30 con opciones en alemán parafraseado. c30: «sei» solo en tabla de lectura y explicación; no se evalúa.
- Todos los `escribir` de transformación traen la frase de partida (c26 e5/e6, c27 e5/e6, c28 i1/e5/e6, c29 i1/e6).
- Morfología revisada a mano contra tablas/ejemplos: ist gestiegen, würde/würden/würdest/würdet, springt (ein), größere (Akk. fem.), festgelegt, tritt, ersten/dritten, neuen (Akk. masc.), Anteile/Rollen/Fälle.
- ⚠ solo en «bekommen» (c26; contraste desde el español: ≠ «volverse») y «Termin» (c28; ≠ «término»). Sin Ecuador, sin Lumo, nombres de NOMBRES_LIBRES.

## Sin resolver
- Prosodia/voz: «Plan B», «Prozent», cifras largas (zweihunderttausend) y «sich verpflichten» conviene escucharlos con la voz de-DE antes de integrar.
- «Der Zielmarkt sind Familien» (concordancia con el predicado plural) viene de la ficha; es correcto pero conviene que lo valide un nativo.
