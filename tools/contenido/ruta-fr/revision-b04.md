# Revisión independiente · N1 francés, bloque 4 (clases 16–20)

- **Archivo:** `tools/contenido/ruta-fr/n1-b04.json` (`fr.n1.c16` … `fr.n1.c20`)
- **Revisor:** IA independiente (no autora), perfil profesor A1 de francés de Francia, con español latinoamericano e inglés americano.
- **Fecha:** 2026-10-01
- **Validador:** `python3 tools/validar_ruta.py fr --borrador tools/contenido/ruta-fr/n1-b04.json` → **0 errores**.
  La cadena completa `--borrador b01 b02 b03 b04` ya no se puede usar tal cual: el integrador copió B1–B3 a `assets/contenido/fr/ruta/` y `curso.json`, así que al pasarlos otra vez como borrador salen «id de unidad duplicado» (c01–c15). Validé B4 contra el curso real (que ya contiene B1–B3) y la validación global `validar_ruta.py fr` también da 0 errores.
- **Comprobación adicional «nada sin enseñar» (más estricta que el validador):** script propio que exige que cada palabra francesa de respuestas, opciones, audios, diálogos, tokens y pares aparezca antes en `ejemplos`, `vocabulario` (tarjetas mostradas), `patron` o `tabla` de esta clase o de una anterior (Fundamentos + B1–B3 integrados). Resultado: 0 faltas (la única pasada era «étudiants» en c16 e4; corregida).

## Veredicto

GO

Todos los puntos del encargo quedan resueltos (ver abajo). Quedan dos observaciones sobre B3, que ya está integrado y que este revisor no podía tocar (sección «No corregido»); no bloquean B4.

## Recuentos

| Clase | Concepto | Tarjetas | Ejemplos | Guiada / indep. | Diálogo | Errores frecuentes | Evaluación |
|---|---|---|---|---|---|---|---|
| c16 | negacion | 10 | 8 | 4 / 4 | 6 | 3 | 6 ítems, 6 formatos |
| c17 | pas-de-il-y-a | 10 | 8 | 4 / 4 | 6 | 4 | 6 ítems, 5 formatos |
| c18 | c-est-il-est | 10 | 8 | 4 / 4 | 6 | 3 | 6 ítems, 6 formatos |
| c19 | preguntas | 10 | 7 | 5 / 4 | 6 | 3 | 6 ítems, 5 formatos |
| c20 | quel-telefono | 8 | 8 | 4 / 4 | 6 | 3 | 6 ítems, 6 formatos |

- **Reciclaje:** entre el 79 % y el 94 % de las palabras de ejemplos y diálogos de cada clase ya se habían enseñado (muy por encima del 30 %).
- **Tipografía:** 0 signos ? ! : ; con espacio normal y 0 apóstrofos rectos en los campos en francés.
- **Convenciones numéricas:** ortografía tradicional (`vingt et un`, `trente et un`… sin guiones; `vingt-deux`… con guion). La reforma de 1990 (`vingt-et-un`) se explica en los textos de las tablas y se acepta en `aceptadas` donde el alumno escribe un número en letras. En los diálogos y la tabla de 21–69 no hay `et` con guiones.

## Cambios aplicados (clase · ítem · antes → después)

### Integración con B1–B3

