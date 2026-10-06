# Encargo: ruta de portugués de Brasil N1–N10 para hispanohablantes, 50 clases por nivel en 10 bloques

Equivale a `ENCARGO_RUTA_ES.md` y `ENCARGO_RUTA_FR.md` para el portugués (DEC-034, DEC-035). Vale para todos los niveles con la tabla «Por nivel». El alumno es **hispanohablante** (apoyo en español; inglés americano como segundo apoyo).

Lee antes:
- tu **paquete de contexto** (`python3 tools/curriculo/paquete.py pt N B`). Contiene tus 5 fichas de `curriculo/pt/nX.json`, el reparto y los hechos, la nota del nivel y una clase modelo. Escribe exactamente lo que dicen las fichas: la gramática nueva es solo la de su `introduce`; lo ya visto va como repaso (`recicla`). Los ejercicios siguen su plan (`ejercicios`): mismo formato, misma clave, misma cosa evaluada. Puedes pulir la redacción y completar `aceptadas`, pistas y feedback;
- `curriculo/pt/MAPA.md`: reglas del idioma, **reparto canónico (Camila Ortega, Dona Marina, Lucas, Ana, Bruno, Bia…)**, cronología, calendario de N1 y hechos reales de Recife. **Manda sobre los nombres de ejemplo de las fichas** si chocan;
- `PLAN_PORTUGUES.md` (DEC-035) y `ESQUEMA_CONTENIDO.md` (esquema 2).

## Por nivel

| Nivel | cefr | nivelInterno | Duración | Sonido del día | Lectura en la situación |
|---|---|---|---|---|---|
| N1 | A1 | 1 | 10–12 min | sí (`sonido` de la ficha) | diálogo de 3–6 líneas |
| N2 | A2 | 2 | 12–15 min | no; nota de pronunciación si hace falta | 6–10 líneas (≈ 80–120 palabras) |
| N3–N4 | B1 | 3–4 | 15 min | no | 150–250 palabras |
| N5–N7 | B2 | 5–7 | 15–20 min | no | 300–500 palabras |
| N8–N10 | C1 | 8–10 | 20 min | no | 400–700 palabras |

Desde N5 los proyectos y cierres incluyen tareas integradas inspiradas en Celpe-Bras (insumo oral o escrito + propósito + interlocutor + producto). Celpe-Bras no tiene nivel A1: en N1 es solo referencia.

## Archivo por bloque

`tools/contenido/ruta-pt/nX-bYY.json` con `{"modulo": "pt.nX-bYY", "unidades": [5 unidades]}`. La revisión va en `revision-nX-bYY.md`.

- **Ids:** `pt.nX.c01` … `pt.nX.c50`. **Orden:** 100·X + n. **Prerrequisitos:** N1 c01 → `pt.f0.apresentar-se`; c01 de los demás niveles → la c50 del nivel anterior; cada clase → la anterior.
- **Textos de apoyo:** todos `{"es": …, "en": …}`: español latinoamericano neutro con tú e inglés americano. Las consignas y explicaciones se escriben desde el español; la versión inglesa compara con el inglés cuando ayuda.
- **Guías de pronunciación (el sonido del día y las notas)**, coherentes con el Nivel 0:
  - ES: «ão» ≈ «aun» nasal sin cerrar la boca; «nh» como la «ñ»; «lh» como «lli» (no «l»+«y»); «ç» como «s»; «rr» y «r» inicial como una «j» suave (en pt-BR); la «r» final suele ser muy suave; «d» y «t» antes de «i» suenan «dyi»/«chi» en la mayor parte de Brasil (el modelo es neutro: no se exige); la «e» y la «o» átonas finales se reducen («leite» ≈ «leitchi»); «s» entre vocales como «z»; «x» varía («xícara» «sh»).
  - EN: «ão» is a nasal «ow»; «nh» like «ny» in «canyon»; «lh» like «lli» in «million»; «ç» is «s»; «rr» like English «h».
  - Nunca se promete un sonido igual al español: se avisa de la diferencia (vocales abiertas/cerradas, nasales, reducción final).

## Cada clase

En orden: `explicacion` (en N1 abre con el sonido del día), `ejemplos` (5–8 con audio), `vocabulario` (6–12 palabras de la ficha, con artículo en los sustantivos), `patron` o `tabla` (conjugaciones completas, **`você/a gente/vocês`** con 3.ª persona; `tu` solo receptivo), `practica_guiada` (3–5 con `pista`), `practica_independiente` (3–4), `situacion` (contexto, diálogo o texto, 1–2 preguntas), `evaluacion` (≥ 4 ítems puntuables y ≥ 2 formatos; los `escribir` abiertos no cuentan). Además: `erroresFrecuentes` ≥ 1, **típicos de hispanohablantes** («Eu sou 27 anos», «Muito obligado», «Eu tengo fome», «Eu gusto de café», «*ñ por nh», «*a casa es grande»), `recicla` ≥ 30 % del vocabulario anterior y los seis formatos (elegir, escuchar, ordenar, completar, escribir, relacionar) a lo largo del bloque.

## Reglas (las comprueba `validar_ruta.py pt`; con `reglasAutoria` también las de calibración, la extensión de la lectura y los apellidos del reparto)

