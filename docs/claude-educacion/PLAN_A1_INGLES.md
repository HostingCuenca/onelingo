# Plan A1 de inglés (niveles internos 1–2) — esqueleto fijo

Fecha: 2026-09-26. Fuente: grafo de la auditoría A (§A1) + huecos de la auditoría B (peticiones corteses, contables/incontables).
Los IDs, `orden`, `nivel` y prerrequisitos de esta tabla son **contractuales**: los agentes de contenido no los cambian.

## Módulos y archivos

| Módulo | Nivel (curso.json) | nivelInterno | Archivo | Propietario |
|---|---|---:|---|---|
| `en.a1-1` «Personas, cosas y lugares» | `a1-1` | 1 | `assets/contenido/en/ruta/a1-1.json` | Agente A1-1 |
| `en.a1-2.presente` «El presente simple» | `a1-2` | 2 | `assets/contenido/en/ruta/a1-2-presente.json` | Agente A1-2P |
| `en.a1-2.comunicar` «Comunicarte en el día a día» | `a1-2` | 2 | `assets/contenido/en/ruta/a1-2-comunicar.json` | Agente A1-2C |

Todas las unidades: `cefr: "A1"`, `nivelInterno` según el módulo, `idiomasApoyo: ["es"]`.

## Unidades

| orden | ID | Tema | Prerrequisitos | Grafo | Guía actual relacionada |
|---:|---|---|---|---|---|
| 6 | `en.a1.posesivos` | my / your / his / her / its / our / their | en.f0.presentarse | possessive-adj | pronouns-possessives |
| 7 | `en.a1.articulo-a-an` | a / an con profesiones y objetos | en.f0.presentarse | articles-a-an | articles-plurals |
| 8 | `en.a1.plurales` | plural regular e irregular frecuente | en.a1.articulo-a-an | plural-nouns | articles-plurals |
| 9 | `en.a1.articulo-the` | the frente a a/an; plural sin artículo | en.a1.plurales | article-the | articles-plurals |
| 10 | `en.a1.adjetivos` | adjetivo invariable antes del sustantivo; colores y tamaños | en.a1.articulo-a-an | adj-position, word-order | order |
| 11 | `en.a1.demostrativos` | this / that / these / those | en.a1.plurales | demonstratives | — |
| 12 | `en.a1.genitivo-s` | Ana's book; familia | en.a1.posesivos | possessive-s | — |
| 13 | `en.a1.have-got` | have got / has got (posesión, familia, rasgos) | en.a1.genitivo-s | have-got | — |
| 14 | `en.a1.there-is-are` | there is / there are ± ? | en.a1.articulo-the | there-is-are | there-be |
| 15 | `en.a1.preposiciones-lugar` | in / on / under / next to / between | en.a1.there-is-are | prep-place-basic | time-place |
| 16 | `en.a1.imperativos` | Sit down / Don't… / Please… (instrucciones) | en.a1.preposiciones-lugar | imperatives | — |
| 17 | `en.a1.integracion-a1-1` | Integración: describir tu casa y tu familia | en.a1.adjetivos, en.a1.demostrativos, en.a1.have-got, en.a1.imperativos | — | — |
| 18 | `en.a1.presente-simple` | presente simple I/you/we/they; S + V + O (+ lugar + tiempo) | en.a1.integracion-a1-1 | pres-simple-aff, word-order | present, order |
| 19 | `en.a1.presente-3s` | he/she/it + -s / -es / -ies | en.a1.presente-simple | pres-simple-3s | present |
| 20 | `en.a1.dont-doesnt` | negación don't / doesn't | en.a1.presente-3s | do-negative | present |
| 21 | `en.a1.do-preguntas` | Do/Does…? + respuestas cortas | en.a1.dont-doesnt | do-questions | present, questions |
| 22 | `en.a1.wh-do` | What / Where / When / What time + do/does; Who + verbo | en.a1.do-preguntas | wh-do | questions |
| 23 | `en.a1.frecuencia` | always / usually / often / sometimes / never (posición con be y con verbos) | en.a1.presente-3s | freq-adverbs | frequency |
| 24 | `en.a1.preposiciones-tiempo` | at / on / in (horas, días, meses, partes del día) | en.a1.presente-simple | prep-time | time-place |
| 25 | `en.a1.integracion-rutina` | Integración: tu rutina y la de otra persona | en.a1.wh-do, en.a1.frecuencia, en.a1.preposiciones-tiempo | — | — |
| 26 | `en.a1.can` | can / can't (capacidad y permiso); Can you…? | en.a1.do-preguntas | can-ability | ability |
| 27 | `en.a1.like-ing` | like / love / hate + sustantivo o -ing | en.a1.presente-3s | like-ing | — |
| 28 | `en.a1.pronombres-objeto` | me / you / him / her / it / us / them | en.a1.presente-simple | object-pron | object-possessive |
| 29 | `en.a1.posesivos-pronombre` | mine / yours / his / hers / ours / theirs; Whose…? | en.a1.pronombres-objeto, en.a1.posesivos | possessive-pron | object-possessive |
| 30 | `en.a1.some-any` | contables e incontables; some / any; How many / How much (básico) | en.a1.there-is-are, en.a1.do-preguntas | some-any-basic | quantity |
| 31 | `en.a1.pedir-cortes` | I'd like… / Can I have…? / Could I…? (bloques); pedir en un restaurante | en.a1.some-any, en.a1.can | (nuevo: polite-requests) | — |
| 32 | `en.a1.presente-continuo` | am/is/are + -ing (ahora) y contraste con presente simple | en.a1.presente-3s, en.f0.be-preguntas | pres-continuous | continuous |
| 33 | `en.a1.conectores` | and / but / or / because / so | en.a1.presente-simple | conj-basic | — |
| 34 | `en.a1.integracion-a1` | Integración final A1: conocer a alguien y quedar en una cafetería | en.a1.pedir-cortes, en.a1.presente-continuo, en.a1.conectores, en.a1.integracion-rutina, en.a1.like-ing, en.a1.posesivos-pronombre | — | — |

Las unidades de integración no enseñan gramática nueva: repasan con ejemplos nuevos, un diálogo más largo y una evaluación mixta (≥ 6 ítems, ≥ 3 formatos). Son la prueba de módulo.

Campo nuevo opcional por unidad: `"guias": ["present"]` (ids de `lib/core/content/grammar_guides.dart`), informativo, para enlazar con la guía de gramática existente.
