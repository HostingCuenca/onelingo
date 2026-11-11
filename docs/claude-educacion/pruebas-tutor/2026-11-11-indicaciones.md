# Prueba de los tutores de la videollamada · 2026-11-11-indicaciones

8 llamadas simuladas (alumno de IA, 5 turnos, un silencio a mitad de llamada), prompt y `responder` reales, voz real en las 0 primeras respuestas y evaluación con la rúbrica de `lib/informe_llamada.ts` (la misma de las llamadas reales).

**Nota media:** 8.8/10 · habla 4.5 · ensena 4.3 · correcciones 4.3 · apoyo 4.4 · tema 4.8 · escucha 4.8 (de 1 a 5).

| Tutor | Idioma | Nivel | Explica | Nota | habla | ensena | correcciones | apoyo | tema | escucha | Voz | Respaldo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Chloe | en | N1 | nativo | 9.3 | 5 | 3 | 5 | 5 | 5 | 5 | ? | 0/0 |
| Julia | fr | N2 | nativo | 7.4 | 4 | 4 | 3 | 4 | 5 | 3 | ? | 0/0 |
| Nora | pt | N3 | nativo | 10 | 5 | 5 | 5 | 5 | 5 | 5 | ? | 0/0 |
| Tomas | it | N2 | nativo | 8.1 | 4 | 4 | 4 | 3 | 5 | 5 | ? | 0/0 |
| Hana | ja | N1 | nativo | 8.9 | 4 | 4 | 5 | 5 | 4 | 5 | ? | 0/0 |
| Lucas | ko | N2 | nativo | 7.4 | 4 | 4 | 2 | 3 | 5 | 5 | ? | 0/0 |
| Diego | ru | N2 | nativo | 9.6 | 5 | 5 | 5 | 5 | 4 | 5 | ? | 0/0 |
| Elena | es | N3 | nativo | 10 | 5 | 5 | 5 | 5 | 5 | 5 | ? | 0/0 |

**Voces:** 0 frases sintetizadas, 0 con la voz de respaldo, 0 con error. Latencia media 0 ms.

## Chloe · en N1 · explica nativo · 9.3/10

**Bien:** Ofreció dos temas sencillos y dejó que el alumno eligiera. · Usó preguntas breves, vocabulario básico y ejemplos concretos. · Cuando apareció ruido o una respuesta incomprensible, pidió repetir sin inventar lo que el alumno quería decir. 

**Problemas:**
- (ensena) «“Hi! Today: ‘I like…’ Choose: food or your day.”» → Después de que el alumno dijera “Pizza” o “Rice”, modelar y hacerle repetir: “I like pizza” / “I like rice”, para practicar realmente la estructura objetivo.
- (ensena) «“You like pizza and rice. What do you drink?”» → Añadir una producción breve del alumno: “I like pizza and rice. I drink water.”

**Alumno:** Nivel 1 real: comprende y produce palabras sueltas y algunas respuestas muy breves con apoyo. Dificultades: Aún no produce espontáneamente la estructura completa “I like…”.; Necesita apoyo para recordar o decir nombres de comidas en inglés.; Responde con palabras sueltas en vez de frases completas..

**Recomendación:** Mantén las preguntas cortas, pero haz que el alumno convierta cada palabra nueva en una frase modelo como “I like pizza” o “I drink water”.

<details><summary>Transcripción</summary>

- **T:** Hi! Today: “I like…” Choose: food or your day. [Elige un tema: comida o tu día.]
- **A:** I like food, yes.
- **T:** Yum! What food do you like? [Di un tipo de comida, por ejemplo: “pizza”.]
- *(silencio: ruido: el alumno no dijo «la de», fue ruido de fondo transcrito)*
- **A:** la de
- **T:** Hmm? Say the food again. [Di el nombre de una comida en inglés.]
- **A:** Pizza
- **T:** Pizza, good! Home or restaurant?
- *(silencio: iniciativa)*
- **T:** At home or at a restaurant? [Elige una: home o restaurant.]
- **A:** Home, por favor.
- **T:** Yes, “home, please.” What do you eat at home? [Di una comida en inglés, por ejemplo “pizza” o “rice”.]
- **A:** Rice.
- **T:** You like pizza and rice. What do you drink?
- **A:** Water, please.
- **T:** Cold or hot? [Elige una: cold o hot.]

