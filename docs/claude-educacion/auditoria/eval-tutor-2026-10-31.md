# Evaluación del tutor de videollamada frente a un buen profesor particular (31-10-2026)

**Qué se midió.** 45 turnos de videollamada (`tutorId` avatar_*), cada uno con un historial de 2 a 6 turnos, el último mensaje del alumno y lo que haría un buen profesor particular.

- **Idiomas.** 24 escenarios de inglés para hispanohablantes, 6 de francés, 6 de alemán, 3 de portugués, 3 de japonés y 3 de español para anglohablantes.
- **Niveles.** 1, 3 y 6.
- **Categorías.** Las 12 del encargo, cada una con 3 a 6 casos.
- **Juez.** gpt-6-sol (`reasoning_effort` medium) evalúa cada turno con siete criterios binarios y una nota global de 1 a 5.

**Herramientas.**

- `tools/pruebas/eval_tutor/escenarios.json`: el banco de escenarios.
- `tools/pruebas/eval_tutor/evaluar.mts`: ejecuta la evaluación.
- `tools/pruebas/eval_tutor/resumir.mts`: genera las tablas.
- `tools/pruebas/eval_tutor/resultados/*.json`: respuestas, latencias, tokens y juicios.
- `tools/pruebas/eval_tutor/cache/`: guarda las respuestas del corrector y del juez para no repetir llamadas.

```bash
cd backend
npx tsx ../tools/pruebas/eval_tutor/evaluar.mts --modelo gpt-4.1-mini --salida ../tools/pruebas/eval_tutor/resultados/gpt-4.1-mini.json
npx tsx ../tools/pruebas/eval_tutor/evaluar.mts --modelo gpt-5.6-luna --esfuerzo none --salida ../tools/pruebas/eval_tutor/resultados/gpt-5.6-luna-none.json
npx tsx ../tools/pruebas/eval_tutor/resumir.mts ../tools/pruebas/eval_tutor/resultados/*.json --peores 8 --detalle
```

**Cómo se llama al tutor.** `responder()` corre en streaming (`onReply` + `signal` + `onFrase`), igual que `routes/chat.ts`, con el reintento único del route y un plazo de 45 s.

- Los escenarios se ejecutan de uno en uno, para que la latencia sea la de un turno real.
- El contexto es sintético y tiene la forma de `contextoSituacion()` para una conversación libre.
- `YA CORREGIDO` se genera con `correccionesPrevias()`, como en producción.
- El corrector (`corregirUltimo`, gpt-5.6-luna) se mide aparte. Su entrada no depende del modelo del tutor, así que se llamó una vez por escenario y sus respuestas y latencias se reutilizaron para los demás modelos.

**Cambios en producción.** No se tocó `lib/ia.ts`, `lib/ia_openai.ts` ni nada de producción. El modelo del tutor se elige con `OPENAI_MODELO`, que el script fija antes de cargar `config`.

**Presupuesto.** Se hicieron 554 llamadas a la API, con un coste aproximado de 2,13 US$:

| Uso | US$ |
|---|---|
| Juez | 1,85 |
| Tutor | 0,27 |
| Corrector | 0,02 |

## Hallazgo técnico previo: el streaming no admite modelos de razonamiento

`generarTutorStream` (`lib/ia_openai.ts`) fija `temperature: 0.7, max_tokens: 700`. Si `OPENAI_MODELO=gpt-5.6-luna` en producción, cada turno de videollamada falla:

> `400 Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.`

La evaluación evita el problema solo en su propio proceso: un envoltorio de `fetch` cambia esos parámetros por `reasoning_effort` y `max_completion_tokens`.

- gpt-5.6-luna y gpt-5.4-mini aceptan `reasoning_effort` `none` y `low`.
- Rechazan `minimal` con un 400.

Para usar uno de ellos como tutor hace falta este cambio mínimo y retrocompatible. **No está aplicado.** Copia la condición que ya usa `pedirJsonOpenAI`:

```ts
// generarTutorStream, en el body:
model: config.openaiModelo,
...(/^(gpt-5|gpt-6|o\d)/.test(config.openaiModelo)
  ? { reasoning_effort: process.env.OPENAI_ESFUERZO_TUTOR ?? 'none', max_completion_tokens: 3000 }
  : { temperature: 0.7, max_tokens: 700 }),
```

