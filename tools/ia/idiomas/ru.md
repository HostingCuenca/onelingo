# Ficha de idioma: ruso (ru)

Esta ficha se inserta en todos los prompts de `tools/ia/prompts/`. Es la única fuente de reglas propias del ruso.

## Alumno y variedad
- **Alumno:** adulto hispanohablante de EE. UU. o Latinoamérica.
- **Idiomas de apoyo:** español latino neutro con «tú» (ustedes, celular, carro o auto, computadora, departamento, manejar, boleto, jugo, papa, lentes) e inglés americano.
- **Ruso estándar contemporáneo** (norma de Moscú): léxico neutro, ortografía vigente con «ё», sin regionalismos, jerga ni vulgaridades (nunca «мат»).
  - La jerga o el registro coloquial solo se usan para comprensión, desde N8, marcados «coloquial» y nunca como respuesta esperada.
  - Sin política, guerra ni sanciones como tema; ningún diálogo sitúa personajes en Ucrania ni en Crimea.
- **Examen de referencia:** TORFL (ТРКИ): ТЭУ = A1, ТБУ = A2, ТРКИ-1 = B1, ТРКИ-2 = B2, ТРКИ-3 = C1, ТРКИ-4 = C2. La c50 de cada nivel imita el formato del examen de su nivel MCER, sin nombrar marcas en las consignas.

## Tratamiento
- «tú» = ты; «usted» = вы (formal); «ustedes» = вы; «nosotros» = мы. «Usted» y «ustedes» comparten forma: lo aclara el contexto (uno o varios interlocutores).
- **Regla por defecto:** вы entre desconocidos, con adultos mayores, en servicios (tienda, hotel, banco, oficina) y en el trabajo. ты con amigos, familia, niños y gente joven. La ficha de la clase fija cuál se usa; no se mezclan en un mismo diálogo salvo que la clase lo enseñe.
- «Вы» va en minúscula siempre (mayúscula solo al inicio de frase). El imperativo formal acaba en «-ите» (повторите, извините); el informal en «-и» (извини).
- **Nombre y patronímico:** no hay patronímicos antes de N5. Desde N5, solo estos: Иванович / Ивановна, Петрович / Петровна, Сергеевич / Сергеевна, Александрович / Александровна («Анна Петровна»). Sin «господин» ni «госпожа»: se usa el nombre o el papel («продавец», «администратор», «врач», «преподаватель»).

## Romanización (`rom`)
Sistema práctico, único y fijo, **neutro**: vale igual para quien usa la app en español o en inglés, porque no imita las convenciones de ninguno de los dos idiomas. Es una **transliteración letra a letra**, no una transcripción fonética: no muestra la reducción vocálica ni el ensordecimiento (eso lo enseñan las guías de pronunciación). Se ve así: молоко → molokó (suena «malakó»), хлеб → khleb (suena «khlep»).

