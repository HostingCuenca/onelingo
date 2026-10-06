# Portugués de Brasil para hispanohablantes · mapa de N1–N10

Fuente única del **hilo de la historia** y del reparto para escribir las fichas `curriculo/pt/nX.json` y los bloques de la ruta (DEC-034, DEC-035). El marco común (`curriculo/marco.json`) fija temas, funciones, léxico y situaciones por bloque; las fichas de cada nivel fijan la gramática (`introduce`). Este mapa no introduce gramática: solo dice **quién, dónde y cuándo**.

## Reglas del idioma y del canon

- **Variedad:** portugués de Brasil (pt-BR) **neutro**, ortografía posterior al Acuerdo (ideia sin acento, sin trema en «frequente», «ótimo», «não»). No se adopta como modelo el acento carioca ni el paulistano; el regionalismo pernambucano (oxente, visse, mainha, arretado, massa) aparece solo como nota cultural o en un diálogo con glosa, nunca como respuesta exigida. El portugués europeo solo se reconoce cuando el plan lo prevé (PLAN_PORTUGUES.md).
- **Tratamiento:** `você` es la forma por defecto entre desconocidos, compañeros y amigos; `a gente` en habla informal; `o senhor / a senhora` con mayores y en trámites. `tu` solo receptivo/regional.
- **Apoyo bilingüe `{"es": …, "en": …}`:** consignas, explicaciones, pistas y feedback; español latinoamericano e inglés americano. En las explicaciones, comparar con el español cuando ayude y **avisar de los falsos amigos** cuando aparezcan (ver ENCARGO_RUTA_PT.md).
- **Prohibido mencionar el país andino y las ciudades que el cliente descartó** (lista exacta en `docs/claude-educacion/ENCARGO_RUTA_PT.md`) en ningún texto de pt. La app apunta a EE. UU. y a toda Latinoamérica; otras nacionalidades en ejercicios (colombiana, mexicana, argentina, peruana, chilena, paraguaya…) están permitidas.
- **Solo hechos reales de Recife y Pernambuco.** Se pueden usar: Recife es la capital de Pernambuco, en el Nordeste, con clima tropical cálido todo el año (la temporada de lluvias fuerte va de abril a agosto); el río **Capibaribe** (y el Beberibe) y sus puentes; el barrio **Recife Antigo** con el **Marco Zero**, el **Porto Digital** (polo de tecnología e innovación), el **Paço do Frevo** y el **Cais do Sertão**; la **Rua do Bom Jesus** y la sinagoga **Kahal Zur Israel**; el **Mercado de São José**; **Boa Viagem** (playa y avenida de la playa; en marea baja se forman piscinas naturales; hay avisos de tiburones en la playa); **Graças** (barrio central junto al Capibaribe); **Olinda**, vecina de Recife y Patrimonio Mundial; el **metrô do Recife**, los ônibus y los carros de aplicativo; el **aeropuerto** internacional (código REC); **Fernando de Noronha**, **Porto de Galinhas** y **Caruaru** como viajes; el **frevo** (Patrimonio Inmaterial de la Humanidad desde 2012) y el **maracatu**; el **Carnaval** (el **Galo da Madrugada** abre el sábado de Carnaval); las fiestas de **São João** (junio); comida: **tapioca, cuscuz, bolo de rolo, pão de queijo, carne de sol, macaxeira, caldinho, cartola, água de coco, suco**; la **UFPE** (Universidade Federal de Pernambuco); el **Cinema São Luiz**. Escritores pernambucanos: Manuel Bandeira, João Cabral de Melo Neto y Clarice Lispector (criada en Recife).
- **No inventar infraestructura.** No se nombran líneas ni estaciones del metro, hospitales, bancos concretos, calles o cuentas de personas reales que no estén en esta lista. Los lugares ficticios del reparto son solo los de la tabla de abajo (empresa, escuela, cafetería, edificio).
- **Moneda y medidas:** el **real** (R$, reais e centavos); se compra en quilos y gramas. Zona horaria de Recife: UTC−3 todo el año (Brasil no usa horario de verano); **Fernando de Noronha** va en UTC−2, una hora por delante de Recife. Miami va 1 hora por detrás hasta el 1 de noviembre de 2026 y 2 horas después (en 2027 vuelve a 1 hora desde el 14 de marzo).
- **Claves:** las de Fundamentos (`previos`) son las de `pt.f0`; las nuevas se introducen una sola vez en su ficha. Lo ya visto va a `recicla`.
- **Los nombres de los ejemplos en las fichas son orientativos.** Si una ficha le da a un nombre canónico un origen, oficio o relación que contradice este mapa, el mapa manda: cambia el nombre por uno secundario (Luana, Valentina, Rafael, Paulo, Carolina…).

## Reparto canónico

| Personaje | Quién es | Trato |
|---|---|---|
| **Camila Ortega** | Protagonista. Estadounidense de **Miami**, 27 años en N1 (nació el 14 de marzo de 1999). Hija de colombianos de Medellín: en casa se habla español (su lengua materna) e inglés. Diseñadora de producto (UX). Se muda a **Recife** en septiembre de 2026 para trabajar en **Maré Digital** y aprende portugués con la profesora Renata. | você con jóvenes y colegas; a senhora / o senhor con mayores |
| **Dona Marina Lins** | 62, recifense, viuda, profesora de Historia jubilada. Alquila una habitación a Camila en su apartamento de **Boa Viagem**. Le gusta contar la historia de la ciudad. | Camila: «a senhora» / «Dona Marina»; ella: você |
| **Lucas Lins** | 22, hijo de Dona Marina, estudia Ciencias de la Computación en la **UFPE** y toca la alfaia en un grupo de maracatu. | você |
| **Ana Beltrão** | 29, recifense, diseñadora, compañera de Camila en Maré Digital y su mejor amiga. | você / a gente |
| **Bruno Cavalcanti** | 38, recifense, coordinador del equipo de producto y jefe directo de Camila. | você |
| **Bia Santos** | 26, dueña de una pequeña cafetería en la Praça de Boa Viagem («Café da Bia»); amiga de Ana. | você |
| **Seu Pedro Barros** | 58, portero del edificio de Dona Marina. | Camila: «o senhor» / «seu Pedro»; él: você |
| **Seu Paulo Gomes** | 64, feriante (frutas y verduras) en la feria del barrio. | o senhor |
| **Professora Renata Souza** | 40, profesora de portugués de Camila en la Escola Capibaribe de Português (Graças). | Camila: «a senhora» al principio; desde N1 B6 você (ella se lo pide) |
| **Frevo** | el gato de Dona Marina, 3 años. | — |

**Familia de Camila (en Miami, barrio de Kendall):** su madre **Gloria** (55), su padre **Jaime** (58) y su hermana **Valeria** (22). Videollamadas los domingos; tiene su abuela materna en Medellín.

**Lugares fijos (ficticios):** Maré Digital, empresa de software que hace aplicaciones para público hispanohablante de EE. UU. y Latinoamérica, con oficina en el **Porto Digital** (Recife Antigo); por eso contrató a una diseñadora nativa de español. Escola Capibaribe de Português, en Graças: clases martes y jueves a las 19:00, aula 3, grupo de 10 alumnos (nivel 1: 30 en total). Café da Bia, en la Praça de Boa Viagem. El edificio de Dona Marina: séptimo piso, a dos cuadras de la avenida de la playa.

Personajes de rol sin nombre: «Garçom», «Garçonete», «Vendedora», «Recepcionista», «Motorista», «Médica», «Policial»… (en portugués: se muestran igual con la interfaz en español o inglés).

