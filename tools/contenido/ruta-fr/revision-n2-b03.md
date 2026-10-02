# Revisión independiente · N2 francés, bloque 3 (clases 11–15)

- **Archivo:** `tools/contenido/ruta-fr/n2-b03.json` (`fr.n2.c11` … `fr.n2.c15`). Revisor distinto del autor.
- **Validador:** `python3 tools/validar_ruta.py fr --borrador …n2-b01.json …n2-b02.json …n2-b03.json` → **0 errores** (repetido tras los últimos cambios). B3 sola da errores «palabras no enseñadas» (mais, oui, maison…) porque esas palabras las enseñan B1/B2: es lo esperado, no un fallo de B3.
- **Plan:** `python3 tools/curriculo/validar_plan.py fr` → 0 errores; ningún aviso «título de la unidad difiere» para c11–c15.

## Veredicto

GO

## Contraste con las fichas

Cada clase enseña lo que dice su ficha y nada de clases posteriores de N2: c11 le / la / l’ / les + negación + mettre; c12 qui / que / qu’ (+ buscar, preguntar el precio); c13 où relativo + y (presente, negación, futuro próximo); c14 ne… plus / rien / personne (rien antes del participio, personne después; sujeto rien ne / personne ne); c15 lui / leur + dire / lire / écrire. No aparece el accord del participio con el pronombre COD (solo reconocimiento, más adelante). Títulos y objetivos coinciden con el plan. Anatomía y tiempos: explicación (+ nota de pronunciación) → tablas → ejemplos (8) → vocabulario → guiada (5, con pista) → independiente (4) → situación (9–10 líneas, 86–100 palabras, 2 ítems) → evaluación. Cada evaluación tiene ≥ 6 ítems puntuables en 6 formatos; el `escribir` con `abierta: true` no puntúa y se suma a esos ítems.

## Cambios aplicados (clase · ítem · antes → después)

### c11
1. **Situación (contexto), coherencia con la decisión de la historia.** «Emma deja el departamento de Léa y se queda un tiempo con Ana» → Emma deja el departamento que compartía con Léa y, mientras ella y Ana buscan un departamento para las dos, se instala unos días en casa de Ana (así c11 precede sin contradicción a la búsqueda de c12 y al departamento nuevo de c13–c15).
2. **Vocabulario `les toilettes` (es).** «el sanitario, el inodoro…» → «el baño (el cuarto pequeño con el inodoro, aparte del cuarto de baño)»; ejemplo 4 y diálogo línea 8: «El sanitario está…» → «El baño (el del inodoro) está cerca de la cocina» / «El baño del inodoro está cerca de la puerta». En: «the toilet (the small room)» → «the toilet (the small separate room)».
3. **Guía de sonido `les toilettes`.** «le tua-lèt» → «lé tua-lèt» (les = «lé»).
4. **Nota de `la cuisine` (en).** «ü as defined in the note below» → «…pronunciation note above» (la nota va antes de las tarjetas).
5. **p1, p4 (tabla le/la/l’/les) — regla de la elisión.** «l’ delante de vocal / Before a vowel» podía leerse como vocal del sustantivo (el ejemplo es «Le tapis ? Je l’aime») → «l’ cuando el verbo empieza por vocal o h muda»; el texto de la tabla añade «mira la primera letra del verbo, no la del sustantivo» (es / en) y la celda «masculino o femenino, si el verbo empieza por vocal».
6. **Evaluación: ítem nuevo e7 (completar).** «Le tapis ? Je ___ aime beaucoup.» (l’ / le / la; aceptadas `l'`, `l`): la ficha pide l’ y no se evaluaba. El ejercicio abierto pasa de e7 a e8.

### c12
7. **p8 · i2 (completar).** «Le studio ___ Ana visite…» → que + vocal exige elisión (**qu’Ana**), así que «que» era incorrecto → «Le studio ___ Léa visite est près du métro» (consigna y feedback con Léa).
8. **Anglicismo británico.** «flatshare» (6 apariciones: vocabulario, ejemplo, diálogo, e2, e5 consigna y par) → «shared apartment» (inglés americano).
9. **Situación (contexto).** «buscan un departamento» → «buscan un departamento nuevo para vivir juntas» (es / en), alineado con la decisión de la historia (Madame Dubois, propietaria, vive en la planta baja del edificio nuevo: ya lo decía la línea 4 del diálogo).

### c13
10. **Nota de pronunciación.** «on y va = «o-ni va»» → «on-ni va» (la nasal on + liaison n; en: “oh-nee VAH” → “ohn-nee VAH”).
11. **p9 · i3 (escribir).** «el sábado» es ambiguo (samedi / le samedi): + aceptadas «Nous y allons le samedi.», «On y va le samedi.», «Samedi, nous y allons.», «Samedi, on y va.».
12. **p11 · e6 (escribir).** + aceptada «Le marché où je vais samedi est près d’ici.».

### c14
13. **Vocabulario `le plombier`.** «el plomero (el fontanero)» → «el plomero» (fontanero es de España).
14. **p3 (tabla de negaciones), texto.** «Todas rodean al verbo conjugado» era falso para personne en el passé composé → «Ne va delante del verbo conjugado y la otra palabra va detrás (con personne en el passé composé, detrás del participio: mira la tabla siguiente)» (es / en).
15. **p11 · e6 (escribir).** + aceptada «Personne n’est dans la cuisine.» (forma válida con personne sujeto).