</details>

## Julia · fr N2 · explica nativo · 7.4/10

**Bien:** Ofreció dos temas y dejó que el alumno eligiera. · Practicó «je veux» con frases concretas y pidió reutilizarlas. · Usó explicaciones breves en español y gradualmente hizo que el alumno produjera frases completas.

**Problemas:**
- (escucha) «Oui, « Je veux parler de la nourriture. » !» → El alumno solo produjo «la de» y había ruido; debía pedirle naturalmente: «Je n’ai pas compris. Répète, s’il te plaît.»
- (apoyo) «« La nourriture » veut dire food.» → Decir «la nourriture» significa «la comida»; introducir inglés no ayuda a este alumno hispanohablante.
- (correcciones) «Tu as bien utilisé « je veux manger ».» → El alumno dijo «Je veux boire agua»; mejor: «Très bien, tu as utilisé “je veux boire”. On dit: “Je veux boire de l’eau.”»
- (ensena) «En français, se dice « de la pizza » después de « manger ».» → Explicar brevemente: «On dit “de la pizza” pour parler d’une quantité non précise.»

**Alumno:** Nivel inicial 2/10: puede repetir estructuras modelo y expresar deseos básicos con bastante apoyo. Dificultades: Mezcla español y francés: «Je veux comida» y «Je veux boire agua».; Necesita apoyo para los artículos partitivos: «de la pizza» y «de l’eau».; Todavía requiere que el tutor modele y fragmente las frases para producirlas..

**Recomendación:** Mantén frases muy breves y un objetivo por turno, pero verifica siempre lo que el alumno dijo antes de corregirlo.

<details><summary>Transcripción</summary>

- **T:** Salut ! Aujourd’hui, on pratique « je veux ». Tu choisis : ta journée ou la nourriture ? [Elige un tema: tu día o la comida. « Je veux » significa «quiero».]
- **A:** Je veux comida.
- **T:** Oui ! On dit : « Je veux parler de la nourriture. » « La nourriture » veut dire food. À toi ! [« Comida » se dice « la nourriture » en francés. Repite la frase completa.]
- *(silencio: ruido: el alumno no dijo «la de», fue ruido de fondo transcrito)*
- **A:** la de
- **T:** Oui, « Je veux parler de la nourriture. » ! Qu’est-ce que tu veux manger ?
- **A:** Je veux manger pizza.
- **T:** Très bien ! On dit : « Je veux manger de la pizza. » À toi, dis toute la phrase ! [En francés, se dice « de la pizza » después de « manger ». Repite la frase completa.]
- *(silencio: iniciativa)*
- **T:** Je veux… manger… de la pizza. À toi ! [Repite la frase completa, despacio.]
- **A:** Je veux manger de la pizza.
- **T:** Parfait, « Je veux manger de la pizza » ! Et tu veux boire quoi ?
- **A:** Je veux boire agua.
- **T:** Tu as bien utilisé « je veux manger ». On dit : « Je veux boire de l’eau. » [En francés, « agua » se dice « de l’eau ». Repite la frase completa.]
- **A:** Je veux boire de l’eau.
- **T:** Oui, « Je veux boire de l’eau » ! Maintenant, quelle pizza tu veux ?

</details>

## Nora · pt N3 · explica nativo · 10/10

**Bien:** Presentó una estructura concreta («eu costumo…») y la hizo practicar en varias situaciones de la rutina. · Respondió claramente a la pregunta sobre «día» y dio una indicación breve en español. · Ante el ruido, pidió repetir sin inventar lo que el alumno había querido decir.

**Alumno:** Nivel 3 real: puede formar frases sencillas y conectar ideas básicas sobre su rutina con apoyo. Dificultades: Necesita confirmar vocabulario cotidiano como «dia».; Todavía practica el uso espontáneo de «costumo».; Está empezando a justificar opiniones con «porque»..