**Nuevos por nivel (los fija este mapa):** N2 · **Seu Alberto Tavares** (dueño del apartamento de Camila y Ana en Graças, o senhor), **Dra. Helena Rocha** (médica, a senhora). N4 · **Iara Menezes** (fundadora y directora de Maré Digital, a senhora). N6 · **Diego Salazar** (cliente mexicano de Maré Digital, você, habla español con Camila) y **Yasmin Farias** (desarrolladora nueva del equipo). N8 · **Tomás Aguirre** (argentino, compañero del curso de preparación del Celpe-Bras, voseo). Ningún personaje nuevo repite nombre ni apellido del reparto (Ortega, Lins, Beltrão, Cavalcanti, Santos, Barros, Gomes, Souza, Tavares, Rocha, Menezes, Salazar, Farias, Aguirre).

## Cronología

- **N1** (sept.–dic. 2026): los primeros meses de Camila en Recife, en casa de Dona Marina.
- **N2** (2027): su primer Carnaval; en B3 Camila y Ana alquilan un apartamento en Graças.
- **N3** (2028): Camila es líder de producto; sus padres la visitan (B3); viaje a Fernando de Noronha (B5).
- **N4** (2029): Camila postula a gerente de producto con Iara (B5); Ana se va a Lisboa a hacer una maestría (B6; desde ahí trae notas de Portugal, solo de reconocimiento).
- **N5–N7** (2030–2032): Camila es gerente de producto; regulariza su residencia (N5 B1); lidera un proyecto de visitas guiadas (N5 B9); en N7 B8 visita a Ana en Lisboa.
- **N8** (2033): Camila se prepara para el Celpe-Bras.
- **N9** (2034): Camila es directora de producto en Maré Digital.
- **N10** (2035): Camila y Lucas fundan **Travessia**, un pequeño estudio de producto digital y localización español–portugués. Camila deja Maré Digital a finales de marzo (Iara queda como mentora); Travessia se prepara de enero a agosto y se lanza oficialmente el 5 de septiembre de 2035, nueve años después de su llegada. Ana colabora desde Lisboa.

## Calendario fijo de N1 (2026; no se contradice)

- **Sábado 5 de septiembre:** Camila llega al aeropuerto de Recife y Dona Marina la recibe. **Lunes 7 de septiembre:** feriado (Independência do Brasil). **Martes 8 de septiembre:** primer día en Maré Digital. Primera clase con Renata: jueves 10 de septiembre.
- **Rutina:** Camila se levanta a las 6:30, entra a trabajar a las 9, almuerza a las 12:30 y sale a las 18; va al trabajo en ônibus o en carro de aplicativo y a la escuela en carro de aplicativo (martes y jueves).
- **Lunes 12 de octubre:** feriado (Nossa Senhora Aparecida). **Lunes 2 de noviembre:** Finados. **Domingo 15 de noviembre:** Proclamação da República. **Viernes 20 de noviembre:** Consciência Negra. **Viernes 25 de diciembre:** Navidad.
- **Martes 3 de noviembre:** Camila planea el paseo a **Olinda**. **Sábado 14 de noviembre:** sale a las 9 con Ana, Bia y Lucas en carro de aplicativo, camina por las ladeiras, almuerza y vuelve a las 6 de la tarde. **Domingo 15:** almuerzo en casa de Dona Marina y feria con seu Paulo.
- **Diciembre de 2026:** Camila lleva casi cuatro meses en Recife y vive en casa de Dona Marina desde septiembre; su última clase del nivel es con la profesora Renata. El Carnaval de 2027 va del sábado 6 al martes 9 de febrero (el Galo da Madrugada, el sábado 6); el miércoles 10 es Quarta-feira de Cinzas.
- **Descripciones fijas:** Dona Marina es baja, de pelo corto y gris, muy simpática; Lucas, alto, de pelo negro y rizado, con lentes y camiseta azul; Ana, alta, inteligente y divertida; Bruno, alto y serio, con barba corta; Bia, baja, con el pelo largo y castaño y siempre sonriente; seu Pedro, bajo y calvo; Camila, de estatura media, pelo largo y castaño oscuro.
- **Precios de referencia:** un suco R$ 6 (dos, R$ 12), una botella de agua R$ 3, un pão de queijo R$ 4. Si una ficha trae otro precio concreto, manda la ficha.

---

## N1 · A1 · referencia Celpe-Bras (sin nivel A1)

Historia: Camila llega a Recife, vive en casa de Dona Marina en Boa Viagem, empieza en Maré Digital y estudia portugués con Renata. Entiende muchas palabras por el español, pero los falsos amigos y los sonidos nuevos la sorprenden. Conoce el barrio, la cafetería de Bia, la feria, el transporte y su primer paseo (Olinda). Cada clase de N1 abre con un **sonido del día** (`sonido` de la ficha).

- **B1 Saludar y presentarse** — llegada al aeropuerto, a casa de Dona Marina y a Maré Digital (Bruno y Ana).
  - `chamar-se`: eu me chamo; como você se chama?
  - `introduce-third-person`: este é/esta é + nome; ele/ela se chama
  - `social-register-formulas`: prazer em conhecer; tudo bem?; como vai?; fórmulas con você y o senhor/a senhora
  - `social-question-pattern`: como/ de onde/ qual + pregunta sin inversión
  - `nationalities-expanded`: brasileiro/brasileira y nuevo repertorio nacional; concordancia de nacionalidad
- **B2 Hablar de mí** — Camila habla de su trabajo, sus idiomas (espanhol, inglês, um pouco de português) y lo que le gusta.
  - `present-regular-ar`: falar, morar, trabalhar: eu/você/ele en presente
  - `present-regular-er`: comer, beber, vender: eu/você/ele en presente
  - `present-regular-ir`: abrir, partir, decidir: presente regular -ir
  - `gostar-de`: gostar de + nombre/infinitivo; um pouco/muito
  - `regular-present-transfer`: presente regular para morar, trabalhar y falar
- **B3 Personas y cosas** — la familia Lins, la familia de Camila (Miami), su cuarto; el gato Frevo.
  - `plural-nouns-articles`: os/as/uns/umas + nombre plural
  - `adj-agreement-plural`: adjetivo plural masculino/femenino concordado
  - `ter-present`: ter: tenho/tem + posesión
  - `age-ter`: tenho/tem + número + anos
  - `possessives-basic`: meu/minha, seu/sua, nosso/nossa
- **B4 Preguntar y negar** — inscripción en la Escola Capibaribe y línea de teléfono; pedir que repitan.
  - `wh-expanded`: quando, qual/quais, quanto(s)
  - `negation-extended`: não + verbo; nunca/nada; não tenho nada
  - `numbers-21-100`: cardinales 21–100; e entre decenas
  - `contact-spelling`: arroba, ponto; confirmar deletreo
  - `confirmation-repair`: é isso?; não, é…; pode repetir?
- **B5 Café y compras** — Café da Bia, la feria de seu Paulo, una camiseta en el shopping.
  - `queria-polite-request`: Queria + sustantivo como fórmula cortés
  - `gostaria-de`: Gostaria de + sustantivo; contraste de registro
  - `prices-reais`: quanto custa?; reais y centavos; cardinales hasta mil
  - `order-quantity-choice`: um/uma + prenda; talla y color
  - `demonstratives-basic`: este/esta, esse/essa, aquele/aquela
