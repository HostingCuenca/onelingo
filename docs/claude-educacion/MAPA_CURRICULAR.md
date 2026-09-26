# Mapa curricular — índice maestro de unidades

Generado con `python3 tools/generar_mapa_curricular.py` desde `assets/contenido/<idioma>/ruta/`. PROBADO = pasa `tools/validar_ruta.py` y `test/ruta_contenido_test.dart`; «inicial» = sin revisión nativa.
Enseña / Practica / Evalúa = pasos de enseñanza / ítems de práctica (guiada + independiente + situación) / ítems de evaluación.

Escala interna (DEC-002): 0 = Fundamentos (Pre-A1) · 1–2 A1 · 3–4 A2 · 5–6 B1 · 7–8 B2 · 9–10 C1 · C2 planificado. Plan de A1 de inglés: [PLAN_A1_INGLES.md](PLAN_A1_INGLES.md).

## Inglés (`en`) · apoyo `es` · revisión revisada

### Fundamentos: tus primeras frases · nivel `f0` · [f0.json](../../assets/contenido/en/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `en.f0.primer-contacto` | 0 | Pre-A1 | Primer contacto | — | PROBADO | 3 | 6 | 5 |
| `en.f0.pronombres` | 0 | Pre-A1 | Pronombres personales | primer-contacto | PROBADO | 3 | 8 | 5 |
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

### Foundations: your first sentences in Spanish · nivel `f0` · [f0.json](../../assets/contenido/es/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `es.f0.sonidos-saludos` | 0 | Pre-A1 | Sounds and greetings | — | PROBADO (inicial) | 4 | 8 | 6 |
| `es.f0.yo-tu-usted` | 0 | Pre-A1 | Yo, tú, usted: pronouns and politeness | sonidos-saludos | PROBADO (inicial) | 5 | 9 | 6 |
| `es.f0.ser` | 0 | Pre-A1 | Ser: who you are and where you're from | yo-tu-usted | PROBADO (inicial) | 5 | 10 | 5 |
| `es.f0.estar` | 0 | Pre-A1 | Estar: how and where you are | ser | PROBADO (inicial) | 4 | 11 | 6 |
| `es.f0.negacion-preguntas` | 0 | Pre-A1 | No, ¿…? and ¡…! | estar | PROBADO (inicial) | 5 | 10 | 6 |
| `es.f0.presentarse` | 0 | Pre-A1 | Introducing yourself | negacion-preguntas | PROBADO (inicial) | 4 | 9 | 5 |

## Francés (`fr`) · apoyo `es` · revisión inicial

### Fundamentos: tus primeras frases · nivel `f0` · [f0.json](../../assets/contenido/fr/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `fr.f0.premier-contact` | 0 | Pre-A1 | Primer contacto | — | PROBADO (inicial) | 4 | 8 | 6 |
| `fr.f0.sons` | 0 | Pre-A1 | Sonidos del francés | premier-contact | PROBADO (inicial) | 6 | 9 | 6 |
| `fr.f0.pronoms` | 0 | Pre-A1 | Pronombres: tu y vous | sons | PROBADO (inicial) | 5 | 9 | 6 |
| `fr.f0.etre` | 0 | Pre-A1 | El verbo «être» | pronoms | PROBADO (inicial) | 5 | 9 | 6 |
| `fr.f0.negation-questions` | 0 | Pre-A1 | Negar y preguntar | etre | PROBADO (inicial) | 5 | 9 | 6 |
| `fr.f0.se-presenter` | 0 | Pre-A1 | Presentarte | negation-questions | PROBADO (inicial) | 3 | 9 | 6 |

## Alemán (`de`) · apoyo `es` · revisión inicial

