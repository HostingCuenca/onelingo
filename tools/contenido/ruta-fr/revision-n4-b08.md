GO

# Revisión N4 · B8 (fr.n4.c36–c40) — viajes y carretera

Revisor independiente (francés de Francia, inglés americano, español neutro de América). Archivo revisado y corregido: `tools/contenido/ruta-fr/n4-b08.json`. Original guardado antes de editar; no se tocó ningún otro archivo ni se ejecutó git.

## Validación

- `python3 tools/validar_ruta.py fr --borrador n4-b01 … n4-b08` (n3-b* ya integrados en `assets/contenido/fr/ruta/`, omitidos; b04 y b05 ya existen): **0 errores**. También 0 errores añadiendo n4-b09 y n4-b10.
- `python3 tools/curriculo/validar_plan.py fr`: ningún «título de la unidad difiere» para fr.n4.c36–c40 (los únicos avisos son c26 de N4 y N5, ajenos a este bloque).

## Contraste con las fichas

Títulos, objetivos, gramática, `introduce`, `recicla`, vocabulario (las 10 / 9 / 9 / 10 / 10 palabras de cada ficha, con artículo; extras del autor: Tahiti, se baigner, passer, réserver en c36; l’assistance, limité, facturer, l’option en c37; recommander en c38; le dépliant, limité à, km/h, rouler, respecter en c39; le papier, en mauvais état en c40, todos enseñados antes de usarse), situación y tarea coinciden con `curriculo/fr/n4.json`. Los planes de ejercicios están completos (5 guiados, 4 independientes, 2 de comprensión y 6 de evaluación por clase; mismo formato y clave; redacción pulida). Nada de c41 en adelante. Reciclaje correcto: futur antérieur y preposiciones de lugar (c36), au cas où / à condition de / sinon (c37), si j’étais vous / subjuntivo con il est… que (c38), nombres, la plupart des, il est interdit / obligatoire de (c39), ne… que, manquer à, faire causativo (c40); `manquer à` es de N3 c15, así que «nivel anterior» es exacto.

Anatomía conforme a «Por nivel» y al encargo: explicaciones (2) → tablas → ejemplos (7–8) → vocabulario → guiada (5, con pista) → independiente (4, sin pista) → situación (c36 156 / c37 172 / c38 160 / c39 153 / c40 152 palabras contadas por espacios, rango 150–250; correo, diálogo, foro, folleto, llamada) → evaluación (5 puntuables en 4–5 formatos + 1 `escribir` con `abierta: true` que no puntúa). Formatos del bloque: los seis (relacionar en c37 e5, c38 e5, c39 g1). Errores frecuentes 3 por clase. Hablantes: Ana, Hugo, Emma (solo mencionada), L’employé, L’opératrice, Un touriste, Un voyageur, Le dépliant (precedente: La brochure, La compagnie). Guías de pronunciación coherentes con las del Nivel 0 (sh para j/g suave, nasales con «en»/«an»/«on», ü y ö definidas en la primera aparición de cada clase).

## Correcciones aplicadas

Todas las clases:
- **Tipografía**: el borrador usaba espacio normal antes de ? ! : ;. Sustituido por U+202F en todo el archivo (49 casos; apóstrofo ’ ya era correcto, 0 apóstrofos rectos).

c36
- Contexto y diálogo[0], Emma «trabaja de noche / la nuit» → «trabaja por las noches / le soir» (es «Tú trabajas por las noches», en «You work in the evenings»): coherente con N3 (Emma solo trabaja en el restaurante de Karim) y con n4-b03 («Elle ne travaille que le soir»).
- i4 (`escribir`, «Esquiamos en los Alpes»): `aceptadas` + «Nous allons en Bretagne. Nous skions dans les Alpes.».

c37
- Diálogo[2], traducción es «¿La caja automática cuesta más cara?» → «¿La caja automática cuesta más?».
- i4 (`escribir`): `aceptadas` ampliadas con las variantes con «on prend» (natural y usada en s2), en ambos órdenes.

c38
- Explicación 1 (es / en): «pronombre (me, te, vous)» → «(te, vous)» («me» no tiene sentido al aconsejar a otra persona).

c39
- Explicación 1 es: «quart y tiers llevan s» era falso (tiers ya termina en s) → «Quart lleva s cuando hay más de uno (trois quarts); tiers ya termina en s en singular y plural». En: igual.
- Explicación 1: la frase «En francés se dice «cent», nunca «ciento»» (es) y «French says pour cent where English says “percent”» (en) no ayudaban ni coincidían → nota útil y paralela: el símbolo % lleva un espacio delante en francés (20 %).
- Situación: eliminada la réplica redundante de Hugo («Le radar, c’est utile : il vérifie la vitesse.»; dos réplicas seguidas con «utile»). Sigue en 153 palabras; s1 y s2 intactas.
- i4 (`escribir`): la consigna fija «verbos en plural, como en la clase» (es / en) porque el singular tras «un quart des conducteurs» también circula; `aceptadas` + «20 pour cent», «20 %» y «20%».