- **B6 Gustos y rutina** — la rutina de Camila y la de la familia Lins; martes y jueves de clase; desde aquí Renata y Camila se tutean.
  - `time-basic`: Que horas são?; é uma; são duas; às
  - `days-time-preps`: em/na + día; días de la semana
  - `reflexives-routine`: eu me levanto/me visto/me deito
  - `frequency-basic`: sempre, geralmente, às vezes, nunca
  - `routine-preferences`: gostar de + infinitivo; a gente + verbo
- **B7 Describir y ubicarse** — describir a la gente; Boa Viagem, la Praça y el Recife Antigo (Marco Zero, Rua do Bom Jesus).
  - `ficar-location-state`: ficar + lugar/estado; onde fica?
  - `morar-vir-present`: moro em; venho de; você vem de
  - `prep-contractions-expanded`: no/na, do/da, para o/a; pra receptivo
  - `existential-tem-ha`: tem conversacional / há formal para existencia
  - `location-description-transfer`: ser/estar/ficar + lugar y adjetivo
- **B8 Verbos frecuentes y comida** — la feria con Dona Marina y seu Paulo; tapioca, cuscuz, carne de sol.
  - `querer-present`: quero/quer + infinitivo o sustantivo
  - `poder-present`: posso/pode + infinitivo
  - `dever-present`: devo/deve + infinitivo de obligación
  - `quantity-muito-pouco`: muito/pouco + alimento; unidade + de
  - `shopping-modal-transfer`: querer + poder + dever en compra
- **B9 Moverse y planes** — ônibus, metrô y carro de aplicativo; planes con Ana, Bia y Lucas.
  - `imperative-directions-basic`: siga/vire/espere como fórmulas de indicación; no paradigma ni negativo
  - `transportes`: ir de ônibus/metrô/trem; destino
  - `ir-infinitivo`: vou/vamos + infinitivo
  - `invitation-politeness`: vamos?; pode ser; infelizmente não
  - `dates-calendar`: no dia + número; em + mês
- **B10 Mi fin de semana y cierre** — el sábado en Olinda; repaso y prueba del nivel.
  - `perfeito-regular-ar`: pretérito perfeito regular -ar: falei/trabalhei/viajei
  - `perfeito-regular-er-ir`: pretérito perfeito regular -er/-ir: comi/bebi/parti
  - `perfeito-irregular-core`: fui/foi, tive, fiz, vim en eventos terminados
  - `desde-faz`: desde + época; faz + período que + presente; há temporal y perfeito composto solo reconocimiento

## N2 · A2 (2027)

Historia: segundo año. Camila hace más cosas en el trabajo; vive su primer Carnaval; se muda con Ana a Graças; viaja por Pernambuco; se enferma; aprende a cocinar con Dona Marina.

- **B1 Rutinas, trabajo y estudio** — la jornada en Maré Digital (Bruno, Ana).
  - `present-irregular`: Expansión productiva del presente irregular con fazer y dizer; ser, ter, vir e ir quedan como transferencia desde N1.
  - `estar-gerundio`: estar + gerúndio
  - `costumar-present`: costumar + infinitivo
  - `adverbs-frequency-expanded`: quase sempre, raramente, normalmente
  - `routine-work-transfer`: horarios y frecuencia en presente
- **B2 Contar experiencias pasadas** — la infancia de Camila en Miami, su universidad, su abuela de Medellín.
  - `preterite-regular-ar`: Pretérito perfeito regular en -ar con expansión productiva de eu, você, ele y ela.
  - `preterite-regular-er`: Pretérito perfeito regular en -er con expansión productiva de eu, você, ele y ela.
  - `preterite-regular-ir`: Pretérito perfeito regular en -ir con expansión productiva de eu, você, ele y ela.
  - `preterite-irregular-frequent`: Núcleo irregular ampliado del pretérito perfeito: disse, pôs, veio, quis y pôde.
  - `imperfecto-descriptive`: imperfeito de ser/estar/morar
- **B3 Casa, barrio y servicios** — Camila y Ana alquilan un apartamento en Graças (dueño: seu Alberto).
  - `parts-home`: partes de la casa
  - `furniture-appliances`: muebles y electrodomésticos
  - `object-indirect-basic`: dar algo para ele/ela y pedir algo para ele/ela; sin introducir lhe
  - `household-repair`: estar com problema, ficar sem y quebrado para problema y consecuencia
  - `past-participle-state`: estar + particípio de estado
- **B4 Planes, citas y predicciones** — la agenda, el clima de Recife (calor y lluvia fuerte) y los planes para el Carnaval y São João.
  - `future-ir-expanded`: ir + infinitivo
  - `appointment-change`: poder + remarcar / confirmar
  - `future-simple-recognition`: será/haverá de reconocimiento
  - `future-simple-weather`: futuro simple climático productivo: choverá, fará, será
  - `appointment-calendar-transfer`: citas, fechas y planes
- **B5 Comparar y elegir productos** — compras para el apartamento; mercado de São José.
  - `comparatives-basic`: mais/menos … que
  - `equality-comparison`: tão … quanto
  - `superlatives-basic`: o/a mais + adjetivo
  - `size-materials`: talla, material y adjetivo
  - `object-pronouns-returns`: me/te como proclíticos en me ajuda/te mostro; ele/ela como objeto tónico coloquial en vou trocar ele/ela; objeto nulo cuando el referente es
- **B6 Restaurante y cocina** — bolo de rolo y tapioca con Dona Marina; restaurante con los amigos.
  - `imperative-affirmative`: imperativo afirmativo frecuente
  - `recipe-sequence`: primeiro/depois/finalmente
  - `se-impersonal`: se en instrucciones impersonales: reconocimiento limitado de mistura-se, aquece-se y serve-se, sin enseñar pasiva ni concordancia
  - `flavors-textures`: sabores y texturas
  - `restaurant-reservation-transfer`: reserva y pedido en presente
- **B7 Viajes y transporte** — viaje a Porto de Galinhas; el aeropuerto y los ônibus de larga distancia.
  - `travel-participles`: perdido/encontrado/danificado para estados del equipaje
  - `ja-ainda-nunca`: já/ainda/nunca + perfeito
  - `por-para-expanded`: por/para en contexto
  - `hotel-checkin`: registro y petición en hotel
  - `travel-notices`: avisos y participios
- **B8 Salud y bienestar** — Camila se enferma; consulta con la Dra. Helena.
  - `symptoms-basic`: síntomas y cuerpo
  - `doer-present`: doer en presente
  - `pharmacy-requests`: pedir remédio y receta
  - `health-habits`: frecuencia y consejo básico con deve y é bom, sin diagnóstico
  - `symptom-duration`: há/faz + duración; desde + momento de inicio
- **B9 Favores, permisos y normas** — normas del condominio y favores entre vecinos.
  - `favor-request`: pode me + infinitivo
  - `offer-help`: posso + infinitivo
  - `permission-expanded`: posso/pode + infinitivo
  - `prohibition-signs`: não pode / é obrigatório
  - `imperative-service`: imperativos irregulares de servicio: faça, diga, venha; uso afirmativo
- **B10 Repaso y proyecto del nivel** — Camila prepara una visita guiada para sus padres.
  - `integrated-past-plan`: contraste inicial: imperfeito para marco o hábito, perfeito para evento cerrado y vou + infinitivo para plan
  - `integrated-service-task`: integración de peticiones, permiso y normas
  - `integrated-a2-portfolio`: integración de rutinas, vivienda, viajes y salud

## N3 · B1 entrada (2028)

Historia: Camila es líder de producto; sus padres visitan Recife; viaje a Fernando de Noronha con incidencias; el cine y la música de Pernambuco.

