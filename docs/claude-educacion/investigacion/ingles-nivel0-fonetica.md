# Inglés Nivel 0 · Leer y pronunciar inglés desde cero
### Investigación de diseño de aprendizaje para OneLingo (adultos hispanohablantes de Latinoamérica, conocimiento cero)

Fecha: 01-10-2026 · Variante objetivo: **inglés general americano (GA)**.

---

## 0. Resumen ejecutivo

1. **La evidencia apoya la fonética sintética sistemática (SSP)**: enseñar correspondencias grafema‑fonema (GPC) en un orden fijo, mezclar sonidos para leer (blending) y separarlos para escribir (segmenting), con textos 100 % decodificables y muy pocas "palabras trampa" al principio (DfE, *The Reading Framework*, 2023; Jolly Phonics; Letters and Sounds).
2. **Los adultos que ya leen español necesitan igual instrucción explícita de fonética inglesa.** Reconocen las letras y leen de izquierda a derecha, por eso parecen más avanzados de lo que están, pero traen la suposición de que "cada letra = un sonido". Hay que desmontar esa idea de forma explícita (CAL / Burt, Peyton y Adams, 2003).
3. **El gran problema del hispanohablante son las vocales**: el español tiene 5 y el inglés GA tiene unas 15 sin contar las de R (el Color Vowel Chart usa 15 + R). Las confusiones clave son /ɪ/–/iː/ (ship/sheep), /æ/–/ʌ/–/ɑ/ (cat/cut/cot), /ʊ/–/uː/ (full/fool), la schwa /ə/ y la vocal de R /ɝ/ (bird). En consonantes: v/b, th, sh, la z sonora, la h, la r inglesa, la s inicial ("eschool"), las consonantes finales y los finales -s/-ed. Y el **acento y ritmo** (el español es silábico y el inglés acentual).
4. **Color Vowel Chart (Taylor y Thompson, ELTS)**: 15 colores, cada nombre de color y su palabra clave comparten la vocal acentuada ("GREEN TEA" = /iː/). **No se puede usar en una app comercial sin licencia**: la imagen tiene licencia CC BY‑NC‑ND (no comercial y sin derivados), "Color Vowel" es marca registrada y ELTS dice que hacer una versión propia del chart para distribuirla viola su copyright. **Recomendación: diseñar un sistema propio** (colores distintos, palabras‑ancla con imagen y sin la fórmula "nombre de color que rima con la palabra"). Más abajo propongo uno.
5. **El TTS falla con fonemas aislados** (por ejemplo, "a" se lee como /eɪ/, el nombre de la letra). Para los ~44 sonidos aislados y las palabras estiradas ("sssaaat") hay que **grabar audio humano**. El TTS sirve para palabras y frases, y las etiquetas de fonema SSML y los diccionarios de pronunciación sirven para corregir palabras concretas. ElevenLabs: SSML `<phoneme>` solo en Flash v2 / Turbo v2 (solo inglés), y los diccionarios con reglas de fonema en eleven_v3, eleven_v4 y flash_v2.
6. **Propuesta**: 14 unidades, unas 80 lecciones de 5–8 min, de "Hello!" (de oído) a leer palabras CVC/CVCe, equipos vocálicos, vocales con R, schwa y acento, y finales -s/-ed. Prueba final: presentarse, deletrear su nombre, leer 50 palabras frecuentes y decodificar pseudopalabras.

---

## 1. Inventario de sonidos del inglés (44 fonemas, GA) frente al español latinoamericano

**Convención.** Uso el conteo "44" de los programas de fonética: 24 consonantes y 20 vocales, contando como unidades de enseñanza las combinaciones con R (ar, or, air, ear). En GA, /ɔ/ se funde con /ɑ/ para buena parte de los hablantes (fusión *cot–caught*). Recomiendo enseñarlas juntas en el Nivel 0.

**Estado para hispanohablantes:**
- ✅ **Lo tiene**: el sonido existe en español latinoamericano.
- 🟡 **Cercano**: existe un sonido parecido o un alófono, pero hay que ajustarlo.
- ❌ **No lo tiene**: es un sonido nuevo y prioritario.

**Frecuencia de grafías.** El orden de las grafías es aproximado, de más a menos frecuente. Se basa en los análisis clásicos de correspondencias fonema‑grafema (tipo Hanna et al.) y en el orden de enseñanza de los programas SSP.

### 1.1 Vocales cortas ("checked")

| # | IPA | Grafías (más → menos frecuentes) | Palabras clave | Español |
|---|---|---|---|---|
| 1 | /æ/ | a (cat), a…e raro (have), ai (plaid), au (laugh) | apple, cat, map | ❌ no existe; el hispanohablante la cambia por /a/ |
| 2 | /ɛ/ | e (bed), ea (bread, head), ai (said), a (any), ie (friend) | egg, ten, red | 🟡 cercana a la "e" española (un poco más abierta) |
| 3 | /ɪ/ | i (sit), y (gym), e (pretty, English), ui (build), o (women) | it, fish, pig | ❌ no existe; el hispanohablante la cambia por /i/ (ship → sheep) |
| 4 | /ɑ/ (+ /ɔ/ fundida) | o (hot), a (father, car), al (calm); para /ɔ/: aw (saw), au (sauce), al (talk), ough (bought) | hot, box, fox / saw, ball | 🟡 /ɑ/ es parecida a la "a" española abierta; /ɔ/ cae entre "a" y "o" |
| 5 | /ʌ/ | u (cup), o (son, love, come), ou (young), oo (blood) | up, sun, bus | ❌ no existe; el hispanohablante la cambia por "a" u "o" |
| 6 | /ʊ/ | oo (book), u (put, full), ou (could, would), o (woman) | book, good, foot | ❌ no existe; el hispanohablante la cambia por "u" (full = fool) |
| 7 | /ə/ schwa | cualquier vocal sin acento: a (about), e (taken), o (lemon), u (supply), i (pencil) | about, banana, the | ❌ no existe; el hispanohablante pronuncia la vocal escrita con "valor completo" |

### 1.2 Vocales largas, "tensas" y diptongos

| # | IPA | Grafías | Palabras clave | Español |
|---|---|---|---|---|
| 8 | /iː/ | ee (see), ea (eat), e (me, be), e_e (these), y/ey (happy, key), ie (field), i (pizza) | see, tea, tree | 🟡 cercana a la "i" española, pero más larga y tensa |
| 9 | /eɪ/ | a_e (cake), ai (rain), ay (day), a abierta (baby), eigh (eight), ey (they), ea (great) | cake, rain, day | 🟡 parecida a "ei" (rey, seis); el hispanohablante la acorta a "e" |
| 10 | /aɪ/ | i_e (time), igh (night), y (my), i (I, hi), ie (pie), uy (buy) | I, ice, kite | ✅ como "ai" (hay, baile) |
| 11 | /oʊ/ | o_e (home), o (go, no), oa (boat), ow (snow), oe (toe), ough (though) | go, home, boat | 🟡 el hispanohablante dice "o" pura, sin el deslizamiento hacia /ʊ/ |
| 12 | /uː/ (+ /juː/) | oo (moon), u_e (rule, June; /juː/ en cute, use), ew (new), ue (blue), o (do, to), ou (soup), ui (fruit) | moon, food, blue | 🟡 cercana a la "u" española, más larga |
| 13 | /aʊ/ | ou (out), ow (cow) | out, house, cow | ✅ como "au" (causa, auto) |
| 14 | /ɔɪ/ | oi (oil), oy (boy) | boy, oil, coin | ✅ como "oi/oy" (hoy, boina) |

### 1.3 Vocales con R (r‑controladas, GA rótico)

| # | IPA | Grafías | Palabras clave | Español |
|---|---|---|---|---|
| 15 | /ɝ/ (/ɚ/ sin acento) | er (her), ir (bird), ur (turn), or tras w (work), ear (learn), our (journey); sin acento: er (teacher), or (doctor), ar (dollar) | bird, girl, nurse | ❌ no existe; el hispanohablante la lee como "er/ir/ur" con vocal española y r vibrante |
| 16 | /ɑr/ | ar (car), ear (heart), uar (guard) | car, star, park | 🟡 "ar", pero con r inglesa (sin vibrar) |
| 17 | /ɔr/ | or (for), ore (more), oor (door), our (four), oar (board), ar tras w (warm) | for, horse, door | 🟡 "or", con r inglesa |
| 18 | /ɛr/ | air (hair), are (care), ear (bear), ere (where), eir (their) | chair, care, bear | 🟡 "er", con r inglesa |
| 19 | /ɪr/ | ear (ear, hear), eer (deer), ere (here), ier (pier) | ear, hear, deer | 🟡 "ir", con r inglesa |
| 20 | /ʊr/ (marginal en GA; muchos dicen /ɔr/ o /ɝ/) | ure (sure, cure), our (tour) | sure, tour, pure | 🟡 |

> **Simplificación para el Nivel 0.** /ʊr/ no se enseña como unidad. "sure, tour, pure" pueden ir como palabras de corazón. /ɔ/ se trata como variante de /ɑ/ (mismo color, con una marca opcional).

