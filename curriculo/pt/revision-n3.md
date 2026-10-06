# Revisión del plan N3 (portugués de Brasil)

Veredicto: GO

Validadores sobre `curriculo/pt/n3.json`: `validar_plan.py pt` → 0 errores (312 avisos de vocabulario repetido, esperables en un nivel B1 que recicla; 87 son de N3); `validar_plan_detallado.py pt curriculo/pt/n3.json` → 0 errores · 50 clases · 662 ejercicios · 662 consignas únicas · 662 ejemplos únicos. Los 50 ids están en estado `planificado` y los campos congelados (id, bloque, título, objetivo, gramática, introduce, recicla, vocabulario, sonido, situación, tarea) coinciden con `tools/curriculo/pt/n3-outline.json`.

Revisión independiente de las 50 clases (los 10 lotes completos, leídos ítem por ítem). A diferencia de N2, los lotes de N3 llegaron en buen estado: no había distractores absurdos tipo «ontem», ni europeísmos, ni subjuntivo/pasiva fuera de plan, y la gramática de cada ejercicio coincide con su clave. Se aplicaron **32 correcciones puntuales** (11 de canon, 9 de distractores, 2 de ambigüedad, 10 de coherencia, 0 de lengua pt-BR) en los lotes de `tools/curriculo/pt/` y se consolidó el nivel. Copia de los lotes originales en el scratchpad del revisor.

## Cambios por tipo

### Canon y personajes (11)

El reparto secundario cambiaba de oficio de una clase a otra y chocaba con el cliente de B7 y B8:

- pt.n3.c01–c05, c26, c28: el colega «Rafael» (equipo de producto, c01–c05) coincidía con el cliente «Rafael» de c17/c20 y el cliente «senhor Rafael Moura» de c39; además era «paciente de 35 años» (c26) y «el que dejó de fumar» (c28). Pasa a **Davi** (nombre secundario ya usado en N2) en esas siete clases; Rafael queda solo como el cliente Rafael Moura (c17 «com o Rafael Moura, cliente de uma agência de turismo», c20, c39).
- pt.n3.c18: «Carolina» (compañera de equipo que corrige errores) chocaba con **Carolina Dias**, dueña de la agencia de turismo de B7 (c31–c38) → «Júlia».
- pt.n3.c19: «Luana» como organizadora del encuentro de diseño era la compañera de equipo de c02 → «Larissa».
- pt.n3.c39: «Rafael Moura, um cliente novo» (ya era cliente desde c17) → «um cliente».
- Ningún personaje canónico recibe oficio ajeno: Bruno (coordinador), Ana (diseñadora), Dona Marina (jubilada), Dra. Helena, seu Alberto y Lucas coinciden con el MAPA. Gloria, Jaime y Valeria (familia) aparecen como en el MAPA; los parientes de Medellín (madrina Patricia, padrino Hernando, cuñado Andrés) y los secundarios sin canon se listan abajo para confirmar.

### Distractores absurdos, agramaticales o no plausibles (9)

- c08 i2: «Bruno estava avisando o cliente quando caiu» (frase sin sentido) → «Bruno avisou o cliente ontem» (contraste real futuro próximo / pasado).
- c10 e0: «uma ocorrência de boletim» (orden inventado) → «Preciso fazer uma boletim de ocorrência» (error real de género).
- c11 s0: «uma árvore na fazenda de Recife» (la familia es de Medellín) → «uma palmeira na praça de Medellín».
- c13 g1: «ficou programador» (ambiguo en habla coloquial) → «tornou programador» (error real: falta el reflexivo de tornar-se).
- c22 e0: «Sería posible hablar com…» (frase en español) → «Seria possível falo com outro funcionário?» (error real de forma verbal tras «seria possível»).
- c30 i2: «Sempre que chove, treinei em casa amanhã» (absurdo temporal) → «…treinei em casa» (contraste real presente habitual / perfeito).
- c32 e1: «para el cual» (español, no interlengua) → «É o projeto para que trabalhamos este mês» (error real: para que ≠ para o qual).
- c45 i1: «O filme dirigiu uma recifense» (absurdo) → «Uma recifense dirigem o filme» (error real de concordancia).
- c46 i1: «O filme premiou três festivais» (absurdo) → «O filme foi premiados em três festivais» (error real de concordancia de la pasiva).

### Lengua, gramática y registro pt-BR (0)

No se halló nada que corregir: sin europeísmos (autocarro, telemóvel, «estou a fazer», «me dói»), sin «tu», sin ortografía anterior al Acordo. Se respetan las dos variantes aceptadas: «Que bom que ele esteja…» y «tornou-se / se tornou», «lhe / te» como contraste de registro (c23), «pedir para eu + infinitivo» (c38). Las tres pruebas de calco con palabras españolas (c31 «sirve», c34 «oficina», c35 «presupuesto», c40 «Como así?») se mantienen: están rotuladas en la consigna como calco y son interferencias reales del hispanohablante.

### Ambigüedad, estímulo insuficiente y claves (2)

- c40 i1: la opción correcta confirmaba «o protocolo é 4821» pero la situación dice 58213 → «58213».
- c44: la situación decía «A sinopse é linda: um trecho do filme…» (una sinopse es texto, no un trecho de la película) → «O trailer é lindo: mostra o cenário do Capibaribe ao amanhecer». Las palabras de vocabulario de la ficha (trecho, sinopse) se conservan por estar congeladas.

### Coherencia con la historia y hechos reales (10)

