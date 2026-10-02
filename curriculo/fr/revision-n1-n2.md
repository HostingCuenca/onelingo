# Revisión del plan FR · N1 (c21–c50) y N2

Fecha: 2026-10-01 · Revisor de plan (FLE, DELF A1/A2) · Fuentes: `PLAN_CLASES.md`, `marco.json` (N1–N2), `PLAN_PRODUCCION.md` §2, `curriculo/fr/n1.json` y `n2.json`.

GO

Las fichas son precisas y caben en una clase de 10–12 minutos. La progresión es sólida: los pronominales van antes de su passé composé (N1 c30 → N2 c08), el COD antes de los pronombres en passé composé (N2 c11 → c25), el futur proche antes del futur simple (N1 c43 → N2 c17), el imparfait antes del contraste PC/imparfait (N2 c09 → c10) y las contracciones antes de las preposiciones de lugar y del futur proche. Corregí las carencias de cobertura A1/A2 y los regionalismos que encontré. `validar_plan.py fr` da 0 errores y 10 avisos (ver abajo).

## Cambios en N1

| Ficha | Antes | Después |
|---|---|---|
| `personajes` | Ana «de viaje en París», vive en Quito; Chloé «apellido Martin», «receptionist»; Monsieur Martin «profesor de la universidad»; Hugo sin apellido | Ana: ecuatoriana recién llegada a París, estudia francés en la escuela de idiomas, padres en Quito. Hugo: campo `apellido: Durand`. Chloé: `apellido: Bernard`, secretaria de la escuela. Monsieur Martin: profesor de francés de la escuela de idiomas (profesor de Ana), único «Martin» del reparto |
| c22 | partitivo sin negación | + «en negativo, de: je ne prends pas de sucre»; recicla `pas-de` |
| c24 | colores noir, blanc, vert, gris | `gris` → `bleu / bleue` (color más frecuente; ejemplo «un pull bleu») |
| c26 | aimer/préférer + infinitivo | + `et-mais-ou` (et, mais, ou: faltaban los conectores básicos en N1); vocabulario: −chanter, +mais, +ou; tarea con mais y ou |
| c27 | faire du / jouer au sin nota | + aviso: au / du como bloques; la regla de contracción llega en c33–c34 |
| c28 | recicla 20–29 | + `nombres-30-49` (fechas hasta el 31) |
| c31 | solo adjetivos; situación 10 (hotel) | + `possessifs-pluriel` (notre/nos, votre/vos, leur/leurs: c15 solo enseñó mon/ton/son); recicla `possessifs`; situación 43; tarea: describir una familia conocida con nos / leur |
| c32 | posición del adjetivo | + `pluriel-irregulier` (-eau → -eaux, -al → -aux; encaja con el sonido o/au/eau); vocabulario −propre +le château; recicla `pluriel-liaison` |
| c35 | dónde está, cómo es, qué hay | + `meteo-base` (il fait beau / chaud / froid, il pleut, il neige, Quel temps fait-il ?), tema típico del DELF A1; vocabulario −l’habitant −célèbre + 3 expresiones del tiempo; recicla `faire-present` |
| c36 | solo prendre | + `boire-present` (movido desde N2 c26) y avoir faim / avoir soif; título «Prendre y boire: las comidas del día»; vocabulario −apprendre −comprendre −un fruit + boire, avoir faim, avoir soif, le lait |
| c42 | preposiciones de lugar | + `chez` (chez Hugo, chez moi, chez le médecin: faltaba en A1); recicla `pronoms-toniques` |
| c45 | invitar / aceptar / rechazar | + el tiempo como motivo («Il pleut : on va au cinéma ?»); recicla `meteo-base` |
| c46 | fait, pris | + vu como participio frecuente (j’ai vu un film); recicla `prendre-present` |
| c47 | 9 verbos con être (tomber, monter…) + jamais | reducido a los 7 de movimiento (aller, venir, arriver, partir, sortir, rentrer, rester); la lista completa queda en N2 c07; ne… jamais en presente y como frase en pasado; vocabulario con participios (allé, parti, resté) |
| c48 | recicla `nombres-11-20` | recicla `il-y-a` (contraste «hay» / «hace»); nota en la gramática |
| c49 | repaso sin boire | + boire; recicla `boire-present`, `possessifs-pluriel`, `meteo-base` |