### 1.4 Consonantes (24)

| # | IPA | Grafías (frecuencia) | Palabras clave | Español |
|---|---|---|---|---|
| 21 | /p/ | p, pp | pen, map, apple | 🟡 existe, pero sin la aspiración inglesa en posición inicial (pʰen) |
| 22 | /b/ | b, bb | bus, bed, cab | 🟡 existe; entre vocales el español la suaviza a [β] |
| 23 | /t/ | t, tt, ed (jumped) | ten, cat, top | 🟡 sin aspiración; en GA hay "flap" entre vocales (water ≈ "wader") |
| 24 | /d/ | d, dd, ed (played) | dog, bed, red | 🟡 entre vocales el español la suaviza a [ð] (dedo) |
| 25 | /k/ | c (cat), k (kit), ck (back), ch (school), q(u) (queen), x = /ks/ | cat, kid, duck | 🟡 sin aspiración |
| 26 | /g/ | g, gg, gu (guess), gh (ghost) | go, bag, dog | 🟡 entre vocales el español la suaviza a [ɣ] |
| 27 | /f/ | f, ff, ph (phone), gh (laugh) | fish, fun, off | ✅ |
| 28 | /v/ | v, f (of) | van, very, five | ❌ el hispanohablante la pronuncia como /b/ (van = ban). Dientes superiores sobre el labio inferior |
| 29 | /θ/ | th (think, bath) | think, three, math | ❌ en Latinoamérica (✅ en España: "z/c" de *cielo*). El hispanohablante la cambia por t/s/f |
| 30 | /ð/ | th (this, the, mother) | the, this, mother | 🟡 existe como alófono de /d/ entre vocales (dedo [ˈdeðo]), pero no al inicio de palabra; el hispanohablante dice "de", "dis" |
| 31 | /s/ | s, ss, c(e/i/y) (city, face), sc (science) | sun, bus, city | ✅ (cuidado con las s iniciales en grupo: s + consonante) |
| 32 | /z/ | s (is, dogs, rose), z, zz, x (xylophone) | zoo, is, nose | ❌/🟡 solo existe como alófono (mismo [ˈmizmo]); el hispanohablante la ensordece a /s/ |
| 33 | /ʃ/ | sh (ship), ti (nation), ci (special), ch (chef), s (sure) | ship, fish, she | 🟡 existe en algunos dialectos (Chile "sh" por ch; sheísmo rioplatense); muchos dicen /s/ o /tʃ/ |
| 34 | /ʒ/ | s (usually, vision), g (beige), si (Asia) | usually, TV/vision, measure | 🟡 "ll/y" rioplatense; rara en el resto de dialectos |
| 35 | /h/ | h, wh (who) | hat, hello, house | 🟡 la "j" española es más áspera (velar); la h inglesa es solo aire ("vaho en un vidrio") |
| 36 | /tʃ/ | ch (chip), tch (catch), t (nature) | chair, much, lunch | ✅ |
| 37 | /dʒ/ | j (job), g(e/i/y) (gem, page), dge (bridge) | job, juice, page | 🟡 como "y/ll" enfática ("¡yo!"); el hispanohablante dice "y" suave o "j" española |
| 38 | /m/ | m, mm, mb (lamb) | man, mom, map | ✅ |
| 39 | /n/ | n, nn, kn (know) | no, ten, sun | ✅ |
| 40 | /ŋ/ | ng (sing), n antes de k/g (bank, finger) | sing, king, long | 🟡 existe antes de k/g (banco), pero no a final de palabra; el hispanohablante añade /g/ ("sing‑g") o la cambia por /n/ |
| 41 | /l/ | l, ll | leg, bell, milk | 🟡 la "l" final inglesa es oscura [ɫ] (milk, ball) |
| 42 | /r/ (ɹ) | r, rr, wr (write) | red, run, car | ❌ la lengua no toca el paladar; el hispanohablante la hace vibrante simple o múltiple |
| 43 | /w/ | w, wh (when), u (queen) | we, wet, when | ✅ como "hu/gu" (hueso, agua); a veces aparece un /g/ intrusivo ("gwet") |
| 44 | /j/ | y (yes), u = /ju/ (use) | yes, you, yellow | ✅/🟡 y = "i" consonántica; ojo con el rehilamiento /ʒ/ o /dʒ/ ("you" ≠ "chu") |

### 1.5 Problemas contrastivos que NO son fonemas sueltos (prioridad alta)

| Fenómeno | Error típico del hispanohablante | Remedio didáctico |
|---|---|---|
| **s inicial + consonante** (st, sp, sk, sm, sn, sl, sw) | "eschool", "espeak", "estop" (epéntesis) | "Silbido de serpiente": alargar la s ("ssss‑top") sin vocal antes. Ejercicio de cronómetro: s → stop |
| **Consonantes finales y grupos finales** (‑st, ‑nd, ‑ks, ‑lt, ‑mp) | omitirlas (*bes* por best) o añadir vocal (*besta*) | marcarlas visualmente con un "punto final" brillante; audio lento → rápido |
| **Ensordecimiento final** | bag→"bak", his→"his/s", five→"faif" | regla de la vibración: mano en la garganta |
| **Finales -s/-es** (3 sonidos: /s/ cats, /z/ dogs, /ɪz/ buses) | todo /s/, o añadir "es" siempre | ver la Unidad 14 |
| **Finales -ed** (3 sonidos: /t/ worked, /d/ played, /ɪd/ wanted) | "work‑ed" con sílaba extra | ver la Unidad 14 |
| **Aspiración p/t/k** | pin suena a "bin", ten a "den" | prueba de la servilleta o la vela |
| **Duración vocálica ante sonora/sorda** | bead/beat iguales | estirar la vocal antes de una consonante sonora |
| **Acento léxico** | ho‑TEL bien, pero DOC‑tor → doc‑TOR, a‑ni‑MAL, his‑to‑RY | círculos grande/pequeño (● • •) y cognados con acento cambiado |
| **Ritmo acentual y reducción** (schwa en palabras función: a, the, to, of, and, can) | todas las sílabas con la misma fuerza ("ritmo de ametralladora") | "palabras perezosas": se muestran en gris y pequeñas |
| **Lectura "a la española"** (letra = sonido fijo) | leer "name" como /náme/, "five" como /fíve/ | ¡es el núcleo del Nivel 0! "En inglés las letras son disfraces: la misma letra suena distinto" |

---

## 2. Las "muchas lecturas" de cada vocal (material de motivación para el adulto)

Este bloque responde directamente a lo que pide el cliente. Conviene enseñarlo como un "descubrimiento" en la Unidad 1 y como un mapa que se va completando en cada unidad. No hay que enseñarlo todo de golpe.

| Letra | Lecturas principales (GA) | Ejemplos |
|---|---|---|
| **a** | /æ/ corta · /eɪ/ "dice su nombre" · /ɑ/ · /ɔ/ · /ə/ sin acento · /ɛr/ · irregulares | apple, ant, cat, **ask** (en GA es /æ/; en el inglés británico es /ɑː/) · mate, fate, ape, cake, rain, day · father, car · ball, talk, saw · about, banana · care · any (/ɛ/), was (/ʌ/) |
| **e** | /ɛ/ · /iː/ · muda (e mágica) · /ə/ · /ɝ/ | egg, bed · me, be, these, see, eat · cake, home · the, taken · her |
| **i** | /ɪ/ · /aɪ/ · /iː/ · /ɝ/ · /ə/ | it, sit, intelligence (/ɪnˈtɛlɪdʒəns/: las dos i son /ɪ/) · I, ice, kite, hi, night · pizza, machine · bird, girl · pencil |
| **o** | /ɑ/ · /oʊ/ · /ʌ/ · /uː/ · /ɔr/ · /ə/ · /ɪ/ | hot, box · go, no, home, boat · son, love, come · do, to · for · lemon · women |
| **u** | /ʌ/ · /juː/ · /uː/ · /ʊ/ · /ɝ/ · /ɪ/ | up, cup, bus · cute, use, music · rule, June · put, full · turn · busy |
| **y** | /j/ · /aɪ/ · /i/ · /ɪ/ | yes, you · my, fly, why · happy, baby, very · gym |
| **oo** | /uː/ larga · /ʊ/ corta · /ɔr/ · /ʌ/ | moon, food, school, choose, goose · book, look, good, foot · door, floor · blood |
| **ow** | /oʊ/ · /aʊ/ | snow, show, slow · cow, now, how |
| **ea** | /iː/ · /ɛ/ · /eɪ/ | eat, sea, tea · bread, head · great, break |

> **Precisión sobre "familias que riman".** *choose* y *goose* comparten la vocal /uː/ (misma "familia de color"), pero **no riman exactamente**: choose termina en /z/ y goose en /s/. Rimas exactas: **goose / loose / moose** y **choose / lose / news / shoes**. Conviene enseñar dos conceptos: "familia de sonido" (misma vocal acentuada) y "familia de rima" (misma vocal + final; *onset‑rime*).