- **B1 Novedades, cambios y logros** — el ascenso a líder de producto.
  - `subjuntivo-presente-formas`: presente do subjuntivo regular (fale, coma, abra) a partir de la forma eu del presente
  - `subjuntivo-presente-irregular`: tenha, faça, vá, seja, esteja, saiba, possa
  - `reaction-que-bom-que`: Que bom que… / Que pena que… + subjuntivo
  - `wishes-que-subjunctive`: Que você tenha sorte!; Tomara que dê certo
  - `news-sharing-markers`: sabia que…?; olha só; pois é; contei que…
- **B2 Incidentes y anécdotas** — un celular olvidado en un ônibus; un día de lluvia.
  - `imperfeito-formas`: imperfeito completo regular e irregular (era, tinha, vinha, punha) para escena y hábito
  - `perfeito-vs-imperfeito`: contraste completo: evento cerrado frente a contexto
  - `estava-gerundio-quando`: estava esperando quando…
  - `impersonal-third-plural`: roubaram meu celular; me ligaram
  - `report-loss-formulas`: perdi/esqueci/deixei; fazer um boletim de ocorrência; achados e perdidos
- **B3 Historias de familia** — Gloria y Jaime visitan Recife; historias de Medellín y de Dona Marina.
  - `relative-que-onde`: o que, a que, onde para personas, cosas y lugares
  - `relative-quem`: quem + preposición para personas (com quem, para quem, a quem)
  - `verbs-of-change`: ficar, virar, tornar-se, passar a + estado
  - `feelings-subjunctive`: fico feliz que…, tenho medo de que… + subjuntivo
  - `family-relationships-expressions`: dar-se bem com, parecer-se com, sentir saudade de
- **B4 Planes con condiciones** — decisiones sobre el trabajo y el viaje.
  - `se-present-future`: se chover, vamos ficar em casa
  - `future-subjunctive-forms`: formas regulares e irregulares (quando eu for, se você puder)
  - `quando-future-subjunctive`: quando/assim que + futuro do subjuntivo para eventos futuros
  - `condition-connectors`: desde que, a não ser que, senão
  - `imperative-negative`: não faça, não venha; formas de você
- **B5 Viajes e incidencias** — Fernando de Noronha: vuelo retrasado y reserva.
  - `futuro-do-preterito-forms`: faria, poderia, gostaria, seria
  - `polite-conditional-requests`: poderia + infinitivo; seria possível…?
  - `object-pronouns-periphrasis`: vou te mandar, pode me ajudar, quero lhe pedir
  - `travel-complaint-formulas`: gostaria de reclamar; infelizmente; o voo atrasou
  - `solution-requests`: poderiam resolver isso?; preciso de uma alternativa; remarcação, reembolso
- **B6 Salud, hábitos y consejos** — hábitos de vida y consejos de la Dra. Helena.
  - `advice-subjunctive`: é importante que…, recomendo que…, sugiro que… + subjuntivo
  - `purpose-para-que`: para que + subjuntivo; para + infinitivo
  - `aspectual-periphrases`: acabar de, voltar a, deixar de, continuar a, começar a + infinitivo
  - `advice-se-eu-fosse-voce`: se eu fosse você, eu… (fórmula de consejo)
  - `quando-enquanto-temporal`: quando/enquanto + perfeito/imperfeito
- **B7 Explicar cómo funciona algo** — Camila explica el producto a un cliente.
  - `serve-para-definition`: é um/uma … que serve para…
  - `relative-with-preposition`: em que, com que, de que, para o qual
  - `infinitivo-pessoal-initial`: para nós fazermos; antes de eles chegarem
  - `breakdown-description`: parou de funcionar; não liga; está dando erro
  - `quote-request`: quanto fica?; pode me passar um orçamento?
- **B8 Transmitir mensajes** — recados entre Bruno, Ana y clientes.
  - `reported-statement`: disse que + tiempo ajustado (ia, estava, tinha)
  - `reported-question-se`: perguntou se / onde / quando
  - `reported-request-pedir-para`: pediu para eu + infinitivo
  - `message-formulas`: pode avisar que…; deixa recado; fala pra ele que…
  - `clarification-formulas`: como assim?; quer dizer que…?; pode repetir o nome?
- **B9 Medios, cine y música** — cine pernambucano (Cinema São Luiz) y frevo.
  - `opinion-indicative-subjunctive`: acho que + indicativo; não acho que / duvido que + subjuntivo
  - `evidence-segundo-parece-que`: segundo…; parece que…; de acordo com
  - `vale-a-pena`: vale a pena + infinitivo; recomendar una obra
  - `news-summary-structure`: quem, o quê, quando, onde en un resumen oral breve
  - `passive-recognition`: é feito, foi instalado; ser + particípio
- **B10 Repaso y proyecto del nivel** — una reseña de una película o canción.
  - `cause-connectors`: porque, como, já que, por causa de
  - `consequence-connectors`: por isso, então, assim
  - `review-writing-structure`: estructura de reseña: presentación, opinión, argumento y recomendación

## N4 · B1 (2029)

Historia: Camila postula a gerente de producto (B5, Iara Menezes); Ana se va a Lisboa (B6) y en las videollamadas trae el portugués de Portugal solo como reconocimiento; Camila renegocia el apartamento (B3); fiestas de São João y medio ambiente (B9).

- **B1 Recuerdos y experiencias de vida** — Camila repasa sus primeros años en Recife.
  - `perfeito-composto-tenho-feito`: tenho + particípio para repetición continuada; contraste con el perfecto español
  - `participles-irregular`: feito, dito, visto, escrito, posto, aberto; ganho/pago
  - `mais-que-perfeito-composto`: tinha + particípio para lo anterior a otro pasado
  - `habitual-past-expressions`: antigamente, naquela época, costumava, quando eu era
  - `chronology-markers`: antes de, depois de, até então, desde que
- **B2 Deseos, lamentos y deducciones** — la despedida de Ana.
  - `devia-ter-regret`: devia/deveria ter + particípio; podia ter
  - `tomara-que-wishes`: tomara que + subjuntivo; eu queria que (receptivo)
  - `deve-ser-deduction`: deve ser, deve ter + particípio
  - `talvez-subjunctive`: talvez + subjuntivo; será que
  - `certainty-degrees`: com certeza, provavelmente, acho que, não tenho certeza
- **B3 Vivienda y convivencia** — Graças, vecinos y el síndico del edificio.
  - `relative-subjunctive`: procuro um apartamento que tenha…
  - `reciprocal-se`: eles se respeitam; um ao outro; uns aos outros
  - `repair-request-subjunctive`: peço que o senhor conserte; pedir que + subjuntivo
  - `lease-terms-formulas`: cláusula, caução, prazo, reajuste, rescisão
  - `task-delegation`: quem fica com…?; fico responsável por…
- **B4 Servicios, bancos y reclamaciones** — una reclamación a una empresa de internet.
  - `formal-email-structure`: Prezado/a…, venho por meio deste, atenciosamente
  - `formal-conditional-requests`: gostaria de solicitar; poderia informar; agradeço desde já
  - `deadlines-prazos`: no prazo de, até o dia, em até X dias úteis
  - `numbers-decimals-percentages`: vírgula decimal, R$ 1.250,00, 3,5 %
  - `written-complaint-structure`: hecho, petición, plazo y número de protocolo
- **B5 Buscar trabajo** — la entrevista con Iara para el nuevo puesto.
  - `professional-experience-narrative`: trabalhei como…, há X anos, estou há X anos em
  - `verbs-with-preposition`: depender de, contar com, participar de, responsável por
  - `word-derivation`: -dor, -mento, -ção, -eiro; in-/des-
  - `interview-answer-formulas`: no meu último emprego…; tenho experiência em…
  - `work-conditions-questions`: salário, benefícios, carga horária, regime de trabalho
