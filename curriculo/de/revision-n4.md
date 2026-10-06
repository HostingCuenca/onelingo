GO

# Revisión independiente del N4 alemán (B1+), c01–c50 (método ligero)

Revisor distinto del autor. Archivo: `curriculo/de/n4.json` (50 fichas `planificado`) contra `tools/curriculo/de/n4-outline.json`. Solo se editó `ejercicios` (campos del outline sin tocar).
Validadores tras las correcciones: `validar_plan_detallado.py de curriculo/de/n4.json` = 0 errores (731 ejercicios); `validar_plan.py de` = 0 errores. Script: `scratchpad/de/fichas/rev-n4.py` (+ partes `rev-n4-p1..p4.py`).

## Veredicto por criterio

1. **Alemán correcto:** sin errores de lengua graves. Konjunktiv II, doble infinitivo, Futur II, pasivas (modal, estado, impersonal, perfecto), genitivo, nominalización, Partizip I, hin/her: todo correcto. Se retiraron formas literarias o raras (*kennte*, *wüsste*) por no estar enseñadas, y distractores que parecían erratas (*mizufrieden*, *misfreundlich* -> *misszufrieden*, *missfreundlich*).
2. **Una sola respuesta:** era el problema principal. Se corrigieron `ordenar` con segundo orden válido (c03 «Der Junge … und rief …» invertible; c08 «kann nicht … der Nachbar»; c28 «eher» móvil; c06 «doch» móvil), `completar` con varios modales o conjunciones posibles (c01, c06, c07, c08, c14, c45, c23 «wegen/aufgrund», c40 «entlang/oberhalb», c35), `relacionar` con pares semánticamente permutables (c01, c09, c10, c45, c47) y `escribir` con cue incompleto (c02, c20 «mir», c27, c36, c34, c04).
3. **Nada sin enseñar:** salió léxico no visto en ejercicios y situaciones (Kapitänin, Gurte, Bäume/pflanzen, radeln, Flur, leise, Start-up, vorbei, bearbeitet, Kundendienst, Antrag, Quatsch, besetzt). Comprobado contra el vocabulario de n1–n4: *Garantie* (n3.c32), *Gerät* (n3.c31), *Verspätung* (n4.c09), *beschädigt* (n4.c12) están enseñados. *Radwege* es compuesto de Rad + Weg (aceptado). c40: `genitive-articles` y `genitive-prepositions` figuran en `previos`, correcto.
4. **Cobertura:** todas las claves de `introduce` están evaluadas; c50 (8 ítems, 5 formatos, 8 claves distintas) cumple el mínimo del formato.
5. **Consignas:** coherentes. Se arreglaron incoherencias entre pregunta de situación y texto (c32, c33, c35, c48: la pregunta citaba una frase que el diálogo no decía), una consigna confusa en c35 y la ambigüedad de tiempo en c35 y c48.
6. **Lumo/Ecuador/continuidad:** limpio (grep Ecuador/Quito/Lumo = 0). Nombres genéricos sin hechos arrastrados.

Notas de autores comprobadas: c40 (genitivo) OK; c32/c36/c37 `ordenar` con separables: únicos tras fijar «Die Heizung/Die Wohnung» (c11) y «Bitte» (c36); c41–c50 léxico B1+ revisado (arriba).

## Cambios (62 ítems/situaciones)

