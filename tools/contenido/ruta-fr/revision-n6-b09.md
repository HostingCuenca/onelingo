# Revisión N6 · B9 (fr.n6.c41–c45)

GO

Revisor independiente (autor distinto). Bloque contrastado con las 5 fichas de `curriculo/fr/n6.json` (incl. `ejercicios`), la `nota` del nivel, `ENCARGO_RUTA_FR.md` (calibración 1–13), `ESQUEMA_CONTENIDO.md`, el reparto de N1–N5 y los bloques N6 b01–b08 y b10.

## Validación

- `python3 tools/validar_ruta.py fr --borrador n6-b01 … n6-b09` → **0 errores** (también 0 errores añadiendo `n6-b10.json`: ninguna palabra retirada la usa el bloque 10).
- `python3 tools/curriculo/validar_plan.py fr` → 0 errores; ningún «título de la unidad difiere» para fr.n6.c41–c45 (el único aviso de títulos es de fr.n8.c06, ajeno al bloque).
- Tipografía: U+202F antes de ? ! : ; y dentro de « », apóstrofo ’ (único `'` restante: variante `D'après` en `aceptadas`, que el validador normaliza).

## Fidelidad a las fichas

- Cada clase enseña exactamente `gramatica` / `introduce` / `recicla` y las palabras de la ficha; las extras (écran, comparer, INSEE, fraude, parier, assister à, remplacer, tuteur, quant à, uniquement, publier, harceler, nuire à…) son necesarias para los ejercicios y están en tarjeta o tabla (vocabulario estricto, punto 11).
- Ejercicios del plan: los 5 guiada + 4 independiente + 2 situación + 6 evaluación de cada ficha están, con el mismo formato y clave (redacción pulida; en c42 el audio y alguna opción difieren de la ficha pero evalúan lo mismo). En c43 se corrigió respecto a la ficha: el audio de evaluación usa «émergeront» (futuro tras «il est fort probable que»), no el subjuntivo de la ficha.
- Nada de clases posteriores (c46–c50).
- Situación (Por nivel N5–N7: 300–500 palabras): c41 349 · c42 364 · c43 325 · c44 330 · c45 322. Los ítems de comprensión coinciden con el texto de cada diálogo.
- Evaluación, ≥ 4 ítems puntuables en ≥ 2 formatos (el `escribir` abierto no cuenta): c41 6 (completar, elegir, escuchar, ordenar, relacionar) · c42 5 · c43 5 · c44 5 · c45 5 (completar, elegir, escuchar, ordenar). Los `escribir abierta` tienen `minimoPalabras` ≤ palabras del modelo (punto 13; el validador lo comprueba).
- Formatos del bloque: elegir, escuchar, ordenar, completar, escribir y relacionar (este último añadido en c41, ver abajo).
- Hablantes: nombres (Hugo, Ana, Karim) o papeles en francés («Le rapport», «L’article», «Le tuteur», «Le règlement»). Tratos canónicos respetados: Ana–Hugo tú; Ana–Karim vous (c43); Hugo y Ana–Le tuteur vous (c44); el director de Ana (c45) sin nombre.

## Correcciones aplicadas (clase · ítem · antes → después)

**c41**
1. Diálogo, última línea de Ana, traducción EN: cortada tras «both are correct.» → completa («Send me the full report: tonight I’ll read it and tell you what I think.»).
2. Tarjeta `v-sondage`, nota es: «la d no se une a la a» (sin sentido) → «on es nasal (la n no suena) y -age = «ash»».
3. Tarjeta `v-sondes`, nota: «sondé = sondé / sondée (igual en el plural)» confuso → «sondé y sondée suenan igual y la s del plural no se pronuncia».
4. Tarjeta `v-enquete`, nota: «-ion = «ion»» (inexacto; la on final es nasal) → se explica la on nasal de opinion.
5. e4 (ordenar): `aceptadas` solo tenía «La majorité… selon une enquête.» → se añade «La majorité des sondés, selon une enquête, préfère le numérique.».
6. Evaluación: se añade e6 `relacionar` (un Français sur trois / près de la moitié / plus de la moitié / une minorité de sondés ↔ glosas distintas); el `escribir` abierto pasa de e6 a e7. Es un ítem puntuable extra sobre el punto `proportions-enquete`; no sustituye a ninguno del plan.

