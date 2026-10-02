# Revisión del plan FR · N3–N6 (B1–B2)

Fecha: 2026-10-01 · Revisor de plan (FLE, DELF B1/B2) · Fuentes: `PLAN_CLASES.md`, `PLAN_FRANCES.md` (§2, §3.4, §4), `marco.json` (N3–N6), `curriculo/fr/n1.json`–`n6.json`, `revision-n1-n2.md`.

GO

Después de los cambios de abajo, el plan es sólido. Cada ficha es concreta y cabe en una clase: 1 o 2 puntos nuevos, de 6 a 12 palabras con artículo y una tarea que se puede comprobar. Las progresiones están bien encadenadas:

- **Subjuntivo:** il faut que → irregulares → impersonales → vouloir que → opinión negativa → duda → proposer que (N3); deseo, emoción, exigencia, finalidad y jusqu’à ce que (N4); concesión, pasado y conjunciones de B2 (N5); relativas, juicio y ce n’est pas que (N6).
- **Pasiva:** intro (N3 c21) → agente (N4 c11) → infinitivo pasivo (N4 c18) → completa (N5 c03) → impersonal (N5 c22) → se faire pasivo (N6 c15).
- **Hipótesis:** si + imparfait (N3) → condicional pasado → si + plus-que-parfait → mixtas (N5 c06 → c07 → c08).
- **Gérondif y participio:** gérondif (N3 c24) → participe présent (N4 c16) → participio compuesto (N5 c05) → tout en (N5 c45) → adjetivo verbal (N6 c13).
- **Concordancia del participio:** con COD antepuesto (N3 c02) → recíprocos (N3 c12) → fait invariable (N3 c33) → avanzada (N6 c40).
- **Conectores:** de causa, oposición y adición (N3); texto de opinión DELF B1 (N4 B10); concesión y articuladores (N5); ensayo dialéctico DELF B2 (N6 c48).
- **Registro:** N4 B6 → tacto y atenuación en N6 B4.

`validar_plan.py fr` da **0 errores y 10 avisos**: son los de N1 que ya estaban, ninguno de N3–N6.

## Cobertura: lo que corregí

N4 tenía que cerrar el B1 (DELF B1) y le faltaban tres puntos que `PLAN_FRANCES.md` §4 asigna a N4 y que el B1 exige. Los adelanté desde N5 conservando la clave:

1. **Discurso indirecto en pasado (concordancia de tiempos).** Ningún nivel B1 lo tenía: N3 B8 y N4 solo transmitían en presente. El marco N4 B10 pide «mensajes transmitidos» para resolver el caso real.
2. **pour que / afin que + subjuntivo.** Es finalidad básica en la producción escrita del B1; hasta ahora N3–N4 solo tenían pour / afin de + infinitivo.
3. **Relativos preposición + lequel.** La progresión pasa a ser: dont (N3) → ce dont y preposición + qui / lequel (N4) → auquel / duquel y dont frente a duquel (N5) → ce à quoi (N6).

Lo que se deja como está, porque lo fija `PLAN_FRANCES.md`:

- Condicional pasado y si + plus-que-parfait en N5 (§3.4 y §4).
- Passé simple en N8 (comprensión).
- avoir beau en N9.

## Cambios

### N3

| Ficha | Antes | Después |
|---|---|---|
| `nota` | «comparte piso con Emma» | «comparte departamento con Emma» |
| c02 | título es «Las fotos que he hecho» | «Las fotos que tomé» (español de América) |
| c12 | tarea es «cómo os conocisteis y si os peleáis o os lleváis bien» | «cómo se conocieron y si se pelean o se llevan bien» |
| c14 | objetivo es «en qué sois distintos» | «en qué son distintos» |
| c22 | ejemplo de «sin inversión»: «où est ma place ?» (que sí lleva inversión estilística) | «pourriez-vous me dire quand nous allons atterrir ? (no: quand allons-nous…)» |
| c25 | en: cancelled | canceled (inglés de EE. UU.) |
| c33 | es: «tu coche» | «tu auto» |
| c40 | «compañera de piso» / flatmate | «compañera de departamento» / roommate |
| c42 | en: film | movie |