- **B6 Tono formal e informal** — correos a Iara y mensajes a Ana en Lisboa.
  - `register-formal-informal`: você, o senhor/a senhora, Prezado; oi/tchau frente a cumprimentos formais
  - `hedging-softeners`: acho que, talvez, só queria confirmar, será que
  - `titles-address-forms`: Doutor/a, Professor/a, seu/dona, primeiro nombre en el trabajo
  - `agreement-disagreement-polite`: concordo; em parte; entendo, mas…
  - `spoken-written-contrast`: pra/para, tá/está, a gente/nós, tô/estou
- **B7 Deporte, ocio y personalidad** — correr junto al Capibaribe; el maracatu de Lucas.
  - `ser-estar-ficar-adjectives`: ser chato/estar chato; ficar nervoso
  - `indefinite-pronouns`: alguém, ninguém, algum/nenhum, qualquer, todo, cada, outro
  - `gerund-manner`: falando alto; aprendi ouvindo música
  - `activity-verbs-jogar-praticar-fazer`: jogar futebol, praticar esporte, fazer ioga
  - `encouragement-formulas`: parabéns; boa sorte; força!; bora
- **B8 Viajar por tu cuenta** — el Agreste (Caruaru) y el sertão.
  - `caso-subjunctive`: caso chova, caso precise
  - `apesar-de-concession`: apesar de + sustantivo/infinitivo; apesar de que
  - `precaution-expressions`: por via das dúvidas; só por precaução; para o caso de
  - `negative-imperative-subjunctive`: Imperativo negativo con subjuntivo: não deixe de…, não se esqueça de…, não esqueça; avisos
  - `rules-impersonal-subjunctive`: é necessário que…; é proibido; é permitido
- **B9 Tradiciones y medio ambiente** — São João; cuidado de la playa y los manglares.
  - `formal-cause-connectors`: devido a, graças a, em virtude de
  - `impersonal-proposals`: é preciso + infinitivo; precisamos + infinitivo
  - `contrast-connectors`: enquanto, ao passo que, por outro lado
  - `passive-ser-intro`: Voz pasiva con ser + participio: foi organizado por, é celebrado em; agente con por.
  - `confirm-information-formulas`: se entendi bem…; ou seja…; quer dizer que…
- **B10 Repaso y proyecto del nivel** — Camila resuelve un caso real y escribe un texto de opinión.
  - `embora-subjunctive`: embora, mesmo que + subjuntivo
  - `discourse-organizers`: em primeiro lugar, além disso, por fim, portanto
  - `adversative-connectors`: porém, contudo, no entanto

## N5 · B2 entrada (2030)

Historia: Camila es gerente de producto; regulariza su residencia (B1); viaja por el Nordeste (B3); lidera un proyecto de visitas guiadas al Recife Antigo con un grupo de guías locales (B9). Desde N5 hay tareas integradas inspiradas en Celpe-Bras (leer o escuchar para escribir o hablar con propósito y destinatario).

- **B1 Cambios de vida y adaptación** — trámites de residencia y balance de cuatro años en Brasil.
  - `imperfeito-subjuntivo-forms`: fizesse, tivesse, fosse, pudesse
  - `querer-que-imperfeito-subjuntivo`: eu queria que + imperfeito do subjuntivo
  - `passive-ser-participle`: foi aprovado pela…; ser + particípio + por
  - `passive-se-productive`: aluga-se, vendem-se, exige-se
  - `infinitivo-composto`: por ter chegado; depois de ter feito; ter + particípio
- **B2 Especular y valorar el pasado** — Camila imagina qué habría pasado.
  - `futuro-do-preterito-composto`: teria + particípio
  - `se-imperfeito-subjuntivo-hypothesis`: se eu tivesse tempo, viajaria
  - `se-mais-que-perfeito-subjuntivo`: se eu tivesse sabido, teria ido
  - `past-probability-pode-ter`: pode ter + particípio; deve ter sido
  - `near-miss-quase`: quase + perfeito; por pouco; se ao menos
- **B3 Viajes con detalle** — viaje por el Nordeste.
  - `relative-cujo-o-qual`: cujo/cuja; o qual, a qual; em cuja
  - `nao-deixe-de-recommendation`: não deixe de + infinitivo; vale muito a pena
  - `descriptive-intensifiers`: Intensificadores (extremamente, bastante, de tirar o fôlego, incrível) y gradación del adj
  - `travel-compensation-formulas`: tenho direito a…; exijo; solicito compensação
  - `narrative-connectors-time`: de repente, enquanto isso, assim que
- **B4 Gastronomía y cultura** — Mercado de São José y la cocina pernambucana.
  - `augmentatives-diminutives`: -inho/-zinho, -ão; cafezinho, pãozinho, valor afectivo
  - `gastronomy-collocations`: ponto da carne, ao ponto, bem passado, tempero
  - `sensory-adjectives`: crocante, picante, cremoso, defumado
  - `review-genre-structure`: apreciación, aspectos positivos y negativos, recomendación
  - `recipe-register-infinitive`: modo de preparo con infinitivo (Misturar, Assar)
- **B5 Salud, ciencia y prevención** — hábitos, salud y divulgación científica.
  - `cause-effect-connectors`: causar, provocar, levar a, resultar em
  - `evidence-expressions`: os dados mostram que…; segundo o estudo; comprovado
  - `prevention-para-evitar-que`: para evitar que + subjuntivo; a fim de que
  - `passive-progressive-sendo`: está sendo estudado; foi ficando
  - `treatment-instructions-formulas`: de 8 em 8 horas; via oral; efeitos colaterais
- **B6 Lo que dijeron otros** — fidelidad al contar lo dicho en reuniones y entrevistas.
  - `reported-speech-backshift-complete`: disse que tinha feito / que faria / que fizesse
  - `reported-requests-subjunctive`: pediu que eu fosse; mandou que
  - `temporal-correlation-connectors`: assim que, logo que, depois que, antes que + subjuntivo
  - `clitic-placement-norms`: me ajuda (habla brasileña) frente a ajuda-me (norma escrita)
  - `source-citing-verbs`: afirmar, declarar, garantir; segundo; conforme
- **B7 Medios con criterio** — noticias, titulares y fiabilidad.
  - `epistemic-modalization`: certamente, supostamente, possivelmente
  - `headline-grammar`: omisión del artículo, presente periodístico, infinitivo
  - `loaded-language-bias`: léxico valorativo y sesgo
  - `source-reliability-formulas`: fonte não identificada; segundo fontes; alega que
  - `science-hedges-tudo-indica`: tudo indica que; pode ser que; parece indicar
- **B8 Acuerdos, desacuerdos y ética** — una decisión del equipo con dilema ético.
  - `concession-subjunctive-extended`: mesmo que, ainda que, por mais que + subjuntivo
  - `polite-disagreement-formulas`: entendo seu ponto, mas…; respeito, porém…
  - `middle-ground-formulas`: por um lado… por outro; um meio-termo; ceder
  - `ethical-judgment-deveria`: deveria / não deveria; seria correto
  - `agreement-closure-formulas`: combinado; fechado; estamos de acordo
- **B9 Liderar un proyecto pequeño** — las visitas guiadas al Recife Antigo.
  - `imperative-plural-instructions`: façam, entreguem; gostaria que vocês…
  - `prioritization-markers`: em primeiro lugar, o mais urgente, antes de mais nada
  - `progress-report-formulas`: já concluímos; falta; está em andamento; estamos atrasados
  - `figures-approximation`: cerca de, aproximadamente, a maioria, metade, um terço
  - `team-motivation-formulas`: vamos conseguir; contem comigo; parabéns, pessoal