**Recomendación:** Continúa con una conversación breve sobre el fin de semana, corrigiendo solo los errores reales y dejando que el alumno elija entre varias actividades.

<details><summary>Transcripción</summary>

- **T:** Olá! Hoje vamos praticar «eu costumo…» para falar da sua rotina. Você prefere falar do seu dia ou do seu trabalho?
- **A:** Eu prefiro falar do meu dia. Como se diz "día" em português?
- **T:** «Día» se diz «dia», com a mesma palavra. Agora, diga uma frase: «Eu costumo…» O que você costuma fazer de manhã? [En portugués, «día» se dice «dia». Completa una frase sobre tu mañana.]
- *(silencio: ruido: el alumno no dijo «la de», fue ruido de fondo transcrito)*
- **A:** la de
- **T:** Hm? Pode repetir? O que você queria dizer?
- **A:** Eu costumo tomar café de manhã.
- **T:** Muito bem! «Eu costumo tomar café de manhã» está perfeito. E à tarde, o que você costuma fazer?
- *(silencio: iniciativa)*
- **T:** E à tarde, você costuma estudar ou descansar? Pode começar assim: «Eu costumo…»
- **A:** Eu costumo descansar à tarde.
- **T:** Você usou «costumo» muito bem para falar da rotina. À noite, você costuma sair ou ficar em casa?
- **A:** À noite eu costumo ficar em casa e ler um livro.
- **T:** Até agora, você usou «costumo» muito bem de manhã, à tarde e à noite. Agora, diga por que você gosta de ler à noite, usando «porque».
- **A:** Eu gosto de ler à noite porque é tranquilo e me ajuda a dormir.
- **T:** Que frase bonita e natural! Para continuar, fale do fim de semana: o que você costuma fazer no sábado e por quê?

</details>

## Tomas · it N2 · explica nativo · 8.1/10

**Bien:** Ofreció dos temas y siguió la elección implícita del alumno: el cibo. · Explicó vocabulario y practicó la frase «Mi piace il cibo» con repetición guiada. · Ante el ruido, pidió repetir sin inventar lo que el alumno había dicho.

**Problemas:**
- (apoyo) «[«Cibo» significa «comida». Repite la frase completa in italiano.]» → [Repite la frase completa en italiano.] La explicación del significado ya se había dado y repetirla corta la fluidez.
- (apoyo) «[Ripeti la frase completa: «Mi piace il cibo».]» → [Repite: «Mi piace il cibo».] Dar la frase completa otra vez es innecesariamente largo; la indicación puede ser más breve.
- (correcciones) «Ah, pizza! In italiano: «Mi piace la pizza».» → «Me gusta pizza» → «Mi piace la pizza». Repite la frase completa.

**Alumno:** Nivel 2 real: comprende y produce frases italianas muy breves con bastante apoyo, pero todavía responde a menudo en español. Dificultades: Necesita apoyo para recordar vocabulario básico como «cibo».; Le cuesta producir espontáneamente la estructura «Mi piace + artículo + sustantivo».; Todavía mezcla español e italiano al responder..

**Recomendación:** Mantén frases muy breves y haz que produzca una respuesta italiana completa en cada turno, reduciendo gradualmente las ayudas en español.

<details><summary>Transcripción</summary>

- **T:** Ciao! Oggi pratichiamo «Mi piace…». Parliamo del tuo giorno o del cibo? [Scegli una: il tuo giorno o il cibo.]
- **A:** Me gusta comida. ¿Qué es 'cibo'?
- **T:** «Cibo» significa comida. In italiano: «Mi piace il cibo». Quale cibo ti piace? [«Cibo» significa «comida». Repite la frase completa in italiano.]
- *(silencio: ruido: el alumno no dijo «la de», fue ruido de fondo transcrito)*
- **A:** la de
- **T:** Hm? Non ho capito. Puoi ripetere?
- **A:** No capisco, ¿puedes repetir?
- **T:** Certo. «Mi piace il cibo». Tocca a te! [Ripeti la frase completa.]
- *(silencio: iniciativa)*
- **T:** Certo. «Mi piace… il cibo». Tocca a te! [Ripeti la frase completa: «Mi piace il cibo».]
- **A:** Mi piace il cibo
- **T:** Eccola: «Mi piace il cibo»! Ti piace cucinare? [Rispondi con «Sì» o «No».]
- **A:** No, no me gusta cocinar.
- **T:** Finora: «Mi piace il cibo», ma non ti piace cucinare. Ti piace mangiare la pasta o la pizza? [Scegli: la pasta o la pizza.]
- **A:** Me gusta pizza
- **T:** Ah, pizza! In italiano: «Mi piace la pizza». Tocca a te! [In italiano usiamo «la» prima di «pizza». Di la frase completa.]

