# Revisión N9 · B5 (fr.n9.c21–c25)

GO

Validación: `validar_ruta.py fr --borrador n9-b01…b09` (N8 ya está integrado en `assets/`, por eso no se pasa) → 0 errores. `validar_plan.py fr` → 0 errores, sin «título de la unidad difiere» para c21–c25. Cada clase tiene 5 ítems puntuables de evaluación en 5 formatos (escuchar, completar, elegir, ordenar, relacionar); los `escribir` son todos `abierta: true` y no cuentan. Los ejercicios de las fichas están presentes (mismo formato y clave); la única desviación es la de la situación (`escribir` en español → `elegir`), decidida por el autor/coordinador. Las situaciones miden 472–544 palabras (rango C1: 400–700). El vocabulario de cada ficha está completo (8 palabras) y no hay contenido de c26+.

## Correcciones

Todas en `n9-b05.json`.

### Todo el bloque
- Tipografía: espacio normal antes de `? ! : ; %` y como separador de miles → U+202F (también en las citas francesas dentro de textos es/en). Los títulos/objetivos se dejaron idénticos al plan.
- Español neutro: «salón(es)» (feria comercial) → «feria(s)»; «formación» (curso) → «capacitación» (como en c02); «horquilla» → «rango»; «Rellené/rellenas» → «Llené/llenas». Cargos: chargée de projet = «encargada de proyectos» / “project coordinator”; cheffe de projet = «jefa de proyectos» / “project manager” (ver «Sin resolver»).
- Todas las situaciones usan ya opciones en francés en las comprensiones (las 5 `s2` con opciones es/en pasaron a francés).

### c21
- Situación `contexto` es/en: «nueva jefa de proyectos» → «nueva encargada de proyectos (chargée de projet)».
- Explicación p2 y fila «Tâche» de la tabla: la tâche iba solo en imparfait, pero Thomas dice «Tâche : réduire ce délai» → «imparfait o infinitivo».
- e2: «À l’époque, je ___ dans une agence de voyages.» → añade «(travailler)» (sin el verbo cabían travaillais/étais…).
- s2: opciones es/en sobre gramática → «Dans la première réponse de Thomas, quelle phrase est l’action ?» (J’ai appelé cinq traiteurs. / Notre agence préparait un salon… / Ma tâche était claire.).
- Ejemplos: 9 → 8 (se quitó «Thomas passe l’entretien devant…», fuera de la horquilla 5–8; los nombres ya se enseñan en la tabla «Para leer»).

### c22
- Coherencia del contrato (pedido del coordinador): contexto y primera réplica de Ana. Antes: «contrat de trois mois se termine en juin, l’agence ouvre le poste de cheffe de projet». Ahora: «Je suis chargée de projet avec un contrat de trois mois, qui se termine à la fin du mois. L’agence ouvre le poste de cheffe de projet en CDI : c’est une promotion.» (se quitó «juin»: ver «Sin resolver»).
- Réplica «Je suis capable de diriger une équipe…» → añade «et je dirige déjà la réunion d’équipe de l’agence» (c16 de B3).
- Faure: «Et si nous vous demandons de diriger une équipe ?» → «demandions» (si + imparfait; en indicativo era incorrecto).
- s2: opciones es/en → «Que veut Ana quand elle dit « je tiens à ce que mes missions évoluent » ?» (Elle veut construire, pas seulement suivre. / quitter l’agence / moins de travail).
- «salones» → «ferias» (traducción de «trois salons»).

### c23
- Renombrado el candidato **Julien → Bastien** en todo el bloque (Julien es el colega de reservas de c04).
- «Avez-vous un permis ?» (pregunta cerrada para un guía a pie, sin sentido profesional; «permiso» además es ambiguo) → «Êtes-vous disponible le week-end ?» (explicación, tabla, g3). Réplicas de Mercier y Ana: «la disponibilité ou le permis» → «la disponibilité ou le diplôme»; «vérifier le permis» → «vérifier la disponibilité».
- Terminología de la relance unificada: «de profundización/probing» → «de seguimiento (relance)» (coincide con la tarjeta de vocabulario y la tabla).
- Nota de pronunciación de «la question fermée»: quitado «La d de «fermée» no existe» (decía algo falso).
- g4 (ordenar): `aceptadas` incluía «Avez-vous travaillé dans quelle agence ?», que no es una pregunta natural → eliminada (queda «Dans quelle agence avez-vous travaillé ?»).
- s2: opciones es/en → «Que répond Bastien à la question sur le groupe en retard ?» (Je téléphonerais au guide… / Je ne ferais rien. / Je ferais le même circuit en moitié moins de temps.).
- Dos réplicas seguidas de Mercier fundidas en una.

