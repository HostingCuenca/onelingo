# Revisión de N6 · B5 (fr.n6.c21–c25)

GO

Revisado por un agente distinto del autor. Validación final: `python3 tools/validar_ruta.py fr --borrador n6-b01…n6-b05` → 0 errores (modo de vocabulario estricto activo). Los borradores n5-b01…b10 ya están integrados en `assets/contenido/fr/ruta/` (encadenarlos con `--borrador` da «id de unidad duplicado»), así que se quitaron de la lista. Encadenando también n6-b06…n6-b10 siguen siendo 0 errores: ninguna palabra que quité o cambié la usa un bloque posterior. `python3 tools/curriculo/validar_plan.py fr` → 0 errores y ningún «título de la unidad difiere» para fr.n6.c21–c25.

Comprobado sin cambios necesarios: cada clase enseña lo que dice su ficha (título, objetivo, gramática, introduce/recicla, vocabulario de 8–9 palabras con todas sus tarjetas visibles, tarea) y contiene los ejercicios del plan (mismo formato y clave, redacción pulida); nada de clases posteriores; situación de 384–428 palabras (rango N5–N7: 300–500) coherente con sus ítems de comprensión; hablantes con nombre o papel/documento en francés («La note», «L’article», como en N5); tipografía (U+202F antes de ? ! : ; y dentro de « », apóstrofo ’; revisada también tras mis cambios); guías de pronunciación (ö y ü definidas en la primera tarjeta donde aparecen en cada clase, nasales como «en», «sh»); español neutro de América (tú) e inglés americano (sin piso/móvil/billete…); los `escribir` abiertos no cuentan.

Cada clase tiene **5 ítems puntuables** en la evaluación (más 1 `escribir` abierto que no puntúa) y ≥ 4 formatos entre ellos:

| Clase | Puntuables | Formatos |
|---|---|---|
| c21 | e1–e5 | completar, elegir, ordenar, escuchar |
| c22 | e1–e5 | completar, elegir, escuchar, ordenar |
| c23 | e1–e5 | elegir, completar, escuchar, ordenar |
| c24 | e1–e5 | elegir, completar, escuchar, relacionar, ordenar |
| c25 | e1–e5 | completar, relacionar, escuchar, elegir, ordenar |

## Palabras que solo se enseñaban en celdas de tabla

Revisé una por una las palabras nuevas que solo aparecen en tablas (c21: slogans, supporte, galerie, articles; c22: méfiants, fidèle, image; c23: rêvé, craqué, tenté, résister, interpelle, rhétorique; c24: collection, omettre, s’adresser, annonce, nominale, verbe, urgence, analyse; c25: connectée, argent, jeté, expression, familière, soutenue). Todas se muestran en una frase completa con su sentido en la columna «Sentido» (es/en), salvo los casos de abajo, que eran celdas solo para el validador y se corrigieron.

## Correcciones (clase, ítem: antes → después)

**c21**
- Tabla p4 (fila «à + lugar → y»), traducción es: «Esta galería, voy cada sábado.» → «Esta galería, voy allí todos los sábados.»
- Ejemplo «Cet achat impulsif, je le regrette» (es): «…me arrepiento.» (sin pronombre) → «Esa compra impulsiva, me arrepiento de ella.»
- e2, feedback es: «Soldes es plural femenino» → «Soldes es plural» (les soldes es masculino plural).
- g2: se quitó `aceptadas` «On en profite, les promos.»: la consigna fija la dislocación a la izquierda y la primera ficha lleva mayúscula.
- Diálogo, Emma: «Les offres, elles sont partout» (dislocación del sujeto, no enseñada) → «Des offres, il y en a partout» (es/en ajustados), que sí es el patrón de la clase.
- Diálogo: dos intervenciones seguidas de Léa fusionadas en una («…je ne le dépasse jamais. Mais on peut acheter une seule chose utile. Moi, je cherche un manteau.»).