1. **c16 · prerrequisito.** `fr.n1.c05` → `fr.n1.c15`.
2. **c17 · número 20 y duplicado de B3.** El 20 ya lo enseña B3 c14 (`vingt`). La tarjeta `vingt` (con nota de sonido) pasa a `la rue`; el texto de la tabla 20–29 dice ahora «El 20 ya lo conoces (clase 14)». Se mantiene la fila 20 de la tabla como puente, sin presentarla como nueva.
3. **c20 · edad como reciclaje, no como tema nuevo.** Antes: tarjetas `quel âge ?` y `un an` («la edad se dice con avoir: j’ai vingt ans») y la explicación 2 reexplicaba avoir. Después: se eliminan esas dos tarjetas; la explicación empieza con «Ya sabes preguntar la edad con quel: Tu as quel âge ? (clase 14)», presenta quel/quelle para cualquier dato y solo recuerda en una frase que la edad va con avoir. La edad se practica como uso de quel en el diálogo (`Quel âge avez-vous, madame ?`, que es la forma de B3) y en s2 (`J’ai ___ ans`).
4. **c20 · tarjeta ton / ta.** Antes: «tu (con tu: ton + masculino, ta + femenino)». Después: `ton / ta / votre`, con nota «Ya los conoces de la familia (ton frère, ta sœur)»; `votre` no se había enseñado antes y aparecía en los ejemplos.
5. **c20 · teléfono.** La explicación 3 añade: «Los pares del 10 al 20 ya los conoces (clase 14); los del 70 al 99 los verás en el bloque 5» (los números de este bloque solo llegan a 69).
6. **c17 · pas de y un/une/des de B3.** La explicación remite a «el mismo un / une / des de la clase 11, ahora en negativo». Se añade la contraparte que faltaba y que el alumno ve en B2 (aimer): le / la / les no cambian. Fila nueva en la tabla (`J’aime le café.` → `Je n’aime pas le café.`), cuarto error frecuente (`Je n’aime pas de café.` → `Je n’aime pas le café.`) y fila preparatoria en la tabla de c16 (`j’aime le café` / `je n’aime pas le café`).
7. **Personajes (coherencia con B1–B3).** Se evita fijar edades, nacionalidades u oficios nuevos para Lucas, que en B1–B3 es a la vez el amigo canadiense, el hermano de Léa de 11 años y un chico de 18.
   - c18 · diálogo: Antes: «C’est Lucas, un ami. Il est canadien.» / «Il est médecin» (Lucas médico) / «C’est le chat de Lucas». Después: Léa muestra a Ana fotos de su madre («C’est ma mère. Elle est médecin.», madre francesa de c15) y «C’est le chat de mon frère !». Las comprensiones se ajustaron (s1: la madre es médica; s2: completar «Elle ___ médecin»).
   - c18 · ejemplos: «C’est une photo de Lucas. Il est canadien.» → «C’est une photo de Hugo. Il est français.».
   - c18 g2: «Hablas de Hugo» + «___ est médecin» (Hugo, 20 años, médico) → «Hablas de la madre de Léa» (respuesta `Elle`; opciones `Elle` / `C’`).
   - c19 · diálogo: Chloé (secretaria o alumna de 19 años en B1/B3) hacía de profesora de Hugo, que es francés → Martin, el profesor de c02, en la universidad (como en c13), con «Oui, bonjour, monsieur.».
   - c20 · diálogo: Martin pasa de profesor a «recepcionista» (en B1 es panadero, profesor y jefe) → Chloé, la secretaria de la escuela de idiomas de c04, que trata de vous a Ana.
8. **Femenino y estados.** Se mantiene el género de los personajes femeninos (Ana: `française`, `équatorienne`, `fatiguée`, `enchantée`).

### Correcciones por clase

**c16 (ne… pas)**
- Título, objetivo y explicaciones sin cambios de fondo.
- **p1 sonido del día.** Inglés: «like the “u” in “the” with rounded lips» (confuso: «the» se pronuncia con schwa y sin labios redondos) → «a short, soft “uh” with rounded lips, like the vowel in “deux”». Español: «como en «deux»» → «como la de «deux» (labios redondeados)».
- **g4 pista.** Antes: «¿Oyes «ne… pas»?» (no distingue entre «No estoy casada» y «No soy de aquí»). Después: «Hay dos cosas que mirar: ¿oyes «ne… pas»? ¿Oyes «mariée» o «d’ici»?».
- **e4 (palabra no enseñada).** Opciones con `étudiants` (plural no enseñado) → `Nous ne sommes pas mariés.` / `Nous sommes mariés.` / `Vous n’êtes pas mariés.` (mariés sí está en ejemplos). Se corrigen el feedback y la traducción de apoyo.
- **Diálogo (c16).** Antes: Hugo preguntaba a una desconocida «Et tu es mariée ?» y no había «Et toi ?», «Enchantée» ni presentación. Después (6 líneas): «Salut ! Je m’appelle Hugo. Tu es française ?» / «Enchantée, Hugo. Non, je ne suis pas française. Je suis équatorienne. Et toi ?» / «Moi, je suis français. Tu habites à Paris ?» / «Non, je n’habite pas ici. Je suis étudiante à Quito.» / «Tu es fatiguée ?» / «Non, pas du tout !».
- **s2.** `Non, je n’habite pas ___.` → `ici`; se añade `à Paris` en `aceptadas` (porque la línea anterior de Hugo menciona París).

