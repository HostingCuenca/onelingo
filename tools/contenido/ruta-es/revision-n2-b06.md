GO

# Revisión N2 B6 (es.n2.c26–c30)

## Validación

`python3 tools/curriculo/validar_bloque.py es 2 6` → 0 errores del bloque (esbozos: n2-b02). JSON válido tras las correcciones.

## Correcciones

- [plan-ficha] c26, tabla p2 (fila poner): tú «pon» → celda de apoyo «irregular tú form: later» (anticipaba imperativo-tu-irregular, que se introduce en c44; la ficha dice que el tú es otra forma y solo pide ponga/pongan) (media)
- [reparto] c26, contexto de la situación: «Saturday in the Andrades' kitchen» → «…kitchen, where Emma and Daniela are visiting» (en N2 ya viven en La Mariscal; son visitas) (baja)
- [reparto] c27, contexto de la situación: «Sunday in the Andrades' dining room» → «Sunday lunch in the Andrades' dining room; Emma and Daniela are visiting» (baja)
- [pedagogía] c27, situación (línea de Jorge): «Gracias, Emma. Daniela, pásamelo, por favor.» → «Gracias, Emma. ¿Y el ají? Daniela, pásamelo, por favor.» (sin antecedente, «lo» podía ser el encebollado, también masculino; ahora la respuesta del diálogo es inequívoca) (media)
- [reparto] c28, contexto de la situación: «In the kitchen» → «In the Andrades' kitchen, Emma (visiting)» (baja)
- [aceptadas] c28, e5: añadida «El pescado se corta, la cebolla se añade y se sirve caliente.» (baja)
- [reparto] c29, situación (Recepcionista): «Restaurante La Mariscal, buenas tardes.» → «Restaurante, buenas tardes.» (La Mariscal es el barrio, no el nombre del local; el contexto en inglés ya dice «a restaurant in La Mariscal») (media)
- [explicación-falsa] c29, tabla p2 fila 3: «¿Podría reservar una mesa para cuatro personas?» / «¿Podrías reservar…?» presentadas como «la misma petición» (significaban «¿puedo reservar?» frente a «¿puedes reservar?») → fila «¿Podría/Podrías traerme la jarra?» (misma petición, usted/tú) y fila nueva con la frase de reservar y la nota «you are the one asking, so there is no tú version» (media)
- [explicación-falsa] c29, g4 pista: «Quería is the polite past form.» → «Quería (from querer) is a polite way to open a request.» (baja)
- [error-validador] c29, ejemplo p4[0]: «personas» no enseñada tras quitar la fila de la tabla → recuperada en la fila nueva de p2 (baja)
- [error-validador] c29, situación: lectura de 59 palabras (mínimo 60) tras quitar «La Mariscal» → Mesero «Muy bien, señorita. Gracias.» y Emma «¿Podría traernos la cuenta al final, por favor?» con sus traducciones (media)
- [explicación-falsa] c30, tabla p2 filas 3 y 4: «Same adjective» pero «El café es amargo / El café está frío» (adjetivos distintos) y «Las papas son crujientes» (las papas no son crujientes por naturaleza) → «El café está amargo» y «Los chifles son crujientes / Las papas están crujientes» (media)
- [explicación-falsa] c30, erroresFrecuentes[1]: «El ají está picante → El ají es picante» (frase natural y correcta en español, mal marcada como error) → «La sopa está salado → La sopa está salada» (concordancia con sopa), con glosa en inglés correcta (media)
- [idioma-es] c30, situación (Mesero): «Aquí está su otra sopa.» → «Aquí está su sopa.» (antinatural) (baja)
- [aceptadas] c30, i4: añadida «Está muy dulce el postre.» (baja)

## Hechos del reparto confirmados

- Emma habla de usted a señora Rosa y a don Jorge; Rosa, Jorge y Daniela la tutean (sábado y domingo de visita en casa de los Andrade) / Emma uses usted with señora Rosa and don Jorge; Rosa, Jorge and Daniela use tú with her (Saturday and Sunday visits at the Andrades' house)
- Rosa enseña a Emma y a Daniela a hacer locro de papa y les habla con ustedes; Emma y Daniela se tutean; la tarjeta de la receta habla de usted / Rosa teaches Emma and Daniela to make locro de papa and addresses them with ustedes; Emma and Daniela use tú; the recipe card uses usted
- Rosa hace encebollado un domingo; Jorge pide el ají a Daniela con tú (la llama su hija: «papá» le dice Daniela) / Rosa makes encebollado on a Sunday; Jorge asks Daniela (his daughter, who calls him «papá») for the chili sauce using tú
- Rosa explica a Emma (de tú, sin órdenes) el encebollado: cebolla y limón, pescado con yuca, cilantro, caliente con arroz, chifle, tostado y rodaja de limón / Rosa explains encebollado to Emma (tú, no commands): onion and lemon, fish cooked with yuca, cilantro, served hot with rice, chifle, tostado and a lemon slice
- Emma reserva por teléfono, de usted, una mesa para cuatro personas el sábado a las 8 de la noche en un restaurante de La Mariscal, a nombre de García (Emma García) y pide el seco de pollo / Emma books by phone, with usted, a table for four on Saturday at 8 p.m. at a restaurant in La Mariscal under the name García (Emma García) and orders the chicken stew
- Sábado por la noche en ese restaurante, con Daniela y Mateo (tú): el seco de pollo de Mateo está muy rico, la sopa de Emma está muy salada y el mesero se la cambia (usted), el arroz de Daniela está un poco frío / Saturday night at that restaurant with Daniela and Mateo (tú): Mateo's chicken stew is very good, Emma's soup is too salty and the waiter replaces it (usted), Daniela's rice is a little cold

## Sin resolver

- c26 y c28 repiten «la receta» y c27/c28/c30 repiten vocabulario entre clases (caliente en c28 y c30); es coherente con las fichas, no se tocó.
- c29 tabla p3 de una sola fila («Quería reservar una mesa.») es redundante con el ejemplo, pero asegura la enseñanza de «quería» mientras B5 (c25) no esté en los esbozos del validador; revisar al integrar el bloque 5.
- c28 erroresFrecuentes[2] («La sopa es servida caliente») es una pasiva gramatical pero poco natural; la glosa lo dice con honestidad, se dejó como distractor.
- Las tres clases c26–c28 sitúan la acción en casa de los Andrade como visita; el sábado/domingo exactos no figuran en el reparto.

Total: 15 correcciones (0 altas, 7 medias, 8 bajas)