</details>

## Hana · ja N1 · explica nativo · 8.9/10

**Bien:** Pidió repetir cuando hubo ruido, sin inventar lo que el alumno había dicho. · Corrigió correctamente «わたしはパンです» a «パンを食べます» y pidió practicar la oración completa. · Usó indicaciones breves en español y mantuvo la mayor parte de la interacción en japonés.

**Problemas:**
- (tema) «食べ物について、一文お願いします。何を食べますか？» → Como el alumno no eligió claramente entre trabajo y comida, preguntar: 「仕事ですか、食べ物ですか？」 y esperar su elección.
- (ensena) «すしの何が好きですか？» → Para este nivel, introducir primero una respuesta sencilla y explicarla: 「すしが好きですか？」 o modelar 「たまごが好きです」 antes de pedir una estructura nueva.

**Alumno:** Nivel 1 real: puede producir frases memorizadas y usar 「を食べます／飲みます」 con apoyo y repetición. Dificultades: Confunde 「わたしは〜です」 con una frase para expresar qué alimento come.; Necesita apoyo para formar frases completas y distinguir 「食べます」 de 「飲みます」.; Todavía no está preparado para responder espontáneamente a preguntas más abiertas como 「すしの何が好きですか？」..

**Recomendación:** Mantén frases muy sencillas, confirma la elección del tema y presenta una sola estructura nueva con un modelo antes de pedir producción.

<details><summary>Transcripción</summary>

- **T:** こんにちは！今日は「わたしは〜です」を練習します。テーマは、仕事ですか、食べ物ですか？ [「わたしは〜です」を使って、仕事か食べ物を選んでください。]
- **A:** わたしは学生です。仕事はわかりません。
- **T:** 学生です、いいですね！食べ物について、一文お願いします。何を食べますか？ [「わたしは〜です」は上手です。食べ物を一つ言ってください。]
- *(silencio: ruido: el alumno no dijo «la de», fue ruido de fondo transcrito)*
- **A:** la de
- **T:** すみません、もう一度お願いします。日本語で言ってください。
- **A:** わたしはパンです。
- **T:** パンを食べます。言ってみて！ [食べ物を言うときは、「パンです」ではなく「パンを食べます」と言います。文全体を言ってください。]
- *(silencio: iniciativa)*
- **T:** パンを食べます。パンを……食べます。言ってみて！ [「パンを食べます」と、文全体を言ってください。]
- **A:** パンを食べます。
- **T:** はい、「パンを食べます」、上手です！飲み物はお茶ですか、水ですか？ [お茶か水を選んでください。]
- **A:** おちゃをのみます。
- **T:** パンを食べます。おちゃも飲みます。次は、何を食べたいですか？ [「パンを食べます」と「おちゃを飲みます」が言えました。食べたい物を一つ言ってください。]
- **A:** すしを食べたいです。
- **T:** すしを食べたいです。いいですね。すしの何が好きですか？

</details>

## Lucas · ko N2 · explica nativo · 7.4/10

**Bien:** Ofreció elegir entre comida y el día, y mantuvo el tema elegido por el alumno. · Pidió repetir de forma natural cuando solo se oyó «la de», sin inventar una respuesta. · Hizo que el alumno produjera varias frases útiles sobre gustos, frecuencia y comida.

