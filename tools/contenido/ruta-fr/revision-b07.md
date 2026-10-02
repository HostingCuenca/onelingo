# Revisión independiente · N1 francés, bloque 7 (clases 31–35)

- **Archivo:** `tools/contenido/ruta-fr/n1-b07.json` (`fr.n1.c31` … `fr.n1.c35`)
- **Revisor:** IA independiente (no autora). Perfil: profesor A1 de francés de Francia, con español latinoamericano e inglés americano.
- **Fecha:** 2026-10-01
- **Validador:** `python3 tools/validar_ruta.py fr --borrador tools/contenido/ruta-fr/n1-b05.json tools/contenido/ruta-fr/n1-b06.json tools/contenido/ruta-fr/n1-b07.json` → **0 errores** (se repitió al final, ya con la regla 6 de calibración y con c25 enseñando grand / petit).
- **Plan:** `python3 tools/curriculo/validar_plan.py fr` → 0 errores; ningún aviso «título de la unidad difiere» para c31–c35. Los 10 avisos que quedan son de situaciones del catálogo fuera del bloque del marco (incluido c31 → situación 43); son del plan, no del contenido.
- **Comprobación extra «nada sin enseñar»** (script propio, más estricto que el validador: solo cuentan ejemplos, tarjetas mostradas, patrón y tabla de esta clase o anteriores): 0 faltas en respuestas, opciones, audios, diálogos, tokens y pares. Solo quedan el distractor `hôpitals` (c32 e6) y la variante aceptada `vas-tu` (c33 i4), que no se muestran como respuesta.
- **Reciclaje** (palabras de ejemplos y diálogos ya enseñadas antes): c31 64 %, c32 71 %, c33 78 %, c34 83 %, c35 73 % (≥ 30 %).
- **Tipografía:** 0 signos ? ! : ; con espacio normal; 0 apóstrofos rectos en campos en francés.

## Veredicto

GO

## Cumplimiento de las fichas (c31–c35)

Cada clase enseña lo que dice su ficha y no adelanta nada de c36–c50: no hay prendre/boire, vouloir/pouvoir/devoir, cantidades, ordinales, imperativo, preposiciones de lugar nuevas (sur, devant…), futur proche, passé récent ni passé composé. «un peu» (c32) ya lo enseñó c03. `se trouver` (c35) se presenta explícitamente como verbo pronominal «como se lever (clase 30)» y se conjuga se trouve / se trouvent: coherente con c30. Títulos y objetivos coinciden con el plan.

## Cambios aplicados (clase · ítem · antes → después)

### Guías de pronunciación (regla 6 de calibración: j y g suave = «sh», in/ain/un = «en»)

1. **c31 · v-jeune.** «yön» → «shön».
2. **c31 · v-gentil y tabla p3 (fila gentil).** «yan-ti» / «yan-tiy» → «shan-ti» / «shan-tiy».
3. **c31 · v-cheveux.** «che-vö» (ch se leería como en español) → «she-vö».
4. **c31 · v-voisin.** «vua-sen» → «vua-zen» (s entre vocales = z, como en «mezón» de B2).
5. **c31 · v-brun y p1.** «como «un»» (ambiguo con el «un» español) → «bren»; en inglés, “bran” sin sonido de n.
6. **c32 · v-joli.** «yo-li» → «sho-li».
7. **c32 · v-ancien.** El femenino «an-syen» se leía como nasal, igual que el masculino. Ahora: masculino «an-syen» (nasal), femenino «an-syenn» (n que suena); en inglés “ahn-syan” / “ahn-syen”.
8. **c33 · v-boulangerie.** «bu-lan-je-ri» (j como en español) → «bu-lan-shö-ri».
9. **c33 · tabla p3 (je vais).** «yö vé» → «shö ve».
10. **c34 · v-venir y tabla p3.** «yö vien» → «shö vyen»; «vien» → «vyen» en todas las filas nasales; las filas ils / elles viennent «vién» → «vyenn» (misma convención «nn» que c31 para una n que suena). Se corrigen también p1 y el feedback de g4.
11. **c34 · v-japon.** «La j suena como la «y» de «ya»…: «ya-pon»» → «La j suena como una «sh» suave: «sha-pon»».
12. **c34 · v-belgique.** «bel-yik» → «bel-shik».
13. **c34 · p1.** «bre-tañ» → «brö-tañ» (la e muda es «ö», definida en c31).
14. **c35 · v-region.** «ré-yon» → «ré-shyon».
15. **c35 · v-il-neige y g3 (pista).** «nej» (la j española es otra cosa) → «nesh».
16. **c35 · p1.** «kon-bien» → «kon-byen» (in = «en»).
17. **c32 · p1 (sonido del día).** Afirmaba que «o», «ô», «au» y «eau» suenan igual: la «o» sola suele ser abierta (moderne, joli) y Fundamentos solo dice que au / eau suenan «o». Ahora: «au», «eau» y «ô» = «o» cerrada; la «o» sola es algo más abierta (es y en).

