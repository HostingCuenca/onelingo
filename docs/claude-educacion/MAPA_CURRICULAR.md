# Mapa curricular — índice maestro de unidades

Generado con `python3 tools/generar_mapa_curricular.py` desde `assets/contenido/<idioma>/ruta/`. PROBADO = pasa `tools/validar_ruta.py` y `test/ruta_contenido_test.dart`; «inicial» = sin revisión nativa.
Enseña / Practica / Evalúa = pasos de enseñanza / ítems de práctica (guiada + independiente + situación) / ítems de evaluación.

Escala interna (DEC-002): 0 = Fundamentos (Pre-A1) · 1–2 A1 · 3–4 A2 · 5–6 B1 · 7–8 B2 · 9–10 C1 · C2 planificado. Plan de A1 de inglés: [PLAN_A1_INGLES.md](PLAN_A1_INGLES.md).

## Inglés (`en`) · apoyo `es` · revisión revisada

### Fundamentos: tus primeras frases · nivel `f0` · [f0.json](../../assets/contenido/en/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `en.f0.primer-contacto` | 0 | Pre-A1 | Primer contacto | — | PROBADO | 3 | 6 | 5 |
| `en.f0.alfabeto` | 0 | Pre-A1 | El alfabeto | primer-contacto | PROBADO | 3 | 6 | 5 |
| `en.f0.pronombres` | 0 | Pre-A1 | Pronombres personales | alfabeto | PROBADO | 3 | 8 | 5 |
| `en.f0.be-afirmativo` | 0 | Pre-A1 | El verbo «to be»: am, is, are | pronombres | PROBADO | 5 | 9 | 5 |
| `en.f0.be-negativo` | 0 | Pre-A1 | Negar con «to be» | be-afirmativo | PROBADO | 3 | 6 | 5 |
| `en.f0.be-preguntas` | 0 | Pre-A1 | Preguntas con «to be» | be-negativo | PROBADO | 3 | 6 | 5 |
| `en.f0.presentarse` | 0 | Pre-A1 | Presentarte | be-preguntas | PROBADO | 3 | 7 | 5 |

### Personas, cosas y lugares · nivel `a1-1` · [a1-1.json](../../assets/contenido/en/ruta/a1-1.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `en.a1.posesivos` | 1 | A1 | Mi, tu, su: los posesivos | presentarse | PROBADO | 4 | 9 | 6 |
| `en.a1.articulo-a-an` | 1 | A1 | A y an: profesiones y objetos | presentarse | PROBADO | 4 | 9 | 6 |
| `en.a1.plurales` | 1 | A1 | Una manzana, dos manzanas: el plural | articulo-a-an | PROBADO | 4 | 9 | 6 |
| `en.a1.articulo-the` | 1 | A1 | The: el, la, los, las | plurales | PROBADO | 4 | 9 | 6 |
| `en.a1.adjetivos` | 1 | A1 | Colores y tamaños: el adjetivo va antes | articulo-a-an | PROBADO | 4 | 9 | 6 |
| `en.a1.demostrativos` | 1 | A1 | This, that, these, those | plurales | PROBADO | 4 | 9 | 6 |
| `en.a1.genitivo-s` | 1 | A1 | Ana's book: el posesivo con 's | posesivos | PROBADO | 4 | 9 | 6 |
| `en.a1.have-got` | 1 | A1 | Have got: tener | genitivo-s | PROBADO | 4 | 9 | 6 |
| `en.a1.there-is-are` | 1 | A1 | There is, there are: hay | articulo-the | PROBADO | 4 | 9 | 6 |
| `en.a1.preposiciones-lugar` | 1 | A1 | In, on, under, next to, between | there-is-are | PROBADO | 4 | 9 | 6 |
| `en.a1.imperativos` | 1 | A1 | Sit down, please: instrucciones | preposiciones-lugar | PROBADO | 4 | 9 | 6 |
| `en.a1.integracion-a1-1` | 1 | A1 | Integración: tu casa y tu familia | adjetivos, demostrativos, have-got, imperativos | PROBADO | 4 | 10 | 8 |

### El presente simple · nivel `a1-2` · [a1-2-presente.json](../../assets/contenido/en/ruta/a1-2-presente.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `en.a1.presente-simple` | 2 | A1 | Tu rutina: el presente simple | integracion-a1-1 | PROBADO | 4 | 9 | 6 |
| `en.a1.presente-3s` | 2 | A1 | He, she, it: la -s del presente | presente-simple | PROBADO | 4 | 9 | 6 |
| `en.a1.dont-doesnt` | 2 | A1 | Negar: don't y doesn't | presente-3s | PROBADO | 5 | 9 | 6 |
| `en.a1.do-preguntas` | 2 | A1 | Preguntar: Do…? y Does…? | dont-doesnt | PROBADO | 5 | 10 | 6 |
| `en.a1.wh-do` | 2 | A1 | Preguntas con What, Where, When y Who | do-preguntas | PROBADO | 5 | 9 | 7 |
| `en.a1.frecuencia` | 2 | A1 | ¿Con qué frecuencia? always, usually, never | presente-3s | PROBADO | 4 | 9 | 6 |
| `en.a1.preposiciones-tiempo` | 2 | A1 | At, on, in: cuándo haces las cosas | presente-simple | PROBADO | 4 | 9 | 7 |
| `en.a1.integracion-rutina` | 2 | A1 | Integración: tu rutina y la de otra persona | wh-do, frecuencia, preposiciones-tiempo | PROBADO | 3 | 8 | 8 |

