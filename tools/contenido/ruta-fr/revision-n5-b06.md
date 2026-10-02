# Revisión N5 · B6 (fr.n5.c26–c30)

GO

Revisor distinto del autor. Se contrastó el bloque con sus 5 fichas (`curriculo/fr/n5.json`, incl. plan de ejercicios), la `nota` del nivel, el reparto de N1–N4, `ENCARGO_RUTA_FR.md` (Por nivel N5 y Calibración 1–10), `ESQUEMA_CONTENIDO.md`, los bloques N5 B1–B5 y las revisiones de N2 como calibración.

Validación (N4 ya integrado, se quitó de `--borrador`): `validar_ruta.py fr --borrador n5-b01 … n5-b06` → **0 errores**. `validar_plan.py fr` → 0 errores y ningún «título de la unidad difiere» para c26–c30 (los títulos conservan los espacios normales de la ficha). La cadena completa b01–b10 solo dio un error ajeno al bloque (c25, B5, «force»), que es de otro agente en curso.

## Veredicto sobre el contenido

Cada clase enseña exactamente lo que dice su ficha (`introduce`: incise-citation, discours-indirect-futur, interrogation-indirecte-passe, verbes-reporte-nuances, prise-de-notes; el resto va como repaso) y contiene los ejercicios planeados en el mismo formato y clave. No hay gramática de clases posteriores: las referencias cruzadas son correctas (c06 condicional pasado, c10 subjuntivo pasado). Anatomía OK (3 explicaciones, tablas, 8 ejemplos, vocabulario 10–12 con las palabras de la ficha, guiada de 5 con `pista`, independiente de 4 sin pista, situación de ≈ 300 palabras con 2 ítems, evaluación con 5–6 ítems puntuables en ≥ 4 formatos; el `escribir` final es `abierta: true` y no cuenta). Tipografía: 0 espacios normales antes de ? ! : ; y 0 apóstrofos rectos. Guías de sonido con las convenciones del Nivel 0 (sh, en/an/on, ü/ö definidas en cada bloque).

## Correcciones aplicadas (clase, ítem, antes → después)

**c26**
- Vocabulario `v-guillemets`, guía de sonido: «lè guiy-mè» / “gheey” → «lè gui-mè» / “ghee-MEH”.
- Tabla p9 «Para leer el informe»: «les travaux terminaient» (no aparece en el texto y es incorrecto) → «les travaux se terminaient» (imparfait de se terminer), como en el diálogo.
- g5 `pista`: «pasado inmediato, futuro y hoy» (impreciso) → «ayer, hoy y mañana».
- e2 `consigna`: añade «(relato en pasado)»; sin eso «aujourd’hui» era una respuesta oral defendible.
- i4 `aceptadas`: añade «Elle a dit qu’elle habitait là depuis un an».

**c27**
- p1 explicación: añade una nota (ES/EN): en la conversación a veces se oye «il a promis qu’il livrera demain», pero en lo escrito y en los ejercicios se aplica la concordancia (conditionnel). Evita que el alumno vea el error de `erroresFrecuentes` como «el francés real».
- e1 y e3 `consigna`: «del relato en pasado» (una sola respuesta: le lendemain / le surlendemain).
- i3 `consigna`: «(con concordancia de tiempos)».

**c28**
- v-question-piege, guía de sonido: «kès-tion» → «kès-tyon» (coherente con el «-syon» de N4).
- i4 `consigna`: «Eres Ana y cuentas lo que pasó…». Antes era ambiguo (3.ª persona también válida) y no había variantes. `aceptadas` añade «Chloé a demandé à Ana pourquoi elle était venue à Paris» y «Chloé lui a demandé pourquoi elle était venue à Paris».

**c29**
- «máster» → «maestría» (español neutro de América) en `contexto` y diálogo; EN «master’s course» → «master’s program».
- e1 `aceptadas`: añade «ait été» («Il nie que le budget ait été dépassé» también es correcto con el hueco antes de «dépassé»).
- i4 `consigna`: fija «usando «prétendre»» (antes «soutenir» podía defenderse).
- Ejemplo «Elle prétend qu’elle a fini le dossier hier», traducción ES: «Afirma (sin que se lo crea)…» → «Afirma (aunque se duda de ello)…».
- v-citation: «si-ta-sion» → «si-ta-syon».