### N4

| Ficha | Antes | Después |
|---|---|---|
| `nota` | Ana «se muda a otro piso» y Madame Dubois «sigue siendo la vecina» (contradictorio: en N2 es la propietaria que vive abajo); Hugo «termina sus estudios» (choca con N6); las conjunciones con subjuntivo, para N5 | En B3 Ana y Emma alquilan un departamento más grande en el mismo barrio; Madame Dubois, antigua propietaria, vive cerca y aconseja a Ana. Hugo termina la licenciatura y empieza un máster. Se explica qué completa el B1 y qué queda para N5 |
| c05 | solo preposición + qui | + `relatifs-composes` (preposición + lequel / laquelle… con preposiciones que no se contraen; auquel y duquel en N5). Título, objetivo (persona **y lugar**), vocabulario (+ la maison d’enfance), tarea con 2 + 2 relativos. «lo que vivisteis» → «lo que viviste» |
| c10 | «peut-être + verbo» (ambiguo) | «il est peut-être malade: peut-être después del verbo» |
| c12 | compañeros de piso / flatmates | compañeros de departamento / roommates |
| c25 | campo en «CV» | «Résumé» |
| c37 | «alquilar un coche» | «alquilar un auto» |
| c40 | campo en «Petrol station…» | «Gas station…» |
| c43 | exiger que + il faudrait que + demander à + inf. | introduce `exiger-que` y `pour-que-afin-que` (finalidad con otro sujeto frente a pour / afin de + inf.); il faudrait que, como repaso; tarea: 2 exigencias y 2 finalidades; «ayuntamiento» → «alcaldía» |
| c45 | relativos del relato: …preposición + qui | …preposición + qui / lequel |
| c46 | resumir un artículo (`verbes-du-resume`) | **«Le témoin a affirmé que…»**: introduce `concordance-des-temps` (présent → imparfait, passé composé → plus-que-parfait, futur → conditionnel; pronombres y marcas de tiempo); vocabulario de testimonios; tarea: transmitir 4 testimonios de un accidente en 6 frases |
| c47 | solo `structure-texte-opinion` | + `verbes-du-resume` (movida desde c46): resumir y luego organizar la opinión; tarea: resumen de 60 palabras más el plan y el primer párrafo; «el coche» → «el auto» |
| c49 | recicla sin discurso indirecto en pasado | + `concordance-des-temps`, `pour-que-afin-que`, `relatifs-composes` |
| c50 | «testimonios en estilo indirecto» | «…en pasado (concordancia de tiempos)»; recicla `concordance-des-temps` |

### N5

| Ficha | Antes | Después |
|---|---|---|
| `nota` | enumera la concordancia de tiempos como contenido nuevo de N5 | cita PLAN_FRANCES §2 para la duración; aclara que la concordancia, pour que y preposición + lequel se vieron en N4 |
| c11 | introduce `relatifs-composes` (todo el sistema lequel) | introduce **`auquel-duquel`**: auquel / auxquelles, duquel después de una locución (près duquel, au cours duquel), dont frente a duquel; recicla `relatifs-composes` |
| c15 | en: cancelled | canceled |
| c21 | introduce `pour-que-afin-que` | introduce **`finalite-formelle`**: en vue de, de façon à / de manière à + inf., con repaso de pour que / afin que; título «En vue de guérir» |
| c26 | introduce `concordance-des-temps` | introduce **`incise-citation`**: cita con inciso e inversión (« … », a-t-il annoncé), paso completo del directo al indirecto (ici → là, aujourd’hui → ce jour-là…), repaso de la concordancia; vocabulario sin duplicados |
| c27 | futur → conditionnel como punto nuevo | repaso de futur → conditionnel (N4); lo nuevo es futur antérieur → conditionnel passé, la semaine suivante y le surlendemain; recicla + `futur-anterieur-intro` |
| c36 | en: rubbish | trash |
| c48 | lista de control: «concordancias» | «concordancias (también la del participio)» |
| c49 | recicla `relatifs-composes` | + `auquel-duquel` |

### N6