- **B10 Repaso y proyecto del nivel** — tarea integrada tipo Celpe-Bras sobre las visitas guiadas.
  - `integrated-task-reading-writing`: Integración tipo Celpe-Bras: lectura de insumos, elección de género y de registro, adecuac
  - `integrated-task-listening-speaking`: Integración tipo Celpe-Bras: escucha de insumos, planificación y respuesta oral con regist
  - `integrated-b2-entry-portfolio`: Autoevaluación y revisión de textos del nivel; criterios de adecuación, coherencia y corre

## N6 · B2 (2031)

Historia: Camila negocia con clientes (Diego) y con su equipo (Yasmin); primera charla en un evento de tecnología (B8); Lucas se gradúa y empieza a trabajar en software (B5).

- **B1 Familias y relaciones hoy** — Camila y Dona Marina comparan generaciones.
  - `generational-comparison-expressions`: antigamente, hoje em dia, cada vez mais
  - `quanto-mais-quanto-menos`: quanto mais…, mais…
  - `anaphoric-reference`: este/esse/aquele, o primeiro/o segundo, o último para retomar
  - `opinion-defense-formulas`: sustento que…; não se pode negar que…
  - `integrated-generations-debate`: Integración de B1: comparación, proporción, anáfora y defensa.
- **B2 Condiciones, contratos y garantías** — contrato con un cliente.
  - `conditional-three-types-contrast`: se + presente; se + imperfeito do subjuntivo; se + futuro do subjuntivo
  - `legal-formulas-plain`: as partes, o contratante, fica estabelecido que
  - `warranty-formulas`: garantia de 12 meses; cobre/não cobre; defeito
  - `restrictive-conditions-salvo-se`: contanto que, salvo se, exceto se
  - `future-subjunctive-indefinite-clauses`: quem quiser, o que vier, onde for
- **B3 Valorar decisiones y dar retroalimentación** — retroalimentación a Yasmin.
  - `past-decision-evaluation`: foi uma boa decisão; acertou ao…
  - `expectation-esperava-que`: esperava que + imperfeito do subjuntivo; era de se esperar
  - `constructive-feedback-formulas`: ponto forte; poderia melhorar; sugiro
  - `receiving-criticism-formulas`: agradeço o retorno; você tem razão
  - `infinitivo-pessoal-extended`: por termos feito; ao chegarem; para eles entenderem
- **B4 Decir las cosas con tacto** — mensajes delicados a clientes y colegas.
  - `indirect-questions-polite`: gostaria de saber se…; você poderia me dizer onde…
  - `euphemism-softening`: não é bem assim; talvez não seja o melhor momento
  - `clitic-placement-formal`: ênclise formal (Informo-lhe; Segue anexo); mesóclise solo reconocimiento
  - `polite-refusal-formulas`: agradeço o convite, mas…; lamento não poder
  - `softened-complaint-formulas`: percebi que…; talvez tenha havido um engano
- **B5 Recursos para convencer** — argumentar con énfasis; anuncios y campañas.
  - `cleft-emphasis`: foi a Ana que…; é que…; quem fez foi…
  - `rhetorical-questions`: preguntas retóricas
  - `nao-so-mas-tambem`: não só… mas também; tanto… quanto
  - `absolute-superlative-issimo`: lindíssimo, facílimo, ótimo
  - `advertising-slogan-devices`: imperativo, rima, repetición y frases nominales
- **B6 Reuniones y plazos** — reuniones de equipo, actas y seguimiento.
  - `turn-taking-formulas`: posso complementar?; deixa eu concluir; passo a palavra
  - `deadline-commitment-formulas`: ficou combinado que…; retorno até…
  - `minutes-passive-conventions`: foi decidido; ficou acordado; registra-se
  - `follow-up-formulas`: só passando para lembrar; conforme combinado
  - `caber-a-responsibility`: cabe a…; fica sob a responsabilidade de…
- **B7 Negociar en la vida diaria** — alquiler, descuentos y compras grandes.
  - `conditional-negotiation-offers`: se vocês aceitarem…, poderíamos…
  - `concession-counteroffer-formulas`: em contrapartida; estamos dispostos a…
  - `written-confirmation-formulas`: conforme conversado; segue o resumo
  - `a-vista-parcelado`: à vista, parcelado, desconto, sinal
  - `bargaining-everyday-formulas`: dá para fazer por…?; fecha por…?
- **B8 Hablar en público** — su primera charla.
  - `speech-structure-markers`: vou falar sobre…; em primeiro lugar; para concluir
  - `reformulation-formulas`: ou seja; em outras palavras; quer dizer
  - `audience-questions-formulas`: boa pergunta; se entendi bem…
  - `oral-synthesis-formulas`: resumindo; em síntese
  - `slide-visual-reference-formulas`: Referencias deícticas a materiales visuales.
- **B9 Tecnología, datos y sociedad** — datos de uso de los productos y su impacto.
  - `data-trend-verbs`: aumentar, cair, crescer, estabilizar; de X para Y
  - `prudent-comparison-formulas`: em relação a; em comparação com; proporcionalmente
  - `tender-a-prediction`: tende a; deve + infinitivo; é possível que
  - `data-limits-formulas`: a amostra não permite concluir…; correlação não implica causa
  - `effect-analysis-formulas`: contribuir para, resultar em, impacto sobre
- **B10 Repaso y proyecto del nivel** — debate, informe y negociación integrados.
  - `integrated-debate-argument`: Integración B1–B5: argumentar con evidencia.
  - `integrated-negotiation-simulation`: Integración B2, B6 y B7: negociación completa.
  - `integrated-b2-portfolio`: Integración de todo N6 para el portafolio B2.

## N7 · B2 alto (2032)

Historia: Camila escribe mensajes delicados para clientes; investiga la historia de Recife (holandeses en el siglo XVII, el puerto, los puentes) para una ruta guiada (B4); visita a Ana en Lisboa (B8; las diferencias entre Brasil y Portugal se comentan como cultura, sin clave de gramática: pt-PT entra en N8 B4); lee a Clarice Lispector, Manuel Bandeira y João Cabral (B9).

- **B1 Registro y matices** — mensajes delicados a clientes.
  - `register-continuum`: coloquial, neutro y formal
  - `connotation-nuance`: sinónimos con connotación distinta
  - `register-reformulation`: pasar un mensaje de informal a formal
  - `delicate-message-formulas`: lamentamos informar; infelizmente não foi possível
  - `nominalization-formal-style`: a realização de…; a ausência de…
- **B2 Cronologías complejas** — relatos largos y planes con varias fechas.
  - `mais-que-perfeito-simples-recognition`: fora, tinha sido en textos escritos
  - `narrative-time-connectors-advanced`: mal, no momento em que, à medida que
  - `future-do-presente-forecasts`: chegará, será realizado; previsiones formales
  - `itinerary-formulas`: partida às 8h; com escala; seguirá
  - `gerundio-simultaneity`: chegando, ao mesmo tempo, indo
- **B3 Lo que pudo ser y lo que sabemos** — reconstruir un suceso y declarar como testigo.
  - `certainty-gradation-modals`: certo, provável, possível, improvável
  - `evidence-explicit-markers`: a prova é; tudo indica; consta que
  - `alternative-scenarios-counterfactual`: se…, teria; a não ser que
  - `witness-statement-formulas`: declaro que; presenciei; vi quando
  - `impossibility-nao-pode-ter-sido`: não pode ter sido; não deve ter sido
