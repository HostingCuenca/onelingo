# Plan del curso de portugués de Brasil

Estado: **Nivel 0, Fundamentos y N1 completos con GO editorial; outline N2 y C01–C10 aprobados en staging; idioma inactivo** · Fecha: 2026-10-03 · Alcance: Nivel 0, Fundamentos y N1–N10. Antes de activar el idioma quedan por elegir y probar dos voces nativas brasileñas, producir/revisar el contraste auditivo F6, cerrar la aprobación/refuerzo determinista del Nivel 0 en el runtime y crear/validar el diagnóstico N1 contra la futura ruta publicada.

Este documento reemplaza cualquier planificación portuguesa anterior. El material retirado a `docs/archivo/pt-legacy-2026-10-03/` es solo histórico y no puede usarse como fuente del curso nuevo.

## 1. Decisiones congeladas

- Variante productiva: **portugués de Brasil (pt-BR)**. El portugués europeo entra solo para reconocimiento desde niveles avanzados.
- Identificador técnico del idioma en assets, progreso y voz: **`pt`**. `pt-BR` describe la variante pedagógica; no se usa como código JSON porque el runtime trabaja con códigos ISO de dos letras.
- Escala del cliente: N1=A1, N2=A2, N3–N4=B1, N5–N7=B2 y N8–N10=C1.
- Volumen: **50 clases por nivel**, 10 bloques de 5; total N1–N10: 500 clases.
- Antes de N1: **Nivel 0 profundo de 10 unidades y 40 microlecciones**, seguido por **Fundamentos de 8 unidades**.
- Todo el contenido nuevo nace con apoyo `{"es": ..., "en": ...}`; español latinoamericano e inglés americano.
- Las explicaciones, ejercicios y repasos son editoriales y deterministas. El tutor IA no es necesario para cursar ni aprobar.
- Portugués no se activa en la ruta nueva hasta tener Nivel 0, Fundamentos, N1, banco de ubicación N1 y pruebas en verde.
- `revision: "inicial"` se mantiene hasta una revisión humana nativa de pt-BR.

## 2. Para quién empieza desde cero

El alumno de Nivel 0 puede no saber qué es Brasil, dónde se habla portugués ni cómo suena el idioma. No se presupone que reconoce `ão`, `nh`, `lh`, `ç`, vocales abiertas/cerradas ni la reducción de vocales finales. Tampoco se presupone que entiende que portugués y español son lenguas distintas.

La primera experiencia debe dejar cuatro ideas claras:

1. Brasil es el país de referencia y el curso enseña el uso brasileño contemporáneo.
2. El portugués se parece al español por escrito, pero **no se puede leer como español**.
3. El alumno aprende primero por oído, luego ve la grafía y finalmente lee y escribe.
4. Las variantes regionales existen; se enseña una forma productiva clara y se entrena reconocimiento gradual.

## 3. Nivel 0 · Leer y pronunciar pt-BR

Diez unidades, cuatro microlecciones de 5–8 minutos cada una. Cada microlección sigue: escuchar sin texto → descubrir la grafía → discriminar → construir/leer → repetir → mini lectura. No introduce conjugaciones ni explicaciones gramaticales largas.