### c24
- Cifras (consistencia): Ana pide 40 000–44 000 bruto anual; Mercier ofrece 38 000 + 10 % variable («c’est le haut de la fourchette»); Ana baja a 40 000 con 2 días de teletrabajo. Faltaba que Mercier aceptara 40 000 y el final repetía 40 000 como acordado, y 38 000 «el máximo» contradecía aceptar 40 000. Ahora: «…c’est déjà le haut de notre fourchette» y Mercier responde «Pour le salaire, je peux monter jusqu’à 40 000 euros, avec la part variable de 10 %…». El resumen final de Ana (40 000, 10 %, 2 días tras la prueba, 3 días de capacitación, 6 meses de prueba por entrevista de evolución) coincide con la conversación.
- «Pour une cheffe de projet qui arrive dans l’agence» (Ana ya trabaja allí) → «Pour un premier poste de cheffe de projet».
- Réplica inicial de Ana: añade «dès le mois prochain, je serai cheffe de projet, et non plus chargée de projet» (el ascenso de c22).
- Error frecuente nº 4: «en contrepartie de deux jours de télétravail demandés → …; en contrepartie, je demande…» era falso (Ana dice «en contrepartie de deux jours…» en la situación) → ahora «en contrepartie à deux jours… → en contrepartie de deux jours…».
- g1: pista de «fourchette» reescrita (tenedor / rango).
- s2: opciones es/en → «Quelle concession Ana fait-elle ?» con tres opciones en francés.

### c25
- Calendario (Ana lleva un año, circuito de Lyon «lancé en mars» chocaba con su entrada): contexto y primera réplica «cheffe de projet depuis neuf mois» (3 meses de contrato + 9); circuito de Lyon «lancé il y a six mois».
- Dos réplicas seguidas de Mercier fundidas («Où voulez-vous aller ?» + pregunta sobre montée en compétences → una sola pregunta) y dos de Ana fundidas.
- «Rellené» → «Llené»; «formación/colega formado» → «capacitación/colega capacitado».
- s2: opciones es/en → «Quelle critique Madame Mercier fait-elle à Ana ?» (Elle garde trop de dossiers pour elle. / arrive en retard aux réunions / dépasse le budget des groupes).

## Hechos del reparto confirmados

