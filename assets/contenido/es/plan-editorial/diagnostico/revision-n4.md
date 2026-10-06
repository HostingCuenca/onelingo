# Revisión independiente · diagnóstico español N4

GO

Revisor: claude-reviewer-dx-es · 2026-10-05 · validador `--idioma es`: `n4.json: OK · 18 ítems`.

## Correcciones (antes → después, gravedad)

| Ítem | Antes → después | Gravedad |
|---|---|---|
| lectura.4 | El texto decía que en los dos países se pone un altar para el difunto y que el feriado era común. En Ecuador el altar no es una práctica general y el 2 de noviembre no es feriado federal en México. → Lo común pasa a ser «visitar el cementerio con flores y recordar a los difuntos»; el feriado se dice solo de Ecuador. La opción correcta es «Se visita el cementerio con flores». | Alta (dato falso) |
| escucha.1 | «Antes de llegar a Quito… ya había comido locro en casa de Mateo» contradecía el reparto: Emma come locro con Rosa en Quito. → «Antes de llegar a México, Emma nunca había comido pan de muerto, pero ya había comido locro en casa de Rosa». Opciones: nunca había comido locro / ya había comido pan de muerto / ya había comido locro (correcta). | Alta (incoherencia con la historia) |
| escritura.1 y 2 | Rúbricas demasiado estrechas: rechazaban «Ojalá el casero baje…», «Ojalá me acepten…» y los temas habituales (casa, alquiler, contrato, precio); «ojalá que» y «cada vez hay» dejaban pasar cualquier continuación. → Listas de frases exactas generadas: «ojalá» (+ pronombre o sujeto + verbo en subjuntivo, con o sin «que» y «no»; unas 10 700 frases), «no estoy/estamos/estaría dispuesto/a/os/as a», «cada vez [verbo] más/menos» y vocabulario del tema (vivienda; páramo, turistas, agua, basura…). Se añaden dos aceptadas por ítem. | Alta |
| gramatica.4 | «Aunque mañana ___ mucho» admitía «llueve» (aunque + indicativo con pronóstico conocido). → «No sé cómo estará el clima mañana. Aunque ___ mucho, saldremos de todos modos.» | Media |
| gramatica.3 | «No la dejas en el carro» se podía leer como enunciado. → «Por favor, no ___ en el carro», que fija el mandato. Distractor «dejes la» (pronombre pospuesto) se mantiene como error típico, claramente incorrecto. Feedback explica los dos distractores. | Media |
| escucha.2 | El distractor «El plomero viene el viernes» no respondía a la pregunta (coste). → «La visita es gratis» (mismo tema, contradice «cuesta aparte»). | Media |
| escucha.4 | Distractor «Porque el tanque está roto» inverosímil. → «Porque la gasolinera cierra pronto». Feedback ajustado. | Baja |
| lectura.1 | Opción 2 no figuraba entre los departamentos del texto («Uno con parqueadero y sin balcón»); «le dio dos» poco natural. → «Ninguno, porque necesita parqueadero» (trampa: no lo necesita); «le ofreció dos». | Media |
| lectura.2 | Distractores ajenos al tema (carta de recomendación, póliza). → «La factura del internet» (trampa temática) y «Su documento de identidad»; frase final más natural, con la longitud del nivel (45 palabras o más). | Media |
| lectura.3 | La pregunta no decía «si el cobro fue un error». → consigna precisa; «cinco días hábiles» en el texto y la clave. | Baja |
| gramatica.1 | Feedback hablaba de un futuro que no era opción. → feedback acorde con las opciones (acepten / aceptan / acepto). | Baja |
| vocabulario.1 | Consigna decía «Emma» sin que el texto la nombrara. → «the professional to call for the pipe». | Baja |
| Posiciones | A/B/C = 5 / 2 / 9 → 5 / 6 / 5 (se reordenaron escucha.2, lectura.2, gramatica.4, vocabulario.4). | Media |
| review | PENDING → GO. | — |

Total: 14 correcciones (4 altas, 6 medias, 4 bajas).

## Comprobaciones

- Una sola respuesta defendible por ítem; la clave de `respuesta` es la correcta tras reordenar. Distractores plausibles para quien no domina el punto (pluscuamperfecto negado, «llueve», «la dejas», «vienen»).
- Escucha: ninguna se resuelve sin oír (nunca/ya había comido, cuesta aparte, «en cuanto termine» como futuro aún no cumplido, «en caso de que»).
- Reparto de clases: principio (c01), mitad (c06, c11–c14, c16–c17) y final (c20, c23, c29, c33, c36, c38, c41, c43, c45, c46). Cada ítem prueba un punto N4: pluscuamperfecto (c01), quedar en (c14), en cuanto + subjuntivo (c23), en caso de que (c38), relativo con subjuntivo (c11), correo formal (c16), plazos (c20), mientras que (c41), ojalá (c06), discrepar (c29), imperativo negativo con pronombre (c36), aunque + subjuntivo (c46), plomero (c12), cajero (c17), sendero (c43), gol (c33), estar dispuesto a (c13), habría que y cada vez más (c45, c43).
- Lectura de Día de Muertos: se dice solo lo cierto en ambos países (visita al cementerio con flores, recuerdo de los difuntos); ofrenda con pan de muerto es de México; colada morada y guagua de pan, de Ecuador; el feriado del 2 de noviembre se atribuye solo a Ecuador.
- Español latino neutro con tildes, ¿¡ y concordancias correctos; «departamento», «parqueadero», «tubería», «cajero», sin formas peninsulares. Tratos: Mateo escribe de usted a una señora; sin diálogos Emma–Inés en el banco.
- Apoyo solo `en`, inglés americano; consignas de 45 a 96 caracteres (máximo 110) y únicas; feedback explica de verdad y no cita posiciones.
- Rúbricas probadas con la normalización de la app: pasan el modelo, las 4 aceptadas y 14 + 8 respuestas habituales de alumno N4 (otros verbos, «ojalá que…», sujetos como «el casero» o «Daniela», «no estamos dispuestos», «cada vez es más», «cada vez llegan más», temas de casa y de páramo); fallan inglés, español sin «ojalá»/«habría que», indicativo tras «ojalá» («ojalá encuentro»), «hay que» en lugar de «habría que» y fuera de tema.
- Longitudes: la correcta es la única más larga solo en escucha.3 y lectura.3 (2/16).

## Sin resolver

- El archivo pesa unos 340 KB por las listas de frases de la rúbrica (el francés N4, 230 KB). Aceptable, pero si el compilado crece demasiado conviene recortar las variantes con clítico.
- gramatica.3: «dejes la» es un error que casi nadie comete; se mantiene por indicación del coordinador y porque no admite lectura correcta.
- La rúbrica no verifica la concordancia sujeto-verbo ni el subjuntivo en todos los casos (p. ej. acepta «Ojalá el casero baje» pero no distingue un sujeto desconocido): ver «frases exactas» arriba.
