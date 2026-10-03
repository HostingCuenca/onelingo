GO

## Validación
`python3 tools/curriculo/validar_bloque.py es 4 8` → 0 errores del bloque (esbozo solo de n4-b01).
Comprobado además a mano: plan de ejercicios de cada ficha (formatos y claves), 5–8 ejemplos, 6–12 palabras de vocabulario, `completar` con un solo `___`, una sola respuesta por ítem (o `aceptadas` completas), pistas solo en la práctica guiada, apoyo solo en inglés americano, títulos de unidad solo en inglés, tabla de usted/ustedes sin vosotros, distractores incorrectos solo en opciones y `erroresFrecuentes` (nunca como modelo en ejemplos, patrones o diálogos), lecturas de 150–250 palabras (ahora 154–169), cronología c37 → c36 → c39 → c38 → c40 sin contradicciones, Emma en Guápulo (no en La Mariscal).

## Correcciones
- [pedagogía] es.n4.c37, situacion (diálogo): 142 palabras → 164 (añadidos «¿Para cuántos días necesita el carro?» / «Para dos días: el sábado y el domingo. Volvemos el domingo por la tarde.») (media)
- [pedagogía] es.n4.c38, situacion (diálogo): 139 palabras → 169 (añadidos el número de la agencia, «En caso de emergencia, llamamos» y «cuidado con la neblina») (media)
- [pedagogía] es.n4.c39, situacion (diálogo): 130 palabras → 161 (guantes de Mateo, lista final de lo que llevan, Mateo llega a las cinco y media) (media)
- [pedagogía] es.n4.c40, situacion (diálogo): 139 palabras → 154 (fotos que Emma le manda a Daniela, «mucha agua y mucho ruido») (media)
- [pedagogía] es.n4.c36, situacion (diálogo): 150 palabras (justo en el límite) → 157 («mi pasaporte», «Solo nosotros dos vamos a manejar») (baja)
- [otro] es.n4.c38, situacion, Despachador: Emma pide «Veinte dólares», luego «llene el tanque» y paga «cuarenta» sin explicación → «Con gusto. Entonces no son veinte dólares, son cuarenta. En un momento está listo.» (alta)
- [otro] es.n4.c38, tabla «To read», fila «la Ruta de las Cascadas»: nombre propio con fila (la regla lo prohíbe; el validador ya aceptaba las palabras) → fila quitada (baja)
- [otro] es.n4.c40, tabla «To read», fila «se quedaron»: forma ya enseñada en es.n4.c14 → fila quitada (baja)
- [explicación-falsa] es.n4.c39, vocabulario v-guantes, nota: «Always plural, like “gloves”» → «Usually plural, like “gloves”; one glove is un guante» (media)
- [aceptadas] es.n4.c39, practica_guiada g2 («Llevo el paraguas por si ___»): solo «acaso» → se añade «las dudas» (también correcto y enseñado en el patrón) y se menciona en el feedback (media)
- [apoyo-en] es.n4.c36, vocabulario v-licencia, nota: «Beware of “license” as a verb…» (confuso) → «In Ecuador la licencia is the card that lets you drive.» (baja)