**c42**
7. Tarjeta `v-ia`, nota: definía ü en una palabra que no la lleva → se quita; ü se define en `v-numerique`, la primera palabra con ü del bloque (calibración 3).
8. Tarjeta `v-vie-privee`, nota: «la e de «vie» … no se pronuncian como en español» (confuso) → «la e de «vie» no suena y -ée = «é»».
9. i2 (ordenar): `aceptadas` sin la variante con inciso → se añade «Le numérique progresse ; la dépendance, de ce fait, augmente.» (con U+202F).
10. Situación: 302 palabras (en el límite inferior) → 364; se añaden dos líneas (Hugo y Ana) con ejemplo del hotel y petición de precisar quién debe actuar; sin palabras nuevas.

**c43**
11. Explicación p1 y tabla p3: «il y a fort à parier que + futur» como regla cerrada, pero el diálogo usa presente («vous avez déjà une idée», correcto) → «+ indicativo, casi siempre en futuro» (es/en y fila de la tabla).

**c44**
12. Tarjeta `v-quant`, nota: «la t final no suena» (error: en «quant à» la t se une a la a) → «kan-ta … la t final se une a la a».
13. Tarjeta `v-du-moins`, nota: «dü mu-en» (dos sílabas) → «dü mwen».
14. Tarjeta `v-correlation`, nota: «rr = r suave» (engañoso para hispanohablantes) → «rr = una sola r francesa».
15. Réplica de Le tuteur: «écrivez : du moins, tout au plus, ne… que» (antinatural) → «écrivez ces limites avec « du moins », « tout au plus » et « ne… que »» (es/en).
16. Coherencia del tutor (ver abajo): `contexto` es/en y tarjeta `v-tuteur` aclaran que es el profesor de la universidad que dirige el mémoire de Hugo y no su responsable de stage; la primera réplica de Hugo menciona «pour mon mémoire».

**c45**
17. Tarjeta `v-pseudonyme`, nota: «aquí se define ö» (ya se definió en c41/c44) → «ö es la «eu» francesa…».
18. Tabla p6, fila abonné: «Chaque abonné peut publier, mais chaque abonnée peut aussi signaler» (forzado) → «Un abonné ou une abonnée peut signaler un contenu offensant.» (es/en).
19. Tabla p6, fila anonymat: «L’anonymat ne protège pas le harcèlement» (impreciso) → «L’anonymat ne justifie pas le harcèlement.» (es/en).
20. Explicación p3: «no se usa como sujeto» (demasiado absoluto) → «casi nunca es el sujeto» (es/en).
21. s2 (completar «Il est interdit de nuire à ___.»): «quiconque» también sería válido tras «à» → la consigna fija «la palabra formal que significa «los demás»».

**Bloque (es neutro de América)**
22. «máster» (España) → «maestría» (como en `hechosDelReparto`) en contextos, tarjeta `v-tuteur` y traducciones de c41, c42, c44 y c45; «trabajo de fin de máster» → «tesis de maestría (mémoire)».

## Hechos del reparto confirmados

