# Prueba de los tutores de la videollamada · 2026-11-11-indicaciones2

4 llamadas simuladas (alumno de IA, 5 turnos, un silencio a mitad de llamada), prompt y `responder` reales, voz real en las 0 primeras respuestas y evaluación con la rúbrica de `lib/informe_llamada.ts` (la misma de las llamadas reales).

**Nota media:** 8.1/10 · habla 4 · ensena 4.3 · correcciones 3.5 · apoyo 4 · tema 4.5 · escucha 4.5 (de 1 a 5).

| Tutor | Idioma | Nivel | Explica | Nota | habla | ensena | correcciones | apoyo | tema | escucha | Voz | Respaldo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Julia | fr | N2 | nativo | 7.8 | 4 | 4 | 3 | 5 | 5 | 3 | ? | 0/0 |
| Tomas | it | N2 | nativo | 9.3 | 4 | 5 | 5 | 4 | 5 | 5 | ? | 0/0 |
| Hana | ja | N1 | nativo | 7.4 | 4 | 4 | 3 | 3 | 4 | 5 | ? | 0/0 |
| Lucas | ko | N2 | nativo | 7.8 | 4 | 4 | 3 | 4 | 4 | 5 | ? | 0/0 |

**Voces:** 0 frases sintetizadas, 0 con la voz de respaldo, 0 con error. Latencia media 0 ms.

## Julia · fr N2 · explica nativo · 7.8/10

**Bien:** Ofreció dos temas y dejó que el alumno eligiera. · Trabajó vocabulario y artículos concretos: «une pomme» y «de l’eau». · Pidió repetir frases completas y comprobó su producción.

**Problemas:**
- (escucha) ««Oui, “Je veux parler de la nourriture” !»» → Como solo hubo ruido y no una respuesta comprensible, debía decir: «Je n’ai pas compris. Tu peux répéter, s’il te plaît ?»
- (correcciones) ««On dit : “Je veux parler de la nourriture, s’il te plaît.”»» → Debía corregir primero la frase producida: «Je veux de la nourriture, s’il te plaît.»; después podía enseñar «parler de» como expresión opcional.

**Alumno:** Nivel 2 real: puede producir «Je veux...» y repetir frases breves con apoyo, pero aún depende de modelos. Dificultades: Omite artículos y partitivos: «Je veux pomme», «Je veux eau».; Le cuesta construir frases para expresar lo que quiere.; Necesita apoyo para distinguir «une», «de la» y «de l’eau»..

**Recomendación:** Mantén preguntas muy breves y corrige un solo elemento cada vez, verificando primero cualquier respuesta que no se entienda.

<details><summary>Transcripción</summary>

- **T:** Bonjour ! Aujourd’hui, on pratique « Je veux… ». Tu choisis : ta journée ou la nourriture ? [Elige un tema: tu día o la comida.]
- **A:** Je veux nourriture, s'il plaît.
- **T:** Oui ! On dit : « Je veux parler de la nourriture, s’il te plaît. » Répète la phrase complète ! [Para hablar de un tema, usamos « parler de ». Repite la frase completa.]
- *(silencio: ruido: el alumno no dijo «la de», fue ruido de fondo transcrito)*
- **A:** la de
- **T:** Oui, « Je veux parler de la nourriture » ! Qu’est-ce que tu veux manger ?
- **A:** Je veux pomme.
- **T:** Avec « une » : « Je veux une pomme. » Aujourd’hui, je veux aussi une pomme bien croquante. À toi ! [En francés, « pomme » necesita « une ». Repite la frase completa.]
- *(silencio: iniciativa)*
- **T:** Je veux… une pomme. À toi ! [Repite la frase completa: «Je veux une pomme».]
- **A:** Je veux une pomme.
- **T:** Bravo, « Je veux une pomme » ! Pour boire, tu veux quoi ?
- **A:** Je veux eau.
- **T:** Très bien : « Je veux de l’eau. » Avec l’eau, on dit « de l’eau ». Répète la phrase complète ! [Con « eau», usamos « de l’eau». Repite la frase completa.]
- **A:** Je veux de l’eau.
- **T:** Parfait, « Je veux de l’eau » ! Après la pomme, tu veux du pain ou du fromage ?

</details>

## Tomas · it N2 · explica nativo · 9.3/10

**Bien:** Ofreció dos temas y siguió la elección del alumno: el cibo. · Pidió repetir cuando la entrada no se entendió, sin inventar una respuesta. · Enseñó y practicó «mi piace», además de explicar «gusto» y corregir el artículo y el orden de la frase.