### Comunicarte en el día a día · nivel `a1-2` · [a1-2-comunicar.json](../../assets/contenido/en/ruta/a1-2-comunicar.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `en.a1.can` | 2 | A1 | Can: lo que sabes y puedes hacer | do-preguntas | PROBADO | 4 | 9 | 6 |
| `en.a1.like-ing` | 2 | A1 | Like, love y hate: tus gustos | presente-3s | PROBADO | 4 | 9 | 6 |
| `en.a1.pronombres-objeto` | 2 | A1 | Me, him, her, us, them | presente-simple | PROBADO | 4 | 9 | 6 |
| `en.a1.posesivos-pronombre` | 2 | A1 | Mine, yours…: ¿de quién es? | pronombres-objeto, posesivos | PROBADO | 4 | 9 | 6 |
| `en.a1.some-any` | 2 | A1 | Some, any, how many, how much | there-is-are, do-preguntas | PROBADO | 4 | 9 | 6 |
| `en.a1.pedir-cortes` | 2 | A1 | Pedir con cortesía en un restaurante | some-any, can | PROBADO | 4 | 9 | 6 |
| `en.a1.presente-continuo` | 2 | A1 | Presente continuo: lo que pasa ahora | presente-3s, be-preguntas | PROBADO | 4 | 9 | 6 |
| `en.a1.conectores` | 2 | A1 | And, but, or, because, so | presente-simple | PROBADO | 4 | 9 | 6 |
| `en.a1.integracion-a1` | 2 | A1 | Integración A1: conocer a alguien y quedar | pedir-cortes, presente-continuo, conectores, integracion-rutina, like-ing, posesivos-pronombre | PROBADO | 3 | 9 | 9 |

## Español (`es`) · apoyo `en` · revisión inicial

### Foundations: sounds, spelling and first phrases · nivel `f0` · [f0.json](../../assets/contenido/es/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `es.f0.sonidos-saludos` | 0 | Pre-A1 | Vowels, stress and greetings | — | PROBADO (inicial) | 5 | 11 | 6 |
| `es.f0.alfabeto` | 0 | Pre-A1 | The alphabet and spelling | sonidos-saludos | PROBADO (inicial) | 4 | 11 | 6 |
| `es.f0.consonantes` | 0 | Pre-A1 | Tricky consonants | alfabeto | PROBADO (inicial) | 5 | 11 | 6 |
| `es.f0.yo-tu-usted` | 0 | Pre-A1 | Yo, tú, usted: pronouns and politeness | consonantes | PROBADO (inicial) | 5 | 9 | 6 |
| `es.f0.ser` | 0 | Pre-A1 | Ser: who you are and where you're from | yo-tu-usted | PROBADO (inicial) | 5 | 10 | 5 |
| `es.f0.estar` | 0 | Pre-A1 | Estar: how and where you are | ser | PROBADO (inicial) | 4 | 11 | 6 |
| `es.f0.negacion-preguntas` | 0 | Pre-A1 | No, ¿…? and ¡…! | estar | PROBADO (inicial) | 5 | 10 | 6 |
| `es.f0.presentarse` | 0 | Pre-A1 | Introducing yourself | negacion-preguntas | PROBADO (inicial) | 4 | 9 | 5 |

### First sentences · nivel `a1-1` · [a1-1.json](../../assets/contenido/es/ruta/a1-1.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `es.a1.pronombres` | 1 | A1 | Pronouns: who's who | presentarse | PROBADO (inicial) | 5 | 11 | 6 |
| `es.a1.ser` | 1 | A1 | Ser: identity, nationality and personality | pronombres | PROBADO (inicial) | 4 | 11 | 6 |
| `es.a1.genero-articulos` | 1 | A1 | Gender and articles: el, la, un, una | ser | PROBADO (inicial) | 4 | 11 | 6 |
| `es.a1.plural-concordancia` | 1 | A1 | Plurals and agreement | genero-articulos | PROBADO (inicial) | 4 | 11 | 6 |
| `es.a1.estar` | 1 | A1 | Estar: feelings, places, and ser or estar | plural-concordancia | PROBADO (inicial) | 4 | 11 | 6 |
| `es.a1.tener-numeros` | 1 | A1 | Tener, numbers 0–100 and age | estar | PROBADO (inicial) | 4 | 12 | 6 |
| `es.a1.verbos-regulares` | 1 | A1 | Regular verbs: -ar, -er, -ir | tener-numeros | PROBADO (inicial) | 4 | 12 | 6 |
| `es.a1.preguntas-negacion` | 1 | A1 | Questions and negatives | verbos-regulares | PROBADO (inicial) | 4 | 12 | 6 |
| `es.a1.presentacion` | 1 | A1 | Introduce yourself: the full version | preguntas-negacion, tener-numeros, verbos-regulares | PROBADO (inicial) | 3 | 10 | 8 |

