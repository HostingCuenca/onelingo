# Ficha de idioma: italiano (it)

Esta ficha se inserta en todos los prompts de `tools/ia/prompts/`. Es la única fuente de reglas propias del italiano.

## Alumno y variedad
- **Alumno:** adulto hispanohablante de EE. UU. o Latinoamérica.
- **Idiomas de apoyo:** español latino neutro con «tú» (ustedes, celular, carro o auto, computadora, departamento, manejar, boleto, jugo, papa, lentes) e inglés americano.
- **Italiano estándar** neutro: léxico panitaliano, ortografía estándar con acentos gráficos correctos («è» verbo frente a «e» conjunción; perché, città, caffè, più, già, così).
  - Los regionalismos y dialectos solo aparecen para comprensión, desde N8, y nunca como respuesta esperada.
- **Tratamiento formal:** «Lei» con mayúscula y el verbo en 3.ª persona del singular, con adultos desconocidos y en el trabajo. «Tu» con amigos, familia y gente joven. La ficha de la clase fija cuál se usa.
- **Exámenes de referencia:** CILS, CELI y PLIDA (A1–C1). La c50 de cada nivel imita el formato del examen de su nivel MCER, sin nombrar marcas en las consignas.

## Nombres y lugares (lista cerrada)
- **Personas:**
  - Nombres: Marco, Giulia, Luca, Chiara, Sofia, Matteo, Francesca, Alessandro, Elena, Paolo, Anna, Giorgio, Sara, Davide, Martina.
  - Apellidos: Rossi, Bianchi, Ferrari, Esposito, Moretti, Marchetti, Lombardi, Mancini, Rinaldi, Ferraro (no uses apellidos que sean palabras corrientes: Conti, Greco, Romano, Colombo, Ricci, De Luca).
  - Fórmulas: «il signor Rossi», «la signora Bianchi», «la dottoressa Conti».
  - Si no, se usa el papel en italiano: «cameriere», «commessa», «medico», «impiegato», «receptionist».
  - Un nombre no pasa de una clase a otra: no hay historia ni reparto.
- **Ciudades:** Roma, Milano, Napoli, Torino, Firenze, Bologna, Venezia, Genova, Palermo, Verona, sin datos verificables (ni líneas de metro, direcciones, precios reales o comercios reales).
  - Lugares genéricos: «la stazione», «la farmacia», «l'ufficio postale».
- **Países permitidos:** México, Colombia, Argentina, Chile, Perú, España, Estados Unidos, Italia, Suiza.
  - **Nunca Ecuador, Quito, Guayaquil, Cuenca ni «ecuatoriano»**, en ningún idioma ni campo.

## Guías de pronunciación (copiar, no inventar otras)
**ES:**
- «c» + e/i = «ch» (ciao ≈ «chao», cena ≈ «chena»); «ch» + e/i = «k» (chiesa ≈ «kiesa»).
- «g» + e/i = como la «j» inglesa de «jeans» (gelato); «gh» + e/i = «g» de «guerra» (spaghetti).
- «gn» = «ñ» (gnocchi, bagno).
- «gli» ≈ «li» muy unido, con la lengua pegada al paladar (figlio ≈ «fí-lio» en un solo golpe).
- «sc» + e/i = «sh» (pesce ≈ «peshe»); «sch» + e/i = «sk» (schiena).
- «z» = «ts» o «ds» (pizza ≈ «pitsa», zero ≈ «dsero»); «qu» = «cu» (quando).
- «h» nunca suena (ho, hai, hanno ≈ «o», «ai», «anno»).
- **Consonantes dobles:** se mantienen más tiempo y cambian el significado: pala/palla, caro/carro, capello/cappello, nono/nonno.
- Vocales siempre plenas, nunca se reducen.
- La «e» y la «o» abiertas o cerradas no se evalúan; solo se avisa de que existen.
- Acento: la mayoría de palabras son llanas; el acento gráfico solo va en la última sílaba (città, perché).

**EN:**
- «c» + e/i like «ch» in «church»; «ch» like «k».
- «g» + e/i like «j» in «jet»; «gh» like «g» in «go».
- «gn» like «ny» in «canyon»; «gli» like «lli» in «million».
- «sc» + e/i like «sh».
- «z» like «ts» or «ds»; single «r» tapped, «rr» rolled.
- Double consonants are held longer and change meaning.
- Vowels are always full: never reduce them to «uh».

Nunca se dice que un sonido es «igual» al español si no lo es: se avisa de la diferencia (dobles, gli, e/o abiertas).