- Hugo recibe de su profesor de la maestría un informe sobre el uso de pantallas para su seminario y lo comenta con Ana (se tutean) (c41). / Hugo gets a report on screen use from his master’s professor for his seminar and discusses it with Ana (they use tu) (c41).
- Ana duerme con el celular junto a la cama y dice que en la recepción del hotel la primera pregunta de los clientes es el wifi (c41). / Ana sleeps with her phone next to the bed and says the first question guests ask at the hotel front desk is about the wifi (c41).
- Hugo escribe para su seminario un texto sobre los efectos de lo digital en la vida diaria y Ana se lo revisa: le dice que es largo (coherente con N5 c29) y que use una idea por frase (c42). / Hugo writes a text for his seminar on the effects of digital technology on everyday life and Ana reviews it: she says it is long (consistent with N5 c29) and to use one idea per sentence (c42).
- En el hotel de Ana la ciberseguridad es una cuestión real: los datos de los clientes deben seguir siendo privados (c42). / At Ana’s hotel cybersecurity is a real issue: guests’ data must stay private (c42).
- Karim y Ana (vous) leen un artículo sobre el trabajo en 2040; Karim piensa que una máquina podría preparar las verduras de su restaurante, pero que sus clientes quizá prefieran un cocinero de verdad, y que su hija cocinará de otra manera que él (c43). / Karim and Ana (vous) read an article on work in 2040; Karim thinks a machine could prepare the vegetables at his restaurant, but his customers may prefer a real cook, and that his daughter will cook differently from him (c43).
- Ana cree que dentro de cinco años quizá el hotel haya instalado una máquina en la recepción para las llegadas, pero que los clientes seguirán prefiriendo hablar con una persona (c43). / Ana thinks that within five years the hotel may have installed a machine at the front desk for arrivals, but that guests will still prefer to talk to a person (c43).
- Le tuteur de Hugo (hombre, vous con Hugo y con Ana) es el profesor de la universidad que dirige su mémoire; es distinto de su responsable de stage (N6 c13); Hugo le presenta con Ana de oyente una nota crítica sobre una encuesta telefónica a jóvenes y redes sociales (más de 3 000 llamadas, 1 000 respuestas, solo jóvenes con teléfono fijo) y añadirá esos límites a su mémoire; reaparece en c48 (c44). / Hugo’s tuteur (a man, vous with Hugo and Ana) is the university teacher who supervises his thesis (mémoire); he is not his internship supervisor (N6 c13); Hugo presents to him, with Ana listening, a critical note on a telephone survey of young people and social media (over 3,000 calls, 1,000 answers, only young people with a landline) and will add those limits to his thesis; he returns in c48 (c44).
- Ana observa que los clientes del hotel que más usan el celular son también los que tienen más trabajo, y por eso no se puede concluir que el celular los canse (c44). / Ana notes that the hotel guests who use their phone the most are also those with the most work, so one cannot conclude that the phone tires them (c44).
- En la página de redes sociales del hotel llegaron esta semana mensajes ofensivos; el director quiere un reglamento claro; Ana lo redacta y Hugo, que se tutea con ella, la ayuda a justificar dos normas (foto de otra persona, moderación) y a cuidar la reputación en línea del hotel (c45). / This week offensive messages arrived on the hotel’s social media page; the director wants clear rules; Ana drafts them and Hugo (they use tu) helps her justify two rules (another person’s photo, moderation) and look after the hotel’s online reputation (c45).

## Sin resolver / avisos para el coordinador

- **«tuteur» en N6 c15 (b03, no editado):** Hugo dice «je me suis fait féliciter par mon tuteur pour mon rapport» en el contexto de su stage, y en c13 habla de «mon responsable de stage». Es compatible con c44/c48 si ese tuteur es el mismo profesor universitario que lee su informe de stage y dirige su mémoire (así lo he fijado en c44); el responsable de stage de c13 sería otra persona, en la empresa. Si el autor de b03 prefería un tutor de empresa, conviene cambiar en c15 «mon tuteur» por «mon responsable de stage». Además `tuteur` se enseña en c44 (tarjeta), después de su uso en el diálogo de c15; el validador no lo marca.
- c41 y c42 hablan del «professeur» y del «séminaire» de Hugo; en c44 es «Le tuteur» y «mon mémoire». Son personas distintas (profesor del seminario / director del mémoire); no hay contradicción, pero ninguna otra clase lo dice.
- La ficha de c43 propone «il est fort probable que les innovations émergent» (subjuntivo) en un audio de evaluación; el bloque usa el futuro, que es lo correcto tras «il est fort probable que». Conviene corregir la ficha si se regenera el plan.
- Palabras retiradas o reformuladas (ninguna usada por b10, comprobado con el validador): «protège» (tabla c45; sigue en el diálogo), «mais / chaque / aussi» de la fila abonné (c45, vocabulario básico enseñado antes).
