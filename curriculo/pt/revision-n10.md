# Revisión del plan N10 (portugués de Brasil)

Veredicto: GO

Validadores sobre `curriculo/pt/n10.json`: `validar_plan.py pt` → 0 errores en N10 (los únicos errores que aparecen son de N9, de otro revisor; 142 avisos de vocabulario repetido en N10, esperables en un nivel C1 que reutiliza léxico); `validar_plan_detallado.py pt curriculo/pt/n10.json` → 0 errores · 50 clases · 670 ejercicios · 663 consignas únicas · 670 ejemplos únicos; `validar_outline_nivel.py pt 10` → 0 errores. Los 50 ids están en estado `planificado` y los campos congelados coinciden con `tools/curriculo/pt/n10-outline.json`.

Revisión independiente de los 10 lotes C01–C50. Se aplicaron **75 correcciones puntuales** (en `tools/curriculo/pt/n10-lote-*.json` y, para C01, también en el esqueleto) y se consolidó el nivel. Copia de los lotes originales en el scratchpad (`pt/r10/orig/`).

## Cambios por tipo

### Canon y personajes (8)

- pt.n10.c01 (esqueleto y lote): la tarea decía «el bar de la Praça de Boa Viagem» mientras que el sitio canónico de Lucas, Ana y Bia es el Café da Bia. Antes: «…Lucas y Ana en el bar de la Praça de Boa Viagem…» → después: «…en el Café da Bia, en la Praça de Boa Viagem…» (es y en). Como `tarea` es campo congelado, se corrigió en el outline y `validar_outline_nivel.py pt 10` sigue en 0 errores.
- pt.n10.c22 y c25: la fuente «Ana Duarte» chocaba con el nombre de Ana Beltrão (personaje canónico, diseñadora en Lisboa) y creaba confusión; pasa a «Marta Duarte».
- pt.n10.c13: la conferenciante decía «na Travessia a gente vai de piada em piada»; Travessia es el estudio de Camila, no el evento. Ahora «aqui no Porto Digital a gente vai de piada em piada».
- pt.n10.c33: «Cinema da Fundação» no está en la lista de lugares reales del MAPA; pasa a «Cinema São Luiz», que sí lo está.
- pt.n10.c37: «Seu vizinho do andar de cima, Heitor» se leía como el tratamiento «seu»; ahora «O vizinho do andar de cima, Heitor».
- pt.n10.c46: «Bar do Cuscuz» era un local inventado con nombre propio; ahora «uma lanchonete de Boa Viagem».
- pt.n10.c48: Diego mediaba con la gráfica sin que se supiera por qué; ahora «a gráfica contratada por Diego para os cartões e banners».

### Distractores absurdos o agramaticales (14)

Cada distractor pasa a ser un error plausible (registro, función del marcador, lógica del conector, falta de adaptación al interlocutor).

- c01: «Não vou nada.» → «Eu vou ao show no sábado, eu vou, sim, eu vou.» (redundancia frente a la elipsis); «Eu agradeço o seu agradecimento formal.» → «Não há de quê, fico à sua disposição.» (registro demasiado formal entre amigos).
- c02: «Aliás ao projeto, falta o teste.» (agramatical) → «Mudando de assunto, falta o teste do projeto.» (marcador equivocado); «Falando nisso, eu comprei pão.» (no sequitur) → «Falando nisso, a reunião de segunda mudou para as dez.» (conector sin enlace con lo dicho).
- c08: «Tudo, e a Camila apareceu antes.» → «E, por isso, a Camila apareceu antes.»; «Tudo ia bem, e depois, também.» → «Tudo ia bem, e depois tudo continuou bem.» (sin giro).
- c10: «A alfaia existe.» → «No fim, a alfaia foi guardada.» (cierre plano).
- c22: «o contexto pesa o contexto pesa.» → «O contexto pesa muito, e ponto.» (sin atribución).
- c26: «turistas em hotéis» → «grandes empresas com departamento de tradução próprio»; «escolas de natação» → «grandes multinacionais».
- c28: «Lançamos em setembro e o servidor.» (agramatical) → «Lançamos em setembro, contanto que o servidor falhe.» (conector con lógica invertida).
- c41: «Você tem documento com foto, a recepcionista.» → «Ela perguntou: o senhor tem documento com foto?» (no adapta el trato al interlocutor).
- c42: «O tabelião, você tem o documento original, ele quer.» → «O tabelião quer saber: o senhor tem o documento original?».
- c45: «O laudo é um registro no cartório para vender carros.» → «O laudo é o documento do cartório que autoriza outra pessoa a agir.» (confusión laudo/procuração).

