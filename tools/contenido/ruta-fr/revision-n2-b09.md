# Revisión independiente · N2 francés, bloque 9 (clases 41–45)

- **Archivo:** `tools/contenido/ruta-fr/n2-b09.json` (`fr.n2.c41` … `fr.n2.c45`). Revisor distinto del autor.
- **Validador:** `python3 tools/validar_ruta.py fr --borrador …n2-b07.json …n2-b08.json …n2-b09.json` → **0 errores** (también con `n2-b10.json` añadido). B9 enlaza con c40 (`prerequisitos`), así que solo valida de forma encadenada: sola, el validador no ve c40 ni su vocabulario y marca palabras de N1 como no enseñadas (efecto de la cadena, no del contenido).
- **Plan:** `python3 tools/curriculo/validar_plan.py fr` → 0 errores y ningún aviso «título de la unidad difiere» para c41–c45.

## Veredicto

GO

## Contraste con las fichas

Cada clase enseña lo que dice su ficha y nada de clases posteriores: c41 me / te / nous / vous (directos e indirectos, delante del verbo y del infinitivo), envoyer y payer (y → i; je paie / je paye), «Ça te dérange de… ? — Pas du tout, ça ne me dérange pas»; c42 pronombre delante del infinitivo (también con ne … pas: je ne peux pas t’aider) y ofrecer, aceptar o rechazar ayuda; c43 est-ce que je peux / je pourrais / ça vous dérange si, avoir le droit de, permettre / interdire (à qqn de + infinitivo); c44 il est interdit / obligatoire / conseillé de, défense de / prière de, infinitivo en carteles (Ne pas fumer), carteles con sustantivo + adjetivo; c45 chaque / chacun / chacune, s’occuper de, penser à, se souvenir de y pronombre tónico tras à / de. No aparece nada de B10 (pasado compuesto de fin de nivel, repaso final) ni de clases posteriores.

Anatomía y tiempos: explicación (+ nota de pronunciación) → tablas → ejemplos (8) → vocabulario (12–14) → guiada (5, con pista) → independiente (4) → situación (8–10 líneas, 82–96 palabras, 2 ítems) → evaluación con 6 ítems puntuables en 6 formatos, más un `escribir` abierto (`abierta: true`) que no puntúa y se suma a esos 6. Cada clase trae 3–4 `erroresFrecuentes`. Hablantes: solo nombres (Ana, Madame Dubois, Monsieur Martin, Hugo, Emma).

## Cambios aplicados (clase · ítem · antes → después)

### c41
1. **p10 · g1 (pista, es).** Remitía a un ejemplo del inglés («como en inglés “help me”»), inútil para quien estudia desde el español → «En francés el pronombre va antes del infinitivo; no se pega al final, como en “ayudarme”.»
2. **p9 · e2 (completar).** Tenía `opciones` (paie / paies / payons) y `aceptadas: ["paye"]`: la forma «je paye», válida, no se podía elegir → se quitan las `opciones` para que se escriba la respuesta; `respuesta` «paie», `aceptadas` «paye».

### c42
3. **Vocabulario `un coup de main` (es).** «una ayuda, un empujón (una mano)» («empujón» es un golpe, no ayuda) → «una mano, una ayuda».
4. **p6 · ejemplo 2 (es) y p10 · i1 (feedback, es).** «¿Quieres una ayudita?» → «¿Quieres una mano?» (español neutro de América).
5. **Situación, línea 6 (Madame Dubois).** «vous avez toujours un coup de main pour moi» no es francés correcto (avoir le coup de main = tener la habilidad) → «Merci, Ana : vous êtes toujours très gentille ! Je peux vous proposer un thé, à vous et à Emma ?» (es / en ajustados). Se cambia además «un café» por «un thé»: Emma odia el café y adora el té (N1 c07 / c09).
6. **Situación, líneas 7–8 y contexto.** Ana trabaja por las tardes en el hotel (B1: sale a las 18 h), así que no podía ir «à quatre heures» sin más → «Nous venons dimanche à quatre heures, avec un gâteau» / «À dimanche, Ana !» (el domingo Ana no trabaja); el contexto dice ahora que Ana vuelve «por la mañana, después de la escuela». Es / en ajustados. Sin palabras nuevas (validado).