ü y ö se definen en c31 (p1 y p5) y se usan después sin cambios.

### Contenido y progresión

18. **c31 · grand / petit (aviso del coordinador).** c25 ya los enseña. Se mantienen como repaso: las notas dicen «Ya conocías grand / petit (clase 25: c’est trop grand). Con personas significa alto / bajo» y la explicación p2 añade la misma remisión. No se presentan como vocabulario nuevo.
19. **c31 · situación (diálogo, contexto y s1).** Antes: una sola vecina en la foto («C’est notre voisine… Elle a des enfants ? … Leur fils…»). Leur exige varios poseedores, así que «leur fils» de una sola persona era incorrecto. Después: una pareja de vecinos (Ana: «Qui est-ce ?» → Léa: «Voilà nos voisins ! Elle est petite et brune, il est grand et blond. Ils sont très gentils.» → «Ils ont des enfants ?»). Modela masculino, femenino, plural, nos y leur. s1 pasa a «¿Cómo es el vecino?» (alto y rubio; distractores bajo y moreno / bajo y rubio), con una sola respuesta. Contexto es/en ajustado.
20. **c31 · i3.** `___ voisins sont gentils` (Nos) → `___ amis sont gentils` (Vos; «Sus amigos (de ustedes)»). Así votre / vos, que el objetivo pide, se practican; nos sigue en e5.
21. **c33 · ejemplos.** Faltaba un ejemplo con aux (solo aparecía en la explicación y en e6). «Ils vont à la piscine.» → «Léa et Emma vont aux États-Unis.».
22. **c33 · situación, última línea.** «Super ! À demain !» (Ana no queda con Hugo al día siguiente: él va al museo con Léa) → «Super ! Bonne journée !» («¡Que tengas un buen día!»).
23. **c33 · i4 (¿Adónde vas?).** `aceptadas` + «Où est-ce que tu vas ?» (est-ce que, c19).
24. **c33 · g5 (pista en inglés).** «Bibliothèque and piscine look like English» (falso) → «“biblio-” is books and a piscine has water».
25. **c34 · ejemplos.** Tenía 9 (máximo 8) y ninguno con de la. Se quita «Il vient du Portugal : il parle portugais.» y «Il vient du parc et il va à la piscine.» pasa a «Hugo vient du parc, et Léa vient de la gare.».
26. **c34 · g3.** «Elle vient du Canada» (repetía el du de g2) → «Je viens de la gare.» / «Je viens du gare.» / «Je viens à la gare.», para practicar de la, que el objetivo anuncia.
27. **c34 · tabla p4.** Columna «País» con la fila «Paris» → «Lugar / Place»; título «Ciudades y países: estar y venir».
28. **c34 · situación (contexto).** Ana esperaba en el vestíbulo y luego decía «Je vais à la gare»: ahora el contexto explica que los padres llegan hoy, que se alojarán en ese hotel y que ella irá a la estación.
29. **c35 · situación (línea 2 de Ana).** El diálogo solo cubría «dónde está» y el tiempo. Se añade «C’est une grande ville avec un vieux quartier !» (cómo es), con adjetivos antes y después. La comprensión s1 sigue con una sola respuesta.
30. **c35 · e5 (¿Qué tiempo hace?).** `aceptadas` + «Quel temps fait il ?» (sin guion, que el corrector no normaliza) y «Quel temps est-ce qu’il fait ?».
31. **c35 · g4 (pista en español).** «ouest a «west» u «oeste»» (inglés dentro del texto en español) → «ouest a «oeste»».

