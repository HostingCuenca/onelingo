# Revisión independiente · N1 francés, bloque 5 (clases 21–25)

- **Archivo:** `tools/contenido/ruta-fr/n1-b05.json` (`fr.n1.c21` … `fr.n1.c25`)
- **Revisor:** IA independiente (no autora), perfil profesor A1 de francés de Francia, con español latinoamericano e inglés americano.
- **Fecha:** 2026-10-01
- **Validación:**
  - `python3 tools/validar_ruta.py fr --borrador tools/contenido/ruta-fr/n1-b05.json` → **0 errores**.
  - Encadenado con B6 (`--borrador n1-b05.json n1-b06.json`) → **0 errores** (antes y después de mis cambios; B6 no usa ninguna palabra que solo enseñe B5).
  - `python3 tools/curriculo/validar_plan.py fr` → 0 errores; ningún aviso «título de la unidad difiere» en c21–c25 (los 10 avisos son de situaciones de B1–B4 y c31).
  - Comprobación propia más estricta que el validador («nada sin enseñar» en respuestas, opciones, audios, tokens, aceptadas, diálogos y pares, contra Fundamentos + B1–B4 + pasos de enseñanza de B5): 0 faltas reales (solo `veux`, que es distractor de `erroresFrecuentes`, el símbolo €, y el rótulo de hablante «La vendeuse» en c23, que es un papel francés permitido).
  - Tipografía: 0 apóstrofos rectos y 0 signos `? ! : ;` sin U+202F en los campos en francés (incluidas las celdas de tablas).
  - Reciclaje (palabras de ejemplos y diálogo ya enseñadas antes): c21 76 %, c22 82 %, c23 75 %, c24 61 %, c25 74 % (mínimo 30 %).

## Veredicto

GO

## Recuentos

| Clase | Concepto | Tarjetas | Ejemplos | Guiada / indep. | Diálogo | Errores frecuentes | Evaluación |
|---|---|---|---|---|---|---|---|
| c21 | je-voudrais | 12 | 8 | 5 / 4 | 6 | 3 | 6 ítems, 6 formatos |
| c22 | partitif | 11 | 8 | 5 / 4 | 6 | 3 | 6 ítems, 6 formatos |
| c23 | nombres-70-99-prix | 11 (antes 12) | 8 | 5 / 4 | 6 | 3 | 6 ítems, 6 formatos |
| c24 | couleurs-vetements | 13 | 8 | 5 / 4 | 6 | 3 | 6 ítems, 6 formatos |
| c25 | demonstratifs-trop | 12 (antes 11) | 8 | 5 / 4 | 6 | 3 | 6 ítems, 6 formatos |

## Contraste con las fichas (c21–c25) y con c26–c50

Cada clase enseña lo que dicen su título, objetivo, gramática, `introduce`, `recicla`, vocabulario, sonido y tarea. Decisiones sobre las elecciones de la autora:

1. **`prendre` solo como «je prends / tu prends» (c22): aceptable.** Hace falta para «decir qué tomas en el desayuno» (objetivo de c22), c36 introduce el verbo completo y la tarjeta ya decía «por ahora tal cual». Cambio: la nota remite ahora explícitamente a la clase 36 y la guía de sonido está corregida (ver abajo). B6 no usa `prends`.
2. **«je voudrais + infinitivo» (payer en c23, essayer en c25): aceptable como frase hecha.** Lo piden las propias fichas («payer par carte / en espèces», «Je voudrais essayer cette veste»). La nota de `payer` aclara que el verbo va tal cual. El infinitivo como estructura (`aimer-infinitif`) sigue siendo de c26.
3. **`pour` (c21): se mantiene.** La ficha incluye «et pour moi…, et pour mon ami…» en su gramática.
4. **`ou` (c23): ELIMINADA.** `et-mais-ou` se introduce en c26 (y B6 ya tiene su propia tarjeta `ou`). Se quitó la tarjeta y toda aparición: la pregunta del vendedor es ahora «Par carte ?» y la respuesta «Oui, par carte» / «Non, en espèces». No queda ningún `ou` francés en B5.
5. **`grand / petit` (c25): se mantiene.** La ficha pide «c’est trop grand» y el objetivo «demasiado grandes o caras»; el femenino (grande, petite) se muestra como pareja léxica, igual que cher / chère. **Aviso para B7/coordinador:** c31 trae `grand / grande`, `petit / petite` como vocabulario nuevo; debe tratarlas como repaso.
6. **`anorak` (c25): faltaba la tarjeta.** Aparecía en la explicación, la tabla y la evaluación (e2) sin traducción. Se añadió la tarjeta (ahora 12).
7. **`lait`, `thé`, `chocolat`** (c21, c22) aparecen en ejemplos o tablas; c36 reintroduce `le lait` en su ficha, sin conflicto (repaso).
8. Marron / orange no figuran en la ficha de c24 (solo noir, blanc, bleu, vert, jaune, rouge); la regla «rouge y jaune no cambian» está explicada. No se añadieron.

