# Revisión del plan N8 (portugués de Brasil)

Veredicto: GO

Validadores sobre `curriculo/pt/n8.json`: `validar_plan.py pt` → 0 errores en N8; `validar_outline_nivel.py pt 8` → 0 errores · 45 claves nuevas (37 del MAPA + 8 de integración); `validar_plan_detallado.py pt curriculo/pt/n8.json` → 0 errores · 50 clases · 663 ejercicios · 662 consignas únicas · 663 ejemplos únicos. Los 50 ids están en estado `planificado`.

Revisión independiente de los 10 lotes (`tools/curriculo/pt/n8-lote-*.json`, copia previa en el scratch). Los lotes eran de buena calidad general (situaciones propias, sin ítems plantilla); se aplicaron unas **120 correcciones puntuales** (cifras aproximadas por tipo) y se consolidó el nivel.

## Cambios por tipo

### Canon y personajes (~29)

- **Edificio de Dona Marina (C37–C39).** El MAPA confirma que vive en un apartamento del séptimo piso en Boa Viagem, con portero (seu Pedro): síndico y ascensor son coherentes. Lo incoherente era que Camila firmara como vecina. Ahora Camila redacta **en nombre de Dona Marina**: carta del 12 de abril de 2033, seguimiento y cierre; la firma pasa de «Camila Ortega» a «Marina Lins» (SIT, g1, e3, i1 de C38 con «Dona Marina:»). Camila vive en Graças (N2–N6), de modo que no es residente de ese edificio.
- **Ana en Lisboa (N4 en adelante, colabora a distancia).** C07: Ana «chega ao escritório», «sem guarda-chuva», «café no teclado» eran escenas presenciales → «Luana» en g0, i1, e0 (la videollamada Ana–Bruno se mantiene, es consistente). C17/C18: «onde faz o mestrado», «para a faculdade», «trabalhar na tese» (cuatro años después de N4) → «onde mora», «para o centro», «num projeto». C32 i1: Ana entrando en una sala → Luana.
- **Nombres canónicos con otro oficio.** C16: oyente «Pedro» (seu Pedro es el portero) → «Rafael» en 6 lugares. C25: «parece o meu avô» → «parece a minha mãe» (Dona Marina ama los refranes).
- **Dona Marina/Camila en casa.** C21: «na cozinha, Dona Marina e Camila conversam» (Camila ya no vive allí) → «Camila visita Dona Marina»; C26: Tomás y Camila ven una película «na sala de Dona Marina» → «na sala do apartamento de Camila»; C31: «o quintal da minha avó, em Miami» → «em Medellín» (la abuela materna vive en Medellín; mangueiras → roseiras) y s1 B.
- **Infraestructura/entidades inventadas** (MAPA: no inventar): «Rádio Recife» → emisora sin nombre (C01); «app Recife Bus» → «um app de ônibus» (C09); «NetRecife» (C36 ×3, C40) → «a operadora»; «candidato Sérgio Mota» → candidato ficticio (C14); «Campanha do Porto Digital» → «Campanha de tecnologia» (C47); «orientador» → «professor do curso» (C42, Camila no tiene orientador).
- **Tomás.** Sus réplicas en español (voseo) dentro de situaciones en portugués (C22 ×2, C23 ×3, C26 ×2, C27, C28, C30 ×2) → portugués con «você»; el voseo queda solo en el reparto y en C19/C20 donde se cita su español («remera», «pileta»). C23: «chegou ontem a Recife… curso em Boa Viagem» (la Escola Capibaribe es de Graças; el MAPA no ubica este curso) → sin lugar.

### Distractores absurdos o agramaticales (11)