**Heurísticas para adultos (con su honestidad estadística):**
1. Vocal sola entre consonantes (CVC: cat, sit, hot) → **corta**.
2. Vocal + consonante + e final (CVCe: cake, kite, home, cute) → **larga** ("dice su nombre"). La e no suena.
3. Vocal al final de una sílaba abierta (go, me, hi, ba‑by) → **larga**.
4. Vocal + r → **sonido nuevo** (car, for, her, bird, turn).
5. Vocal sin acento → casi siempre **schwa** /ə/.
6. Dos vocales juntas → "la primera dice su nombre" (rain, boat, seat). **Ojo**: Clymer (1963) encontró que esta regla solo se cumple en ~45 % de los casos. Por eso conviene enseñar cada equipo vocálico por separado (ai, oa, ee, ea…) y no la regla general.

---

## 3. Orden de enseñanza recomendado (adultos, cero absoluto)

### 3.1 Principios (de SSP adaptado a adultos)
- **Primero los sonidos, luego los nombres de las letras.** Para un adulto el nombre de las letras es útil desde muy pronto: deletrear su nombre, su correo, una dirección. Propongo **separarlos claramente**: Unidad 2 = "nombres" (para deletrear), Unidades 3+ = "sonidos" (para leer). La NAEYC advierte que los nombres de letras confunden si se mezclan con los sonidos.
- **Sonidos "puros"**: /m/ = "mmm", no "muh"; /t/ = soplo corto, no "tuh". Así lo pide expresamente la DfE para facilitar el blending.
- **Orden de alta utilidad**: s a t i p n primero (Jolly Phonics y Letters and Sounds), porque con 6 letras se forman muchísimas palabras CVC (sat, pin, tap, nap, pit…).
- **Ritmo**: un niño ve unos 4 sonidos por semana en la Fase 2. Un adulto alfabetizado en español puede ver **2–4 GPC nuevas por lección** si el sonido existe en español, y **1–2** si es un sonido nuevo (/æ/, /ɪ/, /ʌ/, /v/, th, /ɝ/).
- **Decodificable**: cada frase de lectura usa solo las GPC ya enseñadas y las palabras de corazón ya vistas (requisito de los programas validados por la DfE).
- **Palabras de corazón (heart words)**: se enseñan marcando con ❤️ solo la parte irregular ("the": th es regular, solo la e es "de corazón"). Según el análisis de Farrell y Hunter, solo 82 de las 220 palabras Dolch (37 %) tienen partes irregulares. El resto se decodifica.
- **Chunks orales de supervivencia desde el día 1** (hello, thank you, my name is…), aprendidos de oído como bloque. Más tarde se "descubre" cómo se leen. Esto mantiene la motivación del adulto.

### 3.2 Secuencia (con cantidades)

| Etapa | Contenido | GPC nuevas | Palabras por patrón |
|---|---|---|---|
| A | Chunks orales + concepto "letras ≠ sonidos" | 0 | 10 frases |
| B | Alfabeto: **nombres** de letras (para deletrear) | 26 nombres en 7 grupos de rima | — |
| C | **Sonidos de letras + vocales cortas en CVC**: s a t i p n → m d → c/k ck e h r → b f l ff ll ss → g o u → j v w x y z qu | ~30 | 8–12 por vocal, familias -at -an -ap -it -in -ig -ot -op -ug -un -et -en |
| D | **Dígrafos consonánticos**: sh, ch/tch, th (sorda/sonora), wh, ck, ng, nk, ph | 9 | 8–12 cada uno + pares mínimos |
| E | **Grupos (blends) y finales**: s‑ (st sp sk sm sn sl sw), l‑ (bl cl fl gl pl sl), r‑ (br cr dr fr gr tr), finales (‑st ‑nd ‑nt ‑mp ‑lk ‑sk ‑ft ‑xt) | 0 GPC (combinatoria) | 10 por grupo |
| F | **E mágica / split digraph**: a_e, i_e, o_e, u_e (/juː/ y /uː/), e_e | 5 | 10 cada uno + pares cap/cape |
| G | **Equipos vocálicos largos**: ee/ea, ai/ay, oa/ow/o, igh/ie/y, oo largo/ue/ew | ~14 | 8–12 cada uno + pares ɪ/iː |
| H | **Otros equipos**: oo corto, ou/ow (/aʊ/), oi/oy, au/aw/al | ~8 | 8–10 cada uno |
| I | **Vocales con R**: ar; or/ore/oor/our; er/ir/ur/(w)or; air/are/ear(bear); ear/eer/ere | ~14 | 8–10 cada uno |
| J | **Letras camaleón**: c y g suaves; y como vocal (my / happy); letras mudas (kn, wr, mb, gh, h, t, l) | ~12 | 8 cada uno |
| K | **Schwa y acento**: sílabas débiles, palabras función reducidas, patrones ●• •● •●• ●•• | — | 10 por patrón |
| L | **Finales -s/-es (3 sonidos) y -ed (3 sonidos)** | 6 | 8 por sonido |
| ★ | **Palabras de corazón**: 3–5 por unidad, 40–50 en total | — | — |

---

## 4. The Color Vowel Chart (Karen Taylor y Shirley Thompson · ELTS)

### 4.1 Los 15 colores y su vocal (2.ª edición, versión del Departamento de Estado de EE. UU.)

Cada frase "color + palabra clave" tiene la misma vocal acentuada en las dos palabras. El chart está organizado como el trapecio vocálico (anterior / central / posterior; alta → baja). Las letras y, w y r de los bordes indican el deslizamiento.

| Color + palabra clave | Vocal (IPA, GA) | Ejemplos |
|---|---|---|
| GREEN TEA | /iː/ (iʸ) | see, teacher, people |
| SILVER PIN | /ɪ/ | it, interesting, fish |
| GRAY DAY | /eɪ/ | rain, say, education |
| RED DRESS | /ɛ/ | bed, bread, friendly |
| BLACK CAT | /æ/ | hat, happy, classroom, fantastic |
| WHITE TIE | /aɪ/ | nice, knife, my |
| OLIVE SOCK | /ɑ/ | hot, strong, biological |
| A CUP OF MUSTARD (en otras versiones MUSTARD CUP) | /ʌ/ | up, love, impressive (sílaba acentuada) |
| PURPLE SHIRT | /ɝ/ (vocal con R) | bird, word, work |
| AUBURN DOG | /ɔ/ | saw, talk, dog |
| ROSE COAT | /oʊ/ | go, home, phone |
| WOODEN HOOK | /ʊ/ | good, book, should |
| BLUE MOON | /uː/ | soup, true, super |
| BROWN COW | /aʊ/ | now, house, about |
| TURQUOISE TOY | /ɔɪ/ | boy, oil, choice |

(La lista y la disposición proceden de la presentación oficial de Taylor y Thompson en americanenglish.state.gov. Las ediciones posteriores de ELTS añaden recursos para las vocales con R, por ejemplo una cara posterior o anexos; no he podido verificar el listado exacto de esos anexos.)

### 4.2 Cómo se usa y por qué funciona con adultos
- **"Trust your ears, not your eyes"**: permite hablar de sonidos **sin nombres de letras ni símbolos IPA**. "¿Cómo se dice *a* en inglés?" → gray, black, mustard, auburn, about, any (6 sonidos distintos para la misma letra).
- **Cada palabra tiene un "color"**: el de la vocal de su **sílaba acentuada**. *Soup* es BLUE, *bread* es RED, *knife* es WHITE, *education* es GRAY, *classroom* es BLACK, *biological* es OLIVE. Así se une la vocal con el **acento**, que según los autores es el factor más importante de la inteligibilidad (lo ilustran con la pirámide prosódica de Judy Gilbert).
- **Puente (Color Vowel Bridge)**: la frase clave conocida sirve de ancla para pronunciar palabras nuevas ("*interesting* es SILVER").
- Técnicas: preguntar "¿de qué color es esta palabra?", gestos con las manos para estirar la vocal acentuada, hacer de "detective" de la sílaba acentuada, ordenar vocabulario por colores, juegos de cartas (patentados) y la app Blue Canoe.
- **Por qué funciona con adultos**: (1) evita el IPA, que para un principiante es otra escritura más que aprender; (2) apoya la memoria con doble codificación, color + palabra + imagen; (3) es metalenguaje compartido: "di esa palabra más GREEN"; (4) pone el foco en la vocal acentuada, que es el error de inteligibilidad más grave del hispanohablante.