Con gpt-4.1-mini el cuerpo de la petición queda idéntico al actual.

## Resultados por modelo

Criterios (porcentaje de casos donde aplica y se cumple):

- **a.** Trata bien el error que importa y no inventa errores.
- **b.** La forma correcta dicha es correcta y mínima.
- **c.** Hace el movimiento pedagógico de la categoría.
- **d.** Se ajusta al nivel.
- **e.** Suena humano y conversa.
- **f.** Usa el idioma correcto.
- **tarjeta.** Las correcciones escritas son correctas. Las genera el corrector y son las mismas para todos los modelos.

Latencias en ms medidas desde la llamada:

- **1.ª frase:** el momento en que arranca la voz.
- **fin tutor:** el final del stream.
- **total:** max(tutor, corrector), que es cuando la app recibe el evento `final` con la tarjeta y las sugerencias.

### Calidad

| Modelo del tutor | Nota media (1-5) | a | b | c | d | e | f | tarjeta |
|---|---|---|---|---|---|---|---|---|
| **gpt-4.1-mini (actual)**, ejecución 1 | 2,89 | 76 % | 92 % | 27 % | 51 % | 47 % | 96 % | 91 % |
| gpt-4.1-mini (actual), ejecución 2 | 3,07 | 78 % | 94 % | 27 % | 53 % | 51 % | 98 % | 91 % |
| *gpt-4.1-mini, ambas ejecuciones juntas (90 turnos)* | *2,98* | *77 %* | *93 %* | *27 %* | *52 %* | *49 %* | *97 %* | *91 %* |
| gpt-5.4-mini (`none`) | 2,98 | 76 % | 83 % | 27 % | 73 % | 53 % | 100 % | 91 % |
| **gpt-5.6-luna (`none`)** | **3,40** | 87 % | 94 % | 42 % | 60 % | 76 % | 98 % | 91 % |
| gpt-5.6-luna (`low`) | 3,64 | 87 % | 91 % | 53 % | 67 % | 80 % | 98 % | 91 % |

### Latencia y coste

| Modelo del tutor | 1.ª frase p50 / p90 | Fin tutor p50 / p90 | Total p50 / p90 | US$ tutor/turno | Tokens de entrada / salida |
|---|---|---|---|---|---|
| **gpt-4.1-mini (actual)**, ejecución 1 | 646 / 935 | 1596 / 2093 | 2116 / 3019 | 0,0013 (0,0017 sin caché) | 3545 / 159 |
| gpt-4.1-mini (actual), ejecución 2 | 573 / 836 | 1456 / 1986 | 2220 / 3019 | 0,0007 (0,0017 sin caché) | 3545 / 155 |
| *gpt-4.1-mini, ambas ejecuciones juntas (90 turnos)* | *617 / 865* | *1514 / 2008* | | | |
| gpt-5.4-mini (`none`) | 735 / 898 | 1342 / 1766 | 2116 / 3019 | 0,0027 (0,0034) | 3546 / 152 |
| **gpt-5.6-luna (`none`)** | **791 / 978** | 1755 / 2282 | 2238 / 3019 | **0,0007 (0,0009)** | 3546 / 146 |
| gpt-5.6-luna (`low`) | 1391 / 2272 | 2507 / 3330 | 2848 / 3596 | 0,0007 (0,0010) | 3546 / 198 (48 de razonamiento) |

**Corrector** (`corregirUltimo`, gpt-5.6-luna con `reasoning_effort` low): p50 2116 ms, p90 3019 ms y máximo 31 928 ms (B04, japonés, «えっと…わかりません。»). Cuesta unos 0,00033 US$ por turno. Es más lento que la respuesta completa del tutor, así que marca la latencia total: retrasa la tarjeta, las sugerencias y el guardado del turno, pero no la voz.

**Coste por turno.** Con gpt-4.1-mini, unos 0,0013 + 0,0003 US$ por turno (tutor + corrector). Con gpt-5.6-luna (`none`), unos 0,0007 + 0,0003 US$: la mitad en el tutor. El caché de prompts cubrió entre el 29 % y el 95 % de la entrada, según la ejecución. La cifra «sin caché» es el techo.