| Ficha | Antes | Después |
|---|---|---|
| `nota` | «Hugo presenta su trabajo de fin de estudios» (en N4 ya terminó) | «Hugo, que cursa un máster, presenta su mémoire» (coincide con el vocabulario de c40: le mémoire, le master) |
| c07 | «alquiler de coche» | «alquiler de auto» |
| c20 | «peut-être pourriez-vous… (inversión tras peut-être)», antes de introducirla en c22 | «vous pourriez peut-être…» (la inversión llega en c22) |
| c24 | en: adverts | ads |
| c27 | «il faut que + subjuntivo pasado: il faut que ce soit fini» (no es subjuntivo pasado) | «il faut que vous ayez terminé avant lundi» |

## Claves (para el planificador de N7–N10)

**Ninguna clave cambió de nombre.** Todas siguen introducidas antes de N7.

- **Movidas:**
  - `concordance-des-temps`: N5 c26 → N4 c46.
  - `pour-que-afin-que`: N5 c21 → N4 c43.
  - `relatifs-composes`: N5 c11 → N4 c05.
  - `verbes-du-resume`: N4 c46 → N4 c47.
- **Nuevas:**
  - `auquel-duquel` (N5 c11).
  - `finalite-formelle` (N5 c21).
  - `incise-citation` (N5 c26).

  Que N7–N10 no vuelva a introducirlas.

## Preguntas abiertas

1. **Duración.** `PLAN_FRANCES.md` §2 fija clases de 15–20 min desde N5, con textos de 400–700 palabras. El encargo de esta revisión habla de unos 12–15 min. Las fichas de N5–N6 caben en 15–20 min. Si el objetivo es 12–15, en las tareas largas (N5 c15, c38, c46; N6 c05, c48) el texto de lectura debería quedarse en 300–400 palabras.
2. **Condicional pasado en B1.** Muchos manuales de B1 enseñan j’aurais dû / si j’avais su, y el marco N4 B2 pide «imaginar otros resultados». Se mantiene en N5 por `PLAN_FRANCES.md` §3.4 y §4. Si se quiere que N4 cubra el DELF B1 «de manual», habría que moverlo a N4 B2 junto con si + plus-que-parfait. Son dos claves y obligaría a rehacer N5 c06–c07.
3. **bien que.** `PLAN_FRANCES.md` §4 lo pone en N4, pero el plan lo deja en N5 c04, que es lo habitual en el B2. Recomiendo actualizar `PLAN_FRANCES.md` §4 en lugar de mover la clave.
4. **Passé simple.** Los textos del DELF B2 (prensa, relato) pueden traerlo. `PLAN_FRANCES.md` lo deja para N8. Si el revisor de la prueba de B2 lo echa en falta, una línea de reconocimiento en N6 c03 (à peine… que) sería el lugar natural, siempre que el planificador de N8 no introduzca la clave `passe-simple` dos veces.
5. **Densidad.** Las fichas más cargadas, que caben si se presentan en tabla y se practican solo las formas frecuentes:
   - N3 c27: siete subjuntivos irregulares y las dos raíces.
   - N4 c05: preposición + qui y + lequel.
   - N4 c46: tres transformaciones de tiempo.
   - N5 c26: inciso y cambios de deixis.
6. **Concordancia en pasado tarde en N4.** Entra en c46, tres clases antes de la prueba. Es coherente con el marco (B10: «mensajes transmitidos»), pero el bloque 10 deja de ser solo de integración. La alternativa sería N4 B4 (reclamaciones: «on m’avait assuré que je serais remboursé»), sacrificando `mettre-temps-pour`.
7. **Reparto.** Las fichas de N3–N6 casi no nombran personajes (solo N3 c40, Madame Dubois). Los autores deben tomar el hilo de las notas: Ana en el hotel → coordinadora; Emma, compañera de departamento; Hugo en máster; Karim emprende; Sophie, médica; Madame Dubois. Conviene que el encargo de cada nivel lo recuerde.
8. **Vista legible.** No regeneré `docs/claude-educacion/plan/fr.md`: el encargo limitaba las ediciones a `n3`–`n6` y a esta revisión. Hay que ejecutar `python3 tools/curriculo/ver_plan.py fr` antes de pasar las fichas a los autores.