- Ana trabaja en la agencia de Madame Mercier como chargée de projet (encargada de proyectos) con un contrato de tres meses; se postula al puesto de cheffe de projet (jefa de proyectos) con contrato indefinido, que es un ascenso, ante un jurado de tres personas (Mercier, Monsieur Faure y la responsable de recursos humanos, sin nombre; vous), y es elegida (c22, c24). / Ana works at Madame Mercier’s agency as a chargée de projet (project coordinator) on a three-month contract; she applies for the permanent cheffe de projet (project manager) post, a promotion, before a three-person panel (Mercier, Monsieur Faure and the unnamed head of human resources; vous), and is chosen (c22, c24).
- Monsieur Faure es el responsable de contratación (le responsable du recrutement) de la agencia; Ana lo trata de vous (c21, c22). / Monsieur Faure is the agency’s head of recruitment; Ana addresses him with vous (c21, c22).
- Thomas es candidato a coordinador de eventos de la agencia (antes coordinador en una agencia de viajes); pasó la preselección y el jurado decide al día siguiente entre tres candidatos; Ana asiste como futura colega (c21). / Thomas is a candidate for event coordinator at the agency (previously a coordinator at a travel agency); he passed the shortlisting and the panel decides the next day among three candidates; Ana attends as a future colleague (c21).
- Bastien (no es Julien, el colega de reservas) es candidato a guía de circuitos a pie: estudió historia en Lyon, fue seis años guía de museo y desde hace dos años hace visitas a pie; su abuelo era guía en Lyon; Ana dirige su entrevista por primera vez y Mercier observa (c23). / Bastien (not Julien, the reservations colleague) is a candidate for walking-tour guide: he studied history in Lyon, was a museum guide for six years and has done walking tours for two years; his grandfather was a guide in Lyon; Ana leads his interview for the first time and Mercier observes (c23).
- En el hotel Ana gestionó tres ferias sin retraso y coordinó un equipo; su punto débil es querer controlarlo todo (delegar); ya propuso tres nuevos recorridos a pie por los mercados de París (dos reservados) y dirige la reunión de equipo de la agencia (c22). / At the hotel Ana managed three trade fairs without delay and coordinated a team; her weakness is wanting to control everything (delegating); she has already proposed three new walking routes around the Paris markets (two booked) and leads the agency’s team meeting (c22).
- Contrato de Ana como cheffe de projet (c24): 40 000 € brutos anuales (pidió 40 000–44 000; Mercier ofreció 38 000) + 10 % variable; 2 días de teletrabajo tras el período de prueba; período de prueba de 6 meses (de 4) a cambio de una entrevista de evolución a los 6 meses; capacitación de 3 días en gestión de proyectos; mutuelle pagada al 60 % por la agencia; tickets-restaurant de 9 €/día (la mitad la agencia); 10 RTT al año; cláusula de no competencia de un año (Ana pide 6 meses; la revisa el servicio jurídico); Mercier envía el contrato el viernes. / Ana’s contract as cheffe de projet (c24): €40,000 gross per year (she asked 40,000–44,000; Mercier offered 38,000) + 10% variable; 2 remote days after the trial period; 6-month trial period (from 4) in return for an evolution interview after 6 months; a 3-day project management course; mutuelle 60% paid by the agency; meal vouchers of €9/day (half paid by the agency); 10 RTT days a year; a one-year non-compete clause (Ana asks for 6 months; legal department to review); Mercier sends the contract on Friday.
- Entrevista anual (c25): Ana lleva un año en la agencia (nueve meses como jefa de proyectos); tres objetivos: circuito de Lyon lanzado hace seis meses (420 viajeros, 92 % de satisfacción), presupuesto de los grupos 3 % por debajo, y capacitación de 1 de 2 colegas; la crítica de Mercier es que se queda con demasiados expedientes; Ana pide evolucionar a responsable de programa (programa para América Latina, equipo de tres) y una capacitación de 5 días en management en el plan de septiembre; la promoción interna no llegará antes del año próximo; objetivos del año siguiente: segundo circuito para América Latina, satisfacción superior al 90 % y dos colegas capacitados; Ana propone confiar tres expedientes completos antes de diciembre; balance en enero. / Annual review (c25): Ana has been at the agency a year (nine months as project manager); three goals: the Lyon circuit launched six months ago (420 travelers, 92% satisfaction), groups’ budget 3% under, and training 1 of 2 colleagues; Mercier’s criticism is that she keeps too many files; Ana asks to move toward program manager (Latin America program, team of three) and a 5-day management course in the September plan; internal promotion not before next year; next year’s goals: a second Latin America circuit, satisfaction above 90% and two colleagues trained; Ana proposes handing three complete files over before December; review in January.

## Para el coordinador

- **palabrasLibres** (`curso.json`): añadir **Thomas, Faure, Bastien** (Mercier y Julien ya están). Hoy se aceptan dentro del bloque porque salen en ejemplos/tablas; un bloque posterior que los use necesita que estén en la lista.
- **Ficha c23** (`curriculo/fr/n9.json`): `situacion.texto` nombra «Julien»; cambiar a «Bastien».
- Ninguna palabra francesa retirada la usa un bloque posterior comprobado (n9-b06…b09 validan con 0 errores); se retiraron «permis» y la frase «Thomas passe l’entretien devant…» (palabras ya conocidas por otras vías). n10 no se pudo validar en cadena (sus bloques anteriores no están completos).

## Sin resolver (no bloquea)

- **Cargos en es de B1–B4 y de la ficha/nota del nivel:** c03, c09 y c11 (y el nota de N9) traducen «chargée de projet» como «jefa de proyecto(s)». En B5 se distingue chargée = «encargada de proyectos» y cheffe = «jefa de proyectos» (el ascenso de c22/c24). Conviene armonizar las traducciones es/en de c03/c09/c11 y la nota del nivel («jefa de proyectos (chargée de projet)» → «encargada de proyectos»; la promoción posterior).
- **Calendario de N9:** c10 habla de un cóctel de fin de año, c11 de «depuis le mois de mars» y c16 del planning de marzo; con un contrato de tres meses y un año hasta la entrevista anual no se puede fijar mes por mes. Por eso se quitaron los nombres de mes en c22/c24 («à la fin du mois», «dès le mois prochain») y c25 usa tiempos relativos («depuis neuf mois», «il y a six mois»). Si se fija el calendario, solo hay que ajustar esas frases y «dès septembre / avant décembre / janvier» de c25.
- Los ítems `s2` de comprensión ya no son la pregunta de gramática en español de las fichas (formato `escribir`); ahora comprueban lectura y usan opciones en francés (calibración 14). Si se prefiere la reflexión metalingüística, solo puede ir en un `escribir` abierto, que no puntúa.
