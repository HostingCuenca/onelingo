# Revisión N5 · B1 (fr.n5.c01–c05) — «Un nouveau pays»

GO

Revisor distinto del autor. Contrastado con las 5 fichas de `curriculo/fr/n5.json` (incl. plan de ejercicios), `personajes` / `hechosDelReparto` de N1–N4, `ENCARGO_RUTA_FR.md` (Por nivel N5 + calibración 1–10) y `ESQUEMA_CONTENIDO.md`.

Validación (solo `n5-b01.json`: N1–N4 ya están integrados en `assets/contenido/fr/ruta/`, por lo que se quitaron los `n4-b*.json` de `--borrador`):
- `python3 tools/validar_ruta.py fr --borrador tools/contenido/ruta-fr/n5-b01.json` → 0 errores.
- `python3 tools/curriculo/validar_plan.py fr` → 0 errores; ningún «título de la unidad difiere» para fr.n5.c01–c05.
- Barrido de tipografía (U+202F antes de ? ! : ;, apóstrofo ’, sin ' rectos) y de léxico es/en (sin «piso», «móvil», «billete», «flat», etc.): limpio.

## Correcciones

### Decisión del coordinador (reparto)
- **c03 · situación (Emma y Ana)**: el comprobante de domicilio lo pide a **Monsieur Roux**, no a Madame Dubois. Antes: «Demande un papier à Madame Dubois : c’est elle, ta propriétaire» → ahora «Demande un papier à Monsieur Roux : c’est lui, ton propriétaire»; y en la última intervención de Ana «Madame Dubois est très gentille» → «Monsieur Roux peut me donner un papier cette semana» (también corregidas las traducciones es/en). Se evitó «très gentil» porque en N4 c13–c14 Monsieur Roux tarda en responder.
- **c01 · orden de hechos (hotel → escuela) incompatible con N1–N2**: en N1 Ana llega en septiembre y se inscribe en la escuela en c20 (tres meses de estudio al final de N1); el trabajo en la recepción del hotel empieza en N2 (enero), y N4 dice que lleva dos años en el hotel con un CDD y luego un CDI. La ficha y el borrador contaban lo contrario («después de conseguir el puesto en el hotel se inscribió en la escuela»). Cambios:
  - Diálogo, línea de Ana: «Après avoir trouvé un logement, j’ai cherché du travail. Après m’être installée dans le quartier, j’ai trouvé un poste à la réception d’un hôtel. Ensuite, je me suis inscrite à l’école de langues…» → «Après avoir trouvé un logement et après m’être installée dans le quartier, je me suis inscrite à l’école de langues pour améliorer mon français. Quelques mois plus tard, après avoir cherché du travail pendant plusieurs semaines, j’ai trouvé un poste à la réception d’un hôtel.» (es/en actualizados; el texto sigue con 333 palabras.)
  - Comprensión s1: «Juste après avoir trouvé un logement, Ana… a cherché du travail» → «Après s’être installée dans le quartier, Ana… s’est inscrite à l’école de langues» (opciones: a fait ses valises / s’est inscrite à l’école de langues / est rentrée à Quito; respuesta índice 1). Esto cambia la pregunta del plan de ejercicios de c01 (misma clave y formato): conviene actualizar la ficha de c01 (texto de la situación y pregunta 1) para que el plan no contradiga la ruta.
  - Comprensión s2: «Au début, Ana a surtout ressenti…» (opción «la joie» ambigua, porque antes de partir Ana estaba «très heureuse») → «Après être arrivée à Paris, qu’est-ce qu’Ana a tout de suite ressenti ?» (respuesta única: le dépaysement).
- **c02 · situación**: «Après mon installation, j’ai commencé la recherche d’un travail» → «Quelques mois après mon installation, …» (es/en igual), para que la búsqueda de empleo siga a la escuela y al curso de francés (coherente con c01 y con N2).
- **c04 · situación**: «Au début, bien que j’aie un travail et des cours» → «bien que j’aie des cours tous les jours» (es/en): al llegar, en septiembre, Ana aún no tenía el empleo del hotel; y el primer invierno es antes de enero.

### Francés y explicaciones
- **c01 · explicación 1**: «✗ après faire (se oye en el habla, pero en un texto se corrige a après avoir fait)» → «✗ après faire es incorrecto; hace falta après avoir fait» (es/en). «Après faire» no es una forma del habla corriente; la nota inducía a error.
- **c01 · explicación 2**: «nous être installés» → «nous être installé(e)s» (es/en).
- **c01 · tabla «La concordancia con être»**: la fila «Yo» tenía el pronominal en la columna «être + participio» (m’être installé(e) / m’être adapté(e)). Ahora: «être arrivé(e)» / «m’être installé(e)». La fila «Ellas (partir)» queda «être parties» / «s’être adaptées».
- **c02 · erroresFrecuentes 2**: la lista de «nombres en -tion que elidan» incluía «la recherche» (no es -tion y no elide) → «l’installation, l’adaptation, l’intégration» (es/en, con «ante vocal»).
- **c02 · tabla «Para leer el blog»**: «il a duré» / «Il a duré plusieurs semaines.» (el texto usa «elle a duré») → «elle a duré» / «La recherche a duré plusieurs semaines.».
- **c03 · explicación 3**: «el participio vu no cambia nunca» → «en la norma estándar el participio vu no cambia delante de un infinitivo» (es/en; la concordancia con se voir es discutida en algunos manuales).
- **c04 · tabla «Los subjuntivos de bien que»**: fila «être» duplicada con la de «être (la vie)»; la primera queda «que ce soit».

### Sonido (guías es/en)
- **c01 · le dépaysement**: «lö dé-pé-i-ze-man» → «lö dé-pé-iz-man» (la e es muda; el inglés ya era correcto).
- **c03 · le titre de séjour**: «sé-shür» con «u = ü» → «sé-shur» con «ou = u» (séjour lleva ou, no u; es y en). El resto de guías (ö definida en c01, ü definida en c02 en «le mal du pays», nasales con «en/an/on», j = «sh»/«zh») están bien.

### Ítems (`aceptadas`, órdenes naturales)
- c01 g5: añadido «Elle, après avoir trouvé un logement, a cherché du travail.» c01 e4: añadido «Il, après être arrivé en France, a appris le français.»
- c02 i4: añadido «La recherche d’un travail à Paris par Ana».
- c03 e5 (ordenar): añadido «À la préfecture, le justificatif de domicile a été transmis.»
- c04 e4 (ordenar): añadido «Ana, bien que ce soit difficile, s’adapte.»
- c05 i4: añadidos «Elle parle couramment, ayant vécu dix ans à Paris.» y «Elle, ayant vécu dix ans à Paris, parle couramment.»

## Lo que se comprobó y está bien (sin cambios)
- Cada ficha: título, objetivo, gramática, introduce, recicla, vocabulario (9 palabras de la ficha; c01 añade «le logement», c04 «le climat» y c05 ninguna extra; c02, c03, c04, c05 coinciden) y tarea (versión corta en la evaluación como `abierta`). No hay nada de clases posteriores (condicional pasado en c03 solo como forma de la tabla de la ficha; «même si» mencionado como contraste en c04).
- Plan de ejercicios: los 5 bloques de ejercicios de c01–c05 están en el mismo formato y clave (guiada 5, independiente 4, situación 1–2, evaluación 6–7). Redacción pulida con pistas útiles en guiada y sin pista en independiente.
- Anatomía: explicación, ejemplos (8), vocabulario, tablas (conjugación/forma + «para leer el texto» que enseña las palabras del texto), guiada con `pista`, independiente, situación (314–333 palabras, rango 300–500 de N5) y evaluación con ≥ 5 ítems puntuables en ≥ 3 formatos; el `escribir` abierto (`abierta: true`) no cuenta entre ellos. `erroresFrecuentes` 4 por clase. Todos los formatos aparecen en el bloque.
- Hablantes: nombres o papeles franceses («Chloé», «Ana», «Emma», «La préfecture», «La rédaction»).
- Glosas de `relacionar` distintas; respuestas únicas (se revisaron las opciones de elegir/escuchar). Español neutro de América (departamento, comprobante, licenciatura, ustedes) e inglés americano.

## Hechos del reparto confirmados
- Ana llegó a París en septiembre con dos maletas, había aprendido un poco de francés en Quito, primero se instaló y se inscribió en la escuela de idiomas (N1 c20), y unos meses más tarde, tras buscar trabajo varias semanas, encontró el puesto en la recepción del hotel (N2) / Ana arrived in Paris in September with two suitcases, had learned a little French in Quito, first settled in and enrolled at the language school (N1 c20), and a few months later, after job hunting for several weeks, found the hotel front-desk job (N2).
- Ana abrió una cuenta bancaria y compró un teléfono francés en sus primeras semanas / Ana opened a bank account and bought a French phone in her first weeks.
- Ana sintió desarraigo al llegar; el teléfono fue lo más difícil (barrera del idioma); la nostalgia fue más fuerte en diciembre; llamaba a su familia cada domingo / Ana felt disoriented on arrival; the phone was the hardest part (language barrier); homesickness was strongest in December; she called her family every Sunday.
- Ana superó el aislamiento de su primer invierno creando una red de amigos a partir del curso de francés (invitó a un café a dos compañeras), saliendo todos los días aunque hiciera frío, y manteniendo rutinas (un café y un parque cada semana) / Ana overcame the isolation of her first winter by building a network of friends from her French course (she invited two classmates for coffee), going out every day despite the cold, and keeping routines (a café and a park each week).
- Ana tiene un permiso de residencia (titre de séjour) en renovación: solicitud recibida el 3 de marzo, expediente en examen, el comprobante de domicilio fue rechazado por tener más de tres meses, debe presentar uno nuevo antes del 30 de abril, y su récépissé vale tres meses; se lo pide a su propietario, Monsieur Roux / Ana has a residence permit (titre de séjour) up for renewal: application received March 3, file under review, her proof of address was refused for being more than three months old, she must submit a new one before April 30, and her récépissé is valid for three months; she asks her landlord, Monsieur Roux.
- Karim se vio rechazar una autorización para su terraza (apertura de temporada) / Karim was refused a permit for his terrace (seasonal opening).
- Hugo terminó su licenciatura y empezó una maestría / Hugo finished his bachelor’s degree and started a master’s.
- Emma vino a París a estudiar (ya lleva tres años en París según N3 c01) y trabaja en el restaurante de Karim / Emma came to Paris to study (she has been in Paris three years per N3 c01) and works at Karim’s restaurant.
- Chloé Bernard nació en Montreal en una familia bilingüe (madre francófona, padre anglófono), habla francés e inglés con fluidez, conserva un acento canadiense, llegó a París por trabajo pensando quedarse un año, trabaja en la escuela desde hace varios años, llama a sus padres cada semana y a veces se reúne con la pequeña diáspora canadiense de París / Chloé Bernard was born in Montréal into a bilingual family (French-speaking mother, English-speaking father), speaks French and English fluently, has kept a Canadian accent, came to Paris for work planning to stay a year, has worked at the school for several years, calls her parents every week and sometimes meets up with the small Canadian diaspora in Paris.

## Pendiente / sin resolver
- Actualizar la ficha de c01 en `curriculo/fr/n5.json` (texto de la situación: escuela antes que hotel; pregunta de comprensión 1) para que el plan coincida con el contenido. Es una decisión del coordinador; no se editó el plan.
- Ninguna palabra francesa retirada o renombrada: no hay impacto en bloques posteriores de N5. Solo cambia la forma de c02 («il a duré» → «elle a duré»), sin efecto fuera de la clase.
