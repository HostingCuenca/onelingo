# Revisión independiente · N1 francés, bloque 8 (clases 36–40)

- **Archivo:** `tools/contenido/ruta-fr/n1-b08.json` (`fr.n1.c36` … `fr.n1.c40`). Revisor distinto del autor.
- **Fecha:** 2026-10-01
- **Validación:**
  - `python3 tools/validar_ruta.py fr --borrador tools/contenido/ruta-fr/n1-b08.json` → **0 errores** (antes y después de mis cambios).
  - Encadenado con B9 (`--borrador n1-b08.json n1-b09.json`) → **0 errores**.
  - `python3 tools/curriculo/validar_plan.py fr` → 0 errores; ningún aviso «título de la unidad difiere» para c36–c40 (quedan los 10 avisos de situaciones fuera del bloque del marco, que no son de B8).
- **Comprobación propia «nada sin enseñar»** (script más estricto que el validador: solo cuentan ejemplos, tarjetas mostradas, patrón y tablas de Fundamentos, B1–B7 y de la propia clase hasta ese paso): 0 faltas en respuestas, opciones, audios, diálogos, tokens, pares y `aceptadas`. Solo marca el rótulo de hablante «La caissière» (papel en francés, permitido).
- **Ordenar:** todas las respuestas y `aceptadas` se pueden formar con los tokens dados.
- **Tipografía:** 0 apóstrofos rectos y 0 signos ? ! : ; con espacio normal en campos franceses (U+202F correcto).
- **Reciclaje** (palabras de ejemplos y diálogo ya enseñadas antes): c36 77 %, c37 78 %, c38 81 %, c39 81 %, c40 85 % (mínimo 30 %).
- **Anatomía:** sonido del día → explicación → tablas → 8 ejemplos → tarjetas → 5 guiada / 4 independiente → situación de 6 líneas con 2 comprensiones → evaluación de 6 ítems con 5 formatos → 4 errores frecuentes por clase. Los 6 formatos aparecen en el bloque (relacionar en cada práctica guiada).

## Veredicto

GO

## Contraste con las fichas (c36–c50)

Títulos, objetivos, gramática, `introduce`, `recicla`, vocabulario, sonido y tarea coinciden con `curriculo/fr/n1.json`. No se adelanta nada de c41–c50: no hay imperativo, preposiciones de lugar nuevas, futur proche, passé récent ni invitaciones (las referencias a venir y aller remiten a c34 / c33). Lo que ya se vio va como repaso (partitivo c22, pas de c17, je voudrais c21, aimer + infinitivo c26, números 70–99 c23, fechas c28, au = à + le c33).

Decisiones sobre las adiciones de la autora:

1. **apprendre / comprendre (c36):** aceptable. Solo aparecen como tabla y nota («se conjugan igual que prendre»), con la forma j’apprends / nous apprenons / ils comprennent que pide la ficha.
2. **apporter (c37):** aceptable. La tarea de la ficha dice «qué puedes llevar», y apporter solo se usa como verbo en -er tras je peux / tu peux.
3. **assez (c39) e il faut:** aceptables; la ficha los pide en la gramática (assez de) y en el título (il faut).
4. **quatrième–dixième (c40):** aceptables como tabla de la regla número + -ième (la ficha dice «deuxième, troisième…»); no se piden en ejercicios.
5. **ensemble (c36):** viene de la guía de sonido de la ficha (an / en / em).

## Cambios aplicados (clase · ítem · antes → después)

### Español neutro y claridad
1. **c37 · p5 (texto es), ejemplo 7 (traducción), g3 (pista).** «camarero» → «mesero» (calibración B5).
2. **c36 · p7 (es y en).** «el hambre y la sed no se «son»» (sin sentido en español) → «no se «es» hambre ni sed: se «tienen»»; en inglés «not “been”» → «you don’t “be” hungry or thirsty: you “have” hunger and thirst».
3. **c39 · tarjeta un morceau / une tranche.** «una rebanada (o loncha)» → «una rebanada (o lonja)» (loncha es de España).
4. **c37 · p5 (es).** El ejemplo final decía «je ne veux pas préparer un gâteau» (con la negación mal) mientras la versión inglesa tenía la forma correcta → «préparer de gâteau».
5. **c37 · e5 (consigna es y en).** «Quiero cocinar un pastel» / “bake” (ambiguo) → «Quiero preparar un pastel» / “make”; el feedback dice que también se aceptan faire y cuisiner.

### Guías de pronunciación (regla 6)
6. **c37 · p1 (en).** un œuf = “an uhf” (parecía una vocal normal) → “uh(n) uhf” (misma convención que B3 c11 y B6 c28).
7. **c39 · tarjeta un peu de (en).** “an puh” → “uh(n) puh”.

### Pisos y inglés americano (c40, el punto clave del encargo)
8. **c40 · p8 (es).** «el francés cuenta como el español» (no es cierto en países donde «primer piso» es la planta baja) → «le rez-de-chaussée es la planta baja y no se cuenta como piso; después viene le premier étage (el primer piso, el de justo arriba)… Ojo: en algunos países de América «primer piso» es la planta baja; en francés no».
9. **c40 · p8 (en).** «French counts like Spanish» → «French counts differently from the US»; se añade que las traducciones al inglés usan el número americano con el francés entre paréntesis («fourth floor (3e étage)»). El texto ya decía que el premier étage es el second floor americano.
10. **c40 · traducciones al inglés** (coherentes con `hechosDelReparto`: Ana 1er étage = second floor, Hugo 3e étage = fourth floor):
    - ejemplo 5: «Hugo lives on the third floor» → «…on the fourth floor (3e étage)».
    - tabla p9: «on the second floor» → «on the third floor (2e étage)».
    - g3, i1, e2, e6 (consignas): «third / second floor» → «fourth floor (3e étage)», «fourth floor (3e étage)», «third floor (2e étage)», «fourth floor (3e étage)».
    - diálogo: «He lives on the third floor» → «…fourth floor (3e étage)»; «I live on the first floor» → «…second floor (1er étage)».
    - s2 (opciones en): «On the third floor / On the first floor» → «On the fourth floor (3e étage) / On the second floor (1er étage)».

