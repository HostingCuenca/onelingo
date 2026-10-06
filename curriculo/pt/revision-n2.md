# Revisión del plan N2 (portugués de Brasil)

Veredicto: GO

Validadores sobre `curriculo/pt/n2.json`: `validar_plan.py pt` → 0 errores (225 avisos de vocabulario repetido, esperables en un nivel de reciclaje; C50 repite a propósito); `validar_plan_detallado.py pt curriculo/pt/n2.json` → 0 errores · 50 clases · 650 ejercicios · 631 consignas únicas · 650 ejemplos únicos. Los 50 ids están en estado `planificado` y los campos congelados coinciden con `tools/curriculo/pt/n2-outline.json`.

Revisión independiente de los lotes C01–C10 (ya aprobados) y C11–C50 (nuevos, muchos generados por script). Se aplicaron **118 correcciones puntuales** en los lotes de `tools/curriculo/pt/` y se consolidó el nivel.

## Cambios por tipo

### Canon y personajes (15)

- pt.n2.c13: se quitan los porteros inventados «dona Neide» y «seu Nelson». El único portero canónico (seu Pedro Barros) lo es del edificio de Dona Marina en Boa Viagem; Camila ya vive en Graças, así que el edificio nuevo usa roles sin nombre (la porteira de día, otro porteiro de noche). Además la situación daba la ayuda a dos personas distintas y el relacionar tenía respuesta ambigua: ahora cada objeto tiene un destinatario (chave → vizinha do 302, ajuda → porteira, recado → porteiro).
- pt.n2.c34: «o recepcionista era seu Jorge» → «o recepcionista era um senhor simpático» (el canon usa personajes de rol sin nombre).
- pt.n2.c41: seu Alberto era a la vez «vizinho do 302» y dueño del apartamento; ahora solo es el dueño (vive en Casa Forte, C11).
- pt.n2.c01, c04, c05, c07, c10: nombres canónicos con otro oficio o parentesco contradecían el MAPA y pasan a nombres secundarios. Ejemplos: «Marina chega ao escritório» → «Luana»; «o colega Bruno» (Bruno es el coordinador) → «Davi»; «Ana foi ao mercado com o irmão Pedro… banca da família» → «Luana… Rafael» (Ana es diseñadora; Pedro es el portero); «bairro de Helena» → «Valentina»; Ana en la papelería (C05) → «Luana».
- pt.n2.c32: «Nunca viajei para uma praia do Nordeste com amigos» contradecía Olinda en N1 → «Nunca fui a Porto de Galinhas».
- pt.n2.c46: «Em dezembro, Camila lembrou a viagem a Olinda» (N2 es 2027) → «Num domingo de 2027… de novembro do ano passado»; «em Miami morava perto do mar» → «perto dos pais» (canon: Kendall, cerca de sus padres).

### Pedagogía de registro: C25 «trocá-lo» (4)

- Antes: g1 e i2 presentaban «Vou trocá-lo hoje» como distractor frente a «Vou trocar ele hoje» (marcaba como incorrecta la forma estándar escrita del pt-BR).
- Ahora: la situación enseña el contraste de registro en un diálogo («Falando, a gente diz “trocar ele”; por escrito, aparece “trocá-lo”»). g1 pregunta por la forma escrita equivalente (A «Vou trocá-lo hoje» ✔, B «Vou trocar ela hoje», error de género). i2 pone en contraste el objeto nulo («Vou trocar amanhã») con «Vou trocar ela amanhã» (género); e0 sustituye «ajuda-me» con você por «Você ajuda eu com a troca?» (error real). Ninguna forma estándar queda marcada como incorrecta; la enclisis es solo reconocimiento (una sola pregunta), no producción.
- g0: «posso te ajudar, senhora» mezclaba te con senhora → «Oi, Camila! Eu posso te ajudar?» (vendedor y vendedora unificados).

### Distractores absurdos o agramaticales (39)

Muchos ítems de elegir de los lotes generados usaban un distractor sin sentido («ontem», «amanhã» pegado a cualquier frase) que no medía la clave. Ejemplos:

