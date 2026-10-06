GO

# Revisión independiente del N8 (alemán C1 entrada, método ligero), c01–c50

Revisor distinto del autor. Archivo: `curriculo/de/n8.json` (50 fichas, `planificado`) contra `tools/curriculo/de/n8-outline.json`. Solo se editó `ejercicios`; campos del outline intactos. Script: `scratchpad/de/fichas/rev-n8.py`.
Validadores: `validar_plan_detallado.py de curriculo/de/n8.json` = 0 errores (50 clases, 701 ejercicios); `validar_plan.py de` = 0 errores.

## Veredicto por criterio

1. **Alemán correcto:** muy limpio (género, caso, Konjunktiv II/I, separables, mayúsculas, ä/ö/ü/ß). Errores reales encontrados y corregidos: «an Herr Wolf» (c37, debe ser Herrn); «zu Gesundheit» (c20, zur); «Das Projekt hat Begegnung zum Ziel» sin artículo (c47); «Wie X zeigt, sei …» (indicativo + Konj. I mezclados, c43 y c49); ordenar con «sie ist» tras «So sehr … auch» (orden no estándar, c15); comillas «…» en estímulos y textos alemanes, pasadas a „…“ en todo el nivel (213 «» quedan solo en consignas españolas, correcto).
2. **Una sola respuesta:** el punto más débil del nivel. Corregidos: 8 `ordenar` con otro orden válido (c05, c07, c09, c15, c29, c46, c47 y tokens mal formados en c43), ~35 `completar`/`escribir` con sinónimos válidos (consigna sin pista o con pista de otra palabra) y 3 `relacionar` con pares solapados (c29 allerdings/trotzdem, c30, c35, c50 Kumpel/Typ). c50: el `escribir` de argumentationsanalyse decía «sigue con Zahlen» (la frase termina en Zahlen); ahora «en presente… termina con Zahlen». El otro `escribir` de c50 (pasiva) es único.
3. **Nada sin enseñar:** sin hallazgos graves; el nivel es C1 y el léxico es de la ficha o de niveles previos. Sustituido «außerdem» por reserva (c29) y «Erstattung» se deja (C1). Sin dativo/gramática adelantada.
4. **Cobertura:** cada clave de `introduce` está evaluada en c01–c48 (el validador lo confirma). c49 (proyecto) y c50 (prueba, 8 ítems, 7 claves, 5 formatos) cumplen FORMATO. Observación: c50 no toca los bloques «variedades» ni «cine/literatura» (solo recicla de bloques 1, 2, 5, 6); cumple el mínimo, pero la prueba es sesgada hacia lo académico.
5. **Consignas es/en:** había consignas que no coincidían con el ítem: c13 (gu completar, hablaba de Zuwanderung y el ítem de Steuerlast), c13 sp (Herr Hahn decía algo que decía Frau Roth), c18 sp (viertel zwölf no es la cita), c12 sp (einladen no estaba en el texto), c40 ev (pedía «en el futuro» y la respuesta era sofort), c41 ev (decía «subordinada» y la frase era principal), c08 ev (sin estímulo), c34 («recto»). Todas corregidas.
6. **Sin Lumo / Ecuador / Quito:** comprobado (0 apariciones). Personajes: Frau Roth/Herr Hahn/Frau Keller/Jonas/Anna/Lena son etiquetas genéricas, sin hechos que continúen entre clases.

## Cambios (102 ítems/textos tocados; el recuento cuenta cada campo editado)

