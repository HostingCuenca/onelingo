# Revisión del plan N5 (portugués de Brasil)

Veredicto: GO

Validadores sobre `curriculo/pt/n5.json`: `validar_plan.py pt` → 0 errores (701 avisos de vocabulario repetido, esperables en un nivel B2 que recicla léxico de N3–N4); `validar_plan_detallado.py pt curriculo/pt/n5.json` → 0 errores · 50 clases · 653 ejercicios · 653 consignas únicas · 653 ejemplos únicos. Los 50 ids están en estado `planificado` y los campos congelados coinciden con `tools/curriculo/pt/n5-outline.json`.

Revisión independiente de los diez lotes C01–C50 (ya escritos a mano, no por plantilla: situaciones de 80–250 palabras (media 135) con diálogo, datos propios en cada clase y tareas Celpe-Bras desde B1). Búsqueda automática previa: 0 menciones al país andino ni a las ciudades vetadas, 0 europeísmos léxicos, 0 consignas o ejemplos repetidos. Se aplicaron **52 correcciones puntuales** en `tools/curriculo/pt/n5-lote-*.json` (copia de los originales en la carpeta de scratch) y se consolidó el nivel. No se encontraron distractores absurdos ni agramaticales sin intención (los errores de los distractores son los típicos de hispanohablante: «cujo falésia», «Vende-se móveis», «pãoinho», «seis sete por cento», «Se eu tenho coragem…»), ni errores de pt-BR en las claves de respuesta.

## Cambios por tipo

### Ambigüedad, estímulo insuficiente y claves (27)

- Respuestas con dos soluciones válidas y sin pista: C06 i0 «devia/deveria» → se pide «deber en imperfeito (devia)»; C09 i0 «não pode/deve ter sido» → «poder + ter + participio»; C26 g0 «tinha/havia» → «auxiliar ter (no haver)»; C26 i0 «passada/anterior» → «adjetivo formal que empieza con a-»; C31 g0 «supostamente/possivelmente/provavelmente» → «adverbio que empieza con s- … según se supone»; C37 g1 («porém/contudo/todavia») y C37 i0 («objeção/ressalva/dúvida») → pista de la letra inicial; C12 e0 («muito/bem/bastante») → «la palabra que significa mucho»; C15 s1 («assim/logo que») → «primera palabra de “assim que”»; C23 e1 «de modo/de forma que» → «a ___ de que» (fim); C41 s1 «aprovar/aprove» → «futuro de subjuntivo»; C50 e4 «deveria/devia» → «condicional de dever».
- Ordenar con más de un orden gramatical: C18 e3 («Caldinho da casa cujo tempero…» o «Caldinho cujo tempero… da casa»), C19 g2 (conector «porém» móvil), C20 e2, C25 e3, C28 e3, C30 g2 y e3, C31 g2, C33 g2 → se cambian las palabras para que la frase sea única o la consigna indica con qué palabra empieza.
- C25 e3: la «posología» ya estaba en g0 y la respuesta admitía dos órdenes → «duración del tratamiento» con una frase unívoca.
- C23 e1, C46 i0 («unidad lógica» → «cualidad de un texto sin contradicciones»), C20 e2.

### Coherencia con la historia y hechos reales (12)

- C08: «Como trabalho como freelancer, nem precisaria cumprir aviso prévio» (el aviso prévio es de empleados con contrato; Lucas aún termina la carrera en N5 y se gradúa en N6) → «Como ainda estou terminando a faculdade, nem precisaria cumprir aviso prévio».
- C10: Camila dice a Dona Marina «Vou mandar essa crônica para ele» en un domingo sin explicar dónde está; ahora lo dice «por telefone».
- C14 e2: la «carta de Camila» hablaba de overbooking y de reembolso, que contradecían la situación (vuelo cancelado y reacomodado) → «carta de um passageiro».
- C15 g1: «Lucas procurava água no posto» contradecía la situación («fazia amizade com um vendedor de água de coco») → «conversava com um vendedor de água de coco».
- C23 i2: «casaco» en el clima cálido de Recife → «lanche/lanchinho».
- C38 e2: «Depois de uma hora… acordo» contra «Chegaram a um acordo em vinte minutos» → «vinte minutos».
- C41: Davi pedía «a Rua do Bom Jesus», pero C43 se la asigna a Luana → pide «a sinagoga».
- C45 e2: «O patrocinador fez um reconhecimento público» (el patrocinador acababa de recortar la verba) → «A Iara fez…».
- C48 e2: «nota 8 para a própria coesão» pero el portafolio dice que faltó coesión → «nota 6».
- C50 e0: «As placas foram instaladas pela Prefeitura» contradecía el texto (faltan placas) → «As visitas foram organizadas pela Maré Digital».

