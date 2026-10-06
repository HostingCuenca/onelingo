GO

# Revisión independiente N7 (alemán, método ligero), c01–c50

Archivos: `curriculo/de/n7.json` contra `tools/curriculo/de/n7-outline.json`. Campos del outline sin tocar (comprobado: solo cambia `ejercicios`). Validadores tras las correcciones: `validar_plan_detallado.py de curriculo/de/n7.json` = 0 errores (695 ejercicios, 695 ejemplos únicos); `validar_plan.py de` = 0 errores. Script: `scratchpad/de/fichas/rev-n7.py` (copia previa en `n7.backup.json`).

## Veredicto por criterio

1. **Alemán correcto:** muy bueno. Errores de lengua reales: 1) «sowohl … als auch» con verbo en singular en c31 (el estándar pide plural; corregido en 3 ítems); 2) c35 situación con «gilt die Vereinbarung schriftlich» y «bei spätem Zahlen» (no idiomático); 3) c05 «Ich denke in Gedanken an Sie» (redundante); 4) c41/c42 diálogo con «—Frase!, rief…» sin comillas y con coma mal colocada (ahora «—„…!“, rief…»); 5) c48 un ítem con «Das stimmt, was wir vereinbart haben» poco natural (reemplazado). Declinaciones, V2/verbo final, Konj. I/II, genitivos preposicionales y mayúsculas, bien.
2. **Una sola respuesta:** el problema dominante. Corregidos `escribir` con orden libre (bitte, jedoch, Vorfeld, año tras el verbo, sujeto antes/después de «doch»), `completar` con sinónimos válidos (aber/doch, Soweit/Soviel, Sofern/Soweit, Ehe/Bevor, verblüfft/irritiert, Flut/Lawine, zer-/ver-, ironisch/sarkastisch, vereinbart…), dos `ordenar` con dos órdenes (c17), un `relacionar` arbitrario (c13) y un distractor imposible (c39: «Nicht jeder sagt man»). La mayoría se resolvió con una pista breve en la consigna (inicial de la palabra, «empieza con…», «mantén el orden»).
3. **Nada sin enseñar:** a este nivel el léxico B2+ de los ítems cabe en outline y niveles previos; no encontré gramática adelantada. `vergleich-praep` (c02, c50): verificada en `n6.c02` («im Vergleich zu / verglichen mit / gegenüber + dativo»); «Im Vergleich zum Vorjahr…» es exactamente esa clave y es correcta. Sin cambios.
4. **Cobertura:** cada clave de `introduce` aparece en la evaluación de su clase; c50 evalúa 8 claves del nivel (≥ 5) en 8 ítems; c49 sin gramática nueva. Huecos menores de `recicla` (ver avisos), no corregidos.
5. **Consignas es/en:** claras; corregidas las que no coincidían con el ítem (c04 `konnotation` pedía «sin adornos» para una partícula «ab»; c09 «dónde estudió» para «Studium»; c09 «participio de geboren»; c33 «cierre» para una apertura; c50 «la jurado»).
6. **Sin Lumo/Ecuador/Quito:** comprobado con grep. Nombres genéricos sin continuidad.

## Cambios (108 ediciones de campo, 44 clases)

- **Situaciones (7):** c01 («denselben Inhalt» era falso), c05 (frase redundante), c35 (dos frases no idiomáticas), c41 y c42 (comillas y coma en el diálogo, 2 líneas cada una).
- **c01–c10:** c03 ×2 (bitte/Kannst du fijo), c04 ×2 (posesivo de «yo»; ítem `konnotation` sustituido), c05 ×3 (Mein…, Es…, «un rechazo»), c06 ×3, c07 ×3, c09 ×4, c10 ×2.
- **c11–c20:** c12 ×2 (Soweit con «weit»), c13 ×3 (würden fijo; relacionar rehecho), c14, c15 ×2, c17 (ordenar rehecho), c18 (distractor), c19 ×2, c20 ×2 (ítem zer- rehecho: «zerschnitt»).
- **c21–c30:** c21 ×2, c22 ×4 (Flut/Lawine/Strom ambiguos), c23, c24, c26 ×6, c27, c28 ×2, c29 ×2, c30 ×2.
- **c31–c40:** c31 ×3 (plural tras sowohl…als auch), c32 ×8, c33 ×3, c34 ×2, c35 ×1 + situación, c36, c37 ×4, c38 ×2, c39 ×2 (ítem «Nicht jeder sagt man» → «Nicht immer»), c40.
- **c41–c50:** c41 (ítem «Wie musste sie das nur erklären?» → «Musste sie wirklich alles erklären?»), c42 ×2, c43 (tiempo del ejemplo = estímulo), c44, c45 (espacio antes de «:»), c47 ×4, c48 ×2 (un ítem reemplazado), c49 ×3, c50 ×4 (ordenar con «jetzt nur» → «nur sagen»).
- Sin cambios: c02, c08, c11, c16, c25, c46.

## Sin resolver

- `recicla` no usado en los ítems (hueco de reciclaje, no bloquea): c47 (`zumal`, `erzaehlperspektive`, `gegenueberstellung`), c43 (`prognose-modal`). Con 5–8 ítems de evaluación no hay sitio para todo; el autor de bloque puede cubrirlo en guiada/independiente.
- c43 incluye «als ob» (introducido aquí) mientras `als-ob` ya figura en `previos`: solapamiento de outline, no se puede arreglar editando ejercicios.
- Varios `escribir` siguen siendo cerrados por consigna (piden empezar por X); la clase real debe enseñar la variante alternativa (p. ej. «doch ist er…» tras «zwar»).
- Los `completar` donde dos sinónimos del outline son válidos (immerhin/zumindest/wenigstens, indessen/inzwischen) dependen de la pista de la consigna; el bloque debe repetir esa pista en la clase.

## Avisos para autores de bloque

Errores frecuentes reales del nivel para `erroresFrecuentes`:

1. «sowohl … als auch» con verbo en singular (*sowohl A als auch B zustimmt) y «sowohl … und».
2. Konjunktiv II pasado concesivo: *«Auch wenn er es wusste, wäre…»; hätte/wäre equivocado con kommen/gehen.
3. «ohne dass» sin Konj. II del pasado (*«ohne dass es jemand bemerkte hat»); «zu …, als dass» con indicativo.
4. «anders … als» / «genauso … wie» confundidos (*«anders, wie»).
5. Zustandspassiv vs. Vorgangspassiv: *«war eingeweiht werden».
6. Atributo participial de «bauen»: *«die bauende Brücke» (Partizip I en vez de II).
7. Genitivo preposicional con dativo: *«zugunsten den Mietern», *«hinsichtlich den Kosten».
8. «ehe/bevor»: «ehe» sin Plusquamperfekt; «indessen» confundido con «inzwischen».
9. Posición de «jedoch»: *«Jedoch wir können…» (como conjunción en posición 0).
10. Konjunktiv I: *«das Gesetz seien unnötig», *«er sagt, dass sie lehne ab».
11. Participio sustantivado: *«die Studierende / die Zugewanderte» (plural sin -n); pronunciación de «Studierende/Mitarbeitende» (ni «Studenten»).
12. Reglas comunes para el bloque: `ordenar` con adverbios móviles (heute, jedoch, nur, jetzt) o «es/er» + «jemand» admite varias órdenes; fijar con «empieza con X» o declarar la variante. Falsos amigos en N7: «Karte» (c25), «Schloss» (c24), «Termin».
