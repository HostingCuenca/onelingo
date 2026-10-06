# Revisión independiente de verbos-es.json

**Veredicto: GO** (122 verbos revisados, 2 añadidos: terminar y vender; 0 quitados; 124 en total).

## Método

Las formas se compararon con un conjugador escrito aparte por el revisor (`conj.py`, tablas y reglas propias): cambios vocálicos (e>ie, o>ue, e>i, u>ue, y las -ir con cambio también en pretérito y subjuntivo de «nosotros»), ortografía (-car/-gar/-zar en pretérito yo y subjuntivo, -ger/-gir y -guir ante a/o), pretéritos fuertes (-j- con «-eron»), verbos con «y» (leer, creer, caer, oír, construir), tildes de futuro/condicional/imperfecto, participios irregulares y reflexivos con pronombre en las seis personas (incluido «me he ido»). Con los 122 verbos originales se comprobaron 5.124 formas (122 × 7 tiempos × 6 personas) más 122 participios, y con los 2 añadidos otras 84. Coincidieron todas. Las 2 únicas discrepancias fueron un fallo del propio conjugador del revisor (futuro y condicional de `oír`; el archivo tiene la forma correcta «oiré», «oiría», sin tilde). Los pretéritos -car/-gar/-zar (busqué, llegué, pagué, empecé, almorcé, jugué, crucé, practiqué, expliqué, saqué) y los subjuntivos (busque, llegue, pague, empiece, cruce, juegue, almuerce, practique, explique, saque) están bien, igual que los reflexivos y los irregulares con tilde (dé, esté, envíe, sé, oí/oíste, caí, leí, traído, oído).

Comprobado también: NFC en todo el archivo, seis personas por tabla, «ustedes» = «ellos» en todas las tablas.

## Recuento

| Tipo | Verbos |
|---|---|
| regular | 54 (incluye terminar y vender) |
| irregular | 70 |
| de ellos, reflexivos | 11 |
| nivel 1 / 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9 (generado) | 60 / 28 / 22 / 4 / 4 / 1 / 1 / 2 / 2 |

`tipo` revisado con el conjugador: ningún verbo `regular` tiene cambio de raíz, ortografía ni participio irregular. Los ortográficos (buscar, llegar, pagar, recoger, cruzar, practicar, explicar, sacar) son `irregular` según LEEME, y lo son.

## Correcciones

| Verbo | Campo | Antes → después |
|---|---|---|
| (todas las tablas) | formas | 0 cambios; no había errores de conjugación |
| caer | ejemplo | «El niño cae en el parque.» / The boy falls in the park. → «Las hojas caen en otoño.» / The leaves fall in autumn. (calco poco natural) |
| nacer | ejemplo | «Mi hermano nace en mayo.» / My brother is born in May. → «Muchos bebés nacen en mayo.» / Many babies are born in May. |
| manejar | ejemplo | «Mi padre maneja al trabajo.» → «Mi padre maneja con mucho cuidado.» / My father drives very carefully. |
| decidir | traducción | I've decided to stay home. (perfecto) → I decide to stay home. |
| dar | traducción | I'll give you my phone number. → I'm giving you my phone number. |
| pedir | traducción | I'll order a chicken soup. → I'm ordering a chicken soup. |
| elegir | traducción | I'll choose the soup of the day. → I choose the soup of the day. |
| terminar, vender | añadidos | verbos frecuentes A1–B2 que faltaban (terminar: «Termino el trabajo a las cinco.»; vender: «Vendemos frutas frescas en el mercado.») |

### Niveles de respaldo ajustados (26 verbos sin vocabulario en la ruta)

El nivel de respaldo se ajustó al primer nivel donde la ruta los usa de verdad (frases de los pasos y diálogos de `assets/contenido/es/ruta`).

| Verbo | Antes → después | Dónde aparece |
|---|---|---|
| ser, estar, gustar, llamarse, haber | 1 → 1 (sin cambio) | f0 y N1 («me llamo», «me gusta», «hay») |
| ver, dar, cenar | 2 → 2 (sin cambio) | «nos vemos» N1, «dar, doy» N2, «cenamos» N2 |
| entrar, creer, encontrar, irse, oír | 3 → 3 (sin cambio) | N3 |
| morir, construir | sin cambio | N4, N5 |
| romper | 3 → 2 | «se rompió el vaso» N2 |
| sentir | 3 → 1 | «lo siento» (vocabulario N1) |
| necesitar | 2 → 3 | primera aparición en N3 |
| parecer | 4 → 3 | «me parece que…» N3 |
| despertarse | 3 → 4 | «me desperté» N4 |
| deber | 4 → 5 | «se debe» N5 |
| caer | 3 → 5 | «se cayó» N5 |
| sentirse | 3 → 5 | «me siento mejor» N5 |
| elegir | 4 → 6 | «elige/eligen» N6 |
| descubrir | 5 → 7 | «descubre» N7 |
| resolver | 4 → 3 | ya lo fijaba el generador (vocabulario N3); fuente sincronizada |

## Sin resolver

- `vestirse` no aparece en ninguna frase ni vocabulario de la ruta; queda con nivel 3 de respaldo (rutina diaria, junto a despertarse/levantarse). Revisar cuando se amplíe la ruta.
- `haber` se conjuga como auxiliar («he, has, ha…»); el ejemplo con «hay» es solo el uso impersonal, y la tabla no muestra «hay». No es un error, pero conviene una nota en la UI.
- Selección: posibles añadidos futuros (dejar, conducir, ofrecer, mostrar, comenzar). No se añadieron para no inflar la lista.

## Comprobación

`python3 tools/contenido/verbos/generar_verbos.py` regeneró `assets/contenido/es/verbos.json` (124 verbos) y `--comprobar` no muestra líneas ERROR («Todo al día»).
