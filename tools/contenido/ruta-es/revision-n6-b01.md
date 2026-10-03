GO

# Revisión es N6 B1 (es.n6.c01–c05)

## Validación

`python3 tools/curriculo/validar_bloque.py es 6 1` → `== N6 B1: 0 error(es) del bloque`.

Comprobaciones adicionales hechas por script: un solo `___` por `completar`; `ordenar` forma exactamente la respuesta y todas sus `aceptadas` con los `tokens`; ningún hablante con dos turnos seguidos; 7–8 ejemplos por clase; tablas «To read» de 8–13 filas (máx. 15); fechas de la cronología (12-abr-2031 = sábado; 20-abr domingo; viernes 25-abr; domingo 4-may; martes 13-may). Lecturas finales: c01 353, c02 348, c03 346, c04 345, c05 344 palabras de diálogo.

Palabras de las tablas «To read» ya enseñadas por N1–N5 (comprobadas con el validador y con grep en `assets/contenido/es/ruta/`): feliz, confianza, iglesia. Se quitaron o se redujeron. «casarse», «elegir», «amor», «veintitrés», etc. NO constan como enseñadas (el validador marca «veintitrés» como no enseñada), así que se quedan en las tablas.

## Correcciones

- [reparto] es.n6.c01, p9 contexto: «a week after Emma's thirtieth birthday» → «Sunday, April 20, 2031, a little over a week after…» (cronología fijada) (baja)
- [reparto] es.n6.c01, p9 diálogo (Daniela): «me llama a las dos de la mañana de Madrid… como si todavía estuviera en Quito» → «me llama a la hora de la cena de Quito… y en Madrid ya es muy tarde. ¡Como si todavía estuviera en Quito!» (broma verosímil y clara) (media)
- [pedagogía] es.n6.c01, p9 lectura: 314 → 353 palabras (Rosa «la hice esta mañana para ti»; Daniela «tú hablas de la selección como si fuera tu familia»; Emma «mi papá me pregunta si tengo dinero, como si yo fuera una niña») con material ya enseñado (media)
- [explicación-falsa] es.n6.c01, p4 texto: «Three of these verbs are new in this table: estar, saber and haber» → «The forms of estar, saber and haber are new in this table; the others you already know» (los verbos no son nuevos, sí sus formas) (baja)
- [aceptadas] es.n6.c01, e3: «Usted me trata como si fuera una niña.» (imposible con los tokens) → eliminada (baja)
- [aceptadas] es.n6.c01, i3 y e4: se añaden variantes con pronombre («como si él fuera / fuese el entrenador», «como si ella fuese su hija») (baja)
- [explicación-falsa] es.n6.c02, vocab v-natalidad, nota: «NAH-sah» → «TAH-sah» (tasa) (media)
- [reparto] es.n6.c02, vocab v-pareja-hecho: «legal partnership» sin más → «the term used in Spain», nota «Recognition only… In Ecuador the legal term is unión de hecho» (media)
- [reparto] es.n6.c02, p3b: añadida fila «la unión de hecho» (término ecuatoriano) para poder usarlo en el diálogo (media)
- [reparto] es.n6.c02, p8 diálogo (Emma): «Son parejas de hecho.» → «En Ecuador se llama unión de hecho.» (media)
- [pedagogía] es.n6.c02, errorFrecuente 4: «…hoy hay más parejas de hecho» → «…hoy muchas parejas conviven sin casarse» (no promueve el término de España) (baja)
- [reparto] es.n6.c02, p8 diálogo (Mateo): «a diferencia de nuestros abuelos» → «a diferencia de la gente de antes» (Mateo y Emma no comparten abuelos; evita confundir las dos familias de Guadalajara) (media)
- [reparto] es.n6.c02, p8 diálogo (Emma): «Él conoció a mi abuela en Chicago» → «trabajó en una fábrica de Chicago y allí conoció a mi abuela»; «solo hablábamos inglés» → «mi abuela solo hablaba inglés, así que en mi casa hablábamos inglés» (canon N3 y MAPA) (baja)
- [pedagogía] es.n6.c02, p8 lectura: 314 → 348 palabras (Mateo «vivo lejos de mi familia, a diferencia de mis abuelos»; cierre «Vamos a la mesa») (media)
- [aceptadas] es.n6.c02, e2: aceptada «a diferencia» (daría «A a diferencia de ti») → eliminada (media)
- [plan-ficha] es.n6.c02, p9: añadido e5 `escribir` abierto (no puntuable) que responde a la tarea de la ficha (tres frases con «a diferencia de») (baja)
- [pedagogía] es.n6.c03, p3b: fila «feliz, felices» → «felices» (feliz ya enseñada) (baja)
- [pedagogía] es.n6.c03, p8 lectura: 307 → 346 palabras (Rosa «me casé con Jorge a los veintitrés años»; nueva intervención de don Jorge «no tenía dinero cuando me casé, y fuimos felices»; Daniela «prefiero esperar y elegir bien»; cierre de don Jorge) (media)
- [pedagogía] es.n6.c04, p3b: eliminada la fila «la confianza» (ya enseñada) (baja)
- [pedagogía] es.n6.c04, p8 lectura: 310 → 345 palabras (Emma «somos cinco: mis padres, mis hermanos menores y yo»; Kenji «los domingos toda la familia come junta»; Valentina «cualquier familia funciona, numerosa o pequeña») (media)
- [pedagogía] es.n6.c05, p3b: eliminada la fila «la iglesia» (ya enseñada) (baja)
- [reparto] es.n6.c05, errorFrecuente 4: «Rosa se divorció con su marido» (contradice el canon: Rosa sigue casada con Jorge) → «Él se divorció con su esposa» / «Él se divorció de su esposa» (media)
- [explicación-falsa] es.n6.c05, vocab v-ruptura, nota: «rrook-TOO-rah» → «rroop-TOO-rah» (la p suena como p) (media)
- [apoyo-en] es.n6.c05, p9 diálogo (Rosa): traducción «another chance» → «another option» (coincide con «otra opción») (baja)
- [pedagogía] es.n6.c05, p9 lectura: 306 → 344 palabras («¿Y qué comieron?» / «hizo comida como si hubiera cuarenta invitados, y éramos diez»; Jorge «siempre llegaba a tiempo»; «Son treinta y nueve años»; Emma «Y de su sopa») (media)

