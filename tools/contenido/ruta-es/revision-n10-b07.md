GO

## Validación

`python3 tools/curriculo/validar_bloque.py es 10 7` → 0 error(es) del bloque (tras las correcciones). Lecturas: c31 473, c32 459, c33 484, c34 496, c35 482 palabras. Ningún hablante repite turno; todos los `completar` tienen un solo `___`; todas las preguntas de comprensión tienen opciones en español, sin distractores verdaderos; las respuestas correctas quedan en posiciones 0, 1 y 2 repartidas.

## Correcciones

- [explicación-falsa] c31 p2, explicación de la concordancia: «adjectives in -or add -a» → «adjectives in -dor add -a» (mejor, peor, superior no cambian) (baja)
- [explicación-falsa] c31 erroresFrecuentes[0]: «adjectives in -or» → «-dor» (baja)
- [apoyo-en] c31 p7 g3, feedback: mezcla de español e inglés («desigual is not parejo; prescindible is not necesario») → frase inglesa completa (baja)
- [explicación-falsa] c32 p2: «Parecer + adjective … sounds a little more tentative» (contradecía la nota de «resulta» y el diálogo) → «it gives your impression of the work» (media)
- [explicación-falsa] c32 vocabulario «la reivindicación»: «rreh-ee-been…» (dos sílabas) → «rray-been-dee-kah-SYOHN», ei es un solo sonido (media)
- [aceptadas] c32 p8 i2: añadido el orden natural «La novela adquiere otro sentido a la luz del contexto histórico» (baja)
- [reparto] c33 situación, Emma: «Llevo dos días pensando en el final» → «tres días» (de la noche del sábado 5 a la tarde del martes 8) (media)
- [idioma-es] c33 situación, Sofía: «Una película que hace discutir tres lecturas…» → «Una película que deja tres lecturas distintas…» (más natural) (media)
- [explicación-falsa] c33 p7 g1, feedback: decía que la segunda opción cierra la discusión y la tercera no es español correcto, al revés de las opciones; reordenado (correcta en posición 0) y feedback corregido (alta)
- [pedagogía] c33 situación s1: la respuesta correcta quedaba otra vez en la posición 1; opciones reordenadas (correcta en 2) (baja)
- [explicación-falsa] c33 p10 e1, feedback: «use a form that does not exist» (la opción 3 existe, pero no tiene sentido) → explicación verdadera; opciones reordenadas (correcta en 0) (media)
- [explicación-falsa] c33 erroresFrecuentes[0] y p10 e2: «impersonal passive» → «the se of the passive» (pasiva refleja con sujeto) (baja)
- [idioma-es] c33 vocabulario «el vacío», nota: «vacío/a» con barra → «vacío, vacía» (baja)
- [pedagogía] c33 tabla «To read»: quitada la fila «protesta» (ya enseñada en una clase anterior; el validador sigue en 0) (baja)
- [explicación-falsa] c34 vocabulario «el ejemplar»: pronunciación «eh-heh-mm-PLAHR» → «eh-hehm-PLAHR» (media)
- [pedagogía] c34 tabla «To read»: quitadas las filas de los nombres propios Borges y Neruda; pasan a una tabla «Names you will meet» (el validador exige que los nombres se enseñen antes de usarse) (baja)
- [apoyo-en] c34 tabla, fila «rendir, rinde»: «to pay» (inexacto) → «to render, to give; rendir homenaje = to pay tribute» (media)
- [explicación-falsa] c34 p10 e1, feedback: citaba «citarse a», que no es una opción; ahora «Rendir de and olvidar a do not have that meaning» (media)
- [explicación-falsa] c34 p10 e5, feedback: «a is optional before a title» (contradecía «evocar no lleva preposición») → la a aparece ante «Pedro Páramo» por ser también nombre de personaje (baja)
- [explicación-falsa] c35 erroresFrecuentes[1]: «Words ending in -ción are feminine, so learners guess canon is feminine» (canon no termina en -ción) → explicación correcta sobre -ón (el canon, el balcón) y -ción/-sión (alta)
- [pedagogía] c35 tabla «To read»: quitada «considera» (ya enseñada antes); los nombres propios (Alicia Yánez Cossío, Palacio, Cortázar y García Márquez) pasan a una tabla «Names you will meet»; el ejemplo del boom nombra a Cortázar y García Márquez (baja)
- [pedagogía] c35 situación s1: el distractor «Pablo Palacio» podía ser verdadero según lo enseñado en los ejemplos; → «García Márquez», que el texto da por incluido en el canon (media)
- [otro] c35 situación, Sofía: «sus libros son difíciles de conseguir» (afirmación no verificable sobre una autora real) → «las obras como la suya son difíciles de conseguir», general y verdadera; traducción ajustada (media)
- [reparto] c35 situación, Sofía: «El lunes les mando tres opciones» (lunes 14, fuera del calendario obligatorio del 5 al 13) → «El sábado» (sábado 12) (media)
- [explicación-falsa] c35 vocabulario «la obra», nota: «Obras is also used for the whole production» (el ejemplo era singular) → «La obra de Rulfo also means the whole body of work of an author» (baja)