**Robustez.**

- En la primera pasada, gpt-4.1-mini dejó dos turnos de 45 (X02 y A03) con la respuesta normal en `delta.refusal` («Respuesta rechazada: Nice»). Producción lo reintenta una vez, lo que añade de 1 a 2 s a esos turnos. Con gpt-5.6-luna ocurrió 0 veces en 135 turnos.
- gpt-5.6-luna (`low`) agotó una vez el plazo de 45 s (X02) y salió bien al repetirlo.

**Fiabilidad de la medida.**

- Al volver a juzgar los mismos 45 turnos, la nota coincidió en el 82 % de los casos y difirió como mucho en 1 punto en el 98 %. Los criterios coincidieron entre el 91 % y el 100 %. La media se movió 0,11.
- Dos ejecuciones del tutor actual (temperatura 0,7) dieron 2,89 y 3,07.
- Por tanto, una diferencia de menos de unos 0,2 en la media es ruido:
  - gpt-5.6-luna mejora de forma clara: +0,42 con `none` y +0,66 con `low` frente a la media de 2,98.
  - gpt-5.4-mini no mejora.
- Por categoría hay de 3 a 6 casos, así que esas cifras son orientativas.

### Nota media y movimiento pedagógico (c) por categoría

| Categoría (n) | 4.1-mini ej. 1 | 4.1-mini ej. 2 | 5.4-mini none | 5.6-luna none | 5.6-luna low |
|---|---|---|---|---|---|
| error_claro (6) | 3,50 · 33 % | 3,50 · 17 % | 4,17 · 50 % | 4,00 · 50 % | 4,50 · 83 % |
| correcta (5) | 2,80 · 60 % | 3,40 · 60 % | 3,20 · 80 % | 4,20 · 100 % | 4,80 · 100 % |
| error_menor (3) | 2,00 · 0 % | 2,00 · 0 % | 2,00 · 0 % | 2,33 · 0 % | 2,67 · 0 % |
| repite_bien (3) | 3,33 · 67 % | 4,00 · 67 % | 4,00 · 33 % | 5,00 · 100 % | 4,67 · 100 % |
| vuelve_a_fallar (3) | 2,67 · 0 % | 3,00 · 0 % | 2,33 · 0 % | 2,67 · 0 % | 2,33 · 0 % |
| error_repetido (4) | 3,25 · 25 % | 2,75 · 25 % | 3,00 · 25 % | 2,75 · 0 % | 2,75 · 0 % |
| autocorreccion (3) | 2,00 · 0 % | 2,00 · 0 % | 2,33 · 0 % | 3,00 · 33 % | 4,00 · 67 % |
| por_que (4) | 2,75 · 25 % | 2,25 · 0 % | 2,75 · 0 % | 3,00 · 0 % | 3,75 · 50 % |
| como_se_dice (4) | 3,00 · 0 % | 3,50 · 25 % | 3,25 · 25 % | 3,50 · 25 % | 3,25 · 50 % |
| bloqueo (4) | 3,25 · 75 % | 3,75 · 75 % | 2,50 · 25 % | 3,75 · 100 % | 4,00 · 100 % |
| monosilabos (3) | 2,67 · 0 % | 3,00 · 33 % | 3,00 · 33 % | 3,00 · 33 % | 2,33 · 0 % |
| nivel_alto (3) | 2,67 · 0 % | 3,00 · 0 % | 2,00 · 0 % | 2,67 · 33 % | 3,33 · 33 % |

### Nota media por nivel

| Nivel | 4.1-mini ej. 1 | 4.1-mini ej. 2 | 5.4-mini none | 5.6-luna none | 5.6-luna low |
|---|---|---|---|---|---|
| 1 | 2,82 | 3,00 | 2,71 | 3,24 | 3,41 |
| 3 | 2,95 | 3,09 | 3,14 | 3,41 | 3,73 |
| 6 | 2,83 | 3,17 | 3,17 | 3,83 | 4,00 |

## Los 8 peores casos del tutor actual (gpt-4.1-mini)

