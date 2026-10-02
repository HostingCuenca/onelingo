# Revisión fr.n8.c01–c05 (N8, bloque 1)

GO

Validación: `validar_ruta.py fr --borrador n7-b01…n7-b10 n8-b01` → 0 errores (tras las correcciones). `validar_plan.py fr`: sin «título de la unidad difiere» para fr.n8.c01–c05 (solo c06–c10 y otras, de otros bloques).

## Contraste con las fichas
- Títulos, objetivos, `gramatica`, `introduce`/`recicla`, vocabulario (8, 8, 9, 8 y 8 palabras exactas de cada ficha) y tarea coinciden. No hay contenido de clases posteriores.
- El plan de ejercicios está completo (mismo formato y clave en guiada, independiente, situación y evaluación). Cambios aceptables del autor: transcripciones de c01 e1/e2 como `escuchar` con opciones; el `escribir` de la evaluación de c02–c05 pasa a `abierta` (no puntúa) y la evaluación mantiene ≥ 4 ítems puntuables.
- Evaluación (ítems puntuables / formatos): c01 6 / 4, c02 5 / 4, c03 4 / 3, c04 5 / 4, c05 5 / 5. Todos los `abierta` cumplen `minimoPalabras` con su modelo (10, 20, 20, 15 palabras mínimas frente a 17, 28, 28, 24).
- Situaciones: 434, 443, 443, 452 y 431 palabras de diálogo (N8: 400–700). Hablantes: nombres o papeles en francés (Le voisin, L’annonce, Le chef de bord, Le serveur vocal, Le conseiller, L’experte, Le journaliste).
- Opciones de comprensión en francés en las cinco clases (calibración 14). Tipografía: sin espacios simples ni apóstrofos rectos antes de ? ! : ; en ninguna cadena francesa. Español neutro (boleto, ventanilla, ingrese, marque) e inglés americano (subway, ticket window, pound key) correctos.

## Tabla de formas reducidas (c01, p3 «Se oye → se escribe»)
Es una ayuda real de reconocimiento oral: 25 filas, forma reducida → forma completa, cubre los cinco mecanismos de la explicación (e muda, u de tu, l de il, je+s → ch, ne) con pronombres fusionados (j’te l’ai dit, j’y vais pas), y la pista de g1 remite a ella. La tabla «Para leer» (fou, hein, allô, bisous, un chalet, m’asseoir…) trae sentido y frase de las palabras de los mensajes; no hay celdas sueltas. Nota para audio: las celdas se reproducen por TTS; conviene escuchar «i(l) dit» y «qu’y a» al generar el audio.

## Correcciones aplicadas (clase, ítem, antes → después)
- **c01, tabla p3:** texto «Entre paréntesis, el sonido que cae» (no hay paréntesis salvo en i(l)) → «Toca cada forma para escucharla y compara cómo suena la forma reducida con la completa.» (es/en).
- **c01, explicación p2:** el mecanismo 2 decía que la u de tu solo cae ante vocal, pero la tabla y el diálogo traen «t’sais» → se añade «(y a veces ante otras letras: tu sais → t’sais)».
- **c01, e5:** la consigna no decía de qué ejemplo se hablaba (las opciones hablaban de «été») → se añade `preguntaApoyo` «En «je sais pas» → «chais pas», ¿qué cae de la palabra «je»?».
- **c01, e2:** el distractor «Il dit qu’il y a plus de places» era una transcripción defendible del audio (plus ambiguo en el oral sin ne) → «Il dit qu’il y a encore des places». Queda una sola respuesta.
- **c01, situación (Lucas, cast check c):** «à la campagne» y «j’ai trop bossé cette semaine» sin ancla → «à la campagne, au nord de Montréal» y «j’ai trop bossé cette semaine, entre les cours et le boulot au café» (es/en). Encaja con N2/N3: vive en Montréal, estudia y trabaja los sábados en un café; un chalet junto a un lago es normal en Québec.
- **c02, situación (Le voisin):** mezclaba «tu vois» con «vous» (Ana lo trata de vous) → «vous voyez» (es «¿ve usted?», «¿sabe?»); queda el «tu sais, enfin, vous savez» como autocorrección intencional y la tabla ya explica la variante con vous.
- **c02, situación:** el señor dice «Ah, Quito ! Moi, j’étais chez ma fille» (Lima/Bogotá) y luego habla de la altitud de Quito sin explicar cuándo estuvo → «J’y ai passé deux jours en rentrant.» (es/en).
- **c02, vocabulario v-muletille (en):** «mü-l-TEE-y» → «mül-TEE-y».
- **c03, g3 (ordenar):** faltaban órdenes naturales → `aceptadas` incluye «Le train, en raison d’un incident voyageur, est annoncé avec un retard» y «Le train est annoncé, en raison d’un incident voyageur, avec un retard».
- **c03, i3 (escribir):** se añaden «guichet n°3» (sin espacio) y «guichet 3».
- **c04, situación (cast check a: dos viajes a Quito):** c02 vuelve de «trois semaines chez mes parents, à Quito» y c04 describía otro viaje a Quito sin relación → es el **mismo viaje**: c04 es la ida («Je pars trois semaines chez mes parents, à Quito…») y c02 la vuelta; se actualizan `contexto` y la primera línea de Ana (es/en). No se dice en ninguna parte que las clases sean cronológicas.
- **c04, situación:** el asesor ya daba «le 15, à 9 h 20» y Ana preguntaba después «le vol de quelle heure, vous dites ?» (pregunta sin objeto) → el asesor propone «le 15, le matin»; Ana: «Vous avez bien dit le 15 ? Et le vol de quelle heure ?»; la hora llega en «Le 15, à 9 h 20, oui».
- **c04, situación:** «Pour Madrid, il part à treize heures» respondía a «Il part quand de Madrid» → «De Madrid, il part à treize heures».
- **c04, e5 (modelo abierto):** «reprogrammé jeudi à 9 h 20» contradecía el diálogo → «reprogrammé le 15 à 9 h 20».
- **c04, g4 (ordenar):** se añaden «Qu’entendez-vous par « bientôt » au juste ?» y la variante con coma.
- **c04, e3 (ordenar):** se añade «Le numéro de quel vol ?» (mismos tokens, orden natural).
- **c04, g5 (escribir):** se añaden «Vous avez bien dit 14h40 ?», «à 14 h 40», «À 14 h 40, vous avez bien dit ?» y «Il part à quelle heure ?».
- **c05, e5 (feedback es):** «mais une la oposición» → ««mais» marca la oposición».
- **c05, g4 (escribir con audio):** respuesta única y difícil de teclear → la pista dice que se pueden copiar los símbolos de la tabla y que «->» vale por «→»; `aceptadas` ampliada con «10%», «->» y sus combinaciones.