### Fundamentos: tus primeras frases en alemán · nivel `f0` · [f0.json](../../assets/contenido/de/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `de.f0.laute-gruesse` | 0 | Pre-A1 | Sonidos y saludos | — | PROBADO (inicial) | 4 | 8 | 6 |
| `de.f0.pronomen-du-sie` | 0 | Pre-A1 | Pronombres: ¿du o Sie? | laute-gruesse | PROBADO (inicial) | 4 | 10 | 6 |
| `de.f0.sein-heissen` | 0 | Pre-A1 | sein, heißen y kommen aus | pronomen-du-sie | PROBADO (inicial) | 5 | 11 | 5 |
| `de.f0.der-die-das` | 0 | Pre-A1 | der, die, das: el género | sein-heissen | PROBADO (inicial) | 5 | 10 | 6 |
| `de.f0.nicht-kein-fragen` | 0 | Pre-A1 | Negar y preguntar | der-die-das | PROBADO (inicial) | 5 | 11 | 6 |
| `de.f0.vorstellen` | 0 | Pre-A1 | Presentarte | nicht-kein-fragen | PROBADO (inicial) | 3 | 9 | 5 |

## Portugués (BR) (`pt`) · apoyo `es` · revisión inicial

### Fundamentos: tus primeras frases (portugués de Brasil) · nivel `f0` · [f0.json](../../assets/contenido/pt/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `pt.f0.primeiro-contato` | 0 | Pre-A1 | Primer contacto | — | PROBADO (inicial) | 4 | 8 | 6 |
| `pt.f0.sons` | 0 | Pre-A1 | Sonidos del portugués de Brasil | primeiro-contato | PROBADO (inicial) | 6 | 9 | 6 |
| `pt.f0.pronomes` | 0 | Pre-A1 | Pronombres: eu, você, a gente | sons | PROBADO (inicial) | 5 | 9 | 6 |
| `pt.f0.ser-estar` | 0 | Pre-A1 | Ser y estar | pronomes | PROBADO (inicial) | 5 | 10 | 6 |
| `pt.f0.negacao-perguntas` | 0 | Pre-A1 | Negar y preguntar | ser-estar | PROBADO (inicial) | 5 | 9 | 6 |
| `pt.f0.apresentar-se` | 0 | Pre-A1 | Presentarte y falsos amigos | negacao-perguntas | PROBADO (inicial) | 5 | 9 | 7 |

## Italiano (`it`) · apoyo `es` · revisión inicial

### Fundamentos: tus primeras frases · nivel `f0` · [f0.json](../../assets/contenido/it/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `it.f0.primo-contatto` | 0 | Pre-A1 | Primer contacto | — | PROBADO (inicial) | 4 | 8 | 6 |
| `it.f0.suoni` | 0 | Pre-A1 | Sonidos del italiano | primo-contatto | PROBADO (inicial) | 6 | 9 | 6 |
| `it.f0.pronomi` | 0 | Pre-A1 | Pronombres: tu y Lei | suoni | PROBADO (inicial) | 5 | 9 | 6 |
| `it.f0.essere-stare` | 0 | Pre-A1 | Essere y stare | pronomi | PROBADO (inicial) | 5 | 10 | 6 |
| `it.f0.negazione-domande` | 0 | Pre-A1 | Negar y preguntar | essere-stare | PROBADO (inicial) | 5 | 9 | 6 |
| `it.f0.presentarsi` | 0 | Pre-A1 | Presentarte | negazione-domande | PROBADO (inicial) | 3 | 9 | 6 |

## Chino mandarín (`zh`) · apoyo `es` · revisión inicial

### Fundamentos: tonos, caracteres y primeras frases · nivel `f0` · [f0.json](../../assets/contenido/zh/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `zh.f0.tonos-saludos` | 0 | Pre-A1 | Tonos y saludos | — | PROBADO (inicial) | 5 | 8 | 5 |
| `zh.f0.pinyin` | 0 | Pre-A1 | Sonidos del pinyin | tonos-saludos | PROBADO (inicial) | 7 | 8 | 5 |
| `zh.f0.caracteres` | 0 | Pre-A1 | Tus primeros caracteres | pinyin | PROBADO (inicial) | 5 | 9 | 5 |
| `zh.f0.pronombres` | 0 | Pre-A1 | Yo, tú, él, ella | caracteres | PROBADO (inicial) | 7 | 8 | 5 |
| `zh.f0.shi-bushi-ma` | 0 | Pre-A1 | Soy estudiante: 是, 不 是 y 吗 | pronombres | PROBADO (inicial) | 6 | 9 | 5 |
| `zh.f0.presentarse` | 0 | Pre-A1 | Preséntate | shi-bushi-ma | PROBADO (inicial) | 6 | 9 | 5 |

## Japonés (`ja`) · apoyo `es` · revisión inicial