## Francés (`fr`) · apoyo `es` · revisión inicial

### Fundamentos: tus primeras frases · nivel `f0` · [f0.json](../../assets/contenido/fr/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `fr.f0.premier-contact` | 0 | Pre-A1 | Primer contacto | — | PROBADO (inicial) | 4 | 9 | 6 |
| `fr.f0.alphabet` | 0 | Pre-A1 | El alfabeto y los acentos | premier-contact | PROBADO (inicial) | 5 | 11 | 6 |
| `fr.f0.voyelles` | 0 | Pre-A1 | Las vocales: u, ou, eu, oi… | alphabet | PROBADO (inicial) | 5 | 11 | 6 |
| `fr.f0.sons` | 0 | Pre-A1 | Nasales, r y letras finales | voyelles | PROBADO (inicial) | 5 | 10 | 6 |
| `fr.f0.pronoms` | 0 | Pre-A1 | ¿Tu o vous? Saludar según la persona | sons | PROBADO (inicial) | 4 | 9 | 6 |
| `fr.f0.etre` | 0 | Pre-A1 | C'est… : señalar y presentar | pronoms | PROBADO (inicial) | 5 | 9 | 6 |
| `fr.f0.negation-questions` | 0 | Pre-A1 | Frases para sobrevivir | etre | PROBADO (inicial) | 5 | 9 | 6 |
| `fr.f0.se-presenter` | 0 | Pre-A1 | Presentarte | negation-questions | PROBADO (inicial) | 3 | 9 | 6 |

### Primeras frases · nivel `a1-1` · [a1-1.json](../../assets/contenido/fr/ruta/a1-1.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `fr.a1.pronoms-sujet` | 1 | A1 | Los pronombres: je, tu, il, elle, on… | se-presenter | PROBADO (inicial) | 5 | 11 | 6 |
| `fr.a1.etre` | 1 | A1 | Être: ser y estar | pronoms-sujet | PROBADO (inicial) | 5 | 11 | 6 |
| `fr.a1.genre-articles` | 1 | A1 | Género y artículos: un, une, le, la, les | etre | PROBADO (inicial) | 5 | 11 | 6 |
| `fr.a1.accord-adjectif` | 1 | A1 | Concordancia: petit, petite, petits | genre-articles | PROBADO (inicial) | 5 | 11 | 6 |
| `fr.a1.verbes-er` | 1 | A1 | Verbos en -er: parler, habiter, aimer… | accord-adjectif | PROBADO (inicial) | 6 | 11 | 6 |
| `fr.a1.negation-questions` | 1 | A1 | Negar y preguntar | verbes-er | PROBADO (inicial) | 5 | 11 | 6 |
| `fr.a1.nombres` | 1 | A1 | Los números del 0 al 100 | negation-questions | PROBADO (inicial) | 5 | 11 | 6 |
| `fr.a1.avoir-age` | 1 | A1 | Avoir: tener y la edad | nombres | PROBADO (inicial) | 6 | 11 | 6 |
| `fr.a1.se-presenter` | 1 | A1 | Me presento: todo junto | avoir-age | PROBADO (inicial) | 4 | 10 | 8 |

## Alemán (`de`) · apoyo `es` · revisión inicial

### Fundamentos: tus primeras frases en alemán · nivel `f0` · [f0.json](../../assets/contenido/de/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `de.f0.laute-gruesse` | 0 | Pre-A1 | Sonidos y saludos | — | PROBADO (inicial) | 4 | 8 | 6 |
| `de.f0.alphabet` | 0 | Pre-A1 | El alfabeto y el deletreo | laute-gruesse | PROBADO (inicial) | 4 | 11 | 7 |
| `de.f0.vokale-konsonanten` | 0 | Pre-A1 | Vocales, Umlaute y consonantes | alphabet | PROBADO (inicial) | 6 | 11 | 7 |
| `de.f0.pronomen-du-sie` | 0 | Pre-A1 | Pronombres: ¿du o Sie? | vokale-konsonanten | PROBADO (inicial) | 4 | 10 | 6 |
| `de.f0.sein-heissen` | 0 | Pre-A1 | sein, heißen y kommen aus | pronomen-du-sie | PROBADO (inicial) | 5 | 11 | 5 |
| `de.f0.der-die-das` | 0 | Pre-A1 | der, die, das: el género | sein-heissen | PROBADO (inicial) | 5 | 10 | 6 |
| `de.f0.nicht-kein-fragen` | 0 | Pre-A1 | Negar y preguntar | der-die-das | PROBADO (inicial) | 5 | 11 | 6 |
| `de.f0.vorstellen` | 0 | Pre-A1 | Presentarte | nicht-kein-fragen | PROBADO (inicial) | 3 | 9 | 5 |

