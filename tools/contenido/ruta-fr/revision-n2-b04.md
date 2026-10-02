# Revisión independiente · N2 francés, bloque 4 (clases 16–20)

- **Archivo:** `tools/contenido/ruta-fr/n2-b04.json` (`fr.n2.c16` … `fr.n2.c20`). Revisor distinto del autor.
- **Validador:** `python3 tools/validar_ruta.py fr --borrador …/n2-b04.json` → **0 errores**. Encadenado con `n2-b05.json` y `n2-b06.json` → **0 errores** (tras los últimos cambios).
- **Plan:** `python3 tools/curriculo/validar_plan.py fr` → 0 errores, 10 avisos antiguos de N1 (situaciones fuera del bloque del marco); ningún «título de la unidad difiere» para c16–c20 (los cinco títulos coinciden con la ficha).

## Veredicto

GO

## Contraste con las fichas

Cada clase enseña lo que dice su ficha y nada de clases posteriores. c16: il fait + beau/mauvais/chaud/froid/vingt degrés, il y a du / des / de l’, le temps est nuageux, en été / en automne / en hiver, au printemps, futur proche para el pronóstico. c17: futur simple regular (-er, -ir, -re sin la e; los -ger conservan la e), futur proche frente a futur simple. c18: las diez raíces irregulares (ser-, aur-, ir-, fer-, viendr-, pourr-, voudr-, devr-, verr-, saur-), il y aura, il faudra y quand + futuro. c19: si + presente + futuro / imperativo, s’il / s’ils pero si elle / si elles, ça dépend. c20: je voudrais, j’aimerais, pourriez-vous, ce serait possible, inversión (pouvez-vous, avez-vous, êtes-vous, est-il possible de), ça vous irait / ça me va, empêché / empêchée. No aparece si + imparfait → conditionnel (N3): c20 presenta el condicional solo como fórmulas, con una frase sobre su raíz (la del futuro) y las terminaciones del imparfait, que ya se vio en c09. No se incluye la -t- eufónica (a-t-il…) porque la ficha no la pide; queda para una clase posterior.

Anatomía y tiempos: explicación (+ nota de pronunciación) → tablas → ejemplos (8) → vocabulario → guiada (5, con pista) → independiente (4) → situación (9 líneas, 80–92 palabras, 2 ítems) → evaluación (6 ítems puntuables en 6 formatos + 1 `escribir` abierto que no puntúa). Hablantes: solo nombres de personajes (Ana, Emma, Léa, Hugo, Chloé).

## Cambios aplicados (clase · ítem · antes → después)

### Todas
1. **Tipografía.** 16 casos de «espacio normal + U+202F» (doble espacio) en las explicaciones de c16 («Quel temps il fait  ?») y c20 («Vous pouvez venir  ?», «Est-il possible de…  ?», es y en) → solo U+202F.

### c16
2. **Vocabulario declarado sin enseñar.** `neiger` (v-neiger) no se usaba en ningún paso → eliminado de `vocabulario`. `le degré`, `mauvais` y `pleuvoir` estaban declarados y usados pero faltaban en la tarjeta de vocabulario → añadidos a los `refs` del paso `vocabulario`.
3. **Pronóstico en presente.** Diálogo l. 3 «L’après-midi, il y a du soleil» → «il va y avoir du soleil»; l. 5 «il va faire douze degrés et il y a du vent» → «et il va y avoir du vent» (es / en ajustados). Una predicción para mañana mezclaba futur proche y presente.
4. **e1 (escuchar).** «Samedi, il va pleuvoir et il y a du vent.» → «… et il va y avoir du vent.» (opción correcta y feedback ajustados): la frase mezclaba futur proche y presente.
5. **s1 (pregunta de comprensión).** «¿Qué tiempo hace por la mañana?» → «¿Qué tiempo va a hacer por la mañana?» (en: «What’s the weather going to be like…»). **s2, opción correcta:** «porque hace doce grados y hay viento» → «porque por la noche habrá doce grados y viento».
6. **Tabla «Cómo está el tiempo» (en).** «It’s twenty degrees (20 °C).» → «(20 °C, about 68 °F)» (nota °F opcional).