| Unidad | Microlecciones | Resultado observable |
|---|---|---|
| P1 · Olá, Brasil | 1) Brasil y el portugués; 2) oi/olá/tchau; 3) sim/não/obrigado(a); 4) prueba auditiva inicial | Reconoce el idioma, saluda y responde de oído sin necesitar leer |
| P2 · Letras y nombres | 1) vocales y consonantes transparentes; 2) nombres de A–M; 3) N–Z; 4) deletrear nombre, ciudad y correo | Deletrea datos básicos y reconoce las 26 letras |
| P3 · El aire sale por la nariz | 1) ã y õ; 2) ão/ãe/õe; 3) vocal + m/n; 4) pares como `pão/pau`, `bom/boa` | Identifica nasal/oral y lee las grafías nasales frecuentes |
| P4 · Vocales abiertas y cerradas | 1) é/ê; 2) ó/ô; 3) e/o sin tilde según la sílaba; 4) `avó/avô`, `sede/sede` en contexto | Distingue vocal abierta/cerrada y usa el acento como pista, no como adorno |
| P5 · Finales y ritmo brasileño | 1) e final que se acerca a i; 2) o final que se acerca a u; 3) sílaba tónica; 4) ritmo en palabras y grupos cortos | Lee `nome`, `noite`, `livro`, `bonito` sin pronunciación española literal |
| P6 · R, RR, S y L | 1) r inicial/rr; 2) r intervocálica; 3) s/ss/z y s final; 4) l final brasileña | Distingue `caro/carro`, `casa/caça` y reconoce variación regional sin imitar todas las variantes |
| P7 · Sonidos escritos con dos letras | 1) nh; 2) lh; 3) ch; 4) c/ç/qu, g/gu/j y x de alta frecuencia | Lee `manhã`, `filho`, `chave`, `açúcar`, `queijo`, `gente` |
| P8 · Ti, di y habla conectada | 1) `ti` antes de i; 2) `di` antes de i; 3) enlaces y reducción entre palabras; 4) `para`→`pra`, `está`→`tá` y dictado corto, solo para reconocer | Entiende formas frecuentes del habla sin exigirlas todavía en producción |
| P9 · Acentos y escritura práctica | 1) agudas/graves/esdrújulas sin metalenguaje excesivo; 2) ´ y ^; 3) ~ y ç; 4) nombres, direcciones, precios y carteles | Copia y escribe palabras frecuentes respetando diacríticos que cambian sonido o sentido |
| P10 · Ya puedes empezar | 1) leer un letrero; 2) entender un audio corto; 3) leer un mensaje; 4) prueba final y ruta de refuerzo | Supera una comprobación de lectura, escucha y repetición o recibe unidades concretas para repasar |

### Prueba final del Nivel 0

La comprobación se reparte entre las cuatro microlecciones de P10; no se intenta fingir todo el examen en una sola pantalla. Debe contener, como mínimo:

- 10 ítems auditivos puntuables y aprobar al menos 8;
- 5 contrastes puntuables (nasal/oral, abierta/cerrada, r/rr) y aprobar al menos 4;
- 8 palabras y 2 pseudopalabras construidas solo con patrones enseñados;
- un ejercicio de deletreo/copia de nombre o correo;
- comprensión silenciosa de un mensaje funcional de 25–40 palabras;
- una respuesta determinista a un saludo y un agradecimiento.

El GO exige al menos 80 % de los ítems autocorregibles de P10. Los fallos se agrupan en categorías que remiten a P3–P9. El contenido solo puede usar tipos de paso que soporte el runtime: no se inventa un tipo JSON `ruta_refuerzo`. Antes de activar portugués, el runtime debe calcular y mostrar las unidades de refuerzo a partir de esos grupos y no puede registrar el Nivel 0 como aprobado si no se alcanza el umbral.

Los sonidos aislados o pares mínimos que el TTS no produzca con fiabilidad se graban o revisan por oído humano antes de publicar. `avó/avô`, nasales y `pão/pau` no pueden evaluarse solo por texto normalizado.

### Inventario sonoro congelado

El mapa `sonidos.json` usa exactamente estos doce ids: `a`, `i`, `u`, `e-fechado`, `e-aberto`, `o-fechado`, `o-aberto`, `a-nasal`, `e-nasal`, `i-nasal`, `o-nasal`, `u-nasal`. `ão`, `ãe`, `õe`, `em` y otras grafías se asocian a esos sonidos o secuencias; no se inventan fonemas adicionales para satisfacer la interfaz.

Claves de lectura/pronunciación que aporta Nivel 0 a Fundamentos y N1:

`sound-text`, `alphabet`, `diacritics`, `spelling`, `word-stress`, `open-closed-vowels`, `nasals`, `final-vowel-reduction`, `lh-nh`, `cedilla`, `s-z`, `r-rr`, `br-palatalization`, `final-l`, `pronunciation-variation`, `connected-speech`.

