# Revisión independiente · Nivel 0 francés (F6–F10 + inglés de F1–F5)

Revisor: fonética del francés de Francia, español latinoamericano e inglés americano.
Archivos: `u01-u02.json`, `u03-u05.json` (solo la adaptación al inglés y la coherencia), `u06-u07.json`, `u08-u10.json` (revisión completa).
Validador `validar_nivel0.py fr <archivo> --bilingue`: **0 errores en los cuatro** (10 unidades, 40 lecciones). No faltan emoji.

## Veredicto: **GO**

U6–U10 están bien construidas: siguen el orden del PLAN §3.1 (consonantes → on/an → in/un + desnasalización → gn/ill/R/-ent → elisión, enchaînement, liaison y prueba final). Los pares mínimos son válidos (chou/joue, dessert/désert, poisson/poison, bon/banc/bain, ils‿ont/ils sont, un ami/une amie). Las nasales están bien marcadas (on/om, an/en/am/em, in/ain/ein/im/un; un = in, como en el estándar actual); j’ai = `(ai:e)` y j’aime = `(ai:eh)` son correctos; -ent verbal mudo y en de vent/lent nasal, bien separados. Las correcciones son de coherencia, de pistas visuales y de naturalidad del inglés.

## Regla de dígrafos (aplicada a los cuatro archivos)

`=` marca las letras que dan **un solo sonido consonante distinto de leerlas una a una**: `ch`, `ph`, `gn`, `qu`, `gu` (+e/i), `ss` (contrasta con la s que zumba) y la i semivocal `ll`/`ill`/`il` (fi(ll), abe(ill)e, solei(l)). Las consonantes dobles que suenan como la simple (mm, nn, ll de ballon/elle/ville, rr, pp, tt, cc) van sin marca. `th` = t + `(h:_)`, coherente con la h muda.

## Criterio o / oo (actualizado)

Se sigue la transcripción de los diccionarios del francés de Francia, palabra por palabra: **tomate, robot, chocolat** llevan o abierta en sílaba no final ([tɔmat], [ʁɔbo], [ʃɔkɔla]), igual que cochon, orange, école o soleil, que ya estaban así en U6–U10. Antes, chocolat se marcaba `o` en U2 y `oo` en U6. Moto, coco, photo, vélo, dodo y auto se quedan en `o`. Paul es [pɔl] → `(au:oo)`.

## Cambios por tipo

| Tipo | N.º |
|---|---|
| Marcado fonético o/oo (tomate, robot, chocolat en U2; Paul) | 10 |
| Dígrafo `=` (ss en dessus, dessous, impossible) | 6 |
| Francés: ’ (U+2019) en L’enfant; mayúscula al inicio de frase (×3) | 4 |
| Emoji quitado en pares mínimos (solo una opción tenía imagen y daba la respuesta) | 10 |
| Inglés: naturalidad y comparaciones con sonidos del inglés | 10 |
| Inglés: preguntas «has the X of Y» → «in Y» (como en sonidos.json) | 22 |
| Explicación inexacta (ES + EN) | 2 |
| Español: exactitud y naturalidad | 3 |
| **Total** | **67** |

U+202F: ya estaba bien en «Ça va ?», «Bonjour !» y «Vous avez deux enfants ?»; no hay otros ? ! : ; en el francés.

## Ejemplos antes → después

1. **u02 chocolat** `(ch:=)(o:o)c(o:o)l…` → `(ch:=)(o:oo)c(o:oo)l…` (igual que en u06.l01; también tomate `t(o:oo)…` y robot `r(o:oo)b(o:o)(t:_)`).
2. **u10.l04 lee** `P(au:o)l‿(a:a)rr…` → `P(au:oo)l‿…` (Paul [pɔl]).
3. **u03.l04 / u08.l02** `d(e:schwa)ss(ou:ou)(s:_)`, `p(o:oo)ss(i:i)…` → `(ss:=)`, como en tasse, poisson y dessert.
4. **u07.l04 lee** `L'(en:an)f(an:an)(t:_)…` → `L’(en:an)…` (apóstrofo tipográfico, como en U10).
5. **u08.l02 / u10.l02 / u10.l04 lee** `l(un:in)d(i:i), je…`, `(i:i)l‿(h:_)abite à Paris…`, `(i:i)ls‿(on:on)(t:_) un lapin…` → `L…`, `(I:i)l‿…`, `(I:i)ls‿…`.
6. **Pares mínimos** bouche/bouge, chat/chant, va/vent, long/lent, vie/vin, bon/banc/bain, vont/vent/vin, champignon/champion, fil/fille, ville/fille: solo una opción tenía imagen → se quita esa imagen en el paso de escucha.
7. **u08.l02 lumo** «no cierres la boca al final» / «don't close your mouth» (la n no se hace con los labios) → «al final no subas la lengua al paladar» / «don't lift your tongue to the roof of your mouth».
8. **u10.l01 lumo** «La h casi nunca suena» / «almost always silent» (la h nunca suena; lo que varía es si deja pegar) → «La h no suena, así que casi siempre también se pega» / «The h is silent, so words almost always link through it».
9. **u05.l03 EN** «close to the aw in saw» (en buena parte de EE. UU. *saw* suena «sah») → «close to the o in “or”, but shorter».
10. **u08.l01 EN** «say an open «e»… like English «in»: it is one nasal vowel» → «say the e in bed… like English “in”: it's a single nasal vowel, and the n is silent» (comillas inglesas, sin guillemets; igual en «“an apple” sounds like “anapple”»).
11. **u01.l03 EN** «Just like in English, b and v are different sounds in French: the b brings the lips together…» → «As in English, b and v are two different sounds in French: b brings your lips together; v buzzes, with your top teeth on your lower lip.»
12. **u09 ES** «ill (como la y de yo)» (en el Río de la Plata esa y suena «sh») → «como la y de «hoy»», en el objetivo y en u09.l02.

Otros cambios en inglés: a de father «but shorter»; «Nasals come next» → «Later on: the nasal vowels…» (antes vienen las consonantes de U6); «In the French of France» → «In standard French from France»; «it is» → «it's». En español: «un café pequeño negro» → «un café negro pequeño».

## Notas

- **Emoji nuevos: ninguno.** Agneau usa 1f411, el mismo emoji que mouton (U7). Se acepta porque aparecen en unidades distintas.
- `assets/contenido/fr/nivel0/nivel0.json` (U1–U5 publicadas) todavía tiene tomate, robot y chocolat con `o` y dessus/dessous sin `=`. Hay que reconstruirlo desde estos borradores.
- Palabras de riesgo para el diccionario de pronunciación del TTS: est, ils ont / ils sont, dix ans, un ami, aiment (‑ent mudo), Paul, dessert / désert.
- La revisión de un nativo sigue pendiente antes de publicar (PLAN §7).
