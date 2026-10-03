# Revisión N10 · B8 (fr.n10.c36–c40)

GO

Validación: `validar_bloque.py 10 8` → 0 error(es) del bloque; `validar_plan.py fr` no marca «título de la unidad difiere» para c36–c40.

## Qué se comprobó

- Títulos, objetivos, gramática, `introduce`/`recicla`, vocabulario de las 5 fichas y plan de ejercicios (guiada, independiente, situación, evaluación): todo presente, mismos formatos y claves; nada de clases posteriores (se retiró «ça se fait» de c39, que se introduce en c40).
- Puntos de calibración 13 (los 6 `escribir` abiertos cumplen `minimoPalabras` con su propio modelo), 14 (opciones de comprensión en francés; tablas «Para leer…» con 3–9 filas, sin nombres propios ni celdas sueltas) y 15 (≤ 15 filas por clase).
- Longitud de las situaciones (400–700 palabras): c36 459, c37 407, c38 413, c39 426, c40 438.
- Siglas de c39 (punto 2): CAF, CROUS, PACS, RIB se leen como palabra; SNCF, RATP, APL, CPAM se deletrean. La explicación, la tabla, los ejercicios (g2, e2, e5) y el diálogo son coherentes con esto (el plan decía «l’APL» entre los acrónimos, pero se deletrea: el autor lo trató bien). Género y elisión (la CAF, le CROUS, la RATP, le RIB, l’APL) correctos.
- Vecino recién llegado (punto 1): vive en el edificio de Madame Dubois; Ana lo trata de vous en c39 y c40 (Madame Dubois también, y él a ellas). Sin tuteo en ningún momento del bloque.
- Monsieur Benali (punto 4): solo aparece como etiqueta de hablante en c38 (nunca dentro de un texto francés evaluable), por lo que el validador no exige `palabrasLibres`. No hace falta añadirlo.

## Correcciones (clase, ítem: antes → después)

Tipografía (todo el bloque): el borrador usaba espacio normal antes de ? ! : ; y dentro de « » (0 U+202F). Se convirtió a U+202F en todo el francés y en las citas francesas dentro de textos es/en.

- c36, situación diálogo 18 (Hugo): «Le plombier arrive à huit heures» → «…arrive dans une heure» (el plomero había dicho «dans une heure» a las 7 h 20; incoherencia horaria). ES/EN ajustados.
- c37, vocabulario `v-bidule` y explicación: «el chunche» / «chunche» (regionalismo) → «la cosa» / «cosito».
- c37, situación (diálogo): se eliminó la subtrama incoherente del cargador (la empleada «no lo ve», luego «el conductor lo trajo», «mire sobre la mesa del salón», «el trayecto en taxi guarda la información»). Un solo objeto (el paraguas), final coherente: recoge el paraguas mañana en la oficina; la empleada elogia el método de describir («à quoi il sert, sa forme, sa poignée»).
- c37, situación: «Comment ça s’appelle déjà ?» pasó a la réplica en que Ana busca la palabra (antes lo decía después de que la empleada ya había dicho «parapluie»). Se añadió un breve intercambio sobre la descripción del conductor (casquette, poli) para mantener ≥ 400 palabras sin relleno.
- c37, e6: «tu cartera» → «tu billetera» (cartera es bolso en varios países).
- c38, situación diálogo 9 (Benali): «je préfère toujours poser la question» (contradecía que él se equivocó) → «Vous avez bien fait de poser la question».
- c38, situación diálogos 16–17: el par ilógico («je ne veux pas payer pour mon erreur… avez-vous un compteur pour le détour ?», con ES que decía lo contrario) → Ana: «Je suis désolée pour le détour… Je ne veux pas vous faire perdre de temps.» / Benali: «Ce n’est pas grave, Madame : c’est aussi ma faute. J’aurais dû vérifier l’adresse avant de partir. À deux, nous avons créé un petit quiproquo !»
- c38, g5: audio «Vous m’avez peut-être mal compris ; je n’ai sans doute pas été claire» (la propia tabla dice que señala al otro, y la clave era «sin acusar») → «Je me suis mal exprimée ; je n’ai sans doute pas été claire.»; pista ajustada.
- c38, e1: se quitó `aceptadas: ["exprimé"]` (con «désolée» solo vale «exprimée»; una sola respuesta defendible).
- c39, contexto: «Un vecino de Madame Dubois» → «Un vecino hispanohablante recién llegado al edificio de Madame Dubois» (es/en).
- c39, diálogo 7 (RIB): el «prélèvement automatique» tras enviar el RIB a la CAF (la CAF paga, no cobra) → «avec lui, la CAF verse l’aide sur votre compte».
- c39, diálogos 11–12: Ana explicaba la SNCF y el vecino la preguntaba justo después → se quitó «Et la SNCF, elle, gère les trains».
- c39, diálogos 16–17: lista de «ocho siglas» incluía «carte Vitale» (no es sigla) y dos réplicas seguidas del vecino → una sola réplica con CAF, APL, RIB, CPAM, RATP, SNCF, CROUS, PACS.
- c39, diálogo 20: «Ça se fait» (punto de c40) → «les employés sont là pour ça»; cierre «huit organismes» → «J’ai compris les huit sigles !»; «Pour lundi… avant le dix du mois» (dos plazos) → «avant le dix du mois».
- c40, diálogo 17 (ES): faltaba «¿» en «¿Y se acostumbra venir…?».

