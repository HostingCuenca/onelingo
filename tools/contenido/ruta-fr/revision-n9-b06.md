# Revisión N9 · B6 (fr.n9.c26–c30)

GO

Validación: `validar_bloque.py 9 6` da 0 errores del bloque; `validar_plan.py fr` no marca «título de la unidad difiere» para c26–c30.

## Comprobaciones

- Cada clase enseña lo que dicen sus fichas (títulos, objetivos, gramática, introduce/recicla, vocabulario de 8 palabras, situación y tarea) y trae los ejercicios del plan (5 guiados, 4 independientes, 2 de comprensión, 6 de evaluación con tarea abierta); nada de clases posteriores (c31 en adelante).
- Brief 13: todos los `escribir` abiertos tienen `abierta: true` y su modelo supera `minimoPalabras`.
- Brief 14: todas las opciones de `elegir`/`escuchar` están en francés (comprobado por script: ninguna en es/en).
- Brief 15: las tablas «Para leer…» tienen entre 0 y 5 filas (c26: ninguna; c27: 5; c28: 3; c29: 3; c30: 4). Las filas son lemas o expresiones reales (un indicateur, un axe, améliorer, concerner, interpréter, un tableau, une estimation, impersonnel, recevoir, le suivi, souhaiter, viable, un échantillon, souffrir de, vague) con frase y sentido; las formas conjugadas (reçoive, ait, souffre…) solo aparecen dentro de la frase de ejemplo y glosadas, y no hay nombres propios. El problema conocido de filas con formas flexionadas ya estaba resuelto en el borrador recibido.
- Tipografía: U+202F antes de ? ! : ; y dentro de « » (se normalizó lo que añadí); apóstrofo ’ en todo el bloque.
- Hablantes: solo «Le conseiller», «Madame Mercier», «Ana» y «Hugo». Tratamiento: Ana-Mercier y Ana-conseiller con vous; Ana-Hugo con tu.

## Correcciones

- c27 y c29, explicación 1 (es/en): «moldes»/“molds” → «estructuras»/“patterns” (español e inglés más naturales).
- c27, e6 (modelo abierto): 71 → 111 palabras (más cercano a «150 palabras» de la tarea; contiene 5 construcciones à + infinitivo y 2 relativizaciones); `minimoPalabras` 50 → 60.
- c28, g4 (ordenar): `aceptadas` + «82 % des clients, selon l’enquête de mars, sont satisfaits.» (orden natural omitido).
- c28, i1 (completar): `aceptadas` + «apparait» (grafía sin acento circunflejo, válida en la ortografía rectificada).
- c28, e5 (relacionar): la consigna decía «con su modo» pero dos pares no eran modos → «Une cada expresión con su función»; glosas más distintas: «Un hecho, en indicativo» / «Una estimación, en condicional» / «Fórmula impersonal de constatación» / «Cita de la fuente» (antes «Hecho (indicativo)» y «Impersonal de constatación» se solapaban).
- c28, e6: modelo 63 → 95 palabras (esqueleto + capítulo de constats con fuente, indicativo y condicional).
- c28, situación: +2 réplicas (Hugo sobre títulos precisos del sommaire; Ana relee hechos/estimaciones). 413 → 460 palabras (mínimo del nivel: 400).
- c29, vocabulario «à court terme» (es/en) y e1 (feedback): «próximos días o semanas» → «próximos meses», para que cuadre con g3 («Dentro de tres meses»).
- c29, situación: se quitó la frase «Le conditionnel est volontaire» (la frase anterior no era condicional); +2 réplicas (coste de la mise en œuvre de las dos primeras recomendaciones). 399 → 437 palabras (estaba por debajo de 400).
- c30, explicación 1 (es/en): se quitó la falsa afirmación de que las cuatro locuciones van «todas seguidas por nous concluons que» (ahora «suelen abrir una frase como…»).
- c30, g3 (relacionar): glosas casi sinónimas («Teniendo en cuenta lo comprendido» / «En consideración a») → «A la vista de lo expuesto» / «Con respecto a un criterio» / «A partir de lo que se ha comprendido» / «En consideración a una razón» (coherentes con la pista y la explicación).
- c30, e5 (relacionar): consigna «parte» → «término» (el decisor no es una parte); «Un hecho jerarquizado y matizado» → «Una conclusión que dice hasta dónde llega».
- c30, e6: modelo 75 → 104 palabras; `minimoPalabras` 50 → 60.
- c30, situación: +2 réplicas (por qué empezar por la satisfacción). 402 → 430 palabras.

## Hechos del reparto confirmados