### 4.3 Licencia y uso: lo que podemos y no podemos hacer
- **Imagen del chart y anclas visuales**: licencia **CC BY‑NC‑ND 4.0** (atribución, **no comercial**, **sin derivados**). En el aula se puede usar con atribución. **En una app comercial no se puede sin licencia.**
- ELTS ofrece **licencias comerciales** para webs, libros de texto, **software educativo**, etc. Hay que contactarles.
- **"Color Vowel" es marca registrada** (USPTO). Solo los socios con licencia pueden mostrar el logo.
- **Prohíbe expresamente** "modificar el chart o hacer tu propia versión del chart para distribuirla".
- **Patente**: ELTS dice tener una patente sobre su sistema de pistas audiovisuales (juego *Color It Out!*, app Blue Canoe). La patente encontrada es la US 10,446,056 B1 ("Game with visual cueing system and oral‑aural learning routine"; inventores Taylor, Thompson y McIndoo; titular English Language Training Solutions LLC; concedida el 15‑10‑2019). Google Patents la marca como **expirada (15‑10‑2023)**, probablemente por impago de anualidades. **Hay que confirmarlo con un abogado** antes de asumir que está libre. El copyright y la marca siguen vigentes en cualquier caso.
- **¿Podemos diseñar nuestro propio sistema de colores?** Sí, con cautela:
  - Asociar colores a sonidos es una **idea con mucho arte previo**. Por ejemplo, *Words in Colour* de Caleb Gattegno (años 60) o la patente US 6,126,447 "Color‑assonant phonetics system" (2000), que también usa colores cuyo nombre rima con la vocal. Una idea general no se protege por copyright, pero la **expresión concreta** sí: el chart, su disposición en trapecio y las 15 combinaciones color + palabra.
  - **Para minimizar el riesgo**: (1) no usar el nombre ni la marca "Color Vowel"; (2) no reproducir el trapecio con las mismas casillas; (3) **no copiar las 15 parejas color/sonido** ni sus palabras clave (green‑tea, black‑cat…); (4) no usar la fórmula "nombre de color que comparte la vocal". Mejor anclar cada sonido a una **palabra‑imagen** (apple, fish, cake) con un color que no coincida con el de CVC para ese sonido; (5) citar el CVC como inspiración solo en materiales para docentes, si acaso; (6) revisión legal antes del lanzamiento.
  - Alternativa: **licenciar CVC**. Da credibilidad y material probado, pero los colores en inglés ("silver pin", "auburn dog") no ayudan a un hispanohablante de nivel cero: no conoce esas palabras y no sabe pronunciarlas, que es justo lo que intenta aprender.

### 4.4 Propuesta: "Mapa de Sonidos OneLingo" (sistema propio)

Lógica del diseño:
- **Ancla = palabra con imagen**, no nombre de color.
- **Color = categoría** del sonido. Nunca va solo: siempre va acompañado de icono + palabra, por accesibilidad para daltonismo.
- **Las vocales con R heredan el color de la vocal base y llevan una insignia "r"**. Esto es didáctico: vocal + lengua que se curva.
- **La schwa es la "vocal fantasma"**: se dibuja con un contorno gris punteado.
- Ninguna pareja color/sonido coincide con CVC.

| Sonido | Ancla (imagen) | Color OneLingo | Grafías que se colorean así | Otras palabras |
|---|---|---|---|---|
| /æ/ | 🍎 apple | **Rojo** | a | cat, map, bag, hand |
| /ɛ/ | 🍋 lemon | **Amarillo limón** | e, ea, (ai: said) | ten, bed, red, bread |
| /ɪ/ | 🐷 pig | **Rosa** | i, y | sit, fish, gym, big |
| /ɑ/ (+/ɔ/) | 🦊 fox | **Naranja** (/ɔ/: naranja con rayas) | o, a (father), aw/au/al | hot, box, top; saw, ball, talk |
| /ʌ/ | 🟣 plum (ciruela) | **Morado** | u, o (son), ou | sun, bus, cup, love |
| /ʊ/ | 📘 book | **Turquesa** | oo, u (put), ould | good, look, foot, could |
| /ə/ | 👻 "vocal fantasma" (banana, about) | **Gris punteado (sin relleno)** | cualquier vocal sin acento | the, a, about, lemon |
| /iː/ | 🌊 sea | **Azul marino** | ee, ea, e, e_e, y (happy) | see, tree, eat, me |
| /eɪ/ | 🐍 snake | **Verde** | a_e, ai, ay, a | cake, rain, day, name |
| /aɪ/ | 🪁 kite | **Celeste** | i_e, igh, y, i, ie | I, ice, night, my |
| /oʊ/ | 🥇 gold | **Dorado** | o_e, o, oa, ow | go, home, boat, snow |
| /uː/ | 🎈 balloon | **Fucsia** | oo, u_e, ue, ew | moon, food, blue, new |
| /aʊ/ | 🦉 owl | **Lila** | ou, ow | out, house, cow, now |
| /ɔɪ/ | 🪙 coin | **Plateado** | oi, oy | boy, toy, oil |
| /ɝ/ | 🐦 bird | **Marrón** + insignia r | er, ir, ur, (w)or | her, girl, turn, work |
| /ɑr/ | 🚗 car | Naranja + insignia r | ar | star, park, arm |
| /ɔr/ | 🐴 horse | Dorado + insignia r | or, ore, oor, our | for, more, door, four |
| /ɛr/ | 🪑 chair | Amarillo + insignia r | air, are, ear, ere | care, bear, where |
| /ɪr/ | 👂 ear | Rosa + insignia r | ear, eer, ere | hear, deer, here |

**Consonantes**: en negro y sin color, para no saturar. Marcas especiales:
- **Dígrafos**: barra subrayada que une las dos letras (sh, ch, th, ng). La th sonora lleva el icono 🐝 de vibración y la sorda el icono 💨.
- **Letras mudas**: "fantasma" (opacidad 30 %, tachado suave): k̶now, lam̶b̶, nigh̶t̶.
- **E mágica**: la e en gris claro con una flecha curva que salta hacia la vocal, que pasa a mostrar su color "largo".

---

## 5. Didáctica visual "como para niños", adaptada a adultos

### 5.1 Recursos visuales (de Jolly Phonics, Letters and Sounds, Oxford Phonics World y Starfall)

| Recurso | Origen | Adaptación para adultos |
|---|---|---|
| **Imagen‑ancla por sonido** (a = apple) | Jolly Phonics (historia + acción + canción por sonido); Starfall "Vowel Pals" (Zac the Rat, Peg the Hen) | Imágenes de vida adulta: bus, taxi, map, job, bank, phone, coffee (no osos de peluche). Un personaje mascota sí (Lumo), con humor adulto |
| **Gesto / boca** | Acciones de Jolly Phonics | **Mini‑video o animación de la boca** (vista frontal + corte lateral de la lengua) para los sonidos nuevos: th (lengua entre los dientes), v (dientes sobre el labio), r (la lengua no toca), h (vaho en un vidrio), /ɪ/ vs /iː/ (sonrisa relajada vs tensa), /æ/ (boca muy abierta, "como al ver un precio caro") |
| **Botones de sonido** (puntos bajo los grafemas simples, rayas bajo los dígrafos) | Letters and Sounds / DfE | Tocar cada punto reproduce el sonido; deslizar el dedo por la línea mezcla los sonidos (blending) |
| **Color por sonido** | CVC, Gattegno | Mapa de Sonidos OneLingo (sección 4.4) |
| **Fichas de letras para construir palabras** | Todas las SSP | Arrastrar fichas para formar la palabra que se oye (codificar/deletrear) |
| **Cadenas de palabras** (cat→hat→hot→hop→shop) | Práctica SSP | "Cambia una letra": muy eficaz para descubrir que cada letra cuenta |
| **Cajas de Elkonin** (una caja por sonido) | Fonología | "¿Cuántos sonidos tiene *ship*?" → 3 (sh‑i‑p), aunque tenga 4 letras |
| **Familias de rima** (onset + rime) | Wylie y Durrell: 37 rimas generan unas 500 palabras | Ruleta: inicio (c, m, t, b, l) + "‑ake" |
| **"Dilo despacio, luego rápido"** | Blending oral | Deslizador de velocidad: s‑a‑t → ssaat → sat |
| **Textos decodificables** | Requisito de la DfE | Frases útiles para un adulto ("Ben has a job.", "The bus is at ten.") con imagen de comprensión |
| **Pseudopalabras ("alien words")** | Phonics Screening Check (Reino Unido) | Prueban la decodificación pura, sin adivinar por el vocabulario |

### 5.2 Tipos de ejercicio recomendados para la app (por prioridad)

1. **Escucha → toca la imagen** (sonido o palabra → 2–4 imágenes). Discriminación auditiva.
2. **Botones de sonido + deslizar para mezclar** (decodificación guiada).
3. **Pares mínimos** (ship/sheep, cat/cut, van/ban, think/sink): "¿Cuál oíste?". Es el ejercicio central del Sounds tab de Duolingo (sit/seat, bat/but, should/shoe).
4. **Construir la palabra con fichas** a partir del audio (codificación).
5. **Cambia una letra** (cadenas de palabras).
6. **Clasificar por color** (ordenar palabras en "cubetas" de sonido) y **el intruso** ("¿cuál no tiene el sonido 🍎?").
7. **Contar sonidos** (cajas de Elkonin).
8. **Ruleta de rimas** (‑at, ‑ake, ‑ight…).
9. **Leer en voz alta con ASR**, con feedback por fonema en verde, amarillo o rojo, como hace ELSA Speak. Siempre con modo "intentar de nuevo" y sin castigo.
10. **Frase decodificable + imagen** (comprensión).
11. **Toque de acento**: tocar el círculo grande (● • / • ●).
12. **Dictado de letras por su nombre** (deletrear nombre, correo, ciudad).
13. **Palabra de corazón**: aparece con ❤️ sobre la parte irregular, se escucha, se repite y se "fotografía" (flash).
14. **Mini‑diálogo de supervivencia** (hello, my name is…) con un personaje.