## Revisión punto por punto del encargo

1. **Francés de Francia.** Concordancia (grande, belle, gentille, brune; nos / vos / leurs), posición (antes: BAGS; después: calme, moderne, animé, ancien, bruyant), bel / vieil / nouvel ante vocal o h muda, de + adjetivo plural (de beaux châteaux, de vieux ponts), plurales -eaux / -aux, contracciones au / aux / du / des con à la / à l’ / de la / de l’ intactas, en / au / aux con países y d’ / de / du / des, puntos cardinales con artículo, il fait beau / chaud / froid, il pleut, il neige, Quel temps fait-il ?. Todo correcto. En c32 e5 se acepta también «des beaux châteaux» (muy usado en la lengua hablada); la explicación y el feedback enseñan la forma normativa «de beaux».
2. **Explicaciones es / en.** Claras y cortas; es con tú y léxico neutro (departamento, vecino). En compara con el inglés donde ayuda (their no cambia, adjetivo antes / después, «hace calor» ≠ «il est chaud»).
3. **Una respuesta defendible; `aceptadas`.** Revisados todos los `ordenar` (órdenes con adverbio al inicio en c33; sin orden alternativo natural en los demás), `escribir` y `completar`. Variantes añadidas en los puntos 23 y 30; ya existían «Où tu vas / Où vas-tu», «On vient de France», «sud est».
4. **Pistas y relacionar.** Cada pista ayuda a ese ítem (g1 «¿masculino o femenino?», g3 «escucha il / elle / ils y si la n suena», g4 c34 «n sonora / nasal»). Pares de relacionar con glosas distintas (alto / bajo / joven / tímido; viejo / nuevo / tranquilo / ruidoso; estación / correo / biblioteca / piscina; Alemania / Brasil / Japón / China; norte / sur / este / oeste).
5. **Sonidos del día.** c31 bon / bonne y brun / brune, c32 o / au / eau, c33 h muda, ph y th, c34 gn, c35 on / om: exactos tras los cambios de arriba y coherentes con las fichas.
6. **Hablantes.** Solo nombres del reparto (Ana, Hugo, Léa, Lucas) o papeles en francés (La réceptionniste, La cliente).
7. **Personajes.** Ana (de Quito, vive en París; padres en Quito), Léa (hermano pequeño: «petit et blond», coherente con los 11 años de c15), Hugo y Emma (con Léa), Lucas (Canadá, videollamada con Ana), Emma estadounidense (c34). Formas femeninas para Ana y las mujeres. Cada pregunta de comprensión tiene una sola respuesta.
8. **Anatomía.** Sonido → explicación → tablas → ejemplos (5–8) → tarjetas → guiada (5) → independiente (4) → situación (6 líneas, 2 ítems) → evaluación (6 ítems, 5 formatos en cada clase). Los 6 formatos aparecen en el bloque. `erroresFrecuentes`: 4 por clase.

## Observaciones no bloqueantes

- **Número de tarjetas de vocabulario** (campo `vocabulario` de la unidad): c31 16, c32 13, c35 16 (la ficha lista 12). Los extras son necesarios o ya figuran en la gramática de la ficha: notre / vos / leur y voisin (c31); hôtel para bel hôtel (c32); il neige y le sud-est (c35); Lyon y Marseille como nombres propios. El paso `vocabulario` muestra solo las 12 de la ficha; el resto se enseña en tablas y ejemplos.
- **c32:** hôtel se repite como tarjeta de c33 (l’hôtel), sin conflicto.
- **Plan:** c31 usa la situación 43, que el plan valida con aviso (fuera del bloque 7 del marco). Decisión del coordinador.
- La convención «nn = n que suena» (bonn, brune, an-syenn, vyenn) se explica en c31 p1 y se reutiliza en c34 y c35; la regla 6 del encargo no la nombra, pero evita ambigüedad con «en» = nasal.

## Sin resolver

Nada que bloquee. Validación final: 0 errores.
