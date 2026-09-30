#!/usr/bin/env python3
"""Generate the integrated English N3 C81-C85 learning-strategies block."""
import argparse, hashlib, importlib.util, json, re, subprocess
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]
OUT=REPO/'assets/contenido/en/editorial/n3'
REPORT_OUT=REPO/'build/editorial-n3-81-85'
MAP=REPO/'assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json'
HELPER=REPO/'tools/contenido/generar_editorial_n3_66_70.py'
spec=importlib.util.spec_from_file_location('schema_helpers',HELPER)
h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
NUMBERS=range(81,86)
CONCEPTS={n:f'n3-learning-strategies-{n-80}' for n in NUMBERS}; ALL=list(CONCEPTS.values())
for k,v in dict(OUT=OUT,MAP=MAP,NUMBERS=NUMBERS,CONCEPTS=CONCEPTS,ALL_CONCEPTS=ALL,PHASES=dict(zip(NUMBERS,['input','form','comprehension','production','transfer']))).items(): setattr(h,k,v)

# Every group is mandatory; alternatives preserve one observable criterion.
EVIDENCE_GROUPS={
 'en.n3.c84.p03':[
  ['recognise familiar words','recognize familiar words','know familiar words'],
  ['spelling new words difficult','spelling new words is difficult','struggle to spell new words','difficulty spelling new words'],
  ['sixteen of twenty','sixteen out of twenty','16 of 20','16 out of 20','16/20'],
  ['two weeks','2 weeks','fourteen days','14 days'],
  ['testing five words','test five words','test myself on five words','test myself on 5 words'],
  ['without looking at my notes','without notes','without using notes','from memory'],
  ['every evening','each evening','every night','each night'],['ten minutes','10 minutes'],
  ['correct my errors','correct the errors','correct mistakes','correct my mistakes'],
  ['to learn the difficult spellings','to improve my spelling','so that I can spell them correctly','to remember the spellings'],
  ['dated word lists','word lists with dates','date each word list','date my word lists'],['scores','results'],
  ['compare my first and final lists','compare the first and final lists','compare my first and last lists','compare the first and last lists','compare my first list with my final list','compare my first list with my last list']],
 'en.n3.c84.e04':[
  ['understand short dialogues','follow short dialogues','understand short conversations','follow short conversations'],
  ['miss dates','dates are sometimes difficult','struggle with dates','difficulty understanding dates','have trouble with dates'],
  ['eight of ten dates','eight out of ten dates','8 of 10 dates','8 out of 10 dates','8/10 dates'],
  ['two weeks','2 weeks','fourteen days','14 days'],
  ['listen to a short booking dialogue','listen to short booking dialogues','listen to booking conversations','listen to a booking conversation'],
  ['write the dates','write down the dates','note the dates','record the dates'],
  ['Monday','Mondays'],['Wednesday','Wednesdays'],['Friday','Fridays'],['ten minutes','10 minutes'],
  ['dated answer sheets','answer sheets with dates','date my answer sheets','date each answer sheet'],
  ['so that I can check my progress','to check my progress','to measure my progress','so that I can see my progress','to track my progress'],
  ['compare my first and final scores','compare the first and final scores','compare my first and last scores','compare the first and last scores','compare my first score with my final score','compare my first score with my last score']],
 'en.n3.c84.r03':[
  ['explain my ideas','explain ideas clearly','express my ideas clearly'],
  ['forget past verb forms','past verb forms are difficult','struggle with past verb forms','have trouble with past tense forms'],
  ['nine of ten past forms','nine out of ten past forms','9 of 10 past forms','9 out of 10 past forms','9/10 past forms'],
  ['two weeks','2 weeks','fourteen days','14 days'],
  ['write a short diary entry','write short diary entries','write a diary entry'],
  ['Tuesday','Tuesdays'],['Thursday','Thursdays'],['Sunday','Sundays'],['fifteen minutes','15 minutes'],
  ['check the verbs','check my verbs','review the verbs','check every verb'],
  ['to find and correct my mistakes','to correct my mistakes','to find my mistakes','so that I can correct errors','to correct verb errors'],
  ['original and corrected entries','original entries and corrected entries','originals and corrections','original entries and my corrections'],
  ['compare mistakes in my first and last entries','compare errors in my first and last entries','compare mistakes in the first and last entries','compare my first and last entries','compare the first and final entries','compare my first entry with my last entry']],
 'en.n3.c85.e04':[
  ['identify the main idea well','understand the main idea','find the main idea','recognise the main idea','recognize the main idea'],
  ['need evidence for my answers','answers lack evidence','answers without supporting evidence','do not support my answers','need to support my answers'],
  ['two to three out of five','2 to 3 out of 5','two before and three now','two correct answers to three','from two to three','from 2 to 3'],
  ['four supported answers out of five','four out of five answers','four of five answers','4 out of 5 answers','4 of 5 answers','4/5 answers'],
  ['long texts take too much time','long texts take too long','cannot finish long texts','cannot finish the long texts','not enough time for long texts'],
  ['shorter texts','short texts'],
  ['underline supporting lines','underline a supporting line','underline evidence','underline the supporting lines'],
  ['to explain my answers','to support my answers','so that my answers have evidence','so that I can support my answers','to show evidence for my answers'],
  ['fifteen minutes','15 minutes'],['Monday','Mondays'],['Wednesday','Wednesdays'],['Friday','Fridays'],
  ['two weeks','2 weeks','fourteen days','14 days'],
  ['next Monday','on Monday we will check','on Monday we will review'],
  ['four answers with underlined lines','4 answers with underlined lines','four answers and their supporting lines','four answers with evidence','4 answers with evidence'],
  ['check whether this change helps','check my progress','review my progress','check the four answers','review the four answers','review these answers']],
 'en.n3.c85.r03':[
  ['identify speakers well','can identify speakers well','recognise speakers','recognize speakers','identify the speaker','know who is speaking'],
  ['miss numbers','numbers are still difficult','struggle with numbers','have difficulty hearing numbers'],
  ['four to six','4 to 6','four before and six now','4 before and 6 now'],
  ['eight details out of ten','eight out of ten details','eight of ten details','8 out of 10 details','8 of 10 details','8/10 details'],
  ['tired at night','tired in the evening','nighttime tiredness','evening tiredness'],
  ['practise at lunch','practice at lunch','study at lunch','practise during lunch','practice during lunch'],
  ['pause after each number','pause after every number','stop after each number','pause the audio after each number'],
  ['write it down','write them down','write down each number','note each number','write each number down'],
  ['to check what I hear','to catch numbers accurately','so that I can check the numbers','to understand numbers better','to check the numbers'],
  ['ten minutes','10 minutes'],['Tuesday','Tuesdays'],['Thursday','Thursdays'],['Saturday','Saturdays'],
  ['two weeks','2 weeks','fourteen days','14 days'],
  ['dated answer sheets','answer sheets with dates','date my answer sheets','date each answer sheet'],
  ['on Saturday','next Saturday','this Saturday'],
  ['compare the next sheet with the first','compare my next sheet with my first','compare the first and next sheets','compare my first and next answer sheets','compare my next answer sheet with the first'],
  ['to review my progress','to check my progress','to measure my progress','so that we can check my progress','to see my progress']],
}
REMEDIATION={
 81:{'e01':('t01','r01'),'e02':('t03','r03'),'e03':('t02','r02'),'e04':('t06','r03')},
 82:{'e01':('t01','r02'),'e02':('t03','r03'),'e03':('t04','r02'),'e04':('t06','r03')},
 83:{'e01':('t02','r03'),'e02':('t03','r01'),'e03':('t05','r02'),'e04':('t06','r03')},
 84:{'e01':('t05','r01'),'e02':('t03','r03'),'e03':('t01','r03'),'e04':('t06','r03')},
 85:{'e01':('t03','r02'),'e02':('t06','r03'),'e03':('t05','r03'),'e04':('t06','r03')},
}