- c11 i2: «fica ontem no quarto» → «fica ao lado da varanda».
- c12 g1: «A máquina ontem apartamento?» → «O apartamento é máquina de lavar?» (contraste ter/ser).
- c13 i2: «Peço ajuda para ontem» → «Peço ajuda para ele» (género).
- c14 i2: «Preciso de um técnico ontem consertar» → «…técnico consertar o chuveiro» (falta para).
- c19 g1: «Ontem fará calor» → «Ontem fez calor».
- c20 g1: «Ontem às 18h terei consulta» (futuro simple no enseñado) → «Ontem às 18h tive consulta».
- c24 g1/i2/e0: «de sábado», «número mais fresco», «material maior» → «de tamanho G», «número menor», «tamanho menor».
- c38 g1/i2/e0: «Quantas dia vezes tomo?», «Qual é o consulta?» → «Quantos vezes…» y «Qual é o dose?» (errores reales de género y preposición).
- c39 g1/i2/s0: «Dói dormir bem», «Eu doer uma caminhada», «Deve dormir na praia» → consejos alternativos poco saludables o no pertinentes.
- c45: «Diz o número…» (forma de tu, mezcla de paradigmas) y «Fazer o cadastro ontem» → «Faça o número do documento», «Diga o cadastro».
- c46 g1/e0, c50 e0: «Ontem eu era a praça», «a mala é a rotina» → contrastes reales marco/evento/plan y pregunta/afirmación.

### Lengua, gramática y registro pt-BR (21)

- C37 (doer): «Me dói a garganta» es forma europea/literaria; el pt-BR natural es «Minha garganta dói» → se reescriben situación y ocho ítems (g1, g2, i1, i2, e0, e3, e4).
- Subjuntivo y pasiva analítica (reservados a N3) en situaciones: C45 «Pediu que ela fizesse o cadastro e dissesse o nome» → «Fazer o cadastro e dizer o nome»; C41 «Pediu que ele a ajudasse…» → «Ajuda para carregar uma caixa»; C47 «se ele quebrar» → «por outro modelo»; C48 y C50 «foi encontrada» → «agora está encontrada».
- C12 «amueblado» (palabra española en la situación; además lo bloquea el validador) → «mobiliado».
- C23 g0: «Esta mochila é ___ mais barato → o» (error de género) → «Este modelo é o mais barato»; «leu ela» → «leu Ana».
- C29 «tão doce que ninguém terminou» (estructura fuera de nivel) → «muito doce: ninguém terminou».
- C27: la situación decía «Por último» pero los ítems pedían «Finalmente» (el validador veta «finalmente» en la situación): s1 ahora pide la expresión del texto («Por último»).

### Ambigüedad, estímulo insuficiente y claves (26)

- Respuestas con dos verbos válidos en C26 (coloque/adicione/misture): ahora llevan la pista del infinitivo entre paréntesis; ítem e1 repetido con e3 reemplazado.
- C27 i0 (depois/então) y C24 i0 (algodão/tecido), C29 g0 (doce/macio), C36 i0 (febre/tosse): se añade el dato que decide la respuesta.
- C11: ítems sin apoyo en el texto (la puerta, «o segundo quarto fica perto do corredor», «na sala eu converso») → reescritos con datos de la situación.
- C23 e2: «caneca 90 g» sin referencia → datos de precio y peso en las pistas para que cada superlativo tenga una sola solución.
- C49 e2 y C50 e2: la clave declarada no correspondía al contenido (integrated-service-task / imperfecto-descriptive) → integrated-past-plan / integrated-a2-portfolio.

### Coherencia con la historia y hechos reales (11)

- C14–C15: la avería ocurre antes de que termine la mudanza → «na primeira semana no apartamento de Graças» y «uma semana depois da mudança».
- C40: Camila ya estaba recuperada en C39 → «em maio, voltou a sentir tosse e dor de cabeça»; «Clínica Graças» (nombre inventado) → «Clínica da Dra. Helena».
- C22: ropa de oficina «no Mercado de São José» → «numa loja do centro do Recife»; C28: mezcla para bolo de rolo en ese mercado → «mistura para bolo no supermercado».
- C41: «a mudança» (ya terminada en C15) → vuelven de comprar una mesa; C46: plan «comprar um bilhete para o encontro com Dona Marina» → «bilhete de ônibus para Olinda».
- C36, C38, C39: se eliminan las frases de metacomentario («Ela não tomou nenhuma decisão sobre remédio…», «Ela não deu conselho sobre doenças…») que no eran historia.
- C49: «Posso levar a bagagem perdida? Não, vou pedir ajuda.» (sin sentido) → «Na viagem anterior, minha bagagem estava perdida no aeroporto, mas agora está encontrada.»

