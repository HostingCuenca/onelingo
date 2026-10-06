GO

# Revisión independiente de N1 c11–c50 (plan de alemán, método ligero)

Revisor distinto del autor. `curriculo/de/n1.json` (c11–c50, `planificado`) contra `tools/curriculo/de/n1-outline.json`, `f0.json` y el vocabulario acumulado de c01..cN. c01–c10 siguen con el acta `revision-piloto-n1.md`. Solo se editó `ejercicios`; campos del outline intactos.
Validadores tras las correcciones: `validar_plan_detallado.py de curriculo/de/n1.json` = 0 errores (50 clases, 708 ejercicios); `validar_plan.py de` = 0 errores. Script: `rev-n1.py` (scratchpad), 40 ediciones puntuales en 24 clases.

## Veredicto por criterio

1. **Alemán correcto:** sin errores de lengua en las 40 clases (género, acusativo/dativo, Verbklammer, separables, imperativos, Perfekt con sein/haben, mayúsculas, ß/ä/ö/ü). Solo había un adjetivo declinado fuera de lugar (c48 «ein schöner Ausflug») y «Ich habe halb neun» (c26), calco ambiguo. Corregidos.
2. **Una sola respuesta:** había 1 `ordenar` con dos órdenes (c45 «Lieber Tee oder Kaffee?» / «Kaffee oder Tee»), 1 `ordenar` con dos adjetivos permutables (c31 «klein und schlank»), 1 `completar` con dos respuestas (c29 dann/danach), 1 `relacionar` con par discutible (c49 seit↔hace) y varios `completar`/`escribir` donde otro verbo o un adverbio también valía (wollen/möchte en c39 y c45; dürfen/können en c40, c41, c47; gehen/fahren en c42 y c49; «leider» en c45; falta de «empieza con Hier» en c40). Corregidos (consigna con el verbo, o ítem cambiado).
3. **Nada sin enseñar:** fuente principal de fallos, como en el piloto. Plurales antes de c14 (Kinder, Brüder en c12/c13), «meinen» (acusativo posesivo) en c43, «warum» en c44, «schade» como distractor en c44, «weiter» en c49, «lange/einen Tag» en c48, Schokolade→Tee (c39), «fängt» (cambio vocálico con separable, c35), «schön» antes de c25 (c23), «mit Karte» (dativo, c22), «Okay» (c43), «Gitarre» (c47). Sustituidos por léxico y gramática ya vistos.
4. **Cobertura:** cada clave de `introduce` tiene ≥ 5 ítems en 3 formatos o más; c50 cubre 10 claves del nivel en 5 formatos. Reciclaje (huecos menores, no tocados): c11 sin `email-address`/`moegen-present`; c12 sin `moegen-present`; c15 sin `countries-languages`; c20 sin `spelling-applied`/`doch-answer`; c21 sin `welch-question`/`doch-answer`/`numbers-0-12`/`noun-plural`; c25 sin `introduce-self`; c26 sin `false-friends-basic`; c28 sin `moechten-bestellen`/`time-of-day-greetings`; c29 sin `prices-paying`/`courtesy-danke-bitte`. No bloquea.
5. **Consignas:** corregidas 3 que contradecían el ejemplo (c47 «yo/fútbol» vs «wir/Gitarre»; c50 «tu edad, 28» vs «Anna/30»; c50 «empezando con Ich» vs «Wir…»), 1 ambigua (c32 «qué edificio es el de la pregunta») y varias con verbo no fijado.
6. **Sin Lumo/Ecuador/personajes con continuidad:** comprobado (Anna, Jonas, Lena, Felix, Herr Wolf, Frau Becker/Berger solo como etiquetas).

## Cambios por clase

