# Revisión fr.n9.c16–c20 (N9 · B4, «Reuniones»)

GO

Revisor distinto del autor. Contrastado con las 5 fichas de `curriculo/fr/n9.json` (incluido el plan `ejercicios`), la `nota` del nivel, `n1.json`/`n2.json`, `ENCARGO_RUTA_FR.md` (Por nivel N9 y Calibración 1–15), `ESQUEMA_CONTENIDO.md` y las revisiones de N2/N8.

Validación: `python3 tools/validar_ruta.py fr --borrador n9-b01.json n9-b02.json n9-b03.json n9-b04.json` → 0 errores (N8 ya integrado en `assets/`, quitado de la lista). `python3 tools/curriculo/validar_plan.py fr`: sin «título de la unidad difiere» para c16–c20.

## Resumen de la comprobación

- **Fidelidad a las fichas.** Título, objetivo, gramática, `introduce`/`recicla`, vocabulario (8 palabras por clase, todas en tarjeta), situación y tarea coinciden con las fichas; nada de clases posteriores. Los planes de ejercicios están completos (guiada 5, independiente 4, situación 2, evaluación 6 por clase, mismos formatos y claves).
- **Evaluación.** Cada clase tiene **5 ítems puntuables en 5 formatos** (escuchar, completar, elegir, ordenar, relacionar) + 1 `escribir` abierto (`abierta: true`, modelo ≥ `minimoPalabras`) que no cuenta.
- **Situaciones (palabras del diálogo, N9: 400–700).** c16 431 · c17 472 · c18 433 · c19 405 · c20 421. Dos ítems de comprensión por clase, coherentes con el texto, una sola respuesta, opciones en francés (calibración 14).
- **Anatomía.** explicación(es) → tabla/patrón → ejemplos (8) → vocabulario → guiada con `pista` → independiente sin `pista` → situación → evaluación; 3 `erroresFrecuentes` por clase. Tablas ≤ 11 filas. Hablantes: Ana, Karim, Hugo, Inès, Léo, Madame Mercier.
- **Tipografía.** U+202F antes de ? ! : ; y ’ en todo el francés (555 cadenas revisadas, 0 fallos).

## Arreglos

