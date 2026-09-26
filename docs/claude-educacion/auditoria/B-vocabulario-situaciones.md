# Auditoría B — Vocabulario y situaciones (OneLingo)

Agente B · rama `claude/educacion-multilenguaje` · 2026-09-26 · solo lectura del repositorio (este archivo es el único escrito).
Convenciones: nivel interno 0 = Fundamentos (pre-A1), 1–2 = A1, 3–4 = A2, 5–6 = B1, 7–8 = B2, 9–10 = C1. Los IDs de gramática `en-g-*` son **provisionales** (el agente A define los definitivos); cuando coinciden con un tema de `docs/TEMARIO-GRAMATICA-PROPUESTO.json` se reutiliza su slug; `*` = tema que **no existe** en ese temario.

## Resumen

1. **Solo existe vocabulario real en los niveles 0–2** de los 10 idiomas (JSON del pipeline). En los niveles 3–10, `unidadesDe()` (`lib/core/content/curriculum.dart:431-459`) usa `_bancoGenerico`: **6 palabras + 3 frases por nivel, repetidas en las 20 unidades** (48 palabras y 24 frases distintas para 160 unidades). **Ese banco está en inglés y también se sirve a los otros 9 idiomas**, porque no hay `nivel-3..10.json` para ninguno. Así, un alumno de francés en el nivel 3 ve «Bigger / Más grande».
2. Inglés, niveles 0–2 + situaciones + lectura/escucha: **unas 975 formas textuales distintas** (incluye letras, chunks y frases), **no lemas**. Los 9 idiomas restantes rondan las 290–300 formas en los niveles 1–2, más 57 de vocabulario del nivel 0.
3. Situaciones (solo inglés): he verificado las cifras documentadas. Son **50 situaciones, 150 objetivos, 150 + 400 = 550 entradas, 531 formas distintas, 400 ejemplos y 50 patrones con 100 ejemplos**. No hay **diálogo, listening, lectura, práctica guiada ni evaluación de producción**, y ninguna situación declara su nivel. De las 50, **15 usan en su frase objetivo gramática de B1 (nivel 5–6)**, sobre todo present perfect y pasiva, aunque su vocabulario está marcado como `nivelInicial` 1–4 (A1–A2).
4. Para los idiomas distintos del inglés, la pantalla de situación solo muestra un botón «Practicar con el tutor» (`situation_screen.dart:103-110`). El backend tampoco da contexto curricular al tutor (`situaciones.ts:30`: `unit` solo si `idiomaMeta === 'en'`).
5. Propongo una **plantilla de situación como mini-ruta de 12 pasos**, con variantes A1–B2 y un ejemplo completo de restaurante. También propongo un mapa de las 50 situaciones, un esquema **neutral + contenido por idioma** con 4 situaciones iniciales ya redactadas para cada uno de los 10 idiomas, y un **sistema de estados léxicos con repaso espaciado** (hoy no existe ninguno: `vocabularioAprendido` cuenta tarjetas vistas en lecciones completadas, `providers.dart:181`).

## Inventario real de vocabulario (cifras)

Scripts `python3` sobre los JSON. «Únicas» = forma normalizada (minúsculas y sin romanización entre paréntesis).

### Niveles 0–2 por idioma (`assets/contenido/<idioma>/nivel-*.json`)

| Idioma | N0 ítems escritura | N0 vocab (únicas) | N1 vocab / únicas | N1 frases | N1 diálogo (líneas) | N1 examen | N2 vocab / únicas | N2 frases | Únicas N1∪N2 | Solape N1∩N2 | Repeticiones |
|---|---|---|---|---|---|---|---|---|---|---|---|
| en | 36 | 57 | 160 / 160 | 120 | 82 | 60 | 160 / 160 | 120 | 303 | 17 | 17 |
| es | 37 | 57 | 160 / 160 | 120 | 82 | 60 | 160 / 157 | 120 | 298 | 19 | 22 |
| fr | 38 | 57 | 160 / 159 | 120 | 82 | 60 | 160 / 156 | 120 | 295 | 20 | 25 |
| de | 38 | 57 | 160 / 159 | 120 | 82 | 60 | 160 / 158 | 120 | 302 | 15 | 18 |
| pt | 36 | 57 | 160 / 158 | 120 | 82 | 60 | 160 / 154 | 120 | 294 | 18 | 26 |
| it | 32 | 57 | 160 / 157 | 120 | 82 | 60 | 160 / 155 | 120 | 291 | 21 | 29 |
| zh | 45 | 57 (56) | 160 / 160 | 120 | 82 | 60 | 160 / 156 | 120 | 288 | 28 | 32 |
| ja | 62 | 57 | 160 / 159 | 120 | 82 | 60 | 160 / 156 | 120 | 293 | 22 | 27 |
| ko | 43 | 57 | 160 / 158 | 120 | 82 | 60 | 160 / 156 | 120 | 293 | 21 | 27 |
| ru | 35 | 57 | 160 / 159 | 120 | 82 | 60 | 160 / 159 | 120 | 298 | 20 | 22 |

- Estructura idéntica en los 10 idiomas: 8 unidades en N0, y 20 unidades × 8 palabras × 6 frases en N1 y N2. Las traducciones de N1 comparten entre 97 y 134 de 160 glosas con el inglés, lo que indica un **currículo paralelo traducido, no diseñado para cada idioma**. El español como meta usa glosas monolingües («saludo general»), por eso comparte 0.
- Las repeticiones dentro de N1–N2 son pequeñas (17–32 por idioma; p. ej. it: `lei, piacere, prego, andare…`; zh: `常常, 没, 到, 休息`). Es una reutilización accidental, no programada.
- Los bancos escritos a mano (`idiomas.dart` `_n1`: es 1 unidad, los otros 8 idiomas 6 unidades; `_apoyo`: 6 palabras + 3 frases por idioma; inglés `_unidadesNivel1`: 20 unidades) **solo actúan como respaldo** si falla la carga del JSON. Siguen siendo código muerto con riesgo: si falla `precargar`, las unidades 7–20 muestran el mismo banco de 6 palabras rotado (`bancoNivel1`).

### Niveles 3–10 (todos los idiomas)

| Nivel | Fuente | Palabras distintas | Frases distintas | Unidades que las repiten | Idioma real mostrado |
|---|---|---|---|---|---|
| 3–10 | `_bancoGenerico` (`curriculum.dart:349-414`) | 6 por nivel (48 en total) | 3 por nivel (24) | 20 por nivel (160) | **inglés para los 10 idiomas** |

Resultado: 960 posiciones de vocabulario y 480 de frases mostradas con solo 48 y 24 elementos distintos. Además hay saltos de registro sin progresión: el nivel 8 pasa a «Leverage, Stakeholder…» y el 9 a «Albeit, Rhetoric…».

### Inglés: otras fuentes

| Fuente | Entradas | Únicas | Notas |
|---|---|---|---|
| `situaciones.json` (vocabulario base) | 150 | — | 3 por situación, sin ejemplo ni nivel |
| `situational_vocabulary.json` | 400 | 394 | 8 por situación: 204 nombres, 99 verbos, 97 expresiones; `nivelInicial` 1: 98, 2: 219, 3: 78, 4: 5 |
| Situaciones en total | 550 | **531** | 19 formas repetidas entre situaciones: **10 con otro sentido** (checkout, card, order n/v, rent n/v, report, ticket, board, tap, pass, watch) y 9 con el mismo sentido (aisle, seat, fare, deposit, experience, deadline, example, visit, towel) |
| Patrones situacionales | 50 | — | 1 por situación, 2 ejemplos cada uno (100); solo 1 tiene `note` |
| `reading_units.json` | 20 unidades × 4 | 80 | 2 por nivel 1–10; no enlazadas a situaciones |
| `listening_units.json` | 20 × 4 | 80 | Ídem |
| `biblioteca.json` | 116 preguntas | — | Solo 10 de vocabulario |
| **Unión en inglés** (N0 + N1 + N2 + situaciones + lectura/escucha) | — | **≈975** | Solape situaciones∩N1–2 = 37 formas; situaciones∩lectura/escucha = 24; N1–2∩lectura/escucha = 12 |

Conclusión del inventario: el vocabulario de las situaciones **casi no se conecta** con el del curso (37 de 531 formas coinciden). Tampoco hay un identificador léxico común: cada fuente usa su propio esquema (`palabra`, `en`, `word`, `simbolo`).

## Auditoría de las 50 situaciones (tabla)

La pantalla (`situation_screen.dart`) ofrece hoy lo mismo en las 50:
- Vocabulario: lista de 11 entradas con TTS.
- Patrón con ejemplos y botón «Escuchar frase».
- 3 objetivos con frase modelo.
- Chat de IA por objetivo, en modo práctica.
- Comprobación de vocabulario: opción múltiple entre la palabra y su traducción.
- «Probar mi comunicación con IA», en modo prueba y sin puntuación.

Leyenda:
- ✓ = presente.
- ◐ = parcial.
- ✗ = ausente.
- **T** = solo TTS de frases aisladas, sin tarea de comprensión.
- **T+** / **◐ᴸ** = existe una unidad temática de escucha o lectura, pero **no está enlazada** a la situación.
- Constantes para las 50 filas: Ejemplos ✓ (8 + 2 + 3 frases objetivo), Patrón ◐ (1), Diálogo ✗, Producción ◐ (chat abierto sin tarea ni rúbrica), Evaluación ◐ (reconocimiento con opción múltiple + prueba de IA sin criterio de logro).
- «Nivel implícito» = nivel que exige la gramática de las frases objetivo actuales. «Mín. propuesto» = nivel en el que puede empezar una variante A1/A2.