## Hechos del reparto confirmados

- «El último tren de Chimbacalle» es una película ecuatoriana ficticia, de una directora sin nombre / «El último tren de Chimbacalle» is a fictional Ecuadorian film by an unnamed woman director
- La película ocurre en 1999, el año de la crisis bancaria (feriado bancario de marzo de 1999; dolarización en 2000) y se estrenó en 2034 / The film is set in 1999, the year of the banking crisis (bank holiday of March 1999; dollarization in 2000), and was released in 2034
- La película dialoga con «Pedro Páramo» (Juan Rulfo, 1955); la directora lo cita en una entrevista / The film is in dialogue with «Pedro Páramo» (Juan Rulfo, 1955); the director mentions it in an interview
- Emma, Mateo y Sofía comentan la película y se tutean; en c35 se suma Andrés Vaca y los cuatro se tutean / Emma, Mateo and Sofía discuss the film and use tú; in c35 Andrés Vaca joins and all four use tú
- Calendario de mayo de 2035: sáb 5 cineclub en Quito (c31), dom 6 almuerzo en La Floresta (c32), mar 8 café en La Floresta (c33), jue 10 casa de Sofía (c34), vie 11 oficina de Puente en La Floresta (c35) / May 2035 calendar: Sat 5 cineclub in Quito, Sun 6 lunch in La Floresta, Tue 8 café in La Floresta, Thu 10 at Sofía's house, Fri 11 at the Puente office in La Floresta
- Emma leyó «Pedro Páramo» en el club de lectura del 3 de junio de 2032 (n7-b09), «hace unos tres años» / Emma read «Pedro Páramo» in the reading club on June 3, 2032 (n7-b09), «about three years ago»
- Sofía le presta a Emma su ejemplar (edición vieja) de «Pedro Páramo» el jueves 10 / Sofía lends Emma her old-edition copy of «Pedro Páramo» on Thursday the 10th
- Mateo propone usar las referencias de Rulfo en los tours literarios de Puente / Mateo proposes using the Rulfo references in Puente's literary tours
- Puente añade a sus lecturas una novela de Alicia Yánez Cossío; Sofía enviará tres opciones el sábado 12 y Andrés calculará el costo y llamará a la editorial / Puente adds a novel by Alicia Yánez Cossío to its readings; Sofía will send three options on Saturday the 12th and Andrés will calculate the cost and call the publisher

## Sin resolver

- Nada que bloquee. Aviso para el coordinador: el validador exige que los nombres propios (Borges, Neruda, Cortázar, García Márquez, Alicia Yánez Cossío, Palacio) se enseñen antes de usarse y que no vayan en filas «To read»; se resolvió con una tabla «Names you will meet» (como en n7-b09). Si más adelante se añaden estos nombres a `palabrasLibres` de curso.json, esas tablas se pueden quitar.
- Las afirmaciones sobre Yánez Cossío (novelista ecuatoriana; obra con humor y crítica social) y Pablo Palacio (escritor ecuatoriano) son generales y verdaderas; no se les atribuye ninguna obra concreta.

Total: 25 correcciones (2 altas, 11 medias, 12 bajas)
