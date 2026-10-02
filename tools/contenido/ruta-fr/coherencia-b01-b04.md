# Coherencia de personajes · N1 francés c01–c20 (B1–B4)

Reparto canónico impuesto: Ana (26, ecuatoriana de Quito, recién llegada a París, estudia francés en la escuela de idiomas), Hugo Durand (20, francés, universitario), Léa (19, francesa, estudiante; madre médica y hermano de 11 años), Emma (estadounidense, estudiante, comparte piso con Léa, trabaja de noche en un restaurante), Chloé Bernard (canadiense en París, secretaria de la escuela, casada con un canadiense), Lucas (18, canadiense, vive en un pueblo de Canadá; amigo en línea de Ana), Martin (solo el profesor).

Fuente editada: `n1-b01.json` … `n1-b04.json` (+ `palabrasLibres` en `assets/contenido/fr/ruta/curso.json`). Todo en es y en sincronizado. `integrar.py` termina con 0 errores.

## Conflictos pedidos

| Clase | Ítem | Antes → después |
|---|---|---|
| c01 | paso 8 (situación), contexto | «Ana compra pan donde Martin, el panadero» → «Ana compra pan en la panadería de su barrio» |
| c01 | paso 8, hablante líneas 2 y 4 | `Martin` → `Panadero` (las líneas francesas ya eran «Bonjour, madame !» / «Au revoir, madame.») |
| c01 | paso 8, s1 (opción 1 y feedback) | «Con Martin, el panadero» → «Con el panadero»; feedback «Con Martin, Ana dice…» → «Con el panadero, Ana dice…» |
| c02 | paso 3, ejemplo 5 | «Mon nom, c’est Martin» → «Mon nom, c’est Bernard» (es: «Mi apellido es Bernard») |
| c02 | paso 8 (situación), contexto | «Primer día de clase de francés» → «Primer día de curso» (Hugo y Léa son franceses, no podían estar en una clase de francés). Martin sigue siendo el profesor |
| c03 | paso 9 (situación), contexto | «en la oficina… llega Martin, el jefe» → «en la universidad… llega una profesora» |
| c03 | paso 9, hablante líneas 4 y 6 | `Martin` → `Profesora` (diálogo francés sin cambios) |
| c04 | paso 9, diálogo línea 2 | «Je m’appelle Hugo Martin.» → «Je m’appelle Hugo Durand.» (es/en igual) |
| c04 | paso 9, contexto | «se inscribe en una escuela de idiomas» → «se inscribe en un curso de inglés en una escuela de idiomas» |
| c16 | paso 9 (situación), contexto | «Hugo se presenta ante Ana, una chica que no conoce» → «un vecino se acerca a Ana, la chica nueva del barrio, a quien no conoce» |
| c16 | paso 9, diálogo | Hablante `Hugo` → `Vecino` (sin nombre). Línea 1: sin «Je m’appelle Hugo» → «Salut ! Tu es française ?». Línea 2 de Ana: se quita «Enchantée, Hugo.». Línea 4 de Ana: «Non, je n’habite pas ici. Je suis étudiante à Quito.» → «Oui, j’habite ici. Je ne suis pas de Paris : je suis de Quito.» |
| c16 | paso 9, s2 | texto «Non, je n’habite pas ___.» (resp. «ici», aceptada «à Paris») → «Oui, j’habite ici. Je ne suis pas de ___ : je suis de Quito.» (resp. «Paris», sin aceptadas); feedback actualizado. Conserva el objetivo (ne… pas con être + de + ciudad); s1 (nacionalidad de Ana) intacto |
| c17 | paso 9, contexto | «Ana es nueva en el barrio» → «Ana acaba de mudarse a París y es nueva en el barrio» |
| c10 | paso 4, ejemplo 7 | «Léa et Emma travaillent dans un magasin.» → «Léa et Hugo étudient à Paris.» (es «Léa y Hugo estudian en París.»). Sigue mostrando la terminación muda -ent; no hay ítems que dependan de la frase |
| curso.json | `palabrasLibres` | + «Durand», «Bernard» (se mantienen las anteriores) |

## Otros conflictos encontrados (script que lista toda línea con un personaje)

| Clase | Ítem | Antes → después |
|---|---|---|
| c05 | paso 9, contexto | «Una fiesta internacional en París» (Lucas vive en Canadá) → «Una videollamada internacional de un club de idiomas. Léa, desde París, conoce a Lucas y a Emma.» |
| c06 | paso 9, contexto | «En una fiesta, Ana le muestra a Lucas una foto…» → «En una videollamada, Ana le muestra a Lucas, su amigo canadiense, una foto de sus amigos de París.» |
| c08 | paso 9, diálogo línea 2 | Ana «J’habite à Quito, en Équateur.» → «J’habite à Paris, en France.» (es «Vivo en París, en Francia.»; «en France» ya se enseña en c08) |
| c08 | paso 9, contexto y s1 | contexto añade «ahora que se ha mudado a París»; opción 2 «En el centro de Quito» → «En el centro de París» |
| c10 | paso 9, diálogo línea 3 | Emma «Je parle anglais et français…» → «Je parle anglais, français et italien…» (coincide con lo que dice Emma en c07) |
| c13 | paso 9, diálogo líneas 2–4 | Hugo «j’ai un cours de français» (era francés) → «j’ai un cours» (sin «d’anglais»: no enseñado); «Et Lucas et Chloé ?» (Lucas vive en Canadá) → «Et Léa et Chloé ?»; «Ils sont… Ils ont» → «Elles sont… Elles ont» |
| c13 | paso 9, s1 y s2 | opción «Una clase de francés» → «Una clase»; s2 «Ils ___ à la maison.» → «Elles ___ à la maison.» (resp. «sont»), feedback ajustado |

## Revisado y sin cambios
c07 (Ana conoce a Emma en línea), c09, c11, c12, c14 (edades 19/20/18), c15 (hermano de 11 años, marido canadiense de Chloé), c18 (madre médica), c19 (Martin profesor de Hugo en la universidad), c20 (Ana, 26 años, ecuatoriana, se inscribe en la escuela con Chloé).

## Puntos blandos
- c05: Léa «conoce» a Emma por videollamada; se interpreta que se hacen compañeras de piso después (c10).
- c02/c04: Hugo y Léa están en el «curso» de Martin en c02 (sin decir de qué) y Hugo se apunta a inglés en c04.
- Los hablantes sin nombre son etiquetas en español (`Panadero`, `Profesora`, `Vecino`), como `Secretaria` o `Camarero` en otros bloques.