No se quitó ni renombró ninguna palabra francesa de los pasos de enseñanza; los cambios en diálogos (tu vois, pendant deux jours, Pour Madrid, vous dites en c04) no afectan a bloques posteriores. Palabras añadidas en diálogos (nord, cours, boulot, café, matin, passé, rentrant, encore) ya estaban enseñadas (validador 0 errores).

## Hechos del reparto confirmados
- Hugo, ya guía, prepara una visita guiada al museo para un grupo de cuarenta personas y está agotado (c01) / Hugo, now a guide, is preparing a guided museum tour for a group of forty and is exhausted (c01)
- Léa quiere ir a un concierto el sábado, ya no quedan lugares sentados, no hay metro después de medianoche, y Hugo no le responde (c01) / Léa wants to go to a Saturday concert, there are no seats left, the subway stops after midnight, and Hugo is not answering her (c01)
- Lucas vive en Montréal, estudia y trabaja en un café, y pasa el fin de semana con amigos en el campo, al norte de Montréal, junto a un lago y un chalet; está cansado del trabajo (c01) / Lucas lives in Montréal, studies and works at a café, and spends the weekend with friends in the countryside north of Montréal, by a lake and a chalet; he is tired from work (c01)
- Ana oye sus mensajes de voz en la pausa en el hotel y se tutea con Hugo, Léa y Lucas (c01) / Ana listens to her voicemail on her break at the hotel and uses tu with Hugo, Léa and Lucas (c01)
- Ana pasa tres semanas con sus padres en Quito: la ida (vuelo París–Madrid–Quito, retrasado y cancelado, reprogramado el 15 por la mañana a las 9 h 20, vuelo 4812, sin gastos de cambio) en c04 y la vuelta en c02; es un solo viaje / Ana spends three weeks with her parents in Quito: the outbound trip (Paris–Madrid–Quito flight, delayed then canceled, rebooked on the 15th at 9:20 a.m., flight 4812, no change fees) in c04 and the return in c02; it is a single trip
- En el vuelo de regreso de Quito, Ana habla (de vous) con un vecino de asiento francés, jubilado desde hace cinco años, cuya hija trabaja en Bogotá y a quien le dolió la cabeza por la altitud de Quito; Ana le cuenta que trabaja en la recepción de un hotel y prepara un examen de francés (c02) / On the flight back from Quito, Ana chats (using vous) with a retired French seatmate, retired for five years, whose daughter works in Bogotá and who got a headache from Quito’s altitude; Ana tells him she works at a hotel front desk and is preparing a French exam (c02)
- Ana trata de vous al asesor de la aerolínea (c04) / Ana uses vous with the airline agent (c04)
- Ana pasa un fin de semana en Lyon en casa de la abuela de Hugo (ella sola, como en N2); toma un tren a las 17 h 50 en la Gare de Lyon, con retraso y cambio de vía (c03) / Ana spends a weekend in Lyon at Hugo’s grandmother’s home (alone, as in N2); she takes a 5:50 p.m. train at the Gare de Lyon, with a delay and a track change (c03)
- Ana viaja en un tren de noche a Marseille, escucha una entrevista de radio sobre los trenes de noche y le manda a Hugo (tú) un mensaje con su resumen (c05) / Ana travels on a night train to Marseille, listens to a radio interview about night trains, and sends Hugo (tu) a message with her summary (c05)

## Sin resolver
- c03: la ficha decía «visitar a Léa»; el autor usa a la abuela de Hugo (aprobado por el coordinador, consistente con N2 c06/N6). Léa vive en París, así que la ficha era incoherente.
- Las cinco situaciones son viajes o llamadas independientes; el bloque no afirma un orden cronológico entre c02, c03, c04 y c05 (salvo que c04 es la ida del viaje cuya vuelta es c02).