## Hechos del reparto confirmados
- Emma tiene 28 años cuando alquila el carro (nació el 12-04-2001; año 2029) / Emma is 28 when she rents the car (born April 12, 2001; year 2029)
- Alquiler en una agencia de Quito: el depósito es de cuatrocientos dólares y es una retención en la tarjeta de crédito, no un pago; el dinero vuelve a la tarjeta al devolver el carro / Rental at a Quito agency: the deposit is four hundred dollars and it is a hold on the credit card, not a payment; the money returns to the card when the car is returned
- El conductor debe tener más de 21 años; Emma y Mateo manejan y los dos están en el contrato; el carro se alquila dos días (sábado y domingo) y regresan el domingo por la tarde / The driver must be over 21; Emma and Mateo both drive and both are on the contract; the car is rented for two days (Saturday and Sunday) and they return Sunday afternoon
- Cronología: pocos días antes Emma reserva el carro (c37); el viernes por la tarde lo recoge (c36); el viernes por la noche Emma y Mateo preparan las mochilas en el departamento de Emma en Guápulo (c39); el sábado a las 6 a. m. salen y paran en la gasolinera (c38); el sábado Emma manda un mensaje de voz a Daniela desde Baños (c40) / Timeline: days before, Emma books the car (c37); Friday afternoon she picks it up (c36); Friday night Emma and Mateo pack in Emma's Guápulo apartment (c39); Saturday 6 a.m. they leave and stop at the gas station (c38); Saturday Emma sends Daniela a voice message from Baños (c40)
- Emma vive sola en Guápulo (ya no en La Mariscal) / Emma lives alone in Guápulo (no longer in La Mariscal)
- Trato: Empleada y Despachador tratan de usted a Emma (y ella a ellos); Emma y Mateo se tutean; Emma y Daniela se tutean / Forms of address: the Empleada and the Despachador use usted with Emma (and she with them); Emma and Mateo use tú; Emma and Daniela use tú
- Gasolinera: Emma pide veinte dólares, el Despachador le aconseja llenar el tanque y el total es de cuarenta dólares; la próxima gasolinera está a cuarenta kilómetros; Mateo y Emma revisan la llanta de repuesto / Gas station: Emma asks for twenty dollars, the attendant advises filling the tank and the total is forty dollars; the next gas station is forty kilometers away; Mateo and Emma check the spare tire
- Mochilas: Emma lleva impermeable, chaqueta y sudadera; Mateo lleva botas de caucho y le presta guantes a Emma; descargan el mapa y llevan una linterna; Mateo llega a las cinco y media y salen a las seis / Backpacks: Emma takes a raincoat, jacket and sweatshirt; Mateo takes rubber boots and brings gloves for Emma; they download the map and take a flashlight; Mateo arrives at five thirty and they leave at six
- Viaje: neblina, chaparrón y un derrumbe pequeño a las ocho que les hace perder una hora (desvío); llegan al Pailón del Diablo a las diez con mucha gente; Emma maneja casi todo el camino y Mateo el último tramo; vuelven a Quito al día siguiente / Trip: fog, a downpour and a small landslide at eight that costs them an hour (detour); they reach the Pailón del Diablo at ten with many people there; Emma drives most of the way and Mateo the last stretch; they return to Quito the next day

## Sin resolver
- «Pailón del Diablo» (c40, tabla «To read») es un nombre propio y la regla dice que no lleva fila, pero el validador marca «pailón» y «diablo» como no enseñadas si se quita; se deja la fila. Solución limpia: añadir «Pailón» y «Diablo» a `palabrasLibres` de curso.json (fuera de mi alcance).
- Las filas «To read» que quedan (revisamos, completo, una cosa más, llevarlo, alquilar, pague, veintiocho, en caso de que, llamemos, más adelante, pregunte, revisemos, volvamos, caminen, la carretera, por si acaso, llévate, descarga, anochece, varios, hubo, perdimos, manejé / manejó, el último tramo, nos divertimos, el Pailón del Diablo) siguen porque B2–B7 no enseñan esas formas (comprobado quitándolas: el validador falla). Ninguna tabla pasa de 9 filas. Conviene repetir la prueba cuando exista n4-b01 (hoy es esbozo con solo el vocabulario de las fichas).
- c40, evaluación e4 (ficha): el audio dice «llegamos a la cascada a las cuatro» mientras el diálogo dice que llegan a las diez. Son frases independientes, así que no se contradicen en una sola lectura; se deja como manda la ficha.
- c38, situacion: en la ficha propone Mateo revisar la llanta; en el borrador Mateo pregunta y Emma propone «Revisemos». El hecho (revisan la llanta de repuesto) y las preguntas de comprensión no cambian.
- c37, ejemplos: «Hace falta que la licencia tenga un año de antigüedad» ilustra la antigüedad del permiso (palabra de la ficha), pero no es un requisito del alquiler en el diálogo; no entra en el canon.

Total: 11 correcciones (1 altas, 6 medias, 4 bajas)