**Problemas:**
- (habla) ««Quale gusto di gelato preferisci?»» → Podría decir «Quale gelato preferisci?» o acompañarlo de una ayuda breve, porque «gusto» puede ser difícil para este nivel.

**Alumno:** Nivel inicial real, aproximadamente 2/10: produce frases básicas memorizadas y necesita apoyo para entender vocabulario y construir una frase nueva. Dificultades: No entendió «gusto» y pidió aclaración.; Omitió el artículo en «Mi piace cioccolato».; Necesita apoyo para colocar correctamente «molto» en la frase..

**Recomendación:** Mantén preguntas muy breves y ofrece opciones o modelos antes de pedir frases nuevas, corrigiendo solo un elemento cada vez.

<details><summary>Transcripción</summary>

- **T:** Ciao! Oggi pratichiamo «Mi piace…». Preferisci parlare della tua giornata o del cibo? [Scegli un tema: la tua giornata o il cibo.]
- **A:** Cibo, per favore.
- **T:** Io amo la pizza. E tu, che cosa ti piace? [Rispondi con «Mi piace…» e un cibo.]
- *(silencio: ruido: el alumno no dijo «la de», fue ruido de fondo transcrito)*
- **A:** la de
- **T:** Scusa, non ho capito. Puoi ripetere? [Repite tu respuesta, por favor.]
- **A:** Mi piace la pasta.
- **T:** Sì, «mi piace la pasta»! A me piace la pasta al pomodoro. Ti piace il gelato?
- *(silencio: iniciativa)*
- **T:** Ti piace il gelato? Sì o no? [Rispondi: «Sì, mi piace» oppure «No, non mi piace».]
- **A:** Sì, mi piace.
- **T:** Bene, «sì, mi piace»! Quale gusto di gelato preferisci?
- **A:** No capisco, che gusto?
- **T:** Hai detto bene: «Mi piace la pasta» e «Sì, mi piace». «Gusto» significa sapore: vaniglia o cioccolato?
- **A:** Mi piace cioccolato, molto.
- **T:** Quasi! Si dice: «Mi piace molto il cioccolato». «Il» va davanti a «cioccolato». Tocca a te: ripeti tutta la frase! [En italiano se dice «il cioccolato», porque aquí el nombre necesita artículo. Repite la frase completa.]

</details>

## Hana · ja N1 · explica nativo · 7.4/10

**Bien:** Pidió elegir entre dos temas y mantuvo una actividad adecuada para nivel inicial. · Modeló «パンが好きです» y consiguió que el alumno la repitiera correctamente. · Ante el ruido, pidió repetir de forma natural sin inventar lo que había dicho.

**Problemas:**
- (apoyo) «[«パンが好きです» significa «me gusta el pan». Repite la frase completa.]» → [Repite la frase completa.] La traducción no era necesaria: el alumno ve los subtítulos y puede consultar la traducción.
- (apoyo) «[「パンが好きです」と「朝、パンを食べます」を使えました。次は、朝の飲み物を一つ言ってください。]» → [Di una bebida que tomes por la mañana.] Es más breve y evita traducir o resumir lo que el alumno ya dijo.
- (correcciones) «パンが好きです。朝、パンを食べますね。» → パンが好きです。朝、パンを食べます。 La forma del alumno «朝パン食べます» necesitaba una corrección explícita y un modelo claro, no solo una reformulación.

**Alumno:** Nivel 1 real: entiende y produce frases muy básicas con apoyo, pero todavía mezcla español y japonés. Dificultades: No comprendió inicialmente 食べ物 y necesitó la explicación en español.; Necesita apoyo para formar frases completas y usar partículas como が y を.; Todavía depende de la repetición del modelo para responder en japonés..

**Recomendación:** Mantén frases japonesas muy breves, corrige explícitamente una sola partícula por turno y reduce las traducciones en español a indicaciones indispensables.

<details><summary>Transcripción</summary>

