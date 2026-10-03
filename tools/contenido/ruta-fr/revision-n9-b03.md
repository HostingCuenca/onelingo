# Revisión N9 · B3 (fr.n9.c11–c15)

GO

Validación: `validar_ruta.py fr --borrador n9-b01 n9-b02 n9-b03` da 0 errores (los borradores n8-b01…b10 ya están integrados en `assets/contenido/fr/ruta/`; incluirlos da «id de unidad duplicado», así que se quitan). `validar_plan.py fr`: 0 errores y ningún «título de la unidad difiere» para fr.n9.c11–c15.

Comprobado: las 5 clases traen vocabulario, títulos, objetivos y `introduce` iguales a las fichas; los ejercicios del plan (mismo formato, orden y clave) en guiada, independiente, situación y evaluación; nada de clases posteriores (`recicla` solo con puntos ya introducidos); tipografía francesa (U+202F antes de : ; ? !, ’, « » con U+202F) sin fallos; situaciones de 400–450 palabras (conteo por espacios); cada evaluación con 5 ítems puntuables en 5 formatos (escuchar, elegir/completar, ordenar, relacionar…), y el `escribir` de tarea es abierto y no cuenta; los `escribir` abiertos de situación («Responde en francés…») cumplen `minimoPalabras` con su modelo; tablas «Para leer» de 3–9 filas; todos los hablantes son nombres o papeles (Ana, Karim, Hugo, Madame Mercier, Le client); tuteo/vouvoiement correcto (Ana–Karim, Ana–Mercier, Ana–clientes: vous; Ana–Hugo: tu); español neutro (costos, estación, autobús, credencial) e inglés americano («second floor» para premier étage).

## Cambios (clase, ítem: antes → después)

### c11
- Cifras de Lyon: presupuesto total «12 400 euros» → «14 400 euros» (diálogo fr/es/en, dos veces). Motivo: c13 fija 480 € por persona y c15 un grupo de 30 personas (cena de salida para treinta): 30 × 480 = 14 400.
- Diálogo, Karim: «la décision que l’on vous demande» → «la décision que vous demandez» (el «vous» era ambiguo); es: «que se pide» → «que usted pide».
- Pronunciación de «le message clé»: faltaba definir ö en su primera aparición (se definía solo en la tarjeta 6) → se añade «ö = eu francesa (labios de «o», lengua de «e»)».
- e3 (completar «Objet : ___ du programme…»): `aceptadas` + «validation», «la validation» (también es un sustantivo defendible; la respuesta prevista sigue siendo «révision»).

### c12
- Diálogo: el contexto decía que Hugo enseña el correo de Karim y Ana lo aligera y lo explica, pero el diálogo lo hacía al revés (Ana lo enseñaba, Hugo lo aligeraba). Se intercambian los hablantes Ana/Hugo en las 8 réplicas para seguir la ficha (Ana aligera y explica; Hugo pregunta y comenta). Los textos no cambian.
- «Karim écrit très bien en cuisine» (giro que no existe) → «Karim cuisine très bien» (es «cocina muy bien»; en «cooks very well»).
- Pronunciación de «le pléonasme»: se define ö en su primera aparición (antes solo en la tarjeta 5).

### c13
- Cifras: «120 euros par personne» (tabla «Las cuatro expresiones» e i1) → «480 euros par personne», el precio del viaje a Lyon que usan los ejemplos, el correo y el diálogo.
- e3 (elegir el orden jerárquico): «D’abord le budget, puis le transport, puis les badges» → «D’abord le transport, puis le budget, puis les badges», para no contradecir el correo de Ana ni s1 (la priorité absolue es el transporte). Las opciones no cambian.
- e1 (escuchar): pregunta «Dans quel cas ?» → «Quand faut-il faire un plan B ?» (la original era ambigua con las opciones «Toujours / Jamais»).
- Diálogo, Karim: «dit que vous changez les dates» → «dit que l’on change les dates» (el correo es para el equipo, no para Ana); es y en igual.
- Pronunciación de «le cas échéant»: se define ö en su primera aparición.

### c14
- «Monsieur Laurent» (nombre nuevo) se maneja con un papel: hablante «Monsieur Laurent» → «Le client» (7 réplicas) y el nombre desaparece del francés: tabla «Para leer» («Je comprends votre déception, Monsieur.» y «Le client est très déçu.»), «Bonjour Monsieur.», «… Monsieur.» y la primera réplica («je suis un des clients inscrits»). Antes el nombre solo «estaba enseñado» porque salía en frases de la tabla. El nombre sigue en el `contexto` es/en (texto de apoyo, no se valida). No hace falta tocar `curso.json`.
- Réplica de Ana: «vous êtes le premier client prévenu, Monsieur Laurent» (contradecía el correo enviado a todos esa mañana) → «il a été décidé de prévenir tous les clients le jour même» (es y en igual).
- Género: el cliente dice «Merci d’avoir été clair» a Ana → «claire» (es «clara»).
- es: «Bonne journée» estaba traducido «Buenas tardes» → «Que tenga un buen día».
- Pronunciación de «la suppression d’un service»: «dun» → «den» (la nasal un se escribe «en» según la calibración 6).

### c15
- Réplica de Ana: «L’éclairage sur le coût réel du voyage est meilleur avec l’hôtel central» (uso forzado de «éclairage», sin lógica) → «Mais l’éclairage change si l’on regarde le coût réel : il faut ajouter le transport jusqu’à l’hôtel.» (es y en igual). Da el argumento real contra el hôtel du parc (15 % más barato, pero lejos de la estación).
- e6 (tarea): el modelo decía «Objet : voyage Lyon…» aunque la consigna pide resumir **otro** viaje de grupo → «Objet : voyage de groupe — point de situation»; y «Décision à prendre avant vendredi» (se elige entre salir el jueves o el viernes) → «avant mardi».

