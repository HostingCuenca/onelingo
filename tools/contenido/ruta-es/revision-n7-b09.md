GO

## Validación
`python3 tools/curriculo/validar_bloque.py es 7 9` → 0 error(es) del bloque (tras las correcciones). Calendario comprobado: c41 jueves 3, c42 sábado 5, c43 jueves 10, c44 viernes 18, c45 jueves 24 de junio de 2032 (todo correcto). Lecturas: 369 / 352 / 347 / 355 / 353 palabras (dentro de 300–500). Ningún hablante tiene dos turnos seguidos. Gramática nueva = solo el `introduce` de cada ficha; ejercicios según el plan de cada ficha.

## Correcciones
- [reparto] es.n7.c42, ejemplos, i/e4 (audio, opciones, feedback): «Andrés» → «Pablo» (choque con Andrés Vaca) (media)
- [reparto] es.n7.c42, p6 ejemplo y e5 (consigna, respuesta, aceptadas): «Carmen» → «Ana» (choque con doña Carmen) (media)
- [pedagogía] es.n7.c41, g3: consigna «Which sentence is written as a synopsis?» → «Which sentence follows the synopsis rule (the whole plot in the present)?» para que los distractores en pasado y futuro sean errores inequívocos (media)
- [explicación-falsa] es.n7.c42, p2: «a voz en off speaks in the first person and in the present» (falso en general) → habla en primera persona, como el estilo directo, y suele decir lo que el personaje piensa en el momento (media)
- [explicación-falsa] es.n7.c42, situación (Sofía): «La voz en off dice “yo” y usa el presente» → «En esta película, la voz en off…» (y su traducción) para no generalizar (baja)
- [explicación-falsa] es.n7.c43, vocabulario v-murmurar: «the rr is rolled» (murmurar no tiene rr) → acento en la última sílaba y r suaves (baja)
- [aceptadas] es.n7.c43, erroresFrecuentes + p2 + i3/e4: el guion corto se aceptaba en los ítems mientras erroresFrecuentes lo llamaba error → opción (a): se quita ese error de erroresFrecuentes (quedan 3), p2 explica que en la escritura cuidada se usa la raya y que el guion se acepta solo por comodidad de teclado, y los feedback de i3 y e4 lo dicen igual (alta)
- [aceptadas] es.n7.c43, g1: distractor «¿Dónde estás? -preguntó Emma» (guion corto, ahora tolerado) → «¿Dónde estás? preguntó Emma.» (sin raya); feedback ajustado (media)
- [apoyo-en] es.n7.c44, erroresFrecuentes 1: «with no article and no de or you can say los dos hermanos» → «with no article and no de. You can also say los dos hermanos.» (baja)
- [apoyo-en] es.n7.c45, situación (Mateo): «there is a praise that is repeated» → «there is a compliment that is repeated» (baja)
- [idioma-es] es.n7.c45, erroresFrecuentes 3: «Hay alguien que conozca el final.» (válido en pregunta o con duda) → «Hay alguien que conozca el final: Mateo.» / «…conoce el final: Mateo.», persona concreta y conocida, y la explicación recuerda cuándo sí va el subjuntivo (media)

## Hechos del reparto confirmados
- Club de lectura en un café de La Floresta con Sofía, Mateo y Emma, que se tutean / Reading club at a café in La Floresta with Sofía, Mateo and Emma, who use tú with each other
- Sesiones de junio de 2032: jueves 3 (primera), sábado 5 (cine y café), jueves 10 (segunda), viernes 18 (cine), jueves 24 (última) / June 2032 sessions: Thursday 3 (first), Saturday 5 (film and café), Thursday 10 (second), Friday 18 (film), Thursday 24 (last)
- El club lee «Pedro Páramo» y «Cien años de soledad» / The club reads “Pedro Páramo” and “Cien años de soledad”
- Mateo es de Guadalajara (Jalisco), como Juan Rulfo / Mateo is from Guadalajara (Jalisco), like Juan Rulfo
- Emma leyó el año pasado la novela que luego ven adaptada en el cine (c42) / Emma read last year the novel they then see adapted at the cinema (c42)
- Sofía propone al final (jueves 24) preparar juntos el DELE C1 el año siguiente; Mateo y Emma aceptan / At the end (Thursday 24) Sofía proposes preparing the DELE C1 together next year; Mateo and Emma accept
- B9 no menciona el viaje de estudiantes ni el informe (no contradice B10) / B9 does not mention the student trip or the report (no conflict with B10)

## Sin resolver
- es.n7.c41, p4a («The novel we will summarize»): lleva filas con nombres propios (Pedro Páramo, Juan Preciado, Comala, Juan Rulfo), contra la regla 5 de calibración; no es una tabla «To read» y el validador la acepta, pero conviene añadir a `palabrasLibres` Pedro, Juan, Páramo, Preciado, Comala, Rulfo y Jalisco y retirar esa tabla. Decisión del coordinador (curso.json).
- es.n7.c43: entre p3b (7 filas) y p4 (15 filas, con formas de lectura como escondí/escondiste/escondes, leerla, probemos) hay 22 palabras de lectura; cada tabla cumple el máximo de 15, pero la carga es alta. Reducible reescribiendo la situación con menos formas nuevas.

Total: 11 correcciones (1 altas, 6 medias, 4 bajas)
