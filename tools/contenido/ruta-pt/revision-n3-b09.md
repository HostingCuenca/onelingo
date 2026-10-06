GO

# Revisión pt N3 B9 (pt.n3.c41–c45)

Validador: `python3 tools/curriculo/validar_bloque.py pt 3 9` → 0 errores. Borrador del autor respaldado en el scratch (`rev-n3-b09/n3-b09.autor.json`). Total aproximado de correcciones: 110 (85 filas de tablas «Para ler» quitadas, 38 filas rehechas, 6 tablas «Para ler» sobrantes eliminadas y ~20 ediciones de contenido).

## Contraste con las fichas
- Las 5 clases enseñan su `introduce` y nada más: acho que + indicativo / não acho que, duvido que + subjuntivo (c41), segundo… / de acordo com / parece que (c42), vale a pena + infinitivo (c43), resumen quem / o quê / quando / onde (c44), reconocimiento de la pasiva ser + participio (c45). Vocabulario de la ficha completo (8 por clase); ejercicios, claves y tareas siguen el plan; los `relacionar` de la ficha (e3 en c41, c42, c44; e4 en c43, c45) se conservan; sin menciones de Ecuador.
- ESCUCHA: 2 `escuchar` por clase (g2 y e2), con opciones en portugués y una sola respuesta.
- Guiadas con 3 ítems, independientes con 3; evaluaciones con 5 ítems y 5 formatos.
- Lecturas (situación) de 150 / 148 / 150 / 162 / 154 palabras (el autor tenía 132 / 131 / 132 / 133 / 131): alargadas con réplicas naturales que reciclan lo ya enseñado, sin vocabulario nuevo; en c44 se añadió además el cierre sobre el precio.
- Campo `es` de todos los contextos en español, `en` en inglés: correcto en las 5 clases.

## Cambios por tipo
**Tablas «Para ler» (85 filas quitadas)**
- Método (como en B7/B8): se vació cada tabla «Para ler» y se corrió el validador; solo quedan las palabras no enseñadas en N1–N3 B8 ni antes en el propio bloque (el validador acumula dentro del bloque), en forma base. Quedan: c41 11 (incrível, protagonista, excelente, ruim, concordar, explicação, fotografia, amanhecer, cena, lindo, rio), c42 12 (próprio, diretor, estreia, festival, gratuito, show, orquestra, ponte, recifense, sessão, ganhar, prêmio), c43 2 (disco, dublado), c44 3 (graça, trailer, abertura), c45 10 (atriz, cineasta, júri, popular, resenha, passivo, verbo, elogiar, documentário, TV). Cada clase conserva además su tabla gramatical.
- Cada clase queda con una sola tabla «Para ler» (se eliminaron las de «más palabras») y los ids de paso se renumeraron.
- Formas flexionadas quitadas: viram, viu, divulgou, toca, ganhou, ensaiando, organiza/organizam, custam, vi, acontece, falta, exibiu, dirigem, elogiou, ia, acha, gostei/gostou, concordo, bons, os atores, atores, gratuitas, etc.
- Palabras ya enseñadas quitadas: filme, final, público, sucesso, experiência, perfeito, suficiente, surpreender, entender, dia, sexta, números, fila, domingo, chover, ver, ouvir, comprar, chegar, cedo, antes, porque, quebrado, ar-condicionado, sala, tranquilo, grupo, pernambucano, organizar, mostra, novo, antigo, custar, abrir, faltar, acontecer, dezembro, todo mundo, história, surpresa, apresentação, escrito, composto, instalado, já, principal, alto, pois é, etc.
- Antes → después: «concordo» → «concordar»; «linda» → «lindo»; «os atores» → eliminado (el ejemplo usa «o elenco»); «a cineasta» → «o cineasta»; «a passiva» → «passivo»; «os verbos» → «o verbo»; «a diretora» → «o diretor».
- Fila «a ponte» (c42): «Entre Pontes» aparece en las lecturas y el validador exige «ponte».

**Contenido y coherencia (≈20 ediciones)**
- c41: falso amigo inventado («roteiro no es “rotero”») → «roteiro es el guion y también el itinerario de un viaje»; el apoyo EN decía que en inglés «“I don't think it is” takes a different mood», impreciso → «Spanish works the same way: creo que es, pero no creo que sea»; el apartado de sonido mezclaba é / seja / tem / faz sin sentido → compara «é» (e abierta) con «seja» (e cerrada). Diálogo: dos réplicas seguidas de Camila (la segunda con «Mesmo assim» sin sentido) → fusionadas; añadida réplica de Lucas («não acho que o público goste do final»). El ejemplo modelo del escribir ya no usa «os atores / original» (evita dos palabras sin enseñar): «Acho que o elenco é bom. Não acho que o roteiro seja perfeito. Duvido que o filme ganhe prêmios.»
- c42: se sustituyeron por palabras ya enseñadas «Sério?» → «Verdade?», «Interessante.» (quitado), «é professor» → «mora perto do cinema», «Vamos nessa?» → «Combinado?»; añadida la réplica «Não acho que a fonte seja ruim, porque os números vêm do próprio cinema. Mas o jornal podia divulgar o nome dele» (recicla c41).
- c43: añadido el intercambio Bia/Camila «E a Ana vai também? / Segundo ela, vale a pena ver o filme duas vezes» (150 palabras).
- c44: calendario real 2026 (el curso transcurre en dic. 2026): «sábado, 16 de dezembro» (de la ficha) cae en miércoles → «sábado, 12 de dezembro» en la tabla, el ejemplo y g1; «domingo, dia 10» (el 10 es jueves) → «domingo, dia 13»; typo «segundo la reportagem» → «segundo a reportagem»; añadido cierre (Dona Marina pregunta el precio; Camila: «Dez reais, segundo a reportagem. Vale a pena comprar antes, porque a fila é grande no fim de semana»).
- c45: error frecuente «foi dirigido de uma recifense» (en español también es «por», no es error de hispanohablante) → «aclamado por a crítica» → «pela crítica» (el hispanohablante no conoce la contracción por + a = pela); réplicas ampliadas con la lista de verbos pasivos y «Duvido que alguém não goste dela» (recicla c41).