### Política de variación

| Rasgo | Voz modelo | Se acepta/reconoce | Nunca se exige |
|---|---|---|---|
| e/o finales átonas | reducción urbana brasileña clara | reducción menor o realizaciones regionales inteligibles | imitar una reducción exacta |
| t/d + i | realización de las voces elegidas | forma palatalizada y no palatalizada | tratar una de las dos como error |
| l final | realización de las voces elegidas | realizaciones regionales inteligibles | una única pronunciación nacional |
| r/rr y r final | contraste funcional del modelo | variantes brasileñas que conservan inteligibilidad | copiar el punto de articulación del narrador |
| s final | realización de las voces elegidas | sibilantes regionales brasileñas | adoptar el acento de Río o São Paulo |

La repetición y la lectura en voz alta son **práctica no bloqueante**. La aprobación automática del Nivel 0 depende únicamente de discriminación auditiva, asociación audio-texto, lectura silenciosa, deletreo y construcción/dictado deterministas. La pronunciación humana solo puede ser evaluada por una rúbrica humana u offline futura, nunca por semejanza obligatoria con el acento del TTS.

## 4. Fundamentos · ocho unidades nuevas

Fundamentos usa lo aprendido en Nivel 0 para construir las primeras frases. No vuelve a enseñar el alfabeto como si el alumno no lo hubiera visto.

| Unidad | Contenido | Resultado |
|---|---|---|
| F1 · Primer contacto | oi/olá, bom dia/boa tarde/boa noite, tchau, por favor, com licença, desculpa, obrigado/obrigada | Mantiene un intercambio de supervivencia de 3–4 turnos |
| F2 · Personas y tratamiento | `eu`, `você`, `a gente`, `vocês`, o senhor/a senhora; `tu` solo receptivo/regional | Elige tratamiento y usa `você/a gente` con 3.ª persona |
| F3 · Identidad y estado | presente mínimo de `ser`, `estar`, `estar com`; concordancia singular básica | Dice quién es, cómo está y dónde está |
| F4 · Artículos y concordancia | o/a, um/uma, género léxico y adjetivo singular | Nombra personas y cosas sin asumir el género español |
| F5 · Origen, lugar y contracciones | `em/de + o/a`; no/na/do/da; ciudades frente a países y artículos léxicos por país | Dice dónde vive y de dónde es con la contracción correcta |
| F6 · Preguntar, negar y reparar | não; entonación; onde/como/quem/o que; repetir, más despacio y no entiendo | Pregunta y repara una conversación inicial |
| F7 · Nombre y datos | nombre, apellido, deletreo aplicado, nacionalidad, ciudad y datos de contacto mínimos | Intercambia y confirma datos personales |
| F8 · Mi presentación | integración de F1–F7 y falsos amigos iniciales | Presentación de 6–8 frases y entrevista breve |

El último nodo canónico será `pt.f0.apresentar-se`; `pt.n1.c01` dependerá de él.

### Claves canónicas de Fundamentos

| Unidad | Introduce |
|---|---|
| F1 | `greetings`, `obrigado-agreement` |
| F2 | `subj-pron`, `voce-3rd`, `a-gente`, `o-senhor` |
| F3 | `ser-present`, `estar-present`, `estar-com`, `adj-gender-basic` |
| F4 | `articles-singular`, `noun-gender-basic` |
| F5 | `contraction-em`, `contraction-de`, `country-articles` |
| F6 | `nao-basic`, `intonation-q`, `wh-basic`, `repair-survival` |
| F7 | `spelling-applied`, `nationality-gender`, `personal-data` |
| F8 | `introduce-self`, `false-friends-basic` |

`curriculo/pt/n1.json` debe declarar como `previos` exactamente las 16 claves de Nivel 0 y las 24 claves de esta tabla. N1 las usa mediante `recicla`; cualquier extensión nueva recibe una clave distinta y observable.