- c12: «Wir sind drei Kinder» → «drei Geschwister»; evaluación sin Brüder/Kinder (ihr habt zwei Schwestern; wir haben einen Bruder; Jonas und Lena haben einen Bruder).
- c13: «Meine Eltern haben eine Tochter» (antes «zwei Kinder»).
- c14: situación y ítem wohnen-in con «Seine Brüder» (antes «Die Brüder», sin dueño).
- c22: distractor «Karte» (antes «mit Karte», dativo); consigna de «Die Rechnung, bitte» fija artículo + bitte.
- c23: ítem sin «schön» (adelantado de c25).
- c26: «Es ist halb neun!» (antes «Ich habe halb neun»); sin «also».
- c29: independiente 2 pasa de `completar` (dann/danach) a `elegir`.
- c31: `ordenar` con «ziemlich schlank» (orden único).
- c32: consigna de la pregunta de situación.
- c35: separable «Ich rufe Lena heute ___ → an» (antes «fängt», cambio vocálico).
- c39: «200 Gramm Tee»; consigna «con wollen».
- c40: consignas «con dürfen» en 2 ítems; `escribir` con «empieza con Hier».
- c41, c47: consigna «con dürfen» (también valía kann).
- c42, c49: consigna «con gehen» (también valía fahren); c49 sin «weiter».
- c43: «den Schlüssel» (antes «meinen»); «Ja, gern!» en lugar de «Okay!».
- c44: sin «Warum?»; distractor «Nein, ich habe keine Zeit» (antes «Schade…»).
- c45: `escribir` sin «lamentablemente»; `ordenar` nuevo con orden único; consigna «con wollen».
- c47: `escribir` coherente consigna/ejemplo (wir / Fußball).
- c48: situación sin adjetivo declinado ni «lange»; «Der Ausflug war schön».
- c49: `relacionar` con «desde hace / hace (pasado) / desde cuándo»; situación coherente (Herr Wolf llegó hace dos años).
- c50: `escribir` edad de Anna en letras (dreißig); `escribir` Perfekt «nosotros bebimos té».
- Sin cambios: c11, c15–c21, c24, c25, c27, c28, c30, c33, c34, c36–c38, c46.

## Sin resolver

- Outline c16: «Bus» solo se enseña en la `tarea`, no en `vocabulario`; se dejó en situación/ítem porque la tarea lo trabaja.
- Outline c27: `vocabulario` enseña «im Januar» pero la `gramatica` pide «im Mai»; el bloque debe dar al menos tres meses.
- Outline c17/c21/c22: el dativo en bloque fijo («in der», «mit der U-Bahn», «Haben Sie das in Größe 38?») aparece antes de c34; el bloque debe presentarlo como fórmula.
- Reciclaje con claves no usadas (ver criterio 4); aceptado como en el piloto.

## Avisos para autores de bloque

1. Plurales no enseñados hasta c14 (Kinder, Brüder, Eltern solo como tal): no usarlos en c11–c13.
2. «möchte/will» y «darf/kann» son intercambiables para el hispanohablante: la consigna fija el verbo («con wollen», «con dürfen») y el ítem lo comprueba.
3. `erroresFrecuentes` reales de c11–c50: *Ich habe 19 Jahre (c11); *Das ist mein Mutter (c13); *Ich habe ein Hund (c15); *Ich bin nicht müde / kein müde (c18); *Ja, ich komme nicht tras pregunta negativa (c19); *Welche Bus / Welcher Nummer (c20); *Ich möchte einen Kaffee, bitte? vs «hätte gern» (c21); *Ich nehme der Pullover (c23); *Der Rock ist zu kurz sein / klein zu (c24); *Ich nehme ihn die Jacke (c25); *Es ist halb acht = 7:30 (c26); *Ich stehe auf um sieben (c28); *Am Abend ich koche (c29); *Am gern / liebste (c30); *Es gibt ein Park (c33); *Ich bin in dem Park / im Schule (c34); *Ich kann zu schwimmen (c36); *Du muss (c37); *Du will (c38); *Hier dürft man (c40); *Ich fahre zu Hamburg / nach Arzt (c41); *Gehen Sie rechts an (c42); *Du kommst! / Nehm! (c43); *Ich habe Lust zu gehen ins Kino (c44); *denn muss ich arbeiten (c45); *Ich habe war / Ich bin gewesen (c46); *Ich habe gekochen / Ich habe gesehen einen Film (c47); *Ich habe nach Hause gegangen (c48); *Ich wohne vor zwei Jahren (c49).
4. Falsos amigos para marcar con ⚠: Termin (c37, cita, no «término»), Karte (c22, tarjeta/carta/entrada), Rock (c23, falda, no «rock»), Handy (c14, móvil), bar (c22, «en efectivo», no «bar»), Bank (c34, banco y banca).
5. Situaciones con 3+ hablantes: etiqueta «Nombre:» en cada línea (ya cumplido en todas) y sin línea de escenario en alemán.
6. `ordenar`: evitar pares permutables (Tee/Kaffee, klein/schlank, heute/zusammen); con la primera palabra en mayúscula el Vorfeld queda fijo.

## Formato de ficha

Suficiente. Una mejora barata para el validador: avisar cuando una consigna con `completar` pida un verbo modal sin nombrarlo (wollen/möchten, dürfen/können, gehen/fahren).
