GO

# Revisión independiente de N2 (alemán, método ligero), c01–c50

Revisor distinto del autor. `curriculo/de/n2.json` (50 fichas, `planificado`) contra `tools/curriculo/de/n2-outline.json`, f0 y N1 completo. Solo se editó `ejercicios` (campos del outline comprobados idénticos antes y después).
Validadores: `validar_plan_detallado.py de curriculo/de/n2.json` = 0 errores (701 ejercicios, 701 ejemplos únicos); `validar_plan.py de` = 0 errores. Script: `scratchpad/de/fichas/rev-n2.py`.
Cambios: 48 clases tocadas, 220 ítems o situaciones modificados (+ normalización del separador « / A)» en los `escuchar` que no lo tenían). Sin cambios: c06, c14.

## Veredicto por criterio

1. **Alemán:** correcto en casi todo (reflexivos, V2, weil/dass/wenn, declinaciones, Perfekt, comparativos, werden, zu+infinitivo, dativo/acusativo). No hay errores de lengua graves. Corregidos: «Annas/Jonas' Handy» (genitivo no enseñado) y un diálogo que mezclaba du y «Schicken Sie» (c04); el resto de problemas eran de ambigüedad y de consigna (ver 2 y 5).
2. **Una sola respuesta:** el defecto más frecuente (unos 40 ítems). `ordenar` con Mittelfeld/Vorfeld libre (adverbio de lugar o tiempo movible: «weil um acht der Zug…», «Ich habe im Bus etwas vergessen», «Sie nehmen dreimal täglich…», «Ich werde bald Deutsch…», «Kann ich hier den Koffer lassen?»), `escribir` sin ancla («empieza con…»), `completar` con sinónimo posible (deshalb/deswegen c20, wird/ist c17, soll/kann/darf c42/c36), `relacionar` con dos asignaciones razonables (c15, c37). Corregidos fijando inicio, quitando el adverbio o precisando la consigna.
3. **Nada sin enseñar:** segunda fuente de errores. Sustituidos por léxico ya visto: Kiste, Bett, Fleisch, Suppe, Salat, Zwiebeln-ejemplos, Käse, Geld, Foto, Treppe, Dienstag/Sonntag, Wetter, Kellner/Gast/Passagier (etiquetas de hablante), Entschuldigung-sin-necesidad, Wofür, Interesse, Fenster, Laden, Bibliothek, Hof, WG, Touristeninformation, Dom, Reisebüro, Betreff, lauf-, leise, leer, schnell, viele, diesen, gegen, «Sei» (imperativo de sein), mir/ihn adelantados, bleibe, pünktlich, Trainer, Klasse, Preis, günstig-Laden. Se quitaron las líneas de escenario en alemán con palabras no vistas (c32, c34, c36, c41–c45, c47).
4. **Cobertura:** cada clave de `introduce` tiene ≥ 2 ítems de evaluación en todas las clases; c49/c50 integran ≥ 8 claves y ≥ 3 formatos (c50: 8 ítems, 6 formatos).
5. **Consignas es/en:** 20 consignas contradecían el ítem (tú/ich c04, c32; «ustedes» con wir c04; «cabeza» con Bauch c43, c50; «pescado» sin pescado c27; «el técnico» con Herr Wolf c20; «soja» por salsa c29; «llavero» por llave c41; «tumbado» c12; «ancho/grande» c24; «alegrarse» c40). Corregidas.
6. **Sin Lumo/Ecuador/continuidad:** limpio. Nombres genéricos (Anna, Jonas, Lena, Max, Frau Becker) como etiquetas; sin hechos que se arrastren.

## Léxico simple señalado por el encargo (comprobado contra N1/f0)
- Sí enseñados: müde (f0), Tee (N1 c10/c21), Montag (N1 c27), Wasser (N1 c21), vielleicht (N1 c45), Flughafen (N2 c08, en su propia clase). Sin cambios.
- No enseñados en N1/f0: **Dienstag** (y Donnerstag); en N1 solo Montag, Mittwoch, Freitag. Sustituido por Mittwoch/Freitag en c17 y c38 y por Mittwoch en c45. «viele» (c02) sustituido.