### Primeras frases · nivel `a1-1` · [a1-1.json](../../assets/contenido/de/ruta/a1-1.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `de.a1.pronomen-sein` | 1 | A1 | Todos los pronombres con sein | vorstellen | PROBADO (inicial) | 4 | 11 | 6 |
| `de.a1.verben-praesens` | 1 | A1 | Verbos regulares en presente | pronomen-sein | PROBADO (inicial) | 4 | 11 | 7 |
| `de.a1.zahlen-alter` | 1 | A1 | Números del 0 al 100 y la edad | verben-praesens | PROBADO (inicial) | 4 | 11 | 7 |
| `de.a1.haben` | 1 | A1 | haben: tener | zahlen-alter | PROBADO (inicial) | 4 | 11 | 7 |
| `de.a1.artikel-akkusativ` | 1 | A1 | Artículos en nominativo y acusativo | haben | PROBADO (inicial) | 4 | 11 | 7 |
| `de.a1.vokalwechsel` | 1 | A1 | Verbos que cambian la vocal | artikel-akkusativ | PROBADO (inicial) | 4 | 11 | 7 |
| `de.a1.w-fragen-v2` | 1 | A1 | Preguntas W y el verbo en posición 2 | vokalwechsel | PROBADO (inicial) | 4 | 11 | 7 |
| `de.a1.negation` | 1 | A1 | Negar con nicht y kein | w-fragen-v2 | PROBADO (inicial) | 4 | 11 | 7 |
| `de.a1.vorstellen-integration` | 1 | A1 | Me presento: integración A1 | negation | PROBADO (inicial) | 3 | 10 | 8 |

## Portugués (BR) (`pt`) · apoyo `es` · revisión inicial

### Fundamentos: tus primeras frases (portugués de Brasil) · nivel `f0` · [f0.json](../../assets/contenido/pt/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `pt.f0.primeiro-contato` | 0 | Pre-A1 | Primer contacto | — | PROBADO (inicial) | 4 | 8 | 6 |
| `pt.f0.alfabeto` | 0 | Pre-A1 | El alfabeto y las tildes | primeiro-contato | PROBADO (inicial) | 5 | 11 | 6 |
| `pt.f0.sons` | 0 | Pre-A1 | Vocales: abiertas, cerradas y nasales | alfabeto | PROBADO (inicial) | 7 | 11 | 6 |
| `pt.f0.consoantes` | 0 | Pre-A1 | Consonantes: lh, nh, ç, r, s, t y d | sons | PROBADO (inicial) | 4 | 11 | 6 |
| `pt.f0.pronomes` | 0 | Pre-A1 | Pronombres: eu, você, a gente | consoantes | PROBADO (inicial) | 5 | 9 | 6 |
| `pt.f0.ser-estar` | 0 | Pre-A1 | Ser y estar | pronomes | PROBADO (inicial) | 5 | 10 | 6 |
| `pt.f0.negacao-perguntas` | 0 | Pre-A1 | Negar y preguntar | ser-estar | PROBADO (inicial) | 5 | 9 | 6 |
| `pt.f0.apresentar-se` | 0 | Pre-A1 | Presentarte y falsos amigos | negacao-perguntas | PROBADO (inicial) | 5 | 9 | 7 |

### Primeras frases · nivel `a1-1` · [a1-1.json](../../assets/contenido/pt/ruta/a1-1.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `pt.a1.pronomes` | 1 | A1 | Pronombres y concordancia | apresentar-se | PROBADO (inicial) | 6 | 11 | 6 |
| `pt.a1.ser-estar` | 1 | A1 | Ser y estar: la tabla completa | pronomes | PROBADO (inicial) | 4 | 11 | 6 |
| `pt.a1.artigos-genero` | 1 | A1 | Artículos, género y plural | ser-estar | PROBADO (inicial) | 5 | 11 | 6 |
| `pt.a1.contracoes` | 1 | A1 | Contracciones: no, na, do, da, num, numa | artigos-genero | PROBADO (inicial) | 4 | 11 | 6 |
| `pt.a1.ter` | 1 | A1 | Ter: tener, la familia y «hay» | contracoes | PROBADO (inicial) | 4 | 11 | 6 |
| `pt.a1.verbos-regulares` | 1 | A1 | Verbos regulares: -ar, -er, -ir | ter | PROBADO (inicial) | 4 | 11 | 6 |
| `pt.a1.numeros-idade` | 1 | A1 | Números del 0 al 100 y la edad | verbos-regulares | PROBADO (inicial) | 5 | 11 | 6 |
| `pt.a1.negacao-perguntas` | 1 | A1 | Negar y preguntar con todos los verbos | numeros-idade | PROBADO (inicial) | 4 | 11 | 6 |
| `pt.a1.apresentacao` | 1 | A1 | Presentación completa (integración) | negacao-perguntas, numeros-idade, verbos-regulares | PROBADO (inicial) | 4 | 9 | 8 |

## Italiano (`it`) · apoyo `es` · revisión inicial

