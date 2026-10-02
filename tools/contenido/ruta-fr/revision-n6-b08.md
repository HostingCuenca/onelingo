# Revisión N6 · B8 (fr.n6.c36–c40)

GO

Revisor distinto del autor. Contrastado con las 5 fichas de `curriculo/fr/n6.json` (incl. plan de `ejercicios`), la `nota` del nivel, `personajes` y `hechosDelReparto` de N1–N5, `ENCARGO_RUTA_FR.md` (Por nivel N6 + calibración 1–12), `ESQUEMA_CONTENIDO.md` y `PLAN_CLASES.md`.

Validación (n5-b01…b10 + n6-b01…b08): `0 error(es)`. `validar_plan.py fr`: ningún «título de la unidad difiere» (c36–c40 intactos). Sin avisos de contaminación nuevos en el bloque.

## Verificaciones sin cambios

- Contenido = fichas: títulos y objetivos idénticos; vocabulario de cada tarjeta (9, 9, 9, 8, 9 palabras) coincide con la ficha y se muestra en el paso `vocabulario`; nada de clases posteriores; los repasos (`futur-proche/simple`, `infinitif-passé`, `le neutre`, `ce qui/ce que`, `discours indirect`, `conditionnel d’atténuation`, `accord du participe COD`) entran como repaso.
- Plan de ejercicios: cada clase contiene los ítems planeados con el mismo formato y clave (guiada 5, independiente 4, situación 2, evaluación 6). Cambios del autor dentro de lo permitido (p. ej. c36 i1 `présenterai` en vez de `aborderai`; c37 g3 «cela nous amène»; c37 i1 opciones sin la ambigua «dis»).
- Anatomía: explicación (2), tablas, 8 ejemplos, vocabulario, guiada con `pista`, independiente sin pista, situación y evaluación al final. Situaciones de 310–325 palabras en el diálogo (rango N5–N7: 300–500), con 2 ítems de comprensión coherentes con el texto.
- Evaluación: cada clase tiene 5 ítems puntuables (+1 `escribir` con `abierta: true` que no cuenta). Formatos puntuables: c36–c39 completar/elegir/escuchar/ordenar (4 formatos); c40 completar/elegir/escuchar (3). Cumple ≥ 4 ítems y ≥ 2 formatos en las cinco. `relacionar` no aparece porque el plan de ejercicios de estas fichas no lo prevé.
- Tipografía: U+202F antes de `? ! : ;` y dentro de « » en todo el francés; apóstrofo ’ (sin rectos).
- Hablantes: nombres o papeles en francés (Hugo, Ana, Léa, Monsieur Martin, Une étudiante, Un étudiant); ninguno en español.
- Español neutro de América (tú/ustedes, usted en el trato formal, «maestría», «diapositiva», «micrófono») e inglés americano.
- Francés revisado ítem por ítem: reglas del participio (c40) correctas (se COD/COI, COD pospuesto, `vus partir` / `vu organiser`, `en` invariable); una sola respuesta defendible en todos los `elegir`/`completar`.
- Guías de pronunciación con las convenciones del Nivel 0 (sh/zh, nasales «en/an/on», ü y ö definidas al aparecer).

## Correcciones aplicadas

| Clase | Ítem / campo | Antes → después |
|---|---|---|
| c36 | e4 (ordenar) `aceptadas` | faltaba el orden natural «Nous verrons dans un second temps les limites.» → añadido |
| c36 | textos `en` (tabla p5, i4, situación, s1) | «opening-out» (calco poco natural) → «look ahead» (y «a look ahead» en el diálogo) |
| c36 | e6 consigna | «≈ 50 palabras» (modelo de 38) → «≈ 40 palabras» |
| c37 | vocabulario `v-passons-a` nota | «pa-son-za», liaison inexistente → «pa-son a»: la s de passons no suena (es/en) |
| c37 | g1 `aceptadas` | «ensuite» (válido y enseñado en c36) → añadido junto a «à présent» |
| c37 | e6 consigna | «≈ 40 palabras» (modelo de 23) → «≈ 25 palabras» |
| c38 | situación, línea 1 de Hugo | «Merci d’être venus» a Ana y Léa → «Merci d’être venues» |
| c38 | i2 y e4 (ordenar) `aceptadas` | añadidos «C’est, autrement dit, une formation en ligne.» y «C’est, en clair, un diplôme reconnu.» |
| c38 | vocabulario `v-apprenant` es | «el alumno que aprende» → «el aprendiz… (la persona que sigue una formación)», coherente con las traducciones del diálogo |
| c38 | e6 consigna | «≈ 40 palabras» (modelo de 28) → «≈ 30 palabras» |
| c39 | e2 (completar) | «vous demandez pourquoi» → «vous me demandez pourquoi» (la fórmula enseñada) |
| c39 | explicación p2 (es/en) | «Y prends une question à la fois» (mezcla de idiomas) → «Y toma una pregunta a la vez (je prends une question à la fois)» / «take one question at a time (…)» |
| c39 | e5 (ordenar) `aceptadas` | añadido «Je reviendrai dans ma conclusion sur ce point.» |
| c39 | e6 consigna | «≈ 40» → «≈ 30 palabras» |
| c40 | tablas p3 y p4, columna «Error típico» | celdas `texto` con formas incorrectas (se reproducían con audio y contaban como «enseñadas») → celdas `apoyo` con «✗ » delante (sin audio, sin valor de enseñanza); cabecera «Incorrecto ✗ (error típico: no lo copies)» / «Incorrect ✗ (typical mistake: don’t copy it)» y frase en el `texto` de la tabla: «La última columna muestra formas INCORRECTAS (✗)…». Las formas siguen valiendo como distractores (validador 0 errores). |
| c40 | vocabulario `v-memoire` nota es | «mem-war» → «mé-mwar» |
| c40 | situación, línea final de Ana | «tu as compris les trois cas» (eran más de tres) → «tu as compris le principe» (es/en) |
| c40 | `en` de `l’élève` y explicación p2 | «pupil(s)» (británico) → «school student» / «students» |
| c40 | e6 consigna | se mantiene «≈ 40 palabras» (modelo de 39) |

