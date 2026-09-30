#!/usr/bin/env python3
"""Generate the integrated English N3 C76-C80 editorial shadow block."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / 'assets/contenido/en/editorial/n3'
REPORT_OUT = REPO / 'build/editorial-n3-76-80'
MAP = REPO / 'assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json'
HELPER_PATH = REPO / 'tools/contenido/generar_editorial_n3_66_70.py'
spec = importlib.util.spec_from_file_location('editorial_helpers_66_70', HELPER_PATH)
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
NUMBERS = range(76, 81)
PHASES = {76:'input',77:'form',78:'comprehension',79:'production',80:'transfer'}
CONCEPTS = {n:f'n3-media-reviews-{n-75}' for n in NUMBERS}
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
    sentences = [sentence if '___' in sentence else f'{sentence} Respuesta: ___.' for sentence in sentences]
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
    parts1=[{'text':x[1],'accepted':[x[1]]} for x in a]; parts2=[{'text':x[1],'accepted':[x[1]]} for x in b]
    pools={'practiceGuided':[
      choose(f'{p}.pg01','¿Qué opción nombra una fuente?',['according to the report','the report is true','everyone knows'],0,c,'practiceGuided','According to names the source without claiming certainty.'),
      fill(f'{p}.pg02','Completa una sola palabra: The paper ___ a delay.','reported',['reported','said'],c,'practiceGuided','Reported attributes the information to the paper.'),
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
      fill(f'{p}.r01','Completa una palabra: The coach ___ two changes.','reported',['reported','said'],c,'review','Reported attributes the update to the coach.'),
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
      choose(f'{p}.e01','¿Qué dato sí está en la ficha?',['the café opens at 08:00 next week','the café is popular','the room closed because of rain'],0,c,'evaluation','The director said the opening time; popularity and cause are absent.'),
      listen(f'{p}.e02','Escucha y elige la atribución correcta.','The curator reported that Gallery 2 reopened on Thursday.',['The curator reported Gallery 2 reopened Thursday.','The gallery reopened because of funding.','The curator closed Gallery 2.'],0,c,'evaluation','Only the first option preserves the named fact.'),
      choose(f'{p}.e03','¿Qué debe excluir el resumen?',['una causa no confirmada','la fuente visible','uno de los tres hechos'],0,c,'evaluation','The task requires three facts but forbids an invented cause.'),
      write(f'{p}.e04','Escribe 70–90 palabras con tres hechos atribuidos.',s1,a1,c,'evaluation','The source card supplies exactly three facts; do not add a cause.',word_range=(70,90))],
      'review':[
      choose(f'{p}.r01','¿Qué fuente menciona las vitrinas?',['the notice','an unnamed visitor','a weather report'],0,c,'review','The museum notice gives the number of display cases.'),
      listen(f'{p}.r02','Escucha y elige el hecho exacto.','The curator said the audio tour will start at 10:00 next month.',['the audio tour starts at 10:00 next month','the tour already started','the curator cancelled it'],0,c,'review','The time and future attribution are both stated.'),
      write(f'{p}.r03','Resume 70–90 palabras sin inventar causas.',s2,a2,c,'review','The new museum card has three facts and explicitly withholds a reason.',word_range=(70,90))]}
    rem={f'{p}.e01':route(n,'t01','r01'),f'{p}.e02':route(n,'t02','r02'),f'{p}.e03':route(n,'t03','r01'),f'{p}.e04':route(n,'t06','r03')}
    rows=[('A source card gives the facts you may summarize.','Una ficha de fuente da los hechos que puedes resumir.','Use only visible information.'),('According to and reported identify the source.','According to y reported identifican la fuente.','Keep attribution in the summary.'),('A factual summary includes three important details.','Un resumen factual incluye tres detalles importantes.','Select the three stated facts.'),('Do not add a cause that the card does not confirm.','No añadas una causa que la ficha no confirma.','Absence of a reason is meaningful.'),('A time, number or place can preserve exact detail.','Una hora, número o lugar puede conservar un detalle exacto.','Keep concrete evidence in your words.'),('The director reported three facts; the summary keeps the source and adds no cause.','El director informó tres hechos; el resumen conserva la fuente y no añade causa.','This is the complete production target.')]
    return make_class(n,[('summary','resumen'),('source','fuente'),('reported','informó'),('fact','hecho'),('detail','detalle'),('cause','causa')],rows,pools,rem)

def c75():
    n,c,p=75,CONCEPTS[75],'en.n3.c75'
    sources=[
      'Source A — Town website: The council reported that the river path reopened on Tuesday. Source B — local radio: The presenter said the river path reopened on Tuesday. Both sources mention a new sign at the north gate. The website says the path has two entrances; radio says the north gate is the only entrance. Neither source confirms why the path reopened.',
      'Source A — School notice: The library added evening hours on Monday, according to the notice. Source B — student radio: The presenter reported the same Monday change. Both mention a quiet-study room and a new booking form. The notice says the room has twenty desks; radio says it has eighteen. Neither source confirms who changed the hours.',
      'Source A — Market bulletin: The west entrance reopened on Friday, according to the bulletin. Source B — shopkeeper audio: The shopkeeper said the west entrance reopened on Friday. Both mention a card reader and a queue sign. The bulletin says two readers work; the shopkeeper says one reader works. Neither source confirms the repair cause.']
    answers=[
      ['Both sources confirm that the river path reopened on Tuesday and that a new sign is at the north gate. They differ about entrances: the website says there are two, while the radio says the north gate is the only one. The reports attribute the information to the council website and local radio, and the wording says neither source confirms a reason for reopening. I would verify the entrance count and cause by checking the council current notice or contacting the path office. This compares the headline and exact details without inventing evidence. The comparison records each claim cautiously for a reader.','The council website and local radio agree that the river path reopened on Tuesday and that the north gate has a new sign. Their difference is the number of entrances: the website gives two, but radio gives only one. Neither source confirms why the path reopened. To verify the conflict, I would ask the path office for its current entrance map and an official explanation. These points separate confirmed overlap, disagreement and a useful next step. The comparison also names both sources clearly. A reader can see which detail remains unresolved.'],
      ['The school notice and student radio agree that the library added evening hours on Monday and that it has a quiet-study room and a new booking form. They differ on capacity: the notice says twenty desks, while radio says eighteen. The sources are named and neither confirms who changed the hours. I would verify the capacity and responsible person by checking the school library current notice or asking the librarian. This keeps the comparison source-based and cautious. The unresolved capacity is not silently corrected. The two reports should remain separate until the capacity is checked.','Both the school notice and student radio report Monday evening-hour changes, a quiet-study room and a booking form. The clear difference is capacity: one source states twenty desks and the other states eighteen. Neither says who made the change. I would check the current library notice and confirm the number with the librarian. That step would resolve the conflicting detail without treating an unconfirmed cause as fact. The final capacity should remain open until that source check is complete. This comparison records the disagreement rather than choosing an unsupported answer.'],
      ['The market bulletin and shopkeeper audio agree that the west entrance reopened on Friday and that a card reader and queue sign are present. They differ on working readers: the bulletin says two, while the shopkeeper says one. Neither source confirms the repair cause. I would verify the number by checking the market office current notice and asking staff to test the reader. This comparison keeps the two sources, their coincidence, their difference and a concrete verification step visible.','Both market sources report a Friday reopening at the west entrance and mention a card reader and queue sign. Their difference is the number of working readers, two in the bulletin and one in the shopkeeper audio. The repair cause is not confirmed. I would ask the market office for its current equipment record and test the reader. That check distinguishes the shared facts from the unresolved count without inventing a reason.']]
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
      choose(f'{p}.r01','¿Qué dato coincide en ambas fuentes?',['the west entrance reopened Friday','two readers work','the repair cause is confirmed'],0,c,'review','Both sources give the same reopening day and entrance.'),
      listen(f'{p}.r02','Escucha: elige la diferencia.','The bulletin says two readers work; the shopkeeper says one reader works.',['two versus one reader','both name Friday','both mention a queue sign'],0,c,'review','The reader count is the explicit disagreement.'),
      allreq(write(f'{p}.r03','Compara las fuentes en 90–120 palabras.',sources[1],answers[1],c,'review','The school sources give two coincidences, one capacity conflict and a verification action.',word_range=(90,120)))]}
    rem={f'{p}.e01':route(n,'t01','r01'),f'{p}.e02':route(n,'t02','r02'),f'{p}.e03':route(n,'t03','r02'),f'{p}.e04':route(n,'t06','r03')}
    rows=[('A headline is shorter than its confirmed detail.','Un titular es más corto que su detalle confirmado.','Keep the title separate from the evidence.'),('According to names a source.','According to nombra una fuente.','Attribution keeps information accountable.'),('Confirmed, opinion and uncertainty use different markers.','Confirmado, opinión e incertidumbre usan marcadores distintos.','Read the linguistic evidence before judging a claim.'),('A factual summary keeps three attributed details.','Un resumen factual conserva tres detalles atribuidos.','Do not add an unconfirmed cause.'),('Compare two sources, note one difference, and verify it.','Compara dos fuentes, anota una diferencia y verifícala.','These are the five block concepts in the final transfer.'),('Two sources agree on a detail, differ on another and require a verification step.','Dos fuentes coinciden en un detalle, difieren en otro y requieren verificación.','The model compares visible evidence without inventing certainty.')]
    vocab=[('headline','titular'),('detail','detalle'),('according','según'),('reported','informó'),('fact','hecho'),('opinion','opinión'),('uncertain','incierto'),('summary','resumen'),('source','fuente'),('compare','comparar'),('difference','diferencia'),('verify','verificar')]
    doc = make_class(n,vocab,rows,pools,rem)
    doc['usesPatterns'] = ALL_CONCEPTS
    doc['cumulativeEvaluation'] = ALL_CONCEPTS
    for item in doc['pools']['evaluation']:
        item['requires'] = ALL_CONCEPTS
        content_hash(item)
    return doc

def _parts(values):
    return [
      {'text':value,'accepted':list(dict.fromkeys([
        value,
        value.replace(' | ', ', '),
        value.replace(' | ', '; '),
      ]))}
      for value in values
    ]

def c76():
    n,c,p=76,CONCEPTS[76],'en.n3.c76'
    pools={'practiceGuided':[
      choose(f'{p}.pg01','¿Qué detalle nombra el género?',['It is a mystery.','A nurse finds a letter.','I felt tense.'],0,c,'practiceGuided','Mystery names the genre, not the plot or reaction.'),
      choose(f'{p}.pg02','¿Qué frase resume la trama sin revelar el final?',['A nurse finds a hidden letter.','The ending reveals the thief.','I enjoyed the dialogue.'],0,c,'practiceGuided','The discovery starts the plot without giving away its ending.'),
      listen(f'{p}.pg03','Escucha y elige la reacción.','The film is a comedy about two neighbours. I laughed throughout it.',['I laughed throughout it.','It is a comedy.','Two neighbours meet.'],0,c,'practiceGuided','Laughed states the viewer reaction.')],
      'practice':[
      choose(f'{p}.p01','¿Qué frase describe un personaje?',['The main character is a patient mechanic.','The plot begins at a station.','The review felt hopeful.'],0,c,'practice','The mechanic and personality describe the main character.'),
      listen(f'{p}.p02','Escucha y elige la trama.','This science-fiction story follows a pilot who loses contact with Earth. It made me curious.',['a pilot loses contact with Earth','science fiction','the reviewer felt curious'],0,c,'practice','The pilot’s problem is the plot element.'),
      order(f'{p}.p03','Ordena una reacción del lector.','The ending made me hopeful',c,'practice','Made me hopeful states a personal reaction.')],
      'evaluation':[
      choose(f'{p}.e01','¿Qué opción combina género y personaje?',['a drama with a determined teacher','a missing map at dawn','surprised by the final scene'],0,c,'evaluation','Drama is the genre and teacher is the character.'),
      listen(f'{p}.e02','Escucha y elige el elemento de trama.','The podcast is a biography. A journalist follows a climber during one difficult winter. I found it inspiring.',['a journalist follows a climber','a biography','the reviewer felt inspired'],0,c,'evaluation','The journalist following the climber describes what happens.'),
      choose(f'{p}.e03','¿Qué frase expresa reacción, no valoración técnica?',['The story made me nervous.','The story has three chapters.','The story is historical fiction.'],0,c,'evaluation','Made me nervous is the reader’s response.'),
      multipart(f'{p}.e04','Completa cuatro fichas con género, trama y reacción.',[
        'A: Mystery; a chef searches for a missing recipe; the reader felt curious.',
        'B: Comedy; two cousins open a café; the viewer laughed often.',
        'C: Drama; a runner returns home; the reader felt moved.',
        'D: Science fiction; a robot protects a garden; the viewer felt hopeful.'],
        _parts(['mystery | a chef searches for a missing recipe | curious','comedy | two cousins open a café | laughed often','drama | a runner returns home | moved','science fiction | a robot protects a garden | hopeful']),c,'evaluation','Each response reproduces the three review components visible in its card.',4,source={'text':'Completa cada ficha únicamente con los tres datos visibles.'})],
      'review':[
      choose(f'{p}.r01','¿Qué categoría responde “How did it make you feel?”',['reaction','genre','plot'],0,c,'review','A feeling belongs to the reviewer reaction.'),
      listen(f'{p}.r02','Escucha y elige el personaje.','In this fantasy, a shy baker must protect the village. The story made me smile.',['a shy baker','a fantasy','the reviewer smiled'],0,c,'review','The shy baker is the character.'),
      multipart(f'{p}.r03','Recupera cuatro fichas nuevas de reseña.',[
        'E: Fantasy; a baker protects a village; the reader felt cheerful.',
        'F: Documentary; divers study a reef; the viewer felt informed.',
        'G: Thriller; a driver receives a warning; the reader felt tense.',
        'H: Biography; a doctor builds a clinic; the viewer felt inspired.'],
        _parts(['fantasy | a baker protects a village | cheerful','documentary | divers study a reef | informed','thriller | a driver receives a warning | tense','biography | a doctor builds a clinic | inspired']),c,'review','The recovery separates genre, plot and reaction in four unseen reviews.',4,source={'text':'Usa solo la información explícita de cada ficha.'})]}
    rem={f'{p}.e01':route(n,'t01','r03'),f'{p}.e02':route(n,'t02','r03'),f'{p}.e03':route(n,'t04','r01'),f'{p}.e04':route(n,'t06','r03')}
    rem[f'{p}.e01']['reteachSteps']=[f'en.n3.class-{n:02d}.t01',f'en.n3.class-{n:02d}.t03',f'en.n3.class-{n:02d}.t06']
    rows=[('Genre names the type of story.','Genre nombra el tipo de historia.','Mystery, comedy and drama are genres.'),('Plot tells what happens without the ending.','Plot cuenta qué ocurre sin el final.','Use one central event and avoid spoilers.'),('A character takes part in the story.','Un personaje participa en la historia.','Name a role and one useful quality.'),('Reaction tells how the work made you feel.','Reaction indica cómo te hizo sentir la obra.','Moved, amused and tense are reactions.'),('A review separates story facts from personal reaction.','Una reseña separa hechos de reacción personal.','Do not present a feeling as plot.'),('A mystery follows a chef searching for a recipe, and it made the reader curious.','Un misterio sigue a una chef que busca una receta y despertó curiosidad.','The model contains genre, plot, character and reaction.')]
    return make_class(n,[('genre','género'),('plot','trama'),('character','personaje'),('reaction','reacción'),('mystery','misterio'),('comedy','comedia')],rows,pools,rem)

def c77():
    n,c,p=77,CONCEPTS[77],'en.n3.c77'
    s1=['Contraste en una oración con Although: The plot is simple. The characters are memorable.','Contraste entre dos oraciones con However: The film is long. The final hour moves quickly.','Causa con because: I recommend the podcast. Its interviews are clear.','Contraste en una oración con Although: The setting is beautiful. The dialogue feels weak.','Contraste entre dos oraciones con However: The book is serious. It includes gentle humour.','Causa con because: The review is positive. Its evidence is specific.']
    a1=['Although the plot is simple, the characters are memorable.','The film is long; however, the final hour moves quickly.','I recommend the podcast because its interviews are clear.','Although the setting is beautiful, the dialogue feels weak.','The book is serious; however, it includes gentle humour.','The review is positive because its evidence is specific.']
    s2=['Contraste en una oración con Although: The game is short. Its puzzles are creative.','Contraste entre dos oraciones con However: The series starts slowly. Episode three becomes exciting.','Causa con because: I suggest the novel. Its narrator is convincing.','Contraste en una oración con Although: The music is strong. The story is predictable.','Contraste entre dos oraciones con However: The documentary is detailed. It remains easy to follow.','Causa con because: The review is balanced. It presents evidence and one limit.']
    a2=['Although the game is short, its puzzles are creative.','The series starts slowly; however, episode three becomes exciting.','I suggest the novel because its narrator is convincing.','Although the music is strong, the story is predictable.','The documentary is detailed; however, it remains easy to follow.','The review is balanced because it presents evidence and one limit.']
    pools={'practiceGuided':[
      fill(f'{p}.pg01','Completa: ___ the film is long, it stays engaging.','Although',['Although','although'],c,'practiceGuided','Although introduces a contrast inside one sentence.'),
      choose(f'{p}.pg02','¿Qué conector inicia una segunda oración de contraste?',['However','Because','Although'],0,c,'practiceGuided','However links a contrasting second statement.'),
      fill(f'{p}.pg03','Completa la causa: I recommend it ___ the dialogue is clear.','because',['because','Because'],c,'practiceGuided','Because introduces the evidence for the recommendation.')],
      'practice':[
      listen(f'{p}.p01','Escucha y elige la relación lógica.','Although the plot is familiar, the characters feel fresh.',['contrast','cause','sequence'],0,c,'practice','Although signals contrast between two evaluations.'),
      order(f'{p}.p02','Ordena una opinión con causa.','I liked the series because the actors were convincing',c,'practice','Because links the positive opinion to evidence.'),
      choose(f'{p}.p03','¿Qué combinación conserva el contraste?',['The opening is slow; however, the ending is strong.','The opening is slow because the ending is strong.','Although the opening and the ending are strong.'],0,c,'practice','However preserves two opposing evaluations.')],
      'evaluation':[
      fill(f'{p}.e01','Completa el contraste: ___ it is short, it feels complete.','Although',['Although','although'],c,'evaluation','Although introduces the concession.'),
      listen(f'{p}.e02','Escucha y elige el conector oído.','The plot is quiet. However, the tension grows.',['however','because','although'],0,c,'evaluation','However begins the contrasting second sentence.'),
      choose(f'{p}.e03','¿Qué frase expresa causa?',['I recommend it because the evidence is clear.','Although it is clear, I recommend it.','It is clear; however, I recommend it.'],0,c,'evaluation','Because directly gives the reason.'),
      multipart(f'{p}.e04','Combina seis pares sin cambiar contraste o causa.',s1,_parts(a1),c,'evaluation','Five of six complete sentences must preserve the stated logical relation.',5)],
      'review':[
      choose(f'{p}.r01','¿Qué conector introduce una reserva?',['although','because','so'],0,c,'review','Although can introduce a limitation before praise.'),
      listen(f'{p}.r02','Escucha y elige la causa.','I suggest the book because its examples are practical.',['its examples are practical','I suggest the book','the book is long'],0,c,'review','The clause after because supplies the reason.'),
      multipart(f'{p}.r03','Recupera seis combinaciones equilibradas.',s2,_parts(a2),c,'review','The recovery uses new evidence and six genuine linker decisions.',5)]}
    rem={f'{p}.e01':route(n,'t01','r01'),f'{p}.e02':route(n,'t02','r03'),f'{p}.e03':route(n,'t03','r02'),f'{p}.e04':route(n,'t06','r03')}
    rows=[('Although introduces contrast in one sentence.','Although introduce contraste en una oración.','Place a full clause after although.'),('However connects two contrasting statements.','However conecta dos afirmaciones opuestas.','Use punctuation before and after however.'),('Because gives evidence for an opinion.','Because aporta evidencia para una opinión.','The reason follows because.'),('A balanced review can praise one feature and limit another.','Una reseña equilibrada puede elogiar y limitar.','Contrast prevents an absolute judgement.'),('Keep the original logical relation when combining ideas.','Conserva la relación lógica original al combinar ideas.','Do not replace contrast with cause.'),('Although the opening is slow, the characters are strong; I recommend it because they feel real.','Aunque el inicio es lento, los personajes son sólidos; la recomiendo porque parecen reales.','The model combines contrast, opinion and evidence.')]
    return make_class(n,[('although','aunque'),('however','sin embargo'),('because','porque'),('contrast','contraste'),('cause','causa'),('balanced','equilibrado'),('relation','relación')],rows,pools,rem)

def c78():
    n,c,p=78,CONCEPTS[78],'en.n3.c78'
    source1='Review A: I recommend Silent Harbour. The mystery develops carefully, and Mara is convincing. However, the first chapter is slow. Review B: I do not recommend Fast Track. Its action scenes are clear, but the characters feel flat. It may suit readers who only want a short thriller.'
    source2='Review A: I recommend North Window. The setting feels real, and the dialogue is natural. However, the ending is rushed. Review B: I would not choose Bright Noise. The music is lively, but the plot repeats itself. It may suit viewers who prefer style to story.'
    parts1=[
      {'text':'A recommends; B does not','accepted':['A recommends; B does not','stance: A recommends; B does not']},
      {'text':'A mystery develops carefully','accepted':['A mystery develops carefully','reason 1: A mystery develops carefully']},
      {'text':'Mara is convincing','accepted':['Mara is convincing','reason 2: Mara is convincing']},
      {'text':'the first chapter is slow','accepted':['the first chapter is slow','reservation A: the first chapter is slow']},
      {'text':'readers who only want a short thriller','accepted':['readers who only want a short thriller','possible audience B: readers who only want a short thriller']},
    ]
    parts2=[
      {'text':'A recommends; B does not','accepted':['A recommends; B does not','stance: A recommends; B does not']},
      {'text':'A setting feels real','accepted':['A setting feels real','reason 1: A setting feels real']},
      {'text':'A dialogue is natural','accepted':['A dialogue is natural','reason 2: A dialogue is natural']},
      {'text':'the ending is rushed','accepted':['the ending is rushed','reservation A: the ending is rushed']},
      {'text':'viewers who prefer style to story','accepted':['viewers who prefer style to story','possible audience B: viewers who prefer style to story']},
    ]
    score_req={'text':source1}
    pools={'practiceGuided':[
      choose(f'{p}.pg01','¿Qué frase expresa postura positiva?',['I recommend it.','The opening is slow.','It has six chapters.'],0,c,'practiceGuided','I recommend it states the reviewer’s stance.'),
      choose(f'{p}.pg02','¿Qué frase aporta evidencia?',['The dialogue sounds natural.','I liked it somehow.','It may be suitable.'],0,c,'practiceGuided','A specific feature supports the judgement.'),
      listen(f'{p}.pg03','Escucha y elige la reserva.','I recommend the film because the acting is strong. However, the final scene is long.',['the final scene is long','the acting is strong','the reviewer recommends it'],0,c,'practiceGuided','However introduces the limitation.')],
      'practice':[
      choose(f'{p}.p01','¿Qué combinación contiene postura y razón?',['I recommend it because the narrator is clear.','The narrator appears in chapter two.','However, it is a podcast.'],0,c,'practice','The recommendation and because-clause give stance plus evidence.'),
      listen(f'{p}.p02','Escucha y elige la postura.','The plot is original, but I would not recommend the series because it is too violent.',['negative recommendation','positive recommendation','no opinion'],0,c,'practice','Would not recommend states a negative stance.'),
      order(f'{p}.p03','Ordena una reserva explícita.','However the opening is too slow',c,'practice','However identifies a limit on the positive points.')],
      'evaluation':[
      choose(f'{p}.e01','¿Qué marcador introduce una reserva?',['however','recommend','convincing'],0,c,'evaluation','However signals a limitation or contrast.'),
      listen(f'{p}.e02','Escucha y elige la evidencia positiva.','I recommend the audio drama because the voices are distinct. However, episode one is long.',['the voices are distinct','episode one is long','it is an audio drama'],0,c,'evaluation','Distinct voices are the stated reason for the recommendation.'),
      choose(f'{p}.e03','¿Qué postura es negativa pero limitada?',['I would not choose it, though some viewers may enjoy the style.','Everyone will dislike it.','It has a modern style.'],0,c,'evaluation','The negative stance remains limited by acknowledging a possible audience.'),
      multipart(f'{p}.e04','Completa postura, razones, reserva y audiencia de ambas reseñas.',['Postura de A y B: ___.','Primera razón de A: ___.','Segunda razón de A: ___.','Reserva de A: ___.','Audiencia posible de B: ___.'],parts1,c,'evaluation','All five answers come directly from the two visible reviews.',5,source=score_req,requires=None)],
      'review':[
      choose(f'{p}.r01','¿Qué dato funciona como límite?',['the ending is rushed','the setting feels real','the dialogue is natural'],0,c,'review','A rushed ending is the reservation.'),
      listen(f'{p}.r02','Escucha y elige la postura del reseñador.','The music is lively, but I would not choose the film.',['negative','positive','unstated'],0,c,'review','Would not choose gives the negative stance.'),
      multipart(f'{p}.r03','Recupera postura, razones, reserva y audiencia nuevas.',['Postura de A y B: ___.','Primera razón de A: ___.','Segunda razón de A: ___.','Reserva de A: ___.','Audiencia posible de B: ___.'],parts2,c,'review','The recovery uses a different pair of reviews and five explicit fields.',5,source={'text':source2})]}
    for item in (pools['evaluation'][3],pools['review'][2]): item['origin']['scoring']['requiredParts']=[0,1,2,3,4]; content_hash(item)
    rem={f'{p}.e01':route(n,'t03','r01'),f'{p}.e02':route(n,'t02','r03'),f'{p}.e03':route(n,'t01','r02'),f'{p}.e04':route(n,'t04','r03')}
    rows=[('A stance shows whether the reviewer recommends the work.','Una postura muestra si el reseñador recomienda la obra.','Look for recommend, suggest or would not choose.'),('A reason names a specific feature as evidence.','Una razón nombra un rasgo específico como evidencia.','Plot, acting or dialogue can support a stance.'),('However often introduces a reservation.','However suele introducir una reserva.','The reservation limits the praise.'),('A possible audience can limit a negative review.','Una audiencia posible puede limitar una reseña negativa.','May suit identifies who could still enjoy it.'),('Use words from the review to justify an inference.','Usa palabras de la reseña para justificar una inferencia.','Do not guess a reason not present in the text.'),('The reviewer recommends the mystery for its careful plot and character, but notes a slow opening.','El reseñador recomienda el misterio por trama y personaje, pero señala un inicio lento.','This model joins stance, two reasons and a limit.')]
    return make_class(n,[('stance','postura'),('evidence','evidencia'),('reason','razón'),('reservation','reserva'),('recommend','recomendar'),('reviewer','reseñador'),('audience','audiencia'),('review','reseña')],rows,pools,rem)

def c79():
    n,c,p=79,CONCEPTS[79],'en.n3.c79'
    s1='Ficha: The Last Lantern; misterio. Una estudiante encuentra mensajes en una biblioteca cerrada. Fortalezas: ambiente tenso y protagonista convincente. Límite: inicio lento. No se proporciona el desenlace.'
    s2='Ficha: Small Signals; drama de audio. Dos hermanos reparan una radio comunitaria. Fortalezas: diálogo natural y sonido claro. Límite: episodio central repetitivo. No se proporciona el desenlace.'
    a1=['The Last Lantern is a mystery about a student who finds messages in a closed library. It creates a tense atmosphere, and the main character feels convincing because her choices are believable. Although the opening is slow, the central mystery becomes engaging. I would recommend it to readers who enjoy quiet suspense and careful clues. The review cannot reveal the ending because the source card does not provide it. Overall, the strong setting and character balance the slower beginning without making the recommendation absolute for most readers.','This mystery follows a student who discovers unusual messages inside a closed library. The tense setting is effective, and the protagonist is convincing because her decisions feel natural. However, the opening moves slowly. I still recommend The Last Lantern to readers who like patient mysteries with clues rather than constant action. The source gives no ending, so this review avoids any spoiler. Its atmosphere and believable central character provide two clear reasons for the positive but balanced judgement.']
    a1[1] += ' This recommendation remains useful today.'
    a2=['Small Signals is an audio drama about two siblings who repair a community radio. The natural dialogue makes their relationship believable, and the clear sound helps every conversation remain easy to follow. However, the middle episode repeats some information. I would recommend the series to listeners who enjoy realistic family stories and media settings. The source card gives no ending, so this review does not reveal one. Overall, the dialogue and sound are stronger than the repetitive section, which keeps the recommendation positive but balanced.','This audio drama follows two siblings as they repair a community radio. Its dialogue feels natural, and the sound is clear enough to make each speaker easy to identify. Although the central episode repeats a few ideas, the relationship remains engaging. I recommend Small Signals for listeners who prefer realistic drama to action. The source does not state the ending, so no final event is included here. Two specific strengths support the recommendation, while the repeated middle section provides a fair and relevant limitation.']
    pools={'practiceGuided':[
      choose(f'{p}.pg01','¿Qué contexto evita revelar el final?',['A student finds messages in a closed library.','The final message names the thief.','The last page explains everything.'],0,c,'practiceGuided','The setup introduces the story without its resolution.'),
      choose(f'{p}.pg02','¿Qué frase aporta una razón concreta?',['The protagonist makes believable choices.','The book is good.','Everyone should read it.'],0,c,'practiceGuided','Believable choices are observable evidence.'),
      listen(f'{p}.pg03','Escucha y elige la valoración equilibrada.','The setting is tense; however, the opening is slow.',['praise plus limitation','only praise','plot ending'],0,c,'practiceGuided','The sentence balances one strength and one limit.')],
      'practice':[
      order(f'{p}.p01','Ordena una recomendación con audiencia.','I recommend it to readers who enjoy quiet mysteries',c,'practice','The sentence identifies an appropriate audience.'),
      listen(f'{p}.p02','Escucha y elige la segunda razón.','The dialogue feels natural, and the sound is clear.',['clear sound','natural dialogue','slow opening'],0,c,'practice','Clear sound is the second stated strength.'),
      choose(f'{p}.p03','¿Qué frase evita una valoración absoluta?',['Although it is slow, its characters are strong.','It is perfect for everyone.','Nothing in it could improve.'],0,c,'practice','Although balances limitation and strength.')],
      'evaluation':[
      choose(f'{p}.e01','¿Qué dato puede incluirse sin spoiler?',['the library setting','the identity revealed at the end','the final solution'],0,c,'evaluation','The setting belongs to the visible setup.'),
      listen(f'{p}.e02','Escucha y elige la limitación.','The atmosphere is effective, but the opening takes time to develop.',['slow opening','effective atmosphere','closed library'],0,c,'evaluation','Takes time to develop identifies the limit.'),
      choose(f'{p}.e03','¿Qué oración contiene evidencia, no elogio vacío?',['The character is convincing because her choices feel natural.','The character is amazing.','This is the best character ever.'],0,c,'evaluation','The because-clause supplies specific evidence.'),
      write(f'{p}.e04','Escribe una reseña equilibrada de 80–100 palabras.',s1,a1,c,'evaluation','The response uses setup, two reasons and one limit without adding an ending.',word_range=[80,100])],
      'review':[
      choose(f'{p}.r01','¿Qué público coincide con un drama familiar realista?',['listeners who enjoy realistic family stories','viewers seeking a violent thriller','readers needing the final answer'],0,c,'review','The first audience matches the visible genre and tone.'),
      listen(f'{p}.r02','Escucha y elige una fortaleza concreta.','The voices are distinct, so the audio is easy to follow.',['distinct voices','a perfect story','an unknown ending'],0,c,'review','Distinct voices are observable audio evidence.'),
      write(f'{p}.r03','Recupera una reseña nueva de 80–100 palabras.',s2,a2,c,'review','The recovery uses a new audio drama, two strengths and a proportionate limit.',word_range=[80,100])]}
    rem={f'{p}.e01':route(n,'t01','r03'),f'{p}.e02':route(n,'t03','r03'),f'{p}.e03':route(n,'t02','r02'),f'{p}.e04':route(n,'t06','r03')}
    rows=[('Give only enough plot context to identify the work.','Da solo el contexto necesario para identificar la obra.','Do not reveal the ending.'),('Support the judgement with two specific reasons.','Apoya la valoración con dos razones específicas.','Features such as dialogue and setting count as evidence.'),('Use a linker to balance praise and limitation.','Usa un conector para equilibrar elogio y límite.','Although or however prevents an absolute claim.'),('Name an audience that matches the work.','Nombra una audiencia que coincida con la obra.','The recommendation should be useful.'),('A source card sets the boundary of the review.','Una ficha fija el límite de la reseña.','Do not invent events absent from the card.'),('A balanced review gives setup, two reasons, one limitation and an audience without revealing the ending.','Una reseña equilibrada da contexto, razones, límite y audiencia sin revelar el final.','The full model stays within 80–100 words.')]
    rows[-1]=(a1[0],'Modelo completo: misterio, contexto sin final, dos razones, límite y audiencia.','The 80–100 word model demonstrates the full production target.')
    return make_class(n,[('review','reseña'),('spoiler','revelación del final'),('setting','ambientación'),('dialogue','diálogo'),('limitation','limitación'),('audience','audiencia'),('plot','trama'),('reasons','razones')],rows,pools,rem)

def c80():
    n,c,p=80,CONCEPTS[80],'en.n3.c80'
    sources=[
      'Club de lectura: adultos quieren misterio esperanzador, sin violencia gráfica, máximo 250 páginas. A: Garden Code, misterio 220 páginas; jardinera descifra cartas; humor suave; inicio lento; sin violencia. B: Red Tower, thriller 240 páginas; acción intensa; violencia gráfica. C: Winter Map, drama 190 páginas; triste y sin misterio.',
      'Noche familiar: edades 10+, quieren comedia de menos de 100 minutos y nada aterrador. A: Busy Neighbours, comedia 94 min; dos vecinos preparan una feria; diálogo divertido; final previsible; apta 10+. B: Moon Door, fantasía 88 min; varias escenas aterradoras; 12+. C: Long Weekend, comedia 126 min; apta 10+.',
      'Club de audio: estudiantes quieren diálogo claro, historia moderna, menos de 60 minutos y final no triste. A: City Frequency, drama de audio 52 min; jóvenes arreglan una radio; voces claras; parte media repetitiva; final esperanzador. B: Old Crown, drama histórico 48 min; diálogo difícil. C: Last Goodbye, drama moderno 55 min; final triste.']
    answers=[
      ['Garden Code is the best choice for this reading club. It is a 220-page mystery about a gardener decoding letters, so its genre, plot and length fit the group. Readers describe the gentle humour as enjoyable. Although the opening is slow, the story is hopeful and contains no graphic violence. Red Tower meets the page limit but breaks the violence restriction, while Winter Map is short but is neither mysterious nor hopeful. I recommend Garden Code because it satisfies every essential preference. The club should still warn members that the beginning develops slowly.','I recommend Garden Code for the adult reading club. Its mystery plot follows a gardener who decodes letters, and the book has 220 pages. The gentle humour supports a hopeful reaction. However, members should expect a slow opening. Red Tower is short enough, but its graphic violence conflicts with the limit. Winter Map also fits the length, although its sad drama does not meet the requested genre or tone. Garden Code is therefore the only option matching mystery, hope, length and content needs. The relevant warning is its slower beginning.'],
      ['Busy Neighbours is the strongest option for family night. It is a 94-minute comedy about two neighbours preparing a fair, and its funny dialogue suits viewers aged ten and over. Although the ending is predictable, the film meets the time, age and no-scare limits. Moon Door is shorter, but its frightening scenes and age-twelve rating do not fit. Long Weekend is a suitable comedy for age ten, yet its 126-minute running time is too long. I recommend Busy Neighbours because it matches every required condition, with the predictable ending as the relevant warning.','I recommend Busy Neighbours to this family audience. The 94-minute comedy follows two neighbours organising a fair, and reviewers praise its amusing dialogue. It is suitable for ages ten and over and has no frightening content. However, its ending is predictable. Moon Door lasts only 88 minutes, but scary scenes and a twelve-plus rating break two limits. Long Weekend has the right genre and age rating, although 126 minutes exceeds the maximum. Busy Neighbours therefore offers the best fit, and families should only be warned that the final events are easy to predict.'],
      ['City Frequency is the best recommendation for the student audio club. This modern 52-minute drama follows young people repairing a community radio, and its clear voices make the dialogue easy to understand. Although the middle section repeats some information, the ending is hopeful. Old Crown fits the time limit, but its historical setting and difficult dialogue miss two preferences. Last Goodbye is modern and lasts 55 minutes; however, its sad ending breaks an explicit limit. I recommend City Frequency because it meets the length, setting, clarity and tone requirements, with repetition as the relevant warning.','I recommend City Frequency for these students. It is a modern audio drama lasting 52 minutes, with a plot about young people fixing a community radio. The voices are clear, so the dialogue is accessible. However, the middle part is repetitive. Old Crown is under an hour, but its historical story and difficult speech do not suit the request. Last Goodbye has a modern setting and suitable length, although its sad ending conflicts with the audience limit. City Frequency matches all required preferences; listeners only need a warning about the repeated information in the middle.']]
    allreq=lambda item:(item.update({'requires':ALL_CONCEPTS}) or content_hash(item))
    pools={'practiceGuided':[
      choose(f'{p}.pg01','¿Qué dato es una necesidad de audiencia?',['no graphic violence','a gardener finds letters','the opening is slow'],0,c,'practiceGuided','No graphic violence is an explicit content limit.'),
      choose(f'{p}.pg02','¿Qué opción cumple misterio, tono y extensión?',['Garden Code','Red Tower','Winter Map'],0,c,'practiceGuided','Garden Code alone meets all three requirements.'),
      listen(f'{p}.pg03','Escucha y elige la advertencia relevante.','Garden Code fits the club; however, its opening is slow.',['slow opening','graphic violence','sad ending'],0,c,'practiceGuided','The slow opening is the stated reservation.')],
      'practice':[
      choose(f'{p}.p01','¿Por qué Red Tower no es compatible?',['It contains graphic violence.','It has 240 pages.','It is a thriller.'],0,c,'practice','Graphic violence directly breaks the audience limit.'),
      order(f'{p}.p02','Ordena una recomendación con causa.','I recommend Garden Code because it meets every limit',c,'practice','The sentence connects recommendation and audience fit.'),
      write(f'{p}.p03','Escribe una recomendación breve y una advertencia.',sources[0],['I recommend Garden Code because it is a hopeful mystery under 250 pages without graphic violence. However, its opening is slow.','Garden Code fits the mystery, tone, length and content limits, although the club should expect a slow beginning.'],c,'practice','Both versions name the compatible work, reasons and warning.',word_range=[15,35])],
      'evaluation':[
      allreq(choose(f'{p}.e01','¿Qué opción falla solo por duración en la noche familiar?',['Long Weekend','Moon Door','Busy Neighbours'],0,ALL_CONCEPTS,'evaluation','Long Weekend has the right genre and age rating but exceeds 100 minutes.',source={'text':sources[1]},requires=ALL_CONCEPTS)),
      allreq(listen(f'{p}.e02','Escucha y elige la opción compatible.','The audience wants a comedy under one hundred minutes for age ten, with nothing scary. Busy Neighbours is a ninety-four-minute comedy for age ten.',['Busy Neighbours','Moon Door','Long Weekend'],0,ALL_CONCEPTS,'evaluation','Busy Neighbours satisfies genre, time, age and content limits.',requires=ALL_CONCEPTS)),
      allreq(multipart(f'{p}.e03','Completa cinco decisiones para justificar la recomendación.',['Género y trama de Busy Neighbours: ___.','Reacción o fortaleza textual: ___.','Conector y reserva equilibrada: ___.','Comparación con Moon Door: ___.','Recomendación para la audiencia: ___.'],[
        {'text':'comedy | two neighbours prepare a fair','accepted':['comedy | two neighbours prepare a fair','comedy | neighbours prepare a fair','comedy, two neighbours prepare a fair','comedy, neighbours prepare a fair']},
        {'text':'funny dialogue','accepted':['funny dialogue','amusing dialogue']},
        {'text':'however | predictable ending','accepted':['however | predictable ending','although | predictable ending','However, the ending is predictable','Although the ending is predictable']},
        {'text':'shorter but scary and age 12+','accepted':['shorter but scary and age 12+','shorter but frightening and age 12+']},
        {'text':'recommend Busy Neighbours | meets all limits','accepted':['recommend Busy Neighbours | meets all limits','Busy Neighbours | meets all limits','I recommend Busy Neighbours because it meets all limits','Busy Neighbours meets all limits']},
      ],ALL_CONCEPTS,'evaluation','Five independent fields demonstrate the cumulative review criteria.',5,source={'text':sources[1]},requires=ALL_CONCEPTS)),
      allreq(write(f'{p}.e04','Recomienda una de tres obras en 90–120 palabras.',sources[1],answers[1],ALL_CONCEPTS,'evaluation','The response compares all options and gives one justified choice plus warning.',word_range=[90,120],requires=ALL_CONCEPTS))],
      'review':[
      choose(f'{p}.r01','¿Qué límite descarta Last Goodbye?',['sad ending','55-minute length','modern setting'],0,ALL_CONCEPTS,'review','The sad ending conflicts with the explicit tone limit.',source={'text':sources[2]},requires=ALL_CONCEPTS),
      listen(f'{p}.r02','Escucha y elige la fortaleza de City Frequency.','The drama has clear voices, although its middle section repeats information.',['clear voices','historical setting','sad ending'],0,ALL_CONCEPTS,'review','Clear voices support the audience need for accessible dialogue.',requires=ALL_CONCEPTS),
      write(f'{p}.r03','Recupera la recomendación en 90–120 palabras.',sources[2],answers[2],ALL_CONCEPTS,'review','The new audio scenario compares three works and applies every audience restriction.',word_range=[90,120],requires=ALL_CONCEPTS)]}
    pools['evaluation'][2]['origin']['scoring']['requiredParts']=[0,3,4]; content_hash(pools['evaluation'][2])
    rem={f'{p}.e01':route(n,'t05','r01'),f'{p}.e02':route(n,'t06','r03',cumulative=True),f'{p}.e03':route(n,'t06','r03',cumulative=True),f'{p}.e04':route(n,'t06','r03',cumulative=True)}
    rows=[('Identify the audience genre, tone, length and content needs.','Identifica las necesidades de género, tono, extensión y contenido.','Every mandatory limit must be visible.'),('Compare all three options against the same needs.','Compara las tres opciones con las mismas necesidades.','Do not choose before checking every restriction.'),('Use although, however or because to balance the judgement.','Usa although, however o because para equilibrar la valoración.','A linker connects evidence and reservation.'),('Give plot context and evidence without revealing the ending.','Da contexto y evidencia sin revelar el final.','The recommendation includes a short review.'),('Recommend one compatible work and state a relevant warning.','Recomienda una obra compatible y da una advertencia relevante.','The warning must come from the source.'),('For a reading club, compare genre, plot, reaction, length and limits before making a balanced recommendation.','Para un club, compara género, trama, reacción, extensión y límites antes de recomendar.','This integrated model demonstrates all five concepts.')]
    rows[-1]=(answers[0][0],'Modelo: club lector; compara las tres obras y recomienda Garden Code con advertencia.','The 90–120 word model demonstrates all five concepts in a reading scenario.')
    doc=make_class(n,[('audience','audiencia'),('recommendation','recomendación'),('preference','preferencia'),('limit','límite'),('compare','comparar'),('warning','advertencia'),('judgement','valoración'),('plot','trama')],rows,pools,rem)
    doc['usesPatterns']=ALL_CONCEPTS; doc['cumulativeEvaluation']=ALL_CONCEPTS
    for item in doc['pools']['evaluation']: item['requires']=ALL_CONCEPTS; content_hash(item)
    return doc

BUILDERS={76:c76,77:c77,78:c78,79:c79,80:c80}

def audit(docs):
    assert len(docs) in (1,5) and sum(len(x['pools'][k]) for x in docs for k in x['pools'])==13*len(docs)
    for doc in docs:
        assert doc['status']=='shadow' and doc['runtimeAi'] is False
        assert [len(doc['pools'][k]) for k in ('practiceGuided','practice','evaluation','review')]==[3,3,4,3]
        assert len({i['id'] for pool in doc['pools'].values() for i in pool})==13
        assert len(doc['remediationMap'])==4
        assert len(doc['sequence'])==13
        assert Counter(step['role'] for step in doc['sequence'])==Counter({'presentation':4,'practice':2,'task':1,'quiz':1,'exam':4,'remediation':1})
        assert len({item['format'] for pool in doc['pools'].values() for item in pool})>=4
        for pool in doc['pools'].values():
            for item in pool:
                assert len(item['prompt']['es'])<=90
                scoring=item['origin'].get('scoring',{})
                if 'requiredParts' in scoring:
                    assert item['format']=='completar' and item['answer'].get('parts')
                    assert all(0<=index<len(item['answer']['parts']) for index in scoring['requiredParts'])
    final=docs[-1]
    if len(docs)==5:
        assert final['usesPatterns']==ALL_CONCEPTS and final['cumulativeEvaluation']==ALL_CONCEPTS
        assert all(i['requires']==ALL_CONCEPTS for i in final['pools']['evaluation'])
    if len(docs)==5:
        for n,lo,hi in ((79,80,100),(80,90,120)):
            doc=docs[n-76]
            assert all(lo<=len(re.findall(r"\b[\w’-]+\b",a))<=hi for pool in ('evaluation','review') for i in doc['pools'][pool] if i['format']=='escribir' for a in i['answer']['accepted'])
        c76,c77,c78,c79,c80=docs
        assert 80<=len(re.findall(r"\b[\w’-]+\b",c79['teaching'][5]['en']))<=100
        assert 90<=len(re.findall(r"\b[\w’-]+\b",c80['teaching'][5]['en']))<=120
        assert len(c76['pools']['evaluation'][3]['answer']['parts'])==4
        assert c77['pools']['evaluation'][3]['origin']['scoring']['minimumCorrect']==5
        assert c78['pools']['evaluation'][3]['origin']['scoring']['requiredParts']==[0,1,2,3,4]
        assert c80['pools']['evaluation'][2]['origin']['scoring']['requiredParts']==[0,3,4]
        assert c80['remediationMap']['en.n3.c80.e04']['reteachSteps']==[f'en.n3.class-{n:02d}.t06' for n in NUMBERS]
        assert all(token in c80['teaching'][5]['en'] for token in ('Garden Code','Red Tower','Winter Map'))
        assert 'Busy Neighbours' in c80['pools']['evaluation'][3]['origin']['text']
        assert 'City Frequency' in c80['pools']['review'][2]['origin']['text']
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
    bundle=OUT/'bundle-76-80.json'; bundle.write_text(json.dumps({'schema':'onelingo.editorial.class-bundle.v1','course':'en','level':3,'scale':'client-10-levels-v1','status':'shadow','runtimeAi':False,'variantSeed':VARIANT_SEED,'selectionPolicy':{'deterministic':True},'evidencePolicy':{'attemptRecords':['variantId','libraryVersion','selectionId']},'range':{'start':76,'end':80},'classes':docs},ensure_ascii=False,indent=2)+'\n')
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    report=REPORT_OUT/'REPORT.md'; report.write_text('# INTEGRADO — Inglés N3 C76–C80\n\nEstado: **integrado en shadow tras revisión independiente GO**.\n\n- 5 clases / 65 ítems: componentes de reseña, conectores, comprensión, producción y recomendación para audiencia.\n- Secuencia por clase: 4 presentación, 2 práctica, tarea, quiz, 4 examen y remediación.\n- C76–C78 usan completar multiparte; `requiredParts` protege postura/límite y decisión final.\n- C79 conserva 80–100 palabras y C80 90–120; todas las fuentes de escritura son visibles.\n- C80 demuestra los cinco conceptos en lectura, noche familiar y club de audio.\n- Variantes deterministas y shadow/no-AI.\n\n## Autoauditoría\n\nSe comprobaron fuentes consumibles, distractores plausibles, decisiones multiparte, remediación acumulativa y cinco perfiles de recorrido.\n\n```json\n'+json.dumps(summary,ensure_ascii=False,indent=2)+'\n```\n')
    files=paths+[bundle,report]; manifest=REPORT_OUT/'MANIFEST.sha256'
    entries=[f'{digest(__file__)}  ../../tools/contenido/generar_editorial_n3_76_80.py',f'{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json']
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

