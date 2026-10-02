# Revisión N3 · B7 (fr.n3.c31–c35) — «Objetos, aparatos, talleres y presupuestos»

GO

Revisor independiente. Archivo revisado y corregido: `tools/contenido/ruta-fr/n3-b07.json` (copia previa a mis cambios en el directorio temporal de la sesión). Validación: `validar_ruta.py fr --borrador n3-b01 … n3-b07` → **0 errores**; `validar_plan.py fr` → 0 errores y ningún «título de la unidad difiere» para fr.n3.c31–c35.

## Veredicto por criterio

- Fidelidad a las fichas: las cinco clases enseñan exactamente título, objetivo, gramática, `introduce` y `recicla` de su ficha; no hay nada de fichas posteriores. Todos los ítems del plan de ejercicios están (mismo formato y misma clave); cada clase añade un `relacionar` en práctica independiente, así que el bloque usa los seis formatos.
- Vocabulario: están las palabras de cada ficha más palabras de apoyo que la gramática necesita (c31 visser, enfoncer, serrer, utiliser; c33 bizarre, freiner, vérifier, prêt; c34 donner, mail; c35 casser, la rouille, la panne, le technicien, l’aspirateur). Todas están en `vocabulario` de la unidad y en un paso de enseñanza.
- Francés de Francia: concordancias, pronombres (orden me/te/nous/vous > le/la/les > lui/leur > y > en), `faire` causativo con `fait` invariable, `ça se + verbo`, `il suffit de`, `si/tellement… que`, `tellement de / tant de`, `ça vaut la peine de`: correctos. Tipografía: U+202F antes de ? ! : ; en todos los campos franceses de pasos, ítems y diálogos; solo ’ (sin apóstrofo recto). Los cuatro títulos con «?» usan espacio normal, igual que el plan y las unidades publicadas de N2; no los toqué para no romper la comparación de títulos con el plan.
- Explicaciones es/en: claras y cortas, es neutro con tú, en americano (second floor, tires, windshield, vacuum cleaner, outlet, e-mail). Sin regionalismos prohibidos (comprobé coche, móvil, piso de vivienda, billete, camarero, ordenador, vosotros, zumo, aparcar, patatas).
- Guías de sonido: «sh» para j/g suave y ch (en inglés «zh»), nasales con «en/an/on» (en inglés con aviso de n muda), ü y ö definidos en el paso de pronunciación de c31 antes del vocabulario. Consonantes finales correctas (tournevis, vis, truc, tactile, fragile sí suenan; outil, devis, acompte, caoutchouc no; en caoutchouc la ch suena «ch» y lo avisa).
- Situaciones: diálogos de 14–18 líneas y 160–190 palabras (rango 150–250), hablantes con nombre o papel francés (Ana, Emma, Hugo, Madame Dubois, Le garagiste, Le technicien), coherentes con sus 2 ítems de comprensión.
- Evaluación: cada clase tiene 5 ítems puntuables en 5 formatos (completar, elegir, escuchar, ordenar, escribir) + 1 `escribir` abierto (`abierta: true`) que no sustituye a ninguno.
- `aceptadas`: órdenes naturales en los `ordenar` con adverbio (d’abord/ensuite/hier/demain) y variantes en los `escribir`.

## Correcciones aplicadas

| Clase | Ítem / paso | Antes → después |
|---|---|---|
| c33 | tabla p4 e ítem i3 (Hugo y el parabrisas) | «Hugo a fait changer le pare-brise.» / «Il l’a fait changer.» → «Madame Dubois a fait changer le pare-brise.» / «Elle l’a fait changer.» (consigna, texto, feedback y glosas es/en ajustados). Motivo: Hugo no tiene auto (N1 c06 y N2 «va siempre en bicicleta»). El ejemplo venía de la ficha. |
| c33 | evaluacion e1 | consigna «Completa: …revisar los frenos» → «Completa con vérifier: …» (sin eso réparer/changer también eran válidos). |
| c33 | practica_independiente i2 / evaluacion e5 | `aceptadas` ampliadas con «mon moteur» / «mon pare-brise» (+ «je veux …»). |
| c34 | situacion (diálogo) | El garagiste daba el importe y luego decía «je vais estimer le montant ce soir» (contradicción). Ahora Ana pregunta «Vous pouvez estimer le montant ?» y él responde con el importe; cierre «Je vous le confirme demain par mail.» (glosas es/en ajustadas; `estimer` sigue usado en la clase). |
| c34 | ejemplos p6 y evaluacion e3 | «deux cents euros TTC» → «deux cent quarante euros TTC» (200 € HT + 20 % = 240 € TTC, igual que el diálogo). |
| c34 | situacion, línea de Ana (es) | «Vivo en el primer piso» → «Vivo en la primera planta alta» (en Latinoamérica «primer piso» puede ser la planta baja; en sigue «second floor»). |
| c32 | situacion, última réplica de Madame Dubois | es «¡Es muy fácil!» / en «very easy» para «C’est très pratique !» → «¡Es muy práctico!» / «very handy!». |
| c32 | practica_guiada g4 / practica_independiente i2 | `aceptadas`: + «On allume l’appareil d’abord.»; + «Le chargeur se branche dans la prise.» |
| c31 | situacion, «Voilà !» | glosa «¡Eso es!» / «Exactly!» → «¡Listo!» / «There you go!». |