### c17
7. **p6 (tabla de más verbos), fila `changer`.** La columna «nosotros / ellos» llevaba «nous changerons / vous changerez» → «nous changerons / ils changeront».
8. **i3 y e6 (escribir).** Aceptaban en teoría el futur proche (je vais finir…, tu vas parler…). Consigna: «Escribe en francés: …» → «Escribe en francés con el futur simple: …» (es / en).

### c18
9. **Ejemplo 3.** «Le mois prochain, vous pourrez venir mardi ?» (un martes sin fecha en un mes entero) → «Le mois prochain, vous pourrez venir à Lyon ?» (es / en ajustados).
10. **e5 (relacionar), glosa de `confirmer`.** «decir que sí, con seguridad» (no es lo que significa) → «decir que el plan sigue en pie» (en: «to say the plan is still on»).
11. **i3 y e6 (escribir).** Misma corrección que en c17: «… con el futur simple: …» (je vais aller… era válido para las consignas anteriores).
12. **Situación, cierre.** Hugo «À mercredi !» / Ana «À plus tard !» (la cita es dentro de una semana) → el diálogo termina en «À mercredi !» (9 líneas, 80 palabras). «À plus tard» sigue enseñada en vocabulario y en el ejemplo 7.

### c19
13. **i3 (escribir).** `aceptadas` solo tenía «nous»; «on» es igual de natural (en e6 ya estaba) → + «S’il pleut, on reportera le barbecue.», «On reportera le barbecue s’il pleut.». Consigna con «con el futur simple» (el futur proche también es válido tras si).
14. **e6 (escribir).** Consigna «… con el futur simple: …» (idem).

### c20
15. **p1 (explicación).** «no digas je veux ni tu peux» (tu peux es normal entre amigos) → «(por teléfono, con alguien a quien tratas de vous) no digas je veux ni vous pouvez» (es / en).
16. **Situación, cierre de Chloé.** «Je vous rappelle demain matin. À jeudi !» (ofrecía una confirmación por e-mail y además llamaba, sin motivo) → «Je vous rappelle demain matin si Monsieur Martin est empêché. À jeudi !» (es / en ajustados): da motivo a la llamada y reutiliza si + presente (c19) y empêché. 9 líneas, 89 palabras.

**Palabras eliminadas o renombradas que pudieran usar B5 / B6:** ninguna. Se eliminó solo `neiger` del vocabulario declarado de c16 (no la usan B5 ni B6); «serait» y «possible» de c20 se conservan. Con B5 y B6 encadenados el validador da 0 errores.

## Revisión punto por punto

1. **Francés de Francia.** Expresiones del tiempo correctas (il fait beau / mauvais / vingt degrés, il y a du vent / de l’orage, le temps est nuageux; au printemps pero en été / automne / hiver); futuros regulares e irregulares (prendrai / attendrai sin la e, voyagerai / changerai / mangerai con la e, ser-, aur-, ir-, fer-, viendr-, pourr-, voudr-, devr-, verr-, saur-), il y aura, il faudra; quand + futuro (en las dos partes); si + presente + futuro / imperativo; s’il / s’ils pero si elle / si elles; voudrai (futuro) frente a voudrais (cortesía); inversión con guion (pouvez-vous, avez-vous, êtes-vous, voulez-vous, est-il possible de); empêché / empêchée con concordancia. Tipografía: U+202F y ’ correctos.
2. **Explicaciones es / en.** Cortas y con ejemplos; es con tú y léxico neutro (pasantía, paraguas, caminata, parrillada, abrigo, suéter, correo electrónico); en americano (movies, cookout, fall, sweater, internship). La comparación con el español (subjuntivo tras cuando) y el inglés (when I’m) en c18 es correcta y útil.
3. **Respuesta única y `aceptadas`.** Revisados `ordenar` (todos los órdenes naturales del complemento circunstancial, y «Jeudi à midi, ça vous irait ?» en c20), `completar` (un distractor por ítem, siempre erróneo en el contexto de la consigna), `escribir` (el futur proche solo se acepta donde la consigna no lo excluye: c16 es futur proche por la ficha; c17–c19 piden futur simple) y `elegir` / `escuchar`.
4. **Pistas y relacionar.** Cada pista ayuda a su ítem (infinitivo entero + -ai; raíz irregular; presente tras si; vous detrás del verbo con guion). Las glosas de `relacionar` son distintas entre sí en las 10 listas.
5. **Guías de sonido (regla 6).** sh / zh para ch y g suave, nasales an / on / en, ü y ö definidas en c16 (primera clase del bloque), s y t finales mudas, -ai «é» frente a -ais «è» (c20), «est-il» con t que suena. Comprobadas palabra por palabra; no hubo correcciones.
6. **Situaciones.** 9 líneas y 80–92 palabras (objetivo N2: 6–10 líneas, ≈ 80–120 palabras); una sola respuesta correcta por pregunta; los diálogos modelan el objetivo de la clase (pronóstico y ropa, planes, cita y agenda, plan B, cortesía).
7. **Ejercicio abierto.** En cada clase hay 6 ítems puntuables en 6 formatos; el `escribir` con `abierta: true` no puntúa y se suma a ellos.