- **T:** こんにちは！今日は「わたしは〜です」を練習します。食べ物ですか、毎日のことですか？ [«わたしは〜です» significa «yo soy…»; elige un tema.]
- **A:** ¿食べ物 es comida? Yo no entiendo bien.
- **T:** はい、「食べ物」は comida です。食べ物について、何が好きですか？ [«たべもの» significa «comida». Responde con una comida que te guste.]
- *(silencio: ruido: el alumno no dijo «la de», fue ruido de fondo transcrito)*
- **A:** la de
- **T:** すみません、もう一度お願いします。何が好きですか？ [もう一度、好きな食べ物を言ってください。]
- **A:** Me gusta pan.
- **T:** パンが好きです。言ってみてください！ [«パンが好きです» significa «me gusta el pan». Repite la frase completa.]
- *(silencio: iniciativa)*
- **T:** パンが……好きです。もう一度、言ってみてください！
- **A:** パンが好きです
- **T:** はい、「パンが好きです」、上手です。朝、パンを食べますか？ [«パンが好きです»を上手に言えました。朝にパンを食べるか、答えてください。]
- **A:** Sí, 朝パン食べます。
- **T:** パンが好きです。朝、パンを食べますね。飲み物は何ですか？ [「パンが好きです」と「朝、パンを食べます」を使えました。次は、朝の飲み物を一つ言ってください。]
- **A:** コーヒーを飲みます。
- **T:** コーヒーを飲みます、上手です。昼は何を食べますか？

</details>

## Lucas · ko N2 · explica nativo · 7.8/10

**Bien:** Ofreció una elección sencilla y adecuada al nivel: comida o rutina diaria. · Hizo que el alumno produjera varias veces la estructura «저는 … 좋아해요». · Ante el ruido, pidió repetir con naturalidad sin inventar lo que el alumno quiso decir.

**Problemas:**
- (correcciones) «음식 뒤에는 «를»을 써요.» → 저는 피자를 좋아해요에서 «피자»에는 목적격 조사 «를»을 붙여요. 받침이 있으면 «을»을 써요: 음식을 좋아해요.
- (correcciones) «친구 뒤에는 «는», 음식 뒤에는 «를»을 써요. 다시 말해 보세요!» → 한 번에 하나만 교정하세요: «친구»에는 «는»을 붙여요. 먼저 «친구는 피자 좋아해요?»라고 말해 보세요.
- (ensena) «저는 피자를 좋아해요. 음식 뒤에는 «를»을 써요.» → Añadir una explicación mínima del uso: «를/을» marca la comida que gusta, y después pedir una variación nueva, por ejemplo 햄버거를 좋아해요.

**Alumno:** Nivel 2 real: comprende y produce una frase básica memorizada con apoyo, pero todavía necesita guía para usar las partículas. Dificultades: Omitió inicialmente la partícula «를» en «저는 피자 좋아해요».; Confundió o no pudo producir «친구는 피자를 좋아해요» sin modelado.; Necesita practicar la diferencia entre «는» y «를/을» en frases completas..

**Recomendación:** Mantén frases breves y practica una sola partícula cada vez, variando los alimentos para comprobar que el alumno generaliza la estructura.

<details><summary>Transcripción</summary>

- **T:** 안녕하세요! 오늘은 “저는 … 좋아해요”를 연습해요. 음식이나 하루 중 하나를 골라 보세요. [«좋아해요» significa «me gusta». Elige: comida o tu día.]
- **A:** Comida 좋아해요.
- **T:** 좋아요! 저는 피자를 좋아해요. 어떤 음식을 좋아해요? [«어떤 음식» significa «qué comida». Di: «저는 … 좋아해요».]
- *(silencio: ruido: el alumno no dijo «la de», fue ruido de fondo transcrito)*
- **A:** la de
- **T:** 음? 다시 말해 주세요. 천천히 말해도 돼요.
- **A:** 저는 피자 좋아해요.
- **T:** 아주 좋아요! 저는 피자를 좋아해요. 음식 뒤에는 «를»을 써요. 다시 말해 보세요! [음식 뒤에는 «를»을 써요. 문장 전체를 다시 말해 보세요.]
- *(silencio: iniciativa)*
- **T:** 좋아요! 저는… 피자를… 좋아해요. 말해 보세요!
- **A:** 저는 피자를 좋아해요.
- **T:** 맞아요, «저는 피자를 좋아해요»! 친구는 어떤 음식을 좋아해요?
- **A:** 친구 피자 좋아해요?
- **T:** 좋아요! 저는 피자를 좋아해요. 친구는 피자를 좋아해요? 친구 뒤에는 «는», 음식 뒤에는 «를»을 써요. 다시 말해 보세요!
- **A:** 친구는 피자를 좋아해요.
- **T:** 맞아요, «친구는 피자를 좋아해요»! 햄버거도 좋아해요?

</details>