**c22**
- **Tabla p5 «El pronombre detrás del verbo»**: tenía celdas sueltas «est-», «-ce», «sont-», «-ils», «a-», «-t-elle», «devient-», «-on» que solo existían para que el validador aceptara los huecos «___-ce», «___-ils»… Se reemplazó por una tabla de formas completas con ejemplo y sentido (est-ce, sont-ils, est-elle, a-t-elle, devient-on) y se rediseñaron los huecos para que pidan la forma completa: g1 «Sans doute ___ la meilleure offre.» → est-ce (opciones est-ce / c’est / est-il); g2 «Peut-être ___ la bonne solution.» → est-ce; g4 «Aussi ___ de plus en plus méfiants. (être + ils)» → sont-ils; i1 «Ainsi ___ un client fidèle. (devenir + on)» → devient-on; s2 «Aussi la marque ___ devenue célèbre en quelques mois. (être + elle)» → est-elle; e1 «Sans doute ___ l’image de marque qui plaît. (être + ce)» → est-ce. `aceptadas` con la variante sin guion («est ce», «sont ils»…); pistas y feedback ajustados (es/en). Misma clave y formato que el plan.
- Explicación p1 (es/en): «cuatro adverbios… piden invertir» → «suelen llevar la inversión» (con sans doute / peut-être la inversión es opcional; el texto ya explica que en la lengua oral no se invierte).
- g1, pista (en): «c’est» con comillas españolas → comillas inglesas.
- g5 (ordenar): `aceptadas` + «Jamais une marque n’avait fait autant parler d’elle.» (autant fait / fait autant, ambos naturales); pista ajustada.
- e2: la consigna («adverbio que da sentido de consecuencia») admitía también Alors/Donc → «Elige el adverbio que permite la inversión y da sentido de consecuencia»; distractores Alors / Ainsi / **Mais** (Donc → Mais).
- Situación: s1 citaba «Sans doute est-ce le produit phare de la marque.», que no estaba en la nota → se añadió a la nota («Sans doute est-ce le produit phare de la marque : le manteau en laine se vend toute l’année.»; es/en). La nota ahora es un borrador con dos frases demasiado orales («Peut-être que c’est son image de marque», «Sans doute que c’est la vraie raison…») y cuatro inversiones, como dice Ana («trois ou quatre»); antes la nota ya estaba en registro escrito y la crítica de Ana no coincidía. Contexto es/en ajustado.
- Diálogo Ana/Hugo reordenado: Hugo preguntaba por «aussi» y, sin respuesta, preguntaba por el logo. Ahora: Ana (nota) → Hugo («Et pour « aussi » ?») → Ana (aussi) → Hugo (logo) → Ana (profesor) → Hugo (introducción) → Ana → Hugo. «Ainsi, je garde le même registre» (ainsi sin inversión, justo tras enseñar que ainsi la lleva) → «Je garde le même registre…»; «Dans la première version» → «Dans la première partie» (es/en).

**c23**
- Error frecuente 3: «Qui a jamais rêvé… ?» no es incorrecto en francés (jamais positivo = «alguna vez», registro literario) y la explicación («la negación es obligatoria») era falsa → «Qui n’a pas jamais rêvé de partir ?» → «Qui n’a jamais rêvé de partir ?» (jamais ya es el segundo elemento de la negación; es/en).
- Tabla p4, columna «Fórmula»: celdas `texto` con español («Qui n’a jamais + participio»…) que el audio leería en francés → celdas `apoyo` (es/en). Fila «Ne serait-il pas + adjetivo» (temps es un sustantivo) → «Ne serait-il pas temps de + infinitivo».
- Diálogo: «dans notre téléphone» → «sur notre téléphone»; dos pares de intervenciones seguidas del mismo hablante fusionadas (Léa «Pour la fin…» + «Et si le public…»; Hugo «Exactement…» + «Et un slogan…»).

**c24**
- Error frecuente 1: «Prix cassé !» no es incorrecto (hay un precio cassé) → «Prix cassé sur toute la collection !» → «Prix cassés sur toute la collection !» (varios artículos = varios precios; explicación es/en).
- Tabla p7: la fila «reconnaître» no usaba el verbo (era la fila para «phrase nominale / sans verbe») → título «Palabras para analizar» / «Words for analyzing», fila «la phrase nominale» con ese ejemplo, y fila «reconnaître» con «On reconnaît une phrase nominale : elle n’a pas de verbe.» La fila «analyser» usaba solo el sustantivo → «Pour analyser une annonce, je fais une analyse en trois points.» (se mantienen las palabras que usa el diálogo).
- Ejemplo y diálogo (es): «precios suaves» → «precios amigables».
- e2: la opción «Livraison» también completaba bien («Livraison limitée : profitez-en !») → distractores Offre / Prix / **Satisfait**.
- e5 (ordenar): `aceptadas` + «Profitez-en ! Offre limitée !».
- Diálogo: dos pares de intervenciones seguidas de Ana fusionados; el orden de los consejos queda coherente.

**c25**
- g1, pista: «el que se parece al español/inglés» (en inglés es falso: an arm and a leg) → «Empieza por el que menciona partes del cuerpo (yeux, tête): habla de un precio» (es/en).
- Explicación p2 (es): «y en inglés se dice «hotcakes»» (fuera de lugar en el texto en español) → ««Vender como pan caliente» es se vendre comme des petits pains en francés (los panecillos, no el pan caliente)».
- i4: `aceptadas` + «L’an dernier, cette appli a fait un flop.»
- Diálogo: el «Pas pour moi ! Le café, je le déteste» de Emma respondía a Hugo pero iba después de la intervención de Léa → reordenado (Hugo, Emma, Léa).