### Fundamentos: tus primeras frases · nivel `f0` · [f0.json](../../assets/contenido/it/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `it.f0.primo-contatto` | 0 | Pre-A1 | Primer contacto | — | PROBADO (inicial) | 4 | 8 | 6 |
| `it.f0.alfabeto` | 0 | Pre-A1 | El alfabeto y el deletreo | primo-contatto | PROBADO (inicial) | 4 | 11 | 6 |
| `it.f0.suoni` | 0 | Pre-A1 | C, g, gli, gn y sc | alfabeto | PROBADO (inicial) | 4 | 11 | 6 |
| `it.f0.doppie-vocali` | 0 | Pre-A1 | Dobles, z, vocales y acentos | suoni | PROBADO (inicial) | 5 | 11 | 6 |
| `it.f0.pronomi` | 0 | Pre-A1 | Pronombres: tu y Lei | doppie-vocali | PROBADO (inicial) | 5 | 9 | 6 |
| `it.f0.essere-stare` | 0 | Pre-A1 | Essere y stare | pronomi | PROBADO (inicial) | 5 | 10 | 6 |
| `it.f0.negazione-domande` | 0 | Pre-A1 | Negar y preguntar | essere-stare | PROBADO (inicial) | 5 | 9 | 6 |
| `it.f0.presentarsi` | 0 | Pre-A1 | Presentarte | negazione-domande | PROBADO (inicial) | 3 | 9 | 6 |

### Primeras frases · nivel `a1-1` · [a1-1.json](../../assets/contenido/it/ruta/a1-1.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `it.a1.pronomi-essere` | 1 | A1 | Pronombres y essere: todas las personas | presentarsi | PROBADO (inicial) | 4 | 11 | 6 |
| `it.a1.articoli-indeterminativi` | 1 | A1 | Género y un, uno, una, un' | pronomi-essere | PROBADO (inicial) | 4 | 11 | 6 |
| `it.a1.articoli-plurale` | 1 | A1 | El artículo il, lo, la y el plural | articoli-indeterminativi | PROBADO (inicial) | 4 | 11 | 6 |
| `it.a1.avere` | 1 | A1 | Avere: tener | articoli-plurale | PROBADO (inicial) | 4 | 11 | 6 |
| `it.a1.verbi-are` | 1 | A1 | Verbos en -are: parlare, abitare | avere | PROBADO (inicial) | 4 | 11 | 6 |
| `it.a1.verbi-ere-ire` | 1 | A1 | Verbos en -ere e -ire | verbi-are | PROBADO (inicial) | 4 | 11 | 6 |
| `it.a1.numeri-eta` | 1 | A1 | Números del 0 al 100 y la edad | verbi-ere-ire | PROBADO (inicial) | 5 | 11 | 6 |
| `it.a1.negazione-domande` | 1 | A1 | No y preguntas: chi, che cosa, dove, come, quanti | numeri-eta | PROBADO (inicial) | 5 | 11 | 6 |
| `it.a1.presentazione` | 1 | A1 | Presentación completa | negazione-domande | PROBADO (inicial) | 4 | 10 | 8 |

## Chino mandarín (`zh`) · apoyo `es` · revisión inicial

### Fundamentos: tonos, caracteres y primeras frases · nivel `f0` · [f0.json](../../assets/contenido/zh/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `zh.f0.tonos-saludos` | 0 | Pre-A1 | Tonos y saludos | — | PROBADO (inicial) | 5 | 9 | 5 |
| `zh.f0.pinyin` | 0 | Pre-A1 | Iniciales (1): b p m f · d t n l | tonos-saludos | PROBADO (inicial) | 3 | 10 | 6 |
| `zh.f0.iniciales-gkh-jqx` | 0 | Pre-A1 | Iniciales (2): g k h · j q x | pinyin | PROBADO (inicial) | 4 | 10 | 6 |
| `zh.f0.iniciales-zh-z` | 0 | Pre-A1 | Iniciales (3): zh ch sh r · z c s | iniciales-gkh-jqx | PROBADO (inicial) | 4 | 10 | 6 |
| `zh.f0.finales-simples` | 0 | Pre-A1 | Finales (1): a o e i u ü · ai ei ao ou | iniciales-zh-z | PROBADO (inicial) | 4 | 10 | 6 |
| `zh.f0.finales-nasales` | 0 | Pre-A1 | Finales (2): an en ang eng ong · in ing | finales-simples | PROBADO (inicial) | 3 | 10 | 6 |
| `zh.f0.finales-compuestas` | 0 | Pre-A1 | Finales (3): con i-, u- y ü- | finales-nasales | PROBADO (inicial) | 4 | 10 | 6 |
| `zh.f0.cambios-tono` | 0 | Pre-A1 | Cambios de tono: 3 + 3, 不 y 一 | finales-compuestas | PROBADO (inicial) | 4 | 10 | 6 |
| `zh.f0.caracteres` | 0 | Pre-A1 | Tus primeros caracteres | cambios-tono | PROBADO (inicial) | 5 | 10 | 6 |
| `zh.f0.radicales` | 0 | Pre-A1 | Radicales: las piezas de los caracteres | caracteres | PROBADO (inicial) | 4 | 10 | 6 |
| `zh.f0.pronombres` | 0 | Pre-A1 | Yo, tú, él, ella | radicales | PROBADO (inicial) | 7 | 8 | 5 |
| `zh.f0.shi-bushi-ma` | 0 | Pre-A1 | Soy estudiante: 是, 不 是 y 吗 | pronombres | PROBADO (inicial) | 6 | 9 | 5 |
| `zh.f0.presentarse` | 0 | Pre-A1 | Preséntate | shi-bushi-ma | PROBADO (inicial) | 6 | 9 | 5 |