**Problemas:**
- (correcciones) «피자에 뭐를 넣어요?» → Como el alumno respondió «치즈 좋아해요» en vez de contestar qué pone en la pizza, debió señalarlo brevemente y modelar: «치즈를 넣어요. 다시 말해 보세요: 치즈를 넣어요.»
- (apoyo) «[지금까지 말한 내용을 복습했어요. 치즈 피자의 느낌을 말해 보세요. 예: 맛있어요.]» → La indicación debía estar en español y ser más accesible: «Di cómo es la pizza de queso. Por ejemplo: 맛있어요.»
- (ensena) «가끔 피자를 먹고, 치즈를 좋아해요.» → Debió aprovechar la respuesta para enseñar la diferencia entre «치즈를 넣어요» y «치즈를 좋아해요», y pedir al alumno que produjera la forma correcta.

**Alumno:** Nivel 2 real: comprende preguntas y produce frases memorizadas o muy sencillas con apoyo, pero todavía confunde la estructura que se está practicando. Dificultades: Responder a una pregunta concreta sobre qué ingrediente pone, usando 넣어요.; Distinguir entre 좋아해요 y 넣어요.; Necesita apoyo para ampliar respuestas más allá de frases breves..

**Recomendación:** Mantén preguntas cortas y elecciones claras, pero corrige inmediatamente una sola estructura cuando la respuesta no corresponda a la pregunta.

<details><summary>Transcripción</summary>

- **T:** 안녕하세요! 오늘은 «저는 … 좋아해요»를 연습해요. 음식 이야기할까요, 아니면 하루 이야기할까요? [«좋아해요» significa «me gusta». Elige: comida o tu día.]
- **A:** 음식 좋아해요.
- **T:** 좋아요! 어떤 음식을 좋아해요?
- *(silencio: ruido: el alumno no dijo «la de», fue ruido de fondo transcrito)*
- **A:** la de
- **T:** 음? 다시 말해 주세요. 음식 이름을 말해 주세요. [음식 이름을 한국어로 말해 보세요. 예: 김치, 피자.]
- **A:** 피자 좋아해요.
- **T:** 피자는 자주 먹어요, 가끔 먹어요?
- *(silencio: iniciativa)*
- **T:** 피자는 자주 먹어요, 가끔 먹어요? 하나를 골라 말해 보세요. [«자주» significa «a menudo» y «가끔» significa «a veces». Elige una opción.]
- **A:** 가끔 먹어요.
- **T:** 맞아요! 가끔 먹어요. 피자에 뭐를 넣어요? [«넣어요»는 «poner»라는 뜻이에요. 피자 토핑을 말해 보세요.]
- **A:** 치즈 좋아해요.
- **T:** 가끔 피자를 먹고, 치즈를 좋아해요. 치즈 피자는 어때요? [지금까지 말한 내용을 복습했어요. 치즈 피자의 느낌을 말해 보세요. 예: 맛있어요.]
- **A:** 치즈 피자 맛있어요.
- **T:** 그럼 음료는요? 물 좋아해요, 주스 좋아해요? [물이나 주스 중 하나를 골라 말해 보세요.]

</details>

## Diego · ru N2 · explica nativo · 9.6/10

**Bien:** Ofreció una elección de tema y trabajó una estructura concreta: «Я люблю…» / «Я не люблю…». · Corrigió correctamente «Я люблю еда» a «Я люблю еду» y pidió al alumno que reutilizara la frase. · Ante el ruido, pidió repetir de forma natural, sin inventar lo que el alumno había dicho.

**Problemas:**
- (tema) ««Какую еду ты любишь: пиццу или суп?»» → Después de presentar las opciones, dejar que el alumno elija libremente una comida, por ejemplo: «Какую еду ты любишь? Назови любую еду.»

**Alumno:** Nivel 2 real: puede producir frases muy breves y usar «Я люблю…» y «Я не люблю…» con apoyo y modelos. Dificultades: Confunde el caso acusativo después de «люблю»: «еда» → «еду».; Necesita apoyo para recuperar vocabulario de comidas y bebidas.; Todavía requiere repetición y opciones cerradas para responder con seguridad..

**Recomendación:** Mantén el modelo «Я люблю/не люблю…», pero permite que el alumno elija libremente alimentos y bebidas y amplía gradualmente el vocabulario.

