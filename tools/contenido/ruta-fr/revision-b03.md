# Revisión independiente · N1 francés, bloque 3 (clases 11–15)

- **Archivo:** `tools/contenido/ruta-fr/n1-b03.json` (`fr.n1.c11` … `fr.n1.c15`)
- **Revisor:** IA independiente (no autora), perfil profesor A1 de francés de Francia, con español latinoamericano e inglés americano.
- **Fecha:** 2026-10-01
- **Validador:** `python3 tools/validar_ruta.py fr --borrador n1-b01.json n1-b02.json n1-b03.json` → **0 errores**. También 0 errores con solo `n1-b01.json` + `n1-b03.json` (B3 no depende de palabras de B2).
- **Comprobaciones extra (scripts propios):** (a) «nada sin enseñar» más estricto que el validador (solo cuentan ejemplos, vocabulario mostrado, patrón y tablas de F0, B1 y pasos previos de B3): solo quedan los plurales regulares de palabras ya enseñadas y los distractores deliberadamente incorrectos («la école»); (b) tipografía: 0 apóstrofos rectos y 0 signos sin U+202F en campos en francés (única excepción: la variante aceptada `l'` en c12 e2, que es intencional); (c) reciclaje 48–78 % de las palabras de cada clase.

## Veredicto

GO

Bloque sólido: francés correcto, tablas completas (avoir con las 9 personas, números 0–20, posesivos), explicaciones bilingües cortas y la anatomía completa en las 5 clases (explicación, 8 ejemplos, 8–10 vocablos, tabla/patrón, 4 guiados, 4 independientes, situación con 5–6 líneas + 2 ítems, evaluación de 6 ítems con 6 formatos, 3 errores frecuentes). Los 6 formatos aparecen en el bloque (completar 20 · escuchar 15 · elegir 15 · relacionar 10 · ordenar 10 · escribir 10). Los fallos encontrados eran sobre todo de coherencia de personajes, fonética inexacta y algunos ítems con más de una respuesta válida; todos están corregidos.

## Cambios aplicados (antes → después)

### c11 · un/une/des y números 0–10
1. **Sonido del día (ü sin ancla).** «la ü francesa: ün» → «la ü francesa (la u de «tu»): ün» (y su versión en inglés).
2. **`des` sin pronunciación.** Se añade «des» suena «dé» en la explicación p2.
3. **Tabla de números (p4): ö sin definir y regla incompleta.** «six y dix terminan en «s»…» → «six y dix terminan en «s» cuando los dices solos; delante de una palabra que empieza con consonante (six stylos) esa s no suena», más definición de «ö» (e con labios redondeados) y «ü».
4. **g2 feedback inexacto.** «Six suena «sis»; dix suena «dis»» (el audio es «six stylos», donde la x no suena) → «Six empieza con s y dix con d. En «six stylos» la x final casi no se oye».
5. **g3 pista genérica** («Mira las tarjetas de vocabulario») → anclas por palabra (stylo ≈ estilográfica / stylus, sac ≈ saco / sack, clé ≈ clave / clef, chaise ≈ chair).
6. **i1 ordenar: faltaba un orden natural.** Solo «J’ai un sac et deux livres.» → se añade en `aceptadas` «J’ai deux livres et un sac.».
7. **i2 escribir.** Pide el número «en letras» pero aceptaba «7» → se elimina `aceptadas: ["7"]`.
8. **Situación: faltaba devolver la pregunta.** Ana: «Bof… Voilà mon sac.» → «Bof… Et toi ? Voilà mon sac.»; Hugo: «Un livre, deux stylos et une photo.» → «Ça va très bien ! Un livre, deux stylos et une photo.» (cortesía francesa y consistencia con B1).

### c12 · le/la/l’/les
9. **Sonido del día: «lö» con ö sin definir** → «lö: la ö es una e con los labios redondeados».
10. **Tabla p3: plurales evaluados sin enseñar.** Se añaden las filas l’amie / les amies («le-za-mi», igual que les amis), le chat / les chats, la fille / les filles y la maison / les maisons (antes «les amies», «les chats», «les filles» y «les maisons» aparecían en diálogo y evaluación sin haberse mostrado).
11. **g4 relacionar: pista genérica** → «le garçon y l’homme son masculinos; la fille y la femme, femeninos; garçon y fille son jóvenes, homme y femme adultos».
12. **erroresFrecuentes[1].** «la lait → le lait» (palabra no enseñada en todo el bloque) → «la ordinateur → l’ordinateur» (explica elisión y que ordinateur es masculino aunque «computadora» sea femenino en español).

### c13 · avoir
13. **Sonido del día: regla falsa «Si oyes «z», es avoir».** «vous êtes» también lleva z. → «Si después de ils, elles o nous oyes «z», es avoir», y se contrasta nous avons / nous sommes («nu-za-vón» / «nu-som»).
14. **Tabla être/avoir (p6): afirmación falsa «Con avoir oyes el enlace «z»».** → ils/elles/nous: la z delata a avoir; vous: «vous êtes» («vu-zet») y «vous avez» («vu-za-vé») llevan z las dos, hay que oír el final.
15. **Vocablo un examen: fonética incorrecta.** «eg-za-man» (sugiere /ɑ̃/) → «eg-za-mén; la -en final es nasal, como en «chien»».
16. **g3 relacionar: pista poco útil** («ils sont es del verbo être») → «Solo una de las cuatro formas es de être: la que significa «son / están»».
17. **e6 relacionar: glosas casi idénticas.** «on a = tenemos (coloquial)» frente a «nous avons = nosotros tenemos» → par «on a» sustituido por «ils ont = ellos tienen».