### Fundamentos: kana y primeras frases · nivel `f0` · [f0.json](../../assets/contenido/ja/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `ja.f0.vocales-saludos` | 0 | Pre-A1 | Vocales y saludos | — | PROBADO (inicial) | 6 | 8 | 5 |
| `ja.f0.hiragana-1` | 0 | Pre-A1 | Hiragana: filas か, さ, た y な | vocales-saludos | PROBADO (inicial) | 4 | 8 | 5 |
| `ja.f0.hiragana-2` | 0 | Pre-A1 | Hiragana: filas は a わ, ん y comillas ゛ | hiragana-1 | PROBADO (inicial) | 5 | 8 | 5 |
| `ja.f0.katakana` | 0 | Pre-A1 | Katakana: palabras extranjeras y nombres | hiragana-2 | PROBADO (inicial) | 5 | 8 | 5 |
| `ja.f0.desu` | 0 | Pre-A1 | わたし は がくせい です | katakana | PROBADO (inicial) | 8 | 9 | 5 |
| `ja.f0.jikoshoukai` | 0 | Pre-A1 | Preséntate (じこしょうかい) | desu | PROBADO (inicial) | 6 | 9 | 5 |

## Coreano (`ko`) · apoyo `es` · revisión inicial

### Fundamentos: hangul y primeras frases · nivel `f0` · [f0.json](../../assets/contenido/ko/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `ko.f0.vocales-saludos` | 0 | Pre-A1 | Vocales y saludos | — | PROBADO (inicial) | 6 | 8 | 5 |
| `ko.f0.consonantes-bloques` | 0 | Pre-A1 | Consonantes y bloques | vocales-saludos | PROBADO (inicial) | 5 | 8 | 5 |
| `ko.f0.batchim` | 0 | Pre-A1 | Aspiradas, tensas y 받침 | consonantes-bloques | PROBADO (inicial) | 5 | 9 | 5 |
| `ko.f0.personas` | 0 | Pre-A1 | Yo, nosotros y cómo llamar a los demás | batchim | PROBADO (inicial) | 5 | 8 | 5 |
| `ko.f0.ieyo-yeyo` | 0 | Pre-A1 | 저는 학생이에요 | personas | PROBADO (inicial) | 9 | 9 | 5 |
| `ko.f0.presentarse` | 0 | Pre-A1 | Preséntate | ieyo-yeyo | PROBADO (inicial) | 6 | 9 | 5 |

## Ruso (`ru`) · apoyo `es` · revisión inicial

### Fundamentos: el cirílico y tus primeras frases · nivel `f0` · [f0.json](../../assets/contenido/ru/ruta/f0.json)

| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |
|---|---:|---|---|---|---|---:|---:|---:|
| `ru.f0.bukvy-druzya` | 0 | Pre-A1 | Letras amigas y saludos | — | PROBADO (inicial) | 4 | 9 | 6 |
| `ru.f0.bukvy-novye` | 0 | Pre-A1 | Letras nuevas y sílaba fuerte | bukvy-druzya | PROBADO (inicial) | 4 | 10 | 6 |
| `ru.f0.mestoimeniya` | 0 | Pre-A1 | Pronombres: ¿ты o вы? | bukvy-novye | PROBADO (inicial) | 4 | 10 | 6 |
| `ru.f0.eto` | 0 | Pre-A1 | Я студент: frases sin «ser» | mestoimeniya | PROBADO (inicial) | 5 | 9 | 6 |
| `ru.f0.ne-voprosy` | 0 | Pre-A1 | Negar con не y preguntar | eto | PROBADO (inicial) | 5 | 10 | 5 |
| `ru.f0.predstavlenie` | 0 | Pre-A1 | Presentarte | ne-voprosy | PROBADO (inicial) | 3 | 9 | 6 |

Total: 89 unidades implementadas.

## Diseñado, no implementado

Grafo gramatical inglés pre-A1→C2 (111 nodos `en-g-*`) y mapas A2–C2 de los otros 9 idiomas: [auditoria/A-curriculo-gramatica.md](auditoria/A-curriculo-gramatica.md). Las 50 situaciones: [auditoria/B-vocabulario-situaciones.md](auditoria/B-vocabulario-situaciones.md).