### 5.3 Reglas de "niño, pero adulto"
- Explicar **por qué** en español y en una línea ("En inglés, la e final suele ser muda: solo avisa que la vocal dice su nombre").
- Reducir la carga: **una idea nueva por pantalla**, mucho espacio en blanco, fuente grande, sin cursivas, con "a" y "g" de un solo piso (de escuela) en las fichas.
- Usar el español como **puente** solo donde es fiable (ai, au, oi, ch, f, m, n, s…) y avisar con ⚠️ los "falsos amigos de sonido" (e→/iː/ en *me*, i→/aɪ/ en *I*, u→/ʌ/ en *up*).
- Usar la pronunciación figurada en español ("ei", "bi", "si") **solo para los nombres de las letras** en la Unidad 2. Nunca para /æ/, /ɪ/, /ʌ/, /ə/, /ɝ/, porque fija errores.
- Celebrar los micrologros ("¡Ya lees 40 palabras!") y mostrar el progreso como un **mapa de sonidos que se va coloreando**.

---

## 6. Precaución técnica: audio y TTS para fonemas

### 6.1 El problema
- Los motores TTS están entrenados para **palabras y frases**. Si se les pide "a" o "/æ/" aislado, suelen leer el **nombre de la letra** (/eɪ/), añadir una schwa ("tuh") o producir ruido. Las consonantes oclusivas aisladas (/p t k b d g/) son casi imposibles de sintetizar de forma "pura".
- Los programas SSP exigen **sonidos puros** (DfE): "mmm", no "muh". Un TTS que añade schwa enseña mal el blending.
- Duolingo, en su Sounds tab, sí reproduce los sonidos aislados al tocar cada casilla. Esto sugiere audio curado, no TTS en tiempo real.

### 6.2 Buenas prácticas recomendadas
1. **Grabar con voz humana (locutor nativo GA, o voz clonada revisada a oído)**:
   - los ~44 fonemas aislados, puros;
   - las versiones **estiradas** de los continuos (sssss, mmmm, fffff, aaaa /æ/, iiii /ɪ/);
   - las palabras **segmentadas** ("s‑a‑t") y **estiradas** ("sssaaat").
   - Son unos 300–600 clips en total. Coste bajo y calidad crítica.
2. **Enseñar siempre a través de la palabra‑ancla**: "/æ/ … /æ/ … apple". El fonema aislado es apoyo; la palabra es la referencia.
3. **TTS (ElevenLabs u otro) solo para palabras y frases completas**, **pregeneradas, cacheadas y revisadas a oído**. Nada de generación en vivo en el Nivel 0.
4. **Forzar pronunciaciones con SSML o diccionarios** en las palabras problemáticas (read pasado/presente, live verbo/adjetivo, homógrafos, palabras sueltas en las que el TTS duda):
   - **ElevenLabs**: la etiqueta SSML `<phoneme alphabet="cmu-arpabet" ph="M AE1 D IH0 S AH0 N">Madison</phoneme>` o `alphabet="ipa"` funciona **solo en Eleven Flash v2 / Turbo v2**, solo en inglés y **palabra por palabra**. Recomiendan **CMU Arpabet** por ser más fiable que IPA en v2, y hay que marcar el acento en las palabras de varias sílabas. Los **diccionarios de pronunciación** (.PLS/TXT) con reglas de *fonema* funcionan en **eleven_v3, eleven_v4 y eleven_flash_v2**; en los demás modelos hay que usar reglas de *alias* (escribir la palabra "como suena"). La documentación indica que **v4 mejora el soporte nativo de IPA**. v3 y v4 **no** admiten la etiqueta SSML `<phoneme>` inline.
   - **Azure Speech**: `<phoneme alphabet="ipa" ph="...">` (también sapi, ups, x‑sampa). En IPA no admite espacios; si un fono no se reconoce devuelve un error 400.
   - Ni siquiera con etiquetas de fonema se garantiza una **vocal aislada** limpia, así que hay que grabar.
5. **Evaluar la pronunciación del alumno**: usar un servicio de evaluación con puntuación por fonema (tipo Azure Pronunciation Assessment o el enfoque de ELSA). Umbrales indulgentes en el Nivel 0, con prioridad en la **inteligibilidad** (vocal acentuada, contrastes mínimos) y no en el acento nativo.
6. **Control de calidad**: una lista de verificación por clip (¿suena el nombre de la letra en lugar del sonido? ¿añade schwa? ¿la /æ/ suena como /ɛ/?) revisada por una persona con oído entrenado.

---

## 7. Propuesta concreta: "Nivel 0 · Leer y pronunciar inglés desde cero"

**Formato.** 14 unidades. Cada unidad tiene 5–6 lecciones (4–5 de contenido + 1 de repaso o "jefe"), con 5–8 min por lección y 10–15 ejercicios. En total son ~80 lecciones, unas 8–10 h.

**Por lección.** 1–3 GPC nuevas, 8–12 palabras, 2–3 frases decodificables y 0–2 palabras de corazón ❤️. Cada unidad cierra con una **frase de la vida real**.

Leyenda: 🎨 = color del Mapa de Sonidos (4.4) · ❤️ = palabra de corazón · 🖼️ = idea de imagen.

---

### Unidad 1 · "Hello! Mis primeras palabras" (de oído)
- **Objetivo**: decir y entender 10 chunks sin leerlos todavía; descubrir que "en inglés las letras se disfrazan".
- **Lecciones**:
  1. Hello / Hi / Bye
  2. Yes / No / OK / Please / Thank you
  3. My name is… / I'm…
  4. "¿Cómo se dice *a* en inglés?": apple, cake, car, ball, about (presentación del Mapa de Sonidos con 5 casillas)
  5. Repaso
- **Contenido**: solo audio + imagen + texto "fantasma". El texto se muestra, pero no se exige leerlo.
- **Frase de vida real**: "Hello! My name is ___. Thank you!"

### Unidad 2 · "El abecedario: los nombres de las letras"
- **Objetivo**: decir el nombre de las 26 letras y **deletrear su nombre, apellido y correo**.
- **Grupos por rima** (una lección por grupo o dos):
  - /eɪ/: A H J K
  - /iː/: B C D E G P T V Z(US "zee")
  - /ɛ/: F L M N S X
  - /aɪ/: I Y
  - /oʊ/: O
  - /juː/: Q U W
  - /ɑr/: R
- **Trampas para hispanohablantes**: E se dice "i" y la I se dice "ai"; G ("yi") frente a J ("yei"); A ("ei") frente a E ("i"); H ("eich"); W ("dábel‑iu"); Y ("uai"); V con dientes sobre el labio.
- **Ejercicios**: dictado de letras, "deletrea tu nombre", ¿qué letra oíste? (E/I, G/J, A/E/I).
- **Frase**: "My name is Ana. A‑N‑A."
- ❤️ **I** (la palabra *I* = nombre de la letra I).

### Unidad 3 · "Primeros sonidos: s a t i p n m d" (🎨 🍎 rojo /æ/, 🐷 rosa /ɪ/)
- **Objetivo**: separar el **nombre** de la letra de su **sonido**, mezclar sonidos y leer CVC.
- **Lecciones**:
  1. s, a (/æ/ 🍎 apple, ant)
  2. t, p
  3. i (/ɪ/ 🐷 pig, it), n
  4. m, d
  5. Familias ‑at ‑an ‑ap ‑it ‑in ‑ip
  6. Repaso
- **Palabras**: sat, pat, mat, tap, map, nap, pan, man, an, at, am, dad, mad, sad · sit, pit, tip, sip, pin, tin, dim, did, in, it
- **Pares mínimos**: pan/pin, tap/tip, sat/sit, man/mint (este último solo de escucha)
- ❤️ **the, a, is** ("is": la s suena /z/)
- **Decodificables**: "I am Pam." · "Sam sat." · "It is a map." · "Tim and Dad sat in."
- 🖼️ apple, ant, pig, pin, map, pan, man.

### Unidad 4 · "Más sonidos: c/k ck e h r b f l (ff ll ss)" (🎨 🍋 amarillo /ɛ/)
- **Objetivo**: ampliar el código y presentar /ɛ/.
- **Lecciones**:
  1. c/k/ck
  2. e (/ɛ/ 🍋 lemon, egg)
  3. h (aire, no "j"), r (la lengua no toca)
  4. b, f, l + ff ll ss
  5. Familias ‑et ‑en ‑ed ‑ell ‑ack ‑ick
  6. Repaso
- **Palabras**: cat, can, cap, kid, kit, back, sack, kick, neck · ten, pen, hen, men, net, pet, red, bed, leg (g se previsualiza), bell, sell, tell, less · hat, hit, him, ham · rat, ran, rip, rib · bat, bad, big · fan, fat, fit, fell · lap, lip, lid, left
- **Pares mínimos**: pen/pan, bed/bad, men/man, ten/tan · hat/at (h audible) · fan/van (adelanto)
- ❤️ **he, me, be, we** (e final = nombre), **to**
- **Decodificables**: "Ben has a red cap." (has ❤️ s=/z/) · "Ted fed the ten hens." · "Pat can kick." · "Help!" (adelanto de grupo)
- 🖼️ lemon, egg, hen, bed, bell, cat, kid, hat, red.