## Hechos del reparto confirmados

- El recién llegado hispanohablante (sin nombre, «Le voisin») vive desde hace poco en el edificio de Madame Dubois; Ana lo trata de vous y él a ella (en B9 pasan a tú); es distinto del «voisin du dessous» sin nombre del daño por agua de c36 / The newly arrived Spanish-speaking neighbor (unnamed, “Le voisin”) lives in Madame Dubois’s building; Ana and he use vous (they move to tu in B9); he is distinct from the unnamed “voisin du dessous” of the water-damage scene in c36
- A las 7 h de una mañana, Madame Dubois (3.er piso, vive en el edificio antiguo) sufre una fuga bajo el lavamanos del baño; Ana cierra la llave de paso, Hugo (tú) avisa al administrador (syndic) y Madame Dubois llama al plomero de urgencias y al seguro; el vecino de abajo (vous, sin nombre) tiene una mancha en el techo de la cocina / At 7 a.m., Madame Dubois (third floor, old building) has a leak under the bathroom sink; Ana shuts off the valve, Hugo (tu) alerts the syndic, Madame Dubois calls the emergency plumber and the insurer; the downstairs neighbor (vous, unnamed) has a stain on his kitchen ceiling
- Ana olvidó un paraguas negro con mango de madera en un VTC (de la gare de Lyon a su casa, hacia las 21 h, el conductor sin nombre) y lo recupera al día siguiente en la oficina de objetos perdidos (empleado sin nombre, vous) / Ana left a black umbrella with a wooden handle in a VTC (from the gare de Lyon to her home, about 9 p.m.) and picks it up the next day at the lost-and-found office (unnamed clerk, vous)
- Ana toma un VTC un viernes por la noche con Monsieur Benali (conductor, vous): él entiende «quai de Bercy» en vez de «quai de Valmy»; lo reparan y Ana va a cenar con una amiga sin nombre / Ana takes a VTC on a Friday night with Monsieur Benali (driver, vous): he understands “quai de Bercy” instead of “quai de Valmy”; they sort it out and Ana goes to dinner with an unnamed friend
- Madame Dubois (miembro de la asociación de barrio, vous con Ana y con el vecino nuevo) explica al vecino los códigos del edificio (crémaillère, fête des voisins, ruido tras las 22 h, basura en el rellano, tuteo); Ana dice «vous» a Madame Dubois desde el principio / Madame Dubois (member of the neighborhood association, vous with Ana and the new neighbor) explains the building’s unwritten rules (housewarming, neighbors’ party, noise after 10 p.m., trash on the landing, tu/vous); Ana has always used vous with Madame Dubois

## Sin resolver

- Nada bloqueante. Opcional para el integrador: añadir «Benali» a `palabrasLibres` solo si en el futuro aparece dentro de un texto francés (hoy solo es etiqueta de hablante).
- En c40 los diálogos siguen un formato pregunta–respuesta algo didáctico (inevitable por el objetivo «explicar códigos»); se dejó tal cual por ser comprensible y coherente con los ítems.
