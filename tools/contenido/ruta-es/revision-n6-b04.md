GO

# Revisión es N6 B4 (es.n6.c16–es.n6.c20)

## Validación
- `python3 tools/curriculo/validar_bloque.py es 6 4` → «N6 B4: 0 error(es) del bloque» (antes y después de las correcciones).
- Lecturas (palabras del diálogo): c16 355, c17 347, c18 342, c19 345, c20 340 (todas en 319–355 y las que estaban por debajo de 335 quedaron en 340–380).
- Cada ficha cumple su plan de ejercicios (formato, clave y lo evaluado), 8 ejemplos, 8–9 vocablos, un solo `___` por `completar`, 1 sola respuesta por ítem o `aceptadas` completas, ningún hablante con dos turnos seguidos, sin «vosotros».
- Aritmética comprobada: 480 − 10 % = 432; mitad de 480 = 240; 12 habitaciones × 2 noches × 40 = 960.
- Cronología: c17 llamada un lunes, vuelven a hablar el miércoles; c19 llamada un jueves, hostal de viernes a domingo dentro de tres semanas; c20 llamada un martes, técnico mañana (miércoles), videollamada el jueves; ningún bloque nombra el mes; c18 es «más tarde esa noche» en la misma fiesta de c16 (el abuelo llega después, ahora con «Acaba de llegar»).
- Distractores revisados: todos son errores reales o claramente menos corteses. «Estoy algo molesto» (mujer): el error está en el adjetivo «molesto» y el feedback de c20 g3 lo dice así. «No tienes razón» (c16 e1): el feedback ahora lo marca como negación directa.

## Correcciones
- [idioma-es] c17, situacion (Operador): «Habla el Operador.» → eliminado (autodescribirse por su papel suena artificial) (media)
- [idioma-es] c19, situacion (Agente): «Habla la Agente.» → eliminado (media)
- [idioma-es] c20, situacion (Operadora): «Habla la Operadora.» → eliminado (media)
- [plan-ficha] c17, situacion (Emma): «Aun así, no sé si podemos…» → «Pero no sé si podemos…» (aun-asi se introduce en c46) (alta)
- [pedagogía] c17, situacion: lectura 330 palabras → 347 con cifras comprobables («Con el descuento, son cuatrocientos treinta y dos dólares», «la mitad, doscientos cuarenta dólares», «con salida desde Quito») (media)
- [explicación-falsa] c18, explicacion p2, tabla p7 y situacion: «Por supuesto» solo es ambiguo como respuesta a «¿le importaría?» → «Por supuesto que no» (explicación, fila de la tabla y réplica del Abuelo) (media)
- [reparto] c18, situacion (contexto): sin aviso de que Valentina trata de usted a su abuelo → nota en inglés: «Valentina also uses usted with her grandfather, which is common in Ecuador as a sign of respect.» (media)
- [reparto] c18, situacion (Valentina): el abuelo aparece sin que c16 lo mencione → «Emma, te presento a mi abuelo. Acaba de llegar.» (baja)
- [pedagogía] c18, situacion: lectura 321 → 342 palabras («Me encantan las historias de familia», «Es muy divertida», «y hace mucho calor», «con el pastel») (baja)
- [idioma-es] c19, situacion (Agente): «…para esas fechas ya estamos casi completos, y me temo que no podemos hacer excepciones» (incoherente: nadie pidió una excepción y «esas fechas» confundía con la semana siguiente) → «…para las fechas que usted pidió ya estamos casi completos»; las excepciones pasan a la respuesta sobre el descuento (media)
- [aceptadas] c19, evaluacion e3: faltaba «Me temo que tenemos solo ocho habitaciones» (orden válido con los mismos tokens) → añadida a `aceptadas` (media)
- [pedagogía] c19, situacion: lectura 319 → 345; precio total «novecientos sesenta dólares por las dos noches»; Emma deja de repetir tres veces «le doy mi respuesta mañana» (baja)
- [pedagogía] c20, situacion: lectura 320 → 340 («¿Le parece bien?», «Sí, me parece bien», «y también la velocidad de carga», «y siempre pagamos a tiempo») (baja)
- [pedagogía] c16, evaluacion e1, feedback: «The other two are direct.» → explica que «No tienes razón» niega de frente al otro, para que sea inequívocamente peor que «Yo no lo vería así» (baja)