### Lengua, gramática y registro pt-BR (24)

- c04: «preciso ajuda» → «preciso de ajuda» (ordenar y respuesta); resumen para Bruno reescrito con marcadores correctos.
- c07: «Não foi eu» → «Não fui eu».
- c08: «Para a surpresa, o presente era o meu» → «Para completar, o presente era o meu» (la fórmula no existía); «brindis» (castellano) → «brinde».
- c01: orden «Vou, sim, também» → «Vou também, sim».
- c12: «tremendo de bom» (no estándar, y tampoco claramente neutro) → «a melhor coisa do universo».
- c15: «Um brinde ao Lucas que sempre chega cedo… pra variar» era contradictorio; ahora «que chegou cedo ao ensaio, pra variar».
- c19: «dois minutos de tempo de fala» (redundante y en conflicto con los tres minutos de la situación) → «Cada pessoa tem três minutos; o ___ de fala é igual para todos».
- c20: «Elas propõem» (Bruno es hombre) → «Camila propõe»; «meio termo» → «meio-termo» (ortografía con guion), con su ejercicio de completar.
- c25: «uns quatrocentos palavras» → «umas quatrocentas palavras».
- c26: «mercado hispano-lusófono» (neologismo) → «nos mercados hispanofalante e lusófono».
- c28: «o apartado de contingências» (hispanismo) → «a seção de contingências»; «usamos o reserva» → «usamos o servidor reserva».
- c29: «falta mais número» → «faltam mais números» (situación y respuesta).
- c42: «A notaria enviou» → «O cartório enviou».
- c46: «Que papo reto!» (no encaja como reacción a la anécdota) → «Que ótima história!»; «lero-lero» (despectivo) → «bate-papo».
- c48: «reajuste de dez por cento» como rebaja → «desconto» (y su consigna).
- c49: «uma vista para o ___ do Capibaribe → rio» (no tenía sentido) → «uma vista para o ___ Capibaribe».
- c50: «Na prova de cierre C1» (castellano en texto pt) → «Na prova de encerramento do C1».

### Ambigüedad, estímulo insuficiente y claves (16)

- c03: tres completar de interjección con varias respuestas válidas (Uau/Nossa/Eita…) → se añade la pista de inicial («empieza con U/N»); además la consigna decía que hablaba Lucas cuando hablaba Ana.
- c13: la consigna del dicho «Quem não tem cão caça com gato» hablaba de lluvia; ahora habla de improvisar con un abanico cuando falla el ventilador.
- c21: consigna «qué parte falta: tese, desenvolvimento, conclusão» contradecía el esqueleto dado; se reformula. «Em seguida» y «Em conclusão» aceptaban sinónimos (depois, em suma): ahora el hueco es solo «seguida» y «conclusão».
- c22: «Completa la atribución» admitía Segundo/Conforme/De acordo com → se pide «la fórmula de tres palabras».
- c29: gancho con «lançar/criar/fazer» → pista de inicial («empieza con L»).
- c36: la consigna decía «fecha límite» y la respuesta era «retorno»; se reformula (término que nombra el plazo).
- c41: «perguntou/pergunta» ambiguo → se añade «agora há pouco».
- c43: «explicitar» (poco natural; «explicar» también encajaba) → respuesta «explicar» y consigna ajustada.
- c48: consigna de «prazo» («entrega futura») mal formulada.
- c50: «ele disse que não era isso que queria dizer» no dejaba claro quién era «ele» → «o fornecedor disse que não era isso que ele queria dizer sobre o orçamento».
- c08: la consigna de «Para completar» se ajusta a la nueva fórmula.

### Coherencia con la historia y hechos reales (13)