- c21–c25 (Noronha): el retraso era de tres horas en la situación de c21 (de las 9h al mediodía) pero de cuatro en c24 → c21 pasa de las 8h al mediodía; «chegaríamos depois das dez da noite» (imposible con vuelo al mediodía) → «depois das duas da tarde».
- c18–c19–c25: c18 decía que Camila vuelve a la oficina «no dia 23», pero en c25 regresa de Noronha el lunes 23 de noche → «no dia 24» (martes). Fechas verificadas con el calendario de 2028: sábado 14 y domingo 22 de octubre; sábado 21 de octubre (charla); lunes 23.
- c23: a seu Alberto (dueño del piso) Camila le pedía «entregar a encomenda para o vizinho» (no es su función) → «regar as plantas da varanda» (el piso tiene varanda, N2).
- c16 g0: el plan B del grupo era el Café da Bia, pero el ítem proponía el Cinema São Luiz → Café da Bia.
- c28 / c30: c28 decía que Camila «voltou a correr, como fazia em Miami», pero c30 dice que en Kendall «quase não corria» (y c28 g0 «depois de dois anos parada») → «como fazia na faculdade»; c30 g1 pasa a «Quando eu morava em Kendall, quase não corria».
- c44: la «mostra de 10 a 16 de setembro» quedaba en el pasado en pleno final de año (B6 transcurre en noviembre) → «de 10 a 16 de dezembro» en situación, ítems y resumen (10 al 16 de diciembre de 2028 es domingo a sábado); la fecha de ejemplo «12 de agosto» → «sábado, 16 de dezembro».
- c50 e1: la Dra. Helena recomendaba siete horas en c26 y ocho en el cierre → siete.

## Límites aceptados

- El esqueleto de ejercicios es el mismo en las 50 clases (3 guiados + 3 independientes + 2 de situación + 5–8 de evaluación; c50 con 8 y c49 con 6, un relacionar con propuestas cruzadas por clase): es el formato del nivel y lo exige el validador. Cada clase mantiene datos, escena y distractores propios.
- Conversaciones entre Gloria/Jaime y Dona Marina (c11–c12, c14) en portugués fluido: es una convención didáctica; el canon (padres hispanohablantes) lo cubre con «portugués sencillo o con ayuda de Camila» en los datos de Gloria.
- La película «Entre Pontes», su directora y su banda sonora son ficticios (no se inventa infraestructura real: sí el Cinema São Luiz, el Paço do Frevo y el Marco Zero, que están en el MAPA).
- La enclisis («trocá-lo») queda como en N2: solo reconocimiento. La pasiva analítica (c45) es de reconocimiento con `foi gravado`/`foi dirigido por`.
- c35 y c34 nombran «assistência técnica em Graças» y «oficina perto da estrada» de forma genérica (sin marcas ni calles).
- El vocabulario congelado de c44 («trecho», «sinopse») no aparece ya en la situación tras la corrección de arriba; no es un error del validador.

## Hechos del reparto confirmados

- Camila cumple 29 años el 14 de marzo de 2028; en N3 B1 es ascendida a líder de producto en Maré Digital (Porto Digital); Bruno sigue de coordinador; vive con Ana en Graças (dueño: seu Alberto Tavares, o senhor). Moneda: R$.
- B2: pierde el celular un martes de lluvia, lo recupera el miércoles en los achados e perdidos de la empresa de ônibus (protocolo 4517), sin necesidad de boletim de ocorrência.
- B3: Gloria y Jaime visitan Recife en julio de 2028 (conocen a Dona Marina en Boa Viagem; Jaime engorda dos kilos por la tapioca); vuelven a Miami y planean regresar en diciembre con Valeria; Kendall; abuela materna en Medellín.
- B5: Noronha del sábado 14 al domingo 22 de octubre de 2028 (UTC−2); vuelo con 4 h de retraso, mala azul extraviada (protocolo 4521), vuelo de vuelta cancelado (diária extra R$ 420, voucher R$ 50, reclamo con protocolo 7316); trabaja de nuevo el martes 24.
- B6: Dra. Helena Rocha (a senhora) aconseja siete horas de sueño y no tomar café después de las 16h (octubre); en noviembre Camila retoma la corrida en la avenida de la playa de Boa Viagem a las 6h. Sin diagnósticos.
- B9–B10: Cinema São Luiz, Paço do Frevo, Marco Zero y Recife Antigo reales; maracatu del grupo de Lucas.

## Hechos nuevos a confirmar (no están en el MAPA)

- **Carolina Dias** (dueña de una agencia de turismo, cliente de Maré Digital, você) y **Rafael Moura** (cliente, o senhor): se proponen como personajes secundarios de N3 B4 y B7–B8; no repiten nombre del reparto.
- **Jonas** (central de atendimento de internet), **Moacir** (técnico), **Patricia** (hermana de Gloria y madrina de Camila), **Hernando** (padrino), **Andrés** (cuñado de Jaime) y los colegas **Davi, Júlia, Larissa, Paulo** del equipo de producto.
- Edades en 2028 para `personajes`: Gloria 57, Jaime 60, Valeria 24 (N2 conservó 22 para Valeria; conviene decidir si N2 debe subir a 23).
- Película ficticia **«Entre Pontes»** (drama pernambucano de 2028) y mostra del Cinema São Luiz del 10 al 16 de diciembre (entradas a R$ 10); gran evento de 2028: charla de Camila en un encuentro de diseño en Porto Digital, sábado 21 de octubre (online).
