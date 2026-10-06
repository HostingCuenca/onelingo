GO

# Revisión independiente de N3 (B1), c01–c50 (plan de alemán, método ligero)

Revisor distinto del autor. `curriculo/de/n3.json` (50 fichas, `planificado`) contra `tools/curriculo/de/n3-outline.json`. Solo se editó `ejercicios`; campos del outline intactos.
Validadores tras las correcciones: `validar_plan_detallado.py de curriculo/de/n3.json` = 0 errores (701 ejercicios); `validar_plan.py de` = 0 errores. Script: `scratchpad/de/fichas/rev-n3.py`.

## Veredicto por criterio

1. **Alemán correcto:** sin errores de lengua graves (casos, relativos, genitivo, Konjunktiv II, pasiva, N-Deklination, Satzklammer, mayúsculas). Únicos fallos: «Es das Fotoalbum meiner Mutter» (falta «ist», c13), un distractor con «dem Zeug» (palabra real, c09) y «Immer wenn Jonas Bus fuhr» (c06). Corregidos.
2. **Una sola respuesta:** problema más frecuente (≈25 casos): `ordenar` con Vorfeld libre o inversión posible (c01, c02, c14, c15, c20, c35, c36, c37, c42, c46…), `relacionar` con dos emparejamientos válidos (c41 «alles/das Beste, was…», c44 «Ich hätte/wäre…»), `completar` con dos respuestas válidas (c10 ja/doch, c19 Wenn/Falls, c20 desto/umso, c48 daher/deshalb) y `escribir` abiertos (c16, c17, c37, c44). Se fijaron con consigna («empieza por…», «termina en…»), cue o cambio de ítem.
3. **Nada sin enseñar:** segunda fuente de errores (≈30 casos). Ver «Avisos»: Präteritum de verbos fuertes no enseñados, vocabulario de color y adelantos de clases posteriores. Sustituidos por formas/palabras ya vistas.
4. **Cobertura:** todas las claves de `introduce` se evalúan; c50 evalúa 9 claves del nivel con 4 formatos (sin cambios estructurales). c49 y c50 son integración (introduce vacío).
5. **Consignas es/en:** coherentes salvo: c13 (decía «Jonas» y el ítem Tom), c22 («documento» vs Antrag), c16 («soñaría con el viaje»), c49 («folias»). Corregidas.
6. **Lumo/Ecuador/personajes:** limpio. Nombres genéricos (Anna, Jonas, Lena, Frau Becker…) sin continuidad.

## Cambios (119 ediciones en 38 clases)

- **c01–c03:** orden fijo por «empieza por» (c01, c02); «das Papier» → «das Buch»; en c03 se quitó «bestand»/«riefen» (Präteritum fuerte no enseñado) usando «machte/sahen/erreichte».
- **c04:** consigna del `escribir` fija la persona (ich).
- **c05:** «glücklich» (no enseñado) → «geht es ihm gut» / «stolz».
- **c06:** «fuhr», «anrief» → «war», «ankam»; «den Zeugen» (N-Deklination, c09) → «Anna» / «den Unfall».
- **c07:** `escuchar` con clave perfekt-ieren-mixed ahora entrena esa clave (telefoniert/getelefoniert).
- **c08:** «stand» → «war».
- **c09:** «sprach», «rief», «half» (no enseñados) → «fragte», «hat angerufen»; distractor «dem Zeug» → «den Zeuge»; consigna fija Präteritum.
- **c10:** `completar` ja/doch ambiguo → `elegir`; `ordenar` con denn fijo al final.
- **c13:** «Es ist …»; consigna Tom. **c14, c15:** orden fijo («Arbeit» en vez de «Job»). **c16:** «frei», «Italien» → «Urlaub», «Mexiko/Spanisch»; `escribir` con sujeto coherente (ich) y verbo dado.
- **c17:** `escribir` sin ambigüedad (Vielleicht regnet es); «Stau», «Hunger» → palabras vistas.
- **c18:** «anzufangen/vorzubereiten» (zu en separables, no enseñado) → «da zu sein / fertig zu machen».
- **c19:** «dauert», «spazieren» sustituidos; `completar` Wenn con pista W.
- **c20:** desto/umso fijado; «Donnerstag», «übe», «probiere», «ruhiger» sustituidos; `ordenar` con «Zeit» fija.
- **c21–c24:** «Zuletzt» → «Am Ende»; `trotz` ilógico («Trotz des Streiks hat niemand etwas gesagt») reescrito; «Gutschein» (c25) fuera de c23/c24; «schlafe», «günstiger», «bezahlen» sustituidos; `escribir` con «Wegen» fijo.
- **c22:** consigna del orden. **c26:** distractor `escuchar` «hätte geschlafen» (Konjunktiv II pasado no enseñado hasta c44) → «würde ich weniger schlafen»; «isst» fuera. **c28:** «fehlt» (no enseñado) → «ist nicht da».
- **c31:** «Waren/Tür/geöffnet/bezahlt» sustituidos por «Geräte», «durch den Zug». **c33:** «fiel/ausfiel» (Präteritum fuerte) → Perfekt. **c34, c35:** orden fijo; «einfach» → «gut».
- **c36, c37:** órdenes y pronombre fijados (ihn). **c41:** distractor «das Beste, das» (también correcto) → «wo»; `relacionar` es→de unívoco. **c42:** orden fijo.
- **c44:** `ordenar` sin coma colgante; `relacionar` es→de unívoco; «hätte … kaufen sollen» (Ersatzinfinitiv, no enseñado) → «gern gekauft»; «genutzt» fuera. **c46:** orden de weder…noch fijo; «Halle» → «Schule».
- **c47–c50:** «sammeln», «wachsen», «zeichnet», «hoch», «halte», «üben/übte», «schrieb», «Verfasser», «aktiv» sustituidos; daher/dabei con consigna fija; «folias» → «diapositivas»; c50 «fast nie» → «rara vez».

