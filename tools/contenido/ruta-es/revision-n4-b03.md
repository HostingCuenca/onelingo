GO

## Validación

`python3 tools/curriculo/validar_bloque.py es 4 3` → 0 error(es) del bloque (esbozo: n4-b01, que solo tiene 3 de 5 unidades; B2 es real y completo). El JSON sigue siendo válido. Diálogos de situación: 173, 160, 170, 154 y 154 palabras (rango 150–250). Tablas «To read»: 10–11 filas (≤ 15). Un solo `___` por `completar`; lectura abierta de c15 con modelo de 40 palabras (mínimo 30). Títulos de unidad solo en inglés. Sin vosotros ni peninsularismos en el español meta (el único «grifo» queda como nota de reconocimiento).

## Correcciones

- [reparto] c13, p9 contexto: «Emma ya se mudó y hoy firma» → escena una semana antes de la mudanza (después de la visita de c11, antes de que se dañe el calefón de c12) (alta)
- [reparto] c13, p9 diálogo, 2.ª línea de Emma: «Ya vivo en el departamento y me gusta mucho» → «Me gusta mucho el departamento y quiero vivir allí» (alta)
- [pedagogía] c13, p9 diálogo: dos líneas seguidas de Emma → una sola línea (baja)
- [aceptadas] c13, e3: «Yo no estoy dispuesta a pagar más.» no se puede armar con los tokens → eliminada de `aceptadas` (baja)
- [idioma-es] c12, vocabulario v-grifo: «el grifo» (peninsular) → «la llave del agua», con nota que desambigua «llave» (key) y reconoce «grifo» solo como forma de España (media)
- [idioma-es] c12, i4 relacionar: «Voy a mandar a arreglar el grifo.» → «…la llave del agua.» y feedback ajustado (media)
- [pedagogía] c12, p2 explicación: «Voy a mandar a arreglarlo» (clítico no enseñado, contradice la ficha) → «Voy a mandar a arreglar el calefón» (media)
- [explicación-falsa] c12, errorFrecuente «Me dañó el calefón»: «on purpose or by fault» (inexacto) → explicación del contraste me dañó / se me dañó (baja)
- [pedagogía] c12, p5 tabla «To read», fila «mandé, mandó»: forma ya enseñada en B2 (c06, c10) → marcada como «Review» (baja)
- [pedagogía] c14, p5 tabla «To read»: filas «ver», «así es» (sin uso en la clase) y «reviso» (ya enseñada en B2 c08) eliminadas (baja)
- [explicación-falsa] c15, p2 explicación: «With usted and ustedes you use se» (usted solo no puede ser recíproco) → solo ustedes, con aclaración (media)
- [explicación-falsa] c15, errorFrecuente «uno al otro»: «English says one another in the singular» (falso) → «uno al otro» solo para dos personas, «unos a otros» para el grupo (media)
- [aceptadas] c15, e5: «Nosotros nos ayudamos con mis vecinos» (otro sentido) → eliminada (baja)
- [pedagogía] c15, p5 tabla: filas duplicadas «ofrecer» y «ofrece, ofreció» → una sola («ofrecer, ofrece, ofreció») (baja)
- [explicación-falsa] c15, vocabulario ayuda mutua, nota de pronunciación: solo cubría «mutua» → «ah-YOO-dah MOO-twah» (baja)

## Hechos del reparto confirmados

- Emma ve un departamento en Guápulo con la Agente inmobiliaria (usted entre ambas); quiere uno con un cuarto y vista a la ciudad, que no cueste más de 400 dólares; no tiene carro, no necesita garaje; la Agente tiene uno de un cuarto, amplio y soleado, de 380 dólares al mes, con balcón, amoblado y céntrico; cita el lunes a las 10. / Emma views an apartment in Guápulo with the real estate Agente (usted both ways); she wants one bedroom and a view of the city, under $400; she has no car so no garage; the agent has a one-bedroom, spacious, sunny, furnished, central apartment with a balcony for $380 a month; viewing Monday at 10.
- Contrato de Guápulo: 380 dólares al mes, contrato de un año, un mes de garantía (la Casera pide dos al principio y acepta uno); regla del edificio: no hacer ruido después de las diez de la noche; la Casera (sin nombre) y Emma se tratan de usted. La firma es una semana antes de la mudanza. / Guápulo lease: $380 a month, one-year contract, one month's deposit (the Casera first asks for two, then accepts one); building rule: no noise after 10 p.m.; the Casera (unnamed) and Emma use usted. Signing happens a week before the move.
- Un miércoles por la mañana se le daña el calefón a Emma (ya vive sola en Guápulo); la Casera lo manda arreglar «mañana por la tarde» con su plomero de confianza (no deja que Emma lo mande y descuente el costo del alquiler). / One Wednesday morning Emma's water heater breaks (she already lives alone in Guápulo); the Casera will have it fixed «tomorrow afternoon» by her trusted plumber (she doesn't let Emma do it herself and deduct it from the rent).
- Emma llama al Plomero un miércoles por la tarde (usted entre ambos): quedan en que viene el jueves a las cuatro (su ventana es de cuatro a seis); la visita cuesta 30 dólares y los repuestos se pagan aparte; él avisa si hace falta un repuesto. / Emma phones the Plomero on Wednesday afternoon (usted both ways): they agree he comes Thursday at four (his window is four to six); the visit costs $30 and spare parts are paid separately; he will tell her if a part is needed.
- La Vecina de al lado (señora mayor, usted con Emma) le ofrece su ducha el miércoles por la noche y el jueves por la mañana; hay una reunión de vecinos el jueves por la noche en la portería; los vecinos se saludan, se prestan herramientas, se dejan recados en la portería y se ayudan. / The next-door Vecina (older lady, usted with Emma) offers her shower Wednesday night and Thursday morning; there is a neighbors' meeting Thursday night at the front desk; neighbors greet each other, lend tools, leave messages at the front desk and help one another.
- Emma tutea a Daniela y a Mateo (ejemplos y evaluación: Emma y Daniela se escriben a diario; Mateo y Emma se ven los sábados; Daniela y Emma se llaman todas las noches). / Emma uses tú with Daniela and Mateo (examples and evaluation: Emma and Daniela write to each other daily; Mateo and Emma see each other on Saturdays; Daniela and Emma call each other every night).

## Sin resolver

- La ficha de c12 lista «el grifo»; el borrador lo cambia por «la llave del agua» (decisión del coordinador). Conviene actualizar la ficha del plan para que no vuelva a aparecer «grifo».
- B1 (`n4-b01.json`) tiene solo 3 de 5 unidades, así que el validador lo trata como esbozo. El repaso de B1–B2 se calculó solo contra B2; cuando B1 esté completo conviene volver a comprobar las tablas «To read» de B3.
- La ficha de c14 acepta «vendrá» junto a «viene»; no se añadió porque la consigna fija el presente y el futuro no está enseñado en esta clase (c07 lo introduce como probabilidad en B2).
- El orden cronológico es c11 → c13 (contrato) → mudanza → c12/c14/c15; en el curso c13 viene después de c12. El contexto de c13 lo dice de forma explícita en inglés.
- Los diálogos de c14 y c15 están en el límite bajo (154 palabras); validan, pero no tienen margen si se recorta algo.

Total: 15 correcciones (2 altas, 5 medias, 8 bajas)