Las ocho fichas detalladas ya están congeladas en `curriculo/pt/f0.json`: 24 claves, 102 entradas de vocabulario y, por ficha, 3 ejercicios guiados, 3 independientes, una situación con 2 preguntas y 5 ítems de evaluación. La conversión ejecutable hizo visibles `muito` y `também`, que las fichas ya usaban, y los incorporó al inventario canónico. Las fichas obtuvieron GO independiente y pasan `python3 tools/curriculo/validar_fundamentos.py pt` con 0 errores.

La ruta ejecutable correspondiente obtuvo GO editorial y permanece aislada en `tools/contenido/ruta-pt/borrador-f0.json`: 8 unidades, 102 vocablos, 104 ejercicios y 0 errores de esquema estricto. El acta está en `tools/contenido/ruta-pt/revision-f0.md`. No puede copiarse a `assets/` hasta producir y revisar por oído el contraste A→B de F6; este hito **no** activa portugués ni sustituye las voces y cambios de runtime pendientes.

## 5. Anatomía de las clases N1–N10

- Explicación breve y concreta; N1 abre siempre con un recordatorio sonoro del Nivel 0.
- 5–8 ejemplos con audio.
- 6–12 unidades de vocabulario enseñadas visiblemente.
- Patrón o tabla cuando corresponda.
- Práctica guiada (3–5), independiente (3–4), situación con lectura/diálogo y evaluación (4–8, al menos tres formatos en la ficha).
- Repaso acumulativo real: no crear una clave nueva para renombrar algo ya enseñado.
- Cada bloque termina con transferencia; cada nivel termina con proyecto y prueba.
- Desde N5 se incorporan tareas integradas inspiradas en Celpe-Bras: escuchar o leer para escribir/hablar con propósito, destinatario y género textual definidos.

## 6. Progresión de N1–N10

El tema de cada bloque viene de `curriculo/marco.json`. Esta tabla fija la adaptación lingüística portuguesa que deben desarrollar las 5 fichas de cada bloque.

### N1 · A1

| B | Foco portugués |
|---|---|
| 1 | reciclar saludos/tratamiento; ampliar con `chamar-se`, presentaciones de terceros, nacionalidades y deletreo social |
| 2 | presente regular completo, profesiones, idiomas, `gostar de` y grado (`um pouco`, `bem`) |
| 3 | ampliar artículos/género al plural; introducir `ter`, edad, familia, posesivos y `tem/há` por registro |
| 4 | ampliar interrogativos/negación, números, teléfono/correo y confirmación de datos |
| 5 | pedir con `queria/gostaria`, precios en reales, pagar, ropa, colores y demostrativos |
| 6 | hora, días, rutina, reflexivos, frecuencia; reciclar `a gente` en ocio |
| 7 | descripción; reciclar `ser/estar` e introducir `ficar`, `morar`, `vir`, ciudad y contracciones ampliadas |
| 8 | querer/poder/dever, comida, cantidades, `muito/pouco`, números grandes |
| 9 | indicaciones, imperativo inicial, transporte, `ir + infinitivo`, invitaciones y fechas |
| 10 | pretérito perfeito inicial, fin de semana, `desde/faz`, repaso y proyecto A1 |

### N2 · A2

| B | Foco portugués |
|---|---|
| 1 | presente irregular frecuente, `estar + gerúndio`, `costumar`, adverbios y jornada |
| 2 | pretérito perfeito completo, imperfeito introductorio, secuencia y recuerdos |
| 3 | casa/barrio, objeto indirecto, `estar + particípio`, `ficar`, problemas domésticos |
| 4 | futuro con `ir`, futuro simple de reconocimiento/producción gradual, clima y citas |
| 5 | comparativos/superlativos, talla, devolución y pronombres objeto del uso brasileño |
| 6 | receta, imperativo, `se` impersonal, cortesía y sabores |
| 7 | viajes, participios, `já/ainda/nunca`, avisos y `por/para` |
| 8 | síntomas, `doer`, `estar com`, consejos, duración y hábitos saludables |
| 9 | favores, permiso, obligación, prohibición e imperativos irregulares frecuentes |
| 10 | perfeito vs imperfeito inicial, proyecto de viaje y cierre A2 |