c40
- g3 (`elegir`, «Il ___ de l’huile dans le moteur»): la opción «me manque» también era gramatical («Il me manque de l’huile») → distractor «manques»; opciones manque / manquent / manques; feedback y pista adaptados («el verbo queda en singular, aunque lo que falte sea plural»).
- Error frecuente 1: «Je manque significaría que alguien te echa de menos» era incorrecto → «alguien me extraña» (en: «someone misses me»).
- «echar de menos» (peninsular) → «extrañar» en la explicación 1 («extraño a mi familia») y en la fila de la tabla (manquer à).
- Ejemplo y e1 (es): «Se trata de una falta de gasolina» (calco) → «Se trata de una avería por falta de gasolina».

## Revisado y sin cambios

Preposiciones de regiones, islas y relieve (en Bretagne / dans les Alpes / sur la côte / à la montagne / en Corse / à Tahiti); futur antérieur con d’ici + fecha; en cas de + sustantivo sin artículo; sauf vs sauf si + indicativo (y su error con condicional); au cas où; à condition de; sinon; recommander / déconseiller (à qn) de + infinitivo; il est recommandé / déconseillé de; il est préférable que + subjuntivo (partiez, réserviez, passiez); fracciones, porcentajes y concordancia plural; limité à, au maximum; il manque / il me manque (singular impersonal); il s’agit de; il reste / il ne reste que. Un solo resultado defendible en los ítems (el español de la consigna fija el sentido donde dos formas serían gramaticales, p. ej. c40 g4 «queda» vs «falta»). Todos los `ordenar` aceptan los órdenes naturales (c36 e4, c37 i2 / e4, c38 e4, c39 e4, c40 e4); los `relacionar` tienen glosas claramente distintas; las pistas resuelven cada ítem. Español sin peninsularismos (auto, licencia, llanta, boleto, gasolinera, tanque, ustedes) e inglés americano (gas, tire, highway, license, deductible, ma’am).

## Hechos del reparto confirmados

- Ana y Emma, que viven juntas, planean un viaje de cinco días por Francia (Bretaña, Provenza, vuelta por el suroeste); Ana reserva billetes de tren y avión para el viernes y Emma los hoteles (c36). / Ana and Emma, who live together, plan a five-day trip around France (Brittany, Provence, back through the Southwest); Ana books the train and plane tickets by Friday and Emma the hotels (c36).
- Emma trabaja por las noches (en el restaurante de Karim), por eso Ana le escribe en vez de hablarle (c36; coherente con N3 c05 y n4-b03). / Emma works evenings (at Karim’s restaurant), so Ana writes to her instead of talking (c36; consistent with N3 c05 and n4-b03).
- Ana querría ir un día a Córcega, pero no hay tiempo: quizá el año próximo (c36). / Ana would like to spend a day in Corsica, but there is no time: maybe next year (c36).
- Hugo y Ana alquilan un auto un fin de semana con su amiga Léa: Hugo conduce y Léa, que ya tiene licencia (N3 c02), figura como conductora adicional; depósito de 400 €, franquicia de 500 € sin seguro a todo riesgo, devolución antes de las 20 h (c37). / Hugo and Ana rent a car for a weekend with their friend Léa: Hugo drives and Léa, who already has her license (N3 c02), is the additional driver; 400 € deposit, 500 € deductible without comprehensive insurance, return before 8 p.m. (c37).
- Hugo tiene licencia de conducir (aunque no tiene auto, N1) (c37, c39, c40). / Hugo has a driver’s license (although he has no car, N1) (c37, c39, c40).
- Ana, de Quito, responde en un foro a un turista que quiere visitar Ecuador (recomienda ir fuera de temporada, pasar por la oficina de turismo, evitar las trampas para turistas y empezar por Quito) (c38). / Ana, from Quito, answers a tourist on a forum who wants to visit Ecuador (she recommends off season, the tourist office, avoiding tourist traps and starting with Quito) (c38).
- Ana y Hugo leen un folleto de seguridad vial antes del viaje; Hugo conducirá al día siguiente (c39). / Ana and Hugo read a road-safety leaflet before the trip; Hugo will drive the next day (c39).
- En ese viaje tienen un pinchazo en la autopista A6, cerca de una gasolinera, con Léa a bordo: la rueda de repuesto está en mal estado, falta el gato y solo queda un cuarto de tanque; Ana llama a la asistencia, que envía un mecánico en cuarenta minutos (c40). / On that trip they get a flat tire on the A6 highway near a gas station, with Léa on board: the spare tire is in bad condition, the jack is missing and only a quarter of a tank is left; Ana calls roadside assistance, which sends a tow-truck driver in forty minutes (c40).

Sin contradicciones con N1–N3 ni con los borradores n4-b01…b10 revisados (Hugo sin auto; Léa con licencia desde marzo; Emma solo de noche en el restaurante de Karim; Ana de Quito y en París).

## Pendiente / sin resolver

- Ninguna palabra francesa se eliminó ni renombró (solo «la nuit» → «le soir» en el correo de c36, y una réplica redundante de c39 cuyo vocabulario sigue enseñado), por lo que los bloques posteriores del nivel no se ven afectados.
- Nota de coherencia para el coordinador: el plan decía que Hugo y Ana alquilan el auto; el autor añadió a Léa como tercera persona (c37 y c40). Se mantiene porque la ficha de c37 pide «conducteur supplémentaire» y es coherente con N3 c02 (Léa ya tiene licencia); conviene copiar este hecho al plan con `reparto.py`.