1. **C02 · correcta · inglés N6 · nota 1.** La frase era correcta: «If I had more time, I would learn to play the guitar. My dad used to play it when I was a kid.»
   - Reply: «That's lovely! Just a small thing: we say "My dad used to play it when I was a kid," not "when I was a kid." Can you say the whole sentence?»
   - En la otra ejecución: «…we say "My dad used to play it" not "My dad used to play it it"».
   - El tutor inventa un error y cambia la pregunta de seguimiento por una repetición.
2. **C04 · correcta · alemán N6 · nota 2.** «Fast richtig! Es heißt: „weil ich vielleicht arbeiten muss", nicht „weil ich vielleicht muss arbeiten". Der Grund ist, dass bei „weil" das Verb am Satzende steht. Kannst du den ganzen Satz nochmal sagen?»
   - Atribuye al alumno un error que no cometió.
   - La tarjeta del corrector estaba vacía, que es lo correcto.
3. **A03 · autocorrección · inglés N3 · nota 2 en ambas ejecuciones.** El alumno dijo «She don't… doesn't like spicy food». Reply: «Oh, just a small thing: we say "She doesn't like" not "She don't like." Can you say the whole sentence?»
   - Le corrige lo que ya había arreglado él.
   - A01 y A02 fallan igual en las dos ejecuciones.
4. **M01 · error menor · inglés N3 · nota 2.** «Nice story! Just a small thing: we say "on the weekend," not "in the weekend." Because we use "on" with days or specific days. Can you say the whole sentence?»
   - Para la charla por un error menor.
   - No reacciona a la película del perro.
5. **P01 · por qué · inglés N1 · nota 2.** «Good question! We say "went" because it's the past of "go" and it's irregular. We don't add "-ed" like in regular verbs. For example, "I go" now, but "I went" yesterday. Can you say "I went to the cinema on Saturday"?»
   - Usa jerga en nivel 1 y cinco frases.
   - Le pide repetir una frase hecha en vez de que use la forma por su cuenta.
6. **B03 · bloqueo · español N3 · nota 2.** «No te preocupes, puedo ayudarte. ¿Quieres decir "I went hiking"? En español decimos "Fui de trekking" o "Hice senderismo". ¿Puedes repetirlo?»
   - Responde por él con una actividad inventada.
   - Mete inglés en la reply.
   - En la otra ejecución dio una pista correcta y sacó un 5.
7. **V01 · vuelve a fallar · inglés N1 · nota 2.** «Almost! We say "she works in a bank." Can you say it again?»
   - Repite la misma corrección y vuelve a pedir que la diga, lo que abre un tercer ciclo.
   - No lo dice despacio ni por partes, y no sigue adelante.
   - V02 y V03 hacen lo mismo.
8. **X02 · error repetido · inglés N3 · nota 3.** El turno anterior ya le corrigió «she works». Reply: «Ah, cool! Just a small thing: we say "drives" with an s, because it's he. Can you say the whole sentence?»
   - Le da la forma hecha en vez de preguntar «drive or drives?».
   - La reacción es genérica y no comenta nada sobre el taxi.

## Diagnóstico: patrones que fallan

Cifras del tutor actual sobre las dos ejecuciones (90 turnos), salvo que se indique otra cosa.

### 1. Corrige en voz alta errores menores y para la charla

Pasa en 6 de 6 turnos de `error_menor`, y también con los dos modelos candidatos (c = 0 % en todos).

El propio prompt invita a hacerlo. El ejemplo de corrección del bloque VIDEOLLAMADA empieza por «Just a small thing: we say «I went»…», así que el modelo asocia «cosa pequeña» con «corrección explícita + repetir». Ese molde aparece en casi todas las correcciones («Just a small thing», «Nur eine Kleinigkeit», «Só um detalhe»).

La regla «si el error es pequeño y no estorba, reformúlalo» llega tarde y sin ejemplo propio.

### 2. Corrige lo que el alumno ya arregló solo

Pasa en las 3 autocorrecciones de las dos ejecuciones. La regla está en CÓMO CORREGIR, pero no en el bloque VIDEOLLAMADA, que manda en este modo.

gpt-5.6-luna (`low`) es el único que la cumple siempre en voz.

