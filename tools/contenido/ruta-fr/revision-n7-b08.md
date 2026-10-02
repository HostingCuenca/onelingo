# Revisión N7 · B8 (fr.n7.c36–c40)

GO

Revisado por un agente distinto del autor. Validación: `python3 tools/validar_ruta.py fr --borrador n6-b01…n6-b10 n7-b01…n7-b08` → **0 errores** (modo de vocabulario estricto); al integrarse n6 en `assets/` mientras revisaba, repetí con solo `n7-b01…n7-b08` → 0 errores. `python3 tools/curriculo/validar_plan.py fr` → ningún «título de la unidad difiere» para fr.n7.c36–c40 (el único aviso de ese tipo es de n9). Encadenando también n7-b09 y n7-b10 no aparece ningún error que dependa de palabras de B8 (los pocos errores de esos bloques son propios: c42 «élément», c43 «allure»).

## Contraste con las fichas

Títulos, objetivos, `introduce` / `recicla`, vocabulario (las 8 palabras de cada ficha, todas en tarjeta), `situacion` y `tarea` coinciden con `curriculo/fr/n7.json`. Los ejercicios del plan están todos, en el mismo orden, formato y clave (guiada 5 + independiente 4 + 2 preguntas de situación + evaluación de 6 por clase). Nada de clases posteriores. Cada evaluación tiene **5 ítems puntuables en ≥ 2 formatos** (c36 completar/elegir/escuchar; c37 completar/elegir; c38 completar/elegir/escuchar; c39 completar/elegir/ordenar; c40 completar/elegir) más 1 `escribir` abierto (`abierta: true`, modelo ≥ `minimoPalabras`) que no cuenta. Situaciones de 310 / 320 / 325 / 317 / 310 palabras (rango N5–N7: 300–500). Hablantes: Ana, Lucas, Mateo, Hugo (nombres). Pronunciación (sh, nasales «en» / «an», ü, ö) coherente con las convenciones del Nivel 0 y de N6.

## Correcciones

**Todo el bloque**
- Tipografía: no había U+202F en ninguna parte (31 « ?» y 15 « !» con espacio normal, además de « :» y « ;») → U+202F antes de ? ! : ; en dialogos, ejemplos, tablas, opciones, preguntas, respuestas y errores. El apóstrofo ’ ya era correcto.
- Español neutro de América: «metedura de pata» → «metida de pata» (c38, 8 sitios); «reagrupación familiar» → «reunificación familiar» (c39); «mi oficio» → «mi profesión» (c37). Inglés americano: «in a line» → «in line» (c38).
- Opciones/preguntas en francés (punto 14): las preguntas de comprensión llevaban `preguntaApoyo` (es/en) → `pregunta` en francés en c36 s1, c37 s1, c38 s1, c39 s1 y s2, c40 s1 y s2, y en las guiadas/independientes de c40 (g5, i4). Las opciones de `escuchar` (c36 i4/e5, c38 i4/e5) ya estaban en francés. Se mantienen `preguntaApoyo` solo en c38 g4 e i2 (preguntan el sentido de «déconcerter»/«dérouter»: la pregunta en francés exigiría «désarroi», «perturber», no enseñados).
- Tablas «Para leer…» (punto 14): se eliminaron las filas de relleno y se dejaron solo filas con sentido (palabra + frase + glosa).

**c36**
- Situación, Lucas: «Je prépare mon voyage à Paris» → «Je prépare mon voyage en train : Paris sera ma deuxième étape» (coherente con N7 c09: Lucas sale de Montréal el 3 de mayo y para tres días en casa de Ana); el contexto es/en lo dice igual.
- Tabla «Palabras para leer la crónica»: fila «les Parisiens» («Les Parisiens habitent à Paris.») eliminada (no enseñaba nada).
- i3 (escribir): `aceptadas` + «Les Français déjeunent, en règle générale, vers midi.».
- s1: `preguntaApoyo` → «Que dit Ana des Parisiens ?».

**c37**
- Cast: el borrador decía «Lucas et moi sommes allés à l’anniversaire d’Hugo» (Lucas físicamente en la fiesta). Choca con N7 c09 (Lucas está en París del 8 al 10 de mayo) y con N1 (Hugo nació el 14 de agosto de 2006). Ahora Lucas participa **por videollamada desde Montréal** en el cumpleaños de Hugo, a mediados de agosto: «Samedi, Lucas était avec nous en vidéo, depuis Montréal, pour l’anniversaire de Hugo». Su frase de sorpresa pasa a «Avant mon voyage, je pensais que les Français étaient plus froids… Dès le début de l’appel, on m’a demandé mon métier, et on m’a posé des questions sur mon voyage»; contexto es/en reescrito (14 de agosto, videollamada).
- «d’Hugo» → «de Hugo» (como en N1 «l’anniversaire de Hugo», y evita un token que no estaba enseñado). Fila «étonner» de «Palabras para leer» («Qu’est-ce qui étonne Lucas à l’anniversaire d’Hugo ?»): era relleno para el validador → eliminada. La tabla quedó con una sola fila («explétif»): se eliminó y «explétif» pasa a la tabla de gramática («le ne explétif | Le « ne » explétif n’exprime pas de négation.»); ids de paso renumerados p1–p12.
- «la fête de ma grand-mère» → «la fête pour l’anniversaire de ma grand-mère» (más claro; la abuela de Ana vive en Quito, N3 c15 / N4 c08).
- s1: `preguntaApoyo` → «Que dit Lucas des Français ?»; opción 3 «La fête est courte.» → «Ils sont plus froids qu’il ne le pensait.» (distractor que sí tienta; una sola respuesta).