### Unidad 5 · "o, u y las letras que faltan: g o u + v w j y z x qu" (🎨 🦊 naranja /ɑ/, 🟣 morado /ʌ/)
- **Objetivo**: completar las 5 vocales cortas y contrastar las vocales "a" del inglés.
- **Lecciones**:
  1. g, o (/ɑ/ 🦊 fox, hot)
  2. u (/ʌ/ 🟣 up, sun)
  3. v vs b ("dientes en el labio"), w
  4. j, y, z, x, qu
  5. Gran repaso de las 5 vocales cortas + familias ‑ot ‑op ‑og ‑ug ‑un ‑ut ‑ig
  6. Repaso
- **Palabras**: dog, hot, pot, top, mop, box, fox, log, not, on, job · up, cup, bus, sun, run, fun, bug, mud, but, cut, nut · van, vet, very(❤️ y=/i/) · web, wet, win · jam, jet, jog · yes, yet · zip, zap · six, fix, mix · quiz, quick
- **Pares mínimos** (núcleo): **cat / cut / cot**, hat / hut / hot, bag / bug, cap / cup, ran / run, fan / fun, map / mop · **van / ban, vet / bet, very / berry** · bus / boss
- ❤️ **you, do, go, no, so, I'm**
- **Decodificables**: "The dog is on the bus." · "Yes, I can run!" · "Get up, Jim! It is ten." · "I have a job." (have ❤️) · "Six cups on top."
- 🖼️ fox, sun, bus, cup, van, web, jam, box.
- **Frase de vida real**: "Yes. No. Thank you. I'm Pam."

### Unidad 6 · "Dos letras, un sonido: sh ch tch th wh ng nk ph"
- **Objetivo**: entender los dígrafos (dos letras = un sonido, con una barra que las une) y los sonidos nuevos /ʃ/, /θ/, /ð/, /ŋ/.
- **Lecciones**:
  1. sh
  2. ch / tch
  3. th sorda 💨 (think) y th sonora 🐝 (this)
  4. wh, ng, nk
  5. ph + repaso con pares mínimos
  6. Repaso
- **Palabras**:
  - sh: ship, shop, shut, shell, fish, dish, wish, cash, she
  - ch: chip, chin, chop, chat, much, rich, lunch, check, catch, match
  - th sorda: thin, thick, think, thank, bath, math, moth, with
  - th sonora: this, that, then, them, they, the
  - wh: when, which, what, whip
  - ng: sing, ring, king, long, song, thing
  - nk: pink, bank, think, sink, drink
  - ph: phone, photo
- **Pares mínimos**: ship/sip, she/see, shell/sell · chip/ship, chin/shin, watch/wash · thin/tin, three/tree, thank/tank, think/sink, math/mass · they/day, then/den · sing/sin, thing/thin
- ❤️ **they, what, said, of**
- **Decodificables**: "This is the fish shop." · "I think that is Beth." · "Chip and Seth chat at lunch." · "Thank you! Bye!"
- 🖼️ ship, fish, chair (adelanto), thumb (adelanto mb), ring, phone.

### Unidad 7 · "Grupos de consonantes: sin 'e' delante y sin vocal al final"
- **Objetivo**: eliminar la "eschool" y el "beste": grupos iniciales y finales.
- **Lecciones**:
  1. s + consonante (st sp sk sm sn sl sw)
  2. l‑grupos (bl cl fl gl pl)
  3. r‑grupos (br cr dr fr gr tr)
  4. Finales (‑st ‑nd ‑nt ‑mp ‑lk ‑sk ‑ft ‑xt)
  5. Grupos de 3 (spr str spl scr) + repaso
  6. Repaso
- **Palabras**:
  - s‑: stop, step, spot, spin, skip, skin, snack, snap, slim, slip, swim, smell, spell, Spanish (acento!), student (adelanto)
  - l‑: black, clap, clock, flag, flat, glad, plan, plus
  - r‑: bring, crab, drum, drink, frog, grab, grin, trip, truck, print
  - finales: best, fast, last, hand, sand, went, tent, jump, lamp, milk, desk, gift, left, next, help
  - 3 consonantes: string, strong, splash, script, street (adelanto)
- **Ejercicio clave**: "Sssss… stop!": audio s alargada → palabra; ASR que penaliza la vocal inicial.
- **Pares mínimos**: sleep/asleep (s inicial), star/estar (contraste con el español), best/bet, hand/had, went/wet
- ❤️ **was, are, one, two**
- **Decodificables**: "Stop! The bus is next." · "Fred has a black truck." · "I can swim fast." · "Help! A crab is on the step." · "I am a student from ___." (student ❤️ adelanto)

### Unidad 8 · "La e mágica: la vocal dice su nombre" (🎨 🐍 verde /eɪ/, 🪁 celeste /aɪ/, 🥇 dorado /oʊ/, 🎈 fucsia /uː/, 🌊 azul /iː/)
- **Objetivo**: leer CVCe y contrastarlas con CVC.
- **Lecciones**:
  1. a_e
  2. i_e
  3. o_e
  4. u_e (/juː/ cute, /uː/ June) + e_e
  5. Palabras "e no‑mágica" ❤️ + repaso
  6. Repaso
- **Animación**: la **e** salta por encima de la consonante y "toca" a la vocal, que cambia de color (🍎 rojo → 🐍 verde).
- **Pares**: cap/cape, tap/tape, mat/mate, hat/hate, can/cane, fat/fate, plan/plane · pin/pine, kit/kite, bit/bite, rid/ride, hid/hide, win/wine, fin/fine · hop/hope, not/note, rob/robe · cub/cube, cut/cute, tub/tube, us/use
- **Palabras**:
  - a_e: cake, make, take, name, game, same, late, plate, snake, ape, ate, gate
  - i_e: bike, kite, time, like, five, nine, nice, ride, smile, white
  - o_e: home, hope, nose, rose, bone, note, joke, phone, stone, those
  - u_e: cute, cube, use, huge, June, rule, flute
  - e_e: these, Pete
- ❤️ **have, give, live, come, some, done, love, one** ("la e no siempre es mágica")
- **Decodificables**: "Hi! My name is Kate." · "I like my bike." · "Mike rode home at nine." · "The cute cat ate the cake." · "These five kites are white."
- **Frase de vida real**: "Hi! I'm Kate. I live in Quito. I like to ride my bike."