| Clase | Ítem | Antes → después |
|---|---|---|
| c16–c20 (todas) | nombre de la colega | «Marie» → **«Inès»** en tablas, ejemplos, diálogos (hablante incluido), ítems, `aceptadas`, modelos, errores y contextos (para no confundirla con Marie, la esposa de Joseph de N7). «Inès» se enseña en la tabla de c16 antes de usarse. |
| c16 | tabla p3 | + fila «Nombrar a quien modera»: «Ana est l’animatrice de la réunion.» |
| c16 | situación, línea de Madame Mercier | «l’animateur de réunion, c’est vous, Ana» → «l’animatrice de la réunion, c’est vous, Ana» (feminización de cargos, coherente con c04); traducción es/en ajustada |
| c16 | `erroresFrecuentes` 3 | «Marie sera la secrétaire de séance» (no es incorrecto en francés) → «Je vous propose commencer.» → «Je vous propose de commencer.» (error real del hispanohablante, con explicación es/en) |
| c16, c17, c20 | contexto de la situación | «todos se hablan de vous» → «reunión formal con la directora y un invitado: todos se tratan de vous, aunque entre colegas se tuteen fuera de ella» (c04 establece que en la agencia casi todos se tutean, salvo con la dirección) |
| c18, c19 | contexto de la situación | se quita «todos se hablan de vous» (Ana y Hugo se tutean y no se dirigen directamente; no hay `vous` entre ellos) |
| c17 | contexto | «reunión de seis personas» + «(cinco intervienen, la sexta escucha)» para casar con los 5 hablantes |
| c17 | g4 (ordenar), feedback | «La subordinada temporal va primero» (no es una subordinada) → «El inciso «avant de continuer,» va primero…» |
| c17 | i3 (ordenar) | `aceptadas` + «Pour la prochaine réunion, gardons ce point.» |
| c17 | e4 (ordenar) | `aceptadas` + «Pouvez-vous, en deux mots, conclure ?» |
| c17 | e5 (relacionar) | glosas solapadas («Alguien se desvía del tema» / «Un tema está fuera de la agenda») → «Hay que volver al tema del orden del día» / «Un tema se deja para otro día»; feedback reescrito |
| c18 | i3 (ordenar) | `aceptadas` + «De nos échanges, il ressort que le budget fait débat.» |
| c18 | g4 (ordenar) | `aceptadas` + «Karim préfère le train ; en revanche, Inès préfère l’avion.» |
| c18 | situación, Hugo (es) | «ayuntamiento» → «alcaldía» (español de América, como la `nota` del nivel); en: «city hall’s heritage department» |
| c18 | situación, Karim + síntesis de Madame Mercier | Mercier decía «la majorité accepte deux gammes de prix» sin que nadie lo hubiera aceptado → Karim añade «Deux gammes de prix, pourquoi pas, mais avec de beaux hôtels» (Hugo propone, Inès «pourquoi pas», Karim acepta con condición): la tendencia queda respaldada por el texto |
| c19 | **tablas p5 (subjuntivo)** | Solo 4 filas sueltas (adopter/reporter/voter/lever con nous) → **dos tablas con sentido**: (a) «Un verbo, tres sentidos: voter», paradigma completo de 6 personas en presente / subjuntivo / futuro (je vote – que je vote – je voterai … nous votons – que nous votions – nous voterons … ils votent – qu’ils votent – ils voteront); (b) «¿Un hecho o una propuesta?»: adoptons/adoptions, reportons/reportions, votons/votions, lèvent, con frase y glosa es/en. |
| c19 | explicación p3 | Pasaba rápido por «adoptions, reportions, votions». Ahora enseña el molde (forma ils del presente + -e, -es, -e, -ions, -iez, -ent), por qué se usa el subjuntivo (propuesta, no hecho), que «que nous votions» se escribe como el imparfait pero se reconoce tras «je propose que», la alternativa de + infinitivo con el mismo sujeto y la diferencia con el futuro (infinitivo + -ai, -as, -a, -ons, -ez, -ont: «je voterai»). es y en. Ids de pasos renumerados p1–p12. |
| c19 | i1 | «douze votes pour» → «douze voix pour» (coherente con la clase) |
| c19 | i3 (ordenar) | `aceptadas` + «À la prochaine séance, je propose de reporter le vote.» |
| c19 | s2 | pregunta con «» sin espacio fino (U+202F) → con espacios finos |
| c20 | situación, Ana | «sous peine de retard pour tout le monde» (uso antinatural: «sous peine de» pide sanción o infinitivo) → «faute de quoi tout le monde aura du retard. Il faut le dire tôt.» (traducciones es/en) |
| c20 | e5 (relacionar) | glosas casi iguales («Alguien asume la tarea» / «La tarea se impone a Y») → «X asume la tarea por sí mismo» / «Se asigna la tarea a Y» |
| c20 | i4 (ordenar) | `aceptadas` + «Lundi, la prochaine réunion aura lieu.» |
| c16–c20 | prosa es/en | 82 casos de U+202F antes de «:» fuera de comillas (espaciado francés en texto español/inglés) → eliminados |

## Decisiones que no cambian

- **Preguntas de comprensión de la situación (s2).** Los planes pedían `escribir` «Responde en español…» en las cinco clases; el autor las pasó a `elegir` con opciones en francés (como en N8 y N9-B1, y por la calibración 14). Un `escribir` con respuesta en español no se puede corregir de forma fiable; se acepta el cambio. Mismo «clave» y misma pregunta.
- **Karim como invitado y responsable de acciones** (c16, c17, c20): es lo que piden las fichas (c20: «Karim contacta al hotel»).
- Los modelos de las tareas abiertas (e6) cumplen el mínimo de palabras; el validador lo comprueba.

## Hechos del reparto confirmados