<details><summary>Transcripción</summary>

- **T:** Привет! Сегодня учимся говорить: «Я люблю…». Выбери тему: твой день или еда. [Выбери одну тему: твой день или еда.]
- **A:** Я люблю еда.
- **T:** Хорошо! Мы говорим: «Я люблю еду». После «люблю» — «еду». Скажи всю фразу! [После «люблю» нужно «еду», потому что это то, что ты любишь. Повтори всю фразу.]
- *(silencio: ruido: el alumno no dijo «la de», fue ruido de fondo transcrito)*
- **A:** la de
- **T:** Мм? Повтори, пожалуйста. Скажи: «Я люблю еду». [Повтори фразу по-русски: «Я люблю еду».]
- **A:** Я люблю еду
- **T:** Вот так: «Я люблю еду»! Какую еду ты любишь?
- *(silencio: iniciativa)*
- **T:** Какую еду ты любишь: пиццу или суп?
- **A:** Я люблю пиццу
- **T:** Пицца — вкусно! Что ты любишь пить: чай или кофе? [Выбери: чай или кофе.]
- **A:** Я люблю чай
- **T:** Ты сказал: «Я люблю еду», «Я люблю пиццу» и «Я люблю чай». Теперь скажи: что ты не любишь? [Повтори модель: «Я не люблю…» и добавь еду.]
- **A:** Я не люблю суп.
- **T:** Отлично: «Я не люблю суп»! Что ты не любишь пить?

</details>

## Elena · es N3 · explica nativo · 10/10

**Bien:** Propuso una elección de tema y respetó la preferencia del alumno. · Enseñó «quiero» y «me gustaría» con frases concretas que el alumno produjo correctamente. · Ante el ruido, pidió repetir de forma natural sin inventar lo que el alumno había dicho. La indicación en inglés fue breve y útil.

**Alumno:** Nivel 3 observado: puede formar frases claras sobre su día, trabajo y preferencias con apoyo y modelos breves. Dificultades: Necesita apoyo para iniciar una respuesta en español.; Todavía requiere práctica para desarrollar respuestas espontáneas más largas.; Expresa cierta falta de confianza al hablar con clientes..

**Recomendación:** Mantén preguntas con dos opciones y sigue haciendo que produzca frases completas, reduciendo gradualmente los modelos.

<details><summary>Transcripción</summary>

- **T:** ¡Hola! Hoy practicaremos «quiero» y «me gustaría» para hablar de planes. ¿Prefieres hablar de tu día o de una comida especial?
- **A:** Hello! I want to talk about my day, please.
- **T:** En español: «Quiero hablar de mi día, por favor». Dilo tú ahora. [Say the whole sentence in Spanish: «Quiero hablar de mi día, por favor».]
- *(silencio: ruido: el alumno no dijo «so the», fue ruido de fondo transcrito)*
- **A:** so the
- **T:** Perdón, no te entendí. Cuéntame: ¿cómo fue tu día?
- **A:** My day was good. I want to learn more Spanish.
- **T:** Me alegra. Para practicar, completa esta frase: «Quiero aprender español porque…»
- *(silencio: iniciativa)*
- **T:** Vamos despacio: «Quiero… aprender español… porque…». Completa con una razón, por ejemplo: «porque me gusta viajar». [Complete the sentence with your own reason. Say the whole sentence in Spanish.]
- **A:** Quiero aprender español porque es importante para mi trabajo.
- **T:** ¡Exacto: «Quiero aprender español porque es importante para mi trabajo»! ¿Qué necesitas hacer en español durante tu trabajo?
- **A:** Necesito hablar con clientes y escribir correos en español.
- **T:** Ya usaste «quiero» y «necesito» para hablar de tu trabajo. Ahora practica «me gustaría»: ¿qué te gustaría mejorar primero, hablar o escribir?
- **A:** Me gustaría mejorar hablar primero porque es más difícil para mí.
- **T:** Tiene sentido: hablar con clientes requiere mucha confianza. ¿En qué situación te gustaría practicar primero: una llamada o una reunión?

</details>