## Gramática: lo que más falla en hispanohablantes (úsalo en `erroresFrecuentes` y distractores)
- **Auxiliar del passato prossimo:**
  - \*Ho andato → Sono andato/a: «essere» con verbos de movimiento y cambio y con los reflexivos.
  - El participio concuerda con «essere»: \*Maria è andato → Maria è andata.
- **Artículos:**
  - lo/gli ante s+consonante, z, gn, ps, y: \*il studente → lo studente; \*i zaini → gli zaini.
  - Elisión: \*la amica → l'amica; \*lo ho visto → l'ho visto.
- **Preposiciones articuladas obligatorias:** \*in la casa → nella casa; \*a il cinema → al cinema; \*di il → del.
- **«a» personal del español:** \*Vedo a Marco → Vedo Marco.
- **Piacere:** \*Mi piace i libri → Mi piacciono i libri.
- **Posesivo con artículo:** \*mio libro → il mio libro. Sin artículo con familiar en singular: \*la mia madre → mia madre.
- **«c'è / ci sono»:** \*Ci sono un problema → C'è un problema. «ci» y «ne» se omiten por calco del español.
- **Comparativo:** \*più grande que → più grande di / che (según el caso).
- **Congiuntivo tras opinión:** \*Penso che è → Penso che sia.
- **Dobles:** \*capello (pelo) por cappello (sombrero). Se evalúan solo cuando la clase trata las dobles.
- **Calcos léxicos:** \*esperare → aspettare; \*salire di casa → uscire di casa; \*tenere fame → avere fame.

## Falsos amigos (⚠ obligatoria, con contraste, solo estos o equivalentes igual de reales)
- **Con el español:**
  - burro (mantequilla ≠ asino), caldo (caliente ≠ brodo), salire (subir ≠ uscire).
  - guardare (mirar ≠ conservare), camera (habitación ≠ macchina fotografica), gamba (pierna).
  - aceto (vinagre ≠ olio), largo (ancho ≠ lungo), tirare (jalar ≠ buttare via).
  - imbarazzata (avergonzada ≠ incinta), morbido (suave ≠ morboso), vaso (maceta ≠ bicchiere).
  - negozio (tienda ≠ affare), tasca (bolsillo), cantina (sótano/bodega), nudo (desnudo ≠ nodo).
  - pronto (¿bueno?/listo ≠ presto), presto (pronto/temprano), subire (sufrir ≠ salire), topo (ratón).
- **Solo con el inglés** (⚠ solo en `en`):
  - parenti (relatives ≠ parents), fattoria (farm ≠ factory), magazzino (warehouse ≠ magazine).
  - educato (polite ≠ educated), eventualmente (if needed ≠ eventually), attualmente (currently ≠ actually).
  - libreria (bookshop ≠ library), sensibile (sensitive ≠ sensible), confetti (sugared almonds).
- **No son falsos amigos** (sin ⚠): casa, famiglia, lavoro, scuola, ciao, prego, allora, magari (se explica como expresión, no como trampa).
- **Jerga o registro** (figo, beccare, un casino): se marca «coloquial», sin ⚠.

## Ortografía y forma (reglas duras)
- Apóstrofo recto «'» en elisiones (l'amico, c'è, dov'è, un'amica; «un amico» sin apóstrofo).
- Acento grave en «è», à, ì, ò, ù; agudo en perché, poiché, affinché, né, sé.
- Mayúscula solo en nombres propios, inicio de frase y «Lei» de cortesía. Días, meses, idiomas y gentilicios van en minúscula (lunedì, gennaio, l'italiano, messicano).
- Comillas en el texto italiano: «…» (caporali). En `respuesta` no van comillas.
- En `audio`, números, horas y fechas se escriben en palabras («alle otto e mezza», «venti euro»).
- Nunca se escriben «€», «%», «/», «_» ni «→» en el audio.
- `aceptadas` recoge las variantes reales:
  - orden alternativo correcto;
  - sujeto explícito u omitido («Sono italiano» / «Io sono italiano»);
  - elisión opcional («una amica» no; «l'amica» sí).
  - Nunca se añaden variantes en minúscula ni sin acento: esa tolerancia la pone la app.

## Fundamentos y Nivel 0
Las claves previas (`previos`) y los ids de Fundamentos (`it.f0.*`) vienen en el contexto. N1 c01 parte de lo que enseña f0: saludos, alfabeto, números 0–20 y presentarse.