## Límites aceptados

- El esqueleto de ejercicios es el mismo en las 50 clases (3 guiados + 3 independientes + 2 de situación + 5 de evaluación, un relacionar con pistas cruzadas por clase): es el formato aprobado en C01–C10 y lo exige el validador. Cada clase mantiene datos, escena y distractores propios.
- Las claves C28 (`se-impersonal`) y C18 (`future-simple-recognition`) siguen siendo reconocimiento; C25 solo reconoce `trocá-lo`; no hay producción de enclisis (reservada a N3).
- C35 usa «trem» y «estação de Recife» de forma genérica (sin nombrar líneas ni estaciones).
- C01–C10 mantienen sus ejemplos con nombres secundarios genéricos (Clara, Daniel, Marcos…); solo se tocaron los nombres que contradecían el MAPA.

## Hechos del reparto confirmados

- Camila cumple 28 años el 14 de marzo de 2027; sigue en Maré Digital (Porto Digital) y con la profesora Renata (Escola Capibaribe, Graças). Moneda: R$.
- B3: Camila y Ana alquilan un apartamento amueblado en Graças; dueño seu Alberto Tavares (o senhor), vive en Casa Forte y pasa cada semana. Sala con ventana a la calle, cocina tras el pasillo, baño junto al cuarto mayor, segundo cuarto pequeño y varanda; sofá, mesa pequeña, geladeira, fogão, armário grande en la cocina y máquina de lavar en el baño; el aluguel incluye los muebles.
- La mudanza desde Boa Viagem termina un sábado; en la primera semana: chuveiro roto, una hora sin luz y un vazamento (técnico enviado por seu Alberto). En el edificio de Graças hay porteira y porteiro sin nombre; la vecina del 302 guarda una llave. Seu Pedro Barros es solo el portero del edificio de Boa Viagem.
- Dra. Helena Rocha (a senhora), clínica cerca de Graças: cita martes 9h cambiada al jueves 10h (C17); en abril (temporada de lluvias) consulta por dolor de garganta, tos y fiebre el jueves 14h; farmacia en Graças (jarabe 3 veces al día, comprimido 1 vez después del almuerzo); en mayo nueva llamada por tos y dolor de cabeza (cita miércoles 10h). Sin diagnósticos.
- Compras: teléfono Sol R$ 1.600 / Lua R$ 1.250 (elige el Lua); camisas azul y blanca R$ 70 (talla M); lista lâmpada R$ 18, cadeira R$ 95, panela R$ 85, ventilador R$ 140; chaqueta de algodón G y zapato 38 en una tienda del centro del Recife; cambio del teléfono dos días después.
- Cocina con Dona Marina: arroz con tomate (sábado) y tapioca con queso (domingo); cena con Ana, Bia y Bruno en Boa Viagem; reserva el viernes para el sábado a las 20h a nombre de Camila Ortega.
- Viaje a Porto de Galinhas con Ana: hotel dos noches; recepcionista sin nombre; mala azul perdida y encontrada con una rueda dañada; tren de las 9h con 20 minutos de retraso (plataforma 2).
- Normas de Graças: no estacionar en la entrada, casco obligatorio en la garagem de motos, prohibido fumar en el elevador. Dona Lúcia (vecina mayor) y Caio (vecino joven) son secundarios sin canon.
- Trato: Camila con seu Alberto, dona Lúcia, la Dra. Helena y recepcionistas mayores: o senhor / a senhora; con Ana, Bruno, Bia, Lucas y Renata: você; Dona Marina le habla de você y Camila le habla de «a senhora».
- Recife: clima tropical cálido, lluvias fuertes de abril a agosto; el paseo a Olinda fue en noviembre de 2026 (salida a las 9, regreso a las 18h); en Miami (Kendall) Camila vivía cerca de sus padres.
- Hechos nuevos inventados por los autores que el revisor debe confirmar: precios y pesos de las compras, horarios de las citas, la clínica de la Dra. Helena «cerca de Graças», la farmacia en Graças, Caio y dona Lúcia como vecinos, y el hotel de Porto de Galinhas con recepcionista sin nombre.