- c12: 36 graus en la varanda de Recife → 34 graus (más creíble para el clima de Recife).
- c20: Bruno defendía dos días de oficina y el «punto medio» era tres remotos y dos presenciales, o sea, su propia posición; ahora defiende cuatro días. El ejercicio de ordenar daba «dois remotos e três presenciais», contradiciendo la situación; corregido al 3 remoto + 2 presencial en situación, ordenar y resumen (4 correcciones).
- c22: «relatório da Travessia, 2034»: Travessia no existía en 2034 → «relatório da Maré Digital, 2034».
- c36: la situación hablaba de un «recado no mural» pero era un diálogo en vivo → «explica a avaria no hall do prédio».
- c40: gestiones de banco y cartório en un sábado (cerrados) → «sexta-feira» (situación y consigna del correo).
- c45: «Para vender o carro, você assina uma procuração» (no es exacto) → «Para que sua irmã resolva seus papéis em seu nome, você assina uma procuração», con su consigna.
- c49: «retrospectiva do primeiro ano» el día del lanzamiento (aún no hay primer año) → «o discurso e a rodada de conversa vão funcionar»; «no meu primeiro dia» → «na minha primeira semana» (coherente con C46 y C50).

## Límites aceptados

- El esqueleto de ejercicios es el mismo en las 50 clases (3 guiados + 3 independientes + 2 de situación + 5 de evaluación, más 1 extra de reciclaje en varias clases, un relacionar con pistas cruzadas por clase): es el formato exigido por el validador. Muchos ejercicios de las clases B1–B4 son breves y de tipo A2–B1 (completar una fórmula, elegir entre dos), con un distractor funcional (fórmula adecuada frente a una de registro o función equivocada). No se reescribieron en bloque: cumplen una sola respuesta correcta y un error real.
- Los datos numéricos de C26–C30 (créditos, reparto 60/40 → 50/50, 40 mil reais, estudio con «70 %» en C22) son ficticios, del mundo del ejercicio; no contradicen el MAPA.
- Diego habla español en las situaciones de B9 y C48 (canon: «habla español con Camila»); el validador acepta esos diálogos.
- El título de C14 («El mismo mensaje en cuatro tonos») anuncia cuatro tonos y el ejercicio trabaja formal, cercano, humorístico y neutro en distintas partidas; el título es campo congelado y no se tocó.
- C01–C05 usan el nombre de «Lucas» y «Ana» en la sobremesa de Dona Marina (dos personajes canónicos); en 2035 Ana está en Lisboa y aparece por videollamada o de visita (C15, C49), lo que se acepta.
- Las tareas tipo Celpe-Bras (insumo + propósito + interlocutor + producto) están presentes en C46–C50 y en las tareas de cada clase.

## Hechos del reparto confirmados

- Camila cumple 36 años el 14 de marzo de 2035. Deja Maré Digital a finales de marzo (Iara como mentora) y funda Travessia con Lucas; preparación de enero a agosto; lanzamiento el 5 de septiembre de 2035, nueve años después de su llegada. Moneda: R$.
- Ana colabora desde Lisboa; Bia sigue con el Café da Bia en la Praça de Boa Viagem; Bruno coordina producto en Maré Digital; Yasmin Farias se despide de Maré Digital (C15).
- Trato: você con Lucas, Ana, Bruno, Bia, Yasmin, Diego y Tomás; «a senhora» con Dona Marina, Iara y vecinas mayores; «o senhor» con seu Pedro y seu Paulo. Dona Marina tiene 71 años, seu Pedro 67 (portero en Boa Viagem), seu Paulo 73.
- B9: Camila interpreta entre Diego (cliente mexicano) y una clínica o un cartório (documentos: certidão, procuração, laudo) y media entre Diego y la gráfica del lanzamiento (C48: banners el día 20, cartões el día 3, 10 % de descuento).
- Hechos de Recife usados: Porto Digital, Cais do Sertão, Marco Zero, Capibaribe, Cinema São Luiz, la «Veneza brasileira», clima tropical cálido; bancos y cartórios en días laborables.
- Hechos nuevos inventados por los autores que el revisor debe confirmar: Dona Lúcia (vecina de 78 años, C43; ya aparece como vecina mayor en N2), Heitor (vecino, C37), Elaine (coordinadora del cineclube, C31), el cineclube de Boa Viagem, Fábio, Sônia, Gustavo y Wanda (críticos y socios del club), Rafael (colega de Maré Digital, C18), Wagner (colega, C38), el doctor Renan (médico, C44), dona Rita (vecina de seu Pedro, C07), Marta Duarte (autora de las fuentes, C22/C25), la gráfica contratada por Diego (C48) y la asociación de moradores con su salão y su mutirão (C39).