**c38**
- ES «Tantos trámites es desconcertante» → «Tantos trámites seguidos son desconcertantes»; EN «So many formalities is disconcerting» → «…in a row are disconcerting».
- i3 (escribir): `aceptadas` + «J’ai été surprise que l’on m’ait tutoyée.».
- s1 en francés: «À quoi tient le malaise de Mateo ?».

**c39**
- Situación: «J’ai interrogé cent familles» (inverosímil para una columna de barrio) → «J’ai interrogé six familles : vingt personnes en tout». Las cifras siguen coherentes (≈ la mitad de 20 personas con un pariente en España, uno de cada tres binacional).
- Tabla «Palabras para leer el reportaje»: la fila de 4 frases amontonadas («Un émigré… Une émigrée… Des émigrés… Cette famille n’a pas d’émigré.») → «Un émigré quitte son pays. Ana est une émigrée. Les émigrés équatoriens vivent en Europe.»; filas redundantes («un primo-arrivant», «la situation», «quitter») eliminadas; quedan émigré/émigrée, diaspora y parent (falso amigo: «pariente»).
- e2 y e4: «n’ont pas d’émigré» → «n’ont pas de parent à l’étranger» (evita el token «d’émigré» solo enseñado por la fila de relleno).
- Cast de Mateo: «il est issu d’une famille de Quito» → «Mateo est un primo-arrivant équatorien : il vient d’arriver et tout est nouveau» (mínimo, igual que c38). Ejemplo 5 «Mateo est issu d’une famille d’origine équatorienne» → «Ana est issue d’une famille de Quito».
- Regroupement familial: «il permet à un parent de faire venir sa famille» (parent = pariente vs. padre/madre, ambiguo y mal traducido) → «il permet à une personne installée à Paris de faire venir sa famille».
- Explicación: «d’origine + adjetivo (invariable)» → «siempre en femenino singular, porque concuerda con origine».
- Hugo: «Tu as rencontré des familles ?» (Ana ya acababa de decir que entrevistó seis) → «Une famille en particulier ?». ES de la cita de la madre: «lleva a Ecuador en el corazón» → «se lleva Ecuador en el corazón». EN de la fila «diaspora» más natural.
- s1 y s2 en francés («Quelle est l’idée principale du reportage ?», «Quelle proportion des personnes interrogées a un parent en Espagne ?»).

**c40**
- Tesis de Ana: «Il n’en reste pas moins que ce cliché a un fond de vérité» aparecía sin concesión previa → «On ne peut pas généraliser ; il n’en reste pas moins que…» (es/en ajustados).
- Comillas anidadas «…« tous les Parisiens sont… »…» → “tous les Parisiens sont…” (también en la traducción es).
- «Dans le métro, les gens sont pressés» → «souvent pressés» (no generalizar justo en la clase de evitar estereotipos).
- g5 e i4: preguntas en francés. Para poder hacerlas se enseñó «connecteur / introduit / objection / oppose» en una fila de la tabla de conectores («un connecteur | Un connecteur relie les idées : or introduit une objection, en revanche oppose deux faits.»).
- Error frecuente 1: «…que le cliché soit faux» → «…est répandu» (cambiaba de significado) → ahora «soit répandu» → «est répandu».
- e4 (completar con «or», sin pista): `opciones` [or, car, donc]; sin ellas «mais» y «en revanche» también encajaban.
- s1 y s2 en francés («Quelle est la position finale d’Ana sur les stéréotypes ?», «Quel plan suit l’article ?»).

## Hechos del reparto confirmados