- C03 g1 «Onde fica a sala, né?» → «Quer dizer que todos passaram?» (lectura errónea de «quase todos»); C03 e0 «Eu me refiro aos exercícios…» → «A senhora refere aos exercícios…» (falta el se).
- C14 e0 «pretende à nostalgia o público» → «apela a nostalgia» (falta la crase); C14 i1 «despejou o projeto goela abaixo» → «empurrou… goela abaixo».
- C16 g1/s0 «mandioca-brava de Recife» → «macaxeira» (error real: usar el término nordestino en Río).
- C23 s0 «por favor» → «por exemplo»; C25 g0 B (exceso de gíria, pero coherente); C30 i0 «ser arrepender-se» → «ser muito engraçado, ou seja, causar riso»; C30 s0 «O preço do ingresso» → «O elenco do filme»; C40 e0 «pensa a cidade» → «para toda a cidade».

### Lengua, gramática y ejercicios de ordenar (~30)

- Ordenar con respuesta no gramatical o permutable: C13 g2 (reduzir/reutilizar/reciclar en cualquier orden y contradecía la situación) → «Primeiro reduzimos, depois reutilizamos, por fim reciclamos»; C15 g2 → «Bom sabor, bom aroma e bom preço» con el orden dado en la consigna; C16 g2 «macaxeira aipim mandioca mesmo o alimento» (sin sentido) → «Macaxeira, aipim e mandioca são o mesmo alimento»; C18 g2 «como estás tu a trabalhar que» → «Tu estás a trabalhar hoje»; C19 g2 (Tomás decía «aqui dizemos remera») → «Na Argentina dizemos remera em vez de camiseta»; C23 g2 → «Ficar sem graça, dito de outra forma, é ficar envergonhado»; C46 g2 y e2 (faltaban «vou» y «O»); C47 e2; C50 g2 (comas de «ou seja»).
- C15 i0 «o consumidor ___ o diferencial» → «___ do diferencial» (gostou de); C23 g0 «estar de pé atrás» → «estar com o pé atrás»; C12 e3 pistas ilegibles («lindíssimo no») → «bonitíssimo»; C12 i0 («rime con coração» con respuesta «coração») → «Do grão ao ___».
- Español dentro del insumo en portugués (consignas siguen en español, estímulos pasan a portugués): C38, C39, C40 ×2, C36, C42 ×2, C43 ×2, C45 ×2, C46 ×2, C47, C48 ×3, C49 ×2, C50 ×5, C31 «de noche», C33/C35 «Escena:», C27 «trabajo»; C48 SIT «auténtica» → «autêntica»; C50 SIT «cierre» → «encerramento»; C50 e0/e3 con opciones en español → portugués (antecedentes, descumprimento, pedido, prazo; «Cena, ___ e desfecho»).
- C07 «Touché» → «Justo»; C16 estereotipo fonético («o nordestino alonga as vogais») → ritmo y expresiones regionales; C23 «matar cobra e mostrar o pau» (doble sentido vulgar) → «abacaxi»; C24 «é como uma tempestade» presentado como metáfora → metáfora real; C41/C45 g0, i0 con «(indicar)» (también valía «sugerem»).

### Ambigüedad y estímulo insuficiente (~16)

- Respuesta abierta sin pista: C11 i0 («por ___ minutos» → «(5)»), C28 e1 («enredo» vs «trama» → «sinónimo de trama»), C34 g1/e1 («(suspirar)», «(conversar)»), C50 e1 («(delicado)»), C50 i1 (eslogan paralelo con modelo explícito), C15 e1 (cierre con «cheio… café»), C22 e1 (frase inventada «na maior» → «foi mal pelo atraso (sincero)»).
- C21 i0 (el refrán «de grão em grão» no expresa «corrige el mismo error») y i1 («espeto de pau» con grupo que ensaya poco) → situaciones donde el refrán sí encaja; C28 g2 (categorías «cifra del episodio/fecha» sin sentido) → dato objetivo / opinión sobre la historia / opinión sobre la velocidad; C39 e3 (4 pistas, 3 propuestas) → 4 y 4.

### Coherencia con la historia y hechos (~14)