### Primeras frases · nivel `a1-1` · [a1-1.json](../../assets/contenido/zh/ruta/a1-1.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `zh.a1.pronombres` | 1 | A1 | Todos los pronombres y 的 | presentarse | PROBADO (inicial) | 5 | 10 | 6 |
| `zh.a1.ser-adjetivos` | 1 | A1 | 是 o 很: decir qué es y cómo es | pronombres | PROBADO (inicial) | 4 | 10 | 7 |
| `zh.a1.tener` | 1 | A1 | 有 y 没有: tener y haber | ser-adjetivos | PROBADO (inicial) | 4 | 10 | 6 |
| `zh.a1.verbos` | 1 | A1 | Verbos básicos: 吃, 喝, 去, 来, 看, 学习, 住 | tener | PROBADO (inicial) | 4 | 10 | 7 |
| `zh.a1.numeros` | 1 | A1 | Números del 0 al 99 | verbos | PROBADO (inicial) | 4 | 10 | 7 |
| `zh.a1.clasificadores` | 1 | A1 | 个 y otras palabras de medida; la edad | numeros | PROBADO (inicial) | 4 | 10 | 7 |
| `zh.a1.preguntas` | 1 | A1 | Preguntar: 什么, 谁, 哪儿, 几, 多少 | clasificadores | PROBADO (inicial) | 4 | 10 | 7 |
| `zh.a1.presentacion` | 1 | A1 | Preséntate por completo | preguntas | PROBADO (inicial) | 4 | 10 | 8 |
| `zh.a1.integracion` | 1 | A1 | Integración: conocer a alguien | presentacion | PROBADO (inicial) | 3 | 10 | 8 |

## Japonés (`ja`) · apoyo `es` · revisión inicial

### Fundamentos: hiragana, katakana y primeras frases · nivel `f0` · [f0.json](../../assets/contenido/ja/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `ja.f0.vocales-saludos` | 0 | Pre-A1 | Vocales y saludos | — | PROBADO (inicial) | 6 | 8 | 5 |
| `ja.f0.hiragana-1` | 0 | Pre-A1 | Hiragana: filas か y さ | vocales-saludos | PROBADO (inicial) | 3 | 10 | 6 |
| `ja.f0.hiragana-ta-na` | 0 | Pre-A1 | Hiragana: filas た y な | hiragana-1 | PROBADO (inicial) | 3 | 10 | 6 |
| `ja.f0.hiragana-2` | 0 | Pre-A1 | Hiragana: filas は y ま | hiragana-ta-na | PROBADO (inicial) | 3 | 10 | 6 |
| `ja.f0.hiragana-ya-ra-wa` | 0 | Pre-A1 | Hiragana: filas や, ら, わ y ん | hiragana-2 | PROBADO (inicial) | 3 | 10 | 6 |
| `ja.f0.dakuten-ga-za-da` | 0 | Pre-A1 | Hiragana con ゛: が, ざ y だ | hiragana-ya-ra-wa | PROBADO (inicial) | 3 | 10 | 6 |
| `ja.f0.dakuten-ba-pa` | 0 | Pre-A1 | Hiragana con ゛ y ゜: ば y ぱ | dakuten-ga-za-da | PROBADO (inicial) | 3 | 10 | 6 |
| `ja.f0.yoon` | 0 | Pre-A1 | Hiragana: ゃ, ゅ, ょ pequeñas | dakuten-ba-pa | PROBADO (inicial) | 3 | 10 | 6 |
| `ja.f0.sokuon-largas` | 0 | Pre-A1 | っ pequeña y vocales largas | yoon | PROBADO (inicial) | 4 | 10 | 6 |
| `ja.f0.katakana` | 0 | Pre-A1 | Katakana: ア, カ, サ y la raya ー | sokuon-largas | PROBADO (inicial) | 4 | 10 | 6 |
| `ja.f0.katakana-ta-na-ha` | 0 | Pre-A1 | Katakana: タ, ナ y ハ | katakana | PROBADO (inicial) | 4 | 10 | 6 |
| `ja.f0.katakana-ma-ya-ra-wa` | 0 | Pre-A1 | Katakana: マ, ヤ, ラ, ワ y ン | katakana-ta-na-ha | PROBADO (inicial) | 3 | 10 | 6 |
| `ja.f0.katakana-dakuten-yoon` | 0 | Pre-A1 | Katakana: ゛, ゜, ャ ュ ョ, ッ y ー | katakana-ma-ya-ra-wa | PROBADO (inicial) | 3 | 10 | 6 |
| `ja.f0.katakana-extra` | 0 | Pre-A1 | Katakana: préstamos y tu nombre | katakana-dakuten-yoon | PROBADO (inicial) | 4 | 10 | 7 |
| `ja.f0.desu` | 0 | Pre-A1 | わたし は がくせい です | katakana-extra | PROBADO (inicial) | 8 | 9 | 5 |
| `ja.f0.jikoshoukai` | 0 | Pre-A1 | Preséntate (じこしょうかい) | desu | PROBADO (inicial) | 6 | 9 | 5 |