### Diálogos y respuestas aceptadas
11. **c40 · diálogo, línea 5 de Ana.** «Au troisième étage ? Moi, j’habite au premier étage…» (Ana y Hugo viven en el mismo edificio según `hechosDelReparto`, no tiene sentido que se sorprenda) → «Super ! Moi, j’habite au premier étage. Et toi, Léa ?» («¡Genial! …»; «Great! I live on the second floor (1er étage)…»). La comprensión s2 sigue con una sola respuesta.
12. **c38 · diálogo, última línea.** «À demain, Hugo !» (no han quedado para el día siguiente; mismo problema que revisó B7) → «À bientôt, Hugo !» («Hasta pronto» / “See you soon”).
13. **c39 · e6 (¿Cuánto es en total?).** `aceptadas` + «Combien ça fait ?», «Combien ça fait en tout ?», «Combien ça coûte ?», «Combien ça coûte en tout ?», «Combien c’est ?», «Combien c’est en tout ?» (orden natural con «Combien» inicial, clases 19 y 23).
14. **c40 · i2 (doscientos cincuenta euros).** `aceptadas` + «Deux-cent-cinquante euros.» (ortografía con todos los guiones, rectificación de 1990).
15. **c40 · e5 (cumpleaños el 1 de mayo).** `aceptadas` + «Mon anniversaire, c’est le 1er mai.» (abreviatura que enseña p6).

## Revisión punto por punto del encargo

1. **Francés de Francia.** Conjugaciones de prendre / boire / vouloir / pouvoir / devoir / finir (incluidos prennent, boivent, veulent, peuvent, doivent, finissent), apprendre y comprendre, choisir y réfléchir; acheter con j’achète. Partitivo tras prendre / boire y `de` tras negación y tras cantidad (un kilo de, beaucoup de, trop de, assez de, d’eau, d’œufs), il faut + nombre / infinitivo sin de, il faut ≠ il fait. cent / cents (deux cents euros, deux cent cinquante, cent quatre-vingts, trois cent un), mille invariable, cent un sin et. Ordinales (deuxième… dixième, premier / première, dernier / dernière), au deuxième étage, rez-de-chaussée, le premier mai y el resto de fechas con cardinal. Todo correcto. La nota sobre Canadá / Bélgica / Suiza (déjeuner / dîner / souper) en c36 es exacta.
2. **Explicaciones es / en.** Cortas, con «tú», léxico neutro (departamento, jugo no aparece, canasta, mesero, computadora, bolso); el inglés compara (hunger «had» not «been», polite je voudrais vs je veux, «second floor»).
3. **Una respuesta defendible; `aceptadas`.** Revisados todos los ordenar (órdenes con adverbio al inicio o al final presentes), escribir y completar. Las variantes de números sin guion (`deux cent cinquante euros`) ya son la respuesta base.
4. **Pistas y relacionar.** Cada pista ayuda a su ítem (-s / -t, plural con -iss-, faut = «fo»…). Los pares de los cinco relacionar tienen glosas distintas (receta / harina / huevos / pastel; elegir / comprar / olvidar / terminar; botella / paquete / caja / rebanada / trozo; planta baja / último piso / ticket / mil).
5. **Sonidos del día.** c36 an / en (y ils prennent sin nasal), c37 eu cerrada / abierta, c38 oi, c39 o abierta / cerrada, c40 e final muda: exactos y coherentes con las fichas. ü y ö se definen en c36 p1 y se reutilizan.
6. **Hablantes.** Solo nombres del reparto (Léa, Ana, Hugo) o papeles en francés (La vendeuse, La caissière).
7. **Reparto coherente.** Hugo (estudiante, ama el café, examen, fiesta el 5 de mayo, tercer piso), Léa y Emma (planta baja; Emma bebe té), Ana (primer piso, ecuatoriana). Fecha de la fiesta y pisos coinciden con `hechosDelReparto`. Cada comprensión tiene una sola respuesta.
8. **Cortesía.** Je voudrais frente a je veux (c37), Bonjour madame, s’il vous plaît, merci (c39, c40), À bientôt (c38).

## Observaciones no bloqueantes

- **Tarjetas de vocabulario** (campo `vocabulario` de la unidad): c36 15 y c39 15 (la ficha lista 12). Los extras son los aprobados arriba (ensemble, apprendre, comprendre, assez, il faut). El paso `vocabulario` muestra solo las 12 de la ficha.
- c37 e5 acepta faire y cuisiner junto a préparer; «cuisiner un gâteau» es correcto aunque menos frecuente.
- En español de América «primer piso» no significa lo mismo en todos los países; c40 lo avisa ahora en la explicación.

## Palabras de B9 (prenez / prends / prenons, veux / voulez / peux, dois, première / deuxième)

No se eliminó ni se renombró ninguna palabra francesa de B8. Todas siguen enseñadas (prendre completo en c36; vouloir y pouvoir en c37; devoir en c38; première, deuxième en c40). B9 valida con 0 errores encadenado.

## Sin resolver

Nada que bloquee. Validación final: 0 errores (B8 solo y B8 + B9).
