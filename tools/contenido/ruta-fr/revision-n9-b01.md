# Revisión fr.n9.c01–c05 (N9, bloque 1)

GO

Validación: `validar_ruta.py fr --borrador n9-b01.json` → 0 errores (N8 ya está integrado en `assets/contenido/fr/ruta/`; con los borradores n8-b01…b10 antes de integrarse también dio 0). `validar_plan.py fr`: sin «título de la unidad difiere» para fr.n9.c01–c05 (ni para ningún otro).

## Contraste con las fichas
- Títulos, objetivos, `gramatica`, `introduce`/`recicla`, vocabulario (8 palabras exactas de cada ficha) y tarea coinciden. No hay contenido de clases posteriores; la conjugación de tutoyer/vouvoyer (c04) y el subjuntivo «que vous disiez» (c02) vienen de la ficha (ejercicio de c04 i2 y frase de gramática de c02).
- Plan de ejercicios completo: mismo formato y orden en guiada, independiente y evaluación de las cinco clases. Cambio aceptable del autor: la segunda pregunta de la situación pasa de `escribir` (en español) a `elegir` con opciones en francés (calibración 14); la primera conserva el formato del plan.
- Evaluación: 5 ítems puntuables en 5 formatos (escuchar, elegir, ordenar, completar, relacionar) en las cinco clases + el `escribir` de la tarea como `abierta` (no puntúa). Cada modelo abierto cumple su `minimoPalabras`.
- Situaciones (palabras de diálogo, N9: 400–700): c01 426, c02 409, c03 422, c04 416, c05 400 (límite; incluye el correo). Hablantes: nombres o papeles en francés (Ana, Monsieur Girard, Clément, Le modérateur, La guide, Hugo, Madame Mercier, Julien, Maître Fontaine, Madame Perrin, Le courriel).
- Tablas «Para leer…» de 8, 2, 4, 5 y 0 filas: ayudas reales con sentido y frase; sin celdas sueltas. Opciones de comprensión y de evaluación en francés. Tipografía: sin espacios simples ni apóstrofos rectos antes de ? ! : ; en ninguna cadena francesa (los títulos de unidad conservan el espacio normal del plan, como en las clases publicadas). Español neutro de América (credencial, capacitación, estadías, folleto, alcaldía) e inglés americano correctos. Guías de sonido: ü/ö definidas en la primera tarjeta de cada clase, g/j = «sh» (es) / «zh» (en), nasales conforme a la calibración 6.