## Cambios aplicados (clase · ítem · antes → después)

### Transversal
- **«camarero / camarera» → «mesero / mesera»** (español neutro de América) en todos los textos `es` de c21 (tarjeta `le serveur`: «el mesero / la mesera (camarero / camarera)»; p2, p3, p5, g1, i2, s, e4, etc.).
- **Guías de pronunciación según la calibración 6 del encargo** (j y g suave = «sh», nasales «en/an/on», ü/ö definidas al primer uso del bloque; en inglés «zh»):
  - c21 · tarjeta `je voudrais`: «yö vu-dré» → «shö vu-dré».
  - c21 · p1: se define la «ö» (la e de «deux», labios redondeados) y se añade «je voudrais = «shö vu-dré»» con la nota de que la j se escribe «sh».
  - c24 · p1 (es y en): se quita la comparación con la vieja convención «y» (j’habite = «yabit»). Ahora: «escribimos la j y la g suave como «sh»: jupe = «shüp», jaune = «shon», rouge = «rush»»; inglés «zh» (jupe = “zhüp”). Se definen ü y ö.
  - c24 · tarjetas `jupe` («zhüp» → «shüp») y `jaune / rouge` («zhon» y «ruzh» → «shon» y «rush»).
  - c23 · p1: `cinq` «sénk» → «senk» (nasal in = «en», como «ven» en B3/B4); se añade el aviso «la n escrita después de la vocal solo indica nasalidad» y la definición de ü / ö (es y en).
  - c22 · tarjeta `je prends / tu prends`: la guía «prend» (parecía pronunciarse la d) → «pran»: la d y la s finales no suenan (es y en).

### c21 · Je voudrais un café
- **g3 (escuchar) opciones `en`:** «She asks…» → «The person asks…» (el audio no fija el género del hablante).
- **g5 (ordenar) `aceptadas`:** `Un thé pour moi, s’il vous plaît.` → + `S’il vous plaît, pour moi, un thé.` y `S’il vous plaît, un thé pour moi.`
- **i4 (ordenar) `aceptadas`:** ninguna → `Je voudrais un croissant et un jus d’orange.` (mismos tokens, orden de los dos productos invertido).

### c22 · Du pain, de la confiture
- **g4 pista (es):** «El miel lo hacen las abejas» → «La miel la hacen las abejas» (en español miel es femenina).
- **Tarjeta `je prends / tu prends`:** ver arriba (guía «pran» y remisión a c36).

### c23 · Precios y 70–99
- **Tarjeta `ou`, p9 refs, p3 (es/en), ejemplo p8, i4, diálogo, s2:** eliminada la palabra `ou` (pertenece a c26). Ejemplo: «Par carte ou en espèces ? — En espèces.» → «Par carte ? — Non, en espèces.». i4: opciones «À la caisse. / Par carte. / En espèces.» → «Oui, par carte. / Non, en espèces. / Non, à la caisse.» con la pregunta «Par carte ?» (respuesta: la segunda). Diálogo: «Par carte ou en espèces ?» → «Par carte ?»; Ana: «Par carte, s’il vous plaît.» → «Oui, par carte, s’il vous plaît.»
- **Diálogo, línea 2:** la vendedora no saludaba. Ahora: «Bonjour, madame. Ça coûte quatre-vingt-sept euros cinquante.» (cortesía francesa).
- **Tarjeta `payer`:** nota aclara «el verbo va tal cual, sin cambiar».
- **Error frecuente 3:** «En un precio no se pone «et»» → «Si no nombras los céntimos, no se pone «et»» (deux euros et cinquante centimes sí es válido).
- **g3 (relacionar) pista:** solo explicaba 80 y 90 → «soixante-dix = 60 + 10; quatre-vingts = 4 × 20; quatre-vingt-dix = 4 × 20 + 10».
- **g5 (ordenar) `aceptadas`:** `Le livre, ça coûte combien ?` → + `Combien ça coûte, le livre ?` y `Le livre, combien ça coûte ?`
- **e4 (ordenar) `aceptadas`:** `Le sac, c’est combien ?` → + `Combien c’est, le sac ?` y `Le sac, combien c’est ?`
- **e6 feedback:** «71, 81, 91 y 77.» → cada número con su cifra.