### Primeras frases · nivel `a1-1` · [a1-1.json](../../assets/contenido/ja/ruta/a1-1.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `ja.a1.pronombres` | 1 | A1 | Pronombres: わたし, あなた, かれ… | jikoshoukai | PROBADO (inicial) | 4 | 10 | 6 |
| `ja.a1.kore-sore-are` | 1 | A1 | これ, それ, あれ: señalar cosas | pronombres | PROBADO (inicial) | 4 | 10 | 6 |
| `ja.a1.verbos-masu` | 1 | A1 | Verbos en ます: presente y pasado | kore-sore-are | PROBADO (inicial) | 4 | 10 | 6 |
| `ja.a1.particulas` | 1 | A1 | Partículas: を, に, へ, で, と | verbos-masu | PROBADO (inicial) | 4 | 10 | 6 |
| `ja.a1.numeros-edad` | 1 | A1 | Números del 1 al 100 y la edad | particulas | PROBADO (inicial) | 4 | 10 | 7 |
| `ja.a1.preguntas` | 1 | A1 | Preguntas: なに, どこ, だれ, いつ | numeros-edad | PROBADO (inicial) | 4 | 10 | 6 |
| `ja.a1.jikoshoukai-completo` | 1 | A1 | Presentación completa (じこしょうかい) | preguntas | PROBADO (inicial) | 5 | 10 | 6 |
| `ja.a1.integracion-a1-1` | 1 | A1 | Integración: una conversación completa | numeros-edad, preguntas, jikoshoukai-completo | PROBADO (inicial) | 3 | 9 | 8 |

## Coreano (`ko`) · apoyo `es` · revisión inicial

### Fundamentos: hangul completo y primeras frases · nivel `f0` · [f0.json](../../assets/contenido/ko/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `ko.f0.vocales-saludos` | 0 | Pre-A1 | Vocales básicas y saludos | — | PROBADO (inicial) | 6 | 10 | 6 |
| `ko.f0.consonantes-bloques` | 0 | Pre-A1 | Consonantes básicas y bloques | vocales-saludos | PROBADO (inicial) | 4 | 10 | 6 |
| `ko.f0.aspiradas-tensas` | 0 | Pre-A1 | Aspiradas y tensas: ㄱ ㅋ ㄲ | consonantes-bloques | PROBADO (inicial) | 4 | 10 | 6 |
| `ko.f0.vocales-compuestas` | 0 | Pre-A1 | Vocales compuestas | aspiradas-tensas | PROBADO (inicial) | 5 | 10 | 6 |
| `ko.f0.batchim` | 0 | Pre-A1 | 받침: la consonante final | vocales-compuestas | PROBADO (inicial) | 4 | 10 | 6 |
| `ko.f0.reglas-lectura` | 0 | Pre-A1 | Leer como se habla: 연음 y asimilación nasal | batchim | PROBADO (inicial) | 6 | 10 | 6 |
| `ko.f0.ieyo-yeyo` | 0 | Pre-A1 | ¿Qué es esto? 이거 뭐예요? | reglas-lectura | PROBADO (inicial) | 5 | 10 | 6 |
| `ko.f0.personas` | 0 | Pre-A1 | Personas y familia | ieyo-yeyo | PROBADO (inicial) | 5 | 10 | 6 |
| `ko.f0.presentarse` | 0 | Pre-A1 | Presentarse con frases fijas | personas | PROBADO (inicial) | 4 | 10 | 6 |