## Hechos del reparto confirmados
- Fiesta de cumpleaños de Valentina en un restaurante de La Mariscal, 2031: Emma, Kenji y Valentina se tutean; más tarde llega el abuelo de Valentina, a quien Emma trata de usted y Valentina también (cortesía habitual en Ecuador) / At Valentina's birthday party in a La Mariscal restaurant in 2031, Emma, Kenji and Valentina use tú; later Valentina's grandfather arrives, and both Emma and Valentina use usted with him
- Valentina quiere agregar un tercer día a la caminata del páramo; Emma propone ofrecerlo como opcional y Kenji prefiere un solo día más corto; llevan las tres opciones a la reunión del lunes / Valentina wants to add a third day to the páramo hike; Emma suggests it be optional and Kenji prefers a single, shorter day; they take the three options to Monday's meeting
- Valentina revisa la lista de permisos cada semana desde que se canceló un tour / Valentina checks the permit list every week since a tour was canceled
- Bus turístico: 480 dólares ida y vuelta, 10 % de descuento por pago adelantado (432); Emma propone pagar la mitad (240) esta semana y el resto tras el viaje; el Operador propone adelantar la salida de las 6 a las 5 a. m.; Emma y el Operador se tratan de usted; hablan de nuevo el miércoles tras una llamada un lunes / Tourist bus: $480 round trip, 10% discount for advance payment ($432); Emma proposes paying half ($240) this week and the rest after the trip; the Operator proposes moving departure from 6 to 5 a.m.; Emma and the Operator use usted; they talk again on Wednesday after a Monday call
- Hostal de Baños: Emma pidió 12 habitaciones dobles para un grupo (viernes a domingo, dentro de tres semanas) y quedan 8; 40 dólares por noche con desayuno; la semana siguiente hay las 12 juntas (960 dólares por dos noches) y las 4 restantes pueden ir a lista de espera; la Agente y Emma se tratan de usted; llamada un jueves / Baños hostel: Emma asked for 12 double rooms for a group (Friday to Sunday, in three weeks) and only 8 are left; $40 per night with breakfast; the following week all 12 are available together ($960 for two nights) and the other 4 can go on a waiting list; the Agent and Emma use usted; the call is on a Thursday
- Internet de la oficina de Andes Vivos: llamada un martes, lento desde el lunes; técnico al día siguiente entre 9 y 12; videollamada importante el jueves; el técnico anterior vino hace una semana y llegó tarde; clientes desde hace dos años; la Operadora y Emma se tratan de usted / Andes Vivos office internet: call on a Tuesday, slow since Monday; technician the next day between 9 and 12; important video call on Thursday; the previous technician came a week ago and was late; customers for two years; the Operator and Emma use usted
- Emma llegó a Quito en 2026 y vive en Guápulo (sola) / Emma arrived in Quito in 2026 and lives alone in Guápulo

## Sin resolver
- c16 e4: la ficha acepta también «bastan»; no se añadió a `aceptadas` porque el verbo «bastar» no se ha enseñado (la respuesta sin él ya queda cubierta).
- c18 tabla «Review: imperfect subjunctive» muestra solo yo, nosotros y ellos/ustedes (sin tú); no afecta a los ejercicios.
- c17 y c18 usan el papel «Mesero»/«Abuelo» y «Operador» fuera del reparto base; son roles sin nombre aceptables según el encargo.

Total: 14 correcciones (1 altas, 8 medias, 5 bajas)