### N3 · B1 inicial

| B | Foco portugués |
|---|---|
| 1 | cambios/logros, presente do subjuntivo, reacciones y deseos |
| 2 | perfeito vs imperfeito, incidentes, `estava + gerúndio`, denuncia y secuencia |
| 3 | relativos, relaciones, verbos de cambio, sentimientos + subjuntivo y tradiciones |
| 4 | `se + presente/futuro`, futuro do subjuntivo inicial, planes condicionados e imperativo negativo |
| 5 | reclamaciones de viaje, condicional/futuro do pretérito, cortesía y pronombres en perífrasis |
| 6 | consejos + subjuntivo, finalidad (`para que`), hábitos y perífrasis aspectuales |
| 7 | procesos y averías, infinitivo personal inicial, relativos con preposición, pasiva de reconocimiento y `serve para` |
| 8 | discurso indirecto, preguntas/peticiones transmitidas y atención al cliente |
| 9 | opinión, indicativo/subjuntivo, noticias, cine, música y evidencia |
| 10 | conectores de causa/consecuencia, proyecto comunitario y cierre B1 inicial |

### N4 · B1 consolidación

| B | Foco portugués |
|---|---|
| 1 | `pretérito perfeito composto` (`tenho feito`) frente al perfecto español; mais-que-perfeito composto, hábitos pasados y cronología |
| 2 | deseos, lamentos, probabilidad, `devia ter` y grados de certeza |
| 3 | relativo + subjuntivo, contrato, convivencia, reciprocidad y reparación |
| 4 | correo formal, petición condicional, plazos, números/decimales y reclamación |
| 5 | experiencia profesional, entrevista, verbos con preposición y derivación |
| 6 | registro, atenuación, tratamiento, reunión y diferencias habla/escritura |
| 7 | personalidad, ocio, `ser/estar/ficar`, indefinidos y gerundio de modo |
| 8 | viaje autónomo, `caso`, `por se`, `apesar de`, normas e imprevistos |
| 9 | tradición/ambiente, causa formal, propuestas impersonales y comparación cultural |
| 10 | `embora` + subjuntivo, otros organizadores discursivos y proyecto B1 |

### N5 · B2 inicial

| B | Foco portugués |
|---|---|
| 1 | imperfecto do subjuntivo, cambios de vida, pasiva, infinitivo compuesto |
| 2 | condicional compuesto, probabilidad pasada, hipótesis con `se` y ocasiones perdidas |
| 3 | relativos complejos, narración rica, imprevistos y recomendación de destinos |
| 4 | reseña, lenguaje sensorial, colocaciones gastronómicas y cultura alimentaria |
| 5 | causa/efecto, evidencia, prevención, voz pasiva y divulgación científica |
| 6 | discurso indirecto completo, correlación temporal, colocación pronominal del habla brasileña frente a norma escrita y fidelidad a fuentes |
| 7 | hecho/opinión, modalización, fuente, titular y sesgo |
| 8 | concesión, desacuerdo cortés, ética y términos medios |
| 9 | liderazgo, instrucciones, prioridades, cifras y reporte de avance |
| 10 | tarea integrada tipo Celpe-Bras: insumo + texto con propósito; cierre B2 inicial |

### N6 · B2 consolidación

| B | Foco portugués |
|---|---|
| 1 | comparación generacional, referentes, cohesión y argumentación oral |
| 2 | contratos, garantías, condiciones reales/hipotéticas y lenguaje jurídico accesible |
| 3 | valoración del pasado, obligación/expectativa, crítica constructiva |
| 4 | atenuadores, preguntas indirectas, eufemismo y colocación pronominal formal en la cortesía profesional brasileña |
| 5 | énfasis, contraste, preguntas retóricas y persuasión publicitaria |
| 6 | reuniones, turnos, acta, plazos, seguimiento y responsabilidades |
| 7 | negociación con condiciones, concesiones, contraofertas y confirmación escrita |
| 8 | presentación pública, reformulación, manejo de preguntas y síntesis oral |
| 9 | datos, tendencias, comparación prudente y predicción matizada |
| 10 | debate + informe + negociación integrados; cierre B2 consolidado |