### Primeras frases · nivel `a1-1` · [a1-1.json](../../assets/contenido/ko/ruta/a1-1.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `ko.a1.pronombres` | 1 | A1 | Yo, tú, nosotros: pronombres y 씨 | presentarse | PROBADO (inicial) | 5 | 10 | 6 |
| `ko.a1.identidad` | 1 | A1 | Ser y no ser: 이에요/예요 y 이/가 아니에요 | pronombres | PROBADO (inicial) | 4 | 10 | 6 |
| `ko.a1.tema-sujeto` | 1 | A1 | 은/는 frente a 이/가 | identidad | PROBADO (inicial) | 5 | 10 | 6 |
| `ko.a1.issoyo-eopsoyo` | 1 | A1 | 있어요 / 없어요: tener y haber | tema-sujeto | PROBADO (inicial) | 4 | 10 | 6 |
| `ko.a1.verbos-haeyo` | 1 | A1 | Verbos en 해요체 y negación con 안 | issoyo-eopsoyo | PROBADO (inicial) | 6 | 10 | 6 |
| `ko.a1.particulas` | 1 | A1 | Partículas: 을/를, 에, 에서 | verbos-haeyo | PROBADO (inicial) | 6 | 10 | 6 |
| `ko.a1.numeros` | 1 | A1 | Números y edad | particulas | PROBADO (inicial) | 4 | 11 | 6 |
| `ko.a1.preguntas` | 1 | A1 | Preguntas: 뭐, 어디, 누구, 언제 | numeros | PROBADO (inicial) | 4 | 11 | 6 |
| `ko.a1.integracion` | 1 | A1 | Integración: mi presentación completa | preguntas | PROBADO (inicial) | 4 | 9 | 9 |

## Ruso (`ru`) · apoyo `es` · revisión inicial

### Fundamentos: el cirílico y tus primeras frases · nivel `f0` · [f0.json](../../assets/contenido/ru/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `ru.f0.bukvy-druzya` | 0 | Pre-A1 | Letras iguales y falsos amigos | — | PROBADO (inicial) | 5 | 11 | 6 |
| `ru.f0.bukvy-novye` | 0 | Pre-A1 | Letras nuevas, sonidos conocidos | bukvy-druzya | PROBADO (inicial) | 4 | 11 | 6 |
| `ru.f0.shipyashchie` | 0 | Pre-A1 | Sonidos nuevos: Ж, Ш, Щ, Ч, Ц | bukvy-novye | PROBADO (inicial) | 3 | 11 | 6 |
| `ru.f0.glasnye` | 0 | Pre-A1 | Vocales duras y blandas | shipyashchie | PROBADO (inicial) | 4 | 11 | 6 |
| `ru.f0.znaki` | 0 | Pre-A1 | Ь y Ъ: consonantes duras y blandas | glasnye | PROBADO (inicial) | 3 | 11 | 6 |
| `ru.f0.udarenie` | 0 | Pre-A1 | El alfabeto completo y la sílaba fuerte | znaki | PROBADO (inicial) | 4 | 11 | 6 |
| `ru.f0.mestoimeniya` | 0 | Pre-A1 | Я, ты, вы: pronombres y trato | udarenie | PROBADO (inicial) | 4 | 11 | 6 |
| `ru.f0.eto` | 0 | Pre-A1 | ¿Qué es esto? Это… | mestoimeniya | PROBADO (inicial) | 3 | 11 | 6 |
| `ru.f0.ne-voprosy` | 0 | Pre-A1 | No, sí y ¿dónde?: не, нет, где | eto | PROBADO (inicial) | 4 | 11 | 6 |
| `ru.f0.predstavlenie` | 0 | Pre-A1 | Me llamo… y soy de… | ne-voprosy | PROBADO (inicial) | 3 | 11 | 6 |

### Primeras frases · nivel `a1-1` · [a1-1.json](../../assets/contenido/ru/ruta/a1-1.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `ru.a1.ya-student` | 1 | A1 | Я студент: quién es quién | predstavlenie | PROBADO (inicial) | 4 | 11 | 6 |
| `ru.a1.rod` | 1 | A1 | Género: мой, моя, моё | ya-student | PROBADO (inicial) | 4 | 11 | 6 |
| `ru.a1.mnozhestvennoe` | 1 | A1 | Plural: книги, столы, окна | rod | PROBADO (inicial) | 4 | 11 | 6 |
| `ru.a1.chitat` | 1 | A1 | Verbos (1): читать, знать, работать, делать | mnozhestvennoe | PROBADO (inicial) | 4 | 11 | 6 |
| `ru.a1.govorit` | 1 | A1 | Verbos (2): говорить, любить | chitat | PROBADO (inicial) | 4 | 11 | 6 |
| `ru.a1.voprosy` | 1 | A1 | Preguntas y negación: кто, что, где, как, откуда | govorit | PROBADO (inicial) | 4 | 12 | 6 |
| `ru.a1.chisla` | 1 | A1 | Números del 0 al 20 y la edad | voprosy | PROBADO (inicial) | 3 | 12 | 6 |
| `ru.a1.predstavlenie` | 1 | A1 | Presentarte del todo | chisla | PROBADO (inicial) | 4 | 12 | 6 |
| `ru.a1.integratsiya` | 1 | A1 | Integración: así soy yo | predstavlenie | PROBADO (inicial) | 3 | 10 | 8 |

Total: 204 unidades implementadas.

## Diseñado, no implementado

Grafo gramatical inglés pre-A1→C2 (111 nodos `en-g-*`) y mapas A2–C2 de los otros 9 idiomas: [auditoria/A-curriculo-gramatica.md](auditoria/A-curriculo-gramatica.md). Las 50 situaciones: [auditoria/B-vocabulario-situaciones.md](auditoria/B-vocabulario-situaciones.md).