## Correcciones aplicadas (clase, ítem, antes → después)
- **Todas las clases, vocabulario:** el autor había añadido tarjetas visibles solo para nombres propios (v-nom-girard, v-nom-lefevre = Madame Mercier, v-nom-clement, v-nom-garnier = Maître Fontaine, v-nom-perrin, v-lieu-dijon). Girard, Mercier, Clément, Fontaine, Perrin y Dijon están en `palabrasLibres` → se quitan del `vocabulario` de la unidad y de `refs`; quedan las 8 palabras de la ficha.
- **c01, g3 (ordenar):** faltaba el orden con «Et vous ?» al final → `aceptadas` «Dans quoi travaillez-vous, et vous ?»; la pista dejaba un único orden → «Dans quoi» va antes del verbo invertido, lo más natural es abrir con «Et vous,».
- **c01, g4 (relacionar) y tabla p4:** «Pedir una precisión» y «Pedir que desarrolle» eran glosas casi iguales → «Pedir que aclare lo que dijo» / «Preguntar en qué consiste algo» (es/en, también en la tabla); pista y feedback ajustados.
- **c01, i1 (completar):** «___ le salon» admitía «dans» → la consigna fija «la preposición que expresa el motivo de la visita».
- **c01, e3 (ordenar):** se añaden «Cette année, êtes-vous ici pour la première fois ?» y «Êtes-vous ici cette année pour la première fois ?».
- **c01, situación (traducciones):** «des groupes en automne» se traducía «grupos de adultos» (no está en el francés) → «grupos»; «Chez nous aussi…» con español torpe → «En nuestra región también suelen ser los propios habitantes quienes muestran la zona a los grupos» (en: same idea).
- **c02, g2 (completar):** «Au fait, vous connaissez Hugo ?» también era válido → la frase pasa a «Elle parle cinq langues ; ___, elle est aussi guide.» (solo d’ailleurs); feedback es/en actualizado.
- **c02, g3 (relacionar):** «Por cierto, además» (d’ailleurs) chocaba con «Cambiar de tema» (au fait) → «Añadir un dato que refuerza lo dicho» / «Add a detail that reinforces what was said».
- **c02, e4 (relacionar):** el hueco «___, j’en cherche un !» admitía d’ailleurs y repetía i1; la segunda frase repetía g2 → «— Vous cherchez un guide ? — ___, j’en connais un !» y «Il connaît bien Paris ; ___, il y habite depuis dix ans.»
- **c02, i4 (ordenar):** se añade «Au fait, ce soir, vous savez qui anime l’atelier ?».
- **c02, situación:** «pour des petits groupes» → «pour de petits groupes» (norma del francés cuidado de C1; coincide con c05).
- **c03, contexto de la situación:** «Todos se tratan de usted» contradecía el reparto (Ana tutea a Hugo) → «El moderador trata de usted a los participantes» (es/en). En el diálogo Ana y Hugo no se hablan directamente.
- **c03, g3 (ordenar):** se añade «Pour des groupes scolaires, en tant que chargée de projet, j’organise des circuits culturels.»
- **c03, e2 (completar):** «organiser» también encajaba → la consigna pide el verbo que significa «dirigir y coordinar» (es/en).
- **c03, v-charge-projet (es):** «pro-shé» → «pro-she» (projet = e abierta).
- **c04, e2 (completar):** «Madame Fontaine» también era válido → la consigna dice «el título que se usa para dirigirse a una abogada»; `aceptadas` suma «Maitre» sin acento.
- **c04, g5 (completar):** «fórmula de cortesía de quien acepta tutear» era falso (la dice quien invita) → «de quien invita al otro a tutearlo».
- **c04, e5 (ordenar):** se añade «Veuillez agréer l’expression de mes salutations distinguées, Madame la Directrice.»
- **c04, situación (cronología):** c01 pone a Ana «depuis trois semaines» en la agencia y c04 era su «première vraie journée» → «Lundi matin. Je suis à l’agence depuis deux semaines.» (es/en); sigue siendo «nueva» y no conoce aún a Julien.
- **c04, situación (es):** Ana saluda «Bonjour, Maître» por la tarde; es decía «Buenos días» y en «Good afternoon» → «Buenas tardes».
- **c05, e2 (completar):** «retenir» también encajaba → la consigna pide el verbo que significa «acaparar».
- **c05, i3 (completar):** «recontacter» (palabra de la clase) es equivalente → `aceptadas` suma «recontacter».
- **c05, situación (es):** «como previsto» → «como estaba previsto».

No se quitó ni renombró ninguna palabra francesa de los pasos de enseñanza salvo las tarjetas de nombres propios; sus nombres siguen apareciendo en ejemplos y diálogos y son `palabrasLibres`. Los cambios en frases (g2 y e4 de c02, «de petits groupes», «depuis deux semaines») usan solo palabras ya enseñadas (validador 0 errores). Ningún bloque posterior de N9 usa esas tarjetas (comprobado con b02–b09: solo b05 menciona a Julien).