### Unidad 9 · "Equipos vocálicos (1): sonidos largos" (🌊 /iː/, 🐍 /eɪ/, 🥇 /oʊ/, 🪁 /aɪ/, 🎈 /uː/)
- **Objetivo**: leer las grafías alternativas de las vocales largas y dominar /ɪ/ vs /iː/.
- **Lecciones**:
  1. ee / ea (+ e de me) — **pares /ɪ/–/iː/**
  2. ai / ay
  3. oa / ow / o (go, old)
  4. igh / ie / y (my)
  5. oo largo / ue / ew
  6. Repaso
- **Palabras**:
  - ee/ea: see, tree, green, three, need, feet, sleep, week, meet · eat, sea, tea, read, teach, clean, team
  - ai/ay: rain, train, wait, paint, mail · day, play, say, may, way, stay, today
  - oa/ow/o: boat, coat, road, soap, goat · snow, show, slow, grow, window · go, no, old, cold, gold
  - igh/ie/y: night, light, right, high, might · pie, tie, lie · my, by, fly, cry, sky, why, try
  - oo/ue/ew: moon, food, school, too, zoo, room, spoon · **goose, loose, moose** (rima) · **choose, lose❤️, news, shoes❤️** (rima en /uːz/) · blue, true, glue · new, few, flew
- **Pares mínimos /ɪ/–/iː/**: ship/sheep, sit/seat, hit/heat, fill/feel, live/leave, chip/cheap, bit/beat, bin/bean, still/steal, it/eat. (Nota interna: pares de riesgo social, como beach/sheet, van en práctica guiada y sin humor que avergüence.)
- **Familias de rima** (Wylie y Durrell): ‑ay, ‑ain, ‑eat, ‑ight, ‑ake, ‑ine, ‑ice
- ❤️ **people, school** ("ch" = /k/), **friend, said** (repaso)
- **Decodificables**: "See you at three." · "The train is late today." · "My coat is in the boat." · "Good night!" (good: adelanto de U10) · "Nice to meet you!"
- **Frase de vida real**: "Hello! My name is Lee. Nice to meet you. See you!"

### Unidad 10 · "Equipos vocálicos (2): oo corto, ou/ow, oi/oy, aw/au/al" (📘 turquesa /ʊ/, 🦉 lila /aʊ/, 🪙 plateado /ɔɪ/, 🦊 naranja rayado /ɔ/)
- **Lecciones**:
  1. oo corto (book) frente a oo largo (moon)
  2. ou / ow = /aʊ/; **ow tiene dos lecturas** (snow 🥇 frente a cow 🦉)
  3. oi / oy
  4. aw / au / al (+ nota: en EE. UU. suena casi como 🦊)
  5. Repaso
- **Palabras**:
  - oo corto: book, look, cook, good, foot, wood, took, stood · could/would/should ❤️
  - ou/ow: out, house, mouse, loud, cloud, mouth, our · cow, now, how, down, town, brown
  - oi/oy: oil, coin, point, voice, join · boy, toy, joy, enjoy
  - aw/au/al: saw, draw, law, paw · sauce, August · all, ball, call, small, talk, walk
- **Pares mínimos**: **food/foot, pool/pull, fool/full, Luke/look** · **snow/now, show/how, bowl/owl** · cot/caught (solo de escucha; para muchos americanos son iguales)
- ❤️ **could, would, should, our, walk, talk** (l muda: adelanto de U12)
- **Decodificables**: "Look at the brown cow!" · "How are you? Good, thank you!" · "The boy has a coin." · "I walk to town."

### Unidad 11 · "Vocales con R: la lengua se curva" (🐦 marrón /ɝ/ + insignias r)
- **Objetivo**: leer y decir ar, or, er/ir/ur, air, ear con la **r inglesa** (sin vibrar).
- **Lecciones**:
  1. ar 🚗
  2. or / ore / oor / our 🐴
  3. er / ir / ur / (w)or 🐦
  4. air / are / ear(bear) / ere 🪑
  5. ear / eer / ere 👂
  6. Repaso
- **Palabras**:
  - ar: car, star, park, far, farm, arm, art, card, smart, start
  - or: for, or, born, corn, horse, short, sport, more, store, door, four, your
  - er/ir/ur/(w)or: her, bird, girl, first, shirt, third, turn, nurse, burger, Thursday, work, word, world
  - air: hair, chair, fair, care, share, square, bear, wear, where, there
  - ear: ear, hear, near, year, dear, deer, here, beer
- **Pares mínimos**: hut/hurt, bun/burn, cut/curt · cat/cart, hat/heart (❤️) · shot/short · bed/bird · head/heard
- ❤️ **where, there, were, heart, work** (repaso)
- **Decodificables**: "My car is in the park." · "Where are you from? I'm from Peru." · "Her first word was 'more'." · "I work on Thursday."
- **Frase de vida real**: "Where are you from? I'm from ___. I work at a store."

### Unidad 12 · "Letras camaleón y letras fantasma"
- **Objetivo**: c y g suaves, y como vocal, letras mudas.
- **Lecciones**:
  1. c suave (ce, ci, cy)
  2. g suave (ge, gi, gy, dge) + excepciones
  3. y: consonante / /aɪ/ / /i/
  4. Mudas 1: kn, wr, mb
  5. Mudas 2: gh, h, t, l, w
  6. Repaso
- **Palabras**:
  - c suave: city, cent, center, face, ice, nice, rice, race, place, pencil, juice
  - g suave: gem, giant, page, age, cage, huge, orange, large, gym, bridge · **excepciones**: get, give, girl, gift
  - y: yes, yellow, you · my, by, fly, why · happy, baby, very, city, funny, family
  - kn/wr/mb: know, knee, knife, knock · write, wrong, wrap · lamb, thumb, climb, comb
  - gh/h/t/l/w: night, light, high, daughter, eight · hour, honest · listen, castle · walk, talk, half, could · two, who, answer
- **Visual**: letras fantasma al 30 % de opacidad; tocar la letra muestra 👻 "¡No sueno!".
- ❤️ **who, two, eight, answer, hour**
- **Decodificables**: "I know the answer." · "Write your name on the page." · "The baby is happy." · "Nice city!"

### Unidad 13 · "La vocal fantasma y el ritmo: schwa y acento" (👻 gris punteado)
- **Objetivo**: reducir las vocales sin acento; reconocer y producir el acento de palabra; ver cómo se reducen las palabras función.
- **Lecciones**:
  1. Schwa en 2 sílabas (about, again, away, today, lemon, seven, pencil, sofa, pizza, panda)
  2. Patrones ●• y •● (TAxi, DOCtor, WAter, MOther, TEAcher / hoTEL, toDAY, aGAIN, aWAY, beGIN)
  3. 3 sílabas •●• y ●•• (baNAna, comPUter, toMAto, poTAto / FAmily, HOSpital, Animal, CAmera, CHOColate)
  4. **Cognados con acento traicionero**: DOC‑tor, HOS‑pi‑tal, A‑ni‑mal, PRO‑blem, CHOC‑late, im‑POR‑tant, FA‑mi‑ly
  5. Palabras perezosas: a /ə/, the /ðə/, to /tə/, of /əv/, and /ən/, can /kən/ ("I can go" frente a "Yes, I CAN")
  6. Repaso
- **Visual**: círculos grandes y pequeños sobre las sílabas; la vocal acentuada lleva su color 🎨 "estirado" y las demás van en gris fantasma. Es una idea compatible con lo que enseña el CVC, que dice que cada palabra tiene un color (el de su vocal acentuada), pero aplicada con el sistema propio.
- **Ejercicios**: toca el círculo grande, "¿de qué color es esta palabra?", eco rítmico con palmas.
- **Decodificables**: "Banana, pizza and chocolate, please." · "My family is at the hospital." · "I want a cup of tea." (*of* reducido)

### Unidad 14 · "Finales que cambian: -s/-es y -ed" + Prueba final
- **Objetivo**: pronunciar bien los finales gramaticales; integrar todo lo anterior.
- **Lecciones**:
  1. -s: /s/ tras sorda, /z/ tras sonora o vocal, /ɪz/ tras s, z, sh, ch, j
  2. -ed: /t/ tras sorda, /d/ tras sonora, /ɪd/ tras t, d
  3. Lectura integrada (párrafo decodificable)
  4. Prueba final (ver abajo)
- **Palabras -s**:
  - /s/: cats, cups, books, maps, likes, stops, hats, works
  - /z/: dogs, beds, cars, plays, bags, goes, lives, friends
  - /ɪz/: buses, boxes, wishes, watches, pages, kisses, noses, oranges
- **Palabras -ed**:
  - /t/: worked, helped, liked, stopped, washed, watched, jumped, looked
  - /d/: played, lived, called, opened, cleaned, rained, smiled, moved
  - /ɪd/: wanted, needed, started, waited, painted, ended, visited, added
- **Regla visual**: 🖐️ mano en la garganta. "Si tu voz está apagada, sigue apagada; si está encendida, sigue encendida." Las palabras con ‑ed /t/ y /d/ **no ganan sílaba** (worked = 1 sílaba).
- **Decodificable final** (párrafo): "Hi! My name is Rosa. I'm from Lima. I work at a store. I like music and books. Yesterday I played with my kids and we watched a film. Nice to meet you!"

---

### ✅ Prueba final del Nivel 0 ("Ya puedo leer inglés")
| Competencia | Prueba | Criterio sugerido |
|---|---|---|
| Saludar y presentarse | Leer y decir: "Hello! My name is ___. I'm from ___. Nice to meet you. Thank you. Bye!" | ASR ≥ 70 % por palabra; vocal acentuada correcta en name, meet, from |
| Deletrear | Deletrear su nombre y una palabra dictada usando los nombres de las letras | 100 % de las letras de su nombre; ≥ 80 % en la dictada |
| 50 palabras frecuentes | Leer 50 palabras en tarjetas flash (abajo) | ≥ 45/50, ≤ 3 s por palabra |
| Decodificar CVC/CVCe | 10 palabras reales + **10 pseudopalabras** (zop, chab, fush, tade, bime, plote, vun, thig, stum, kepe) | ≥ 16/20 |
| Pares mínimos | 12 ítems de escucha (ship/sheep, cat/cut, van/ban, think/sink, full/fool, hut/hurt) | ≥ 80 % |
| Leer en voz alta | Párrafo decodificable de la U14 | Comprensión (3 preguntas con imagen) + ASR ≥ 65 % |

**Las 50 palabras frecuentes del Nivel 0** (tomadas sobre todo de los primeros 100 de Fry, más supervivencia; ❤️ = palabra de corazón):
the❤️, a❤️, I❤️, you❤️, is❤️, are❤️, am, my, your❤️, he, she, it, we, they❤️, to❤️, of❤️, and, in, on, at, for❤️, with, this, that, what❤️, where❤️, who❤️, how, yes, no, not, can, do❤️, go, have❤️, like, see, look, come❤️, here, there❤️, one❤️, two❤️, said❤️, was❤️, be, me, hello, name, from❤️.

(Los 25 primeros de Fry cubren cerca del 30 % de las palabras de los textos escolares y los 100 primeros, aproximadamente la mitad.)

---

## 8. Notas sobre cómo enseñan otros (benchmark)
- **Duolingo (curso de inglés)**: tiene una **pestaña de pronunciación** (icono de boca) con vocales arriba y consonantes abajo. Cada casilla muestra el **símbolo + una palabra ejemplo**, y al tocarla se oye el sonido aislado. Las lecciones se centran en **pares de sonidos** (sit/seat, bat/but, should/shoe), con identificación, discriminación y emparejamiento audio‑palabra. Hay ejercicios "listen then speak" con reconocimiento de voz. Lección para OneLingo: los pares mínimos como columna vertebral funcionan a escala. Pero Duolingo usa IPA, y para un nivel cero conviene **sustituir el IPA por imagen + color**.
- **ELSA Speak**: feedback **por fonema** con código de color (verde, amarillo, rojo). Es un buen modelo para la capa de evaluación; requiere un motor de evaluación de pronunciación.
- **Starfall**: 4 pasos (ABCs → Learn to Read → It's Fun to Read → I'm Reading), personajes por vocal (Vowel Pals) y 15 libritos decodificables CVC.
- **Oxford Phonics World**: 5 niveles (alfabeto → vocales cortas → vocales largas → grupos consonánticos y combinaciones → combinaciones avanzadas). Es una secuencia muy parecida a la propuesta.
- **Jolly Phonics**: 42 sonidos en 7 grupos (s a t i p n / c k e h r m d / g o u l f b / ai j oa ie ee or / z w ng v oo / y x ch sh th / qu ou oi ue er ar). Historia, acción y canción para cada sonido.
- **Letters and Sounds (DfE, 2007)**:
  - Fase 2: s a t p i n m d g o c k ck e u r h b f ff l ll ss, con palabras trampa to, the, no, go, I, into.
  - Fase 3: j v w x y z zz qu ch sh th ng ai ee igh oa oo ar or ur ow oi ear air ure er, con palabras trampa he, she, we, me, be, was, you, they, all, are, my, her.
  - Fase 5: grafías alternativas ay ou ie ea oy ir ue aw wh ph ew oe au a‑e e‑e i‑e o‑e u‑e.

---

## 9. Riesgos y decisiones abiertas
1. **Licencia CVC**: decidir si se licencia o se usa el sistema propio (recomendado). En cualquier caso, hacer una revisión legal antes de publicar.
2. **Audio**: presupuesto para la grabación humana de unos 300–600 clips (fonemas puros, estirados, segmentados).
3. **Motor de evaluación de pronunciación**: elegir proveedor y umbrales indulgentes para el Nivel 0.
4. **Dialecto**: GA en todo el nivel. Marcar como "británico" solo cuando haya diferencias visibles (ask, can't, tomato).
5. **Daltonismo**: el color nunca va solo; siempre se acompaña de icono y palabra‑ancla.
6. **Carga emocional**: los adultos sienten vergüenza al pronunciar. Conviene un modo "practicar en silencio" (solo escuchar y tocar) y un modo "hablar".

---

## Fuentes

- Color Vowel Chart. "Teaching Spoken English with the Color Vowel Chart" (Taylor y Thompson, webinar del Departamento de Estado de EE. UU.): https://americanenglish.state.gov/files/ae/resource_files/teaching_spoken_english_with_the_color_vowel_chart_webinar_presentation_0.pdf
- Color Vowel Chart, guía del profesor (AE): https://educapes.capes.gov.br/bitstream/capes/63039/1/the_color_vowel_chart_teachers_guide_AE.pdf
- Color Vowel: "Can I Use This?" (copyright, CC BY‑NC‑ND, licencias, patente): https://www.colorvowel.com/about-us/copyright
- Color Vowel, licencias: https://www.colorvowel.com/licensing
- Color Vowel, gráfico interactivo: https://www.colorvowel.com/interactive-chart
- Marca COLOR VOWEL (Justia Trademarks): https://trademark.justia.com/865/15/color-86515353.html
- Patente US 10,446,056 B1 (Taylor, Thompson, McIndoo; ELTS): https://patents.google.com/patent/US10446056B1/en
- Patente US 6,126,447 "Color‑assonant phonetics system": https://patents.justia.com/patent/6126447
- American English, recurso Color Vowel Chart: https://americanenglish.state.gov/resources/color-vowel-chart
- Jolly Phonics (Jolly Learning): https://jollylearning.com/en-gb/our-programmes/jolly-phonics
- Grupos de Jolly Phonics (resumen): https://learnphonics.co/jolly-phonics
- DfE, *The Reading Framework* (julio de 2023): https://assets.publishing.service.gov.uk/media/664f600c05e5fe28788fc437/The_reading_framework_.pdf
- DfE, validación de programas SSP: https://dera.ioe.ac.uk/id/eprint/39132/1/Validation%20of%20systematic%20synthetic%20phonics%20programmes%20supporting%20documentation%20-%20GOV.UK.pdf
- Letters and Sounds, Fase 2: https://letters-and-sounds.com/phase-2-introduction/
- Letters and Sounds, Fase 3: https://letters-and-sounds.com/phase-3-introduction/
- Resumen de fases y palabras trampa de Letters and Sounds: https://www.abhps.com/wp-content/uploads/2022/03/Summary-of-Letters-and-sounds-phases-and-tricky-words.pdf
- Oxford Owl, qué es Letters and Sounds: https://home.oxfordowl.co.uk/reading/what-is-letters-and-sounds/
- Oxford Phonics World, guía de la app: https://www.oxfordphonicsworld.com/app-guide/
- Starfall, Learn to Read: https://teach.starfall.com/lv/resources/information/how-to-read
- Starfall (Wikipedia): https://en.wikipedia.org/wiki/Starfall_(website)
- CAL, "Reading and Adult English Language Learners: The Role of the First Language" (digest): https://www.cal.org/caela/esl_resources/digests/reading.html
- CAL, "Teaching Reading to Adult English Language Learners" (guía del formador): https://www.cal.org/caela/scb/III_D_TeachingReading.pdf
- CAL, "How should adult ESL reading instruction differ from ABE reading instruction?": https://www.cal.org/adultesl/pdfs/briefs/how-should-adult-esl-reading-instruction-differ-from-abe-reading-instruction.pdf
- Burt, Peyton y Adams (2003), *Reading and Adult English Language Learners: A Review of the Research*: https://www.semanticscholar.org/paper/Reading-and-Adult-English-Language-Learners:-A-of-Burt-Peyton/4a52476e836809de6b978bfab2934ab3fd96fd10
- CAL, "Teaching Emergent Adult Readers": https://www.cal.org/wp-content/uploads/2022/05/TeachingEmergentAdultReaders.pdf
- Sistemas vocálicos del inglés americano y del español: https://uw.pressbooks.pub/jorgestextbook/chapter/chapter-1/
- Pronunciation Studio, errores de pronunciación de hispanohablantes: https://pronunciationstudio.com/spanish-speakers-english-pronunciation-errors/
- IH Journal, "Pronunciation for Spanish speakers": https://ihworld.com/ih-journal/issues/issue-48/pronunciation-for-spanish-speakers/
- Latino Literacy, "Teaching English Phonics to Spanish‑Speakers": https://www.latinoliteracy.com/teaching-english-phonics-spanish-speakers/
- Universidad de Valladolid, TFM sobre dificultades segmentales: https://uvadoc.uva.es/bitstream/handle/10324/52671/TFM_F_2021_021.pdf?sequence=1
- Iowa State, "‑ed and ‑s endings" (Teaching Pronunciation): https://iastate.pressbooks.pub/teachingpronunciation/chapter/chapter-5-ed-and-s-endings/
- Ellii, pronunciación de los finales de pasado: https://ellii.com/blog/pronunciation-of-past-tense-endings
- Lista Fry, primeras 100 palabras: https://sightwords.com/sight-words/fry/
- Reading Rockets, "A New Model for Teaching High‑Frequency Words" (palabras de corazón): https://www.readingrockets.org/topics/phonics-and-decoding/articles/new-model-teaching-high-frequency-words
- Johnston (1999), "The timing and teaching of word families" (las 37 rimas de Wylie y Durrell): https://libres.uncg.edu/ir/uncg/f/F_Johnston_Timing_1999.pdf
- ILA, limitaciones de las generalizaciones fónicas (Clymer, 45 %): https://www.literacyworldwide.org/blog/literacy-now/2014/04/16/limitations-of-broad-phonics-generalizations-when-two-vowels-go-walking-the-first-one-doesn-t-necessarily-do-the-talking
- NAEYC, los nombres de las letras pueden confundir: https://www.naeyc.org/resources/pubs/yc/mar2015/letter-sound-relationships
- Duolingo, English Sounds tab: https://blog.duolingo.com/duolingo-english-sounds-tab
- ELSA Speak: https://elsaspeak.com/en/new-homepage/
- ELSA Speak, reseña con feedback por fonema: https://e-student.org/elsa-speak-review/
- ElevenLabs, buenas prácticas de TTS (etiquetas de fonema, alias): https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
- ElevenLabs, "Do pauses and SSML phoneme tags work with the API?": https://elevenlabs.io/docs/help-center/technical/do-pauses-and-ssml-phoneme-tags-work-with-the-api
- ElevenLabs, diccionarios de pronunciación: https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries
- Microsoft Azure, pronunciación con SSML: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-pronunciation
- Microsoft Azure, alfabetos fonéticos: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-ssml-phonetic-sets