## Hechos del reparto confirmados

- Rosa tiene 62 años en 2031, es profesora de primaria jubilada y se casó con Jorge, taxista, a los 23 años (1992) / Rosa is 62 in 2031, a retired elementary school teacher, and married Jorge, a taxi driver, at 23 (1992)
- Rosa y Jorge se conocieron cuando ella tenía 20 años: Jorge la llevaba cada mañana en su taxi a la escuela donde ella enseñaba; llevan 39 años casados / Rosa and Jorge met when she was 20: Jorge drove her every morning in his taxi to the school where she taught; they have been married 39 years
- Rosa y don Jorge tutean a Emma; Emma les habla de usted («señora Rosa», «don Jorge») y tutea a Daniela / Rosa and don Jorge use tú with Emma; Emma uses usted with them («señora Rosa», «don Jorge») and tú with Daniela
- Emma cumple 30 años el sábado 12 de abril de 2031; el almuerzo de c01 es el domingo 20 de abril; vive sola (desde 2029, Guápulo) / Emma turns 30 on Saturday, April 12, 2031; the c01 lunch is Sunday, April 20; she lives alone (since 2029, Guápulo)
- Emma tiene un hermano y una hermana menores (sin nombre; la familia son cinco con sus padres), sus padres viven en Chicago y se casaron a los 28 años / Emma has a younger brother and sister (unnamed; five in the family with her parents); her parents live in Chicago and married at 28
- El abuelo paterno de Emma era de Guadalajara, trabajó en una fábrica de Chicago y allí conoció a la abuela, que solo hablaba inglés; en casa de Emma solo se hablaba inglés / Emma's paternal grandfather was from Guadalajara, worked in a Chicago factory and met her grandmother there; she spoke only English; only English was spoken at Emma's home
- Mateo Ruiz es mexicano de Guadalajara; sus abuelos (otra familia, también de Guadalajara) tuvieron seis hijos y sus padres dos; Mateo no es hijo único (hermano o hermana, sexo sin fijar: el texto solo dice «hermanos»); vive en Quito y alquila su departamento / Mateo Ruiz is Mexican from Guadalajara; his grandparents (a different family, also from Guadalajara) had six children and his parents two; Mateo is not an only child (a sibling of unspecified sex: the text only says «hermanos»); he lives in Quito and rents his apartment
- En abril–mayo de 2031 Mateo todavía «quiere abrir su estudio de diseño este año» (no lo ha abierto) / In April–May 2031 Mateo still «wants to open his design studio this year» (he has not opened it yet)
- Daniela sigue en Madrid, habla por videollamada, tutea a todos y trata de tú a sus padres; es hija única (hecho nuevo, admisible: el reparto solo dice «hija de Rosa y Jorge») / Daniela is still in Madrid, talks by video call, uses tú with everyone, including her parents; she is an only child (new but admissible: the cast only says «daughter of Rosa and Jorge»)
- Una prima de Rosa se separó de su marido el año pasado y se comprometió con otro hombre este año (hecho nuevo) / One of Rosa's cousins separated from her husband last year and got engaged to another man this year (new fact)
- Valentina creció con su mamá («éramos solo las dos»); los abuelos de Kenji viven con sus padres; Emma, Kenji y Valentina se tutean / Valentina grew up with her mom («it was just the two of us»); Kenji's grandparents live with his parents; Emma, Kenji and Valentina use tú with each other
- En Ecuador el término legal es «unión de hecho»; «pareja de hecho» queda como nota de reconocimiento (España) / In Ecuador the legal term is «unión de hecho»; «pareja de hecho» is kept only as a recognition note (Spain)

## Sin resolver

- «Daniela es hija única», «una prima de Rosa» y «la prima de Mateo (casada con una doctora)» son hechos nuevos admisibles; el coordinador debe copiarlos al reparto si los acepta (el último viene de la ficha de c05).
- «Veintitrés» no consta como enseñada en N1–N5 para el validador, aunque aparece en notas de vocabulario; por eso se conserva en la tabla de c03. Si se quiere unificar, enseñarla antes en un paso de enseñanza.
- Las fichas de c04 traen un error de plan en la tarea («la congarantía»); el borrador ya usa «la confianza», pero conviene corregir `curriculo/es/n6.json` (el revisor no lo toca).
- c02 evaluación: la ficha decía «Unlike his brother, Mateo lives in Quito»; se cambió a «sus padres» para no fijar el sexo del hermano o hermana de Mateo.

Total: 24 correcciones (0 altas, 13 medias, 11 bajas)
