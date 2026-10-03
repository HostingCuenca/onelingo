GO

## Validación
`python3 tools/curriculo/validar_bloque.py es 1 7` → 0 error(es) del bloque (antes y después de las correcciones). Los nombres propios Guayaquil, Cuenca y Loja no dieron problema: ya están en `palabrasLibres` de `assets/contenido/es/ruta/curso.json`.

## Correcciones
- [apoyo-en] c31, p2: «Their plurals are inteligentes and jóvenes and joven gets an accent mark in the plural» → «…jóvenes (joven adds -es and gets an accent mark in the plural)» (baja)
- [explicación-falsa] c33, p4 (tabla del/al): la columna «Never written like this» contenía «de la tienda» y «a la tienda» (formas correctas) y reproducía con audio «de el parque» y «a el mercado» → tabla «The pieces / Always written like this» con celdas de apoyo («de + el parque») y solo formas correctas (del parque, al mercado, de la tienda, a la tienda, Voy al mercado.) (media)
- [reparto] c33, p2: «La farmacia está enfrente del hotel y el banco…» → «La farmacia está enfrente de la tienda y el banco está al lado de la farmacia» (el hecho fijo es farmacia enfrente de la tienda) (media)
- [reparto] c33, g2: «La farmacia está enfrente del parque» (y distractores) → «La iglesia está enfrente del hotel» (consigna, opciones y feedback), para no contradecir farmacia enfrente de la tienda; sigue evaluando enfrente + del (media)
- [plan-ficha] c33, e2: hueco «al ___ del banco → lado» (solo evaluaba el sustantivo) → «___ del banco → al lado» con opciones al lado / enfrente; evalúa «al lado de» + «del» como pide la ficha en un solo hueco (media)
- [aceptadas] c33, i3, e5, e6: solo con sujeto → añadidas «Está cerca del hotel.», «Está enfrente del mercado.», «Está detrás del mercado.» (baja)
- [idioma-es] c34, p4 (tabla): «No hay un cajero aquí.» → «No hay cajero aquí.» (con negación lo natural es sin artículo, como dice la explicación) (baja)
- [aceptadas] c34, i3: añadida «Está cerca del hotel.» (baja)
- [explicación-falsa] c35, p2: la nota de ser de / venir de decía que «Vengo de Chicago» y «Soy de Chicago» eran casi lo mismo y que ambos eran naturales para vivir/crecer → explica que «soy de» dice el origen (pregunta habitual ¿De dónde eres?), «vengo de» el lugar del que uno viene, y que ¿De dónde vienes? también se usa al conocer a alguien de otra ciudad o país, que es como la usa la clase (media)
- [explicación-falsa] c35, errorFrecuente «Estoy de Chicago»: «“I'm from Chicago” is soy de or vengo de, never estoy de» → «Estar does not say where you are from. For “I'm from Chicago” use soy de Chicago (origin) or vengo de Chicago (where you come from)» (media)
- [pedagogía] c35, situación, línea 3: la Chica respondía sin que nadie le preguntara → Emma añade «Y tú, ¿de dónde vienes?» (con traducción) (baja)
- [plan-ficha] c35, vocabulario: «el país» y «la ciudad» no están en la ficha y no se usaban → sustituidos por «Estados Unidos», «México» y «Ecuador» (palabras de la ficha; nota de pronunciación de México con la «h» fuerte); refs del paso p3 actualizadas (media)
- [apoyo-en] c35, p2 y tabla p4: «Venimos is regular» → «Venimos keeps its e» (baja)

## Hechos del reparto confirmados
- Don Jorge es alto y serio / Mr. Jorge is tall and serious
- Señora Rosa es baja y muy simpática / Mrs. Rosa is short and very nice
- Daniela es alta, inteligente y divertida / Daniela is tall, intelligent and fun
- Mateo es alto, tiene el pelo corto y negro, lleva lentes y una chaqueta azul / Mateo is tall, has short black hair, and wears glasses and a blue jacket
- Emma y la Recepcionista del hotel de La Mariscal se tratan de usted; Emma y Mateo se tutean / Emma and the hotel Receptionist (La Mariscal) use usted; Emma and Mateo use tú
- Emma le habla de usted a doña Carmen y ella la tutea (le dice «Emma») / Emma uses usted with Doña Carmen and she uses tú with Emma
- En la tienda de La Floresta, la farmacia está enfrente de la tienda y el banco al lado de la farmacia / At the La Floresta corner store, the pharmacy is across from the store and the bank is next to the pharmacy
- En un hotel de La Mariscal hay un cajero enfrente de una farmacia y un restaurante en la esquina / Near a hotel in La Mariscal there is an ATM across from a pharmacy and a restaurant on the corner
- Emma viene de Chicago y Mateo viene de Guadalajara / Emma comes from Chicago and Mateo comes from Guadalajara
- En la fiesta de amigos de Daniela, un chico viene de Cuenca y una chica de Guayaquil (sin nombre, todos de tú) / At the party of Daniela's friends, a guy comes from Cuenca and a girl from Guayaquil (unnamed, all use tú)

## Sin resolver
- Las oraciones de práctica de c33 son sueltas y no forman un mapa único (p. ej. «el banco está enfrente del mercado» en e5 frente a «el mercado está entre el banco y el parque» en i4, ambos fijados por la ficha). Solo se unificó lo que contradecía el diálogo o el hecho fijo de la farmacia.
- En c34, e4 y g2/e2 usan «farmacia enfrente del hotel» y «cajero enfrente de la farmacia»: coherente con el hotel de La Mariscal de c34, no con La Floresta de c33. Se dejó así; si se prefiere, el coordinador puede añadir el hecho «en La Mariscal, la farmacia está enfrente del hotel».
- «¿De dónde vienes?» como pregunta de origen en una fiesta viene de la ficha; en la vida real lo habitual es «¿De dónde eres?». La explicación de c35 lo reconoce, pero conviene que c35 no se tome como sustituto de ser de.

Total: 13 correcciones (0 altas, 7 medias, 6 bajas)