### N7 · B2 alto

| B | Foco portugués |
|---|---|
| 1 | registro coloquial/neutro/formal, connotación y reformulación |
| 2 | cronologías complejas y control de tiempos/modos en relatos largos |
| 3 | escenarios alternativos, certeza/duda y evidencia explícita |
| 4 | historia de lugares/objetos, pasiva, agentes, fuentes y exposición |
| 5 | metáforas, comparaciones, modismos brasileños frecuentes y humor contextual |
| 6 | tesis, evidencia, contraargumento, réplica y cierre |
| 7 | negociación multipartita, ofertas condicionadas y acuerdo escrito |
| 8 | contacto cultural, generalización prudente y pt-BR regional de reconocimiento |
| 9 | narrador, punto de vista, diálogo, reseña y recomendación literaria/cinematográfica |
| 10 | caso nuevo con análisis, debate y revisión; cierre B2 alto |

### N8 · C1 inicial

| B | Foco portugués |
|---|---|
| 1 | habla rápida, reducción, enlaces, turnos y aclaraciones precisas |
| 2 | implícito, ironía suave, presuposición, atenuación e inferencia |
| 3 | recursos persuasivos, encuadre, eslogan, campaña y análisis crítico |
| 4 | variedades de Brasil y reconocimiento inicial de pt-PT, sin mezcla productiva |
| 5 | modismos/refranes en contexto y control de registro |
| 6 | pódcast, cine y televisión: tomar notas, resumir y comentar |
| 7 | memoria, crónica, literatura brasileña con fragmentos autorizados o propios y estilo evocador |
| 8 | reclamación escalada, seguimiento, carta formal y cierre documentado |
| 9 | lenguaje académico, cautela, fuentes, gráficos y exposición |
| 10 | proyecto cultural integrado y cierre C1 inicial |

### N9 · C1 profesional

| B | Foco portugués |
|---|---|
| 1 | networking, afinidad, identidad profesional y seguimiento |
| 2 | relato profesional con gancho, tensión, giro y aprendizaje |
| 3 | mensaje ejecutivo, pirámide invertida, síntesis y brevedad |
| 4 | moderación de reuniones, desacuerdo, resumen de posturas y acta |
| 5 | entrevistas, método STAR adaptado, candidatura y preguntas estratégicas |
| 6 | informe, datos, límites de la evidencia, fuentes y recomendaciones |
| 7 | evaluación de riesgos, advertencia y prevención en varios sectores |
| 8 | normas, trámites brasileños, deberes, derechos y explicación pública clara |
| 9 | conflicto, intereses, reparación, mediación y acuerdo |
| 10 | propuesta profesional con calendario, presupuesto, riesgos y defensa oral |

### N10 · C1 dominio

| B | Foco portugués |
|---|---|
| 1 | conversación larga natural, elipsis, marcadores y cambio de tema |
| 2 | narración avanzada, ritmo, escena, voz y desenlace |
| 3 | humor, ironía, exageración y referencias culturales sin estereotipos |
| 4 | diplomacia, concesión, refutación y protección de la imagen del interlocutor |
| 5 | escritura académica extensa, síntesis de fuentes y discusión cauta |
| 6 | proyecto/negocio, financiación, contingencias, pitch y negociación |
| 7 | crítica cultural con vocabulario evaluativo y contexto |
| 8 | inmersión práctica en Brasil: servicios, barrio, trabajo e imprevistos |
| 9 | mediación entre personas y textos; adaptación para distintos públicos |
| 10 | proyecto final integrado inspirado en usos reales y tareas Celpe-Bras |