| Letra | `rom` | Ejemplo |
|---|---|---|
| а | a | адрес (ádres) |
| б | b | брат (brat) |
| в | v | вода (vodá) |
| г | g (siempre g) | город (górod) |
| д | d | дом (dom) |
| е | ye al inicio de palabra, tras vocal o tras ь / ъ; e en los demás casos | есть (yest'), нет (net), доброе (dóbroye) |
| ё | yo | моё (moyó), дёшево (dyóshevo), жёлтый (zhyóltyy) |
| ж | zh | женщина (zhénshchina) |
| з | z | здесь (zdes') |
| и | i | мир (mir) |
| й | y | мой (moy), чай (chay) |
| к | k | книга (kníga) |
| л | l | лампа (lámpa) |
| м | m | мама (máma) |
| н | n | нос (nos) |
| о | o | окно (oknó) |
| п | p | папа (pápa) |
| р | r | рука (ruká) |
| с | s | сестра (sestrá) |
| т | t | стол (stol) |
| у | u | сумка (súmka) |
| ф | f | фамилия (famíliya) |
| х | kh | хорошо (khoroshó), хлеб (khleb) |
| ц | ts | цена (tsená) |
| ч | ch | чай (chay) |
| ш | sh | шесть (shest') |
| щ | shch | щи (shchi) |
| ъ | " | объём (ob"yóm) |
| ы | y | мы (my), новый (nóvyy) |
| ь | ' | пять (pyat'), семья (sem'yá) |
| э | e | это (éto) |
| ю | yu | юг (yug) |
| я | ya | я (ya), пятый (pyátyy) |

Reglas fijas:
1. **Acento:** tilde aguda sobre la vocal tónica en toda palabra de 2 o más sílabas; los monosílabos no llevan marca (дом → dom). La «ё» de una palabra de 2+ sílabas lleva siempre acento en el `rom` (моё → moyó). En el `rom` se usan á é í ó ú ý. **El acento va solo en el `rom`:** el texto cirílico nunca lleva marca de acento (ni U+0301).
2. **й = y** y **ы = y**, también en las terminaciones: -ай → ay, -ой → oy, -ый → yy, -ий → iy (добрый → dóbryy, русский → rússkiy, Дмитрий → Dmítriy). «мой» (moy) y «мои» (moí) se distinguen por la última letra y por el acento.
3. **ь = '** y **ъ = "** (comilla recta); ь se escribe antes de vocal sin separarla: семья → sem'yá.
4. **г = g siempre**, también ante e, i, э (книги → knígi, Сергей → Sergéy). Un hispanohablante leería «ge/gi» como «je/ji»: la guía de pronunciación recuerda que г es la «g» de «gato». El sonido «j» se escribe «kh» (х: хорошо → khoroshó).
5. **е** = ye al inicio de palabra, tras vocal o tras ь / ъ; e tras consonante. **ё** = yo siempre, también tras ж, ш, ч, щ (жёлтый → zhyóltyy); es siempre tónica.
6. Mayúsculas como en el original (Ж → Zh, Щ → Shch, Ю → Yu, Е inicial → Ye). Los signos de puntuación se copian tal cual (guion largo «—», «…»).
7. Una palabra rusa = una palabra `rom`; los guiones se conservan: по-русски → po-rússki.

**Dónde va:** en N1–N4, en todo texto ruso (vocabulario, ejemplos, diálogos, estímulos, opciones); desde N5, solo en el vocabulario. En el JSON, el campo `rom` va junto a `texto`. No llevan `rom` los `tokens` de `ordenar`, la `respuesta` ni las `aceptadas` (la app los compara en cirílico). El `rom` lleva siempre el acento; el cirílico no lo lleva en ningún campo.

## Nombres y lugares (lista cerrada)
- **Personas:**
  - Nombres femeninos (8): Анна (Ánna), Мария (Maríya), Елена (Yeléna), Ольга (Ól'ga), Наталья (Natál'ya), Татьяна (Tat'yána), Ирина (Irína), Светлана (Svetlána).
  - Nombres masculinos (7): Иван (Iván), Александр (Aleksándr), Дмитрий (Dmítriy), Сергей (Sergéy), Андрей (Andréy), Михаил (Mikhaíl), Максим (Maksím).
  - Apellidos (masculino / femenino): Иванов (Ivánov) / Иванова (Ivánova), Петров (Petróv) / Петрова (Petróva), Смирнов (Smirnóv) / Смирнова (Smirnóva), Кузнецов (Kuznetsóv) / Кузнецова (Kuznetsóva), Макаров (Makárov) / Макарова (Makárova), Васильев (Vasíl'yev) / Васильева (Vasíl'yeva), Новиков (Novíkov) / Новикова (Novíkova), Фёдоров (Fyódorov) / Фёдорова (Fyódorova), Михайлов (Mikháylov) / Михайлова (Mikháylova), Павлов (Pávlov) / Павлова (Pávlova).
  - No uses nombres o apellidos que sean también palabras comunes (Вера, Надежда, Любовь, Роза, Соколов, Волков, Орлов, Козлов, Лебедев).
  - El apellido femenino concuerda: «Анна Иванова», «Иван Иванов». Un nombre no pasa de una clase a otra: no hay historia ni reparto.
  - Si no, se usa el papel en ruso: «продавец», «администратор», «врач», «преподаватель», «сотрудница».
- **Ciudades (10):** Москва (Moskvá), Санкт-Петербург (Sankt-Peterbúrg), Казань (Kazán'), Новосибирск (Novosibírsk), Екатеринбург (Yekaterinbúrg), Самара (Samára), Краснодар (Krasnodár), Сочи (Sóchi), Воронеж (Vorónezh), Владивосток (Vladivostók), sin datos verificables (ni líneas de metro, direcciones, precios reales o comercios reales).
  - Lugares genéricos: «магазин», «аптека», «почта», «вокзал».
- **Países permitidos:** México, Colombia, Argentina, Chile, Perú, España, Estados Unidos, Rusia, Alemania.
  - **Nunca Ecuador, Quito, Guayaquil, Cuenca ni «ecuatoriano»** (ni «эквадор», «эквадорец»), en ningún idioma ni campo.

## Guías de pronunciación (copiar, no inventar otras)
**ES:**
- **Vocales tónicas** plenas: а ≈ «a», о ≈ «o», у ≈ «u», э ≈ «e» de «mesa», и ≈ «i» de «sí». Las vocales «iotizadas» я, ю, ё, е suenan «ya, yu, yo, ye» tras vocal o al inicio, y **ablandan** la consonante anterior si van tras ella.
- **Reducción** (аканье / иканье): sin acento, о y а suenan «a» corta (молоко ≈ «malakó», хорошо ≈ «jarashó», вода ≈ «vadá»); en las demás sílabas átonas, casi un murmullo. е y я átonas suenan «i» breve (язык ≈ «yizík», река ≈ «riká»). La vocal tónica es más larga y clara.
- **Consonantes duras y blandas:** casi toda consonante tiene un par duro y uno blando. Para ablandar, la parte media de la lengua sube hacia el paladar como al decir «i»: нь ≈ «ñ» suave, ль ≈ «l» con «i» fundida. Cambian el significado: мат / мать, брат / брать, был / быль, угол / уголь. Se ablanda con ь o con е, ё, и, ю, я después de la consonante. ж, ш, ц son siempre duras; ч, щ y й, siempre blandas.
- **ы:** vocal central, entre «i» y «u»: di «i» con los labios sin redondear y la lengua hacia atrás. ты ≠ ти; мы ≠ ми. Tras ж, ш, ц se escribe «и» pero suena «ы» (жить ≈ «zhyt'»).
- **ш, ж, щ, ч, ц:** ш ≈ «sh» con la lengua curvada hacia atrás (más grave que en inglés); ж = ш sonora (≈ «j» del francés «jour»; ≈ «y» rioplatense de «yo»); щ ≈ «sh» larga y blanda (no «shch» separados); ч ≈ «ch» de «chico» pero blanda y sin explosión fuerte; ц ≈ «ts» de «pizza».
- **ь y ъ:** ь no suena: ablanda la consonante anterior (мать, день) o, antes de vocal, suena «consonante + y» (семья ≈ «simyá»). ъ es un separador duro: pausa breve antes de е, ё, ю, я (объём ≈ «abyóm»).
- **Acento móvil:** no se escribe en un texto normal y cambia de sílaba según la forma: рука / руки, вода / воды, окно / окна. «ё» es siempre tónica. Se aprende con cada palabra; se muestra solo en el `rom` (tilde aguda), nunca en el cirílico.
- **Ensordecimiento:** b, d, g, v, z, zh suenan p, t, k, f, s, sh al final de palabra y ante consonante sorda: хлеб ≈ «jlep», друг ≈ «druk», глаз ≈ «glas», ложка ≈ «lóshka». Y al revés, una sorda ante sonora se sonoriza: сдать ≈ «zdat'».
- **Otras:** р = «rr» vibrante múltiple; л dura = «l» con la lengua atrás (como en el inglés «ball»); в = «v» labiodental, nunca «b»; х ≈ «j» de «jamón»; г = «g» de «gato», siempre; в y д en здравствуйте y -надцать no suenan (la «в» tras «здра», la «д» de одиннадцать); «-ого / -его» se lee «-ово» (ничего ≈ «nichivó»); что se lee «shto».
- **Entonación de pregunta (sí/no):** la voz sube sobre la sílaba tónica de la palabra por la que se pregunta y **baja después**; no sube al final como en español: Это стол? se dice con subida en «стол».
- Nunca se dice que un sonido es «igual» al español si no lo es: se avisa de la diferencia (ы, ж, щ, duras y blandas, reducción).

**EN:**
- Stressed vowels are full: а like «a» in «father», о like «o» in «more», у like «oo» in «moon», э like «e» in «bed», и like «ee» in «see».
- Unstressed о and а reduce to a short «uh» (молоко ≈ «muh-luh-KOH»); unstressed е and я reduce to a short «i» (язык ≈ «yi-ZIK»).
- Consonants are hard or soft; soft means the middle of the tongue rises toward the palate, like «y» in «canyon» for нь and «lli» in «million» for ль. They change meaning: мат / мать, брат / брать. ж, ш, ц are always hard; ч, щ, й always soft.
- ы is a central vowel: say «ee» with the tongue pulled back and lips unrounded. ты ≠ ти.
- ш like «sh» with the tongue curled back; ж like «s» in «measure»; щ a long soft «sh»; ч like «ch» in «church» but softer; ц like «ts» in «cats».
- ь is silent and softens the consonant before it; ъ is a hard separator: a tiny pause before е, ё, ю, я.
- Stress is free and mobile: рука / руки. «ё» is always stressed. Learn each word with its stress.
- Voiced consonants devoice at the end of a word and before a voiceless one: хлеб ≈ «khlep», друг ≈ «druk». Voiceless ones voice before a voiced one: сдать ≈ «zdat'».
- в like «v» (never «w»); х like «h» in «loch»; г always like «g» in «go»; р is a trilled «r»; hard л like «l» in «ball».
- Yes/no question: the pitch rises on the stressed syllable of the questioned word and falls afterwards; it does not rise at the end.

## Gramática: lo que más falla en hispanohablantes (úsalo en `erroresFrecuentes` y distractores)
- **Casos:** \*Я вижу Анна → Я вижу Анну; \*Я живу в Москва → Я живу в Москве; \*Это книга Анна → Это книга Анны; \*с Иван → с Иваном. Un caso por vez; en Fundamentos solo bloques (меня зовут, я из Мексики, в Москве, у меня нет брата).
- **Género:** \*Она сказал → Она сказала (pasado); \*красивый книга → красивая книга; \*мой сумка → моя сумка. Sustantivos en -ь: мать (f), день (m); excepciones: папа, дядя masculinos; кофе masculino e indeclinable.
- **Aspecto:** \*Вчера я прочитал книгу два часа → Вчера я читал книгу два часа (proceso) frente a Вчера я прочитал книгу (resultado); el futuro compuesto solo con imperfectivo: \*Я буду прочитать → Я буду читать / Я прочитаю.
- **Verbos de movimiento:** \*Я иду на работу каждый день → Я хожу на работу каждый день; \*Я иду в Москву на поезде → Я еду в Москву на поезде. Unidireccional (идти, ехать) frente a multidireccional (ходить, ездить); a pie (ходить) frente a en transporte (ездить).
- **Ausencia de «ser/estar» en presente:** \*Я есть студент → Я студент; \*Анна есть дома → Анна дома. «Есть» solo expresa existencia o posesión (У меня есть брат).
- **Orden de palabras:** el elemento nuevo va al final: Стол стоит в комнате («la mesa está en la habitación») frente a В комнате стоит стол («en la habitación hay una mesa»). Sin verbo auxiliar ni inversión en las preguntas: \*Есть ты студент? → Ты студент?
- **Duro / blando:** \*мат por мать; \*был por быль; \*ти por ты. Evalúalo solo cuando la clase trata el par.
- **У меня есть…:** \*Я имею брата → У меня есть брат; \*Я имею 20 лет → Мне двадцать лет; \*Я нравится кофе → Мне нравится кофе (gustar: la persona va en dativo). La ausencia: \*У меня нет брат → У меня нет брата (genitivo).
- **Negación doble:** \*Я знаю ничего → Я ничего не знаю; «не» siempre delante del verbo.
- **Preposiciones в / на:** \*в работе → на работе; \*в почте → на почте; \*Я живу в Москву → Я живу в Москве (dónde: preposicional; adónde: acusativo, Я еду в Москву).
- **Numerales:** \*два книги → две книги; 2–4 + genitivo singular (две книги), 5+ + genitivo plural (пять книг).
- **Posesivo reflexivo:** \*Он любит его маму (la suya) → Он любит свою маму.
- **Calcos léxicos:** \*Я есть голод → Я хочу есть; \*Я говорю испанский → Я говорю по-испански.

## Falsos amigos (⚠ obligatoria, con contraste, solo estos o equivalentes igual de reales)
- **Con el español:**
  - фамилия (apellido ≠ familia, que es семья), спина (espalda ≠ espina), лист (hoja ≠ lista, que es список).
  - магазин (tienda ≠ magacín/revista, que es журнал), гимназия (liceo ≠ gimnasio, que es спортзал), бланк (formulario ≠ blanco).
  - интеллигентный (educado, culto ≠ inteligente, que es умный), акция (promoción; acción bursátil ≠ acción, que es действие).
  - но (pero ≠ no, que es нет), артист (intérprete ≠ artista, que es художник).
- **Solo con el inglés** (⚠ solo en `en`):
  - магазин (store ≠ magazine), мы (we ≠ my), он (he ≠ on).
  - аспирант (PhD student ≠ aspirant), кабинет (office, study ≠ cabinet), симпатичный (good-looking ≠ sympathetic).
  - интеллигентный (cultured ≠ intelligent), акция (share, promotion ≠ action), фамилия (last name ≠ family), лист (leaf, sheet ≠ list).
- **No son falsos amigos** (sin ⚠): университет, студент, театр, банк, метро, такси, паспорт, музей, парк, ресторан, фабрика, адрес, телефон, интернет, шоколад, газета.
- **Jerga o registro** (круто, ладно, блин): se marca «coloquial», sin ⚠. Nunca vulgaridades.

## Ortografía y forma (reglas duras)
- **Alfabeto:** cirílico estándar; nunca se mezclan letras latinas dentro de una palabra rusa (a, e, o, p, c, x latinas parecen cirílicas: se evitan).
- **Mayúsculas:** solo en nombres propios (Анна, Москва, Россия), inicio de frase y títulos. Días, meses, idiomas y gentilicios van en minúscula (понедельник, январь, русский, мексиканец, по-русски). «Вы» de cortesía va en minúscula.
- **ё:** en todo material didáctico se escribe siempre («ё», nunca «е»): моё, дёшево, всё, ещё, её, твёрдый, живёте, Фёдоров. La respuesta correcta lleva ё y `aceptadas` nunca añade la variante con «е»: esa tolerancia la pone la app.
- **Marca de acento:** el texto cirílico **nunca lleva marca de acento** (ni U+0301 ni ninguna otra) en ningún campo: vocabulario, ejemplos, explicaciones, consignas, estímulos, opciones, respuestas, `aceptadas`, `tokens`, `audio` y diálogos se escriben limpios (привет). Así la comparación exacta y la voz sintética quedan limpias.
  - El acento se muestra **solo en el `rom`**: tilde aguda sobre la vocal tónica de toda palabra de 2+ sílabas (privét, zdrávstvuyte); los monosílabos no se marcan; la «ё» de 2+ sílabas siempre (yó). El validador da error si aparece U+0301.
- **Comas (obligatorias):**
  - Antes de oraciones subordinadas: что, чтобы, потому что, если, когда, который (Я знаю, что он дома.).
  - Antes de а y но (Это не стол, а стул.). No se pone coma ante «и» entre elementos de una enumeración.
  - Tras vocativo e interjecciones iniciales (Анна, здравствуйте! / Да, это стол.).
- **Guion largo (—):** entre dos sustantivos en presente: Анна — врач; con «это» + sustantivo se usa: Москва — это город. Con pronombre personal sujeto no hay guion: Я студент, Он врач.
- Comillas en el texto ruso: «…» (angulares). En `respuesta` no van comillas.
- En `audio`, números, horas y fechas se escriben en palabras («десять рублей», «половина восьмого»). Nunca se escriben «₽», «%», «/», «_» ni «→», ni marcas de acento ni `rom` en el audio.
- `aceptadas` recoge las variantes reales:
  - orden alternativo correcto (Я живу в Москве. / В Москве я живу.);
  - guion opcional entre sustantivos (Анна — врач. / Анна врач.);
  - sujeto explícito siempre: los pronombres no se omiten en las respuestas esperadas.
  - Nunca se añaden variantes en minúscula, sin «ё» ni sin signos: esa tolerancia la pone la app.

## Formas de citación del vocabulario
- **Sustantivo:** nominativo singular, sin artículo (no los hay en ruso), en `texto`; el **género** abre siempre la `nota` («Masculino.» / «Femenino.» / «Neutro.»; en `en`: «Masculine.» / «Feminine.» / «Neuter.»). Se indican también las excepciones (sustantivos en -ь, папа, кофе), el plural irregular y el acento móvil. Los que solo existen en plural llevan «Solo plural.».
- **Verbo:** par de aspecto, imperfectivo primero y perfectivo después, separados por «—» con espacios: читать — прочитать. Si no hay par en ese sentido, solo el infinitivo y la nota «Sin par perfectivo en este sentido.». Los verbos de movimiento van uno por vocablo, con la nota «unidireccional» o «multidireccional» y su perfectivo (идти → пойти).
- **Adjetivo:** masculino nominativo singular (новый, большой); la concordancia se enseña en la nota o en un ejemplo.
- **Pronombres y números:** nominativo; las formas oblicuas (меня, у меня, из Мексики) solo como bloque fijo hasta que la clase enseñe el caso.
- **Frases:** forma completa con su puntuación; los huecos se escriben «…» (Мне … лет).
- Todo vocablo lleva `rom` (acento incluido) siguiendo la romanización de esta ficha.

## Separación de palabras para `ordenar`
- Los tokens se separan por espacios normales, como en español. Los signos de puntuación van pegados a la palabra (Анна!, Москве.).
- Las palabras con guion son un solo token (по-русски, Санкт-Петербург); el guion largo «—» es un token propio, separado por espacios.
- Sin acento ni `rom` dentro de los tokens.

## Fundamentos y Nivel 0
Las claves previas (`previos`) y los ids de Fundamentos (`ru.f0.*`) vienen en el contexto. N1 c01 parte de lo que enseña f0: saludos, alfabeto, números 0–20, ты / вы y presentarse. Nunca se asume que el alumno ya lee cirílico con soltura: en N1–N4 todo texto ruso lleva `rom`.