## Notas de autores (comprobadas)

- c28/c29: «Ich glaube/weiß, dass…»: glauben (N2 c18) y wissen ya están enseñados; el orden es único. Sin cambio.
- c26: ver arriba (distractor sustituido). c33/c40: reciclaje ligero aceptado (c40 no evalúa ninguna clave de `recicla`; hueco menor).

## Sin resolver

- Outline: c13 «Vorfahre»; c42 cognados («Serie», «interessant») y c06 «Polizei/Polizist» (se enseñan en c08/c09) quedan como transparentes; el outline debería adelantarlos o no usarlos en la situación.
- c03/c04/c05: ninguna clase del nivel enseña el Präteritum de más verbos fuertes que las 8 de c02. Los bloques posteriores solo pueden usar esos 8, regulares, war/hatte/modales o Perfekt.
- Falsos amigos (Termin, Karte, Gift, Chef…) no están marcados con ⚠ en las fichas; recordarlo en los bloques.
- Verificación de audio de-DE pendiente.

## Avisos para autores de bloque

Errores frecuentes reales del nivel (`erroresFrecuentes`):
1. *«Als» / «wenn»* en pasado: *Wenn ich ankam, sah ich…* (hecho único = als; repetido = immer wenn).
2. *Verbo en 2.ª posición tras seitdem/als/während/bevor/obwohl/damit/falls* (*obwohl ich bin müde*) y *trotzdem/daher + verbo final*.
3. *Plusquamperfekt con auxiliar equivocado*: *nachdem ich gegessen war* / *angekommen hatte*.
4. *Pasiva: «wurde» + infinitivo, «durch» con persona* (*von* con personas, *durch* con medios).
5. *N-Deklination*: *den Kollege, mit dem Zeug*.
6. *Relativo equivocado*: *Das Beste, das ich sah* (usar was), *der Verein, deren…*, *die Stadt, was…*.
7. *Genitivo con -s en femenino o plural*: *der Mutters*; *Annas* sí, *Marias*; *wegen dem*.
8. *«ohne/um/statt … zu» con sujeto distinto* (*um er pünktlich zu sein*), *zu antes del prefijo separable*: *aufzustehen*.
9. *«brauchen» sin zu*: *Du brauchst nicht kommen*.
10. *Konjunktiv II*: *Wenn ich hätte Zeit*, *Ich wäre gegangen* con hätte/wäre mezclados, *würde* + haben/sein.
11. *Comparativo atributivo sin terminación*: *ein besser Ergebnis*.
12. *Ordenar*: evitar «Fronting» libre (Vorfeld) sin fijar con «empieza por…»; evitar adverbios móviles (*sofort, wohl, gern, rechtzeitig, heute*).
13. *Palabras y formas no enseñadas colándose*: Präteritum de verbos fuertes distintos a los 8 de c02, zu + separables (*anzufangen*), Konjunktiv II pasado antes de c44, «Gutschein/Verkehr/Stau/Hunger/frei».
