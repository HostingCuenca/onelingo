# Revisión N4 · B3 (fr.n4.c11–c15)

GO

Revisor distinto del autor. Archivo revisado y editado: `tools/contenido/ruta-fr/n4-b03.json`.

Validación: `python3 tools/validar_ruta.py fr --borrador n4-b01.json n4-b02.json n4-b03.json` → 0 errores (los borradores de N3 ya están integrados en `assets/contenido/fr/ruta/` y se quitaron de la lista). `python3 tools/curriculo/validar_plan.py fr`: 0 errores y ningún «título de la unidad difiere» para fr.n4.c11–c15 (solo c26, ajeno al bloque).

## Contraste con las fichas

Títulos, objetivos, gramática, `introduce` (voix-passive-agent, obligation-absence, laisser-infinitif, jusqu-a-ce-que, ne-ni-ni + sans-infinitif), `recicla`, vocabulario (las 9 palabras de cada ficha están, con artículo; el autor añadió algunas, ver abajo) y tarea coinciden con `curriculo/fr/n4.json`. Los ejercicios del plan están todos (5 guiados, 3–4 independientes, 2 de comprensión y 6 de evaluación por clase) con su formato y su clave; el autor pulió consignas y cambió dos ítems del plan por otros mejores (c13 i2: «Vous ne voulez pas réparer la serrure ?» era ilógico; c15 g3: «sans un mot» contradecía la regla «sans + sustantivo sin artículo»). Nada de c16 en adelante: ni relativos con preposición, ni condicional pasado, ni «bien que» / «avant que» / «à moins que». Todo lo reciclado (voix-passive-intro N3 c21, faire-causatif N3 c33, ça-fait-que N3 c01, déjà/pas encore N3 c03, subjonctif N3 c26–c27, avant de N3 c20, futur antérieur N3 c19, ne… aucun N3 c25, órdenes indirectas N3 c36, impersonales N2 c44, chacun N2 c45) se había introducido antes.

Anatomía correcta en las cinco: explicación → tablas → ejemplos (8) → vocabulario → guiada (5, todas con pista) → independiente (sin pista) → situación (160–193 palabras, 2 ítems) → evaluación (5 puntuables en ≥ 3 formatos + 1 `escribir` con `abierta: true`, que no sustituye a ninguno de los 5). Hablantes: Ana, Emma, «L’agence immobilière», «Le syndic», «La secrétaire», «Le voisin» (todos nombres o papeles en francés). Tipografía: U+202F antes de ? ! : ; y ’ en todo el texto francés. Sin castellanismos de España ni anglicismos británicos (barrido automático; «no vale la pena» es la única coincidencia y es correcto).

## Correcciones

| Clase | Ítem | Antes → después |
|---|---|---|
| c11 | situación, línea de Ana (texto fr, es, en) | «l’appartement est entouré de jardins, il est apprécié de tous les voisins» (los vecinos «aprecian» el departamento: sentido raro) → «l’appartement est entouré de jardins et le quartier est apprécié de tous les voisins» (y su traducción es/en); `quartier` ya se enseña en la tabla p5 |
| c11 | practica_independiente, ítem nuevo i4 | El bloque no usaba `relacionar` (la calibración pide los seis formatos a lo largo del bloque y ninguna ficha de B3 lo planifica): añadido `relacionar` con 4 pares de vocabulario del contrato (dépôt de garantie / état des lieux / préavis / quittance de loyer) con glosas claramente distintas (dinero que se devuelve / informe del estado / aviso antes de irse / recibo de pago). Todas las palabras ya estaban en el paso `vocabulario`. Las independientes de c11 pasan de 3 a 4 (dentro del rango 3–4). |
| c12 | i4 `escribir` (aceptadas) | Solo admitía «les poubelles» en 3 variantes → 8 variantes: las 4 fórmulas de «no hace falta» (pas besoin de / ce n’est pas la peine de / on n’est pas obligé de / il n’est pas nécessaire de) × «les poubelles» / «la poubelle» |
| c13 | p1 explicación (es, en) | «el participio laissé no cambia» (afirmación demasiado tajante: antes se concordaba con frecuencia) → «se deja invariable (es la norma actual)» / «stays invariable (the current norm)» |
| c13 | i4 `escribir` (aceptadas) | Solo «ça fait… est en panne… Toujours pas de réponse» → 12 variantes: «ça fait» / «il y a… que» (ambos vistos en N3 c01; la consigna no fija cuál), «est en panne» / «est cassée», con «Toujours pas de réponse.» / «… !» / «… et toujours pas de réponse» |
| c14 | i4 `escribir` (aceptadas) | «Mientras llega» admite «arrive» y «vienne»: añadidas 4 variantes con «vienne» (con «le technicien» y con «il», ambos órdenes) |
| c15 | situación, nota de Emma (fr, es, en) | «vous pouvez faire de la musique, mais sans bruit après minuit» (contradictorio: música sin ruido) → «vous pouvez faire une fête, mais sans faire de bruit après minuit» (y es/en); además modela sans + infinitivo |
| c15 | situación, respuesta del vecino (es) | «¡De acuerdo con el acuerdo!» → «¡Estoy de acuerdo con su propuesta!»; «¡Buenas noches!» (traducía «Bonne soirée !») → «¡Que pase buena noche!» |

## Comprobado y correcto (sin cambios)