**c30**
- Situación, informe: «plusieurs clients demandent souvent quand le hall sera ouvert» → «demandaient… serait ouvert» (rompía la concordancia de tiempos que el bloque enseña tras «a signalé que»); traducciones ES/EN ajustadas. Tabla p9: «ils demandent» → «ils demandaient».
- Tabla p9: se eliminan la fila duplicada de «électricité» (queda «électricité (f.)») y «habituel / habituels» (no aparece en la situación); la glosa «pres. / OD» → «prés. / resp. / OJ (ordre du jour: orden del día) / pb (problème)» (la abreviatura francesa es OJ, no OD).
- p2 explicación: añade nota sobre el tiempo: en un acta se escribe a menudo el futuro de un acuerdo vigente («aura lieu»), pero al contar lo dicho se aplica la concordancia («aurait lieu», «seraient prévenus»); así el ejemplo del p2 y la situación (aurait lieu) no se contradicen.
- i1 y e1 `aceptadas`: añade «demandé» (válido: «Il a été demandé de + infinitif»).
- i4 `aceptadas`: añade «vingt chaises» y las variantes con «convenu».
- Guías de sonido: «-sion» → «-syon» en abréviation, décisions y action.

## Hechos del reparto confirmados

- Ana trabaja en la recepción del hotel y coordina un pequeño proyecto, la renovación del hall; trata de vous al director (c26, c27, c30) / Ana works at the hotel front desk and coordinates a small project, the lobby renovation; she uses vous with the director.
- Ana escribe al director un informe de una llamada de un cliente que llegaba con su esposa mientras el hall estaba en obras: la recepción provisional está en el salón del desayuno, las obras terminan el viernes, y Ana propone avisar a los clientes antes de su llegada (c26) / Ana writes the director a report of a call from a customer arriving with his wife while the lobby was under construction: the temporary front desk is in the breakfast room, the work ends on Friday, and Ana proposes warning customers before they arrive.
- Ana se reúne con el proveedor de colchones por el hall; el proveedor ya había incumplido plazos en enero y febrero, y Ana propone escribirle para confirmar las fechas por escrito (c27) / Ana meets the mattress supplier about the lobby; he had already missed deadlines in January and February, and Ana proposes writing to him to confirm dates in writing.
- Chloé entrevista a Ana para el boletín de la escuela (se tratan de vous); le aconseja seguir estudiando francés y no evitar el teléfono, que es la dificultad de Ana (le da miedo); Hugo (se tutean) le propone practicar y la llamará esa noche a las 8 (c28) / Chloé interviews Ana for the school newsletter (they use vous); she advises her to keep studying French and not to avoid the phone, which is Ana’s difficulty (it scares her); Hugo (they use tu) offers to practice and will call her that night at 8.
- Hugo, en su maestría, redacta el resumen de una entrevista a un ministro (ficticio) sobre la renovación de una estación; Ana suele releerle los textos y le dice que sus frases son demasiado largas (c29) / Hugo, in his master’s program, writes the summary of an interview with a (fictional) minister about a train station renovation; Ana usually proofreads his texts and tells him his sentences are too long.
- Reunión del 12 de marzo del proyecto del hall (presentes: Ana, coordinadora, y el director; excusada: la responsable de obras): la inauguración, prevista para fines de marzo, se aplaza a abril; el mobiliario se entrega en unas dos semanas; Ana envía el nuevo calendario antes del viernes y escribe el mensaje a los clientes; el director contacta al proveedor el lunes a las 9; próxima revisión de avance el 15 de abril (c30) / March 12 meeting on the lobby project (present: Ana, the coordinator, and the director; excused: the person in charge of the works): the opening, planned for the end of March, is postponed to April; the furniture is delivered in about two weeks; Ana sends the new calendar by Friday and writes the message to customers; the director contacts the supplier on Monday at 9; next progress check is April 15.

Coherentes con N4 (Ana lleva años en el hotel, Hugo en maestría, Ana–Chloé vous, Ana–Hugo tu, Ana–director vous) y con B1–B5 de N5 (Ana en la recepción del hotel en c11; Hugo con su maestría en c08; c28 retoma «bulletin»/entrevista de Chloé como en c01 y c05).

## Sin resolver / notas

- Ninguna palabra francesa retirada o renombrada la usa un bloque posterior de N5 (b07–b10 validan sin errores nuevos): se quitó «habituel / habituels» y «électricité» duplicada, y «ils demandent» → «ils demandaient», «les travaux terminaient» → «se terminaient», todo solo en la tabla p9 de c30 y c26.
- Las cinco situaciones miden 300–309 palabras (mínimo de N5 = 300): correcto pero sin margen. Los diálogos de c26, c27, c29 y c30 son un solo hablante (informe, correo, resumen, notas + acta) y los hablantes son nombres o papeles/documentos en francés («Ana», «Hugo», «Chloé», «Les notes d’Ana», «Le procès-verbal»), igual que en B1–B5 («La préfecture», «La rédaction»).
- Aviso para quien integre: en c30 el acta usa «aura lieu» (explicado) en el p2 y «aurait lieu» en la situación; ambos son coherentes con la nota añadida.