## Hechos del reparto confirmados
- Ana, chargée de projet en una agencia de turismo cultural de París dirigida por Madame Mercier (vous), lleva dos semanas allí en c04 y tres en c01; prepara circuitos a la medida para grupos extranjeros, escolares y empresas (c01, c03, c04) / Ana, a project manager at a cultural tourism agency in Paris run by Madame Mercier (vous), has been there two weeks in c04 and three in c01; she prepares tailor-made tours for foreign groups, school groups and companies (c01, c03, c04)
- Ana abre una conversación con Monsieur Girard, expositor de la oficina de turismo de Lyon (recorridos en torno a la seda y la cocina), en el cóctel del Salón del turismo cultural de París; Madame Mercier los ve (c01) / Ana starts a conversation with Monsieur Girard, an exhibitor from the Lyon tourist office (routes around silk and food), at the Cultural Tourism Fair cocktail in Paris; Madame Mercier sees them (c01)
- Clément, colega de otra agencia de viajes (se tratan de vous), lleva seis años preparando circuitos a pie en la Provenza; su primer viaje a pie fue en Ecuador; usan el mismo traiteur de Marseille que la agencia de Ana; hablan del salón de Lyon en noviembre (c02) / Clément, a colleague from another travel agency (they use vous), has prepared walking tours in Provence for six years; his first trip on foot was in Ecuador; he uses the same Marseille caterer as Ana’s agency; they mention the Lyon fair in November (c02)
- Ana camina todos los fines de semana, hacía excursiones con su padre en Quito, preparó un recorrido literario por París y le gustan los museos de barrio, los libros viejos y los relatos de viaje (c02) / Ana walks every weekend, went hiking with her father in Quito, prepared a literary route through Paris, and likes neighborhood museums, old books and travel narratives (c02)
- Hugo trabaja en el servicio de patrimonio de la alcaldía y dirige visitas gratuitas de los barrios antiguos que hacen los propios habitantes; se presenta en un encuentro de jóvenes profesionales del turismo, donde Ana también se presenta; Ana lo tutea (c03) / Hugo works at the city hall heritage department and runs free tours of old neighborhoods led by residents; he introduces himself at a meetup of young tourism professionals where Ana also introduces herself; Ana uses tu with him (c03)
- Julien, colega joven del servicio de reservas, de edad casi igual a la de Ana, la tutea y es quien propone el tuteo; la jefa de servicio es además la autora de la guía de la agencia (c04) / Julien, a young colleague in the reservations department, almost Ana’s age, uses tu with her and is the one who suggests it; the head of department is also the author of the agency’s guide (c04)
- Maître Fontaine es la abogada que revisa un contrato de Ana; se tratan de vous (puede decirse «Maître» o «Madame Fontaine») (c04) / Maître Fontaine is the lawyer who reviews a contract for Ana; they use vous (one may say “Maître” or “Madame Fontaine”) (c04)
- Madame Mercier prefiere «Madame» y «Cordialement» en los correos diarios; Ana no le propone el tuteo (c04) / Madame Mercier prefers “Madame” and “Cordialement” in everyday emails; Ana does not suggest tu to her (c04)
- Madame Perrin, directora de un hotel de Dijon (se tratan de vous), prepara para otoño un fin de semana de vino e historia para parejas y pequeños grupos de amigos; quedan en un café el jueves a las diez y Ana le envía el correo de seguimiento (c05) / Madame Perrin, director of a hotel in Dijon (they use vous), is planning a fall weekend about wine and history for couples and small groups of friends; they agree on a coffee on Thursday at ten and Ana sends her the follow-up email (c05)

## Sin resolver
- **Julien repetido en N9-b05 (c23):** `n9-b05.json` usa «Julien» para el candidato a guía al que Ana entrevista; aquí Julien es el colega de reservas (c04). Con un mismo nombre y dos papeles distintos choca con el reparto: conviene renombrar uno de los dos (en N8 el coordinador ya cambió un «Julien» a «Mathieu» por lo mismo). No toqué b05.
- c01–c05 no afirman un orden cronológico; solo c01 («depuis trois semaines») y c04 («depuis deux semaines») fijan antigüedad y son coherentes entre sí.
- Los títulos de unidad conservan un espacio normal antes de «?» / «!» (como las clases publicadas); si el integrador quiere U+202F también en títulos, hay que cambiarlo a la vez en el plan.
- c05: la situación mide justo 400 palabras (límite inferior de N9); el correo se cuenta dentro. Si se quiere margen, añadir una réplica breve.