- **c01** g0, i2 (relacionar con mains permutables), e1 (coma tras «Jedes Mal» para excluir «Immer»).
- **c02** i1 (cue con las dos frases a unir). **c03** g2 (orden único). **c04** g2 (sin *wüsste*), e0 (sin *kennte*), e4 (cue y consigna únicos; consigna sin «completa» por el validador).
- **c06** i0, e2 (token «ich doch»), e4. **c07** g0, e1 (modal fijado en consigna). **c08** i1, e0, e2 (token «kann nicht»), e5.
- **c09** i0, i2. **c10** i2 (consecuencias distintas). **c11** g1, e2 (arranque fijado). **c14** e5. **c16** e1 (sin «Antrag»).
- **c20** e4 («mir» en el cue). **c23** e6 («aufgrund» fijado). **c26** g2 (sin Start-up), sit («Mia Kern»: el diálogo no identificaba a Mia con Frau Kern).
- **c27** i2. **c28** e3 (token «würde eher»), e4. **c31** g1, e0, e4 (sin Kapitänin). **c32** g1, i1, q0 (la pregunta no coincidía con el diálogo).
- **c33** q1 (Spiel -> Turnier). **c34** e1, e4 (sin «vorbei»). **c35** q0, q1, e4, e5. **c36** i2, e4 (sin «Gurte»). **c38** e6. **c40** i2 (sin «radeln»), e0.
- **c43** e4 (sin pflanzen/Bäume). **c45** g0, i2. **c47** i2. **c48** e4, sit y q0/q1 («besetzt» -> «voll»). **c49** i1, e2, sit («Kundendienst» -> «Firma Wolf»). **c50** g0 (sin Streit/Flur), i0 (sin «leise»).
- Sin cambios: c05, c12, c13, c15, c17, c18, c19, c21, c22, c24, c25, c29, c30, c37, c39, c41, c42, c44, c46.

## Sin resolver

- c50 no puede evaluar lo que declara el outline (texto argumentado de ~160 palabras, lectura y conversación) con 8 ítems cerrados; la prueba real debe incluir producción libre fuera de las fichas.
- Los `recicla` de c48–c50 son listas largas (12–14 claves); no todas aparecen en los ítems (hueco aceptado, como en el piloto N1).
- Los `ordenar` de subordinada (c32 g2, c33 i0, c39 i0, c42 i0) devuelven la subordinada sin punto y con tokens sin coma; es coherente con el validador pero conviene normalizarlo en la app.
- Léxico no enseñado tolerado por ser transparente: Opa/Suppe (c01), Kasse (c39), Süßes/Süßigkeiten (c32/c33).

## Avisos para autores de bloque (`erroresFrecuentes`)

1. Verbo en 2.ª posición tras conectores subordinantes: *«Immer wenn wir hatten Ferien»*, *«als ob er ist müde»*, *«Da er war krank»*, *«auch wenn es regnet, ich gehe»* (tras la subordinada, el verbo de la principal va primero).
2. Correlato equivocado: *«Ich erinnere mich davon»*, *«träume daran»* (da-/dar- + preposición del verbo).
3. Perfekt/pasiva: *«Ich habe arbeiten gemusst»*, *«ist abgesagt geworden»* (worden, no geworden), *«hat eingeführt worden»* (auxiliar sein).
4. Konjunktiv II con indicativo: *«Ich wünschte, ich bin entspannt»*, *«Wenn ich doch Zeit habe»*, *«Ich habe das nicht sagen sollen»* (hätte sollen).
5. Genitivo: *«Die Höhe die Rechnung»*, *«aufgrund die Störung»*, *«innerhalb von 14 Tage»* (dativo tras «von»), *«der Betrag»* sin -s en masculino.
6. Prefijos inventados: *«mizufrieden»*, *«missgeduldig»*; contrario correcto con un-.
7. Pasiva de estado frente a proceso: *«Die Tür wird geschlossen»* (acción) vs *«ist geschlossen»* (resultado).
8. Falsos amigos y ⚠: *«Termin»*, *«Garantie»*, *«Chef»* (registro), *«Gift»*; «dürfte» = probable, no «permitido».
9. *Sich lassen*: *«lässt erklären sich»*; *sein + zu* con separables: *«zurück zu geben»* (zurückzugeben, una palabra).
10. Tuteo/ustedeo: mezcla *«Wollen Sie dich duzen»*; en correos, «Mit freundlichen Grüßen» sin coma ni minúscula en el nombre.