La tarjeta también falla en A03: `depurarCorrecciones` no filtra «She don't… doesn't», porque busca «She doesn't» completo detrás y el alumno solo repitió «doesn't».

### 3. Se inventa errores en frases correctas

Pasa en 3 de 10 turnos (C02 dos veces y C04).

El corrector no se equivocó en ninguno de ellos. Las tarjetas de C02, C04, A01 y A02 estaban vacías, que es lo correcto.

Con gpt-5.6-luna, en `none` y en `low`, pasó 0 veces de 5.

### 4. No hace que se autocorrija cuando el error ya se trabajó

Lo hizo en 0 de 6 turnos (X01–X03, donde `cambio.tipo` es «palabra» y aplica la pregunta «¿X o Y?»). Con todos los modelos juntos, solo 1 vez de 15, y mal formulada: «Does your dad drive or drives a taxi?».

Hay dos causas:

- La regla de `correccionesPrevias` es abstracta: habla de «tipo de error» y de «cambio.tipo palabra». El modelo no ve que «I play» es el mismo caso que «I go».
- La regla choca con «(4) SIEMPRE … pídele que diga la frase completa».

Esa misma regla de opciones se dispara donde no toca: en `vuelve_a_fallar`, gpt-5.6-luna convierte el segundo intento en un examen de opciones («¿Dices «soy» o «tengo» veinte años?»).

### 5. Ante un segundo fallo, repite la misma corrección

`vuelve_a_fallar` cumple el 0 % con todos los modelos. El tutor actual repite la misma frase y vuelve a pedir que la diga. No la dice despacio ni por partes, y no sigue adelante.

El modelo no detecta que es el segundo intento, aunque el historial lo muestra.

### 6. Los turnos son largos para el nivel

La media es de unas 3 frases en N1, N3 y N6. `d_nivel` falla en 43 de 90 turnos, sobre todo por el número de frases.

Hay dos causas:

- El prompt se contradice: VIDEOLLAMADA dice «máximo 2 frases en niveles 1-4», y FORMA dice «1-3 frases».
- El molde de corrección (reacción + «we say X, not Y» + porqué + «Can you say…») ya ocupa 3 o 4 frases.

### 7. Usa jerga y da el porqué en niveles 1-2

- En P01 dice «irregular» y «regular verbs» en las dos ejecuciones. También lo hacen gpt-5.4-mini y gpt-5.6-luna (`low`).
- En E01 da el porqué en nivel 1 («for past actions»).

La regla de «sin jerga» solo cubre las correcciones, no las respuestas a «¿por qué?».

En P04 la regla en francés está mal generalizada: «pour les verbes de mouvement… on utilise être». En `por_que`, el tutor pide repetir una frase dada en vez de que el alumno use la forma en una frase propia.

### 8. Reacciones genéricas

`e_humano` falla en 46 de 90 turnos: «Fast richtig!», «Oh, cool!», «Good!», «Ah, entiendo»…

Con gpt-5.6-luna baja a 11 de 45 con `none` y a 9 de 45 con `low`. Es la mayor ventaja del modelo.

### 9. No sube el nivel cuando el alumno muestra más

`nivel_alto` cumple entre el 0 % y el 33 % con todos los modelos. Ante un alumno B2 en un curso N1, sigue con preguntas cerradas de principiante o cambia de tema.

El prompt fija el perfil del nivel configurado y no le dice que se adapte a lo que el alumno demuestra en el turno.

### 10. Ante monosílabos, no da un modelo de respuesta

En `monosilabos` hace una pregunta, a veces doble, pero no ofrece un comienzo de frase ni un modelo.

La tarjeta del corrector marca como errores respuestas elípticas válidas: «Home» → «At home» y «Center» → «downtown».

### 11. Lo que ya funciona razonablemente

- El idioma correcto (f): 97 %.
- La forma corregida cuando corrige (b): 93 %.
- Pedir repetir tras un error claro: 11 de 12.
- Las pistas ante un bloqueo: 75 %, con un fallo grave en B03.
- La tarjeta del corrector: 91 %.

## Recomendaciones priorizadas

### 1. Prompt de VIDEOLLAMADA (coste cero, mayor impacto en c y d)