### c14 · edad y 11–20
18. **Personajes incoherentes.** Lucas tenía 16 años (ejemplo) y 11 (diálogo) siendo canadiense adulto en B1; Emma 12 y Hugo 15 (ejemplo) frente a Hugo 17 (diálogo) y Hugo universitario (c13); Martin (panadero, profesor y jefe en B1) cumplía 20; Chloé (secretaria/profesora en B1–B2) cumplía 19. Ahora el reparto es único: **Hugo 20, Léa 19, Lucas 18**, y los ejemplos usan «La fille a seize ans», «Le garçon a douze ans et la fille a quinze ans» y «C’est l’anniversaire de Hugo : il a vingt ans !».
19. **Situación.** El cumpleaños pasa de Chloé a Léa (Hugo: «Joyeux anniversaire, Léa !»; Léa: «J’ai dix-neuf ans. Et toi ?»; Hugo: «Moi, j’ai vingt ans. Et Lucas, il a quel âge ?»; Léa: «Lucas ? Il a dix-huit ans.»). s1 con opciones 19 / 20 / 18 y s2 («Lucas a ___ ans» → dix-huit; se quita la variante «11»).
20. **g1 pista** («Del 11 al 16 terminan en -ze») no separaba treize / seize / trois → «Treize empieza con «tr» y termina en «z»; seize empieza con «s»; trois no termina en «z»».
21. **g3 pista genérica** («Mira la tabla») → anclas (quatorze ≈ catorce, onze ≈ once, seize empieza con s, vingt es el único sin -ze).
22. **g4 contexto.** «Preguntas la edad a una señora que no conoces» → «Eres recepcionista y le preguntas la edad a una señora que no conoces» (más natural en francés).
23. **i2 escribir.** Pedía «en letras» pero aceptaba «19» → solo «dix neuf» (sin guion) como variante.
24. **i4 feedback falso.** «la g y la t no suenan» (en «vingt ans» la t suena: «van-tan», como dice el propio sonido del día) → «la g no suena y la t solo se oye ante «ans»».

### c15 · familia y posesivos
25. **Personaje incoherente.** «Le mari de Léa est canadien» (Léa es joven, soltera y tiene hermano de 11 años) → «Le mari de Chloé est canadien» (coincide con B2 c08: Chloé vive en Canadá).
26. **Situación.** Se elimina la frase meta «Es la mini lectura del bloque “Mi familia”» del contexto; el hermano sigue sin nombre («C’est mon frère. Il a onze ans.») para no chocar con Lucas (adulto canadiense de B1). s1 («¿Quién es el chico de la foto?») conserva una sola respuesta.
27. **g3 relacionar: pista genérica** → anclas (frère ≈ fraterno, sœur ≈ sor, fils ≈ filial, mari ≈ marido).
28. **i3 escribir.** Se aceptan las variantes sin ligadura: «J’ai deux soeurs.», «J’ai 2 sœurs.», «J’ai 2 soeurs.».
29. **e5 escribir.** «Sa mère est canadienne» (la madre de Hugo, que es francés en B1/B2) → «Sa mère est française» (consigna y feedback ajustados).

### Tipografía
30. Los espacios normales antes de «?» y «!» en citas francesas de textos de apoyo y en el diálogo nuevo pasan a U+202F.

## Calibración de B1: comprobación punto por punto
1. **ordenar con todos los órdenes:** revisados los 10 ítems; solo c11 i1 tenía otro orden natural (corregido). El resto no admite permutaciones con sus tokens.
2. **Pistas y glosas de relacionar:** corregidas (c11 g3, c12 g4, c13 g3, c13 e6, c14 g1, c14 g3, c15 g3).
3. **Guías de sonido:** corregidas las de z/liaison en c13, la t de «vingt ans» en c14 y la x de «six stylos» en c11; ö/ü definidas en la primera aparición (c11 y c12). Las consonantes finales con r (sœur, père, mère, cours, ordinateur) están anotadas como suenan.
4. **Diálogos:** devuelven «Et toi ?», se despiden o agradecen; los de c14 y c15 ya modelan el objetivo con los datos de los personajes.
5. **Personajes:** reparto fijo en B3 (Hugo francés de 20 años; Léa francesa de 19, con padres franceses y un hermano de 11; Lucas canadiense de 18; Chloé adulta casada con un canadiense). Formas femeninas correctas (étudiante, française, canadienne).

## Notas para el coordinador y el revisor de B2 (no se tocó B2)
- **Incoherencia de personajes entre B1 y B2:** Léa es francesa en B1 c05 pero «elle est canadienne» en B2 c06; Emma es estadounidense en B1 c05 y canadiense en B2 c10. B3 no contradice B1 (no fija la nacionalidad de Emma y Léa es francesa).
- **Solapamiento de progresión B2/B3:** B2 ya usa «un homme / une femme / un garçon / une fille», «une maison», «un appartement» (c06, c08) y enseña le/la/l’/les con aimer (c09) antes de que c11–c12 formalicen un/une y le/la/les. No hay contradicción (las sonoridades coinciden: le «lö», les «lé», nous‿habitons), pero el reciclaje de c12 sube al 76 % con B2 y conviene que c12 siga presentándose como la clase que explica el plural por el artículo.
- **Validación mecánica débil:** el validador solo cuenta como enseñado el vocabulario declarado y las celdas de tablas de las clases previas (no sus ejemplos) y trata «amies» como forma de «ami». Para esta revisión se comprobó además con un script que cada palabra de ítems y diálogos aparece en un paso de enseñanza previo.

## Lo que no se pudo corregir
Nada pendiente.