- c02: sp consigna; ev escribir (ambiguo haste/’ne; ahora «hast du»→«haste»).
- c03: ev escuchar (la audio no distinguía oral/escrito; ahora corrige «weil – ich bin»).
- c04: ev escribir (cue: das Büro, geschlossen).
- c05: in elegir (u. a. también significa «und andere»; distractor cambiado); ev ordenar (empieza con Treffen).
- c06: in escribir, ev escribir (cue de verbo/sujeto).
- c07: gu/in/ev completar (sinónimos sozusagen/quasi/gewissermaßen; pista inicial), ev ordenar, ev escribir (posición).
- c08: ev elegir (añadido el estímulo «nicht ohne Risiko»).
- c09: gu ordenar (ihm das / das ihm).
- c10: gu/ev completar (Glücklicherweise vs Erfreulicherweise), ev escribir (Unglücklicherweise).
- c12: gu ordenar (!), sp completar (texto).
- c13: gu completar, sp elegir, sp completar (desajustes consigna/ítem).
- c14: sp completar (para quién es «Sie»), ev completar (können).
- c15: ev ordenar (nuevo, orden único), ev escuchar (distractor), ev escribir (stimmen).
- c16: gu/ev/sp completar (liegen/sitzen/stehen explícitos).
- c18: sp completar (la cita), ev escribir (duplicaba otro ítem).
- c19: gu elegir y ev escuchar (distractor absurdo; duplicado de audio).
- c20: in completar («zur Gesundheit»), sp completar (alineado al texto), ev ordenar.
- c21: ev escribir (Übung macht den Meister también consolaba).
- c22: ev relacionar (consigna).
- c23: ev completar (aufgeben/aufhören).
- c25: ev elegir (opción A mal formulada), sit («sagt man es anders»).
- c26: ev escribir (cue). c27: ev completar (weglassen/kürzen). c28: in escribir, ev completar.
- c29: sp completar, ev relacionar (pares solapados), ev ordenar (dativo/acusativo libres), ev escribir.
- c30: gu relacionar, in/ev completar, in/ev escribir (cues de modal y verbo).
- c32: ev escribir (beginnen). c33: in escribir, in completar (leises/gedämpftes, Stille/Ruhe).
- c34: in completar (müssen/kann), in escribir. c35: ev elegir, ev relacionar (par «gehen» doble), ev escribir.
- c36: in escribir, ev completar, ev escribir. c37: sit («an Herrn Wolf»). c38: in/ev escribir.
- c39: gu completar (gemäß/nach), in elegir (distractor absurdo). c40: ev completar (künftig).
- c41: ev ordenar (consigna errónea). c43: gu completar, in escribir, ev elegir, ev ordenar (tokens), sit (Konj. I).
- c44: ev completar. c46: ev ordenar. c47: in ordenar, ev completar. c48: in escribir, ev completar.
- c49: sit (Konj. I). c50: gu relacionar (pares solapados), ev escribir (consigna contradictoria).
- Todo el nivel: «…» → „…“ en `ejemplo` y `situacion.texto`.

## Sin resolver

- `recicla` de c05–c12, c34, c35 y otros incluye claves que ningún ítem usa (heikle-formeln, zeitenfolge, ehe-indessen, temporal-praep-gehoben, biografischer-stil, daraufhin-zuvor, irreal-konzessiv, vertragssprache-konj1…): son claves de N7 y de bloques posteriores que el outline reparte sin espacio real en 6 ítems; hueco menor aceptado.
- Las `situacion` de 3–6 líneas (≥24 palabras) son mucho más cortas que los «400–700 palabras» de la nota del outline; es una decisión del método ligero (el texto largo lo desarrolla el bloque).
- c50 sesgada a bloques 1, 2, 5 y 6 (ver criterio 4); para ampliar habría que sustituir ítems repetidos de hedging/reduktionen.
- Varias claves (c20 bedeutung-aushandeln, c47 «richtet sich an») admiten frases libres en la producción real; el ítem fija el cue, pero el bloque debe revisar `aceptadas`.

## Avisos para autores de bloque

1. **`escribir`/`completar` con sinónimos válidos:** la consigna debe dar la letra inicial o el verbo exacto (weglassen/kürzen, sofort/umgehend, Glücklicherweise/Erfreulicherweise, Stille/Ruhe, Mangel/Defekt, zeigt/betont/belegt, Prüfung, gemäß/nach).
2. **Orden de objetos y de adverbios móviles** (dativo antes/después de acusativo: «Ich empfehle die Serie allen»; «als Beispiel» antes/después; «noch», «gewissermaßen»): fijar con «empieza con X» o con otra frase.
3. **Konjunktiv I:** «Wie X zeigt, sei …» es incorrecto; solo tras verbos de decir (betont, sagt) y sin «wie … zeigt».
4. **«so sehr … auch»:** el orden tras la concesiva es verbo en 2.ª posición («ist sie unzufrieden») en estándar; evitar ordenar con la principal detrás.
5. **Errores de caso en cartas:** «an Herrn Wolf» (n-Deklination), «zur Gesundheit», «gemäß dem Vertrag / den AGB»; «gemäß § 437 BGB» sin artículo.
6. **Falsos amigos y usos:** Termin/Chef/Aktion («promoción» vs acción), Handy, Evidenz («pruebas», no «evidencia» general), Kulanz.
7. **Regionalismos:** «viertel acht» = 7:15 y «dreiviertel acht» = 7:45 en el sur, el este y Austria (en el norte: Viertel nach/vor); «Servus/Moin/Grüezi» marcar región; en Suiza «ss» siempre y «parkieren».
8. **Formas literarias:** «glomm/buk/focht» son solo reconocimiento; aceptar estándar (glimmte, backte) como distractor, no como respuesta.
9. **Comillas:** en alemán „…“ (no «…»); las consignas españolas sí usan «…».