- **Nada sin enseñar.** Cada palabra portuguesa de respuestas, opciones, audios, diálogos y ordenar aparece antes en un paso de enseñanza (`ejemplos`, `vocabulario`, `patron`, `tabla`) de esta clase o de una anterior, incluidos Fundamentos (`pt.f0.*`). Aquí **la cercanía con el español no cuenta**: «ótimo» o «difícil» también se enseñan.
- **pt-BR neutro, ortografía posterior al Acuerdo.** `você` por defecto; `a gente` en lenguaje informal; `o senhor / a senhora` con mayores. Léxico: ônibus (no autocarro), celular (no telemóvel), café da manhã (no pequeno-almoço), geladeira, banheiro, trem/metrô, time (equipo), moça/moço, xícara, suco, sorvete, gerente. Sin gerundio con «estar a + infinitivo» (pt-PT): se dice «estou falando». Sin trema (frequente, linguiça) y sin los acentos que el Acuerdo eliminó («ideia», «europeia», «voo»). Preposición con país y ciudad según la ficha. No se imita el acento de Río ni de São Paulo; el regionalismo pernambucano solo como glosa.
- **Falsos amigos (obligatorio).** Cuando una palabra de la clase se parezca a una española con otro sentido, la explicación lo marca con ⚠ («falso amigo») y el contraste. Mínimo, y siempre que aparezcan: **esquisito** (raro) ≠ exquisito (delicioso = *delicioso, ótimo*), **polvo** (pulpo) ≠ polvo (*pó*), **grávida** (embarazada) ≠ embarazada (*grávida*; «embaraçada» = avergonzada/enredada), **oficina** (taller) ≠ oficina (*escritório*), **ninguém** (nadie; ≠ ninguno), **apelido** (apodo) ≠ apellido (*sobrenome*), **salada/salado** (ensalada; salado = *salgado*), **largo** (ancho) ≠ largo (*comprido*), **pegar** (agarrar, tomar [ônibus]) ≠ pegar (golpear), **rato** (ratón) ≠ rato (momento), **vaso** (jarrón; ≠ vaso = *copo*), **cena** (escena/cena = *jantar*), **abrigo** (refugio; abrigo de ropa = *casaco*), **cola** (pegamento; ≠ fila = *fila*). Los falsos amigos nuevos que inventes van en el informe. Los pares de `relacionar` y los ítems de falsos amigos nunca incluyen una opción que también sea defendible.
- **Una sola respuesta** por ítem; si dos formas valen (você/a gente, con y sin pronombre sujeto, «ônibus»/«busão»), la consigna fija cuál o `aceptadas` incluye todas. Sujeto omitido, femenino/masculino y órdenes naturales en `ordenar` van en `aceptadas`. El validador tolera la falta de tilde y avisa; no exijas ni evalúes solo por la tilde, salvo en las clases de diacríticos.
- **Hablantes:** el nombre del personaje del reparto o su papel en portugués («Garçom», «Vendedora», «Recepcionista»). Nunca el papel en español.
- **Canon.** Lee `personajes` y `hechosDelReparto` de N1 y el nivel. **Camila Ortega es la protagonista** (estadounidense de Miami, hija de colombianos, vive en Recife); los personajes secundarios de las fichas (Luana, Valentina, Rafael, Carolina…) pueden quedarse. **Nunca Ecuador, Quito, Guayaquil, Cuenca ni «equatoriano»**; otras nacionalidades están bien. Solo hechos reales de Recife/Pernambuco (lista de `MAPA.md`); sin inventar líneas de metro, hospitales ni bancos. En el informe lista los hechos nuevos que inventes (`- es / en`) para que el revisor los confirme.
- **Opciones de comprensión** en portugués desde N3 (en N1–N2 pueden ir en español). No se pasan opciones al español para esquivar palabras no enseñadas: se enseña la palabra o se reformula.
- **Tablas de lectura** («Para ler: …»): como máximo 15 filas, palabra + sentido + frase; los nombres propios no llevan fila. Si hacen falta más, la situación se reescribe con palabras ya enseñadas.
- **Un solo hueco** por `completar` (la app escribe la respuesta en todos los `___`).
- **Producción abierta:** en un `escribir` con `abierta: true`, el modelo tiene al menos `minimoPalabras` palabras.
- **Audio:** frases naturales de pt-BR; nada de texto que sonaría distinto leído en voz alta (sin «_», «→» ni símbolos). Los números y monedas (R$ 6,50) se leen completos.

## Validación

```bash
python3 tools/curriculo/validar_plan.py pt              # fichas y MAPA.md (0 errores)
python3 tools/curriculo/validar_plan_detallado.py pt    # plan de ejercicios (0 errores)
python3 tools/curriculo/validar_bloque.py pt N B        # tu bloque, encadenado con los borradores previos no integrados
```

0 errores del bloque. Si un borrador anterior ya está en `assets/contenido/pt/ruta/`, quítalo de la cadena (daría «id duplicado»). El revisor (distinto del autor) deja `revision-nX-bYY.md` con GO o REVISE, con «## Hechos del reparto confirmados» y «## Sin resolver», y comprueba: corrección del portugués de Brasil, progresión, claridad en español **y** en inglés, falsos amigos marcados y una sola respuesta defendible por ítem.

## Calibración (se completa con cada revisión)

1. Antes del primer bloque: confirmar con la voz elegida que las nasales, «lh», «nh» y las vocales abiertas/cerradas suenan según las guías.
2. Las fichas heredan nombres de ejemplo antiguos (Quito y Camila ya se limpiaron); si ves otro choque con el reparto, el reparto manda y lo anotas en «Sin resolver».