No eliminé ni renombré ninguna palabra francesa enseñada: los bloques posteriores del nivel (b08–b10) no se ven afectados.

## Hechos del reparto confirmados

- Ana y Emma arman un armario en su departamento y no conocen los nombres de las herramientas; Hugo las ayuda por videollamada (los tres se tutean), les dice que no necesitan taladro ni sierra, solo el destornillador / en: Ana and Emma assemble a wardrobe in their apartment and don’t know the tool names; Hugo helps by video call (all three use tu) and says they don’t need the drill or the saw, only the screwdriver
- Madame Dubois compra una tableta con pantalla táctil y Ana baja a explicarle cómo se usa; se tratan de vous; Madame Dubois invita un té a Ana (no café) / en: Madame Dubois buys a touchscreen tablet and Ana goes downstairs to show her how to use it; they use vous; Madame Dubois offers Ana a tea (not coffee)
- Ana trabaja en el hotel por la tarde y por la noche está en casa (coherente con N2) / en: Ana works at the hotel in the afternoon and is home in the evening (consistent with N2)
- Madame Dubois tiene un auto pequeño que lleva al garagiste: el motor ya no arranca con frío, ruido al frenar desde hace una semana y un faro roto; hace cambiar las llantas, hacer la vidange y revisar los frenos; está listo el jueves y lo recoge por la tarde (va en autobús mientras tanto); revisó el parabrisas, el embrague y el volante el año pasado / en: Madame Dubois has a small car she takes to the garage: the engine no longer starts when it’s cold, a strange noise when braking for a week and a broken headlight; she has the tires changed, the oil changed and the brakes checked; it’s ready Thursday and she picks it up in the afternoon (she takes the bus meanwhile); she had the windshield, clutch and steering wheel checked last year
- La hija de Madame Dubois (de N2/N3 c13) también repara su auto siempre en ese taller / en: Madame Dubois’s daughter (from N2/N3 c13) always has her car repaired at that same garage
- Ana llama al taller de parte de Madame Dubois (el auto está allí desde el lunes) y dice que vive en la primera planta alta (= second floor), es decir, es su vecina, no su hija / en: Ana phones the garage on Madame Dubois’s behalf (the car has been there since Monday) and says she lives on the French first floor (= second floor), so she is her neighbor, not her daughter
- Presupuesto del taller: 200 € sin impuestos = 240 € TTC, mano de obra y piezas incluidas, sin anticipo, gratis, válido un mes, se paga con tarjeta o en efectivo, se envía por correo al día siguiente / en: The garage quote: €200 before tax = €240 tax included, labor and parts included, no deposit, free, valid for a month, payable by card or cash, e-mailed the next day
- Ana y Emma tienen una aspiradora muy vieja (caucho gastado, tornillo de acero oxidado, muchas averías) que ya no funciona; el técnico cobra 60 € por repararla frente a 100 € una nueva; Emma duda por el precio, pero deciden comprar otra más resistente (modelo de metal) / en: Ana and Emma have a very old vacuum cleaner (worn rubber, rusty steel screw, many breakdowns) that no longer works; the technician charges €60 to repair it vs. €100 for a new one; Emma hesitates over the price, but they decide to buy a sturdier one (metal model)
- Coherentes con lo previo: Madame Dubois viuda y propietaria que vive en la planta baja, Ana en el primer piso, Hugo sin auto, Ana y Emma hacen el aseo con la aspiradora (N2 c15) / en: Consistent with earlier facts: Madame Dubois is a widowed landlady on the ground floor, Ana on the first floor, Hugo has no car, Ana and Emma vacuum with their own vacuum cleaner (N2 c15)

## Pendiente / sin resolver

- Los títulos de c31 y c34 llevan espacio normal antes de «?» (así están en el plan `curriculo/fr/n3.json` y en los de N2 publicados). Si se quiere U+202F, hay que cambiarlo a la vez en el plan y en el borrador.
- Las situaciones de c33 y c35 quedan en 160 palabras aproximadas (el mínimo de «Por nivel» es 150): válidas, sin margen para recortar.
- La ficha de c33 usaba a Hugo como ejemplo del parabrisas (fr.n3.c33 `ejercicios.independiente`); el borrador ahora usa Madame Dubois. Conviene que el coordinador actualice ese ejemplo del plan por coherencia con el reparto.