| # | Situación | Voc | Verbos | Expr | Listen | Lect. | Nivel implícito | Mín. propuesto | Gramática por encima del nivel del vocabulario (1–4) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Restaurante | ✓11 | ◐1 | ✓2 | T | ✗ | 3 | 1 | «This is not what I ordered» (relativa libre + pasado) |
| 2 | Cafetería | ✓11 | ◐1 | ✓2 | T+ | ◐ᴸ | 1–2 | 1 | — |
| 3 | Supermercado | ✓11 | ✓2 | ✓2 | T | ◐ᴸ | 4 | 1 | comparativo (smaller), cantidades |
| 4 | Tienda | ✓11 | ✓2 | ✓3 | T | ✗ | 4 | 2 | comparativo (cheaper) |
| 5 | Ropa | ✓11 | ✓2 | ✓2 | T | ✗ | 4 | 2 | too + adj, comparativo |
| 6 | Zapatos | ✓11 | ✓2 | ✓2 | T | ✗ | 4 | 2 | comparativo (better) |
| 7 | Aeropuerto | ✓11 | ✓2 | ✓2 | T | ✗ | **5** | 2 | «has been delayed» (perfect + pasiva) |
| 8 | Avión | ✓11 | ✓2 | ✓2 | T | ✗ | 2 | 1 | — |
| 9 | Inmigración | ✓11 | ✓2 | ✓2 | T | ✗ | **5** | 2 | pregunta indirecta «what I need to declare»* |
| 10 | Hotel | ✓11 | ✓2 | ✓2 | T+ | ✗ | 3 | 2 | continuo (is not working) |
| 11 | Taxi/Uber | ✓11 | ✓2 | ✓2 | T | ✗ | 3 | 2 | will |
| 12 | Alquiler de coche | ✓11 | ✓2 | ✓2 | T | ✗ | 3 | 3 | — |
| 13 | Gasolinera | ✓11 | ◐1 | ✓3 | T | ✗ | 2 | 2 | léxico: *forecourt* (nivel 4, poco rentable) |
| 14 | Taller | ✓11 | ✓3 | ◐1 | T+ | ✗ | 3 | 3 | will |
| 15 | Médico | ✓11 | ✓2 | ✓2 | T | ✗ | **5** | 2 | «has hurt since», patrón «I have had … since» |
| 16 | Farmacia | ✓11 | ✓2 | ✓2 | T | ✗ | 4 | 3 | should |
| 17 | Dentista | ✓11 | ✓2 | ✓2 | T | ✗ | 3 | 3 | cláusula when |
| 18 | Banco | ✓11 | ✓2 | ◐1 | T | ✗ | **5** | 3 | «has been blocked» (perfect + pasiva) |
| 19 | Pagar | ✓11 | ✓2 | ✓2 | T | ✗ | **5** | 1 | «I was charged twice», «It was declined» (pasiva) |
| 20 | Entrevista | ✓11 | ✓2 | ✓2 | T | ✗ | **5** | 5 | «What would my responsibilities be?» |
| 21 | Trabajo | ✓11 | ✓2 | ✓2 | T+ | ✗ | **5** | 3 | «I have finished» (perfect) |
| 22 | Jefe | ✓11 | ✓2 | ✓2 | T | ✗ | 4 | 4 | superlativo |
| 23 | Reunión | ✓11 | ✓2 | ✓2 | T | ✗ | 4 | 5 | suggest + -ing |
| 24 | Teléfono | ✓11 | ✓2 | ✓2 | T | ✗ | 4 | 3 | ask sb to + phrasal |
| 25 | Servicio al cliente | ✓11 | ✓2 | ✓2 | T+ | ✗ | **5** | 3 | «has not arrived» |
| 26 | Alquilar vivienda | ✓11 | ✓2 | ✓2 | T | ✗ | 3 | 3 | — |
| 27 | Avería en casa | ✓11 | ✓2 | ✓2 | T | ✗ | **5** | 3 | «We have had no hot water since…» |
| 28 | Técnico | ✓11 | ✓2 | ✓2 | T+ | ◐ᴸ | 3 | 3 | — |
| 29 | Policía | ✓11 | ✓2 | ✓2 | T | ✗ | **5** | 3 | «My wallet was stolen» (pasiva) |
| 30 | Tráfico | ✓11 | ✓2 | ◐1 | T | ✗ | **5** | 3 | «There has been an accident» |
| 31 | Autobús | ✓11 | ✓2 | ✓2 | T+ | ◐ᴸ | 4 | 1 | «tell me when to get off» |
| 32 | Tren | ✓11 | ✓2 | ✓2 | T | ✗ | 3 | 2 | will + *make a connection* |
| 33 | Direcciones | ✓11 | ✓2 | ✓2 | T | ✗ | 2 | 1 | — |
| 34 | Escuela | ✓11 | ✓2 | ✓2 | T+ | ◐ᴸ | 1–2 | 1 | — |
| 35 | Profesor | ✓11 | ✓2 | ✓2 | T | ✗ | **5** | 3 | «focus on improving» (prep. + -ing, preposición al final) |
| 36 | Deportes | ✓11 | ✓2 | ✓2 | T | ✗ | 3 | 2 | pasado |
| 37 | Gimnasio | ✓11 | ✓2 | ✓2 | T | ✗ | 3 | 2 | show me how + frase |
| 38 | Playa | ✓11 | ✓2 | ✓2 | T | ✗ | 2 | 2 | — |
| 39 | Vacaciones | ✓11 | ✓2 | ✓2 | T | ◐ᴸ | **6** | 3 | «Would you rather», «If it rains, we could» |
| 40 | Cine | ✓11 | ✓2 | ✓2 | T | ✗ | 2 | 1 | — |
| 41 | Música | ✓11 | ✓2 | ◐1 | T | ✗ | 4 | 2 | might |
| 42 | Películas/series | ✓11 | ✓2 | ✓2 | T | ✗ | 4 | 3 | valoración en pasado + contraste |
| 43 | Familia | ✓11 | ✓3 | ◐1 | T | ✗ | 2 | 1 | — |
| 44 | Conocer a alguien | ✓11 | ✓2 | ✓2 | T | ✗ | 2 | 1 | like + -ing (como chunk) |
| 45 | Relaciones sociales | ✓11 | ✓2 | ✓2 | T | ✗ | **5** | 3 | «How has your week been?», would rather |
| 46 | Fiesta | ✓11 | ✓2 | ✓2 | T | ✗ | 3 | 2 | pasado |
| 47 | Cumpleaños | ✓11 | ✓2 | ✓2 | T | ✗ | 2 | 1 | — |
| 48 | Cocina | ✓11 | ✓2 | ✓2 | T | ✗ | 2 | 2 | — |
| 49 | Tareas de la casa | ✓11 | ✓2 | ✓2 | T | ◐ᴸ | 2 | 2 | «Let us make…» (poco natural: usar *Let's*) |
| 50 | Conversación libre | ✓11 | ✓2 | ✓2 | T | ✗ | **5** | 3 | «One reason is that…» |

Hallazgos adicionales:
- **Ninguna situación tiene campo `nivel`.** La app sugiere situaciones sin considerar el nivel (`suggestedSituation` solo mira evidencia reciente y objetivos personales).
- Hay **15 situaciones con nivel implícito ≥ 5** (7, 9, 15, 18, 19, 20, 21, 25, 27, 29, 30, 35, 39, 45, 50; la 20 y la 50 son de B1 por diseño). Varias son situaciones de supervivencia que un A1/A2 necesita (19 Pagar, 15 Médico, 29 Policía). Hace falta una **variante A1/A2 sin perfect ni pasiva**, p. ej. «My flight is late», «Someone took my wallet», «I have a sore throat. It started yesterday.»
- También hay ejemplos de vocabulario con gramática de B1 marcada con nivel 2–3: «I have not used this printer before» (21), «We have not booked our accommodation yet» (39), «I have not seen the ending yet» (42), «Has the payment gone through?» (19).
- **Variedad británica** (petrol, tyre, lift, trousers, trainers, rubbish, licence, bill, flat) con **TTS en-US** (`localeVoz['en'] = 'en-US'`, `idiomas.dart:20`). Esto es incoherente y falta un alias US/UK.
- Los contenidos de escucha y lectura temáticos (café, clase, autobús, hotel, turno, reparación, entrega, cocina compartida) existen, pero **no se referencian** desde la situación.
- La comprobación de vocabulario solo mide reconocimiento de L2 a L1; no hay recuperación ni producción controlada.

## Plantilla de situación como mini-ruta

Cada situación pasa de «lista + chat» a una **ruta de 12 pasos**. Cada paso declara `objetivoId`, `itemsLexicos[]`, `gramatica[]`, `habilidad` y `evidencia` (qué se guarda). Una sesión dura 10–15 min. Los pasos 1–7 forman la **ruta base de la variante**, y los pasos 8–12 se desbloquean con evidencia.

| # | Paso | Qué hace el alumno | Contenido requerido | Evidencia guardada |
|---|---|---|---|---|
| 1 | Objetivo | Lee «Puedo…» (2–4 objetivos observables) y elige subobjetivo | `objetivos[]` con descriptor «Puedo…» por variante | inicio |
| 2 | Vocabulario visual | Imagen + audio + palabra; 5–8 ítems nuevos como máximo, el resto ya conocidos | `itemsLexicos[]` con ID léxico, imagen, audio y ejemplo en contexto | exposición (estado *visto*) |
| 3 | Verbos y expresiones | Chunks funcionales (pedir, preguntar, aclarar) con registro | `chunks[]` con `funcion` y `registro` | exposición |
| 4 | Construcción de frases | Patrón con huecos tipados → armar frases (arrastrar o escribir) | `patrones[]` con `slots` tipados (contable, plato, precio…) y reglas de concordancia | reconocimiento/recuperación |
| 5 | Diálogo modelo | Diálogo de 6–10 turnos con audio por turno; alternar roles | `dialogo[]` (hablante, texto, audio, traducción oculta) | exposición |
| 6 | Listening | Audio nuevo (no el diálogo) de 30–90 s, con variación de voz y velocidad | `listening` con guion, audio y velocidad por nivel | — |
| 7 | Comprensión | 3–5 preguntas: detalle, número o precio, inferencia (B1+) | `preguntas[]` | respuestas (listening real) |
| 8 | Práctica guiada | Huecos sin banco, ordenar, responder al camarero con opciones → sin opciones | `ejercicios[]` (≥ 3 tipos) | recuperación con/sin ayuda |
| 9 | Variaciones | El mismo objetivo en otro contexto (café → comida rápida; UK → US) | `variaciones[]` | transferencia |
| 10 | Conversación con IA | Tarjeta de rol con misión, restricciones y criterio de éxito | `rolIA` con misión, perfil de nivel e ítems objetivo | turnos + ítems usados (etiquetados por el tutor) |
| 11 | Evaluación | Tarea breve con rúbrica de 4 criterios, más 5 ítems de recuerdo diferido | `evaluacion` con rúbrica y umbral | resultado por objetivo (nunca solo con IA) |
| 12 | Repaso | Los ítems entran al repaso espaciado; se programa una reaparición en otras situaciones | `reutiliza[]`, `alimenta[]` | estado léxico |

**Variantes por nivel** (misma situación, objetivos que crecen):

| Variante | Nivel interno | Qué cambia | Longitud de turno | Gramática típica |
|---|---|---|---|---|
| A1 | 1–2 | Fórmulas fijas (X, please; Can I have…?), números y precios, sí/no | 2–6 palabras | be, artículos/plurales, preguntas con *how much*, can como chunk |
| A2 | 3–4 | Modificar, preferir, cantidades, pasado simple para explicar | 5–10 | peticiones corteses*, contables/incontables*, cantidades, comparativos, pasado |
| B1 | 5–6 | Resolver un problema, explicar causa, condiciones | 10–15 | perfect, pasiva básica, 1.er condicional, preguntas indirectas* |
| B2 | 7–8 | Negociar, reclamar con mitigación, matizar | párrafo | pasiva, estilo indirecto, hedging, concesión |
| C1 (opc.) | 9–10 | Registro escrito (reseña o reclamación formal), ironía, cortesía estratégica | libre | editing-register, inversión |

Regla editorial: **ninguna frase modelo de una variante puede usar gramática de un nivel superior**, salvo como chunk memorizado marcado `chunk: true`. Esta regla debe validarse con un script de CI que compare `gramatica[]` con el nivel.

## Ejemplo completo: restaurante

Situación 1, inglés, variedad por defecto **US** (coherente con el TTS en-US) con alias UK. Contenido original.

**Objetivo global.** Puedo comer en un restaurante: conseguir mesa, pedir comida y bebida, adaptar el pedido a mis restricciones, resolver un error y pagar.

### Objetivos por variante

| Variante | «Puedo…» |
|---|---|
| A1 | pedir mesa para N · pedir un plato y una bebida · preguntar un precio · pedir la cuenta |
| A2 | pedir con cortesía (I'd like / Could we get) · quitar o cambiar un ingrediente · decir una alergia · pedir por separado |
| B1 | cambiar un pedido ya hecho · explicar que el plato no es lo pedido y pedir solución · revisar un error en la cuenta |
| B2 | reclamar con mitigación y negociar una compensación · preguntar por la preparación (restricciones complejas) · opinar sobre el servicio |

### Vocabulario visual (ítems con nivel de introducción)

| Grupo | A1 (1–2) | A2 (3–4) | B1+ (5+) |
|---|---|---|---|
| Comida | soup, salad, chicken, fish, rice, bread, cheese, egg, burger, pasta, fries (UK chips) | steak, side salad, dressing, sauce | medium-rare, grilled, deep-fried |
| Bebida | water, juice, coffee, tea, soda (UK soft drink) | sparkling water, still water, a glass of…, a bottle of… | refill, house wine |
| Menú | menu, dessert | appetizer (UK starter), main course, side dish, today's special | tasting menu, set menu |
| Mesa | table, chair, plate, glass, fork, knife, spoon | napkin, highchair, booth | — |
| Personas/lugar | server/waiter, kitchen | host, reservation | manager |
| Cantidades | one, two… twenty, small, large | some, more, another, half, a portion of | a side of, split between |
| Precios | price, dollar, cent, How much? | total, check (UK bill), tip, receipt | service charge, overcharged |
| Restricciones | no, with, without | allergic to, nuts, gluten, dairy, vegetarian, vegan, spicy, instead of | cross-contamination, gluten-free option |
| Problemas | cold, hot, wrong | missing, not what I ordered | undercooked, mix-up, the wait |

### Verbos y expresiones clave

`have` (Can I have…?), `want` (marcado como menos cortés), `would like / I'd like`, `get` (Could we get…?), `order`, `bring`, `share`, `pay`, `split`, `recommend`, `change`, `swap`, `cancel`, `check`.
Fórmulas: *Table for two, please* · *Are you ready to order?* · *For here or to go?* · *Anything else?* · *Excuse me!* · *Enjoy your meal.*

### Construcción de frases (patrones con huecos tipados)

| Variante | Patrón | Slots y restricciones | Ejemplos |
|---|---|---|---|
| A1 | `{item}, please.` | item: plato o bebida con artículo | A coffee, please. / The chicken, please. |
| A1 | `Can I have {item}, please?` | item contable → a/an; incontable → some | Can I have a salad, please? |
| A1 | `How much is {item}?` → `It's {price}.` | price: «twelve fifty» = $12.50 | How much is the soup? It's six dollars. |
| A2 | `I'd like {item} with/without {ingredient}.` | ingredient incontable sin artículo | I'd like the burger without onions. |
| A2 | `Could we get {quantity} {item}?` | quantity: two / some / another | Could we get two more glasses of water? |
| A2 | `I'm allergic to {allergen}. Is there {allergen} in {dish}?` | allergen incontable o plural | I'm allergic to nuts. Are there nuts in the salad? |
| A2 | `Can I have {x} instead of {y}?` | x, y del mismo tipo | Can I have rice instead of fries? |
| B1 | `Sorry, I ordered {x}, but this is {y}.` | x, y platos | Sorry, I ordered the fish, but this is chicken. |
| B1 | `I think there's a mistake on the check: we didn't have {x}.` | pasado negativo | …we didn't have any desserts. |
| B1 | `Would it be possible to {verb}?` | verbo base | Would it be possible to change my order? |
| B2 | `I'm afraid {problem}. Would you mind {verb-ing}…?` | mitigación + gerundio | I'm afraid my steak is quite undercooked. Would you mind sending it back? |

### Diálogos modelo

**A1 (8 turnos)**
> Server: Hi! Table for two? — Guest: Yes, please.
> Server: Here's the menu. Something to drink? — Guest: Water, please.
> Server: Are you ready to order? — Guest: The chicken and rice, please.
> Guest: How much is the soup? — Server: It's five dollars.
> Guest: The check, please. — Server: Sure. That's eighteen dollars.

(«¿Mesa para dos?», «Agua, por favor», «El pollo con arroz, por favor», «¿Cuánto cuesta la sopa?», «La cuenta, por favor».)

**A2 (10 turnos)**
> Server: Good evening. Do you have a reservation? — Guest: No, we don't. Could we get a table for three?
> Server: Of course. Here you are. — Guest: Thanks. I'd like the pasta, but without cheese, please.
> Server: No problem. And for you? — Friend: I'm allergic to nuts. Is there anything with nuts in the curry?
> Server: Yes, there are some cashews. I can ask the kitchen to leave them out. — Friend: Great. Can I have rice instead of bread?
> Guest: Could we pay separately, please? — Server: Sure, I'll bring two checks.

**B1 (resolución de un error)**
> Guest: Excuse me. Sorry, I ordered the vegetable curry, but this one has chicken in it.
> Server: Oh, I'm so sorry. I'll take it back and bring the right one.
> Guest: Thank you. Also, I think there's a mistake on the check. We didn't have any desserts.
> Server: You're right, that was another table's order. Here's the correct check.

**B2 (reclamación y compensación, esquema)**: el comensal explica una espera larga y un plato mal cocinado con mitigación (*I'm afraid…, I'd appreciate it if…*). El servidor ofrece una alternativa y el comensal negocia (*Would it be possible to take it off the bill?*). Cierre cortés.

### Listening (A2, guion original, ~70 palabras)

> «Hi there, welcome to Rosa's. Tonight's specials are a tomato soup for six dollars and a grilled fish with rice for fourteen fifty. The fish comes with a small salad. We also have a vegan burger, but I'm afraid we don't have any fries left tonight, so it comes with potatoes. Can I get you something to drink while you decide?»

**Comprensión:** (1) ¿Cuánto cuesta el pescado? → $14.50 (número/precio). (2) ¿Qué acompaña al pescado? → arroz y una ensalada pequeña (detalle). (3) Pides la hamburguesa vegana con papas fritas: ¿qué pasa? → no quedan; viene con patatas (inferencia, A2+).

### Práctica guiada (progresión de apoyo)

1. Relacionar imagen con palabra (reconocimiento, A1).
2. Escuchar un pedido y marcar en un menú ilustrado qué se pidió (listening y números).
3. Completar sin banco: «___ I have the soup, please?» / «I'm allergic ___ nuts.»
4. Ordenar: *instead / can / of / rice / I / have / fries* → «Can I have rice instead of fries?».
5. Responder al camarero (audio) primero con 3 opciones y después sin opciones.
6. Transformar, subiendo de registro: *I want water* → *Could I have some water, please?*
7. B1: detectar el error en una cuenta (lectura de un ticket) y formular la queja.

### Variaciones

Comida rápida en mostrador («For here or to go?»). Grupo que divide la cuenta. Cliente con dieta vegana. Llamada para reservar (conecta con la situación 24). **UK vs US**: bill/check, starter/appetizer, chips/fries; propina: service charge en UK frente a 15–20 % en US. Café (situación 2) como versión A1 reducida.

### Conversación con IA (tarjeta de rol por variante)

| Variante | Misión del alumno | Comportamiento del tutor | Criterio de éxito |
|---|---|---|---|
| A1 | Mesa + 1 plato + 1 bebida + preguntar un precio + pedir la cuenta | Frases de 3–6 palabras, habla lenta, ofrece 2 opciones si hay bloqueo | Los 5 subobjetivos logrados, con ≥ 3 turnos sin sugerencia |
| A2 | Pedir para 2 con 1 modificación y 1 alergia; pagar por separado | Introduce un imprevisto (ingrediente agotado) | Modificación + alergia expresadas con fórmula cortés |
| B1 | Llega un plato equivocado y hay un error en la cuenta | No resuelve hasta que el alumno explica el problema | Problema, causa y solución pedida, más confirmación |
| B2 | Espera larga + plato mal hecho; negociar | Resiste una vez y acepta una propuesta razonable | Mitigación + propuesta + cierre cortés |

El tutor devuelve `itemsUsados[]` (IDs léxicos usados correctamente o con error). Hoy devuelve `corrections` sin IDs léxicos, por lo que hay que ampliar el contrato de `/chat`.

### Evaluación

Hay dos componentes:

- **Recuerdo diferido**: 5 ítems de la situación, sin opciones, al menos 24 h después.
- **Tarea de rol** (IA o docente) evaluada con rúbrica de 0–3 por criterio:
  - logro de la tarea;
  - precisión de las formas objetivo;
  - adecuación y cortesía;
  - comprensión de la réplica.

La variante se da por superada con ≥ 8/12 y ningún criterio en 0. La IA solo registra la evidencia; el certificado de la variante requiere también el ejercicio de listening (paso 7) y el recuerdo diferido. Esto es coherente con `situaciones.ts`: «Un turno sin correcciones no demuestra dominio».

### Repaso

Todos los ítems A1 y A2 entran al repaso espaciado. Se reutilizan de forma programada en:
- situación 2 (café): bebidas, tamaños;
- situación 19 (pagar): precios, check/receipt;
- situación 48 (cocina): ingredientes, cantidades;
- situación 47 (cumpleaños): cake, dessert;
- situación 3 (supermercado): cantidades, alérgenos.

### Gramática que requiere cada variante (IDs provisionales)

| Variante | Requiere (antes de la variante) | Se practica aquí |
|---|---|---|
| A1 | en-g-be, en-g-articles-plurals, en-g-questions (how much), en-g-numbers-prices* | en-g-polite-please-chunks* (X, please / Can I have… como chunk) |
| A2 | A1 + en-g-ability, en-g-quantity, en-g-past | en-g-polite-requests* (I'd like, Could we get), en-g-countable-uncountable* (some/any/a glass of), en-g-prepositions-with-without-instead* |
| B1 | A2 + en-g-comparisons | en-g-perfect (We've been waiting), en-g-passive-basic (Is service included? It's cooked in butter), en-g-would-possible* (Would it be possible…), en-g-indirect-questions* (Could you tell me what's in…?) |
| B2 | B1 + en-g-first-conditional | en-g-reported (We were told…), en-g-hedging, en-g-mitigation* (I'm afraid…, I'd appreciate it if…) |
| C1 | — | en-g-editing-register (reseña o reclamación escrita) |

**Hueco crítico**: el temario propuesto no incluye **peticiones corteses (would like / could)** ni **contables/incontables**. Sin embargo, 30 de las 50 situaciones usan *Could I/you/we…*, *Can I have* o *I'd like* en objetivos o patrones (36 si se cuentan los ejemplos). El agente A debe crear `en-g-polite-requests` en el nivel 1–2 (como chunk) y en el 3 (como estructura).

## Mapa de las 50 situaciones

Prefijo `en-g-` omitido; `*` = tema nuevo, no presente en el temario. Variantes: el nivel indica la variante mínima; entre corchetes, el foco de cada variante.

| # | Situación | Mín | Objetivos comunicativos | Vocabulario núcleo | Funciones / expresiones | Gramática (prov.) | Variantes |
|---|---|---|---|---|---|---|---|
| 1 | Restaurante | 1 | mesa; pedir; modificar; pagar/resolver | comida, bebida, menú, cubiertos, precios, alérgenos | X, please; Can/Could I have; I'm allergic to; The check, please | polite-requests*, countable-uncountable*, questions, past | A1[pedir] A2[modificar/alergias] B1[error] B2[reclamar] |
| 2 | Cafetería | 1 | pedir bebida; personalizar; aquí/llevar | bebidas, tamaños, leche/azúcar, envases | A small latte, please; with/without; for here/to go | articles-plurals, polite-requests* | A1[pedir] A2[personalizar] B1[corregir pedido] B2[charla con barista] |
| 3 | Supermercado | 1 | localizar; cantidades/precios; alternativa | alimentos, envases, secciones, pesos | Where is/are…?; How much is…?; Do you have…? | there-be, quantity, comparisons | A1[localizar] A2[cantidades] B1[agotado/sustituto] B2[reclamar precio] |
| 4 | Tienda | 2 | buscar; comparar; devolver/cambiar | objetos, colores, precios, recibo | Do you sell…?; Which one is cheaper?; Can I return…? | comparisons, past, polite-requests* | A1[precio] A2[comparar] B1[devolución] B2[negociar reembolso] |
| 5 | Ropa | 2 | talla; probar; ajuste; cambiar | prendas, tallas, colores, materiales | Do you have this in M?; Can I try it on?; too big | comparisons, too-enough* | A1[talla/color] A2[ajuste] B1[cambio] B2[asesorar estilo] |
| 6 | Zapatos | 2 | número; ajuste; comodidad | calzado, partes, tallas | size eight; too tight; Which pair is better? | comparisons, too-enough* | A1[número] A2[ajuste] B1[comparar uso] B2[defecto/garantía] |
| 7 | Aeropuerto | 2 | facturar; puerta/horario; retraso | equipaje, documentos, horas, lugares | Where do I check in?; Which gate?; My flight is late | present (horarios), time-place, perfect (B1) | A1[lugares/horas] A2[facturar] B1[retraso/opciones] B2[reubicación] |
| 8 | Avión | 1 | asiento; pedir algo; malestar | asiento, objetos de cabina, bebidas | Excuse me, this is my seat; Could I have…? | be, polite-requests* | A1[pedir] A2[cambiar asiento] B1[problema] B2[conflicto con pasajero] |
| 9 | Inmigración | 2 | propósito; duración/alojamiento; aclarar | documentos, propósito, tiempo | I'm here on vacation; for two weeks; Could you repeat that? | be, continuous (arreglo futuro), indirect-questions* (B1) | A1[respuestas cortas] A2[detalles] B1[declarar/aclarar] B2[incidencias] |
| 10 | Hotel | 2 | registrarse; servicios; problema | habitación, servicios, horarios | I have a reservation; Is breakfast included?; …isn't working | there-be, continuous, present | A1[check-in] A2[servicios] B1[queja] B2[cambio/compensación] |
| 11 | Taxi/Uber | 2 | destino; tiempo/tarifa; cambiar ruta | lugares, direcciones, dinero | To the station, please; How long will it take?; Stop here | imperatives*, will-offers*, polite-requests* | A1[destino] A2[tarifa/tiempo] B1[cambio de ruta] B2[disputa de tarifa] |
| 12 | Alquilar coche | 3 | solicitar; condiciones; daños previos | vehículo, seguro, documentos, combustible | I'd like to rent…; Does the price include…?; There's a scratch | polite-requests*, there-be, past | A2[alquilar] B1[condiciones/daños] B2[disputa] |
| 13 | Gasolinera | 2 | surtidor; cantidad; pagar | combustible, surtidor, pago | Which pump?; Fill it up, please; Pump three | imperatives*, numbers-prices* | A1[pagar] A2[cantidad] B1[fallo del surtidor] |
| 14 | Taller | 3 | avería; presupuesto; plazo | partes del coche, ruidos, costes | It makes a strange noise; How much will it cost? | present, will-offers*, quantity | A2[describir] B1[presupuesto] B2[reclamar reparación] |
| 15 | Médico | 2 | cita; síntomas; instrucciones | cuerpo, síntomas, tiempo | I have a headache; It hurts here; It started yesterday | present, past; perfect (B1: since/for) | A1[dolor] A2[cita/síntomas] B1[historia] B2[dudas sobre tratamiento] |
| 16 | Farmacia | 3 | receta; cómo tomar; efectos | medicamentos, formas, frecuencia | How often should I take it?; with food | advice, frequency | A2[receta] B1[instrucciones] B2[alternativas] |
| 17 | Dentista | 3 | revisión; molestia; procedimiento | boca, dientes, sensaciones | It hurts when I drink cold things; Please stop | present, time-clauses* | A2[molestia] B1[procedimiento] B2[opciones/coste] |
| 18 | Banco | 3 | abrir cuenta; comisiones; tarjeta | cuenta, tarjeta, operaciones, comisiones | I'd like to open an account; Is there a fee?; My card doesn't work | polite-requests*, there-be; passive-basic (B1) | A2[trámite] B1[bloqueo] B2[reclamar comisión] |
| 19 | Pagar | 1 | forma de pago; total; cobro erróneo | dinero, tarjeta, números, recibo | Can I pay by card?; Cash or card?; You charged me twice | numbers-prices*, ability; passive-basic (B1) | A1[pagar] A2[revisar total] B1[doble cobro] B2[reclamación] |
| 20 | Entrevista | 5 | experiencia; fortalezas; preguntar puesto | trabajo, habilidades, estudios | I have experience in…; I'm good at…; What would the role involve? | perfect, verb-patterns, polite-would* | B1[presentarse] B2[casos/competencias] C1[negociar condiciones] |
| 21 | Trabajo | 3 | aclarar tarea; avance; pedir ayuda | tareas, horarios, herramientas | What should I do first?; Could you help me with…? | advice, polite-requests*; perfect (B1) | A2[pedir ayuda] B1[informar avance] B2[delegar] |
| 22 | Jefe | 4 | prioridades; feedback; plazo | proyectos, plazos | Which task is the most urgent?; Could we move the deadline? | comparisons, future-plans, polite-requests* | A2[prioridad] B1[feedback] B2[negociar plazo] |
| 23 | Reunión | 5 | intervenir; proponer; acuerdos | reunión, decisiones | May I add something?; We could…; I suggest -ing | verb-patterns, modal-suggestions* | B1[proponer] B2[desacuerdo cortés] C1[moderar] |
| 24 | Teléfono | 3 | identificarse; pedir repetición; recado | teléfono, números, recados | This is Ana; Could you speak more slowly?; Can she call me back? | continuous, polite-requests*, verb-patterns | A2[recado] B1[aclarar] B2[llamada formal] |
| 25 | Servicio al cliente | 3 | explicar problema; solución; seguimiento | pedido, entrega, reembolso | My order didn't arrive; Could you send a new one? | past, polite-requests*; perfect (B1) | A2[explicar] B1[solución] B2[escalar reclamación] |
| 26 | Alquilar vivienda | 3 | disponibilidad; gastos; visita | casa, gastos, contrato | Is it still available?; Are bills included?; Can I see it on Saturday? | there-be, questions | A2[consultar] B1[condiciones] B2[negociar] |
| 27 | Avería en casa | 3 | notificar; impacto; seguimiento | averías, partes de la casa | There's a leak; There's no hot water; When can someone come? | there-be; perfect (B1: since) | A2[notificar] B1[impacto] B2[exigir plazo] |
| 28 | Técnico | 3 | falla; visita; presupuesto | electricidad, aparatos | This socket doesn't work; Are you free tomorrow? | present neg., polite-requests* | A2[describir] B1[presupuesto] B2[garantía] |
| 29 | Policía | 3 | pedir ayuda; describir hecho; intérprete | objetos personales, lugares, descripción física | Someone took my wallet; It happened near…; I need an interpreter | past, past-continuous; passive-basic (B1) | A2[denunciar] B1[describir] B2[declaración detallada] |
| 30 | Tráfico | 3 | indicaciones; incidente; alternativa | vía, señales | Turn left at the lights; There's an accident ahead | imperatives*, obligation; perfect (B1) | A2[indicaciones] B1[incidente] B2[explicar infracción] |
| 31 | Autobús | 1 | recorrido; billete; parada | transporte, lugares, billetes | Does this bus go to…?; One ticket to…, please | present, questions; indirect-questions* (A2+) | A1[billete] A2[parada] B1[cambio de ruta] |
| 32 | Tren | 2 | billete; andén; conexión | billetes, horarios | A round-trip ticket to…; Which platform? | present (horarios), will-offers* | A1[billete] A2[andén] B1[conexión perdida] |
| 33 | Direcciones | 1 | pedir; confirmar; describir ubicación | lugares de la ciudad, direcciones | How do I get to…?; Turn left; It's across from… | imperatives*, time-place | A1[pedir] A2[dar] B1[ruta compleja] |
| 34 | Escuela | 1 | aula; horario; materiales | objetos escolares, asignaturas | Where is room four?; What time does it start? | be, there-be, present | A1 única + A2[normas] |
| 35 | Profesor | 3 | aclaración; entregas; orientación | tareas, evaluación | Could you explain that again?; When is it due? | polite-requests*, advice | A2[aclarar] B1[orientación] B2[revisión de nota] |
| 36 | Deportes | 2 | preferencias; contar partido; opinar | deportes, equipo, resultados | Which team do you support?; They scored; I think… | present, past | A1[gustos] A2[partido] B1[análisis] |
| 37 | Gimnasio | 2 | inscripción; uso de equipo; rutina | máquinas, cuerpo, horarios | How much is a membership?; Could you show me how…? | polite-requests*, how-to* | A1[precio] A2[demostración] B1[plan] |
| 38 | Playa | 2 | organizar; servicios; seguridad | playa, clima, seguridad | Shall we…?; Where can we rent…?; Is it safe to swim? | shall-suggestions*, ability | A1[lugares] A2[planes] B1[normas] |
| 39 | Vacaciones | 3 | planes; comparar; adaptar | viaje, alojamiento, actividades | We're going to…; What do you recommend?; If it rains… (B1) | future-plans, comparisons; first-conditional (B1) | A2[planes] B1[alternativas] B2[negociar itinerario] |
| 40 | Cine | 1 | elegir; entradas; características | cine, horarios, entradas | What's on tonight?; Two tickets, please | present, numbers-prices* | A1[entradas] A2[elegir] B1[opinar] |
| 41 | Música | 2 | gustos; describir; recomendar | géneros, instrumentos | What kind of music do you like?; You might like… (A2+) | present, verb-patterns (like -ing) | A1[gustos] A2[describir] B1[recomendar] |
| 42 | Películas/series | 3 | presentar; resumir; opinar | géneros, personajes | It's a comedy about…; The plot was…, but… | present narrativo, past; concession (B2) | A2[resumir] B1[opinar] B2[crítica] |
| 43 | Familia | 1 | presentar; relaciones; tradiciones | familia, verbos de vida diaria | I live with…; We usually… | pronouns-possessives, present, frequency | A1[presentar] A2[relaciones] B1[tradiciones] |
| 44 | Conocer a alguien | 1 | presentarse; preguntar; intereses | datos personales, aficiones | Hi, I'm…; What do you like doing?; Me too | be, questions | A1 núcleo + A2[intereses] |
| 45 | Relaciones sociales | 3 | iniciar; invitar; rechazar con cortesía | social, emociones | Would you like to…?; I can't make it, but thanks | polite-would*, past; perfect (B1) | A2[invitar] B1[límites] B2[conflicto] |
| 46 | Fiesta | 2 | saludar anfitrión; charlar; despedirse | fiesta, comida, gente | Thanks for having me; How do you know…? | present, past | A1[saludos] A2[charla] B1[anécdota] |
| 47 | Cumpleaños | 1 | felicitar; organizar; agradecer | celebración, regalos | Happy birthday!; Shall we…?; Thank you for… | shall-suggestions* | A1[felicitar] A2[organizar] |
| 48 | Cocina | 2 | ingredientes; pasos; sustituciones | ingredientes, utensilios, verbos de cocina | First, chop…; How much flour do we need? | imperatives*, countable-uncountable*, sequencers* | A1[ingredientes] A2[receta] B1[adaptar] |
| 49 | Tareas de la casa | 2 | rutina; repartir; acordar | tareas, objetos de la casa | I do the laundry on…; Could you… while I…? | present, frequency, will-offers* | A1[rutina] A2[repartir] B1[negociar] |
| 50 | Conversación libre | 3 | tema; desarrollar idea; mantener intercambio | opinión, conectores | I think… because…; What do you think? | conjunctions*, first-conditional (B1) | A2[opinión simple] B1[argumentar] B2[debatir] |

Temas gramaticales nuevos que aparecen en el mapa y no están en el temario:
- polite-requests, polite-would
- countable-uncountable, too-enough
- imperatives, will-offers, shall-suggestions, modal-suggestions
- indirect-questions, how-to
- time-clauses, sequencers, conjunctions
- numbers-prices

## Adaptación multilingüe + situaciones iniciales por idioma

### Qué es universal y qué se adapta

| Tipo | Situaciones | Qué varía por idioma |
|---|---|---|
| **Universales** (objetivos idénticos; cambia solo la lengua) | 3, 5, 6, 8, 14, 17, 24, 28, 31–38, 40–44, 48–50 | Léxico y registro |
| **Adaptación cultural o de registro** | 1, 2 (propina, llamar al camarero, pagar en caja o en mesa, «para llevar»); 4, 19 (regateo, pago móvil en zh); 10 (propina, *check-in*); 11 (apps locales, taxi en ja con puerta automática); 20, 22, 23 (jerarquía; keigo/존댓말); 45–47 (regalos, tabúes numéricos, formas de invitar/rechazar) | Objetivos iguales, pero cambian notas culturales, fórmulas y registro por defecto |
| **Dependientes del sistema local** (texto neutral + aviso) | 7, 9 (normas fronterizas), 12, 13, 30 (lado de conducción, autoservicio), 15, 16 (sistema sanitario), 18 (banca), 26, 27 (contratos: depósitos, 礼金 en ja, 전세 en ko), 29 (policía, 交番 en ja) | Solo práctica lingüística; sin instrucciones legales ni médicas |

### Registro y cortesía por idioma (qué debe saber cada variante A1)

| Idioma | Tratamiento | Llamar al personal / pedir | Propina (orientativo, revisar) | Nota crítica para A1 |
|---|---|---|---|---|
| en | sin T/V; cortesía = *please / could* | *Excuse me* | US 15–20 %; UK suele venir como *service charge* | *I want* suena brusco |
| es | tú / usted (vos regional) | *Disculpe*, *¿Me trae…?* | ES opcional y baja; LatAm ~10 % | Variante por defecto a decidir (ES o LatAm) |
| fr | tu / vous; *Monsieur / Madame* | *S'il vous plaît !* (no *garçon*) | *service compris*; redondeo | *Bonjour* obligatorio al entrar |
| de | du / Sie; Herr/Frau + apellido | *Entschuldigung!* | redondear 5–10 % al pagar, diciéndolo | *Zahlen, bitte* / pago en la mesa |
| pt | você / o senhor, a senhora; tu (PT y sur de BR) | *Com licença*, *Por favor!* | BR 10 % en la cuenta (opcional) | pt-BR por defecto (TTS pt-BR); marcar pt-PT |
| it | tu / Lei | *Scusi!* | *coperto* en la cuenta; propina opcional | En el bar, a menudo se paga primero en caja |
| zh | 你 / 您 | 服务员 (fúwùyuán) / 你好 (nǐ hǎo) | no habitual | Pago móvil; clasificadores (一 杯) |
| ja | です/ます (A1); el personal usa 尊敬語 | すみません (sumimasen) | no se deja | No responder a いらっしゃいませ; no usar さん con el nombre propio |
| ko | 해요체 (A1); 합쇼체 al saludar | 저기요 (jeogiyo) / 여기요 (yeogiyo) | no habitual | 반말 prohibido con desconocidos; nativo frente a sino-coreano para contar |
| ru | ты / вы; nombre + patronímico | Извините! (izvinite) | ~10 % habitual en restaurante | Casos gramaticales ya en A1 (без сахара, с молоком) |

### Representación: situación neutral + contenido por idioma

1. **Ficha neutral** (una sola vez), p. ej. `assets/contenido/situaciones/sit-001.json`: `id`, `slug`, `categoria`, `edadMinima`, `sensibilidad`, `objetivos[{id, funcion, descriptor_es, variante}]`, `slots` semánticos (`dish`, `drink`, `price`, `allergen`) y `conceptosLexicos[]` (IDs de concepto neutrales: `food.soup`, `money.bill`, `func.request-politely`).
2. **Contenido por idioma**, p. ej. `assets/contenido/<idioma>/situaciones/sit-001.json`:
   - `variantes{A1..B2}` con `frases[]`, `dialogo[]`, `listening`, `ejercicios[]`;
   - `itemsLexicos[]`: ID léxico del idioma → concepto neutral, con romanización y audio;
   - `gramatica[]` (`<idioma>-g-*`), `registro` y `notasCulturales[]`;
   - `alias` de variedad (US/UK, BR/PT, ES/LatAm).
3. Un idioma **puede omitir** un objetivo (`noAplica` + razón) o **añadir** uno propio (p. ej. ja: «responder a la pregunta 店内でお召し上がりですか»). El validador de CI exige que cada objetivo neutral esté cubierto u omitido explícitamente.
4. El backend (`situaciones.ts`) carga la ficha según `idiomaMeta` (hoy solo carga la de inglés).

### Situaciones iniciales por idioma (fundamentos/A1)

Hay cuatro situaciones por idioma:
- **S1**: Saludos y cortesía.
- **S2**: Presentarse.
- **S3**: Números y precios.
- **S4**: Cafetería.

Formato: ítem = glosa en español. En zh, ja, ko y ru, la romanización va entre paréntesis según la convención del repo; zh y ja llevan espacios entre palabras (convención de niveles 1–3). Todo el contenido es original y requiere revisión nativa (ver Decisiones).

#### Inglés (en)
- **S1** · hello = hola · hi = hola (informal) · good morning = buenos días · good afternoon = buenas tardes · good evening = buenas noches (al llegar) · goodbye / bye = adiós · please = por favor · thank you / thanks = gracias · you're welcome = de nada · sorry = perdón · excuse me = disculpe · see you later = hasta luego
  - Frases: «Hi! How are you?» = ¡Hola! ¿Cómo estás? · «I'm fine, thanks. And you?» = Bien, gracias. ¿Y tú? · «Excuse me, sorry!» = ¡Disculpe, perdón! · «See you tomorrow!» = ¡Hasta mañana!
- **S2** · name = nombre · I'm = soy · from = de (origen) · country = país · city = ciudad · live = vivir · student = estudiante · teacher = profesor/a · friend = amigo/a · nice to meet you = mucho gusto · what = qué · where = dónde
  - Frases: «My name is Ana.» = Me llamo Ana. · «What's your name?» = ¿Cómo te llamas? · «I'm from Ecuador.» = Soy de Ecuador. · «Where are you from?» = ¿De dónde eres? · «Nice to meet you.» = Mucho gusto.
- **S3** · one = uno · two = dos · three = tres · ten = diez · twenty = veinte · fifty = cincuenta · a hundred = cien · price = precio · dollar = dólar · cheap = barato · expensive = caro · how much = cuánto
  - Frases: «How much is this?» = ¿Cuánto cuesta esto? · «It's five dollars.» = Son cinco dólares. · «That's expensive!» = ¡Qué caro! · «Two, please.» = Dos, por favor.
- **S4** · coffee = café · tea = té · water = agua · milk = leche · sugar = azúcar · juice = jugo · sandwich = sándwich · cake = pastel · cup = taza · small = pequeño · large = grande · menu = menú
  - Frases: «A small coffee, please.» = Un café pequeño, por favor. · «Can I have a tea with milk?» = ¿Me da un té con leche? · «No sugar, thanks.» = Sin azúcar, gracias. · «How much is it?» = ¿Cuánto es?

#### Español (es) — el contenido meta ya es español: se da glosa o registro, como hace hoy `es/nivel-1.json`
- **S1** · hola · buenos días · buenas tardes · buenas noches · adiós · hasta luego · por favor · gracias · de nada · perdón · disculpe (formal) / disculpa (informal) · ¿qué tal? (informal)
  - Frases: «Hola, ¿qué tal?» (informal) · «Buenos días, ¿cómo está usted?» (formal) · «Muy bien, gracias. ¿Y usted?» (formal) · «¡Hasta mañana!»
- **S2** · me llamo · soy · de (origen) · el país · la ciudad · vivir · estudiante · profesor / profesora · amigo / amiga · mucho gusto · encantado / encantada (concordancia con quien habla) · ¿cómo? · ¿dónde?
  - Frases: «Me llamo Ana.» · «¿Cómo te llamas?» (tú) / «¿Cómo se llama usted?» (usted) · «Soy de Ecuador.» · «Vivo en Quito.» · «Encantada.» (dicho por una mujer)
- **S3** · uno · dos · tres · diez · veinte · cincuenta · cien · el precio · el dólar / el euro · barato · caro · ¿cuánto?
  - Frases: «¿Cuánto cuesta?» · «Cuesta diez dólares.» · «Es muy caro.» · «Dos, por favor.»
- **S4** · un café · un té · agua · leche · azúcar · jugo (América) / zumo (España) · pan · pastel / torta (regional) · la taza · la carta · la cuenta · con / sin
  - Frases: «Un café con leche, por favor.» · «Para mí, un té sin azúcar.» · «¿Me trae la cuenta, por favor?» · «¿Cuánto es?»

#### Francés (fr)
- **S1** · bonjour = hola / buenos días · bonsoir = buenas tardes/noches · salut = hola (informal) · au revoir = adiós · à bientôt = hasta pronto · s'il vous plaît = por favor (formal) · s'il te plaît = por favor (informal) · merci = gracias · de rien = de nada · pardon = perdón · excusez-moi = disculpe · oui / non = sí / no
  - Frases: «Bonjour, madame !» = Buenos días, señora. · «Comment allez-vous ?» = ¿Cómo está usted? · «Très bien, merci. Et vous ?» = Muy bien, gracias. ¿Y usted? · «Bonne journée !» = ¡Que tenga buen día!
- **S2** · je m'appelle = me llamo · je suis = soy · j'habite à = vivo en · le pays = el país · la ville = la ciudad · étudiant / étudiante = estudiante · le professeur = el profesor · l'ami / l'amie = el amigo / la amiga · enchanté / enchantée = encantado/a · comment = cómo · où = dónde · équatorien / équatorienne = ecuatoriano/a
  - Frases: «Je m'appelle Ana.» = Me llamo Ana. · «Comment vous appelez-vous ?» = ¿Cómo se llama usted? · «Je suis équatorienne.» = Soy ecuatoriana. · «J'habite à Quito.» = Vivo en Quito. · «Enchantée !» = ¡Encantada!
- **S3** · un = uno · deux = dos · trois = tres · dix = diez · vingt = veinte · cinquante = cincuenta · cent = cien · le prix = el precio · l'euro = el euro · cher = caro · pas cher = barato · combien = cuánto
  - Frases: «C'est combien ?» = ¿Cuánto es? · «Ça coûte dix euros.» = Cuesta diez euros. · «C'est trop cher.» = Es demasiado caro. · «Deux, s'il vous plaît.» = Dos, por favor.
- **S4** · un café = un café · un thé = un té · de l'eau = agua · le lait = la leche · le sucre = el azúcar · un jus d'orange = un jugo de naranja · un croissant = un cruasán · une tasse = una taza · la carte = la carta · l'addition = la cuenta · avec = con · sans = sin
  - Frases: «Un café, s'il vous plaît.» = Un café, por favor. · «Je voudrais un thé sans sucre.» = Quisiera un té sin azúcar. · «Un croissant et un jus d'orange.» = Un cruasán y un jugo de naranja. · «L'addition, s'il vous plaît.» = La cuenta, por favor.

#### Alemán (de)
- **S1** · Hallo = hola · Guten Morgen = buenos días · Guten Tag = buenos días / buenas tardes · Guten Abend = buenas noches (al llegar) · Tschüss = chao (informal) · Auf Wiedersehen = adiós (formal) · bitte = por favor / de nada · danke = gracias · Entschuldigung = disculpe / perdón · ja = sí · nein = no · Wie geht's? = ¿qué tal?
  - Frases: «Guten Tag, Frau Müller!» = ¡Buenos días, señora Müller! · «Wie geht es Ihnen?» = ¿Cómo está usted? · «Gut, danke. Und Ihnen?» = Bien, gracias. ¿Y usted? · «Bis morgen!» = ¡Hasta mañana!
- **S2** · ich heiße = me llamo · ich bin = soy · ich komme aus = soy de · wohnen = vivir · das Land = el país · die Stadt = la ciudad · der Student / die Studentin = el/la estudiante · der Lehrer / die Lehrerin = el/la profesor/a · der Freund / die Freundin = el amigo / la amiga · Freut mich! = ¡Mucho gusto! · wie = cómo · woher = de dónde
  - Frases: «Ich heiße Ana.» = Me llamo Ana. · «Wie heißen Sie?» = ¿Cómo se llama usted? · «Woher kommst du?» = ¿De dónde eres? · «Ich komme aus Ecuador.» = Soy de Ecuador. · «Ich wohne in Quito.» = Vivo en Quito.
- **S3** · eins = uno · zwei = dos · drei = tres · zehn = diez · zwanzig = veinte · fünfzig = cincuenta · hundert = cien · der Preis = el precio · der Euro = el euro · billig = barato · teuer = caro · wie viel = cuánto
  - Frases: «Wie viel kostet das?» = ¿Cuánto cuesta esto? · «Das kostet zehn Euro.» = Cuesta diez euros. · «Das ist zu teuer.» = Es demasiado caro. · «Zwei, bitte.» = Dos, por favor.
- **S4** · der Kaffee = el café · der Tee = el té · das Wasser = el agua · die Milch = la leche · der Zucker = el azúcar · der Saft = el jugo · der Kuchen = el pastel · das Brötchen = el panecillo · die Tasse = la taza · die Karte = la carta · die Rechnung = la cuenta · mit / ohne = con / sin
  - Frases: «Einen Kaffee, bitte.» = Un café, por favor. (acusativo; se enseña como chunk) · «Ich möchte einen Tee mit Milch.» = Quisiera un té con leche. · «Ein Stück Kuchen, bitte.» = Un trozo de pastel, por favor. · «Zahlen, bitte!» = ¡La cuenta, por favor!

#### Portugués (pt, variante BR por defecto)
- **S1** · oi = hola (informal) · olá = hola · bom dia = buenos días · boa tarde = buenas tardes · boa noite = buenas noches · tchau = chao · até logo = hasta luego · por favor = por favor · obrigado / obrigada = gracias (según quien habla) · de nada = de nada · desculpe = disculpe · tudo bem? = ¿todo bien?
  - Frases: «Oi, tudo bem?» = Hola, ¿todo bien? · «Tudo bem, e você?» = Todo bien, ¿y tú? · «Muito obrigada!» = ¡Muchas gracias! (dicho por una mujer) · «Até amanhã!» = ¡Hasta mañana!
- **S2** · meu nome é = mi nombre es · eu sou = yo soy · sou de = soy de · morar = vivir · o país = el país · a cidade = la ciudad · estudante = estudiante · professor / professora = profesor/a · amigo / amiga = amigo/a · prazer = mucho gusto · como = cómo · onde = dónde
  - Frases: «Meu nome é Ana.» = Me llamo Ana. · «Como você se chama?» = ¿Cómo te llamas? · «Eu sou do Equador.» = Soy de Ecuador. · «Moro em Quito.» = Vivo en Quito. · «Muito prazer!» = ¡Mucho gusto!
- **S3** · um / uma = uno/una · dois / duas = dos · três = tres · dez = diez · vinte = veinte · cinquenta = cincuenta · cem = cien · o preço = el precio · o real (reais) = el real · barato = barato · caro = caro · quanto = cuánto
  - Frases: «Quanto custa?» = ¿Cuánto cuesta? · «Custa dez reais.» = Cuesta diez reales. · «Está muito caro.» = Está muy caro. · «Dois, por favor.» = Dos, por favor.
- **S4** · um café = un café · um chá = un té · água = agua · leite = leche · açúcar = azúcar · suco = jugo (PT: sumo) · pão de queijo = pan de queso · bolo = pastel · a xícara = la taza (PT: chávena) · o cardápio = la carta (PT: ementa) · a conta = la cuenta · com / sem = con / sin
  - Frases: «Um café, por favor.» = Un café, por favor. · «Eu queria um suco de laranja.» = Quería un jugo de naranja. · «Sem açúcar, por favor.» = Sin azúcar, por favor. · «A conta, por favor.» = La cuenta, por favor.

#### Italiano (it)
- **S1** · ciao = hola / chao (informal) · buongiorno = buenos días · buonasera = buenas tardes/noches · arrivederci = adiós · a presto = hasta pronto · per favore = por favor · grazie = gracias · prego = de nada · scusi = disculpe (Lei) · scusa = disculpa (tu) · sì / no = sí / no · come stai? = ¿cómo estás?
  - Frases: «Buongiorno, signora!» = ¡Buenos días, señora! · «Come sta?» = ¿Cómo está usted? · «Bene, grazie. E tu?» = Bien, gracias. ¿Y tú? · «A domani!» = ¡Hasta mañana!
- **S2** · mi chiamo = me llamo · sono = soy · vengo da = vengo de · abitare = vivir · il paese = el país · la città = la ciudad · studente / studentessa = estudiante · l'insegnante = el/la profesor/a · amico / amica = amigo/a · piacere = mucho gusto · come = cómo · dove = dónde
  - Frases: «Mi chiamo Ana.» = Me llamo Ana. · «Come ti chiami?» = ¿Cómo te llamas? · «Vengo dall'Ecuador.» = Vengo de Ecuador. · «Abito a Quito.» = Vivo en Quito. · «Piacere!» = ¡Mucho gusto!
- **S3** · uno = uno · due = dos · tre = tres · dieci = diez · venti = veinte · cinquanta = cincuenta · cento = cien · il prezzo = el precio · l'euro = el euro · economico = barato · caro = caro · quanto = cuánto
  - Frases: «Quanto costa?» = ¿Cuánto cuesta? · «Costa dieci euro.» = Cuesta diez euros. · «È troppo caro.» = Es demasiado caro. · «Due, per favore.» = Dos, por favor.
- **S4** · un caffè = un café (expreso) · un cappuccino = un capuchino · un tè = un té · l'acqua = el agua · il latte = la leche · lo zucchero = el azúcar · una spremuta = un jugo natural · un cornetto = un cruasán · la tazza = la taza · il menù = el menú · il conto = la cuenta · con / senza = con / sin
  - Frases: «Un caffè, per favore.» = Un café, por favor. · «Vorrei un cappuccino e un cornetto.» = Quisiera un capuchino y un cruasán. · «Senza zucchero, grazie.» = Sin azúcar, gracias. · «Il conto, per favore.» = La cuenta, por favor.

#### Chino mandarín (zh, simplificado + pinyin)
- **S1** · 你好 (nǐ hǎo) = hola · 您好 (nín hǎo) = hola (respetuoso) · 早上 好 (zǎoshang hǎo) = buenos días · 晚上 好 (wǎnshang hǎo) = buenas noches (al llegar) · 再见 (zàijiàn) = adiós · 谢谢 (xièxie) = gracias · 不 客气 (bú kèqi) = de nada · 对不起 (duìbuqǐ) = lo siento · 不好意思 (bù hǎoyìsi) = disculpe · 请 (qǐng) = por favor · 是 (shì) = sí / ser · 明天 见 (míngtiān jiàn) = hasta mañana
  - Frases: 你 最近 怎么样？(nǐ zuìjìn zěnmeyàng?) = ¿Qué tal te va? · 我 很 好，谢谢。(wǒ hěn hǎo, xièxie.) = Estoy bien, gracias. · 老师 好！(lǎoshī hǎo!) = ¡Hola, profesor/a! · 明天 见！(míngtiān jiàn!) = ¡Hasta mañana!
- **S2** · 我 (wǒ) = yo · 你 (nǐ) = tú · 叫 (jiào) = llamarse · 名字 (míngzi) = nombre · 是 (shì) = ser · 人 (rén) = persona · 厄瓜多尔 (Èguāduō'ěr) = Ecuador · 学生 (xuésheng) = estudiante · 老师 (lǎoshī) = profesor/a · 朋友 (péngyou) = amigo/a · 认识 (rènshi) = conocer · 哪 (nǎ) = cuál/qué · 什么 (shénme) = qué
  - Frases: 我 叫 安娜。(wǒ jiào Ānnà.) = Me llamo Ana. · 你 叫 什么 名字？(nǐ jiào shénme míngzi?) = ¿Cómo te llamas? · 我 是 厄瓜多尔 人。(wǒ shì Èguāduō'ěr rén.) = Soy ecuatoriano/a. · 你 是 哪 国 人？(nǐ shì nǎ guó rén?) = ¿De qué país eres? · 认识 你 很 高兴。(rènshi nǐ hěn gāoxìng.) = Encantado/a de conocerte.
- **S3** · 一 (yī) = uno · 二 (èr) = dos · 两 (liǎng) = dos (con clasificador) · 三 (sān) = tres · 十 (shí) = diez · 二十 (èrshí) = veinte · 一百 (yìbǎi) = cien · 块 (kuài) = yuan (coloquial) · 钱 (qián) = dinero · 多少 (duōshao) = cuánto · 贵 (guì) = caro · 便宜 (piányi) = barato · 个 (gè) = clasificador general
  - Frases: 这个 多少 钱？(zhège duōshao qián?) = ¿Cuánto cuesta esto? · 十五 块。(shíwǔ kuài.) = Quince yuanes. · 太 贵 了！(tài guì le!) = ¡Es demasiado caro! · 我 要 两 个。(wǒ yào liǎng gè.) = Quiero dos.
- **S4** · 咖啡 (kāfēi) = café · 茶 (chá) = té · 水 (shuǐ) = agua · 牛奶 (niúnǎi) = leche · 糖 (táng) = azúcar · 果汁 (guǒzhī) = jugo · 杯 (bēi) = taza/vaso (clasificador) · 大 杯 (dà bēi) = grande · 小 杯 (xiǎo bēi) = pequeño · 热 (rè) = caliente · 冰 (bīng) = con hielo · 菜单 (càidān) = menú · 买单 (mǎidān) = pagar la cuenta
  - Frases: 我 要 一 杯 热 咖啡。(wǒ yào yì bēi rè kāfēi.) = Quiero un café caliente. · 请 给 我 菜单。(qǐng gěi wǒ càidān.) = Deme el menú, por favor. · 不要 糖，谢谢。(bú yào táng, xièxie.) = Sin azúcar, gracias. · 服务员，买单！(fúwùyuán, mǎidān!) = ¡Camarero/a, la cuenta!
  - Nota: 你好吗 (nǐ hǎo ma) es de manual y poco natural en el uso real; se enseña, pero se marca como tal.

#### Japonés (ja, estilo です/ます)
- **S1** · こんにちは (konnichiwa) = hola / buenas tardes · おはよう ございます (ohayō gozaimasu) = buenos días · こんばんは (konbanwa) = buenas noches (al llegar) · さようなら (sayōnara) = adiós (despedida larga) · またね (mata ne) = hasta luego (informal) · ありがとう ございます (arigatō gozaimasu) = muchas gracias · どういたしまして (dō itashimashite) = de nada · すみません (sumimasen) = disculpe / perdón · ごめんなさい (gomen nasai) = lo siento · はい (hai) = sí · いいえ (iie) = no · おやすみなさい (oyasumi nasai) = buenas noches (al dormir)
  - Frases: おはよう ございます。(ohayō gozaimasu.) = Buenos días. · お元気 です か。(ogenki desu ka.) = ¿Cómo está? (tras un tiempo sin verse) · はい、元気 です。(hai, genki desu.) = Sí, estoy bien. · また 明日。(mata ashita.) = Hasta mañana.
- **S2** · わたし (watashi) = yo · 名前 (namae) = nombre · ～です (desu) = ser · ～人 (-jin) = de nacionalidad… · 日本 (Nihon) = Japón · エクアドル (Ekuadoru) = Ecuador · 学生 (gakusei) = estudiante · 先生 (sensei) = profesor/a · 友だち (tomodachi) = amigo/a · はじめまして (hajimemashite) = encantado/a (primer encuentro) · よろしく おねがいします (yoroshiku onegaishimasu) = un placer / cuento con usted · どこ (doko) = dónde · 何 (nan) = qué
  - Frases: はじめまして。(hajimemashite.) = Encantado/a. · わたし は アナ です。(watashi wa Ana desu.) = Soy Ana. · エクアドル 人 です。(Ekuadoru-jin desu.) = Soy ecuatoriano/a. · お名前 は？(onamae wa?) = ¿Su nombre? · よろしく おねがいします。(yoroshiku onegaishimasu.) = Mucho gusto.
- **S3** · いち (ichi) = uno · に (ni) = dos · さん (san) = tres · じゅう (jū) = diez · ひゃく (hyaku) = cien · せん (sen) = mil · 円 (en) = yen · いくら (ikura) = cuánto (precio) · 高い (takai) = caro · 安い (yasui) = barato · これ (kore) = esto · ひとつ (hitotsu) = uno (objeto) · ふたつ (futatsu) = dos (objetos)
  - Frases: これ は いくら です か。(kore wa ikura desu ka.) = ¿Cuánto cuesta esto? · 五百 円 です。(gohyaku en desu.) = Son 500 yenes. · これ を ふたつ ください。(kore o futatsu kudasai.) = Deme dos de estos. · ちょっと 高い です ね。(chotto takai desu ne.) = Es un poco caro, ¿no?
- **S4** · コーヒー (kōhī) = café · お茶 (ocha) = té · 水 (mizu) = agua · ミルク (miruku) = leche · さとう (satō) = azúcar · ジュース (jūsu) = jugo · ケーキ (kēki) = pastel · メニュー (menyū) = menú · お会計 (okaikei) = la cuenta · ホット (hotto) = caliente · アイス (aisu) = con hielo · ください (kudasai) = deme, por favor · おねがいします (onegai shimasu) = por favor
  - Frases: ホット コーヒー を ひとつ ください。(hotto kōhī o hitotsu kudasai.) = Un café caliente, por favor. · ミルク は いりません。(miruku wa irimasen.) = No necesito leche. · すみません、お会計 おねがいします。(sumimasen, okaikei onegai shimasu.) = Disculpe, la cuenta, por favor. · ここ で 食べます。(koko de tabemasu.) = Para comer aquí.
  - Nota: el personal responde en 敬語 (お召し上がりですか…). Se enseña a **reconocerlo** en A1, no a producirlo.

#### Coreano (ko, 해요체; romanización revisada)
- **S1** · 안녕하세요 (annyeonghaseyo) = hola · 안녕 (annyeong) = hola/chao (entre amigos) · 안녕히 가세요 (annyeonghi gaseyo) = adiós (a quien se va) · 안녕히 계세요 (annyeonghi gyeseyo) = adiós (a quien se queda) · 감사합니다 (gamsahamnida) = gracias (formal) · 고마워요 (gomawoyo) = gracias · 천만에요 (cheonmaneyo) = de nada · 죄송합니다 (joesonghamnida) = lo siento (formal) · 미안해요 (mianhaeyo) = perdón · 네 (ne) = sí · 아니요 (aniyo) = no · 또 만나요 (tto mannayo) = nos vemos
  - Frases: 안녕하세요! (annyeonghaseyo!) = ¡Hola! · 잘 지냈어요? (jal jinaesseoyo?) = ¿Qué tal has estado? · 네, 잘 지냈어요. (ne, jal jinaesseoyo.) = Sí, he estado bien. · 내일 봐요! (naeil bwayo!) = ¡Hasta mañana!
- **S2** · 저 (jeo) = yo (cortés) · 이름 (ireum) = nombre · 이에요 / 예요 (ieyo / yeyo) = ser (tras consonante / vocal) · 사람 (saram) = persona · 한국 (Hanguk) = Corea · 에콰도르 (Ekwadoreu) = Ecuador · 학생 (haksaeng) = estudiante · 선생님 (seonsaengnim) = profesor/a · 친구 (chingu) = amigo/a · 반갑습니다 (bangapseumnida) = encantado/a · 어디 (eodi) = dónde · 뭐 (mwo) = qué
  - Frases: 저는 아나예요. (jeoneun Ana-yeyo.) = Soy Ana. · 에콰도르 사람이에요. (Ekwadoreu saramieyo.) = Soy ecuatoriano/a. · 이름이 뭐예요? (ireumi mwoyeyo?) = ¿Cómo te llamas? · 만나서 반갑습니다. (mannaseo bangapseumnida.) = Encantado/a de conocerle.
- **S3** · 일 (il) = uno · 이 (i) = dos · 삼 (sam) = tres · 십 (sip) = diez · 백 (baek) = cien · 천 (cheon) = mil · 만 (man) = diez mil · 원 (won) = won · 얼마 (eolma) = cuánto · 비싸요 (bissayo) = es caro · 싸요 (ssayo) = es barato · 하나 / 둘 (hana / dul) = uno / dos (nativos, para contar) · 개 (gae) = clasificador de objetos
  - Frases: 이거 얼마예요? (igeo eolmayeyo?) = ¿Cuánto cuesta esto? · 만 원이에요. (man wonieyo.) = Son diez mil wones. · 너무 비싸요. (neomu bissayo.) = Es muy caro. · 두 개 주세요. (du gae juseyo.) = Deme dos.
- **S4** · 커피 (keopi) = café · 아메리카노 (amerikano) = americano · 차 (cha) = té · 물 (mul) = agua · 우유 (uyu) = leche · 설탕 (seoltang) = azúcar · 주스 (juseu) = jugo · 케이크 (keikeu) = pastel · 메뉴 (menyu) = menú · 잔 (jan) = taza (clasificador) · 따뜻한 (ttatteutan) = caliente · 아이스 (aiseu) = con hielo · 주세요 (juseyo) = deme, por favor · 계산 (gyesan) = pago / cuenta
  - Frases: 아이스 아메리카노 한 잔 주세요. (aiseu amerikano han jan juseyo.) = Un americano con hielo, por favor. · 설탕 빼 주세요. (seoltang ppae juseyo.) = Sin azúcar, por favor. · 포장해 주세요. (pojanghae juseyo.) = Para llevar, por favor. · 계산해 주세요. (gyesanhae juseyo.) = Cóbreme, por favor.
  - Nota: los precios se leen con números sino-coreanos (만 원) y los objetos se cuentan con números nativos (두 개, 한 잔). Hay que enseñar ambos sistemas antes de S3.

#### Ruso (ru)
- **S1** · здравствуйте (zdravstvuyte) = hola (formal) · привет (privet) = hola (informal) · доброе утро (dobroye utro) = buenos días · добрый день (dobryy den') = buenas tardes · добрый вечер (dobryy vecher) = buenas noches (al llegar) · до свидания (do svidaniya) = adiós · пока (poka) = chao · спасибо (spasibo) = gracias · пожалуйста (pozhaluysta) = por favor / de nada · извините (izvinite) = disculpe · да (da) = sí · нет (net) = no
  - Frases: Как у вас дела? (kak u vas dela?) = ¿Cómo le va? · Хорошо, спасибо. А у вас? (khorosho, spasibo. a u vas?) = Bien, gracias. ¿Y a usted? · Извините, пожалуйста. (izvinite, pozhaluysta.) = Disculpe, por favor. · До завтра! (do zavtra!) = ¡Hasta mañana!
- **S2** · я (ya) = yo · меня зовут (menya zovut) = me llamo · как (kak) = cómo · из (iz) = de (origen) · страна (strana) = país · город (gorod) = ciudad · жить (zhit') = vivir · студент / студентка (student / studentka) = estudiante · преподаватель (prepodavatel') = profesor/a · друг / подруга (drug / podruga) = amigo / amiga · очень приятно (ochen' priyatno) = mucho gusto · где (gde) = dónde
  - Frases: Меня зовут Ана. (menya zovut Ana.) = Me llamo Ana. · Как вас зовут? (kak vas zovut?) = ¿Cómo se llama usted? · Я из Эквадора. (ya iz Ekvadora.) = Soy de Ecuador. · Я живу в Кито. (ya zhivu v Kito.) = Vivo en Quito. · Очень приятно! (ochen' priyatno!) = ¡Mucho gusto!
- **S3** · один (odin) = uno · два (dva) = dos · три (tri) = tres · десять (desyat') = diez · двадцать (dvadtsat') = veinte · сто (sto) = cien · рубль (rubl') = rublo · цена (tsena) = precio · сколько (skol'ko) = cuánto · стоит (stoit) = cuesta · дорого (dorogo) = caro · дёшево (dyoshevo) = barato
  - Frases: Сколько это стоит? (skol'ko eto stoit?) = ¿Cuánto cuesta esto? · Сто рублей. (sto rubley.) = Cien rublos. · Это дорого. (eto dorogo.) = Es caro. · Два, пожалуйста. (dva, pozhaluysta.) = Dos, por favor.
  - Nota: la concordancia es 1 рубль / 2–4 рубля / 5+ рублей. Se enseña como chunk en A1.
- **S4** · кофе (kofe) = café (masculino) · чай (chay) = té · вода (voda) = agua · молоко (moloko) = leche · сахар (sakhar) = azúcar · сок (sok) = jugo · пирожное (pirozhnoye) = pastelito · чашка (chashka) = taza · меню (menyu) = menú · счёт (schyot) = cuenta · с (s) = con · без (bez) = sin
  - Frases: Кофе, пожалуйста. (kofe, pozhaluysta.) = Un café, por favor. · Можно чай с молоком? (mozhno chay s molokom?) = ¿Me da un té con leche? · Без сахара, пожалуйста. (bez sakhara, pozhaluysta.) = Sin azúcar, por favor. · Счёт, пожалуйста. (schyot, pozhaluysta.) = La cuenta, por favor.

## Sistema de reutilización y repaso de vocabulario

### Identidad léxica común (requisito previo)

- Formato del ID: `<idioma>:<lema>:<categoría>[:<sentido>]`, p. ej. `en:order:v:request`, `en:order:n:purchase`, `en:tap:n:faucet`, `en:tap:v:contactless`.
- Los chunks usan `en:chunk:could-i-have`.
- Cada ID apunta a un **concepto neutral** (`food.soup`) para enlazar idiomas.
- Todas las fuentes (`nivel-*.json`, situaciones, lectura/escucha, N0) deben referenciar IDs, no texto. Esto resuelve las 10 polisemias detectadas y permite medir la reutilización real.

### Estados y evidencia necesaria

| Estado | Evidencia mínima (sin ayuda salvo que se indique) | Tipos de actividad que la generan |
|---|---|---|
| **visto** | ≥ 1 exposición con significado (tarjeta, diálogo, lectura, audio) | Pasos 2, 3 y 5 de la mini-ruta |
| **reconocido** | 2 aciertos de reconocimiento, en **2 sesiones distintas** | Opción múltiple, emparejar, elegir imagen al oír la palabra |
| **recordado** | 1 recuperación sin opciones correcta **≥ 1 día después** de la exposición | L1→L2 escrito u oral, imagen→palabra, hueco sin banco |
| **producido** | 1 uso correcto en producción semilibre o libre, en contexto | Paso 8 sin opciones; turno de IA con `itemsUsados` = correcto (el tutor etiqueta; la transcripción **no** vale para pronunciación) |
| **dominado** | producido en **≥ 2 contextos distintos** (situación o unidad) + recuperación diferida correcta **≥ 21 días** después de la primera producción + sin fallos en las 2 últimas revisiones | Repaso espaciado + otra situación |

Degradación:
- Un fallo en una revisión de un ítem *dominado* lo baja a *recordado*.
- Dos fallos seguidos bajan un estado.
- Los aciertos con pista cuentan como exposición, no como evidencia.

Se conservan la primera respuesta y la ayuda recibida, coherente con `registrarPractica`, que ya guarda `primeraCorrecta`. Repetir la misma tarjeta el mismo día no sube de estado.

### Repetición espaciada

- **Cajas tipo Leitner** con intervalos de 1, 3, 7, 16, 35 y 90 días. Un acierto sube una caja; un fallo baja 2 cajas, con mínimo 1. El estado léxico condiciona el **tipo** de ejercicio de repaso:
  - reconocido → recuerdo;
  - recordado → hueco en frase nueva;
  - producido → mini-tarea situacional.
- **Sesión diaria**:
  - primero los vencidos (tope de 20);
  - después 5–8 nuevos, solo si hay < 30 vencidos;
  - composición 70–80 % conocido / 20–30 % nuevo;
  - intercalar categorías.
- **Reutilización programada**: cada situación declara `reutiliza[]` (≥ 60 % de su vocabulario A1/A2 debe venir de unidades o situaciones previas) y `alimenta[]`. El validador comprueba que cada ítem nuevo reaparezca en **≥ 3 contextos posteriores** en ≤ 2 niveles. Así se corrige el solape actual de 37 de 531 formas.
- **Selección contextual**: al abrir la situación X, los vencidos que pertenecen a X o a sus `alimenta[]` se practican dentro de la situación, no como tarjetas sueltas.
- El chat de IA recibe los ≤ 8 ítems en estado *recordado* de esa situación, para provocar su uso (`materialSituacion`).

### Almacenamiento y sincronización (Flutter web/móvil)

- **Local**: clave propia `vocab.v1.<idioma>` en SharedPreferences, separada de `progreso`. Hoy `_save` serializa y sube el estado completo en cada cambio (`providers.dart:333-338`), lo que no escala.
- **Formato compacto por ítem**: `{s: estado(0–4), b: caja, due: yyyymmdd, n: aciertos, l: fallos, ctx: [ids de contexto ≤ 5], ev: [últimas 5 evidencias {t, ok, ayuda, fecha}], u: updatedAt}`.
- **Tamaño**: con 3.000 ítems a ~150 B son ~450 KB. Cabe en localStorage (web, ~5 MB) y en móvil.
- **Sincronización**: `POST /progreso/vocab` con **deltas** (ítems con `u` > último sync). Fusión en el servidor por ítem:
  - `u` más reciente gana en `s`, `b` y `due`;
  - `n` y `l` = máximo;
  - `ev` = unión ordenada, recortada a 5.

  Funciona sin conexión; el servidor nunca rebaja un estado sin evidencia.
- **Métricas visibles**: «palabras vistas» (lo que hoy llama `vocabularioAprendido`), «recordadas», «dominadas». Se recomienda **renombrar** el contador actual, que hoy sugiere aprendizaje con solo haber visto tarjetas.

## Decisiones que requieren revisión humana

1. **Niveles 3–10 en los 9 idiomas distintos del inglés muestran contenido en inglés** (`_bancoGenerico`). Hay que decidir si se bloquean u ocultan esos niveles hasta tener contenido, o si se genera. Afecta a lo que promete el plan de pago («10 niveles · 1 000 lecciones», `catalog.dart`).
2. **Variedad del inglés**: el léxico es británico y el TTS es en-US. Opciones: US por defecto con alias UK (la que propongo) o cambiar el TTS a en-GB. También hay que decidir la aceptación de ambas variantes en corrección libre.
3. **Español como idioma meta con interfaz en español**: hay que definir el público (¿hablantes de otras lenguas?) y si se usa glosa monolingüe; también la variante ES o LatAm.
4. **pt-BR frente a pt-PT**, y la **moneda y el país de referencia** por idioma en precios (USD, EUR, BRL, CNY, JPY, KRW, RUB).
5. **Nivel de cortesía por defecto**:
   - ja: です/ます en A1; 敬語 solo receptivo;
   - ko: 해요체, con 합쇼체 solo en fórmulas;
   - ru, fr, de, it, es: se propone **usted/vous/Sie/Lei/вы** en situaciones de servicio y tú en S2 entre pares.
6. **Umbrales de «dominado»** (2 contextos + 21 días) e intervalos del repaso. Deben pilotarse con alumnos y docentes.
7. **Situaciones sensibles o por edad** (9, 15, 16, 29, 45; laborales 20–25): definir `edadMinima` y si se muestran a menores. Ya se señaló en `docs/VOCABULARIO-ESCOLAR.md`.
8. **Nivel de cada situación**: aprobar la columna «Mín. propuesto» y la regla de «ninguna gramática superior salvo chunk marcado».
9. **Temas gramaticales nuevos** (polite-requests, countable-uncountable, imperatives, indirect-questions…) para el grafo del agente A.
10. **Revisión nativa obligatoria** del contenido de la sección multilingüe antes de pasarlo a assets. Puntos de especial cuidado: tonos de zh (一/不 sandhi), elección 이에요/예요 en ko, casos en ru, concordancia de género en fr/pt/es, y datos culturales de propina (son orientativos).

## Fuentes (fecha 2026-09-26)

Repositorio (rama `claude/educacion-multilenguaje`, leído el 2026-09-26):
- `assets/contenido/en/situaciones.json` y `backend/src/content/situaciones-en.json` (idénticos, verificado con `cmp`).
- `assets/contenido/en/situational_vocabulary.json` y `backend/src/content/situational-vocabulary-en.json` (idénticos).
- `assets/contenido/<10 idiomas>/nivel-0.json`, `nivel-1.json`, `nivel-2.json`.
- `assets/contenido/en/reading_units.json`, `listening_units.json`, `biblioteca.json`, `diagnostico.json`.
- `lib/core/content/curriculum.dart` (idiomas; `_bancoGenerico` 349–414; `unidadesDe` 431–459), `idiomas.dart` (`_n1`, `_apoyo`, `bancoNivel1`, `localeVoz`), `situation_units.dart`, `catalog.dart` (50 situaciones, `perfilesNivel`), `contenido_json.dart`.
- `lib/features/situations/situation_screen.dart`, `lib/core/state/providers.dart` (`vocabularioAprendido`, `registrarPractica`, `guardarTurnoSituacion`, `_save`).
- `backend/src/lib/situaciones.ts`.
- `docs/VOCABULARIO-ESCOLAR.md`, `docs/situaciones-ia.md`, `docs/TEMARIO-GRAMATICA-PROPUESTO.json`.

Referencias externas (conocimiento general; **no consultadas en línea en esta sesión** y sin contenido copiado):
- Council of Europe, *CEFR Companion Volume* (2020), para descriptores «Puedo…» y la noción de tarea.
- Nation, I. S. P., *Learning Vocabulary in Another Language* (2.ª ed., 2013), para exposición repetida y el paso de receptivo a productivo.
- Cepeda et al. (2006), *Psychological Bulletin*, metaanálisis sobre práctica distribuida, como base de los intervalos crecientes.
- Las listas de Cambridge A2/B1 ya citadas en `docs/VOCABULARIO-ESCOLAR.md` se usan solo como referencia editorial.