### Coherencia del viaje de grupo a Lyon (c11–c15)
- Presupuesto total 14 400 € = 30 personas × 480 € (c11, c13, c15); cena de salida para treinta personas en el restaurante de Karim (c15).
- Hôtel du centre/«central» retiene las fechas hasta el viernes (c11) y la decisión se toma antes del viernes (c15); en c11 Ana ya había comparado dos hoteles (c15: central y du parc).
- Transporte aún sin confirmar y prioridad absoluta (c11: «je dois encore parler au transporteur»; c13; c15: el car está libre jueves y viernes, precio tras el lunes).
- Guía: tuvo un problema y se encontró otro (c11) → reservado (c15). Presupuesto a validar por Madame Mercier antes del jueves (c11, c13).

Palabras francesas quitadas o renombradas que usen bloques posteriores: solo «Laurent» (no aparece en ningún otro borrador ni en los publicados). No se quitó ninguna palabra enseñada de los pasos de enseñanza; «cuisine» y «jour même» ya estaban enseñadas.

## Hechos del reparto confirmados

- Ana, como chargée de projet en la agencia de Madame Mercier (vous), prepara el viaje de grupo a Lyon: 30 personas, 480 € por persona (precio indicativo), presupuesto total de 14 400 € que Mercier debe validar antes del jueves (c11, c13). / Ana, as project manager at Madame Mercier’s agency (vous), is preparing the Lyon group trip: 30 people, 480 euros per person (guide price), a total budget of 14,400 euros that Mercier must approve before Thursday (c11, c13).
- Detalles del viaje a Lyon (c11, c15): el hotel del centro retiene las habitaciones hasta el viernes; hay un hotel del parque 15 % más barato pero lejos de la estación; tarifa de grupo del hotel confirmada el 3 de marzo (110 € la noche); el transporte (autobús) está libre jueves y viernes pero sin precio confirmado; el guía está reservado (tras cambiar de guía); el seguro está por firmar; la cena de salida (30 personas) será en el restaurante de Karim; Madame Mercier elige el hotel central. / Lyon trip details (c11, c15): the downtown hotel holds the rooms until Friday; a park hotel is 15% cheaper but far from the station; the group rate was confirmed on March 3 (110 euros a night); the bus is free Thursday and Friday but the price is not confirmed; the guide is booked (after switching guides); the insurance is still to be signed; the departure dinner (30 people) will be at Karim’s restaurant; Madame Mercier chooses the central hotel.
- Karim, el chef, revisa como amigo los borradores de Ana (escribe cada semana a sus proveedores); Ana y Karim se tratan de vous (c11, c13). / Karim, the chef, reviews Ana’s drafts as a friend (he writes to his suppliers every week); Ana and Karim use vous (c11, c13).
- Hugo, en el servicio de patrimonio de la alcaldía, organiza una visita con 40 inscritos y un bufé que prepara Karim; Hugo y Ana se tutean y Ana aligera el correo redundante de Karim (c12). / Hugo, at the city heritage department, organizes a visit with 40 registered guests and a buffet prepared by Karim; Hugo and Ana use tu, and Ana tightens Karim’s redundant email (c12).
- Ana envía a su equipo un correo semanal con cinco tareas jerarquizadas: transporte (prioridad absoluta), presupuesto con Madame Mercier, hotel, programa a los clientes y credenciales; la reunión del viernes se mantiene (c13). / Ana sends her team a weekly email with five ranked tasks: transport (top priority), budget with Madame Mercier, hotel, program to the clients and badges; Friday’s meeting stays (c13).
- La agencia suprime el circuito «Alpes en automne» (12 inscritos, mínimo 20; entra en vigor el 1 de marzo; los clientes eligen hasta el 15 de febrero entre reembolso íntegro u otro circuito al mismo precio). Un cliente descontento, Monsieur Laurent (en francés solo «Le client»), reservó hace un año para ir con su hijo y elige el circuito de primavera; Ana lo trata de vous (c14). / The agency cancels the “Alpes en automne” tour (12 registered, minimum 20; effective March 1; clients choose by February 15 between a full refund or another tour at the same price). A disappointed client, Monsieur Laurent (in French only “Le client”), booked a year ago to go with his son and takes the spring tour; Ana addresses him with vous (c14).
- Ana trata de vous a Madame Mercier, a Karim y a los clientes, y de tu a Hugo (c11–c15). / Ana uses vous with Madame Mercier, Karim and clients, and tu with Hugo (c11–c15).

## Sin resolver

- Tareas de la ficha vs. ítems: c11 e6 pide reescribir un borrador de ≈ 90 palabras en ≈ 80 (la ficha decía 250 → 80) y c12 e6 reducir ≈ 75 palabras a ≈ 65 (la ficha, 200 → 100). Se dejan así por viabilidad en un ejercicio de la app; son abiertos y no puntúan. Si se quiere el tamaño original, el borrador de partida tendría que reescribirse.
- Calendario: c14 entra en vigor el 1 de marzo (anuncio en febrero) y c11/c15 se fechan en marzo. Las clases se leen por separado y no se dice el año, pero no se debe presentar c14 como anterior a c15 en una misma línea del tiempo.
- La situación de c13 mide justo 400 palabras (conteo por espacios, límite inferior de «Por nivel»); cualquier recorte posterior la dejaría corta.
- Si el coordinador prefiere que «Monsieur Laurent» aparezca en el francés del diálogo, habría que añadir «Laurent» a `palabrasLibres` de `curso.json` (hoy no hace falta).
- n9-b04 menciona otro viaje a Lyon (queja de un cliente); no está en mi alcance, pero conviene que su revisor lo compare con las cifras de arriba.