## Hechos del reparto confirmados

- Hugo prepara en su maestría una exposición oral de cinco minutos sobre la formación en línea, con apoyo visual de cinco diapositivas (título, plan, contexto, resultados, conclusión) y un dato de enganche de su encuesta / Hugo is preparing a five-minute oral presentation for his master’s on online training, with five slides (title, outline, context, results, conclusion) and a hook figure from his survey
- La encuesta de Hugo la respondieron cien estudiantes: tres de cada diez ya tienen un curso en línea y sesenta de cada cien creen que el diploma está reconocido por las empresas / One hundred students answered Hugo’s survey: three in ten already take an online course and sixty in a hundred think the diploma is recognized by companies
- Hugo ensaya ante Ana y Léa (c36, c38) y solo con Ana (c37) una charla de tres minutos para el seminario del día siguiente; los tres se tutean / Hugo rehearses in front of Ana and Léa (c36, c38) and only Ana (c37) a three-minute talk for the next day’s seminar; the three use tú with each other
- Monsieur Martin es profesor invitado en el seminario de maestría de Hugo y es profesor de Hugo en la universidad (N1 c19); Hugo le habla de vous y él también de vous a Hugo; Martin corrige y devuelve a Hugo su texto sobre la formación (c39, c40) / Monsieur Martin is a guest professor at Hugo’s master’s seminar and Hugo’s university teacher (N1 c19); Hugo and Martin use vous with each other; Martin marks and returns Hugo’s text on his training course (c39, c40)
- Léa asiste al seminario de Hugo y le pregunta por el papel del formador; Hugo la tutea / Léa attends Hugo’s seminar and asks him about the trainer’s role; Hugo uses tú with her
- Hugo escribe un mémoire (tesina de maestría) que entregará después de corregir los errores de concordancia señalados / Hugo is writing a master’s dissertation (mémoire) that he will hand in after fixing the agreement mistakes marked in red

## Consistencia con N1–N5 y con bloques vecinos

- Martin: N1 lo fija como profesor de Hugo en la universidad (vous mutuo), N2–N5 como profesor de francés de Ana en la escuela. Ser además profesor invitado del seminario de Hugo es compatible. El texto de c40 NO lo llama «tutor» (la ficha dice «su tutor», pero las fichas c44 y c48 usan «Le tuteur» sin nombre para el tutor del máster); así no se contradicen.
- Hugo estudia una maestría desde septiembre (N4, N5): coherente. Ana y Léa se tutean con Hugo; Ana con Martin no aparece en el bloque.
- Nada cambia el reparto canónico (punto 12): no aparecen Roux, Lefort ni Dubois en el bloque.

## Pendiente / no resuelto

- Ninguno bloqueante. Observaciones menores para el coordinador: (1) c36 habla de una exposición de 5 minutos y c37 de una charla de 3 minutos para el seminario (lo fijan las fichas); son dos ensayos distintos y el texto no los confunde. (2) c23 (otro bloque) trata una charla de Hugo sobre consumo; c36–c39 son sobre formación en línea: son charlas distintas.
- Palabras francesas eliminadas o renombradas: ninguna. (Se añadieron solo aceptadas; `venues` no estaba declarada pero la palabra pasa el validador.)