- Francés de Francia: concordancias del participio de la pasiva, par / de según acción o sentimiento, pasiva con futuro y modal, il ne faut pas (que) frente a pas besoin de / ce n’est pas la peine de / on n’est pas obligé de, laisser / faire + infinitivo, ça fait… que, toujours pas de, jusqu’à ce que / en attendant que + subjuntivo (venir, arriver, finir, avoir), ne… ni… ni…, sans + infinitivo / sustantivo sin artículo, «ni lui ni moi ne voulons».
- Una sola respuesta defendible por ítem; la consigna fija par / de (c11 g1, g2, e1, e2) y «ya no» (c15 e5 → plus). `ordenar`: los órdenes alternativos naturales están en `aceptadas` donde existen (c14 i2 y e5); en el resto solo hay un orden natural.
- Pistas específicas de cada ítem; ninguna fuera de la práctica guiada. Explicaciones en es (tú, neutro) y en (americano), con el contraste para anglohablantes (you must not / you don’t have to) y para hispanohablantes («no hay que» ambiguo).
- Guías de sonido: ö se define en c11 («l’état des lieux») y ü en c12 («parties communes») la primera vez que aparecen en el bloque; nasales in / an / on con «en» / «an» / «on»; j y g suave «sh» (es) y «zh» (en).
- Textos de situación coherentes con sus 2 ítems de comprensión (cada pregunta tiene una única respuesta en el texto).

## Hechos del reparto confirmados

- Ana y Emma firman el contrato de un departamento más grande en el mismo barrio (c11): alquiler de 1 100 euros al mes, la fianza se paga antes de entrar y el propietario la devuelve un mes después de la entrega de las llaves, la inmobiliaria hace el état des lieux el día de la entrada y piensan firmar el sábado. / Ana and Emma sign the lease for a bigger apartment in the same neighborhood (c11): rent 1,100 euros a month, the deposit is paid before move-in and the landlord returns it one month after the keys are handed over, the agency does the inspection report on move-in day and they plan to sign on Saturday.
- El nuevo edificio tiene syndic, gardien, local à vélos en el patio y un reglamento colgado en la entrada; Ana quiere hablar con el gardien y va a la reunión de vecinos, Emma no (c12). / The new building has a building manager, a superintendent, a bike room in the courtyard and house rules posted in the entrance; Ana wants to talk to the superintendent and goes to the neighbors’ meeting, Emma does not (c12).
- El propietario del nuevo departamento es Monsieur Roux, a quien Ana trata de vous; llevan un mes viviendo allí (c13, c14). / The landlord of the new apartment is Monsieur Roux, whom Ana addresses with vous; they have lived there for a month (c13, c14).
- Averías del nuevo departamento: el calentador de agua lleva tres semanas descompuesto, hay humedad y moho en el baño, el fregadero de la cocina lleva dos semanas atascado y la cerradura de la puerta una semana rota; Ana mandó llamar a un plomero la semana pasada y no pudo repararlo; dos mensajes a Monsieur Roux sin respuesta (c13, c14). / Breakdowns in the new apartment: the water heater has been broken for three weeks, there is dampness and mold in the bathroom, the kitchen sink has been clogged for two weeks and the door lock broken for one week; Ana had a plumber come last week and he couldn’t fix it; two messages to Monsieur Roux are unanswered (c13, c14).
- Ana está en el trabajo hasta las seis entre semana (coherente con N2 c03: sale del hotel a las 6). / Ana is at work until six on weekdays (consistent with N2 c03: she leaves the hotel at six).
- Visita técnica del calentador el jueves entre las 14 h y las 16 h; Emma estará en casa porque solo trabaja por la noche (en el restaurante de Karim); hasta que llegue el técnico cortan el agua caliente y no se duchan (c14). / The technician’s visit for the water heater is Thursday between 2 and 4 p.m.; Emma will be at home because she only works in the evening (at Karim’s restaurant); until the technician comes they turn off the hot water and don’t shower (c14).
- El vecino de arriba (sin nombre, trato de vous) puso música hasta las dos de la mañana; Emma le deja una nota (Ana y ella no podían dormir) y él acepta hacer menos ruido por la noche y avisar antes de una fiesta (c15). / The upstairs neighbor (unnamed, addressed with vous) played music until two in the morning; Emma leaves him a note (she and Ana couldn’t sleep) and he agrees to make less noise at night and to warn them before a party (c15).
- Madame Dubois, antigua propietaria, es apreciada por todos sus vecinos y sigue viviendo cerca (c11, ejemplo; coherente con la nota del nivel). / Madame Dubois, their former landlady, is well liked by all her neighbors and still lives nearby (c11, example; consistent with the level note).

## Palabras añadidas por el autor (todas enseñadas antes de usarse)

c11: la remise des clés, entouré / entourée, apprécié / appréciée. c12: ce n’est pas la peine y pas besoin de como tarjetas, obligé / obligée, nettoyer, les poubelles, jeter. c13: couler y Monsieur Roux (esta última declarada en el vocabulario de la unidad pero sin tarjeta propia; el validador la da por conocida). No he quitado ni renombrado ninguna palabra francesa, así que ningún bloque posterior del nivel se ve afectado.

## Pendiente / a vigilar

- N3 c05 (hecho del reparto) dice que Emma «ya solo trabaja los fines de semana» en el restaurante de Karim; el reparto indicado por el coordinador para N4 es que trabaja por las noches. c14 dice «Elle ne travaille que le soir», compatible con ambos y con que esté en casa el jueves a las 14 h. Los bloques posteriores de N4 deben mantener «por la noche».
- Las situaciones miden 160–193 palabras (c13, c14 y c15 en el borde inferior del rango 150–250 de la tabla «Por nivel», por debajo de las «unas 170–210» de las fichas). Cumplen el rango del encargo y sus textos son completos; si se quiere más lectura, ampliar en una futura pasada.