### c43
7. **Error frecuente 3 y p1 (es).** «en inglés “allows us to use” no pide ese de» no ayuda a un hispanohablante → «en español decimos “nos permite usar”, sin preposición, pero en francés el de es obligatorio» (en ambos textos; en ya estaba bien).

### c44
8. **Situación (contexto, es / en).** «Ana visita el gimnasio de Hugo» chocaba con B8: en c39 y c40 Ana y Hugo, y Ana y Léa, ya coinciden en la salle de sport del barrio y Ana va «de plus en plus» → «Ana y Hugo están en la salle de sport del barrio, donde entrenan los dos. Hay un letrero nuevo con el reglamento y Hugo se lo explica.» (el diálogo no cambia).
9. **p10 · e6 (escribir).** Pedía la misma frase que acababa de ordenar e4 («Il est obligatoire de porter un casque») → «Está prohibido estacionar aquí» / «Il est interdit de stationner ici.» (frase distinta, solo vocabulario enseñado).
10. **p6 (tabla «Carteles con un sustantivo», texto es / en).** No decía que aquí el adjetivo sí concuerda (animaux interdits), mientras la explicación afirma que en la fórmula impersonal no cambia → se añade la aclaración.
11. **Vocabulario nuevo `le portable`.** Aparecía en carteles y diálogo sin entrada propia → «el celular» / “the cell phone”, con guía «lö por-ta-bl» / “luh por-TAH-bluh”; añadido a `vocabulario` y a los `refs` del paso.

### c45
12. **p6 · ejemplo 8 (es).** «hacemos la limpieza juntas» (género sin referente) → «juntos».
13. **Situación · s1 (elegir).** Distractor «Léa, que vive cerca» (dato no establecido en el reparto) → «Léa, que viene a cenar» / “Léa, who comes for dinner.” (falso en el diálogo, consistente con el reparto).

## Revisión punto por punto

1. **Francés de Francia.** Pronombre antes del infinitivo y con la negación (je ne peux pas t’aider, je ne vais pas le faire, tu ne dois pas lui dire); «tu me peux aider» solo como distractor erróneo; envoyer (j’envoie, nous envoyons, ils envoient) y payer (je paie / je paye, nous payons, ils paient); «ça te dérange de garder le chat ? — pas du tout, ça ne me dérange pas» y «ça vous dérange si je pars plus tôt ?»; permettre à qqn de (il me permet de, je vous permets de les rendre) e interdire (vous interdisez); avoir le droit de con artículo; infinitivos de carteles (Ne pas fumer, Éteindre le portable, Tenir la porte) con «ne pas» junto antes del infinitivo; il est interdit / obligatoire / conseillé de (adjetivo invariable); chacun / chacune con son / sa y verbo en singular; penser à / s’occuper de / se souvenir de + pronombre tónico (je pense à elle, je m’occupe d’eux, je me souviens de toi), con la trampa «je lui pense» explicada. Tipografía: U+202F antes de ? ! : ; y ’.
2. **Explicaciones es / en.** Cortas, con ejemplos y trampas comunes. es con tú y léxico neutro (celular, estacionar, cochecito, computadora, departamento, pastel); en americano (cell phone, parking, stroller, helmet, apartment, “ma’am”). El inglés compara donde ayuda (“help me” / aider moi, “allows us to use” / permet de, “each one does their part” / sa part).
3. **Respuesta única y `aceptadas`.** Revisados todos los `ordenar` (c41 g4 ya traía «Ce soir, je t’envoie un message»; c42 g4, c43 g4, c44 g3, c45 g5 tienen un único orden natural; c45 e4 ya traía el orden con el complemento al final), los `escribir` (c42 e6 con «Madame» al inicio o al final; je paie / je paye en c41 e2) y los distractores: cada uno es erróneo por una sola razón (le por la / lui, vous por nous / te, interdit por obligatoire, soir por soirs).
4. **Pistas y relacionar.** Las pistas ayudan a su ítem (pronombre que se pega al infinitivo, ne … pas alrededor de peux, de tras défense, concordancia de chaque). Glosas de los `relacionar` claramente distintas (prestar / pedir prestado / enviar / molestar; caja / escalera / cochecito / una mano; permiso / prohibir / dejar un lugar / permitido; prohibido / obligatorio / recomendado / letrero; encargarse de / pensar en / acordarse de / por turnos).
5. **Guías de sonido (regla 6).** j y g suave = «sh» (en: “zh”), ch = «sh», nasales in / un = «en», an / en = «an», on = «on» (en: aviso de que la n no suena), oi = «ua», ü y ö definidas en c41 y remitidas en c43–c45, eu / e = «ö», s entre vocales = z, liaison «vu-zan».
6. **Hablantes y situaciones.** 9, 8, 10, 9 y 9 líneas (objetivo N2: 6–10 líneas, ≈ 80–120 palabras): 89, 82, 92, 93 y 96 palabras. Una sola respuesta correcta por pregunta de comprensión. Los `escribir` abiertos no sustituyen a los 6 ítems puntuables de cada evaluación.