### c24 · La ropa y los colores
- **p2 (es) y error frecuente 1 (es):** «une robe noire (una falda negra)» → «(un vestido negro)» (robe = vestido; falda es jupe).
- **Tarjeta `un pull`:** «un suéter, un jersey» → «un suéter» (jersey es de España).

### c25 · Ce pull, cette robe
- **Tarjeta nueva `un anorak`** («un anorak (chamarra con capucha)» / “an anorak (a hooded jacket)”), añadida a p7.
- **Tarjeta `ce / cet / cette / ces`:** «estos, esas…» → «este, ese / esta, esa / estos, estas, esos, esas».
- **p4 (tabla), fila 3:** `cet anorak` repetido en las dos filas → `cet anorak noir` (suma concordancia con color).
- **p3 (es / en):** «Vous avez la taille M ?» no tenía traducción → se añade «(¿tiene la talla M?)» / “(do you have size M?)”.
- **Diálogo, línea 3:** Ana nunca daba las gracias → «Merci ! Elle est super ! Ça coûte combien ?» (es: «¡Gracias! ¡Es genial! ¿Cuánto cuesta?»).

## Punto por punto del encargo y de la calibración

1. **Francés de Francia.** Verificado: colores (noir/noire, blanc/blanche, bleu/bleue, vert/verte, jaune y rouge invariables); precios («2,50 €» = deux euros cinquante; «0,80 €» = quatre-vingts centimes; «4,80» = quatre euros quatre-vingts); 70–99 (soixante et onze, quatre-vingts con s, quatre-vingt-un sin s ni et, quatre-vingt-dix-sept…); variante de 1990 explicada en el texto (soixante-et-onze) y números en letras con `aceptadas` completas (cifras y sin guion: `70`, `soixante dix`, `85`, `quatre vingt cinq`); cifras de precio con y sin € y con coma o punto (`15,90`, `15.90`, `15 euros 90`…). Cet / cette: cet solo con masculino + vocal; cette con todos los femeninos (écharpe).
2. **Ordenar:** todos los órdenes naturales incluidos (ver g5, i4, e4 y los de c23).
3. **Pistas y relacionar:** pistas específicas de cada ítem; glosas de los `relacionar` distintas entre sí.
4. **Sonidos del día:** c21 (è / ê / ai), c22 (u / e / eu), c23 (consonantes finales de los números; el aviso sobre quatre-vingts), c24 (ch / j / ge), c25 (s / ss / z) son exactos tras las correcciones.
5. **Diálogos:** modelan el objetivo y la cortesía (Bonjour madame / monsieur, s’il vous plaît, merci, Et toi ?, C’est tout, merci). Hablantes: Le serveur, La vendeuse, Ana, Hugo, Léa. Cada comprensión tiene una sola respuesta.
6. **Personajes (coherencia con `personajes`):** Ana (ecuatoriana, recién llegada), Hugo (le encanta el café, cumpleaños en c23/c24), Léa (amiga de Ana y de Hugo). No se fija ninguna edad, oficio ni nacionalidad nueva. Hugo y Ana usan vous con el mesero y la vendedora y se tutean entre amigos.
7. **es y en:** el español usa «tú» y palabras neutras (mesero, suéter, jugo, probador, chamarra); el inglés compara con «I’d like», «I want», «some», «too / very», «this / that».
8. **Anatomía y errores frecuentes:** cumple en las cinco clases (tabla de recuentos).

## No corregido / avisos para el coordinador

1. **c31 (B7):** `grand / grande`, `petit / petite` ya se enseñan en c25 como pareja léxica; c31 debería tratarlas como repaso.
2. **c26 (B6):** `ou` ya no lo trae B5; B6 tiene su propia tarjeta `ou`. No hay nada que ajustar en B6 por mis cambios (no eliminé ni cambié ninguna palabra francesa que B6 use).
3. **Convención j = «sh» en B1–B4:** B2 c08 («yabit», «ya-»), B2 c09 («yem», «yö») y B4 c16 («yö nö süi pa») siguen escribiendo la j como «y». Están integrados y no los toqué; si se quiere uniformar con la calibración 6, hay que corregirlos en `assets/contenido/fr/ruta/`.
4. **c24 · colores:** `marron` y `orange` (invariables) no están en la ficha de c24; si el coordinador los quiere, irían en c24 como dos tarjetas más junto con la nota de invariabilidad.