- Ana presenta a Monsieur Perrot, asesor del banco (en francés «Le conseiller», vous), las cuentas anuales de la agencia por encargo de Madame Mercier: ventas 1,2 M€ contra 900 000 € en 2025, margen bruto 12 % contra 8 %, gastos fijos 300 000 € (25 % contra 33 % de las ventas), resultado de explotación 85 000 € contra 40 000 €, beneficio neto 60 000 €, tesorería 150 000 € (seis meses de gastos fijos) y umbral de rentabilidad alcanzado en septiembre contra noviembre; el préstamo servirá para abrir una oficina en Lyon / Ana presents the agency’s annual accounts to Monsieur Perrot, a bank advisor (“Le conseiller”, vous), at Madame Mercier’s request: sales 1.2 M€ against 900,000 € in 2025, gross margin 12% against 8%, fixed costs 300,000 € (25% against 33% of sales), operating result 85,000 € against 40,000 €, net profit 60,000 €, cash 150,000 € (six months of fixed costs) and break-even reached in September against November; the loan is meant to open an office in Lyon
- Ana comenta ante Madame Mercier (vous) el cuadro de mando trimestral: tasa de ocupación 78 % contra 70 %, satisfacción de 80 % a 82 % (cuestionario propio, solo 40 % de respuesta), cancelaciones de 4 % a 7 % (solo grupos escolares); no concluye que la nueva guía mejoró la satisfacción (correlación no es causalidad) / Ana comments to Madame Mercier (vous) on the quarterly dashboard: occupancy rate 78% against 70%, satisfaction from 80% to 82% (own questionnaire, only 40% response rate), cancellations from 4% to 7% (school groups only); she does not conclude that the new guide improved satisfaction (correlation is not causation)
- Informe de Ana sobre la satisfacción: encuesta de marzo con 300 cuestionarios y 120 respuestas (40 %), 82 % de clientes satisfechos, plazo de respuesta de cinco a tres días, 90 % recomienda a los guías; Hugo (servicio de patrimonio de la alcaldía, se tutean) revisa el estilo y la separación entre hechos y análisis / Ana’s satisfaction report: March survey with 300 questionnaires and 120 answers (40%), 82% of customers satisfied, response time down from five to three days, 90% recommend the guides; Hugo (city heritage department, they use tu) reviews style and the separation of facts and analysis
- Recomendaciones del informe (Mercier, vous): responder a los correos en 24 h (chantier prioritaire; hoy son tres días), mensaje de seguimiento a cada cliente, servicio al cliente de dos personas, formar a los guías en español y, a largo plazo, una oficina en Lyon si las cifras lo permiten; desaconsejan cambiar los precios este año; Mercier pide un responsable y una fecha por medida y un primer balance del chantier prioritario en un mes / Report recommendations (Mercier, vous): answer emails within 24 h (priority project; today it takes three days), a follow-up message to each customer, a two-person customer service, training the guides in Spanish and, in the long term, an office in Lyon if the figures allow it; they advise against changing prices this year; Mercier asks for an owner and a date per measure and a first review of the priority project in one month
- Resumen ejecutivo de una página (≈ 200 palabras): tres conclusiones matizadas (satisfacción buena pero a relativizar, plazos de respuesta como punto débil, guías bilingües apreciados), límites (muestra de 120 respuestas, período de tres meses) y decisión pedida: validar el plan de acción en tres etapas (correos y seguimiento en el mes; servicio al cliente y formación en el año; oficina de Lyon si las cifras lo permiten); Mercier lo presenta mañana / One-page executive summary (about 200 words): three qualified conclusions (good satisfaction but to be qualified, response times as the weak point, bilingual guides appreciated), limits (120 answers, three-month period) and the decision requested: approve the three-step action plan (emails and follow-up within the month; customer service and training within the year; Lyon office if the figures allow it); Mercier presents it tomorrow

## Sin resolver

- Las situaciones tienen 430–460 palabras de diálogo (más el contexto): dentro del rango 400–700 del nivel, pero por debajo de las ≈ 500–600 que sugieren las fichas de c28 y c30; ampliarlas obligaría a introducir léxico no enseñado.
- Los modelos de las tareas de c28 (95 palabras) y c30 (104) son más cortos que los «200 palabras» pedidos en la tarea; el máximo (250) deja espacio al alumno y el ejercicio no puntúa.
- c26 e1 (escuchar) compara «12 % contre 8 %» con cifras; se mantiene así porque la ficha lo plantea y la opción correcta es única.
- Los porcentajes llevan espacio normal antes de «%» (la regla del proyecto solo exige U+202F antes de ? ! : ;).