- **B4 Historias de ciudades y objetos** — historia de Recife.
  - `historical-passive-ser-se`: foi fundada em; construiu-se
  - `historical-present`: presente histórico narrativo
  - `attribution-impersonal-se`: atribui-se a; acredita-se que; estima-se que
  - `guided-tour-formulas`: à nossa esquerda; repare que; vale notar
  - `source-exposition-structure`: introducción, desarrollo, fuentes y cierre
- **B5 Humor, metáforas y modismos** — chistes, metáforas y expresiones frecuentes.
  - `metaphor-comparison-como-se`: como se + imperfeito do subjuntivo; feito; parece
  - `idioms-brazilian-frequent`: quebrar o galho; dar um jeito; dar as caras
  - `humor-wordplay-double-meaning`: trocadilho, duplo sentido, exagero
  - `joke-telling-structure`: preparación, giro y remate
  - `figurative-language-transfer`: integración de lenguaje figurado y humor
- **B6 Argumentar y debatir** — un debate con tesis y réplica.
  - `thesis-evidence-structure`: tese, argumento, exemplo
  - `refutation-formulas`: é verdade que…, mas; isso não procede
  - `debate-turn-formulas`: peço a palavra; réplica
  - `argument-closing-formulas`: portanto, em suma, diante disso
  - `debate-integration-transfer`: integración del debate completo
- **B7 Negociaciones con varias partes** — acuerdo escrito entre varias partes.
  - `conditional-offer-chains`: se A aceitar X, B poderá Y
  - `written-agreement-formulas`: fica acordado; as partes concordam
  - `reconciling-interests-formulas`: conciliar; ambos os lados
  - `ambos-cada-um-reference`: ambos, cada um, um e outro, tanto A quanto B
  - `negotiation-integration-transfer`: integración de negociación multilateral
- **B8 Culturas en contacto** — Lisboa y las diferencias entre Brasil y Portugal.
  - `generalization-hedging`: em geral; costuma-se; nem todos; a maioria
  - `culture-shock-formulas`: estranhar; acostumar-se a; estar acostumado a
  - `stereotype-avoidance-formulas`: nem todo…; sem generalizar
  - `regional-brazilian-recognition`: Nordeste, Sudeste, Sul; solo reconocimiento
  - `intercultural-comment-transfer`: integración de comentario intercultural
- **B9 Relatos, personajes y narradores** — autores pernambucanos.
  - `narrator-point-of-view`: primera/tercera persona; narrador omnisciente
  - `literary-dialogue-punctuation`: travessão; verbos dicendi (murmurou, exclamou)
  - `character-analysis-adjectives`: léxico para describir carácter y conflicto
  - `literary-clitics-mesoclisis-recognition`: ênclise, mesóclise en textos literarios
  - `free-indirect-speech-recognition`: discurso indirecto libre
- **B10 Repaso y proyecto del nivel** — caso nuevo con análisis, debate y revisión.
  - `integrated-register-case`: registro y matices integrados
  - `integrated-debate-analysis`: análisis y debate integrados
  - `integrated-b2-high-portfolio`: dossier B2 alto integrado

## N8 · C1 entrada (2033)

Historia: Camila prepara el Celpe-Bras en un curso donde conoce a Tomás (argentino, voseo); habla rápida y radio; variedades del portugués (Nordeste, Sudeste, Sur); reclamación por escrito; presenta un estudio breve en un curso universitario (B9).

- **B1 Escucha rápida y habla conectada** — radio y conversaciones rápidas en el curso.
  - `spoken-reductions-extended`: né, cê, tô, vamo, cadê
  - `backchannel-markers`: aham, pois é, sei, então
  - `clarification-precise-formulas`: você se refere a…?; quer dizer que…?
  - `note-taking-shorthand`: abreviaturas y notas al vuelo
  - `discourse-fillers-hesitation`: tipo, assim, sabe, né
- **B2 Leer entre líneas** — textos con implícitos.
  - `presupposition-triggers`: já não, ainda, até, deixou de
  - `mild-irony-markers`: olha só; que beleza, hein
  - `inference-expressions`: dá a entender que; pelo visto; subentende-se
  - `attitude-lexicon`: léxico de actitud y tono
- **B3 Cómo persuade un mensaje** — discursos, eslóganes y campañas.
  - `persuasion-devices-framing`: encuadre, repetición, preguntas
  - `slogan-rhyme-brevity`: brevedad y rima
  - `parallelism-repetition`: paralelismo y triple repetición
  - `critical-analysis-formulas`: o texto pretende…; apela a…
- **B4 Variedades de la lengua** — Nordeste, Sudeste, Sur y primer contacto con pt-PT.
  - `regional-brazilian-varieties`: macaxeira/aipim/mandioca; léxico y entonación
  - `pt-pt-lexical-recognition`: autocarro, comboio, pequeno-almoço; solo reconocimiento
  - `pt-pt-grammar-recognition`: estar a + infinitivo, tu, ênclise; solo reconocimiento
  - `adapt-to-interlocutor-formulas`: aqui dizemos…; você quer dizer…?
- **B5 Expresiones idiomáticas** — modismos y refranes en contexto.
  - `proverbs-refranes`: dichos populares en contexto
  - `idioms-register-control`: gíria frente a formal
  - `paraphrase-techniques`: ou seja; dito de outra forma
  - `lyrics-commentary-vocab`: verso, estribilho, metáfora
- **B6 Cine, series y pódcasts** — notas, resumen y comentario.
  - `film-analysis-vocab`: plano, cena, roteiro, trilha sonora
  - `podcast-summary-structure`: tema, postura y conclusión
  - `evaluative-language-reviews`: léxico evaluativo
  - `comment-opinion-formulas`: na minha leitura…; o que mais chama atenção
- **B7 Literatura y memoria** — crónica y fragmentos literarios.
  - `evocative-imperfeito-memory`: imperfeito evocativo; eu me lembro de
  - `adverbs-mente-precision`: advérbios em -mente para precisión
  - `chronicle-genre-structure`: crônica: cena, reflexión, cierre
  - `stylistic-figures`: comparación, personificación, metonimia
- **B8 Reclamar y dar seguimiento por escrito** — reclamación escalada.
  - `escalated-complaint-structure`: antecedentes, incumplimiento, petición, plazo
  - `formal-letter-formulas`: Ao Senhor…; Aguardo retorno
  - `insistence-courtesy-formulas`: reitero; conforme e-mail anterior
  - `case-closure-formulas`: dou por encerrado; solicito confirmação por escrito
- **B9 Estudiar y presentar con cautela** — estudio breve en un curso universitario.
  - `academic-hedging`: parece sugerir; os resultados indicam que…
  - `academic-citation-formulas`: segundo X (2020); de acordo com
  - `graph-description-formulas`: o gráfico mostra; eixo; pico
  - `presentation-structure-academic`: objetivo, método, resultados, conclusão
- **B10 Repaso y proyecto del nivel** — proyecto cultural integrado.

## N9 · C1 (2034)

Historia: Camila es directora de producto en Maré Digital: contactos en una feria en São Paulo (B1), reuniones (B4), selección de personal (B5), informes (B6), riesgos y prevención en la temporada de lluvias (B7), trámites públicos como la naturalización (B8; el certificado Celpe-Bras, emitido por el Inep, es uno de los comprobantes de lengua que se aceptan) y un conflicto con un proveedor (B9).