- Ana es chargée de projet en la agencia de turismo cultural que dirige Madame Mercier (se le trata de vous); en c16 modera por primera vez la reunión semanal del equipo (lunes, 9–10 h) / Ana is a project manager (chargée de projet) at the cultural tourism agency run by Madame Mercier (addressed with vous); in c16 she chairs the weekly team meeting for the first time (Monday, 9–10 a.m.)
- Inès es una colega de la agencia (secrétaire de séance en c16, 20); no es Marie, la esposa de Joseph de N7 / Inès is a colleague at the agency (secretary of the meeting in c16, c20); she is not Marie, Joseph’s wife from N7
- Léo es otro colega de la agencia (guardián del tiempo en c16, acapara la palabra en c17, reserva el autobús en c20 y es miembro de la asociación de guías en c19); no es Léa / Léo is another agency colleague (timekeeper in c16, hogs the floor in c17, books the bus in c20, and is a member of the guides’ association in c19); he is not Léa
- En una reunión formal con la directora y un invitado, el equipo se trata de vous, aunque entre colegas se tutean fuera de ella (c04) / In a formal meeting with the director and a guest, the team uses vous, although colleagues use tu outside it (c04)
- Karim (dueño del restaurante) es invitado recurrente del equipo: su restaurante acoge la cena del circuito de marzo (40 personas, número exacto 10 días antes), vigila el tiempo en c16 y contacta al hotel en c20; Ana lo trata de vous / Karim (restaurant owner) is a recurring guest of the team: his restaurant hosts the March tour dinner (40 people, exact count ten days ahead), he keeps time in c16 and contacts the hotel in c20; Ana uses vous with him
- Ana propone un circuito de ocho días en Cuenca en lugar de Quito; Quito ya está en el programa de la agencia y la «piste» de Quito queda descartada; la decisión sobre la fecha (julio u octubre) queda para el viernes / Ana proposes an eight-day tour in Cuenca instead of Quito; Quito is already in the agency’s program and the Quito option is ruled out; the decision on the date (July or October) is set for Friday
- Hugo trabaja en el servicio de patrimonio de la alcaldía y confirma que el centro histórico de Cuenca es patrimonio protegido desde 1999 (c18) / Hugo works in the city hall’s heritage department and confirms that Cuenca’s historic center has been protected heritage since 1999 (c18)
- Hugo preside la asamblea general de la asociación de guías (c19): 17 presentes, quórum de 13, cuota de 40 a 50 euros adoptada por 12 a favor, 3 en contra y 2 abstenciones (Madame Mercier y Ana se abstienen en nombre de la agencia, miembro de la asociación); la comisión de calidad se aplaza (14 votos) / Hugo chairs the general meeting of the guides’ association (c19): 17 present, quorum of 13, fee raise from 40 to 50 euros carried with 12 for, 3 against and 2 abstentions (Madame Mercier and Ana abstain on behalf of the agency, a member of the association); the quality committee is postponed (14 votes)
- Calendario de c20: reunión el lunes 8 a las 9 h; Inès valida el calendario (viernes 12), Karim contacta al hotel (jueves 11), Ana envía el presupuesto (lunes 15), Léo reserva el autobús (miércoles), Inès redacta el acta (mañana); próxima reunión el lunes 15 a las 9 h; el presupuesto de comunicación queda abierto / Calendar in c20: meeting on Monday the 8th at 9 a.m.; Inès approves the schedule (Friday 12th), Karim contacts the hotel (Thursday 11th), Ana sends the budget (Monday 15th), Léo books the bus (Wednesday), Inès writes the minutes (tomorrow); next meeting Monday the 15th at 9 a.m.; the communication budget stays open

## Pendiente / sin resolver

- **`curso.json` → `palabrasLibres`:** «Inès» no está; hoy valida porque se enseña en una tabla de c16. Si algún bloque posterior la usa sin enseñarla, conviene añadirla (junto a Léo y Cuenca, que ya están). Yo no edité `curso.json`.
- No se quitó ni renombró ninguna palabra francesa enseñada que un bloque posterior de N9 pueda necesitar: solo se añadieron formas (animatrice, paradigma de voter, adoptons/reportons/votons, voterai/voteras/…). Se retiró del diálogo de c20 la expresión «sous peine de retard», que nadie más enseña. El borrador de B5/B6/B9 no tiene errores en c16–c20 al validarse junto a este bloque.