def build(n):
    c=CONCEPTS[n]; p=f'en.n3.c{n}'
    pools={k:[] for k in ['practiceGuided','practice','evaluation','review']}
    def add(key,fmt,prompt,data,feedback,source=None,requires=None):
        pool={'pg':'practiceGuided','p':'practice','e':'evaluation','r':'review'}[key.rstrip('0123456789')]
        kw={'source':{'text':source}} if source else {}
        if requires: kw['requires']=requires
        args=(f'{p}.{key}',prompt)
        if fmt=='q': item=h.choose(*args,data,0,c,pool,feedback,**kw)
        elif fmt=='l': item=h.listen(*args,data[0],data[1],0,c,pool,feedback,**kw)
        elif fmt=='o': item=h.order(*args,data,c,pool,feedback,**kw)
        elif fmt=='m': item=h.match(*args,data,c,pool,feedback,minimum=len(data),**kw)
        elif fmt=='f':
            item=h.multi_fill(*args,source or '',data[0],data[1],c,pool,feedback,requires=requires)
            item['answer']['accepted'].append(' '.join(data[1]))
            h.content_hash(item)
        elif fmt=='w': item=h.write(*args,source,data,c,pool,feedback,word_range=(80,100) if n==84 else (90,120),requires=requires)
        pools[pool].append(item); return item
    if n==81:
        vocab=[('strength','fortaleza'),('difficulty','dificultad'),('goal','meta'),('feedback','retroalimentación'),('already','ya'),('improve','mejorar')]
        rows=[('My strength is reading. I already understand short texts.','Mi fortaleza es la lectura. Ya entiendo textos cortos.','Una fortaleza describe algo que ya haces bien.'),('I find spelling difficult. This is my main difficulty.','Me cuesta la ortografía. Esta es mi principal dificultad.','La dificultad señala un obstáculo actual.'),('My goal is to improve my pronunciation.','Mi meta es mejorar mi pronunciación.','Una meta expresa un resultado futuro.'),('Feedback: You explain clearly, but you miss verb endings.','Retroalimentación: Explicas con claridad, pero omites terminaciones verbales.','Separa el comentario positivo del problema específico.'),('I already remember names, but I want to remember dates too.','Ya recuerdo nombres, pero también quiero recordar fechas.','Una frase puede incluir una fortaleza y una meta.'),('I understand questions well. Fast answers are difficult. I want to follow longer conversations.','Entiendo bien las preguntas. Las respuestas rápidas me cuestan. Quiero seguir conversaciones más largas.','Identifica capacidad actual, dificultad y resultado deseado por separado.')]
        add('pg01','q','¿Qué comentario describe una fortaleza actual?',['I explain my ideas clearly.','I struggle with long words.','I hope to speak for two minutes.'],'Explicar con claridad ya es una capacidad; las otras frases expresan dificultad y meta.')
        add('pg02','q','¿Cuál describe una dificultad al estudiar?',['I cannot remember new verbs.','I want to learn ten verbs.','I know common verbs well.'],'Cannot remember identifica el problema presente con los verbos.')
        add('pg03','l','Escucha a Ana: ¿qué quiere conseguir?',('I read instructions easily, but I miss details in audio. I want to understand phone messages.',['understand phone messages','read instructions easily','miss details in audio']),'Want to presenta la meta de Ana; leer instrucciones es su fortaleza.')
        add('p01','m','Relaciona estos comentarios con su función.',[('I can spell familiar words.','fortaleza actual'),('I forget words under pressure.','dificultad actual'),('I aim to learn five phrases.','meta futura')],'Can, forget y aim to distinguen capacidad, obstáculo y objetivo.')
        add('p02','l','Escucha a Leo: identifica su problema.',('My notes are clear. I lose my place when people speak quickly. I want to follow group discussions.',['following fast speech','taking clear notes','joining a future discussion']),'Lose my place localiza la dificultad de Leo en el habla rápida.')
        add('p03','o','Ordena la meta sobre vocabulario.','I want to learn useful words','Want to learn expresa un resultado de aprendizaje deseado.')
        add('e01','l','Escucha a Sara: selecciona su fortaleza.',('I can give clear examples. I hesitate before questions. My goal is to ask questions confidently.',['giving clear examples','asking questions confidently','answering without hesitation']),'Sara ya da ejemplos claros; la confianza al preguntar es una meta.')
        add('e02','q','¿Cuál es una meta de aprendizaje, no una capacidad ni un problema?',['I hope to understand longer talks.','I understand simple talks now.','I get lost during long talks.'],'Hope to sitúa el resultado en el futuro.')
        add('e03','q','¿Qué dificultad menciona este alumno?',['remembering word stress','learning six words next week','using short sentences clearly'],'La dificultad es olvidar el acento; las otras opciones son una meta y una fortaleza.',source='I use short sentences clearly, but I forget word stress. Next week I want to learn six words.')
        add('e04','f','Clasifica cinco comentarios: strength, difficulty o goal.',(['I can explain the rules accurately. → ___','I often confuse similar sounds. → ___','I aim to read a page without help. → ___','My written examples are clear. → ___','I would like to speak more fluently. → ___'],['strength','difficulty','goal','strength','goal']),'Can y are describen logros; confuse indica dificultad; aim y would like indican metas.')
        add('r01','q','¿Qué parte del diario es un logro actual?',['I recognise common question words.','I want to ask better questions.','I mix up two question forms.'],'Reconocer palabras interrogativas ya es una capacidad demostrada.')
        add('r02','l','Escucha a Omar: ¿qué le cuesta?',('I write clear paragraphs, but I need help with commas. I hope to edit my own work.',['using commas','writing clear paragraphs','editing independently in the future']),'Need help with commas identifica una necesidad actual.')
        add('r03','f','Clasifica otros cinco comentarios: strength, difficulty o goal.',(['I can follow short recipes. → ___','I struggle to remember technical terms. → ___','I plan to understand a whole lecture. → ___','I cannot hear the difference between these sounds. → ___','I already use full stops correctly. → ___'],['strength','difficulty','goal','difficulty','strength']),'Follow y use correctamente indican fortalezas; struggle y cannot señalan dificultades; plan indica meta.')
    elif n==82:
        vocab=[('purpose','propósito'),('strategy','estrategia'),('review','repasar'),('remember','recordar'),('record','grabar'),('notice','notar')]
        rows=[('A strategy is an action; its purpose is the result you want.','Una estrategia es una acción; su propósito es el resultado que deseas.','Explica qué haces y para qué lo haces.'),('I review my notes to remember key ideas.','Repaso mis apuntes para recordar las ideas principales.','Después de to usa un verbo en forma base.'),('I record my voice so that I can notice mistakes.','Grabo mi voz para poder notar errores.','So that introduce sujeto y verbo: I can notice.'),('I practise with a partner to build confidence.','Practico con un compañero para ganar confianza.','La acción debe servir al propósito indicado.'),('I use large cards so that I can read the words easily.','Uso tarjetas grandes para poder leer las palabras fácilmente.','No pongas un sujeto justo después de to: usa so that.'),('I test myself to find gaps, and I check the answers so that I can correct them.','Me pongo a prueba para encontrar lagunas y reviso las respuestas para poder corregirlas.','Ambas estructuras conectan una estrategia con su finalidad.')]
        add('pg01','q','Completa “I read aloud ___ improve my fluency”.',['to','so that','because'],'Improve no tiene sujeto propio; el propósito se introduce con to.')
        add('pg02','q','Completa “I use pictures ___ I can remember new nouns”.',['so that','to','for'],'I can remember es una oración completa y necesita so that.')
        add('pg03','l','Escucha: ¿para qué se graba Kim?',('I record short answers so that I can hear where I pause.',['to notice pauses','to practise handwriting','to learn spelling rules']),'Hear where I pause vincula la grabación con detectar pausas.')
        add('p01','m','Relaciona cada estrategia con el propósito más directo.',[('test yesterday’s words without notes','check what I still remember'),('compare my recording with the model','notice pronunciation differences'),('make a weekly timetable','reserve regular study time')],'Cada acción produce un resultado distinto: memoria, pronunciación u horario.')
        add('p02','o','Ordena el propósito de usar ejemplos.','I write examples to understand new expressions','To understand explica por qué se escriben ejemplos.')
        add('p03','f','Completa con to o so that según la estructura.',(['I repeat the dialogue ___ speak more smoothly.','I label objects ___ I can learn their names.'],['to','so that']),'Speak sigue directamente a to; I can learn necesita so that.')
        add('e01','l','Escucha: elige el propósito de la estrategia.',('I cover the definitions and explain each word so that I can check my understanding.',['checking understanding','copying every definition','improving letter shapes']),'Explicar sin mirar comprueba comprensión; no es una tarea de copia.')
        add('e02','q','¿Qué plan usa correctamente una cláusula con sujeto?',['I set reminders so that I remember to study.','I set reminders to I remember to study.','I set reminders so that remember to study.'],'So that admite I remember; to no introduce ese sujeto.')
        add('e03','q','¿Qué estrategia responde al problema de olvidar el significado?',['Test words with pictures to recall their meaning.','Copy words neatly to improve handwriting.','Speak louder to increase the volume.'],'Relacionar palabras con imágenes ejercita su significado; copiar con cuidado mejora la letra.')
        add('e04','f','Completa seis planes usando to o so that.',(['I group words by topic ___ find them quickly.','I study in a quiet room ___ I can concentrate.','I ask for examples ___ understand the rule.','I keep a vocabulary notebook ___ I can review old words.','I practise questions ___ prepare for the interview.','I slow the audio down ___ I can hear each ending.'],['to','so that','to','so that','to','so that']),'To precede un verbo base; so that precede I can y una finalidad completa.')
        add('r01','q','¿Qué frase expresa bien el propósito de un descanso?',['I take breaks to stay focused.','I take breaks to I stay focused.','I take breaks so that stay focused.'],'Stay focused no lleva sujeto en esta versión; corresponde to.')
        add('r02','l','Escucha: ¿qué resultado busca Eva?',('I save corrected sentences so that I can avoid the same errors next time.',['avoiding repeated errors','collecting more uncorrected sentences','finishing without checking']),'Guardar correcciones ayuda a evitar los mismos errores en otro intento.')
        add('r03','f','Recupera to y so that en seis estrategias distintas.',(['I draw a simple diagram ___ organise my ideas.','I practise with a timer ___ I can finish on time.','I mark stressed syllables ___ pronounce longer words.','I use headphones ___ I can hear the speaker clearly.','I read the question twice ___ avoid careless mistakes.','I keep a progress log ___ I can compare my results.'],['to','so that','to','so that','to','so that']),'Diagramas, tiempo y registro mantienen la distinción entre infinitivo y oración con sujeto.')
    elif n==83:
        vocab=[('achievement','logro'),('feedback','retroalimentación'),('specific','específico'),('next step','siguiente paso'),('check','comprobar'),('ending','terminación')]
        rows=[('Feedback can name an achievement and a specific problem.','La retroalimentación puede señalar un logro y un problema específico.','No interpretes todo el comentario como crítica.'),('Your ideas are clear, but you sometimes miss an ending.','Tus ideas son claras, pero a veces omites una terminación.','Clear ideas es el logro; miss an ending es el problema.'),('The next step is to check each verb before you submit your work.','El siguiente paso es comprobar cada verbo antes de entregar tu trabajo.','Una acción observable dice qué hacer y sobre qué hacerlo.'),('Practise more is less specific than rewrite three incorrect sentences.','Practica más es menos específico que reescribe tres frases incorrectas.','Prefiere acciones que puedas comprobar después.'),('Keep using examples; add one reason after each opinion.','Sigue usando ejemplos; añade una razón después de cada opinión.','Conserva la fortaleza mientras corriges la dificultad.'),('You used the right words. Two answers lacked reasons. Add a reason to each answer.','Usaste las palabras adecuadas. A dos respuestas les faltaban razones. Añade una razón a cada respuesta.','Extrae tres columnas: logro, problema y siguiente acción.')]
        add('pg01','q','Según el comentario, ¿qué debe conservar Luz?',['her clear examples','missing reasons','shorter examples without reasons'],'El docente valora los ejemplos claros; la mejora corresponde a las razones.',source='Your examples are clear. However, your opinions need reasons. Add one reason after each opinion.')
        add('pg02','q','¿Qué acción permite comprobar una mejora concreta?',['Underline and correct the three verb errors.','Try to become a better student.','Feel more confident about verbs.'],'Subrayar y corregir tres errores deja evidencia observable.')
        add('pg03','l','Escucha: selecciona el siguiente paso recomendado.',('Your introduction is clear. You repeat the same adjective. Replace two repeated adjectives with different words.',['replace two repeated adjectives','remove the introduction','repeat the adjective more often']),'El paso propuesto modifica dos repeticiones y conserva la introducción.')
        add('p01','m','Relaciona cada comentario con una acción adecuada.',[('Three sentences have no full stop.','Add punctuation at the end of those sentences.'),('Two answers do not explain why.','Add a reason to both answers.'),('Your speech is difficult to hear.','Make another recording at a higher volume.')],'Las acciones responden a puntuación, razones y volumen.')
        add('p02','l','Escucha a la tutora: ¿cuál es el logro?',('Your headings help the reader. Two paragraphs have no examples. Add an example to each of those paragraphs.',['useful headings','examples in every paragraph','longer paragraphs']),'La tutora aprueba los títulos; los ejemplos siguen pendientes.')
        add('p03','o','Ordena una acción para revisar un borrador.','Check the tense in every sentence','Check y every sentence definen una revisión observable.')
        add('e01','l','Escucha la tutoría: ¿qué problema sigue presente?',('You used six new words correctly. Your answers are hard to follow because the events are out of order. Number the events before rewriting.',['events in the wrong order','six incorrectly used words','missing new vocabulary']),'La secuencia dificulta la comprensión aunque el vocabulario sea correcto.')
        add('e02','q','¿Qué acción responde al comentario sobre preguntas?',['Rewrite the four questions with the correct word order.','Learn four more greetings.','Make the answers longer.'],'El problema exige revisar el orden de las preguntas.',source='Your greetings sound natural. Four questions have incorrect word order.')
        add('e03','q','¿Qué respuesta conserva el logro y corrige el problema?',['Keep the examples and add a conclusion.','Remove the examples and keep the ending.','Add more examples but leave out the conclusion.'],'La tarea pide mantener ejemplos útiles y completar el cierre.',source='Your examples support your ideas well. There is no conclusion. Add a final sentence with your main point.')
        note='Tutor: Your story has a clear beginning. You change from past to present in the middle. Underline every verb and rewrite the present forms in the past.'
        item=add('e04','f','Escucha y completa: logro, problema y acción. Copia los fragmentos.',(['Achievement: a ___.','Problem: you change from ___.','Next step: underline every verb and ___.'],['clear beginning','past to present','rewrite the present forms in the past']),'La tutoría distingue inicio claro, cambio de tiempo y corrección de formas verbales.',source=note)
        item['origin'].update(audio=note,audioMode='tts',languageCode='en',speedOptions=[0.75,1.0],maxReplays=3,revealTranscriptAfterAttempt=True); h.content_hash(item)
        add('r01','q','¿Qué acción concreta mejora este mensaje?',['Add the date and room number to the invitation.','Use more polite greetings in the invitation.','Write a longer invitation without details.'],'El saludo ya funciona; faltan dos datos concretos.',source='Your greeting is polite. The invitation does not say when or where to meet.')
        add('r02','l','Escucha: ¿qué debe mantener el alumno?',('Your pace is comfortable. Some final sounds disappear. Keep the same pace and repeat the words with clear endings.',['the comfortable pace','the missing final sounds','a much faster pace']),'La velocidad es adecuada; la corrección afecta a los sonidos finales.')
        add('r03','f','Lee otra tutoría y recupera las tres columnas con palabras del texto.',(['Achievement: accurate ___.','Problem: three answers lack ___.','Next step: ___ beside each answer.'],['calculations','units','write the correct unit']),'La nueva tutoría separa cálculos correctos, unidades ausentes y anotación requerida.',source='Your calculations are accurate. Three answers lack units. Write the correct unit beside each answer.')
    elif n==84:
        vocab=[('measurable','medible'),('task','tarea'),('frequency','frecuencia'),('deadline','fecha límite'),('evidence','evidencia'),('progress','progreso')]
        rows=[('A measurable goal says how much you want to improve.','Una meta medible indica cuánto quieres mejorar.','Incluye un número o criterio que permita comprobar el resultado.'),('A task describes what you will do to reach the goal.','Una tarea describe qué harás para alcanzar la meta.','Indica una acción concreta.'),('Frequency tells us how often: twice a week or every day.','La frecuencia indica cada cuánto: dos veces por semana o cada día.','Diez minutos expresa duración, no frecuencia.'),('The deadline is in two weeks. Keep each recording as evidence.','La fecha límite es dentro de dos semanas. Conserva cada grabación como evidencia.','El plazo y un producto guardado permiten revisar el avance.'),('Compare your first and last scores to check progress.','Compara tu primera y última puntuación para comprobar el progreso.','La evidencia debe medir la misma habilidad que la meta.'),('I will answer eight of ten questions correctly in two weeks. I will practise on Monday, Wednesday and Friday and save my scores.','Responderé correctamente ocho de diez preguntas en dos semanas. Practicaré lunes, miércoles y viernes y guardaré mis puntuaciones.','El modelo reúne meta, tarea, frecuencia, plazo y evidencia.')]
        add('pg01','q','¿Qué meta se puede medir al terminar dos semanas?',['Answer nine of twelve questions correctly.','Become much better at questions.','Feel happy when I study questions.'],'Nueve de doce respuestas permite verificar el resultado final.')
        add('pg02','q','¿Qué dato expresa frecuencia de estudio?',['four times a week','for fifteen minutes','by the end of June'],'Cuatro veces por semana cuenta sesiones; minutos mide duración y junio el plazo.')
        add('pg03','l','Escucha: ¿qué guardará Sol como evidencia?',('I will practise spelling every weekday for two weeks. I will keep my weekly test sheets to compare the scores.',['weekly test sheets','a list of possible study rooms','an empty timetable']),'Las pruebas permiten comparar resultados de ortografía entre semanas.')
        add('p01','m','Relaciona cada dato del plan con su función.',[('record a one-minute answer','tarea'),('every Tuesday and Thursday','frecuencia'),('reach seven correct answers by 15 May','meta y plazo'),('save the audio files','evidencia')],'El plan identifica acción, sesiones, resultado fechado y producto verificable.')
        add('p02','l','Escucha a Ben: ¿qué dato falta en su plan?',('I want to spell eighteen words correctly in two weeks. I will test myself and save each result, but I have not decided how often to practise.',['practice frequency','a measurable target','evidence of results']),'Ben tiene meta y registro, pero todavía no ha decidido la frecuencia.')
        practice_source='Write as Ada. Strength: recognising familiar words. Difficulty: spelling new words. Goal: spell sixteen of twenty words in two weeks. Task: test five words without notes, then correct errors. Frequency: every evening for ten minutes. Evidence: dated word lists and scores. Compare the first and final lists. Include a purpose with to or so that.'
        practice_answer='I recognise familiar words, but I find spelling new words difficult. My goal is to spell sixteen of twenty words correctly in two weeks. Every evening, I will spend ten minutes testing five words without looking at my notes. Then I will correct my errors to learn the difficult spellings. I will keep dated word lists and scores so that I can see my progress. At the end of two weeks, I will compare my first and final lists and check how many words I can spell correctly.'
        add('p03','w','Practica un plan de 80–100 palabras con los datos de Ada.',[practice_answer,practice_answer.replace('I find spelling new words difficult','spelling new words is difficult for me')],'El texto organiza fortaleza, dificultad, meta, rutina diaria y comparación de listas.',source=practice_source)
        add('e01','l','Escucha: ¿qué prueba serviría para comprobar la meta?',('My goal is to understand eight details in a short talk by the end of two weeks. I will listen three times a week.',['answers to the same type of listening questions','the number of pages copied by hand','a list of days when the app was open']),'Las respuestas de comprensión miden detalles entendidos; abrir la aplicación no demuestra aprendizaje.')
        add('e02','q','¿Qué plan incluye una frecuencia definida?',['Practise ten words on Monday, Wednesday and Saturday.','Practise ten words when possible.','Practise ten words for a short time.'],'Los tres días concretos permiten comprobar si se completaron las sesiones.')
        add('e03','q','¿Qué cambio vuelve medible esta meta?',['Write eight correct sentences out of ten by Sunday.','Enjoy writing much more soon.','Think about writing whenever possible.'],'Ocho de diez y el domingo convierten la intención en un resultado comprobable.',source='Initial goal: I want to get better at writing.')
        source='Profile: Nina understands short dialogues but misses dates. Target: identify eight of ten dates correctly in two weeks. Task: listen to a short booking dialogue and write the dates. Frequency: Monday, Wednesday and Friday, ten minutes each time. Evidence: keep dated answer sheets and compare the first and final scores. Write as Nina. Include every detail; use to or so that for purpose.'
        a='I understand short dialogues, but I sometimes miss dates. My goal is to identify eight of ten dates correctly in two weeks. I will listen to a short booking dialogue and write the dates on Monday, Wednesday and Friday. Each session will last ten minutes. I will keep dated answer sheets so that I can check my progress. At the end of the second week, I will compare my first and final scores to see whether I have reached my goal.'
        add('e04','w','Redacta el plan de Nina en 80–100 palabras usando los datos del perfil.',[a,a.replace('I sometimes miss dates','dates are sometimes difficult for me')],'El plan conserva ocho de diez, seis sesiones en dos semanas y hojas fechadas para comparar resultados.',source=source)
        add('r01','q','¿Qué evidencia comprueba una mejora en pronunciación?',['first and final recordings of the same sounds','the colour of the study notebook','a calendar with no completed sessions'],'Comparar grabaciones de los mismos sonidos permite observar el cambio.')
        add('r02','l','Escucha el plan: identifica el plazo.',('I will practise twenty useful phrases every other day. After fourteen days, I will test myself without notes and save the result.',['after fourteen days','every other day','twenty useful phrases']),'Catorce días marca el control final; cada dos días es la frecuencia.')
        source='Profile: Luis can explain ideas but forgets past verb forms. Target: use nine of ten past forms correctly in two weeks. Task: write a short diary entry and check the verbs. Frequency: Tuesday, Thursday and Sunday, fifteen minutes each session. Evidence: save the original and corrected entries; compare mistakes in the first and last entries. Write as Luis and state the purpose of checking.'
        a='I can explain my ideas, but I often forget past verb forms. In two weeks, I want to use nine of ten past forms correctly. I will write a short diary entry on Tuesday, Thursday and Sunday. Each session will take fifteen minutes. I will check the verbs to find and correct my mistakes. I will save the original and corrected entries as evidence. After two weeks, I will compare mistakes in my first and last entries so that I can measure my progress.'
        add('r03','w','Escribe el plan de Luis en 80–100 palabras con frecuencia y evidencia.',[a,a.replace('I often forget past verb forms','past verb forms are difficult for me')],'El diario vincula nueve formas correctas, tres sesiones semanales y comparación de errores.',source=source)
    else:
        vocab=[('progress','progreso'),('obstacle','obstáculo'),('adjust','ajustar'),('keep','mantener'),('review','revisar'),('evidence','evidencia')]
        rows=[('Review the evidence before you change your plan.','Revisa la evidencia antes de cambiar tu plan.','Compara resultados reales con la meta inicial.'),('My score rose from four to six. This shows progress.','Mi puntuación subió de cuatro a seis. Esto muestra progreso.','Mejorar no significa necesariamente haber alcanzado la meta.'),('Noise was an obstacle, so I will study in a quiet room.','El ruido fue un obstáculo, así que estudiaré en una sala tranquila.','El ajuste debe responder al obstáculo identificado.'),('Keep the goal, but adjust the task or study time.','Mantén la meta, pero ajusta la tarea o el horario.','No abandones una meta alcanzable porque una estrategia haya fallado.'),('We will review my recordings next Friday to check the change.','Revisaremos mis grabaciones el próximo viernes para comprobar el cambio.','Acuerda fecha, evidencia y criterio para el próximo control.'),('I explain clearly but miss endings. I record answers to hear errors. My score improved, but noise interrupted practice. I will use a quiet room twice a week and check my next recording on Friday.','Explico con claridad, pero omito terminaciones. Grabo respuestas para oír errores. Mejoré, pero el ruido interrumpió la práctica. Usaré una sala tranquila dos veces por semana y revisaré la siguiente grabación el viernes.','Integra perfil, propósito, acción tras el comentario, plan medible y ajuste basado en evidencia.')]
        add('pg01','q','¿Qué ajuste responde al obstáculo de ruido?',['Practise in a quiet room at the same time.','Keep practising beside the loud television.','Replace the listening goal with copying words.'],'El lugar tranquilo reduce el ruido y conserva la habilidad que se quiere mejorar.')
        add('pg02','q','Meta: 8/10; antes: 3/10; ahora: 6/10. ¿Qué conclusión es válida?',['There is progress, but the goal is not reached.','There is no progress at all.','The goal has already been exceeded.'],'Seis supera tres, pero aún no alcanza ocho.')
        add('pg03','l','Escucha: ¿qué control se ha acordado?',('Keep the goal of ten correct forms. Practise shorter sessions before work. On Friday, bring two diary entries and we will count the correct forms.',['count correct forms in two entries on Friday','stop writing until the end of the month','count the number of empty diary pages']),'El control fija viernes, dos entradas y recuento de formas correctas.')
        add('p01','m','Relaciona cada resultado parcial con un ajuste justificado.',[('Evening fatigue caused missed sessions.','Move practice to the morning.'),('Long recordings were never completed.','Use shorter recordings with the same target sounds.'),('Unknown words interrupted every sentence.','Review the key words before the listening task.')],'Cada ajuste responde al obstáculo sin sustituir el objetivo por otra habilidad.')
        add('p02','l','Escucha a Tom: ¿qué evidencia demuestra avance?',('I still want nine correct answers. Last week I got five; today I got seven on the same type of quiz. I missed a session because of work.',['the score increased from five to seven','one session was missed','the goal is still nine']),'El cambio de puntuación es evidencia de avance; faltar es un obstáculo y nueve sigue siendo meta.')
        add('p03','o','Ordena el ajuste que mantiene la meta.','I will practise earlier to avoid tiredness','Practise earlier responde al cansancio mediante un cambio de horario.')
        add('e01','l','Caso A: escucha y selecciona un ajuste que conserve la meta.',('Maya explains ideas clearly but misses final sounds. She records answers to hear mistakes. Her score rose from five to seven out of ten; her goal is nine. Evening noise interrupted two sessions. Her tutor recommends a quiet room. They agree to practise there on Tuesday and Thursday and compare recordings next Friday.',['Use the quiet room twice a week and compare recordings on Friday.','Lower the goal to seven and stop recording.','Keep the noisy room and count pages copied on Friday.']),'El ajuste usa el consejo, conserva nueve de diez y acuerda evidencia y fecha.',requires=ALL)
        add('e02','q','Caso A: ¿qué combinación distingue fortaleza, dificultad y meta?',['clear ideas; missing final sounds; nine correct sounds','nine correct sounds; clear ideas; missing final sounds','missing final sounds; nine correct sounds; clear ideas'],'Las ideas claras ya son fortaleza; las terminaciones son el problema y nueve es la meta.',source='Maya explains ideas clearly, misses final sounds and aims for nine correct sounds out of ten.',requires=[ALL[0],ALL[4]])
        add('e03','q','Caso B: elige el ajuste con propósito y control verificable.',['Use shorter texts to practise evidence; compare four answers on Monday.','Stop checking evidence because the score improved.','Copy longer texts and count pages sometime next month.'],'Textos más cortos permiten completar la tarea; cuatro respuestas el lunes mantienen un control concreto.',source='Noah understands the main idea but gives answers without evidence. His tutor asks him to underline supporting lines. His score rose from two to three out of five; the target is four. Long texts prevent him finishing. They agree to use shorter texts and review four answers on Monday.',requires=ALL)
        source='Case B follow-up: Noah identifies the main idea well but answers without supporting evidence. Goal: four of five answers supported by a line from the text. Results: two before, three now. Obstacle: long texts cannot be finished in his study time. Tutor: use shorter texts, underline a supporting line for each answer. Revised plan: fifteen minutes on Monday, Wednesday and Friday for the next two weeks. Control: next Monday, bring four answers with underlined lines. Write as Noah: profile, progress, purpose, action, frequency, goal and agreed control.'
        a='I identify the main idea well, but I need evidence for my answers. My score rose from two to three out of five, so I have made progress. My goal is still four supported answers out of five. Long texts take too much time. Following my tutor’s advice, I will use shorter texts and underline supporting lines to explain my answers. I will practise for fifteen minutes on Monday, Wednesday and Friday for two weeks. Next Monday, I will bring four answers with underlined lines so that we can check whether this change helps.'
        add('e04','w','Caso B: revisa el plan en 90–120 palabras y justifica el ajuste.',[a,a.replace('I have made progress','my results have improved')],'La revisión usa dos a tres, textos demasiado largos, ajuste pertinente, meta constante y control del lunes.',source=source,requires=ALL)
        add('r01','q','Caso C: ¿qué conclusión permite el registro?',['Listening improved, but the target is still ahead.','The learner has already reached eight details.','The learner became worse at listening.'],'Pasar de cuatro a seis es progreso parcial hacia ocho detalles.',source='Iris aims to catch eight of ten details in voice messages. Her first score was four; her latest score is six.',requires=[ALL[0],ALL[4]])
        add('r02','l','Caso C: escucha y elige una acción que responda al comentario.',('Iris, you identify the speaker well, but you miss numbers. Your tutor recommends pausing after each number and writing it down. Practise at lunch because you are too tired at night.',['pause after each number and write it down at lunch','keep listening at night without writing numbers','practise speaker names instead of numbers']),'Pausar y anotar números responde a la dificultad; el almuerzo evita el cansancio.',requires=[ALL[2],ALL[4]])
        source='Case C: Iris identifies speakers well but misses numbers. Goal: catch eight of ten details in voice messages. Score: four before, six now. Obstacle: tiredness at night. Tutor recommends pausing after each number and writing it down. Adjustment: practise at lunch for ten minutes on Tuesday, Thursday and Saturday for two weeks. Evidence: dated answer sheets. Agreed check: compare the next sheet with the first one on Saturday. Write as Iris, keeping the goal and explaining why the strategy and schedule help.'
        a='I identify speakers well, but I still miss numbers in voice messages. My score improved from four to six, although my goal remains eight details out of ten. I am too tired at night, so I will practise at lunch. Following my tutor’s advice, I will pause after each number and write it down to check what I hear. I will study for ten minutes on Tuesday, Thursday and Saturday for two weeks. I will keep dated answer sheets as evidence. On Saturday, we will compare the next sheet with the first one to review my progress.'
        add('r03','w','Caso C: escribe una revisión de 90–120 palabras con el próximo control.',[a,a.replace('I still miss numbers','numbers are still difficult for me')],'La revisión conserva ocho detalles, reconoce seis y conecta horario, tarea y hojas fechadas con el control.',source=source,requires=ALL)
    vocab += {81:[('understand','entender')],82:[('practise','practicar'),('cards','tarjetas'),('check','comprobar')],83:[('reason','razón'),('answers','respuestas')],84:[('scores','puntuaciones')],85:[('record','grabar')]}[n]
    remediation={f'{p}.{key}':h.route(n,teaching,review) for key,(teaching,review) in REMEDIATION[n].items()}
    if n==85:
        remediation[f'{p}.e01']['reteachSteps']=[f'en.n3.class-85.t03',f'en.n3.class-85.t04',f'en.n3.class-85.t05']
        remediation[f'{p}.e01']['reviewSteps']=[f'{p}.r02',f'{p}.r03']
    doc=h.make_class(n,vocab,rows,pools,remediation)
    for pool in doc['pools'].values():
        for item in pool:
            if item['id'] in EVIDENCE_GROUPS:
                item['origin']['scoring']['evidenceGroups']=EVIDENCE_GROUPS[item['id']]
                h.content_hash(item)
    # Segment at clause boundaries; avoid the old helper's unaligned bilingual half-splits.
    for lesson in doc['teaching']:
        for separator in ['. ', '; ', ', but ', ' so that ', ' to ', ' before ', ': ', ' and ', ' is ']:
            if separator in lesson['en']:
                left,right=lesson['en'].split(separator,1)
                lesson['segments']=[left+separator,right]
                break
    if n==85: doc.update(usesPatterns=ALL,cumulativeEvaluation=ALL)
    return doc

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def generate(seed):
    h.VARIANT_SEED=seed; docs=[]; files=[]
    for n in NUMBERS:
        doc=build(n); docs.append(doc)
        path=OUT/f'class-{n}.json'; path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n'); files.append(path)
        subprocess.run(['python3',str(REPO/'tools/contenido/validar_bundle_editorial.py'),'--file',str(path),'--start',str(n),'--end',str(n),'--level','3'],check=True)
    bundle=OUT/'bundle-81-85.json'
    bundle.write_text(json.dumps(dict(schema='onelingo.editorial.class-bundle.v1',course='en',level=3,scale='client-10-levels-v1',status='shadow',runtimeAi=False,variantSeed=seed,selectionPolicy={'deterministic':True},evidencePolicy={'attemptRecords':['variantId','libraryVersion','selectionId']},range={'start':81,'end':85},classes=docs),ensure_ascii=False,indent=2)+'\n'); files.append(bundle)
    subprocess.run(['python3',str(REPO/'tools/contenido/validar_bundle_editorial.py'),'--file',str(bundle),'--start','81','--end','85','--level','3'],check=True)
    for doc in docs:
        assert [len(doc['pools'][k]) for k in doc['pools']]==[3,3,4,3]
        for pool in doc['pools'].values():
            for item in pool:
                if item['format']=='escribir':
                    low,high=item['origin']['scoring']['wordRange']
                    assert all(low<=len(re.findall(r"\b[\w’-]+\b",text))<=high for text in item['answer']['accepted']), item['id']
                    normal=lambda value:' '.join(re.findall(r'[a-z0-9]+',value.lower()))
                    matches=lambda text:all(any(normal(phrase) in normal(text) for phrase in group) for group in item['origin']['scoring']['evidenceGroups'])
                    for model in item['answer']['accepted']:
                        assert matches(model),item['id']
                        paraphrase=model.replace('My goal is','My aim is').replace('My score rose','My score increased').replace('I identify speakers well','I can identify speakers well')
                        assert matches(paraphrase),item['id']+' paraphrase'
                        assert low<=len(re.findall(r"\b[\w’-]+\b",paraphrase))<=high
                    target,wrong={
                        'en.n3.c84.p03':('sixteen of twenty','six of twenty'),
                        'en.n3.c84.e04':('eight of ten dates','two of ten dates'),
                        'en.n3.c84.r03':('nine of ten past forms','two of ten past forms'),
                        'en.n3.c85.e04':('four supported answers out of five','two supported answers out of five'),
                        'en.n3.c85.r03':('eight details out of ten','two details out of ten'),
                    }[item['id']]
                    assert not matches(item['answer']['accepted'][0].replace(target,wrong)),item['id']+' wrong target'
    REPORT_OUT.mkdir(parents=True,exist_ok=True)
    report=REPORT_OUT/'REPORT.md'
    report.write_text('# INTEGRADO — Inglés N3 C81–C85\n\nEstado: integrado en shadow tras corrección y GO independiente.\n\n65 ítems; cada clase contiene 3 guiados, 3 independientes, 4 evaluativos y 3 repasos. Fuentes visibles, feedback específico, remediación determinista, shadow y runtimeAi=false.\n\nC81: cinco clasificaciones de fortalezas, dificultades y metas. C82: seis propósitos con to/so that. C83: tutoría con logro, problema y acción. C84: planes de dos semanas, 80–100 palabras. C85: tres escenarios (Maya/pronunciación, Noah/lectura, Iris/escucha), revisión de 90–120 palabras, cinco conceptos acumulativos.\n\nValidación individual y bundle ejecutada por el generador. La auditoría independiente confirmó GO tras simulación de respuestas naturales. Escrituras: dos variantes deterministas; el corrector local no equivale a aceptar cualquier paráfrasis semántica.\n\nEl vocabulario y las firmas estímulo-respuesta están preservados en cada JSON (vocabulary, usesVocabulary, origin, answer, contentHash). Infraestructura de esquema compartida con C66–70; contenido redactado de nuevo.\n')
    report.write_text(report.read_text()+'\n## Corrección tras REVISE\n\nLas cinco escrituras extensas incluyen evidenceGroups: cada criterio es obligatorio y admite frases equivalentes; se conserva wordRange. Se verifican ambos modelos, las paráfrasis My aim is / My score increased / I can identify speakers well y el rechazo al sustituir la meta numérica por otra. Esto amplía la corrección determinista, sin afirmar comprensión semántica ilimitada. Las veinte remediaciones son explícitas por habilidad. C81 e02 reenseña metas y practica clasificación; C85 e01 reenseña ajuste y control con recuperación de escucha y producción; C85 e02 recupera el perfil completo. C82 e03 no depende de la posición de una opción.\n')
    evidence=REPORT_OUT/'AUTHOR_EVIDENCE.json'
    evidence.write_text(json.dumps({'status':'INTEGRATED','independentReview':'GO','mapDigest':digest(MAP),'previousClassDigest':digest(REPO/'assets/contenido/en/editorial/n3/class-80.json'),'assumptions':['N3 B1 map overrides the generic A2 wording in the protocol.','Writing uses deterministic accepted variants; unrestricted semantic grading is not claimed.'],'classes':[{'id':d['id'],'formats':sorted({i['format'] for pool in d['pools'].values() for i in pool}),'skills':d['skills'],'concepts':d['usesPatterns'],'vocabularyIntroduced':d['usesVocabulary'] if d['id'].endswith('81') else [v for v in d['usesVocabulary'] if v not in {w for old in docs[:docs.index(d)] for w in old['usesVocabulary']}],'vocabularyReusedWithinBlock':[v for v in d['usesVocabulary'] if v in {w for old in docs[:docs.index(d)] for w in old['usesVocabulary']}],'signatures':[{'id':i['id'],'contentHash':i['contentHash']} for pool in d['pools'].values() for i in pool]} for d in docs]},ensure_ascii=False,indent=2)+'\n')
    files.extend([report,evidence])
    manifest=REPORT_OUT/'MANIFEST.sha256'
    entries=[
        f'{digest(__file__)}  ../../tools/contenido/generar_editorial_n3_81_85.py',
        f'{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json',
        f'{digest(HELPER)}  ../../tools/contenido/generar_editorial_n3_66_70.py',
    ]
    entries.extend(f'{digest(x)}  ../../{x.relative_to(REPO)}' for x in files if x.parent==OUT)
    entries.extend(f'{digest(x)}  {x.name}' for x in files if x.parent==REPORT_OUT)
    manifest.write_text('\n'.join(entries)+'\n')
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--all',action='store_true'); ap.add_argument('--variant-seed',default='0'); args=ap.parse_args(); generate(args.variant_seed)