- C38: «a pendência já dura dez dias» tras «oito dias depois» → «oito» (s0 incluido); C39: reparación el 20 de abril (mismo día del seguimiento) → 25 de abril.
- C43 e1: «se estabilizaram num patamar» con un solo dato → «ficaram num patamar»; C44 e3: «resultados = pico em abril» (dato de otro gráfico) → «uso mais intenso à noite», coherente con el esquema de e4 y C45.
- C47 SIT: conversación «gravada em Porto Alegre» donde el vendedor dice «no Recife se diz macaxeira» → conversación en una feira do Recife con turista gaúcha.
- C49: diálogo de cierre atribuía a Tomás la frase de Camila (s1) → Camila.
- C26 «o rosto da menina» (Central do Brasil: el protagonista es un niño, Josué) → «menino».
- Clave de integración (requisito de `validar_plan.py`): las clases quintas de B2–B9 (C10, C15, C20, C25, C30, C35, C40, C45) llevaban `introduce: []`; se añade una clave `*-transfer` por clase (`implicit-reading-transfer`, `persuasion-analysis-transfer`, `varieties-adaptation-transfer`, `idioms-register-transfer`, `cultural-review-transfer`, `memory-narrative-transfer`, `complaint-dossier-transfer`, `academic-presentation-transfer`) en el esqueleto `n8-outline.json`, en los lotes, en `n8.json` y en el MAPA (N8, bloque correspondiente), y el ítem integrador e4 de cada clase la evalúa.

### Se mantiene (consistente)

- Gráfico de visitas de Maré Digital (C43) y estudio de 40 participantes (C41/C44/C45): datos de ejercicio coherentes con una gerente de producto de una empresa de aplicaciones; quedan declarados como ficticios en `hechosDelReparto`.
- Fuentes «Nogueira (2020)» y «Pereira e Lopes (2018)» (C42, C49): ejemplos ficticios para practicar la fórmula de cita; no repiten nombres del reparto. Se declaran en `hechosDelReparto`.
- «Joana» (C16, C20): oyente anónima del Recife, no es canónica; **Tomás Aguirre** (C01–C50) es canónico (N8).
- Referencias reales: Ponte Buarque de Macedo, Ponte Maurício de Nassau, Rua da Aurora, Mercado de São José, Marco Zero, UFPE, Rossio/Sintra/Cascais; películas «Central do Brasil», «Bacurau», «Aquarius» (rodada en Recife), «Que Horas Ela Volta?».

## Hechos del reparto confirmados

- Camila Ortega cumple 34 el 14-03-2033; gerente de producto en Maré Digital; vive en Graças (apartamento de seu Alberto) y visita a Dona Marina en Boa Viagem.
- Tomás Aguirre (argentino, voseo en español), compañero del curso de preparación del Celpe-Bras; se tratan de você; la profesora del curso es «a professora» (a senhora).
- Ana Beltrão vive en Lisboa desde N4 y colabora a distancia; su pt-PT es solo de reconocimiento.
- Dona Marina (69), edificio con síndico y ascensor en Boa Viagem; Lucas (29, desarrollador, alfaia); Bia (33, Café da Bia); Bruno (45); Iara (a senhora).
- Cronología de B8: carta 12-04-2033, seguimiento 20-04, cierre 25-04.

## Hechos nuevos a confirmar

- Camila escribe en nombre de Dona Marina las cartas al síndico (C37–C39).
- Lucas trabaja como desarrollador en 2033 (N6 B5 lo da por empezado).
- El curso de preparación del Celpe-Bras no tiene sede ni profesora con nombre en el MAPA (se mantiene sin nombre).
- Tomás participa también en la presentación del curso de la UFPE de B9.
- Ejemplos ficticios del nivel (Entrega Já, Rota Certa, «Maré Mais Verde», Gráfica Boa Vista, Joana/Rafael/Luciana/Lia/Caio).