## Hechos del reparto confirmados

- Léa da una fiesta en su casa el sábado; el viernes por la noche Ana y Emma miran el pronóstico (nublado y lluvia por la mañana, 12 grados por la noche) y deciden ponerse abrigo (c16). / Léa throws a party at her place on Saturday; on Friday night Ana and Emma check the forecast (cloudy and rain in the morning, 12 degrees at night) and decide to wear coats.
- Ana planea viajar más adelante a Quito en avión para comer con su familia y hablar español con ellos (c17); sigue trabajando en el hotel y estudiando francés. / Ana plans to fly to Quito later to eat with her family and speak Spanish with them (c17); she keeps working at the hotel and studying French.
- Ana trabaja los martes por la tarde en el hotel y no está disponible; Hugo y Ana quedan el miércoles por la noche para ir al cine a las 8 y confirman por mensaje el miércoles por la mañana (c18, c20). / Ana works Tuesday afternoons at the hotel and is not available; Hugo and Ana plan a Wednesday-evening movie at 8 and confirm by message on Wednesday morning.
- Hugo termina su pasantía (stage) a las 6 de la tarde (c18). / Hugo’s internship (stage) ends at 6 pm.
- El domingo Léa, Hugo y Ana hacen un barbecue en el parque; el plan B si llueve es comer en casa de Ana y Emma (c19). / On Sunday Léa, Hugo and Ana have a barbecue at the park; the plan B if it rains is to eat at Ana and Emma’s place.
- Ana tiene una cita con Monsieur Martin el martes a las 2; Chloé (secretaria) la mueve al jueves a mediodía y Ana y Chloé se tratan de vous (c20; coincide con N1 c20, c29 y c48). / Ana has an appointment with Monsieur Martin on Tuesday at 2; Chloé (the secretary) moves it to Thursday at noon, and Ana and Chloé address each other with vous (consistent with N1 c20, c29 and c48).

## Sin resolver (no bloquea)

- **Cuatro hechos nuevos no están todavía en `curriculo/fr/n2.json`** (`hechosDelReparto` solo llega al bloque 3): fiesta de Léa el sábado, viaje de Ana a Quito, pasantía de Hugo hasta las 6 y cine con Hugo el miércoles. El coordinador puede copiar las líneas de arriba con `bloque: 4`.
- **Fiesta del sábado y barbecue del domingo (c16 / c19):** no se dice si son del mismo fin de semana. La tabla de pronóstico de c16 da «dimanche: il va faire beau», coherente con el barbecue al aire libre del domingo.
- **Hugo, clases y pasantía:** B1 dice que Hugo termina las clases a las 5; en c18 termina la pasantía a las 6 (después de las clases o en días sin clase). No hay contradicción dura; si el coordinador lo quiere, se puede precisar en una clase posterior.
- **c20, «jeudi à midi»:** en el planning de Monsieur Martin de c04 (un día concreto) el almuerzo es después de la reunión de las 11; no es la misma jornada, así que no choca.
- **Ejercicios de redacción de c18, e7:** el modelo usa «Salut Hugo !» y futuros irregulares; correcto para la clase.

Validación final: 0 errores.