## Cambios en N2

| Ficha | Antes | Después |
|---|---|---|
| `nota`, `personajes` | «Ana se muda a París» un año después; «piso»; Chloé Martin | Ana ya vive en París desde N1 y en B3 busca departamento nuevo con Emma (Emma deja el de Léa); Hugo Durand, Chloé Bernard, Monsieur Martin profesor de la escuela; «piso» → «departamento» |
| c02 | un courriel | un e-mail (uso de Francia) |
| c12, c14, c15, c45 | «piso» (España) | «departamento» (español neutro de América) |
| c16 | introduce el tiempo desde cero | repasa `meteo-base` y amplía (il fait mauvais, degrés, il y a du vent / des nuages, estaciones, pronóstico con futur proche) |
| c21 | comparativo | + `donner-son-avis` (je trouve que, je pense que, à mon avis: imprescindible para la producción escrita del DELF A2); + «à mon avis» en vocabulario; c22 lo recicla |
| c25 | pronombres en passé composé | + nota: la concordancia del participio con el COD (je l’ai achetée) solo se reconoce en N2; se trabaja en N3 |
| c26 | introduce `boire-present` | lo recicla (boire pasa a N1 c36); vocabulario boire → commander |
| c31 | «billetes»; composter | «boletos»; composter (en desuso en la SNCF) → le contrôleur / la contrôleuse |
| c37 | avoir + sustantivo | + repaso de avoir faim / avoir soif |

## Claves (para el planificador de N3–N6)

- **Movida:** `boire-present` (N2 c26 → N1 c36).
- **Nuevas en N1:** `et-mais-ou` (c26), `possessifs-pluriel` (c31), `pluriel-irregulier` (c32), `meteo-base` (c35), `chez` (c42).
- **Nueva en N2:** `donner-son-avis` (c21).
- Ninguna otra clave cambió de nombre ni de clase. Cuidado con no volver a introducir estas claves en N3–N6: el validador lo marcaría como error.

## Avisos que quedan (10)

- c03, c04, c11, c13, c14, c16, c17, c18, c20: situación fuera de las del bloque del marco. Son clases ya escritas y revisadas; no se tocan.
- c31: situación 43 (Hablando sobre la familia) fuera del bloque 7 (33, 10). Es intencional: la tarea es describir a una familia conocida, y el hotel (10) no tenía sentido para eso.

## Preguntas abiertas

1. **Contenido escrito c01–c20 (otro agente):** el panadero de c01 se llama «Martin» y en c02 Chloé dice «Mon nom, c’est Martin»; en c19 Martin es profesor de la universidad de Hugo. El reparto canónico pide Chloé Bernard y Monsieur Martin como profesor (en el plan: de la escuela de idiomas). Hay que confirmar si en c19 Hugo sigue en la universidad con otro profesor o si la escena pasa a la escuela.
2. **Partes de la casa y del cuerpo en A1:** el marco N1 no las incluye; llegan al inicio de N2 (c11 casa, c36 cuerpo). Con «malade» (c03) y «il y a» (c17) basta para el DELF A1, pero si el cliente quiere más, una clase de B3 o B8 de N1 podría adelantar las habitaciones.
3. **Estaciones:** quedan en N2 c16 (`saisons`). Muchos manuales las ven en A1; se podrían adelantar a N1 c35 si sobra tiempo en esa clase.
4. **Densidad:** N2 c15 (COI + dire, lire, écrire), c18 (diez raíces del futuro) y c25 (posesivos + pronombres en passé composé) son las fichas más cargadas. Caben en 12 minutos si el autor presenta las raíces o las conjugaciones en tabla y practica solo las formas frecuentes; si el revisor del bloque las ve largas, partir `dire-lire-ecrire` hacia c32 (il dit que…).
5. **Fuera de N2 a propósito (para N3):** subjuntivo (il faut que), ne… que, vivre (j’ai vécu), concordancia del participio con el COD y plus-que-parfait.