## Hechos del reparto confirmados

- Madame Dubois (viuda, dos hijos) tiene un gato y una hija a cuya casa va el sábado; le pide a Ana que cuide al gato y le presta su llave; se mandan mensajes el domingo y Ana le envía una foto del gato (c41). / Madame Dubois (a widow with two children) has a cat and a daughter whose house she visits on Saturday; she asks Ana to look after the cat and lends her her key; they text on Sunday and Ana sends her a photo of the cat (c41).
- Madame Dubois lleva una caja pesada por la escalera con libros de cocina para Ana y Emma; Ana la carga a la cocina y Madame Dubois las invita a un té (no a un café: Emma lo odia) el domingo a las 16 h; Ana y Emma llevan un pastel (c42). / Madame Dubois is carrying a heavy box of cookbooks for Ana and Emma up the stairs; Ana carries it to the kitchen and Madame Dubois invites them for tea (not coffee: Emma hates it) on Sunday at 4 p.m.; Ana and Emma bring a cake (c42).
- Ana sale de clase a las 10 los martes (en vez de las 10:30) porque trabaja en el hotel; Monsieur Martin le permite salir antes una vez por semana y entregar la tarea el lunes, pero no usar el diccionario en el examen (c43). / Ana leaves class at 10 on Tuesdays (instead of 10:30) because she works at the hotel; Monsieur Martin lets her leave early once a week and hand in homework on Monday, but not use the dictionary during the exam (c43).
- Ana y Hugo entrenan en la salle de sport del barrio (la de c39 y c40); su reglamento prohíbe fumar, obliga a llevar zapatillas deportivas, pide apagar los celulares en la sala, prohíbe estacionar frente a la salida de emergencia, y recomienda llegar con anticipación y llevar casco en bicicleta (no es obligatorio) (c44). / Ana and Hugo work out at the neighborhood gym (the one in c39 and c40); its rules forbid smoking, require sports shoes, ask people to turn off phones in the room, forbid parking in front of the emergency exit, and recommend arriving early and wearing a helmet when biking (not mandatory) (c44).
- Ana y Emma escriben las normas de su departamento (primer piso, sobre Madame Dubois): cada semana una hace las compras por turnos, cada una ordena su cuarto, prohibido hacer ruido después de las 22 h por Madame Dubois, cada una hace su parte; Emma lava los platos cada noche y Ana se ocupa de Léa y Hugo cuando vienen a cenar (c45). / Ana and Emma write the house rules for their apartment (on the first floor, above Madame Dubois): each week one of them does the shopping, taking turns; each tidies her own room; no noise after 10 p.m. out of consideration for Madame Dubois; each does her part; Emma does the dishes every night and Ana takes care of Léa and Hugo when they come for dinner (c45).

## Sin resolver

- Nada que impida el GO. Notas para bloques siguientes: Madame Dubois tiene gato y el hermano de Léa también (N1); son gatos distintos. Si en B10 aparece el fin de semana de Madame Dubois, el sábado de c41 y el domingo de c42 son fines de semana distintos o el mismo (ella vuelve el domingo): ambos son compatibles.