## 7. Evaluación

OneLingo mantiene su escala MCER para N1–N10. Celpe-Bras no sustituye esa escala: sirve como referencia brasileña de tareas comunicativas integradas y géneros reales. Desde B2 cada cierre debe combinar insumo oral o escrito, propósito, interlocutor y producto.

La ubicación v2 tendrá 18 ítems por nivel y cinco habilidades, y solo incluirá niveles publicados consecutivos. Nivel 0 tiene una prueba de salida propia y Fundamentos termina con entrevista/presentación breve.

Rangos orientativos que se congelan antes de las fichas: N1 situación 30–60 palabras y producción 30–50; N2 80–150 y producción 60–100; N3–N4 150–250 y producción 120–180; N5–N7 300–500 y producción 200–300; N8–N10 400–700 y producción 250–400. La producción abierta no sustituye los ítems autocorregibles necesarios para aprobar.

Cada bloque obtiene GO solo con ficha completa, `validar_plan.py`, validador de ruta del borrador, 100 % de apoyos ES/EN, norma pt-BR, audio normal/lento comprobado, una respuesta defendible por ítem, revisión separada desde ES y EN y revisor distinto del autor. El plan portugués no está completo hasta que existan **los diez archivos n1…n10**; que el validador actual permita archivos ausentes no equivale a GO.

## 8. Producción ordenada

1. Retirar el legado portugués de las fuentes activas (hecho; respaldo en `docs/archivo/pt-legacy-2026-10-03/`).
2. Congelar este plan y crear el diseño detallado del Nivel 0.
3. Escribir y revisar Nivel 0; validar con `validar_nivel0.py pt --bilingue`; implementar y probar el umbral/refuerzo determinista antes de activarlo.
4. Diseñar las ocho fichas detalladas de Fundamentos, congelar claves/ejercicios y obtener GO independiente (hecho: `curriculo/pt/f0.json`, 0 errores).
5. Escribir Fundamentos f0 nuevos desde las fichas; validar la ruta y obtener revisión separada ES/EN (GO editorial en staging; audio F6 bloquea publicación).
6. Crear y revisar las 500 fichas `curriculo/pt/n1.json`…`n10.json` (N1 completo con GO: 50/50 clases, 652 ejercicios y auditoría longitudinal; outline N2 aprobado en `tools/curriculo/pt/n2-outline.json`: 50/50 clases y 48 claves nuevas; N2 C01–C10 aprobadas con 130 ejercicios; C11–C50 y N3–N10 pendientes).
7. Producir situaciones y verbos portugueses con autor/revisor separados.
8. Crear `ENCARGO_RUTA_PT.md`, integrador portugués y pruebas específicas.
9. Poblar N1 por bloques B1→B10; crear diagnóstico N1 en paralelo.
10. Activar portugués solo tras N1 completo y probado.
11. Continuar N2→N10 sin saltos, con GO por bloque y auditoría longitudinal por nivel.

## 9. Fuentes rectoras

- Inep, Celpe-Bras: https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/celpe-bras/celpe-bras
- Documento base Celpe-Bras: https://download.inep.gov.br/publicacoes/institucionais/avaliacoes_e_exames_da_educacao_basica/documento_base_do_exame_celpe_bras.pdf
- ABL/VOLP (norma ortográfica brasileña): https://www.academia.org.br/nossa-lingua/busca-no-vocabulario
- Museu da Língua Portuguesa, variación del habla: https://acervo.museudalinguaportuguesa.org.br/acervos/8770/variacoes-no-falar-1
- Programas A1–C1 del Camões/QUAREPE, usados solo para progresión MCER, **no** como norma de léxico, pronunciación, gramática o registro pt-BR: https://www.instituto-camoes.pt/activity/o-que-fazemos/ensinar-portugues/professorado/programas-epe
- Marco común y reglas OneLingo: `curriculo/marco.json`, `PLAN_CLASES.md`, DEC-033 y DEC-034.