1. **Corregir en voz alta solo los errores que importan.** Que el prompt nombre los tres casos: impide entender, es el objetivo de la sesión o se repite. Todo lo demás se reformula sin señalarlo.
   - Dar un ejemplo de reformulación: «Oh, on the weekend? What was the movie?».
   - Cambiar «Just a small thing» por una fórmula que no presente el error como «pequeño».
2. **Añadir la autocorrección al bloque VIDEOLLAMADA:** «si se corrige solo, celébralo ("You fixed it yourself!") y no corrijas nada».
3. **Una sola regla de longitud.** Proponemos:
   - N1-2: 2 frases cortas, más la petición de repetir si corrige.
   - N3-4: 2-3 frases.
   - N5 y más: 3 frases.
   - Quitar «1-3 frases» de FORMA.
   - El porqué hablado, solo desde N3.
4. **«¿Por qué?» en N1-2 sin términos gramaticales.**
   - Responder con un contraste («Today I go, yesterday I went») y pedirle una frase propia, no repetir una dada.
   - En francés, la lista de verbos con être («aller, venir, partir, arriver…»), no «verbes de mouvement».
5. **Reaccionar a un detalle concreto** de lo que dijo. Prohibir arrancar con un elogio genérico («Good!», «Fast richtig!»).
6. **Ajustar el nivel al alumno.** Si el último mensaje está claramente por encima del nivel configurado, subir un escalón: pregunta abierta de más profundidad y una expresión útil.
7. **Ante monosílabos**, dar un modelo o un comienzo de frase («You can say: I walked around the…»).

### 2. Estado del turno calculado por la app (sin latencia, arregla V, X, A y R)

Calcularlo de forma determinista, como ya hace `tipoCambio()`, e inyectarlo junto al último mensaje, como ya se hace con `recordatorio()`. Así el modelo no tiene que deducirlo:

- El tutor pidió repetir en el turno anterior:
  - Si el mensaje coincide (normalizado) con la forma correcta: *«repitió bien: celébralo citando la forma y vuelve al hilo»*.
  - Si no coincide: *«2.º intento fallido: di la forma despacio, por partes, y sigue con una pregunta; no pidas repetir otra vez»*.
- El mensaje contiene una reparación («X… Y», que la heurística de `depurarCorrecciones` ya reconoce): *«autocorrección: elógiala, no corrijas»*.
- Hay una corrección previa de `cambio.tipo` «palabra» y el mensaje no es un intento de repetición: dar la instrucción concreta con un ejemplo en el idioma de la llamada («si vuelve a usar presente por pasado, pregunta "I play or I played?"; no le des la forma ni pidas repetir»). Que sea una sola regla, sin el «SIEMPRE pide repetir» compitiendo con ella.
- Mensaje de dos palabras o menos, o «no sé / I don't know», o «¿cómo se dice…?»: la instrucción correspondiente de la categoría.

### 3. Modelo del tutor: gpt-5.6-luna con `reasoning_effort` `none`

Requiere el cambio mínimo de `generarTutorStream` descrito arriba.

Frente a gpt-4.1-mini:

- Nota +0,4.
- Cero falsos errores en frases correctas.
- e_humano: del 49 % al 76 %.
- Mitad de coste en el tutor.
- Sin el error de `refusal`.

El precio es unos +170 ms en la primera frase (p50 791 frente a 617 ms) y +110 ms en el p90.

`low` sube la nota otros 0,25 (autocorrecciones y porqués), pero añade ~0,8 s en el p50 y ~1,4 s en el p90 de la primera frase, y tuvo un plazo de 45 s agotado. No conviene para cada turno de voz. Podría usarse solo para estados concretos («¿por qué?»), si el estado del turno de la recomendación 2 decide el esfuerzo.

**Descartar gpt-5.4-mini:** no mejora (2,98), cuesta el doble que el actual y empeora la exactitud de la forma corregida (b: 83 %).

### 4. El corrector antes de hablar: no como puerta, sí como señal

Su veredicto es mejor que el del tutor: acertó en todos los casos donde el tutor se inventó un error o corrigió una autocorrección. Pero esperar a que termine retrasaría el comienzo de la voz de unos 0,6 s a unos 2,8 s en el p50 y más de 3,6 s en el p90, con colas de 30 s. Alternativas, por orden:

- **a.** Aplicar las recomendaciones 1 y 2, que eliminan la mayoría de los falsos errores sin esperar.
- **b.** Medir el corrector con `reasoning_effort` `none` y un prompt reducido a «¿hay un error que importe? → forma». Si su p90 baja de unos 700 ms, puede ir antes del tutor y decidirle el movimiento.
- **c.** «Reacción primero»: la primera frase (la reacción) sale en streaming de inmediato. La parte de corrección se genera con el veredicto del corrector, que llega mientras suena la primera frase. Cuesta una segunda llamada corta por turno con error.

Además:

- Poner al corrector un tope de unos 8 s, para que una cola (31,9 s en B04) no retrase la tarjeta, las sugerencias y el guardado.
- Añadirle una regla: una respuesta elíptica a una pregunta («Home», «Center») no es un error.
- Arreglar `depurarCorrecciones` para que filtre la autocorrección con sujeto («She don't… doesn't»): comparar la palabra que cambia, no el fragmento completo.

### 5. Volver a medir tras cada cambio

Repetir la evaluación tras cada cambio (unas 90 llamadas y 0,4 US$ por modelo). Considerar mejora solo lo que supere unos 0,2 de nota media o un cambio claro en c por categoría. Es buena idea ampliar el banco con casos de situaciones con objetivo (contexto real de `contextoSituacion`) y turnos de `aviso`.

**Límites de esta evaluación:**

- Mide turnos aislados con un contexto sintético, sin material de situación.
- Usa texto limpio, sin ruido de transcripción.
- El juez es un modelo, aunque su consistencia es alta, como se vio arriba.
- La voz y el avatar no se evalúan.

## Después de los cambios (31-10-2026, mismos 45 escenarios y juez)

| Versión | Nota media | a_errores | c_movimiento | e_humano | 1.ª frase p50/p90 (ms) |
|---|---|---|---|---|---|
| gpt-4.1-mini, prompt anterior (producción) | 2,89 | 76 % | 27 % | 47 % | 646 / 935 |
| gpt-4.1-mini, prompt nuevo (v2) | 3,29 | 93 % | 39 % | 60 % | 687 / 929 |
| gpt-5.6-luna `none`, prompt nuevo (v2) | 3,53 | 93 % | 49 % | 78 % | 874 / 1149 |
| gpt-5.6-luna `none`, prompt nuevo + estado del turno (v3) | 3,62 | 93 % | 47 % | 87 % | 867 / 1073 |

Cambios: jugadas A–F en la videollamada (autocorrección, repetición, error ya corregido, corregir, reformular, no corregir), sin jerga en niveles 1-2, longitud por nivel, reacción concreta, ajuste de nivel; `estadoTurno()` (repite su frase / segundo intento / monosílabos, sin IA); tutor `OPENAI_MODELO_TUTOR` = gpt-5.6-luna con `reasoning_effort` none en streaming; corrector con tope de 8 s, respuestas cortas válidas y autocorrecciones; `depurarCorrecciones` detecta «She don't… doesn't».
«vuelve_a_fallar» pasó de 0 % a 67 % de movimiento correcto (nota 2,33 → 4,00). Siguen flojos «error_repetido» (0 %: en la evaluación no llega el bloque YA CORREGIDO que producción sí arma desde la base) y «error_menor» (a veces aún lo señala). Diferencias < 0,2 en la media son ruido.

## Veredicto antes de hablar (01-11-2026)

**Problema.** En llamadas reales el tutor no corregía en voz alta: decidía solo y el corrector bueno llegaba después, cuando la voz ya había sonado (solo cambiaba la tarjeta escrita). Además, la jugada E reformulaba en silencio los errores «menores» y, tras una corrección, el turno siguiente nunca corregía.

**Cambio.**