### Lengua, gramática y registro pt-BR (8)

- C07: «Se eu pudesse voltar no tempo, teria feito um intercâmbio» mezclaba imperfeito do subjuntivo con condicional compuesto en una clase de hipótesis del presente → «…faria um intercâmbio aos vinte anos» (situación y relacionar).
- C16 g1: la advertencia «⚠ en portugués no existe -illo» no explicaba el distractor «pãoinho» → «⚠ tras -ão se usa -zinho, no -inho».
- C18 g1: «esquisito significa “raro”» → «significa “extraño”, no “exquisito”» (el falso amigo exacto).
- C19: la «cartola» (plátano frito con queso, azúcar y canela) se describía como «aveludada» → «quentinha e crocante» (e2 y e3).
- C27 e4: «pediu que não deixássemos o relatório» cambiaba el destinatario del pedido original («não deixe», dirigido a Camila) → «pediu que eu não deixasse».
- C16 vocabulario: «paozão» sin tilde (el texto usa «pãozão»); se deja como está en el campo congelado del esqueleto (ver «Sin resolver»).

### Canon y personajes (5)

Nombres secundarios repetidos con roles distintos dentro del mismo nivel, que confundían al alumno: se renombran sin tocar el reparto canónico.

- C05: Carolina (chilena del pódcast) → **Daniela** (Carolina queda como analista de datos de Maré Digital desde C26).
- C06: Luana (lectora de Caruaru) → **Michele** (Luana Freitas es la guía del proyecto desde C30).
- C13: reseñas de «Rafael» y «Carolina» → **Henrique** y **Priscila** (Rafael y Carolina son compañeros de equipo en C26–C40).
- C19: «Luana P.» y «Valentina M.» → **Marcela P.** y **Larissa M.**
- C27: la practicante Valentina → **Patrícia** (Valentina es la funcionaria del despachante en C02).

Nombres del reparto verificados contra el MAPA: Camila (31 años, gerente de producto), Dona Marina («a senhora», Boa Viagem, profesora de Historia jubilada), Lucas (alfaia, UFPE), Ana en Lisboa (N4 B6), Bruno (coordinador), Bia (Café da Bia), seu Pedro (portero), Renata (grupo B2 en la Escola Capibaribe), seu Alberto (dueño del apartamento de Graças), Iara Menezes (directora), Dra. Helena Rocha. No aparece ningún personaje de N6–N10 (Diego Salazar, Yasmin, Tomás).

### Distractores absurdos o agramaticales

0 hallados. Los distractores de elegir/completar son errores reales de hispanohablante (concordancia de cujo, «Vende-se móveis», imperfeito do subjuntivo vs. indicativo, falsos amigos). Se dejaron los distractores de registro (p. ej. «Você está errado e pronto», «Troca essa carne agora») porque modelan errores de adecuación, objetivo de N5.

## Límites aceptados

- El esqueleto de ejercicios es el mismo en las 50 clases (3 guiados + 3 independientes + 2 de situación + 5 de evaluación, un relacionar con pistas cruzadas por clase; C50 con 8 de evaluación): es el formato aprobado y lo exige el validador. Cada clase mantiene datos, escena y distractores propios.
- Las situaciones tienen entre 80 y 250 palabras, media 135 (el PLAN fija 300–500 para N5–N7); el validador las acepta y los ejercicios de producción piden 60–100 palabras (el PLAN, 200–300). Si se quiere el rango del PLAN, hay que ampliar C46–C50.
- En ítems de «ordenar» de 7–9 palabras quedan algunos con una segunda frase gramatical muy marginal (p. ej. C41 e3, C42 g2); se priorizó que el orden dado sea el natural.
- C05 g0 («Por ter chegado» / «Por chegar») y C21 i1 («por isso» / «porque») se resuelven por la forma pedida y por el sentido, no por una pista literal.
- C02, C14, C22, C24, C32–C34: noticias, estudios, medicamentos, cifras y rumores son ficticios; se presentan sin nombrar medios, hospitales ni bancos reales.
- C48 sigue hablando de un «relatório para a Iara» y C44 de uno «para o patrocinador»: son dos informes distintos del proyecto.

