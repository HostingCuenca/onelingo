GO

# Revisión pt N3 B1 (pt.n3.c01–c05)

Validador: `python3 tools/curriculo/validar_bloque.py pt 3 1` → 0 errores. Borrador del autor respaldado en el scratch (`rev-n3-b01/n3-b01.autor.json`). Total de correcciones: 27 (más 8 conversiones mecánicas `preguntaApoyo` → `pregunta`).

## Contraste con las fichas
- Las 5 clases enseñan exactamente su `introduce` (subjuntivo regular, irregular, Que bom/Que pena que, Que você/Tomara que, marcadores de novedad); reciclan lo de su `recicla`. Formatos, claves y tarea de evaluación siguen el plan de ejercicios. Nombres de las fichas (Davi, Luana, Bruno, Ana, Lucas, Bia, Dona Marina) conservados; ninguna mención de Ecuador.
- ESCUCHA: ya había 2 `escuchar` por clase (10 en total: c01 g2/e1, c02 g2/e2, c03 g1/i1, c04 g2/e3, c05 g1/e3), todos con distractor = error real (conversa/converse, sabe/saba/saiba, dá/dê, pois é vs. olha só). Los 5 `relacionar` de la ficha (c01 e4, c02 g3/e3, c03 e3, c05 i1) se conservan. Evaluaciones con ≥4 ítems puntuables y ≥2 formatos.
- Lecturas de la situación: 130–137 palabras (mínimo del validador para N3: 130).

## Cambios por tipo
**Pronunciación / explicaciones (4)**
- c01 explicación 3: «decida» tiene tónica «i», no «e» cerrada → «lidere» (es y en). «no los iguales» → «no los mezcles».
- c02 explicación 3: «tenha» ≈ «tenia» → «teña» (la «nh» suena como «ñ»).
- c05 tabla «Marcadores»: ejemplo «Sabia que a Bia vai viajar?» (hecho inventado) → «Sabia que a festa é no sábado?».

**Hechos y cronología (7)**
- c05 situación: «a gente pode falar disso no sábado» cuando el diálogo ya ocurre un sábado → «na segunda» (es «el lunes», en «on Monday»).
- c05: los padres «querem visitar Recife em junho» (ficha y autor) choca con el MAPA (llegan en julio de 2028) → «em julho» en la situación (añadido) y en la evaluación e5 (consigna es/en y modelo). Fila «julho» añadida a «Para ler».
- c05 e5: «o São João aqui é lindo» (junio, y julio es temporada de lluvias) → «o café da Bia é ótimo».
- c05 ejemplos 1 y 2: «Bia vai abrir outro café» (hecho nuevo e innecesario) → «a festa do café é no sábado às 19h» / «Que bom que a festa seja no sábado!».
- c04: Ana, línea «…esteja na sala às 10h, também a equipe de produto» (forzada) → recortada; Lucas agrega «Obrigado, Dona Marina! Camila, que a sua apresentação seja ótima!» para mantener 130+ palabras.
- c03 contexto: Ana y Camila viven juntas en N3; se aclara «(Ana no está en el apartamento)» para el mensaje de voz.
- c02 contexto: tarjeta «de la equipe y de sus amigos» (firman Lucas y Dona Marina, que no son del equipo).

**Apoyo es/en (5)**
- Columnas de «Para ler»: «Frase» en inglés → «Sentence» (5 tablas); «Exemplo» → «Example».
- c01 fila «mãos»: «manos (las manos)» → «las manos». c03 fila «estágio»: «el internado de práctica» → «la pasantía, las prácticas».

**Deduplicación contra N1–N2 (10 filas de «Para ler» eliminadas por ya enseñadas)**
- c02: descansar, fim de semana, precisa, sempre. c03: festa. c04: tudo, ótimo. c05: mostra, confirma, pergunta, pode deixar. Además se retira la fila «lindo» (c05, ya sin uso) y en c01 la fila «esperar» queda limpia (espero/espere, sin formas mezcladas).
- Dudas de verbos extra: `vir` (n1.c32), `gostar` (n1.c09/c30), `dar` (n2.c13) y `chover` (n2.c19) ya están enseñados en presente; en c03/c04 solo se añaden sus formas de subjuntivo (venha, goste, dê, chova), que es lo nuevo y lo que piden los ejercicios: se dejan en las tablas, sin añadirlas a `vocabulario`. `passar` (passe) no estaba enseñado: queda solo como glosa en «Para ler» de c04. Resueltas.

**Validador de meta (8)**
- `preguntaApoyo` con texto idéntico en es y en (portugués) → `pregunta` (meta); así el validador comprueba las palabras: afloró «longo» (c05 e1) → «Camila: Hoje o dia foi ótimo.».

## Dudas del autor, decididas
1. Verbos extra: ver arriba.
2. Hechos (lunes del ascenso, Davi/Luana/Marina felicitan, fiesta del café sábado 19h, prova jueves 14h y entrevista viernes 9h, Ana a Caruaru, padres): coherentes con el MAPA; solo se corrigió «junio» → «julio». El «viernes» de c02 (Ana invita al Café da Bia) es otra celebración (el ascenso), distinta de la fiesta del sábado; se deja.
3. c03 «Que bom que» + subjuntivo, con nota sobre el indicativo coloquial: correcto.

## Falsos amigos marcados (⚠)
ninguém (c03), torcida y prova (c04), pois é y aliás (c05); notas de «esperar» (c01) y «mudança» (c02). No se inventan falsos amigos nuevos.

## Correcciones de ficha
- pt.n3.c05, `ejercicios.evaluacion[4]` («los padres de Camila querem visitar Recife em junho»): el MAPA fija que Gloria y Jaime llegan en julio de 2028; debería decir julho.

## Hechos del reparto confirmados
- Lunes: Bruno anuncia en el grupo del equipo de producto de Maré Digital que Camila es la nueva líder de producto; felicitan Bruno, Davi, Ana y Luana. Bruno le pide presentar las metas del trimestre el jueves, abrir la reunión de planejamento y que Davi le mande el relatório; Camila pide dos ideas por persona para el próximo mes; Ana propone una tapioca juntas en el almuerzo.
- Tarjeta de felicitación (Ana la organiza; escriben Davi, Luana, Lucas, Dona Marina, Bruno): Ana invita a Camila a comemorar con la gente en el Café da Bia el viernes.
- Martes por la noche: Ana (fuera del apartamento) manda un mensaje de voz con 4 noticias: el cliente aprobó el protótipo, Davi está enfermo y no viene el miércoles, Ana no irá a la fiesta de aniversario del café del sábado porque viaja a Caruaru con su familia, Lucas tiene entrevista de estágio en una empresa del Porto Digital el viernes.
- Jueves, 8h (grupo «Amigos de Recife»): la primera presentación de Camila como líder para un cliente es a las 10h; Lucas tiene prova de algoritmos a las 14h y la entrevista de estágio el viernes a las 9h; Dona Marina está en el grupo (llama «minha filha» a Camila); la fiesta de aniversario del Café da Bia es el sábado a las 19h (Bia espera que no llueva; habrá maracatu, rumor del grupo de Lucas).
- Sábado a la tarde, Café da Bia: Lucas consiguió el estágio (se lo contó a Bia el viernes); Camila contó a sus padres su ascenso y su mamá quiere visitar Recife en julio; Camila y Bia hablarán del tema el lunes. Davi vuelve al trabajo el lunes.
- Nombres secundarios usados: Davi, Luana (colegas de Maré Digital, sin oficio fijo). Dona Marina tutea con você y Camila le dice «a senhora»; el resto se trata de você.

## Sin resolver
- Ninguno.