- Ana escribe la crónica «Une Équatorienne à Paris» para la revista del barrio («la revue du quartier») y se tutea con Lucas, Hugo y Mateo; trata de vous a nadie en este bloque. / Ana writes the column “Une Équatorienne à Paris” for the neighborhood magazine (“la revue du quartier”) and uses tu with Lucas, Hugo and Mateo; she uses vous with no one in this block.
- Lucas, que vive en Montréal, prepara su gran viaje en tren por Europa (sale de Montréal el 3 de mayo; París es su segunda etapa y se aloja tres días con Ana, N7 c09) y le pide a Ana la verdad sobre los clichés de los franceses antes de viajar (c36). / Lucas, who lives in Montréal, is preparing his big train trip across Europe (leaving Montréal May 3; Paris is his second stop and he stays three days with Ana, N7 c09) and asks Ana for the truth about clichés on the French before he goes (c36).
- Hugo celebra su cumpleaños (nació el 14 de agosto, N1) con una fiesta un sábado de mediados de agosto: aperitivo-cena largo, se discute de política, Léa lleva un pastel grande (c37). Es una fiesta distinta de la del 5 de mayo de N1 c28. / Hugo celebrates his birthday (born August 14, N1) with a party on a Saturday in mid-August: a long dinner-style cocktail party, people discuss politics, Léa brings a big cake (c37). It is a different party from the May 5 one in N1 c28.
- Lucas asiste a ese cumpleaños de agosto solo por videollamada desde Montréal (no está en París: su visita fue en mayo); antes de su viaje pensaba que los franceses eran más fríos y le sorprende que sean más directos de lo que pensaba (c37). / Lucas attends that August birthday only by video call from Montréal (he is not in Paris: his visit was in May); before his trip he thought the French were colder and is surprised they are more direct than he thought (c37).
- Léa es discreta y teme que la encuentren demasiado fría (c37). / Léa is discreet and worries that people will find her too cold (c37).
- La abuela de Ana vive en Quito; su fiesta de cumpleaños allí empieza tarde y termina muy tarde (coherente con N3 c15 y N4 c08). / Ana’s grandmother lives in Quito; her birthday party there starts late and ends very late (consistent with N3 c15 and N4 c08).
- Mateo, joven ecuatoriano recién llegado a Francia (primo-arrivant), se tutea con Ana; ella lo acompaña a su cita en la prefectura: el empleado lo tutea (le sorprende), nadie habla en la cola, le piden justificante tras justificante y una foto; Ana se lo explica (código implícito, tradición administrativa) y lo usa para su crónica (c38). / Mateo, a young Ecuadorian who has just arrived in France (primo-arrivant), uses tu with Ana; she goes with him to his appointment at the prefecture: the clerk uses tu with him (a surprise), nobody talks in line, they ask for one proof of address after another and a photo; Ana explains it (implicit code, administrative tradition) and uses it for her column (c38).
- Ana entrevistó a seis familias ecuatorianas de París (veinte personas) para un reportaje de la revista del barrio: una de ellas, de Quito, vive cerca de la estación; la madre viene de un pueblito y sus hijos, de segunda generación, son binacionales; Ana se define como emigrada; Hugo la ayuda y escucha (c39). / Ana interviewed six Ecuadorian families in Paris (twenty people) for a neighborhood-magazine report: one of them, from Quito, lives near the station; the mother comes from a small village and her children, second generation, are dual-national; Ana calls herself an emigrant; Hugo helps and listens (c39).
- Hugo lee el borrador del artículo de Ana sobre los clichés de París y los parisinos (tesis, antítesis, síntesis) y lo propone a la revista del barrio (c40). / Hugo reads the draft of Ana’s article on clichés about Paris and Parisians (thesis, antithesis, synthesis) and suggests it to the neighborhood magazine (c40).
- Madame Lefort sigue siendo la vecina de abajo a quien molesta el ruido (ejemplo de c37, coherente con N5). / Madame Lefort is still the downstairs neighbor who is bothered by noise (c37 example, consistent with N5).

## Sin resolver / avisos

- No hay ningún ítem `relacionar` en el bloque: el plan de ejercicios de c36–c40 no incluye ninguno y no se añadió (el encargo pide usar todos los formatos a lo largo del bloque; el formato falta aquí pero está en otros bloques del nivel).
- Lucas ya había visitado París en N2 B7 (tres noches en un hotel cerca del aeropuerto): que en c36 pida «la verdad» sobre los clichés antes de su viaje de mayo es plausible porque entonces apenas salió de la zona del aeropuerto, y no se dijo «por primera vez» en el texto. Si el coordinador quiere cerrarlo, basta una línea en N7 c09.
- `Mateo` ya está en `palabrasLibres` de `curso.json`; no hace falta tocar nada. No se enseñó ni «Mateo» ni «d’Hugo» como filas de vocabulario.
- Palabras que quité de pasos de enseñanza: «étonner / étonne» (fila de c37), «cherchent» y el resto de las frases de las filas «un primo-arrivant», «la situation» y «quitter» de c39, y «d’émigré» (c39). Comprobado: ningún bloque posterior (n7-b09, n7-b10) las usa; al encadenarlos solo salen errores propios de esos bloques.
- Los diálogos quedan en el límite bajo de «Por nivel» (310–325 palabras): válidos, sin margen para recortar.