## Sin resolver

- `tools/curriculo/pt/n5-outline.json` (campo congelado `vocabulario` de C16): «paozão» debería ser «pãozão». No lo he tocado porque el encargo no incluye el esqueleto; basta una corrección de una palabra y volver a consolidar.

## Hechos del reparto confirmados

- Camila cumple 31 años el 14 de marzo de 2030; gerente de producto en Maré Digital (Porto Digital); vive en Graças (apartamento de seu Alberto); cuatro años en Recife en septiembre de 2030; sigue con Renata (grupo B2, Escola Capibaribe). Moneda: R$.
- B1: autorización de residencia por plazo indeterminado ante la Polícia Federal en marzo de 2030, deferida el 12 de junio de 2030; recogida biométrica en 30 días. Seu Alberto da una declaración de domicilio. Balance de cuatro años para el mural de Renata.
- Ana vive en Lisboa (N4 B6) y sigue en contacto por mensajes; Lucas (26) busca su primer empleo en software (se gradúa en N6 B5); Dona Marina vive en Boa Viagem con Frevo y revisa las fechas históricas de las visitas guiadas (profesora de Historia jubilada); seu Pedro, portero de su edificio.
- Camila viaja con la familia en Miami (hermana Valeria); estuvo en Fernando de Noronha en 2028 (N3 B5); Porto de Galinhas (piscinas naturales en la marea baja), Olinda (ladeiras, mirador) y Caruaru (feria) son reales.
- Recife: Mercado de São José, Marco Zero, Rua do Bom Jesus, sinagoga Kahal Zur Israel, Paço do Frevo, Porto Digital, Cartola y bolo de rolo, frevo Patrimonio Inmaterial desde 2012, Defesa Civil, Procon, Galo da Madrugada (hechos de la lista del MAPA).
- Trato: a senhora / o senhor con Iara, seu Alberto, Dra. Helena y personal de trámites; você con Ana, Bruno, Bia, Lucas, Renata y el equipo; a Dona Marina le habla de «a senhora» y ella la tutea con você.

## Hechos nuevos a confirmar

- es: los trámites (certidão de antecedentes, taxa hasta cinco días hábiles antes, 30 días para la biometría) son verosímiles pero no verificados contra la normativa vigente de la Polícia Federal. / en: the procedure details are plausible but not verified against current Polícia Federal rules.
- es: el despachante de la filial de Boa Viagem (C02), el aviso de la aerolínea y los números de protocolo (4471, REC48213) y los montos (R$ 280,00) son ficticios. / en: the despachante branch, the airline notice, protocol numbers and amounts are fictional.
- es: la farmacia da a Dona Marina horarios 6h, 14h y 22h para un antibiótico de 8 en 8 horas, con receta de la Dra. Helena (C25); Lucas «duerme en casa de la madre» esa noche (C25). / en: the pharmacy gives Dona Marina 6:00, 14:00 and 22:00 for an 8-hourly antibiotic prescribed by Dr. Helena (C25).
- es: guías del proyecto Luana Freitas, Davi, Júlia y Mateus; equipo de Maré Digital: Rafael, Carolina, Gustavo y Patrícia; cliente Rodrigo Prado. / en: project guides and team names are secondary characters with no canon.
- es: datos del mes piloto (612 visitantes, 410 de lengua española, 305 con nota máxima, R$ 18.100 de taquilla, R$ 20.000 de presupuesto) y del primer año (cerca de 7 mil visitantes; relatório a la Prefeitura hasta diciembre). / en: pilot-month and first-year figures are invented for the exercises.
- es: encuesta de Maré Digital (~70 % sin carteles en español), consulta pública de la Prefeitura con plazo el día 30 y red de hoteles de Boa Viagem como patrocinador (C46, C49). / en: Maré Digital survey, Prefeitura public consultation and hotel-chain sponsorship are invented.
- es: aviso de que la ladeira de Olinda y el paseo en buggy se recomiendan en un mismo audio de guía (C12); el buggy es una actividad real de Porto de Galinhas. / en: the Olinda guide mentions the Porto de Galinhas buggy ride.