### c15
16. **p1 (explicación).** «En español usas le / les para todos…; la diferencia es que en francés lui no distingue masculino y femenino» era engañoso (le del español tampoco distingue género) → «Equivalen al le / les del español (le escribo = je lui écris; les digo = je leur dis) y, como ellos, no distinguen el género».
17. **p10 · i4 (escribir).** «Le pido a Ana que ponga la mesa» admitía también «Je demande à Ana de mettre la table» (válido, pero sin el pronombre objetivo) → consigna «Escribe en francés con lui: …»; respuesta única «Je lui demande de mettre la table.».
18. **Situación (contexto).** «viven juntas» → «viven juntas en su departamento nuevo» (es / en).

## Revisión punto por punto

1. **Francés de Francia.** Posición del pronombre y negación (je le mets, je ne la trouve pas, nous ne les mettons pas, je n’y vais pas), futur proche con y (on va y aller; no se evalúa «je vais le mettre» porque c11 no lo incluye), y delante del verbo, rien antes del participio y personne después (je n’ai rien fait / je n’ai vu personne), qui / que / qu’ / où, lui (un sujeto, sin género) / leur (sin -s) frente a le / la / les con verbos con à (demander, dire, téléphoner, écrire, répondre). Conjugaciones de mettre, dire, lire, écrire correctas. Tipografía: U+202F y ’.
2. **Explicaciones es / en.** Cortas y con ejemplos; es con tú y léxico neutro (baño, alcaldía, refrigerador, plomero, sala); en americano (apartment, faucet, plumber, elevator, hot water, trash, laundromat, dry cleaner’s).
3. **Respuesta única y `aceptadas`.** Revisados los `ordenar` (el segundo orden con el complemento circunstancial al inicio ya figura donde existe), `completar`, `escribir` y `elegir`. Un distractor por ítem, siempre erróneo (je mets le, que a, qui il a, je ne y vais, je la dis merci).
4. **Pistas y relacionar.** Cada pista ayuda a su ítem (género y número en c11, verbo vs. sujeto en c12, lugar vs. función en c13, tipo de palabra en c14, una persona vs. varias en c15). Glosas de `relacionar` distintas en las 10 listas (mueble / habitación / tarea / lugar / averías).
5. **Guías de sonido (regla 6).** ch / g suave = «sh» (en: «zh»), nasales an / on / en / ain = «an / on / en» (en: aviso de que la n no suena), ü y ö definidas en c11 (primera clase del bloque), «ö» para eu / e, enlaces (nous y allons, on y va), s final muda.
6. **Hablantes.** Solo Ana, Emma y Madame Dubois. Madame Dubois: vous, 68 años, propietaria, vive en la planta baja; Ana y Emma, en el primer piso (c12 y c14).
7. **Situaciones.** 9–10 líneas, 86–100 palabras (objetivo N2: 6–10 líneas, ≈ 80–120 palabras) y una sola respuesta correcta por pregunta.

## Hechos del reparto confirmados

- Ana y Emma se mudan juntas a un departamento nuevo que alquilan a Madame Dubois (c12–c15). / Ana and Emma move together into a new apartment they rent from Madame Dubois.
- Emma deja el departamento que compartía con Léa y, antes de mudarse, pasa unos días con Ana (c11). / Emma leaves the apartment she shared with Léa and stays a few days with Ana before the move.
- Madame Dubois es la propietaria, se trata de vous y vive en la planta baja (rez-de-chaussée) del edificio nuevo; el departamento está en el primer piso (c12, c14). / Madame Dubois is the landlady, addressed with vous, and lives on the ground floor of the new building; the apartment is on the 1er étage (US second floor).
- Léa y Hugo siguen en el edificio antiguo y vienen a cenar a casa de Ana y Emma (c15). / Léa and Hugo stay in the old building and come to Ana and Emma’s for dinner.
- Ana pide el alquiler (950 euros, más 80 de gastos) y visita el departamento un sábado a las 10 h (c12). / Ana asks about the rent (950 euros plus 80 in utilities) and views the apartment on a Saturday at 10.
- Ana y Emma reparten las tareas: Emma lava los platos y saca la basura, Ana lava la ropa y pasa la aspiradora (c15). / Ana and Emma split the chores: Emma does the dishes and the trash, Ana the laundry and vacuuming.

## Sin resolver (no bloquea)

- **Pisos coincidentes:** en N1 Ana vive en el primer piso del edificio antiguo y en N2 B3 también en el primero del edificio nuevo (con Dubois en la planta baja). No hay contradicción, pero el coordinador puede variar el piso del nuevo departamento si quiere evitar la confusión.
- **`personajes` de n2.json:** Léa dice «amiga de Chloé y de Hugo…» y Emma «deja el departamento de Léa y lo comparte con Ana» (coherente); Madame Dubois «vive en el piso de abajo» (coherente). Conviene que el coordinador precise en `datos` de Dubois que es la planta baja del edificio nuevo (no el antiguo).
- c11 no incluye «je vais le mettre» (futur proche con COD) porque la ficha no lo pide; si el coordinador lo quiere, iría en una clase posterior.
- Referencias a Madame Dubois en los ejemplos de c15 («Je lui téléphone demain») dependen de que c14 cierre la avería con ella; coherente en el orden actual.

Validación final: 0 errores.