**c17 (pas de, il y a, 20–29)**
- **Título.** «pas de e il y a» (la «e» ante palabra francesa que empieza con i- se lee mal) → «pas de / il y a».
- **p1 sonido.** La guía escribía «ven» y luego «vent-dö»; el texto decía que la n no se pronuncia. Se añade «(en las guías, una n escrita después de la vocal solo indica nasalidad: no cierres la boca con la n)», en español y en inglés.
- **Tabla 20–29.** Se añade la nota sobre la grafía de 1990 (`vingt-et-un`).
- **ordenar i1 / e4.** Se añaden órdenes naturales a `aceptadas`: «Ici, il n’y a pas de pharmacie.» y «Dans la rue, il y a un chat.».
- **escribir i2 / completar i3 (números).** `aceptadas` completas: `24`, `vingt-quatre`, `vingt quatre` / `23`, `vingt trois`. El corrector de la app no normaliza los guiones: sin estas variantes un alumno que escribe «vingt trois» fallaba.
- **g4 pista.** «Mira la tabla de 20 a 29.» (genérica) → «Cada cifra termina como el número que ya sabes: deux = 2, cinq = 5, huit = 8; «et un» = 1.».
- **Diálogo.** Antes (5 líneas) solo practicaba pas de; el bloque pedía los números 20–29 en la situación. Después (6 líneas): se mantienen las cuatro líneas de pharmacie/café/voiture/vélo y se añade «Moi non plus ! Et ton appartement, c’est le vingt-trois ?» / «Non, c’est le vingt-huit !». s2 (¿Hugo tiene coche?, redundante con la línea 4) → «¿Cuál es el número del apartamento de Hugo?» (23 / 28 / 22).

**c18 (c’est / il est, qui est-ce, qu’est-ce que c’est)**
- **Título.** «C’est e il est» → «C’est / il est».
- **Vocabulario.** De 10 tarjetas, 8 repetían literalmente B3 (livre, stylo, sac, clé, téléphone, photo) y la clase casi no tenía palabras nuevas. Se sustituyen stylo, sac, téléphone y photo por `un crayon`, `un cahier`, `un ami / une amie` y `un professeur / une professeure`, con notas de sonido (kreyón, kayé, ami = amie, profesör). Siguen stylo, téléphone, photo y sac en ejemplos y práctica como reciclaje.
- **Tabla.** Las filas con `rouge` / `bleue` (colores: B5) → `C’est Léa. / Elle est française.` y `C’est un chien. / Il est sympa.`.
- **Ejemplos.** «C’est un stylo rouge.» (color no enseñado en vocabulario) → «Ce n’est pas un crayon, c’est un stylo.» (además muestra que c’est no cambia al negar, como en c17); «Qu’est-ce que c’est ? — C’est un téléphone.» (duplicaba el primero) → «C’est une amie de Léa. Elle est étudiante.».
- **g3 relacionar.** Pares livre / cahier / crayon / clé (glosas claramente distintas), con pista «Piensa para qué sirve cada cosa: una «clé» abre una puerta; un «cahier» es para escribir.» (antes «Mira las tarjetas de vocabulario»).
- **e5 escribir.** Se acepta `C’est qui ?` (forma natural y enseñada en B2 c06) además de `Qui est-ce ?`.
- **Diálogo.** Reescrito con la madre de Léa (ver Integración 7); incluye «Elle est sympa ? — Oui, très sympa !».

**c19 (preguntas, est-ce que, 30–49)**
- **Tarjeta rara.** `est-ce qu’il` («¿él…?») → `est-ce que / est-ce qu’il` (una sola tarjeta, con la regla de que → qu’) y nueva tarjeta `la fête` (la fiesta), que aparece en ejemplos, i4, e3 y el diálogo y no estaba en tarjetas.
- **Tabla 30–49.** La nota ahora dice que 31 y 41 llevan «et un» sin guiones (desde 1990 también «trente-et-un»).
- **escribir i2.** `aceptadas` + `quarante-et-un`.
- **ordenar e4.** `aceptadas` + «Combien d’étudiants il y a ?» (orden natural con la palabra interrogativa al inicio).
- **g5 pista.** «Mira la tabla de las palabras para preguntar.» → «où es lugar, combien es cantidad, quand es tiempo y pourquoi es causa.».
- **Diálogo.** Martin y Hugo (ver Integración 7), con «Oui, bonjour, monsieur.» para modelar la cortesía.