## Cambios por clase (resumen)
- c01 e2 (consigna/pregunta Sie), e6 (opciones ambiguas). c02 g2 (plural), i1/e4 (orden), sit (viele, Dienstag), e6 (Kollegin adelantada). c03 e4, e6. c04 sit (du/Sie, an+Dat, ihn), i1, e3 (dos órdenes), e4. c05 g2 (bleibe), i1, i2 (key ihr con wir), i3, sit, e3 (dos órdenes), e4.
- c07 sit (mir, gearbeitet). c08 sit (Flugzeug). c09 e4 (tú/ich), e6. c10 e4. c11 i1, sit, e3, e4, e6 (Kiste, Bett, steht/Sofa antes de c12). c12 i1, i3, e4. c13 i1, sit, e3 (Information, Haus). c15 i3 (relacionar ambiguo), e3. c16 g2, e1 (reisen). c17 sit (Wetter, Dienstag), q1, q2, e6 (wird/ist).
- c18 sit/e4 (Plan antes de c19). c19 sit, e2. c20 g1, q2, e2, e4 (deshalb/deswegen). c21 i2, i3, e2, e5 (Annas, declinación «billigere» adelantada). c22 g2, i3, sit, e1. c23 i3, sit, q2, e2 (Mantel), e3. c24 g3 (neu), i3 (Kleid), sit, q2, e1, e4. c25 g2, sit (diesen, denn), q2, e3, e5. c26 i2, i3, sit, e1, e2, e5 (Salat, Zwiebeln, Käse, meinen, wie viele).
- c27 g1, g2, i1, i2, sit, q1, e1, e3, e4, e5 (Fleisch/Fisch/Salat/Suppe antes de c28). c28 i2, sit, e3. c29 i1, i2, sit, q1, q2, e1, e4, e5. c30 g1, g2, i1, i3, sit, q1, q2, e3. c31 e1, e3, e4 (pünktlich, hält). c32 i1, i2, sit, e3, e5. c33 sit (schnell). c34 i2, sit. c35 sit (Passagier).
- c36 sit, e3, e6. c37 i3, e5. c38 g3, i1, sit, e2, e3, e6. c39 sit, e1, e6. c40 i2, sit, q2, e1, e3, e5. c41 i1, i3, sit, e1, e2, e5, e6. c42 g1, sit, e3, e5, e6. c43 g2, sit, q2, e3, e4, e6, e7.
- c44 sit, q2, e3. c45 g1, sit, q1, e3, e4, e5. c46 g3, sit, q2, e2. c47 g3, i1, i2, sit, e3. c48 g1, g2, sit, e1, e3, e4, e5. c49 g1, i1, sit, q1, q2, e1 (beginnt, Dom, punto de encuentro vs. cine). c50 i1, i3, sit, e1, e2.
- Transversal: 21 `escuchar` (c21+) sin « / A)» tras el audio, normalizados.

## Sin resolver
- Outline c48/c49/c50: `recicla` con 12–14 claves (parece copiada); es inabarcable en 6–8 ítems, no es error de ejercicios. c49 tiene `introduce` vacío igual que c50 (aceptado por validador).
- Outline: palabras de vocabulario ya vistas en N1/N2 (das Jahr, das Problem, vielleicht, absagen/verschieben repetidos en c19–c20, bequem en c24 pero usado antes). Sin impacto.
- Participios fuertes no listados en ninguna clase: gefunden, abgegeben (c48), gebrochen (c39), gesprochen/gewaschen (evitado/aceptado). El bloque debe enseñarlos como bloque léxico.
- «fliegen» (c08) solo aparece como participio geflogen en N1 c48; se mantiene por ser el tema del viaje; el bloque debe enseñar el infinitivo.
- Falsos amigos por marcar con ⚠ en el bloque: Termin (cita, no «término»), Karte (carta/tarjeta/mapa), Rezept (receta médica o de cocina).

## Avisos para autores de bloque (erroresFrecuentes reales del nivel)
1. Reflexivo en acusativo/dativo: *Ich dusche mir, *Ich putze mich die Zähne, *Er beeilt mich; Sie con sich.
2. Adverbio de frecuencia y V2: *Ich oft arbeite, *Manchmal ich habe.
3. weil/dass/wenn con verbo final y separables: *weil ich bin krank, *weil ich fange an, *dass er ruft an; coma obligatoria.
4. Perfekt: *geaufräumt, *gevergessen, *gefotografiert (ge- en separables/inseparables/-ieren); haben/sein.
5. Präteritum modal: *Ich habe nicht konnte; solo war/hatte y modales (resto en Perfekt).
6. Wechselpräpositionen: wo?+Dativ / wohin?+Akkusativ: *Ich gehe in der Küche, *Ich bin in die Küche; stellen/stehen, legen/liegen, hängen.
7. Dativ vs. Akkusativ con helfen/danken/gehören/gefallen; *Ich helfe die Nachbarin; *Die Wohnung gefällt ich.
8. Comparativo con als/wie: *größer wie, *so größer wie, *mehr gut; superlativo *am meisten besten.
9. Declinación del adjetivo: *Der rote Pullover/den roten, *ein neuer Hemd; sin artículo: frischer Fisch / mit frischem Gemüse.
10. Orden con pronombres: *Ich gebe dir es, *Ich bringe Anna ihn (pron. acusativo antes del dativo nominal).
11. nicht müssen ≠ nicht dürfen (no hace falta ≠ prohibido); sollte-advice: *Du sollte.
12. Mir ist kalt / Mir tut der Kopf weh (no *Ich bin kalt, *Mich tut…). Wissen Sie, ob + verbo final (*ob fährt der Zug).
13. zu+Infinitiv separable: *zu anrufen → anzurufen; zum+verbo nominalizado con mayúscula (*zum lernen).
14. Falsos amigos y morfología: Termin, Chef, Karte, Rezept; ß vs. ss (heiß, größer, Straße).
