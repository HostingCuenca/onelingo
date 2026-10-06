GO

# Revisión independiente de N9 (alemán C1 profesional, c01–c50)

Revisor distinto del autor. `curriculo/de/n9.json` (50 fichas, `planificado`) contra `tools/curriculo/de/n9-outline.json`.
Validadores tras las correcciones: `validar_plan_detallado.py de curriculo/de/n9.json` = 0 errores (680 ejercicios, ejemplos únicos); `validar_plan.py de` = 0 errores.
Campos congelados del outline: comprobados idénticos antes/después. Solo se editó `ejercicios` (≈122 cambios, ver abajo). Script: `scratchpad/de/fichas/rev-n9.py`.

## Veredicto por criterio

1. **Alemán correcto:** muy limpio. Solo 2 errores de lengua reales: «Tausenden Firmen» (c07, debía ser «Tausenden von Firmen») y comillas «…» en texto alemán (c15, c18; ahora „…“). Una consigna con categoría gramatical errónea en 5 ítems (preposición/verbo/sustantivo mal rotulados: c04 i1, c07 i1 y e1, c19 e1, c41 e1). Distractor dudoso en c28 g1 («Zufolge der Umfrage» es admisible en registro formal): sustituido por un error de caso.
2. **Una sola respuesta:** era el problema mayor. Corregidos: `completar` con 2+ respuestas válidas (denn/eigentlich c01, c41, c50; genauso/ebenso/ebenfalls c02; weil/da c03; verantwortlich/zuständig c03; Zunächst/Zuerst/Anfangs c06 y c12; Plötzlich/Dann c06; wussten/wissen c07; mal/doch c42; laut/gemäß/nach c28; unter-/verboten c37, c38; anbei/andernfalls/sonst c40; nachweisen/belegen c25; überprüfen/prüfen c39; steigern/erhöhen c21); `escribir` demasiado abiertos (c12 e3 y c24 e3 pasados a `ordenar`; el resto fija el arranque o el verbo en la consigna); `ordenar` con dos órdenes válidos (c13 e2, c45 g2, c48 g2, c17 vocativo, c10 i0); `relacionar` ambiguos (c01, c22, c23, c25) y ejemplos incoherentes con la consigna (c06 e3 duplicaba g2; c08 sq1 duplicado y mal atribuido, reemplazado).
3. **Nada sin enseñar:** a C1 el criterio es laxo; no se halló gramática adelantada. Solo se tocó un caso: «Ihnen» no estaba en el estímulo de c41 i1; «15. Mai» sobraba en c40 i1.
4. **Cobertura:** cada `introduce` se cubre en guiada/independiente/situación/evaluación. c49 (proyecto) y c50 (prueba, `introduce` vacío, 7 ítems, 7 claves, 5 formatos) correctos.
5. **Consignas es/en:** claras; las ambiguas se afinaron con pista léxica («empieza por …») sin revelar la solución. Estímulo de c40 i1, c43 i0 y c48 i1 no contenía palabras necesarias para la respuesta (immer→oft, «ehrgeizig» vs ambitioniert, fecha): corregidos.
6. **Lumo/Ecuador/personajes:** nada (grep 0). Nombres genéricos (Wolf, Becker, Berger, Roth, Anna, Jonas, Lena) sin hechos que se arrastren; reaparecen solo como etiquetas.

## Cambios por clase (nº de ítems/situaciones tocados)

c01 4 · c02 7 · c03 3 · c04 2 · c05 2 · c06 5 · c07 4 · c08 1 · c10 1 · c12 2 · c13 2 · c14 2 · c15 1 · c16 1 · c17 2 · c18 3 · c19 2 · c20 1 · c21 2 · c22 3 · c23 3 · c24 2 · c25 5 · c26 3 · c27 3 · c28 7 · c29 2 · c30 1 · c31 1 · c32 3 · c33 3 · c34 1 · c35 4 · c36 1 · c37 1 · c38 2 · c39 3 · c40 3 · c41 4 · c42 3 · c43 1 · c44 3 · c45 3 · c46 1 · c47 2 · c48 3 · c49 2 · c50 3. Sin cambios: c09, c11.

## Sin resolver

- Outline c19: el grupo `situacion` es un acta («Beschluss 1: …»), no un diálogo; el validador lo admite, pero el bloque debe mantener el formato tabla/acta como pide `gramatica` («estilo telegráfico»).
- Outline c46, c49, c50 declaran «integración / sin gramática nueva»: su ítem de `introduce` es solo reciclaje; correcto para c49–c50, algo débil para c46 (clave `angebot-praesentieren` no enseña estructura propia). Sin impacto en los ejercicios.
- Muchos ítems `escuchar` (c35, c36, c37, c38, c39, c40, c41, c44–c46, c48) tienen como opción A la frase idéntica al audio y B una frase obviamente distinta: prueba de reconocimiento, no de comprensión. Aceptable para el método ligero; los bloques deberían parafrasear el audio en la opción correcta.
- Verificación de audio de-DE (Umlaut, ich/ach) pendiente según el Encargo.

## Avisos para autores de bloque (errores frecuentes reales del nivel)

1. «Ich habe den Eindruck, *dass* + V final» y «Ich verstehe, dass Sie verärgert *sind*»: V2 en subordinada (*«…dass Sie sind verärgert»*, *«Ich würde mir wünschen, dass wir können»*).
2. Indirekte Frage: «Mich würde interessieren, *ob Sie reisen können*» (no *«ob können Sie reisen»*); *«Ich möchte wissen, was *reizt Sie*».
3. Konjunktiv I sin «dass» («sagt, er *habe*»); confundir con «dass + Indikativ». *«sei/seien»*: concordancia (*«das Budget seien»*).
4. Preposiciones fijas con acusativo/dativo: *«entschuldigen *zu*»* (→ für), *«liegt *auf* 50.000»* (→ bei), *«steigen *am* 6 %»* (→ um/auf), *«Widerspruch *an*legen»* (→ einlegen), *«Gerade *wegen* ich bin neu»*.
5. «zufolge» pospuesto con dativo (*«Zufolge der Umfrage», «Den Umfrage zufolge»*); «laut» + dativo (+ genitivo en formal).
6. «zwar … aber»: orden *«zwar ich habe»* (debe ser «zwar habe ich»); «gerade weil/deshalb».
7. «ist zu + infinitivo» con separables: *«freizu halten»* (→ freizuhalten), *«ist zu *getragen*»*; «haben … zu» (obligación) confundido con «haben zu + tiempo».
8. Pasiva: *«Das Gebäude *ist* evakuiert»* (estado) vs «wird evakuiert» (proceso); «Beschlossen *wurde*, dass … *wird*» (tiempos).
9. Futur I con «werden» y V final en subordinada («dass wir das Team informieren werden»).
10. Falsos amigos de registro: Bescheinigung/Bescheid, Termin (plazo/cita), Frist ≠ Termin, Kulanz ≠ Gnade.
11. Konjunktiv II: *«würde haben»* en lugar de «hätte»; «Wenn ich … bekäme» con *«würde»* duplicado en ambas partes.
12. Comillas alemanas „…“ en el texto alemán (los autores usaron «…» en dos ejemplos).