**c20 (quel / quelle, 50–69, teléfono)**
- **Objetivo.** «decir la edad» como tema → «Pedir datos con quel / quelle (también la edad)».
- **g3 pista.** «La edad no va con être.» (no distingue entre `Tu as quel âge ?` y `Tu as quelle âge ?`) → «Comprueba dos cosas: ¿avoir o être? ¿Quel o quelle?».
- **g4 pista.** «Mira las tablas de números.» → «Cada decena empieza como su cifra: trois → trente, quatre → quarante, cinq → cinquante, six → soixante.».
- **completar i3.** `aceptadas`: `58`, `cinquante huit`.
- **Tabla 50–69.** Nota de 1990 para 51 y 61.
- **Diálogo.** Antes: Martin pedía nombre, nacionalidad y celular de forma encadenada. Después: Chloé pregunta nacionalidad, edad («Quel âge avez-vous, madame ?») y teléfono («…, s’il vous plaît ?»), con cortesía y las tres funciones de quel. s2: `portable` / `téléphone` (dos respuestas posibles) → completar `J’ai ___ ans` (respuesta `vingt-six`; `26` y `vingt six` aceptadas).

## Revisión punto por punto del encargo

1. **Francés y tipografía.** Elisiones correctas (n’, qu’, d’, c’), U+202F antes de ? y !, apóstrofo ’. Números 21–69 con ortografía tradicional y variante de 1990 aceptada donde se escribe un número. Teléfonos de dos en dos (06 45 52 68 31, etc.), con 01–09 como «zéro + cifra» y `aceptadas` con y sin separadores (`0622335567`, `06.22.33.55.67`, `06-22-33-55-67`).
2. **Nada sin enseñar.** Comprobado con el script estricto (ver arriba): 0 faltas.
3. **Explicaciones bilingües.** Español con tú; el inglés compara con «do», «not», «I am twenty», «what / which», «no» (pas de).
4. **Una respuesta defendible; `aceptadas`.** Revisados todos los `ordenar` (órdenes naturales añadidos en c17 y c19), los `escribir`/`completar` con números y los de pregunta (c18 e5: `C’est qui ?`; c19 e5 con `française`).
5. **Pistas y relacionar.** Pistas rehechas en c16 g4, c17 g4, c18 g3, c19 g5, c20 g3 y g4. Pares de relacionar con glosas claramente distintas.
6. **Sonidos del día.** c16 (e muda y «ö»), c17 (nasales «in/ain/ien», y = i, aviso sobre la n de las guías), c18 (qu = k), c19 (an/en nasales), c20 (-el/-elle, x de soixante) son exactos. «ö» se define en c16 (primera aparición en B4) y «ü» ya la define B1.
7. **Diálogos.** Modelan el objetivo de cada clase y la cortesía (Enchantée, Et toi ?, madame / monsieur, s’il vous plaît). Cada comprensión tiene una sola respuesta.
8. **Anatomía y errores frecuentes.** Cumple en las cinco clases (tabla de recuentos).

## No corregido / avisos para el integrador (fuera de B4)

1. **B3 c14 (ya integrado):** la guía de sonido de `vingt` usa «van» (y «van-tan» en «vingt ans»; también «kanz» para quinze), mientras que B4 c17 usa «ven» (la vocal de «vingt» es la de «in», no la de «an»). No toqué B3. Si se quiere uniformar, lo exacto es «ven» / «ven-tan». No afecta al validador.
2. **Lucas en B1–B3:** es el amigo canadiense (c05, c08), el hermano de Léa de 11 años (c15) y un chico de 18 años (c14). B4 evita fijar su edad, nacionalidad u oficio, pero la inconsistencia sigue en B1–B3 y conviene resolverla en el integrador. También Chloé aparece como secretaria (c04), profesora (c08) y amiga de 19 años en B3; B4 usa solo la versión «secretaria de la escuela» (c20).
3. Esta validación se hizo con B4 como único borrador, porque B1–B3 ya están integrados. Si se retiran de `assets/contenido/fr/ruta/` para integrar de nuevo, la cadena `b01 b02 b03 b04` deberá volver a dar 0 errores.