**Distractores y errores frecuentes**: revisados; los demás son errores reales de hispanohablante o calcos (acho de que; segundo que; de acordo a; segundo eu; vale pena / vale a pena de / vale a pena que; o sábado; onde/quando; filmado/lançada sin concordancia). Una sola respuesta por ítem; sin cambios.

**ES neutro latino**: «función», «jugo», «celular», «tráiler», «entrada»; sin «coche», «móvil», «vale», «ordenador».

## Dudas del autor, decididas
1. Tablas «Para ler» con formas ya vistas (acha, viu, ganhou…): deduplicadas contra N1–N3 B1–B8 y dentro del bloque; ver arriba (≤12 filas por clase).
2. Hechos «Entre Pontes», Cinema São Luiz, mostra 10–16 de diciembre, entradas R$10, maracatu de Lucas: confirmados (ver abajo).

## Correcciones de ficha
- pt.n3.c44: el ejemplo de la ficha «sábado, 16 de dezembro» no es sábado en 2026 (cae en miércoles; la mostra va del jueves 10 al miércoles 16). El borrador usa «sábado, 12 de dezembro». La ficha no se toca.
- Observación menor: «Entre Pontes» se describe como «novo» en c41 y «foi lançado em março» en c45 (ficha); se interpreta como estreno en festivales en marzo y llegada reciente a las salas de Recife.

## Hechos del reparto confirmados
- c41: Camila, Ana y Lucas salen del Cinema São Luiz de ver «Entre Pontes» (película pernambucana sobre una familia que vive cerca del Capibaribe): Ana elogia la actuación de la protagonista; Camila dice que la banda sonora tiene frevo y maracatu; Lucas no cree que el guion sea perfecto (final muy rápido, dudo que el público entienda todo); todos creen que la crítica la va a apreciar; Ana propone un jugo en el Café da Bia.
- c42: Ana lee en el celular la nota del periódico («Filme recifense ganha mais duas semanas no Cinema São Luiz»): más de diez mil personas ya la vieron, según el cine mismo; un entrevistado la vio tres veces (nombre no divulgado); Bia quiere ir el sábado con ellas; sesión de las siete, la más tranquila (según Lucas).
- c43: Camila le manda un audio a Bia: vale a pena ver la película en el Cinema São Luiz (sala linda, sesión de las siete); el sábado hay estreno de otra película pernambucana; el grupo de maracatu de Lucas toca el domingo en un festival en el Recife Antigo (una orquesta de frevo toca antes; entradas gratuitas); Ana también va.
- c44: almuerzo del domingo: Camila resume a Dona Marina la nota: el Cinema São Luiz organiza una mostra de cine pernambucano del 10 al 16 de diciembre (jueves a miércoles, 2026), entradas R$10, abre con «Entre Pontes»; Camila, Ana, Lucas y Dona Marina van el domingo 13. Ejemplos: orquesta de frevo, show gratis en el Paço do Frevo / Marco Zero; el grupo de maracatu de Lucas se presenta en el Paço do Frevo el domingo a las 17h (ejemplo del ejercicio, no hecho del relato).
- c45: reseña de un sitio de cultura leída por Ana: «Entre Pontes» dirigida por una cineasta recifense, filmada en Recife y Olinda, guion escrito en dos años, banda sonora grabada por una orquesta de frevo, lanzada en marzo, exhibida en tres festivales, aclamada por la crítica y premiada por el jurado popular; Lucas pidió que la vieran de nuevo con él.
- Nombres: Camila, Ana, Lucas, Bia, Dona Marina. Anónimos: la cineasta, el entrevistado. Ningún nombre secundario nuevo.

## Sin resolver
- Ninguno.

## Nota del orquestador

N3 transcurre en 2028 (MAPA), no en 2026: el 16-12-2028 es sábado y el 10-12-2028 domingo. Se revierte el cambio de fechas de c44 a lo de la ficha («sábado, 16 de dezembro», «domingo, dia 10»), que además coincide con las traducciones. La corrección de ficha sobre c44 queda anulada.