## Comprobaciones de reparto

- Hugo hace una maestría en París desde septiembre (N4 c02, N5 b02 y b06–b07 «mon master», N6 b01–b04 «mon mémoire»). En este bloque su máster aparece como seminario (c22), charla (c23) y mémoire (c25: «dans un mémoire, je dirais plutôt…»): coherente. Ningún ítem lo da por trabajando en una empresa ni contradice que rechazó el puesto de Lyon (N5 b02); «mon professeur» queda sin nombre (Monsieur Martin es el profesor de Ana, no el de Hugo).
- Tratamientos: Emma, Léa y Hugo se tutean (c21, c25); Hugo y Ana se tutean (c22, c23, c24). Ana no sale en c21 ni c25 y no se le atribuye nada.
- Emma odia el café y toma té; Hugo lo adora (N1 c09–c10): se respeta en c21 y c25.
- «Maison Lumière» es una marca ficticia; no choca con ninguna marca del reparto.

## Hechos del reparto confirmados

- Un sábado de rebajas, Emma, Léa y Hugo recorren una galería comercial (se tutean); Hugo hace una lista antes de ir a las rebajas y su punto débil es la compra impulsiva; Emma compró un bolso tras ver un eslogan en su celular; Léa tiene seis tarjetas de fidelidad y no usa ninguna, anota su presupuesto cada semana / One sale Saturday, Emma, Léa and Hugo walk through a shopping mall (they use tu); Hugo makes a list before the sales and impulse buying is his weak spot; Emma bought a bag after seeing a slogan on her phone; Léa has six loyalty cards and uses none, and writes down her budget every week (c21).
- Léa busca un abrigo y Emma mira desde hace un mes un abrigo gris; Hugo prefiere un café, Emma un té / Léa is looking for a coat and Emma has been eyeing a gray coat for a month; Hugo has a coffee, Emma a tea (c21).
- Hugo escribe, para un seminario de su máster, una nota de análisis sobre una marca de ropa ficticia, «Maison Lumière»; Ana (se tutean) le corrige el registro y él la envía al día siguiente a su profesor (sin nombre) / For a seminar in his master’s, Hugo writes an analysis note on a fictional clothing brand, “Maison Lumière”; Ana (they use tu) corrects the register and he sends it to his professor (unnamed) the next day (c22).
- Hugo ensaya delante de Ana y Léa el gancho de una charla de su máster sobre consumo y publicidad; el público será su profesor y tres estudiantes de otro máster; el año pasado compró unos audífonos demasiado caros y los usó una sola vez / In front of Ana and Léa, Hugo rehearses the hook of a master’s talk on consumption and advertising; the audience will be his professor and three students from another master’s program; last year he bought headphones that were too expensive and used them only once (c23).
- Hugo y Ana analizan tres anuncios: un plan de celular («5 euros al mes» durante tres meses y luego 19), una tienda de ropa (envío gratis desde 50 euros) y una campaña de viajes a Marsella (fin de semana desde 99 euros); Hugo escribe dos eslóganes («Café frais, prix doux !» y «Livraison offerte, profitez-en !») / Hugo and Ana analyze three ads: a phone plan (5 euros a month for three months, then 19), a clothing store (free delivery from 50 euros) and a travel campaign to Marseille (weekend from 99 euros); Hugo writes two slogans (“Café frais, prix doux !” and “Livraison offerte, profitez-en !”) (c24).
- Emma y Léa leen un artículo de tendencias; Léa quiere desde hace un mes una chaqueta de lana y tiene tres pares de zapatos blancos; Emma duda en comprar un reloj inteligente que cuesta mucho; Hugo no usaría expresiones familiares en su mémoire y su «tendencia» es el café / Emma and Léa read a trends article; Léa has wanted a wool jacket for a month and owns three pairs of white shoes; Emma hesitates over an expensive smartwatch; Hugo would not use informal idioms in his mémoire and his “trend” is coffee (c25).

## Sin resolver

- Nada bloqueante. Avisos para otros bloques: (1) el único «Hugo trabaja en una empresa» posible está fuera de este bloque (N6 b03 c15 habla de una pasantía de Hugo); b05 no lo toca. (2) En c22 y c25 la nota/artículo se muestra como varios «hablantes» seguidos («La note», «L’article»): es la convención de N5 para documentos. (3) La palabra «analyse», «reconnaître», «phrase nominale» y las formas «est-ce / sont-ils / est-elle / a-t-elle / devient-on» quedan enseñadas en tablas con sentido; no se quitó ninguna palabra francesa que pudiera usar un bloque posterior (solo desaparecieron las celdas de fragmento «-ce», «-ils», «-elle», «-on», «est-», «sont-», «a-», «devient-», que ningún bloque posterior usa).