- **B1 Crear contactos** — la feria en São Paulo.
  - `networking-opening-formulas`: abrir conversación en eventos
  - `affinity-building-formulas`: buscar intereses comunes
  - `professional-introduction-pitch`: presentación profesional de 30 segundos
  - `follow-up-message-formulas`: foi um prazer; como combinamos
- **B2 Historias con propósito** — una historia de producto con gancho.
  - `story-hook-formulas`: comecei com…; imagine que…
  - `tension-narrative-tenses`: presente histórico; perfeito e imperfeito narrativos
  - `plot-turn-markers`: só que; foi aí que
  - `lesson-extraction-formulas`: a lição é…; aprendi que…
- **B3 Mensajes claros y breves** — correos ejecutivos.
  - `executive-summary-structure`: pirámide invertida
  - `brevity-nominalization`: nominalización y listas
  - `priority-signal-formulas`: ação necessária; em resumo
  - `decision-communication-formulas`: decidimos que…; a partir de…
- **B4 Dirigir reuniones** — moderar y registrar acuerdos.
  - `meeting-moderation-formulas`: abertura, pauta, encerramento
  - `giving-floor-formulas`: passo a palavra a…; quem gostaria de…?
  - `debate-summary-formulas`: resumindo as posições…
  - `minutes-action-items`: responsável, prazo, ação
- **B5 Entrevistas y procesos de selección** — selección de personal.
  - `star-answer-structure`: situação, tarefa, ação, resultado
  - `candidacy-defense-formulas`: o que posso agregar…
  - `interviewer-question-formulas`: preguntas de entrevistador
  - `salary-negotiation-formulas`: pretensão salarial; benefícios
- **B6 Informes y datos** — informes con límites de la evidencia.
  - `report-structure-formal`: resumen, método, resultados, recomendaciones
  - `data-source-citation-rigor`: fonte, ano, amostra
  - `conclusion-hedging-limits`: com as ressalvas…
  - `recommendation-formulas`: recomenda-se; sugere-se
- **B7 Riesgo, seguridad y prevención** — temporada de lluvias.
  - `risk-assessment-formulas`: probabilidade e impacto
  - `warning-formulas`: atenção; sob pena de
  - `prevention-measure-formulas`: a fim de evitar; recomenda-se
  - `emergency-instruction-formulas`: mantenha a calma; evacuem
- **B8 Normas y trámites públicos** — naturalización y trámites.
  - `normative-text-comprehension`: fica vedado; é facultado; sujeito a
  - `duty-right-formulas`: tem direito a; é dever de
  - `procedure-steps-formulas`: protocolar, apresentar, comparecer
  - `appeal-formulas`: interpor recurso; solicitar revisão
  - `plain-language-explanation-formulas`: explicar uma norma em linguagem simples
- **B9 Negociar y resolver conflictos** — conflicto con un proveedor.
  - `interest-based-negotiation-formulas`: posiciones frente a intereses
  - `conflict-management-formulas`: gestionar tensión
  - `i-messages-no-blame`: eu me sinto…quando…
  - `reparation-proposal-formulas`: proponho que…; como forma de reparar
- **B10 Repaso y proyecto del nivel** — propuesta con calendario, presupuesto y riesgos.

## N10 · C1 dominio (2035)

Historia: Camila y Lucas fundan Travessia (estudio de producto digital y localización español–portugués); conversación natural, humor, debate, escritura extensa, crítica cultural, vida de barrio y mediación (Camila interpreta entre un cliente hispanohablante y una clínica o una notaría, **cartório**, B9).

- **B1 Conversación natural** — charlas largas con amigos y colegas.
  - `conversation-ellipsis`: elipsis; e aí?; beleza
  - `topic-change-markers`: falando nisso; aliás; voltando
  - `spontaneous-reactions-interjections`: nossa; caramba; poxa
  - `discourse-markers-spoken-advanced`: tipo, então, sabe, quer dizer
  - `conversation-natural-transfer`: Integración: elipsis, cambio de tema, interjecciones y marcadores en una sobremesa larga.
- **B2 Contar historias con maestría** — anécdotas con ritmo y desenlace.
  - `narrative-pacing-devices`: ritmo y suspenso
  - `scene-voice-dialogue-mimicry`: voz y diálogo
  - `ending-impact-formulas`: cierre con impacto
  - `descriptive-detail-scene`: detalle descriptivo
  - `anecdote-integrated-transfer`: Integración: ritmo, voces, detalle y cierre en una anécdota completa.
- **B3 Humor, ironía y cultura** — humor sin estereotipos.
  - `irony-structures`: ironía y sarcasmo
  - `hyperbole-exaggeration`: exageración intencional
  - `cultural-references-recognition`: referencias culturales
  - `tone-adaptation-cultural`: adaptar el tono
  - `humor-culture-transfer`: Integración: ironía, exageración, referencias y tono en un número de humor sin estereotipo
- **B4 Debate complejo y diplomacia** — mesa redonda.
  - `refutation-precise-formulas`: refutar con precisión
  - `strategic-concession-formulas`: conceder para avanzar
  - `face-saving-formulas`: proteger la imagen del otro
  - `roundtable-moderation-formulas`: moderar una mesa
  - `debate-diplomacy-transfer`: Integración: refutar, conceder, proteger al otro y moderar en un debate completo.
- **B5 Escritura académica y extensa** — textos largos y fuentes.
  - `academic-essay-structure`: estructura de ensayo
  - `source-synthesis-formulas`: síntesis de fuentes
  - `cautious-discussion-formulas`: discusión cautelosa
  - `clarity-revision-checklist`: revisión de claridad
  - `extended-writing-transfer`: Integración: tesis, fuentes, cautela y revisión en un texto extenso final.
- **B6 Proyectos y negocios propios** — Travessia.
  - `business-plan-formulas`: plan de negocio
  - `financing-formulas`: financiación
  - `contingency-formulas`: caso ocorra; na eventualidade de
  - `pitch-structure`: pitch
  - `partner-negotiation-formulas`: negociar con socios
- **B7 Crítica cultural: cine y literatura** — reseñas con contexto.
  - `critical-review-structure`: estructura de crítica
  - `evaluative-vocabulary-advanced`: léxico evaluativo
  - `contextual-analysis-formulas`: análisis en contexto
  - `interpretation-defense-formulas`: defender una interpretación
  - `cultural-criticism-transfer`: Integración: estructura, léxico evaluativo, contexto y defensa en una crítica completa.
- **B8 Vivir en la lengua** — barrio, servicios e imprevistos.
  - `unforeseen-resolution-formulas`: resolver imprevistos
  - `improvisation-formulas`: improvisar
  - `misunderstanding-repair-formulas`: reparar malentendidos
  - `community-integration-formulas`: integrarse en la comunidad
  - `neighborhood-life-transfer`: Integración: imprevistos, improvisación, aclaraciones y comunidad en un día de barrio.
- **B9 Mediar entre personas y textos** — Camila interpreta en una clínica o en un cartório.
  - `mediation-formulas`: ele diz que…; ela quer saber se…
  - `summarizing-for-third-parties`: resumir para terceros
  - `text-adaptation-audience`: adaptar un texto
  - `informal-interpreting-formulas`: interpretar informalmente
  - `legal-medical-register-recognition`: certidão, procuração, consulta, exame
- **B10 Repaso y proyecto final** — Travessia se lanza el 5 de septiembre de 2035.
  - `integrated-conversation-narrative`: Integración: conversación natural, anécdota y humor en una charla larga de presentación de
  - `integrated-debate-writing`: Integración: debate diplomático, escritura académica y crítica en un texto de postura.
  - `integrated-mediation-business`: Integración: negocio, imprevistos, comunidad y mediación en la preparación del lanzamiento
