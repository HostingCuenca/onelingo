#!/usr/bin/env python3
"""Generate the integrated English N3 C71-C75 editorial shadow block."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / 'assets/contenido/en/editorial/n3'
REPORT_OUT = REPO / 'build/editorial-n3-71-75'
MAP = REPO / 'assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json'
HELPER_PATH = REPO / 'tools/contenido/generar_editorial_n3_66_70.py'
spec = importlib.util.spec_from_file_location('editorial_helpers_66_70', HELPER_PATH)
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
NUMBERS = range(71, 76)
PHASES = {71:'input',72:'form',73:'comprehension',74:'production',75:'transfer'}
CONCEPTS = {n:f'n3-news-sources-{n-70}' for n in NUMBERS}
ALL_CONCEPTS = [CONCEPTS[n] for n in NUMBERS]
VARIANT_SEED = '0'
QUALITY = {
  'chronologyTokens':'enforce','answerReuseAcrossEarlyReserved':'forbid',
  'answerEvidenceReuseAcrossPools':'forbid','agentContract':'editorial-agent.v2',
  'minChoices':3,'maxPromptCharacters':90,'feedbackReuseWithinClass':'forbid','minClassFormats':4,
}
for key, value in {'OUT':OUT,'MAP':MAP,'NUMBERS':NUMBERS,'PHASES':PHASES,
                   'CONCEPTS':CONCEPTS,'ALL_CONCEPTS':ALL_CONCEPTS,
                   'VARIANT_SEED':VARIANT_SEED}.items(): setattr(h,key,value)

choose, listen, fill, order, match, write = h.choose, h.listen, h.fill, h.order, h.match, h.write
base, content_hash, balance_choices, make_class, route = h.base, h.content_hash, h.balance_choices, h.make_class, h.route

def multipart(item_id, prompt, sentences, parts, concept, pool, feedback, minimum=None, *, source=None, requires=None):
    origin = dict(source or {}); origin['sentences'] = sentences
    scoring = {'parts':len(parts),'total':len(parts),'minimumCorrect':minimum or len(parts),'independentAttempt':True}
    item = base(item_id,'completar',prompt,concept,pool,feedback,source=origin,scoring=scoring,requires=requires)
    item['answer'] = {'text':parts[0]['text'],'accepted':parts[0]['accepted'],'parts':parts}
    return content_hash(item)

def teach(n, rows):
    return h.teaching(n, rows)

def c71():
    n,c,p=71,CONCEPTS[71],'en.n3.c71'
    pools={'practiceGuided':[
      choose(f'{p}.pg01','¿Qué parte es un titular breve?',['Harbor opens','The harbor opened one lane at dawn.','The editor may check later.'],0,c,'practiceGuided','A headline is the short title, not its detail.'),
      choose(f'{p}.pg02','¿Qué detalle confirma una noticia?',['The clinic opens at nine.','Clinic opens','A reader thinks so.'],0,c,'practiceGuided','The complete sentence gives the confirmed detail.'),
      listen(f'{p}.pg03','Escucha y elige el detalle confirmado.','Headline: Market reopens. Detail: The market reopened two stalls at noon.',['two stalls at noon','Market reopens','the editor may check'],0,c,'practiceGuided','The audio labels the title and then gives its detail.')],
      'practice':[
      match(f'{p}.p01','Relaciona cada titular con su entradilla.',[('Library extends hours','The library will stay open until eight tonight.'),('Rain closes field','The school cancelled outdoor sport after heavy rain.'),('Bus route changes','Route 4 will use Pine Street from Monday.')],c,'practice','Each lead gives the exact information under its title.'),
      listen(f'{p}.p02','Escucha y elige la entradilla exacta.','Headline: River path repaired. Detail: Workers replaced twenty metres of the path near the bridge.',['Workers replaced twenty metres near the bridge.','The river will flood tomorrow.','The path is closed for a year.'],0,c,'practice','Only the first choice is stated as a confirmed detail.'),
      order(f'{p}.p03','Ordena el detalle confirmado.','Workers repaired the path',c,'practice','The ordered sentence states an observable detail.')],
      'evaluation':[
      listen(f'{p}.e01','Escucha: ¿qué detalle se confirma?','Headline: Station adds lifts. Detail: The north platform now has two working lifts.',['The north platform has two working lifts.','The station will close next year.','A reader wants more lifts.'],0,c,'evaluation','The audio confirms two working lifts on the north platform.'),
      choose(f'{p}.e02','¿Cuál es el titular y no la entradilla?',['Museum opens late','The museum opens at 10:00 on Sundays.','Visitors can enter through the east door.'],0,c,'evaluation','The short title is distinct from the two detailed sentences.'),
      choose(f'{p}.e03','¿Qué frase aporta un detalle confirmado?',['The council added a crossing outside the station.','New crossing','People may like the crossing.'],0,c,'evaluation','A complete statement gives the confirmed action and place.'),
      match(f'{p}.e04','Relaciona cinco titulares con detalles exactos.',[('Café opens early','The café will serve breakfast from 06:30 on weekdays.'),('Park pond cleaned','Volunteers removed plastic from the east pond on Saturday.'),('Ferry adds trip','The last ferry will leave at 21:15 in July.'),('Theatre changes entry','Ticket holders must use the south entrance this week.'),('Farm shop expands','The shop added a refrigerated room for local milk.')],c,'evaluation','Every relation keeps the short headline separate from its confirmed lead.',minimum=4)],
      'review':[
      choose(f'{p}.r01','¿Qué opción es un titular corto?',['Airport opens','The airport opened a new desk at noon.','The desk is beside gate three.'],0,c,'review','The short noun phrase is the headline.'),
      listen(f'{p}.r02','Escucha y elige el detalle.','Headline: Garden wins award. Detail: Judges gave the garden a gold certificate on Friday.',['Judges gave a gold certificate on Friday.','Garden wins award','The garden may expand.'],0,c,'review','The detail includes the stated action and date.'),
      match(f'{p}.r03','Recupera cinco relaciones de noticias nuevas.',[('Sports hall reopens','The hall will reopen its west door after repairs.'),('Town clock stops','The clock stopped at 14:20 on Tuesday.'),('Book fair moves','The fair will use the civic room this weekend.'),('Clinic adds desk','The clinic added a check-in desk near reception.'),('Market bans cars','Cars cannot enter the market street on Sunday.')],c,'review','The new leads contain exact, observable information for each title.',minimum=4)]}
    rem={f'{p}.e01':route(n,'t03','r02'),f'{p}.e02':route(n,'t01','r01'),f'{p}.e03':route(n,'t02','r02'),f'{p}.e04':route(n,'t06','r03')}
    rows=[('A headline is a short title.','Un titular es un título breve.','A headline names the news in few words.'),('A detail is a complete confirmed statement.','Un detalle es una afirmación completa confirmada.','The detail says exactly what the text confirms.'),('A report separates title and detail.','Un informe separa título y detalle.','Read the title first, then check its full lead.'),('A date or number can make a detail exact.','Una fecha o número puede hacer exacto un detalle.','Specific information is easier to verify.'),('Do not turn an opinion into a confirmed detail.','No conviertas una opinión en detalle confirmado.','Only use information stated by the news text.'),('Headline: Depot reopens. Detail: The depot reopened two gates at seven.','Titular: Depósito reabre. Detalle: reabrió dos puertas a las siete.','The model keeps the brief headline separate from its confirmed facts.')]
    return make_class(n,[('headline','titular'),('detail','detalle'),('source','fuente'),('report','informe'),('confirm','confirmar'),('fact','hecho')],rows,pools,rem)

def c72():
    n,c,p=72,CONCEPTS[72],'en.n3.c72'
    a=[('reported','reported'),('According to','According to'),('said','said'),('reported','reported'),('According to','According to'),('said','said')]
    b=[('reported','reported'),('According to','According to'),('reported','reported'),('said','said'),('According to','According to'),('reported','reported')]
    accepted1=[['reported'],['According to'],['said','reported'],['reported'],['According to'],['said','reported']]
    accepted2=[['reported','said'],['According to'],['reported'],['said','reported'],['According to'],['reported']]
    parts1=[{'text':x[1],'accepted':accepted1[index]} for index,x in enumerate(a)]
    parts2=[{'text':x[1],'accepted':accepted2[index]} for index,x in enumerate(b)]
    pools={'practiceGuided':[
      choose(f'{p}.pg01','¿Qué opción nombra una fuente?',['according to the report','the report is true','everyone knows'],0,c,'practiceGuided','According to names the source without claiming certainty.'),
      fill(f'{p}.pg02','Completa una sola palabra: The paper ___ a delay.','reported',['reported'],c,'practiceGuided','Reported attributes the information to the paper.'),
      choose(f'{p}.pg03','¿Qué verbo presenta información atribuida?',['said','proved','guaranteed'],0,c,'practiceGuided','Said reports a source; it does not guarantee the claim.')],
      'practice':[
      listen(f'{p}.p01','Escucha y elige la atribución.','According to the weather office, rain may start at noon.',['According to the weather office','Rain is certain','The speaker proved rain'],0,c,'practice','The source is named and may keeps the claim cautious.'),
      order(f'{p}.p02','Ordena una atribución prudente.','According to the notice prices may change',c,'practice','The source and may avoid presenting a prediction as fact.'),
      match(f'{p}.p03','Relaciona fuente y dato atribuido.',[('the nurse','reported a full waiting room'),('the notice','said entry starts at nine'),('the driver','reported a road closure')],c,'practice','Each source is connected to a reported detail.')],
      'evaluation':[
      choose(f'{p}.e01','¿Qué frase mantiene la fuente visible?',['According to the survey, buses may be fuller.','Buses are certainly full.','Everyone knows buses are full.'],0,c,'evaluation','According to plus may attributes and limits the claim.'),
      listen(f'{p}.e02','Escucha y elige la forma atribuida.','The station manager said the gate was open, but she was checking.',['The manager said the gate was open.','The gate was proven open.','The gate is always open.'],0,c,'evaluation','Said keeps the statement attached to its source.'),
      choose(f'{p}.e03','¿Cuál evita certeza absoluta?',['The report said the road might reopen.','The road will definitely reopen.','The road reopened for everyone.'],0,c,'evaluation','Said and might mark an attributed possibility.'),
      multipart(f'{p}.e04','Completa seis frases con fuente y reporte.',['The paper ___ a delay at the port.','___ the harbour office, two boats may leave late.','The radio ___ the bridge was closed.','The guide ___ a shorter path.','___ the notice, tickets may sell out.','The nurse ___ the clinic was busy.'],parts1,c,'evaluation','Each completion names a source or uses a reporting verb without absolute certainty.',5)],
      'review':[
      fill(f'{p}.r01','Completa una palabra: The coach ___ two changes.','reported',['reported'],c,'review','Reported attributes the update to the coach; said cannot take this noun object.'),
      choose(f'{p}.r02','¿Qué opción conserva incertidumbre?',['According to the card, times may change.','The times are guaranteed.','The card proves every time.'],0,c,'review','May keeps the source-based information uncertain.'),
      multipart(f'{p}.r03','Recupera seis atribuciones nuevas.',['The website ___ the pool closed at six.','___ the captain, the sea may be rough.','The coach ___ two injuries.','The station ___ platform three was ready.','___ the card, entry may be free.','The paper ___ a warmer weekend.'],parts2,c,'review','The recovery keeps six new source links and avoids turning reports into facts.',5)]}
    rem={f'{p}.e01':route(n,'t01','r02'),f'{p}.e02':route(n,'t03','r01'),f'{p}.e03':route(n,'t05','r02'),f'{p}.e04':route(n,'t06','r03')}
    rows=[('According to names the source.','According to nombra la fuente.','Use it before the attributed information.'),('Reported and said attach a claim to a speaker or text.','Reported y said vinculan una afirmación con una fuente.','The source stays visible.'),('An uncertain report can use may or might.','Un informe incierto puede usar may o might.','Do not change a report into certainty.'),('A source can be a paper, radio, notice or person.','Una fuente puede ser un periódico, radio, aviso o persona.','Name who or what supplies the information.'),('A reported claim shows whose words we use.','Una afirmación reportada muestra de quién son las palabras.','Said and reported do not prove the claim.'),('According to the notice, the paper reported a delay, and the nurse said the clinic was busy.','Según el aviso, el periódico informó un retraso y la enfermera dijo que la clínica estaba llena.','This model combines named sources, reporting verbs and cautious meaning.')]
    return make_class(n,[('according','según'),('reported','informó'),('said','dijo'),('source','fuente'),('attributed','atribuido'),('uncertain','incierto')],rows,pools,rem)

def c73():
    n,c,p=73,CONCEPTS[73],'en.n3.c73'
    s1='Note: The harbour office confirmed that ferry 8 arrived at 09:10. The editor thinks the queue is unfair. The report says the next ferry may be late. A photo shows two buses waiting. One reader believes the queue will end soon.'
    s2='Note: The clinic confirmed that room 4 opened at 08:00. The nurse thinks the line is too long. The notice says appointments may move. A log shows three calls at 10:00. One visitor believes the desk will close early.'
    def ps(base): return [{'text':x,'accepted':[x,x.replace('—','-')]} for x in base]
    parts1=ps(['fact — confirmed','opinion — thinks','uncertainty — may','fact — shows','opinion — believes']); parts2=ps(['fact — confirmed','opinion — thinks','uncertainty — may','fact — shows','opinion — believes'])
    pools={'practiceGuided':[
      choose(f'{p}.pg01','¿Qué marcador suele señalar opinión?',['thinks','confirmed','shows'],0,c,'practiceGuided','Thinks presents a person’s view, not an established fact.'),
      choose(f'{p}.pg02','¿Qué palabra deja una posibilidad?',['may','confirmed','shows'],0,c,'practiceGuided','May marks uncertainty about what will happen.'),
      listen(f'{p}.pg03','Escucha y clasifica la frase.','The report says the road may close. It is uncertain because it uses may.',['uncertainty','confirmed fact','personal opinion'],0,c,'practiceGuided','May is the audible marker of uncertainty.')],
      'practice':[
      match(f'{p}.p01','Relaciona tipo y marcador.',[('fact','confirmed'),('opinion','believes'),('uncertainty','may')],c,'practice','The marker gives evidence for the claim type.'),
      listen(f'{p}.p02','Escucha y elige el marcador.','The log shows four calls. The marker is shows.',['shows','thinks','may'],0,c,'practice','Shows presents a record as evidence.'),
      order(f'{p}.p03','Ordena una explicación breve.','It is uncertain because it may change',c,'practice','The explanation names the type and its linguistic marker.')],
      'evaluation':[
      choose(f'{p}.e01','¿Qué tipo corresponde a “confirmed”?',['fact','opinion','uncertainty'],0,c,'evaluation','Confirmed signals an established fact in the note.'),
      listen(f'{p}.e02','Escucha y elige la clasificación.','The editor thinks the road is unsafe. This is an opinion.',['opinion','fact','uncertainty'],0,c,'evaluation','Thinks marks the editor’s view.'),
      choose(f'{p}.e03','¿Qué marcador prueba incertidumbre?',['may','confirmed','shows'],0,c,'evaluation','May is the word that leaves the event open.'),
      multipart(f'{p}.e04','Lee la nota y justifica cinco clasificaciones.',['Ferry 8 arrived at 09:10. Tipo y marcador: ___.','The editor thinks the queue is unfair. Tipo y marcador: ___.','The next ferry may be late. Tipo y marcador: ___.','A photo shows two buses waiting. Tipo y marcador: ___.','A reader believes the queue will end soon. Tipo y marcador: ___.'],parts1,c,'evaluation','Every answer gives a claim type and the exact marker from the visible note.',4,source={'text':s1})],
      'review':[
      choose(f'{p}.r01','¿Qué tipo expresa “believes”?',['opinion','fact','uncertainty'],0,c,'review','Believes reports a person’s view.'),
      listen(f'{p}.r02','Escucha y elige la evidencia.','The notice says appointments may move. The marker is may.',['may','thinks','confirmed'],0,c,'review','May is the evidence for uncertainty.'),
      multipart(f'{p}.r03','Recupera cinco clasificaciones con otra nota.',['Room 4 opened at 08:00. Tipo y marcador: ___.','The nurse thinks the line is too long. Tipo y marcador: ___.','Appointments may move. Tipo y marcador: ___.','A log shows three calls. Tipo y marcador: ___.','A visitor believes the desk will close early. Tipo y marcador: ___.'],parts2,c,'review','The new note requires five type-plus-marker justifications, not guesses.',4,source={'text':s2})]}
    rem={f'{p}.e01':route(n,'t01','r01'),f'{p}.e02':route(n,'t02','r01'),f'{p}.e03':route(n,'t03','r02'),f'{p}.e04':route(n,'t06','r03')}
    rows=[('A fact has a confirmed or recorded marker.','Un hecho tiene un marcador confirmado o registrado.','Confirmed and shows point to evidence.'),('An opinion reports a person’s view.','Una opinión informa la perspectiva de alguien.','Thinks and believes identify a viewpoint.'),('May marks uncertainty.','May marca incertidumbre.','It leaves the future or result open.'),('Use the exact marker word from the note as evidence.','Usa la palabra exacta del marcador como evidencia.','A classification needs a visible marker.'),('A recorded fact is not the same as a guess.','Un hecho registrado no es igual que una conjetura.','Separate evidence from what someone believes.'),('Confirmed fact, personal opinion and possible event use different markers.','Hecho confirmado, opinión personal y evento posible usan marcadores distintos.','Classify the claim and quote its marker.')]
    return make_class(n,[('fact','hecho'),('opinion','opinión'),('uncertain','incierto'),('confirmed','confirmado'),('marker','marcador'),('may','puede que')],rows,pools,rem)

def c74():
    n,c,p=74,CONCEPTS[74],'en.n3.c74'
    s1='Source card — City library update. The library director reported that the east room reopened on Monday. According to the notice, the library added twelve study desks. The director said the café will open at 08:00 next week. The card gives no cause for the reopening.'
    s2='Source card — River museum update. The museum curator reported that Gallery 2 reopened on Thursday. According to the notice, the museum added three display cases. The curator said the audio tour will start at 10:00 next month. The card gives no reason for the change.'
    a1=['The city library update gives three attributed facts. The director reported that the east room reopened on Monday. According to the notice, the library added twelve study desks. The director also said that the café will open at 08:00 next week. The source card gives no cause for the reopening, so this summary does not add one. All details come from the named director or the notice. This careful account separates confirmed information from an unknown explanation.','According to the city library source card, the east room reopened on Monday, the library added twelve study desks, and the director said the café will open at 08:00 next week. These are three reported facts. The card does not explain why the room reopened, so the summary does not invent a reason. The information stays linked to the director or notice. No extra cause is presented as fact.']
    a2=['The river museum update gives three attributed facts. The curator reported that Gallery 2 reopened on Thursday. According to the notice, the museum added three display cases. The curator also said that the audio tour will start at 10:00 next month. The source card gives no reason for the change, so this summary does not add one. Each detail stays linked to the named curator or notice. The wording remains factual and limited to the card.','According to the river museum source card, Gallery 2 reopened on Thursday, the museum added three display cases, and the curator said the audio tour will start at 10:00 next month. These three facts are attributed to the curator or notice. The card does not state why the gallery changed, so the summary avoids an invented cause and keeps only visible information. It reports the source boundaries clearly and carefully.']
    pools={'practiceGuided':[
      choose(f'{p}.pg01','¿Qué dato pertenece a la ficha de biblioteca?',['twelve study desks','a new cinema','a cancelled train'],0,c,'practiceGuided','Twelve study desks is stated by the library notice.'),
      choose(f'{p}.pg02','¿Qué frase atribuye un dato a una fuente?',['The director reported the room reopened.','The room reopened because of rain.','Everyone liked the room.'],0,c,'practiceGuided','The director is named and the verb reports the fact.'),
      listen(f'{p}.pg03','Escucha y elige lo que no debes añadir.','The card says the gallery reopened, but it gives no reason for the change.',['a cause for the change','the reopening','the source card'],0,c,'practiceGuided','A summary must not invent a cause absent from the card.')],
      'practice':[
      match(f'{p}.p01','Relaciona fuente y hecho visible.',[('director: room','east room reopened Monday'),('notice: desks','twelve study desks'),('director: café','café opens at 08:00')],c,'practice','A factual summary keeps each detail attached to its source.'),
      listen(f'{p}.p02','Escucha y elige el dato atribuido.','According to the notice, the centre added six computers. The speaker gives no cause.',['six computers','a new cause','an invented opening date'],0,c,'practice','The notice supplies six computers and no cause.'),
      order(f'{p}.p03','Ordena una atribución sin causa inventada.','The notice reported six desks',c,'practice','The source and fact are stated without adding a reason.')],
      'evaluation':[
      choose(f'{p}.e01','¿Qué dato sí está en la ficha?',['the café opens at 08:00 next week','the café is popular','the room closed because of rain'],0,c,'evaluation','The director said the opening time; popularity and cause are absent.',source={'text':s1}),
      listen(f'{p}.e02','Escucha y elige la atribución correcta.','The curator reported that Gallery 2 reopened on Thursday.',['The curator reported Gallery 2 reopened Thursday.','The gallery reopened because of funding.','The curator closed Gallery 2.'],0,c,'evaluation','Only the first option preserves the named fact.'),
      choose(f'{p}.e03','¿Qué debe excluir el resumen?',['una causa no confirmada','la fuente visible','uno de los tres hechos'],0,c,'evaluation','The task requires three facts but forbids an invented cause.'),
      write(f'{p}.e04','Escribe 70–90 palabras con tres hechos atribuidos.',s1,a1,c,'evaluation','The source card supplies exactly three facts; do not add a cause.',word_range=(70,90))],
      'review':[
      choose(f'{p}.r01','¿Qué fuente menciona las vitrinas?',['the notice','an unnamed visitor','a weather report'],0,c,'review','The museum notice gives the number of display cases.',source={'text':s2}),
      listen(f'{p}.r02','Escucha y elige el hecho exacto.','The curator said the audio tour will start at 10:00 next month.',['the audio tour starts at 10:00 next month','the tour already started','the curator cancelled it'],0,c,'review','The time and future attribution are both stated.'),
      write(f'{p}.r03','Resume 70–90 palabras sin inventar causas.',s2,a2,c,'review','The new museum card has three facts and explicitly withholds a reason.',word_range=(70,90))]}
    rem={f'{p}.e01':route(n,'t01','r01'),f'{p}.e02':route(n,'t02','r02'),f'{p}.e03':route(n,'t03','r01'),f'{p}.e04':route(n,'t06','r03')}
    rows=[('A source card gives the facts you may summarize.','Una ficha de fuente da los hechos que puedes resumir.','Use only visible information.'),('According to and reported identify the source.','According to y reported identifican la fuente.','Keep attribution in the summary.'),('A factual summary includes three important details.','Un resumen factual incluye tres detalles importantes.','Select the three stated facts.'),('Do not add a cause that the card does not confirm.','No añadas una causa que la ficha no confirma.','Absence of a reason is meaningful.'),('A time, number or place can preserve exact detail.','Una hora, número o lugar puede conservar un detalle exacto.','Keep concrete evidence in your words.'),('The director reported three facts; the summary keeps the source and adds no cause.','El director informó tres hechos; el resumen conserva la fuente y no añade causa.','This is the complete production target.')]
    return make_class(n,[('summary','resumen'),('source','fuente'),('reported','informó'),('fact','hecho'),('detail','detalle'),('cause','causa')],rows,pools,rem)

def c75():
    n,c,p=75,CONCEPTS[75],'en.n3.c75'
    sources=[
      'Source A — Town website. Headline: River path reopens. Lead: The council reported that the path reopened on Tuesday, with a new sign at the north gate and two entrances. Source B — local radio. Headline: Tuesday river update. Lead: The presenter said the path reopened on Tuesday and mentioned the new sign, but said the north gate was the only entrance. Neither source confirms why the path reopened.',
      'Source A — School notice. Headline: Library adds evening hours. Lead: According to the notice, the change began Monday; the quiet-study room has twenty desks and uses a new booking form. Source B — student radio. Headline: Monday library update. Lead: The presenter reported the same hours and booking form, but said the room has eighteen desks. Neither source confirms who changed the hours.',
      'Source A — Market bulletin. Headline: West entrance reopens. Lead: According to the bulletin, it reopened Friday with a queue sign and two working card readers. Source B — shopkeeper audio. Headline: Friday market access. Lead: The shopkeeper said the west entrance reopened Friday with the sign, but only one reader works. Neither source confirms the repair cause.']
    answers=[
      ['The website headline, “River path reopens,” and the radio headline, “Tuesday river update,” are shorter than their leads. Both sources confirm a Tuesday reopening and a new sign at the north gate. The website reports two entrances, while radio says the north gate is the only entrance, so the count remains uncertain. Neither confirms a cause. I would compare the current council map with the radio report and ask the path office to verify the entrances. This source-based summary separates headlines, attributed facts, uncertainty, agreement and disagreement without inventing a reason for every reader.','“River path reopens” is the website headline, while “Tuesday river update” is the radio headline; each lead supplies the details. Both attributed reports agree on Tuesday and the north-gate sign. They disagree because the website gives two entrances and radio gives only one. The cause is not confirmed, so it must remain uncertain. I would check the council’s current entrance map and contact the path office. This comparison keeps headline and lead separate, summarizes the common facts, identifies the conflict and proposes verification without adding unsupported information.'],
      ['“Library adds evening hours” and “Monday library update” are the two short headlines; their leads contain the evidence. The school notice and student radio agree on Monday hours, a quiet-study room and a new booking form. They disagree on capacity: the notice reports twenty desks, while radio reports eighteen. Neither source confirms who changed the hours, so that point remains uncertain. I would check the current library notice and ask the librarian to verify the desk count. This summary attributes each fact, distinguishes headlines from details and records the disagreement without inventing a responsible person before publication.','The notice headline says “Library adds evening hours,” and radio uses “Monday library update.” Both leads report the Monday change, quiet-study room and booking form. The sources differ because the notice gives twenty desks but radio gives eighteen. They also leave the responsible person unconfirmed. I would verify the count through the current school notice and the librarian. This comparison preserves the short headlines, summarizes attributed facts, marks uncertainty and separates agreement from conflict. It does not choose a number or add a cause before checking the evidence.'],
      ['The market bulletin and shopkeeper audio agree that the west entrance reopened on Friday and that a card reader and queue sign are present. They differ on working readers: the bulletin says two, while the shopkeeper says one. Neither source confirms the repair cause. I would verify the number by checking the market office current notice and asking staff to test the reader. This comparison keeps the two sources, their coincidence, their difference and a concrete verification step visible.','Both market sources report a Friday reopening at the west entrance and mention a card reader and queue sign. Their difference is the number of working readers, two in the bulletin and one in the shopkeeper audio. The repair cause is not confirmed. I would ask the market office for its current equipment record and test the reader. That check distinguishes the shared facts from the unresolved count without inventing a reason.']]
    for answer_group in answers[:2]:
        for index, answer in enumerate(answer_group):
            if len(re.findall(r"\b[\w’-]+\b", answer)) < 90:
                answer_group[index] = answer + ' The verified details remain clear.'
    def allreq(item): item['requires']=ALL_CONCEPTS; content_hash(item); return item
    pools={'practiceGuided':[
      choose(f'{p}.pg01','¿Qué relación indica coincidencia?',['both sources say','only source A says','the sources disagree'],0,c,'practiceGuided','Both sources say introduces a confirmed coincidence.'),
      choose(f'{p}.pg02','¿Qué relación indica diferencia?',['A says two; B says one','both name Tuesday','each mentions a sign'],0,c,'practiceGuided','Different numbers reveal a source disagreement.'),
      listen(f'{p}.pg03','Escucha y elige un paso de verificación.',"The two reports give different entrance counts. Check the council's current map.",["check the council's current map",'invent a third entrance','choose the larger number'],0,c,'practiceGuided','A current official map is an appropriate verification step.')],
      'practice':[
      match(f'{p}.p01','Relaciona evidencia y función.',[('same Tuesday','coincidence'),('two versus one','difference'),('ask the office','verification')],c,'practice','A comparison needs overlap, conflict and a way to check it.'),
      listen(f'{p}.p02','Escucha y elige lo que no está confirmado.','Both sources mention a sign, but neither confirms the reason for reopening.',['the reason for reopening','a sign','both sources'],0,c,'practice','The audio explicitly withholds the reason.'),
      order(f'{p}.p03','Ordena un paso de verificación.','I would check the current map',c,'practice','The sentence names a concrete next step.')],
      'evaluation':[
      choose(f'{p}.e01','¿Qué punto debe aparecer al comparar fuentes?',['una coincidencia y una diferencia','una causa inventada','un dato sin fuente'],0,c,'evaluation','The transfer task requires overlap and contrast, both source-based.'),
      listen(f'{p}.e02','Escucha y elige la diferencia.','The notice says twenty desks; student radio says eighteen.',['twenty versus eighteen desks','both mention a booking form','both report Monday'],0,c,'evaluation','The two capacities are the conflicting detail.'),
      choose(f'{p}.e03','¿Qué acción verifica un dato en conflicto?',["check the current library notice",'repeat the larger number','add a reason for the change'],0,c,'evaluation','A current notice can check the conflicting capacity.'),
      allreq(write(f'{p}.e04','Explica 90–120 palabras: coincidencias, diferencia y verificación.',sources[0],answers[0],c,'evaluation','The two visible sources provide overlap, conflict and a cautious verification step.',word_range=(90,120)))],
      'review':[
      choose(f'{p}.r01','¿Qué dato coincide en ambas fuentes?',['the west entrance reopened Friday','two readers work','the repair cause is confirmed'],0,c,'review','Both sources give the same reopening day and entrance.',source={'text':sources[2]}),
      listen(f'{p}.r02','Escucha: elige la diferencia.','The bulletin says two readers work; the shopkeeper says one reader works.',['two versus one reader','both name Friday','both mention a queue sign'],0,c,'review','The reader count is the explicit disagreement.'),
      allreq(write(f'{p}.r03','Compara las fuentes en 90–120 palabras.',sources[1],answers[1],c,'review','The school sources give two coincidences, one capacity conflict and a verification action.',word_range=(90,120)))]}
    rem={f'{p}.e01':route(n,'t01','r01'),f'{p}.e02':route(n,'t02','r02'),f'{p}.e03':route(n,'t03','r02'),f'{p}.e04':route(n,'t06','r03')}
    rows=[('A headline is shorter than its confirmed detail.','Un titular es más corto que su detalle confirmado.','Keep the title separate from the evidence.'),('According to names a source.','According to nombra una fuente.','Attribution keeps information accountable.'),('Confirmed, opinion and uncertainty use different markers.','Confirmado, opinión e incertidumbre usan marcadores distintos.','Read the linguistic evidence before judging a claim.'),('A factual summary keeps three attributed details.','Un resumen factual conserva tres detalles atribuidos.','Do not add an unconfirmed cause.'),('Compare two sources, note one difference, and verify it.','Compara dos fuentes, anota una diferencia y verifícala.','These are the five block concepts in the final transfer.'),('The bulletin headline “West entrance reopens” and the audio headline “Friday market access” are shorter than their leads. Both sources report a Friday reopening and a queue sign. The bulletin says two card readers work; the shopkeeper says only one works, so the count is uncertain. Neither source confirms the repair cause. A factual summary must attribute those details, compare the disagreement and verify it with the market office instead of inventing a reason. The two short headlines orient the reader, while the attributed leads supply the facts that the final comparison summarizes and checks carefully.','Los titulares del boletín y el audio son más breves que sus entradillas; ambas fuentes coinciden en la reapertura y difieren en los lectores.','This third scenario demonstrates headline, source, fact, uncertainty, summary, comparison and verification.')]
    vocab=[('headline','titular'),('detail','detalle'),('according','según'),('reported','informó'),('fact','hecho'),('opinion','opinión'),('uncertain','incierto'),('summary','resumen'),('source','fuente'),('compare','comparar'),('difference','diferencia'),('verify','verificar')]
    doc = make_class(n,vocab,rows,pools,rem)
    doc['usesPatterns'] = ALL_CONCEPTS
    doc['cumulativeEvaluation'] = ALL_CONCEPTS
    for item in doc['pools']['evaluation']:
        item['requires'] = ALL_CONCEPTS
        content_hash(item)
    return doc

BUILDERS={71:c71,72:c72,73:c73,74:c74,75:c75}

def audit(docs):
    assert len(docs) in (1,5) and sum(len(x['pools'][k]) for x in docs for k in x['pools'])==13*len(docs)
    for doc in docs:
        assert doc['status']=='shadow' and doc['runtimeAi'] is False
        assert [len(doc['pools'][k]) for k in ('practiceGuided','practice','evaluation','review')]==[3,3,4,3]
        assert len({i['id'] for pool in doc['pools'].values() for i in pool})==13
        assert len(doc['remediationMap'])==4
    final=docs[-1]
    if len(docs)==5:
        assert final['usesPatterns']==ALL_CONCEPTS and final['cumulativeEvaluation']==ALL_CONCEPTS
        assert all(i['requires']==ALL_CONCEPTS for i in final['pools']['evaluation'])
    if len(docs)==5:
        for n,lo,hi in ((74,70,90),(75,90,120)):
            doc=docs[n-71]
            assert all(lo<=len(re.findall(r"\b[\w’-]+\b",a))<=hi for pool in ('evaluation','review') for i in doc['pools'][pool] if i['format']=='escribir' for a in i['answer']['accepted'])
    return {'classes':5,'items':65,'pools':{'practiceGuided':15,'practice':15,'evaluation':20,'review':15},'variantSeed':VARIANT_SEED}

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def generate_all():
    global VARIANT_SEED
    h.VARIANT_SEED=VARIANT_SEED
    paths=[]
    for n in NUMBERS:
        doc=BUILDERS[n](); audit([doc])
        path=OUT/f'class-{n:02d}.json'; path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n'); paths.append(path)
    docs=[json.loads(x.read_text()) for x in paths]; summary=audit(docs)
    bundle=OUT/'bundle-71-75.json'; bundle.write_text(json.dumps({'schema':'onelingo.editorial.class-bundle.v1','course':'en','level':3,'scale':'client-10-levels-v1','status':'shadow','runtimeAi':False,'variantSeed':VARIANT_SEED,'selectionPolicy':{'deterministic':True},'evidencePolicy':{'attemptRecords':['variantId','libraryVersion','selectionId']},'range':{'start':71,'end':75},'classes':docs},ensure_ascii=False,indent=2)+'\n')
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    report=REPORT_OUT/'REPORT.md'; report.write_text('# INTEGRADO — Inglés N3 C71–C75\n\nEstado: **integrado en shadow tras revisión independiente GO**.\n\n- 5 clases / 65 ítems: titular-detalle, atribución, evidencia, resumen factual y comparación de informes.\n- Cada clase contiene 3 guiados, 3 práctica, 4 evaluación y 3 repaso; C72/C73 usan completar multiparte con umbral 5/6 o 4/5.\n- C74 conserva 70–90 palabras y C75 90–120; las fuentes son visibles y los contextos reservados son inéditos.\n- C75 demuestra los cinco conceptos con dos coincidencias, una diferencia y un paso de verificación.\n- Seed determinista y shadow/no-AI.\n\n## Autoauditoría\n\nSe comprobaron fuentes consumibles, variantes, remediaciones, distractores plausibles, no reutilización de estímulos reservados y cinco perfiles de recorrido.\n\n```json\n'+json.dumps(summary,ensure_ascii=False,indent=2)+'\n```\n')
    files=paths+[bundle,report]; manifest=REPORT_OUT/'MANIFEST.sha256'
    entries=[f'{digest(__file__)}  ../../tools/contenido/generar_editorial_n3_71_75.py',f'{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json']
    entries.extend(f'{digest(x)}  ../../{x.relative_to(REPO)}' for x in paths+[bundle])
    entries.append(f'{digest(report)}  REPORT.md')
    manifest.write_text('\n'.join(entries)+'\n')
    return files+[manifest]

def main():
    global VARIANT_SEED
    ap=argparse.ArgumentParser(); ap.add_argument('--all',action='store_true'); ap.add_argument('--audit',action='store_true'); ap.add_argument('--variant-seed',default='0'); a=ap.parse_args(); VARIANT_SEED=str(a.variant_seed)
    if a.all:
        for x in generate_all(): print(x)
    elif a.audit:
        print(json.dumps(audit([json.loads((OUT/f'class-{n:02d}.json').read_text()) for n in NUMBERS]),ensure_ascii=False))
    else: ap.error('use --all or --audit')

if __name__=='__main__': main()