- `veredictoRapido()`: el corrector en versión corta (gpt-5.6-luna, `reasoning_effort` none, sin análisis escrito, máximo 1 error). Sobre los 45 escenarios: p50 1,0 s, p90 1,3 s, y los mismos errores que el corrector completo (que tarda 1,8 s con `none` y 2,1 s con `low`).
- `hablarConVeredicto()`: el tutor arranca a la vez y sus frases esperan al veredicto (tope 1,5 s). Sin error, o si el tutor ya cita la forma buena entre comillas (`corrigeEnVoz`), sale su respuesta. Si se saltó el error, se descarta antes de sonar y se pide otra con el veredicto en `estadoTurno`.
- Política de la videollamada (decidida por el producto): todo error real se corrige en voz alta, con la forma buena, el porqué en palabras fáciles (en N1-2 con un contraste, sin jerga) y la petición de decir la frase completa. Si la repetición falla, por partes y un intento más; al segundo fallo, la frase bien y seguir. Ya no hay «error menor» reformulado en silencio, así que la categoría `error_menor` del banco espera ahora corrección en voz.

**Resultado (sin juez, `resultados/v5-veredicto-gpt-5.6-luna-none.json`).** Los 16 turnos con error del banco se corrigen en voz alta con porqué y petición de repetir; las 5 frases correctas, las 3 repeticiones bien hechas y las 3 autocorrecciones no reciben corrección.

| Versión | 1.ª frase p50 / p90 (ms) | Total p50 / p90 (ms) |
|---|---|---|
| v3 (producción hasta hoy) | 867 / 1073 | 2245 / 3240 |
| Esperar siempre al veredicto | 2120 / 2517 | 3172 / 3964 |
| v5: tutor en paralelo + veredicto | 1213 / 1964 | 2298 / 3598 |

## Expectativa explícita (02-11-2026)

**Problema.** `estadoTurno()` adivinaba si el alumno estaba repitiendo comparando su frase con la anterior suya (≥ 60 % de palabras en común y al menos 3). Fallaba en tres casos:
- una repetición parcial («I went to the park» tras pedir la frase entera con «with my sister»);
- una respuesta a una pregunta abierta parecida a lo que ya dijo («I like pizza a lot» → «I like pizza with cheese and ham a lot»): se tomaba por repetición y el tutor la celebraba como corrección;
- una opción elegida en una palabra («Ate.»): contaba como «respuestas muy cortas».

**Cambio.** El tutor declara en cada turno qué espera (`espera`, justo después de `reply` en el JSON):
- `repetir`, con la frase exacta en `modelo`;
- `elegir`, con las opciones en `modelo`, separadas por « / »;
- `responder`.

El servidor la manda en el evento SSE `espera` en cuanto el tutor termina, sin esperar al corrector. La página la guarda en el turno del tutor y la devuelve en el historial. `estadoTurno()` la usa así:
- **`repetir`:** compara con la frase pedida, cuenta los intentos por las veces que el tutor pidió la misma frase, y si el alumno siguió con otra cosa avisa de no insistir.
- **`elegir`:** acepta una respuesta corta y celebra la opción.
- **`responder`:** nunca la trata como repetición.
- **Sin `espera`** (clientes viejos o aviso sin ella): la heurística de antes.

**Resultado (sin juez).** En `resultados/v6-espera-b.json`, 29 escenarios: los 24 de antes más 5 nuevos (Q01–Q05, categoría «expectativa»).
- El tutor declaró la expectativa correcta en los 29: `repetir` con la frase en cada corrección, `elegir` en «¿X o Y?» y `responder` en las preguntas abiertas.
- Q01 celebra la repetición parcial.
- Q02 conversa, sin «Perfect».
- Q03 celebra «ate».
- Q04 responde a su pregunta, sin insistir.
- Q05 (segundo fallo) dice la frase bien y sigue.
- Los 24 de antes, sin cambios de conducta.

Latencia en los mismos 24 escenarios:

| Versión | 1.ª frase p50 / p90 (ms) | Total p50 / p90 (ms) |
|---|---|---|
| v5 | 1233 / 1716 | 2248 / 3240 |
| v6, corrida 1 | 1285 / 2165 | 2450 / 3932 |
| v6, corrida 2 | 1453 / 1636 | 2610 / 3383 |

La primera frase no espera al campo nuevo (va después de `reply`); la diferencia está dentro del ruido de la API. El final del JSON se alarga ~15 tokens.
