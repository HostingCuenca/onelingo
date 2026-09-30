#!/usr/bin/env python3
"""Genera el mapa editorial N2 y las clases 01-15 en estado shadow.

El contenido es completamente editorial y determinista. El script no activa
unidades ni modifica el índice de curso que consume producción.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n2"
MAP_OUT = ROOT / "assets/contenido/en/plan-editorial/mapa-n2-editorial-v2.json"
SCALE = "client-10-levels-v1"


BLOCKS = [
    ("routines-expanded", "Rutinas y horarios con detalle", [
        ("Detailed daily schedules", "Horarios diarios detallados"),
        ("How often and how long", "Frecuencia y duración"),
        ("State and action verbs", "Verbos de estado y acción"),
        ("Explain a typical week", "Explicar una semana típica"),
        ("Routine profile: read and respond", "Perfil de rutina: leer y responder"),
    ]),
    ("present-contrast", "Rutina, temporalidad y cambios", [
        ("Temporary situations", "Situaciones temporales"),
        ("Actions happening around now", "Acciones alrededor del momento actual"),
        ("Present simple or continuous", "Presente simple o continuo"),
        ("Current projects and changes", "Proyectos y cambios actuales"),
        ("Routine versus now", "Rutina frente a ahora"),
    ]),
    ("past-simple-expanded", "Pasado simple para contar experiencias", [
        ("Regular past and time expressions", "Pasado regular y expresiones de tiempo"),
        ("Common irregular past verbs", "Verbos irregulares frecuentes"),
        ("Past negatives and questions", "Negaciones y preguntas en pasado"),
        ("Tell events in sequence", "Contar acontecimientos en secuencia"),
        ("A day that changed plans", "Un día que cambió los planes"),
    ]),
    ("past-narrative", "Detalles y contexto en una historia", [
        ("Was, were and past descriptions", "Was, were y descripciones pasadas"),
        ("There was and there were", "There was y there were"),
        ("Past continuous foundations", "Bases del pasado continuo"),
        ("Interrupted actions", "Acciones interrumpidas"),
        ("A short personal story", "Una historia personal breve"),
    ]),
    ("future-plans", "Planes con be going to", [
        ("Intentions for the near future", "Intenciones para el futuro cercano"),
        ("Evidence-based predictions", "Predicciones basadas en evidencia"),
        ("Ask about plans", "Preguntar por planes"),
        ("Plan a weekend", "Planificar un fin de semana"),
        ("Present a practical plan", "Presentar un plan práctico"),
    ]),
    ("future-decisions", "Arreglos, decisiones y predicciones", [
        ("Present continuous for arrangements", "Presente continuo para arreglos"),
        ("Will for instant decisions", "Will para decisiones instantáneas"),
        ("Will for neutral predictions", "Will para predicciones neutrales"),
        ("Choose the appropriate future", "Elegir el futuro apropiado"),
        ("Coordinate a group plan", "Coordinar un plan grupal"),
    ]),
    ("present-perfect-experience", "Experiencias hasta el presente", [
        ("Have and has with experiences", "Have y has con experiencias"),
        ("Ever and never", "Ever y never"),
        ("Been and gone", "Been y gone"),
        ("Ask follow-up questions", "Hacer preguntas de seguimiento"),
        ("Experience interview", "Entrevista sobre experiencias"),
    ]),
    ("present-perfect-time", "Pasado terminado y experiencia vigente", [
        ("Present perfect or past simple", "Present perfect o pasado simple"),
        ("Already, yet and just", "Already, yet y just"),
        ("For and since foundations", "Bases de for y since"),
        ("Recent news and details", "Noticias recientes y detalles"),
        ("Personal update", "Actualización personal"),
    ]),
    ("comparisons", "Comparar personas, lugares y opciones", [
        ("Short comparative adjectives", "Adjetivos comparativos cortos"),
        ("Long comparative adjectives", "Adjetivos comparativos largos"),
        ("Irregular comparatives", "Comparativos irregulares"),
        ("Compare two choices", "Comparar dos opciones"),
        ("Recommend the better option", "Recomendar la mejor opción"),
    ]),
    ("degree-and-superlatives", "Extremos, grado y suficiencia", [
        ("Superlatives in a group", "Superlativos en un grupo"),
        ("Too and not enough", "Too y not enough"),
        ("As ... as", "As ... as"),
        ("Describe advantages and limits", "Describir ventajas y límites"),
        ("Choose from three options", "Elegir entre tres opciones"),
    ]),
    ("quantity", "Cantidades y compras", [
        ("Countable and uncountable review", "Repaso de contables e incontables"),
        ("A few, a little and enough", "A few, a little y enough"),
        ("Too much and too many", "Too much y too many"),
        ("Plan quantities for an event", "Planificar cantidades para un evento"),
        ("Solve a shopping problem", "Resolver un problema de compras"),
    ]),
    ("obligation-advice", "Obligación, necesidad y consejo", [
        ("Have to and don't have to", "Have to y don't have to"),
        ("Must and mustn't", "Must y mustn't"),
        ("Should and shouldn't", "Should y shouldn't"),
        ("Explain rules and advice", "Explicar reglas y consejos"),
        ("A practical advice guide", "Una guía práctica de consejos"),
    ]),
    ("requests-permission", "Peticiones, permiso y ofrecimientos", [
        ("Can and could for requests", "Can y could para peticiones"),
        ("May and can for permission", "May y can para permiso"),
        ("Offers with can and shall", "Ofrecimientos con can y shall"),
        ("Respond politely", "Responder con cortesía"),
        ("Service conversation", "Conversación de servicio"),
    ]),
    ("travel", "Viajes y desplazamientos", [
        ("Transport and tickets", "Transporte y billetes"),
        ("Directions with landmarks", "Indicaciones con puntos de referencia"),
        ("Travel problems", "Problemas de viaje"),
        ("Ask for help while travelling", "Pedir ayuda durante un viaje"),
        ("Complete a travel plan", "Completar un plan de viaje"),
    ]),
    ("work-study", "Trabajo y estudio", [
        ("Tasks and responsibilities", "Tareas y responsabilidades"),
        ("Schedules and deadlines", "Horarios y plazos"),
        ("Give a short progress update", "Dar una actualización breve"),
        ("Ask for clarification", "Pedir una aclaración"),
        ("Work and study simulation", "Simulación de trabajo y estudio"),
    ]),
    ("health", "Salud y bienestar cotidiano", [
        ("Symptoms and body states", "Síntomas y estados físicos"),
        ("Advice for common problems", "Consejos para problemas comunes"),
        ("Appointments and instructions", "Citas e instrucciones"),
        ("Describe what happened", "Describir lo sucedido"),
        ("Health conversation", "Conversación sobre salud"),
    ]),
    ("city-services", "Vivienda, ciudad y servicios", [
        ("Home problems", "Problemas del hogar"),
        ("Public services", "Servicios públicos"),
        ("Report a problem", "Informar de un problema"),
        ("Arrange a repair", "Organizar una reparación"),
        ("Solve a neighbourhood issue", "Resolver un problema vecinal"),
    ]),
    ("technology", "Tecnología y comunicación", [
        ("Devices and basic actions", "Dispositivos y acciones básicas"),
        ("Messages and online plans", "Mensajes y planes en línea"),
        ("Explain a simple technical problem", "Explicar un problema técnico sencillo"),
        ("Give step-by-step instructions", "Dar instrucciones paso a paso"),
        ("Digital communication task", "Tarea de comunicación digital"),
    ]),
    ("social-problems", "Vida social y resolución de problemas", [
        ("Invitations and alternatives", "Invitaciones y alternativas"),
        ("Apologies and explanations", "Disculpas y explicaciones"),
        ("Agree and disagree politely", "Estar de acuerdo y discrepar con cortesía"),
        ("Find a compromise", "Encontrar un acuerdo"),
        ("Resolve a social plan", "Resolver un plan social"),
    ]),
    ("a2-capstone", "Cierre integrado A2", [
        ("Review: time and tense", "Repaso: tiempo y tiempos verbales"),
        ("Review: quantity and comparison", "Repaso: cantidad y comparación"),
        ("Review: modals and interaction", "Repaso: modales e interacción"),
        ("Integrated A2 project", "Proyecto integrado A2"),
        ("Final A2 performance", "Desempeño final A2"),
    ]),
]


def S(number, title_en, title_es, concept, vocab, models, extras, blanks, wrongs):
    return dict(number=number, title_en=title_en, title_es=title_es, concept=concept,
                vocab=vocab, models=models, extras=extras, blanks=blanks, wrongs=wrongs)


SPECS = [
S(1, "Detailed daily schedules", "Horarios diarios detallados", "n2-detailed-schedules",
  [("shift","turno"),("commute","desplazamiento"),("break","descanso"),("usually","normalmente"),("before","antes de"),("after","después de"),("weekday","día laborable"),("schedule","horario")],
  [("I usually start my shift at eight.","Normalmente empiezo mi turno a las ocho.","Usually va antes del verbo principal."),("My commute takes thirty minutes.","Mi desplazamiento dura treinta minutos.","Takes expresa duración."),("I have a short break before lunch.","Tengo un descanso corto antes del almuerzo.","Before sitúa una acción antes de otra."),("After work, I study for an hour.","Después del trabajo, estudio durante una hora.","After work abre la secuencia."),("On weekdays, my schedule is very regular.","Los días laborables, mi horario es muy regular.","On weekdays expresa frecuencia semanal.")],
  [("Maya begins work at nine.","Maya empieza a trabajar a las nueve."),("Her bus ride takes twenty minutes.","Su viaje en autobús dura veinte minutos."),("She checks her schedule before breakfast.","Ella revisa su horario antes del desayuno."),("We finish our shift at six.","Terminamos nuestro turno a las seis."),("On Tuesdays, Leo works from home.","Los martes, Leo trabaja desde casa."),("After dinner, I prepare my bag.","Después de cenar, preparo mi bolso.")],
  [("Completa: I ___ start my shift at eight.","usually"),("Completa: Her bus ride ___ twenty minutes.","takes"),("Completa: We finish our ___ at six.","shift"),("Completa: After dinner, I prepare my ___.","bag")],
  ["I usually starts my shift at eight.","Her bus ride take twenty minutes.","We finishes our shift at six.","On Tuesdays, Leo work from home."]),
S(2, "How often and how long", "Frecuencia y duración", "n2-frequency-duration",
  [("often","a menudo"),("twice","dos veces"),("once","una vez"),("month","mes"),("last","durar"),("hour","hora"),("every","cada"),("how long","cuánto tiempo")],
  [("How often do you exercise?","¿Con qué frecuencia haces ejercicio?","How often pregunta frecuencia."),("I exercise twice a week.","Hago ejercicio dos veces por semana.","Twice a week indica dos ocasiones."),("How long does the class last?","¿Cuánto dura la clase?","How long pregunta duración."),("The class lasts for an hour.","La clase dura una hora.","For introduce la duración."),("We meet once every month.","Nos reunimos una vez cada mes.","Once every month expresa periodicidad.")],
  [("Nora calls her parents twice a week.","Nora llama a sus padres dos veces por semana."),("The meeting lasts forty minutes.","La reunión dura cuarenta minutos."),("How often does Sam cook at home?","¿Con qué frecuencia cocina Sam en casa?"),("I visit the library once a month.","Visito la biblioteca una vez al mes."),("How long do your lessons last?","¿Cuánto duran tus clases?"),("We walk every Saturday morning.","Caminamos cada sábado por la mañana.")],
  [("Completa: I exercise ___ a week.","twice"),("Completa: The meeting ___ forty minutes.","lasts"),("Completa: How ___ does Sam cook at home?","often"),("Completa: We walk ___ Saturday morning.","every")],
  ["How often you do exercise?","The meeting last forty minutes.","How often Sam does cook at home?","How long your lessons do last?"]),
S(3, "State and action verbs", "Verbos de estado y acción", "n2-state-action-verbs",
  [("believe","creer"),("need","necesitar"),("prefer","preferir"),("understand","entender"),("belong","pertenecer"),("carry","llevar"),("wait","esperar"),("know","saber"),("tea","té"),("key","llave"),("boxes","cajas")],
  [("I understand the instructions.","Entiendo las instrucciones.","Understand describe un estado mental."),("She prefers tea to coffee.","Ella prefiere té en vez de café.","Prefer suele usarse en presente simple."),("This key belongs to Omar.","Esta llave pertenece a Omar.","Belong expresa posesión estable."),("We need more time.","Necesitamos más tiempo.","Need describe una necesidad."),("He is carrying two boxes now.","Ahora está llevando dos cajas.","Carry es una acción visible en progreso.")],
  [("I believe your story.","Creo tu historia."),("Lina knows the answer.","Lina sabe la respuesta."),("They are waiting outside now.","Ahora están esperando fuera."),("This jacket belongs to me.","Esta chaqueta me pertenece."),("We prefer the earlier train.","Preferimos el tren más temprano."),("I am carrying my laptop today.","Hoy estoy llevando mi portátil.")],
  [("Completa: I ___ the instructions.","understand"),("Completa: Lina ___ the answer.","knows"),("Completa: They are ___ outside now.","waiting"),("Completa: This jacket ___ to me.","belongs")],
  ["I am understanding the instructions.","Lina is know the answer.","They waiting outside now.","This jacket is belonging to me."]),
S(4, "Explain a typical week", "Explicar una semana típica", "n2-typical-week",
  [("normally","normalmente"),("occasionally","ocasionalmente"),("during","durante"),("evening","tarde-noche"),("appointment","cita"),("training","entrenamiento"),("chores","tareas domésticas"),("weekend","fin de semana")],
  [("I normally work from Monday to Friday.","Normalmente trabajo de lunes a viernes.","Normally resume el patrón habitual."),("During the week, I have two appointments.","Durante la semana, tengo dos citas.","During introduce un periodo."),("I occasionally train in the evening.","Ocasionalmente entreno por la tarde-noche.","Occasionally indica baja frecuencia."),("On Saturday, we do our household chores.","El sábado hacemos las tareas domésticas.","On se usa con días."),("At the weekend, I make time for friends.","El fin de semana reservo tiempo para amigos.","At the weekend presenta el cierre semanal.")],
  [("Ravi normally studies in the morning.","Ravi normalmente estudia por la mañana."),("During the week, he works three shifts.","Durante la semana trabaja tres turnos."),("He occasionally has a late appointment.","Ocasionalmente tiene una cita tarde."),("On Thursday, he attends training.","El jueves asiste a entrenamiento."),("At the weekend, Ravi visits his family.","El fin de semana Ravi visita a su familia."),("On Sunday evening, he plans the next week.","El domingo por la tarde planifica la semana siguiente.")],
  [("Completa: I ___ work from Monday to Friday.","normally"),("Completa: ___ the week, he works three shifts.","During"),("Completa: He occasionally has a late ___.","appointment"),("Completa: On Sunday evening, he ___ the next week.","plans")],
  ["I normally works from Monday to Friday.","During the week, he work three shifts.","He occasionally have a late appointment.","At the weekend, Ravi visit his family."]),
S(5, "Routine profile: read and respond", "Perfil de rutina: leer y responder", "n2-routine-profile",
  [("profile","perfil"),("flexible","adaptable"),("fixed","fijo"),("rarely","rara vez"),("team","equipo"),("online","en línea"),("deadline","plazo"),("balance","equilibrio")],
  [("Eva has a flexible work schedule.","Eva tiene un horario laboral flexible.","Has describe su situación habitual."),("She usually meets her team online.","Normalmente se reúne con su equipo en línea.","Usually sitúa la frecuencia."),("Her deadlines are fixed, but her hours are not.","Sus plazos son fijos, pero sus horas no.","But contrasta dos datos."),("She rarely works after seven.","Rara vez trabaja después de las siete.","Rarely va antes del verbo principal."),("This routine gives her a good balance.","Esta rutina le da un buen equilibrio.","This routine resume el perfil.")],
  [("Tom has a fixed morning shift.","Tom tiene un turno fijo de mañana."),("He meets his team in person twice a week.","Se reúne con su equipo en persona dos veces por semana."),("His commute lasts about forty minutes.","Su desplazamiento dura unos cuarenta minutos."),("Tom rarely checks email at night.","Tom rara vez revisa el correo por la noche."),("His profile shows a regular weekday routine.","Su perfil muestra una rutina laboral regular."),("At the weekend, he chooses a flexible schedule.","El fin de semana elige un horario flexible.")],
  [("Completa: Eva has a ___ work schedule.","flexible"),("Completa: His commute ___ about forty minutes.","lasts"),("Completa: Tom ___ checks email at night.","rarely"),("Completa: He chooses a flexible ___.","schedule")],
  ["Eva have a flexible work schedule.","His commute last about forty minutes.","Tom rare checks email at night.","His profile show a regular weekday routine."]),
S(6, "Temporary situations", "Situaciones temporales", "n2-temporary-situations",
  [("temporarily","temporalmente"),("stay","alojarse"),("project","proyecto"),("this week","esta semana"),("currently","actualmente"),("share","compartir"),("office","oficina"),("until","hasta"),("cousin","primo"),("bus","autobús"),("desk","escritorio")],
  [("I am staying with my cousin this week.","Me estoy alojando con mi primo esta semana.","El continuo describe una situación temporal."),("She is currently working on a new project.","Actualmente trabaja en un proyecto nuevo.","Currently refuerza la temporalidad."),("We are sharing an office until Friday.","Estamos compartiendo una oficina hasta el viernes.","Until marca el límite temporal."),("They are taking the bus this month.","Este mes están tomando el autobús.","This month contrasta con un hábito estable."),("He is not using his usual desk today.","Hoy no está usando su escritorio habitual.","Not va después de is.")],
  [("Mina is staying near the station this week.","Mina se aloja cerca de la estación esta semana."),("Her team is working in a temporary office.","Su equipo trabaja en una oficina temporal."),("They are sharing two meeting rooms.","Están compartiendo dos salas de reuniones."),("I am taking an evening course this month.","Este mes estoy haciendo un curso nocturno."),("We are not following the usual schedule today.","Hoy no seguimos el horario habitual."),("Leo is helping with the project until June.","Leo está ayudando con el proyecto hasta junio.")],
  [("Completa: I am ___ with my cousin this week.","staying"),("Completa: Her team is ___ in a temporary office.","working"),("Completa: We are not ___ the usual schedule today.","following"),("Completa: Leo is helping ___ June.","until")],
  ["I staying with my cousin this week.","Her team working in a temporary office.","We not are following the usual schedule today.","Leo helping with the project until June."]),
S(7, "Actions happening around now", "Acciones alrededor del momento actual", "n2-around-now",
  [("improve","mejorar"),("prepare","preparar"),("course","curso"),("these days","estos días"),("research","investigar"),("develop","desarrollar"),("practice","practicar"),("recently","últimamente"),("English","inglés"),("exam","examen"),("transport","transporte"),("days","días")],
  [("I am improving my English these days.","Estoy mejorando mi inglés estos días.","These days abarca un periodo actual."),("She is preparing for an exam.","Se está preparando para un examen.","La acción está en desarrollo."),("We are developing a new course.","Estamos desarrollando un curso nuevo.","El proyecto ocurre alrededor de ahora."),("They are researching local transport.","Están investigando el transporte local.","Researching expresa trabajo en curso."),("He is practicing more these days.","Estos días está practicando más.","These days señala un cambio actual.")],
  [("Sara is learning to drive these days.","Sara está aprendiendo a conducir estos días."),("Her brother is preparing a presentation.","Su hermano está preparando una presentación."),("We are improving the online course.","Estamos mejorando el curso en línea."),("I am researching new study methods.","Estoy investigando nuevos métodos de estudio."),("They are practicing together this month.","Están practicando juntos este mes."),("Omar is developing a simple website.","Omar está desarrollando un sitio web sencillo.")],
  [("Completa: I am ___ my English these days.","improving"),("Completa: Her brother is ___ a presentation.","preparing"),("Completa: They are ___ together this month.","practicing"),("Completa: Omar is ___ a simple website.","developing")],
  ["I improving my English these days.","Her brother are preparing a presentation.","They is practicing together this month.","Omar develop a simple website now."]),
S(8, "Present simple or continuous", "Presente simple o continuo", "n2-simple-continuous-contrast",
  [("every day","cada día"),("right now","ahora mismo"),("usually","normalmente"),("today","hoy"),("deliver","entregar"),("cycle","ir en bicicleta"),("normally","normalmente"),("instead","en cambio"),("customer","cliente")],
  [("I cycle to work every day.","Voy al trabajo en bicicleta cada día.","El presente simple expresa rutina."),("Today, I am taking the bus instead.","Hoy estoy tomando el autobús en cambio.","El continuo expresa una excepción temporal."),("She usually delivers orders in the morning.","Normalmente entrega pedidos por la mañana.","Usually acompaña al hábito."),("Right now, she is helping a customer.","Ahora mismo está ayudando a un cliente.","Right now exige una acción en curso."),("We normally eat at home, but today we are eating out.","Normalmente comemos en casa, pero hoy comemos fuera.","But contrasta rutina y situación actual.")],
  [("Ben walks to class every day.","Ben camina a clase cada día."),("This morning, he is riding with a friend.","Esta mañana está yendo con un amigo."),("They usually serve lunch at noon.","Normalmente sirven el almuerzo al mediodía."),("Right now, they are preparing breakfast.","Ahora mismo están preparando el desayuno."),("I normally work upstairs.","Normalmente trabajo arriba."),("Today, I am using the meeting room instead.","Hoy estoy usando la sala de reuniones en cambio.")],
  [("Completa: I ___ to work every day.","cycle"),("Completa: He is ___ with a friend this morning.","riding"),("Completa: They usually ___ lunch at noon.","serve"),("Completa: Today, I am ___ the meeting room.","using")],
  ["I am cycle to work every day.","He rides with a friend right now.","They are usually serve lunch at noon.","Today, I use the meeting room right now."]),
S(9, "Current projects and changes", "Proyectos y cambios actuales", "n2-current-projects",
  [("change","cambiar"),("grow","crecer"),("become","volverse"),("update","actualizar"),("system","sistema"),("neighbourhood","barrio"),("busier","más ocupado"),("gradually","gradualmente"),("schedule","horario")],
  [("Our neighbourhood is becoming busier.","Nuestro barrio se está volviendo más concurrido.","Becoming describe un cambio en progreso."),("The company is updating its system.","La empresa está actualizando su sistema.","Updating señala un proyecto actual."),("My responsibilities are growing gradually.","Mis responsabilidades están creciendo gradualmente.","Gradually describe cambio progresivo."),("We are changing the class schedule.","Estamos cambiando el horario de clases.","Changing presenta una modificación actual."),("The team is testing the new update.","El equipo está probando la nueva actualización.","Testing muestra una fase del proyecto.")],
  [("The town is becoming more popular.","La ciudad se está volviendo más popular."),("Our office is changing its booking system.","Nuestra oficina está cambiando su sistema de reservas."),("The project is growing every week.","El proyecto está creciendo cada semana."),("I am updating the contact list.","Estoy actualizando la lista de contactos."),("The streets are getting busier this month.","Las calles se están volviendo más concurridas este mes."),("We are testing a simpler schedule.","Estamos probando un horario más sencillo.")],
  [("Completa: The neighbourhood is ___ busier.","becoming"),("Completa: Our office is ___ its booking system.","changing"),("Completa: I am ___ the contact list.","updating"),("Completa: We are ___ a simpler schedule.","testing")],
  ["Our neighbourhood becoming busier.","Our office are changing its booking system.","I updating the contact list.","We testing a simpler schedule."]),
S(10, "Routine versus now", "Rutina frente a ahora", "n2-routine-now-integration",
  [("normally","normalmente"),("currently","actualmente"),("temporary","temporal"),("routine","rutina"),("instead","en cambio"),("because","porque"),("these days","estos días"),("contrast","contraste"),("home","casa"),("team","equipo")],
  [("Nadia normally works at the main office.","Nadia normalmente trabaja en la oficina principal.","Normally introduce la rutina."),("These days, she is working from home.","Estos días está trabajando desde casa.","These days introduce la excepción temporal."),("She is using a different computer because hers is broken.","Está usando otro ordenador porque el suyo está averiado.","Because explica el cambio."),("Her team usually meets on Mondays.","Su equipo normalmente se reúne los lunes.","Usually expresa el patrón estable."),("This week, they are meeting on Tuesday instead.","Esta semana se reúnen el martes en cambio.","Instead marca la alternativa actual.")],
  [("Luis normally studies in the library.","Luis normalmente estudia en la biblioteca."),("Today, he is studying at home.","Hoy está estudiando en casa."),("His class usually starts at ten.","Su clase normalmente empieza a las diez."),("This week, it is starting at eleven.","Esta semana empieza a las once."),("He is following a temporary schedule.","Está siguiendo un horario temporal."),("The contrast explains his late lunch.","El contraste explica su almuerzo tardío.")],
  [("Completa: Nadia ___ works at the main office.","normally"),("Completa: Today, he is ___ at home.","studying"),("Completa: This week, it is ___ at eleven.","starting"),("Completa: He is following a ___ schedule.","temporary")],
  ["Nadia normally working at the main office.","Today, he studies at home right now.","This week, it starting at eleven.","He following a temporary schedule."]),
S(11, "Regular past and time expressions", "Pasado regular y expresiones de tiempo", "n2-regular-past",
  [("yesterday","ayer"),("last night","anoche"),("visited","visitó"),("finished","terminó"),("arrived","llegó"),("called","llamó"),("ago","hace"),("planned","planificó")],
  [("I visited my aunt yesterday.","Visité a mi tía ayer.","-ed marca el pasado regular."),("We finished the report last night.","Terminamos el informe anoche.","Last night fija el tiempo pasado."),("The bus arrived ten minutes ago.","El autobús llegó hace diez minutos.","Ago cuenta desde el presente hacia atrás."),("She called me after dinner.","Me llamó después de cenar.","Called es el pasado de call."),("They planned the trip on Monday.","Planificaron el viaje el lunes.","Plan dobla la consonante antes de -ed.")],
  [("Marta cleaned the kitchen yesterday.","Marta limpió la cocina ayer."),("We watched a film last night.","Vimos una película anoche."),("The train arrived an hour ago.","El tren llegó hace una hora."),("I emailed the office after lunch.","Envié un correo a la oficina después del almuerzo."),("They booked the tickets on Friday.","Reservaron los billetes el viernes."),("Sam studied for the test last weekend.","Sam estudió para el examen el fin de semana pasado.")],
  [("Completa: I ___ my aunt yesterday.","visited"),("Completa: We ___ a film last night.","watched"),("Completa: The train ___ an hour ago.","arrived"),("Completa: Sam ___ for the test.","studied")],
  ["I visit my aunt yesterday.","We watch a film last night.","The train arrive an hour ago.","They book the tickets on Friday."]),
S(12, "Common irregular past verbs", "Verbos irregulares frecuentes", "n2-irregular-past",
  [("went","fue"),("had","tuvo"),("made","hizo"),("saw","vio"),("took","tomó"),("bought","compró"),("came","vino"),("gave","dio")],
  [("We went to the market early.","Fuimos al mercado temprano.","Went es el pasado de go."),("I had a quick breakfast.","Tomé un desayuno rápido.","Had es el pasado de have."),("She made a list before shopping.","Hizo una lista antes de comprar.","Made es el pasado de make."),("They saw an old friend there.","Vieron allí a un viejo amigo.","Saw es el pasado de see."),("He took the last bus home.","Tomó el último autobús a casa.","Took es el pasado de take.")],
  [("Nina bought fresh bread.","Nina compró pan fresco."),("Her brother came with her.","Su hermano vino con ella."),("They went to a small café.","Fueron a una cafetería pequeña."),("I gave the driver the address.","Le di la dirección al conductor."),("We had lunch near the station.","Almorzamos cerca de la estación."),("Omar took a photo of the square.","Omar tomó una foto de la plaza.")],
  [("Completa: We ___ to the market early.","went"),("Completa: Her brother ___ with her.","came"),("Completa: We ___ lunch near the station.","had"),("Completa: Omar ___ a photo.","took")],
  ["We goed to the market early.","Her brother comed with her.","We haved lunch near the station.","Omar taked a photo of the square."]),
S(13, "Past negatives and questions", "Negaciones y preguntas en pasado", "n2-past-questions-negatives",
  [("did","auxiliar de pasado"),("didn't","no hizo"),("why","por qué"),("when","cuándo"),("leave","salir"),("find","encontrar"),("remember","recordar"),("answer","responder")],
  [("Did you find the address?","¿Encontraste la dirección?","Did abre la pregunta en pasado."),("I didn't find it at first.","No la encontré al principio.","Después de didn't va el verbo base."),("When did the meeting start?","¿Cuándo empezó la reunión?","Did mantiene start en forma base."),("Why did Ana leave early?","¿Por qué Ana se fue temprano?","Why pide una razón."),("She didn't remember the room number.","No recordó el número de sala.","Didn't remember expresa negación pasada.")],
  [("Did Leo answer your message?","¿Leo respondió tu mensaje?"),("He didn't answer yesterday.","No respondió ayer."),("Where did you leave the keys?","¿Dónde dejaste las llaves?"),("I didn't see them on the desk.","No las vi en el escritorio."),("When did the bus arrive?","¿Cuándo llegó el autobús?"),("Why did they change the time?","¿Por qué cambiaron la hora?")],
  [("Completa: ___ you find the address?","Did"),("Completa: He ___ answer yesterday.","didn't"),("Completa: Where did you ___ the keys?","leave"),("Completa: Why did they ___ the time?","change")],
  ["Did you found the address?","He didn't answered yesterday.","Where you did leave the keys?","Why did they changed the time?"]),
S(14, "Tell events in sequence", "Contar acontecimientos en secuencia", "n2-past-sequence",
  [("first","primero"),("then","después"),("next","a continuación"),("finally","finalmente"),("suddenly","de repente"),("missed","perdió"),("returned","regresó"),("noticed","notó")],
  [("First, I checked the train time.","Primero revisé la hora del tren.","First inicia la secuencia."),("Then, I walked to the station.","Después caminé hasta la estación.","Then añade el segundo paso."),("Next, I bought my ticket.","A continuación compré mi billete.","Next continúa el orden."),("Suddenly, I noticed the wrong platform.","De repente noté el andén equivocado.","Suddenly introduce un evento inesperado."),("Finally, I returned home by bus.","Finalmente regresé a casa en autobús.","Finally cierra la historia.")],
  [("First, Maya packed her bag.","Primero Maya preparó su bolso."),("Then, she called a taxi.","Después llamó a un taxi."),("Next, the taxi stopped in traffic.","A continuación el taxi se detuvo en el tráfico."),("Suddenly, Maya noticed the time.","De repente Maya notó la hora."),("She missed the first train.","Perdió el primer tren."),("Finally, she took the next one.","Finalmente tomó el siguiente.")],
  [("Completa: ___, I checked the train time.","First"),("Completa: ___, she called a taxi.","Then"),("Completa: She ___ the first train.","missed"),("Completa: ___, she took the next one.","Finally")],
  ["First, I check the train time yesterday.","Then, she call a taxi.","She miss the first train.","Finally, she take the next one."]),
S(15, "A day that changed plans", "Un día que cambió los planes", "n2-past-reading-integration",
  [("cancelled","canceló"),("storm","tormenta"),("decided","decidió"),("journey","viaje"),("instead","en cambio"),("safe","seguro"),("message","mensaje"),("unexpected","inesperado")],
  [("The train company cancelled our morning train.","La compañía ferroviaria canceló nuestro tren de la mañana.","Cancelled es un pasado regular con objeto."),("A storm changed our travel plans.","Una tormenta cambió nuestros planes de viaje.","Changed es pasado regular."),("We decided to stay in town instead.","Decidimos quedarnos en la ciudad en cambio.","Decided to presenta la nueva decisión."),("I sent my family a message.","Envié un mensaje a mi familia.","Sent es pasado irregular."),("Finally, we found a safe place to stay.","Finalmente encontramos un lugar seguro donde alojarnos.","Found cierra la solución.")],
  [("The airport closed because of the storm.","El aeropuerto cerró por la tormenta."),("Mia didn't continue her journey.","Mia no continuó su viaje."),("She called the hotel and changed the booking.","Llamó al hotel y cambió la reserva."),("Then, she bought a ticket for the next day.","Después compró un billete para el día siguiente."),("Her brother came to meet her.","Su hermano vino a encontrarla."),("The unexpected day ended safely.","El día inesperado terminó de forma segura.")],
  [("Completa: The company ___ our morning train.","cancelled"),("Completa: Mia didn't ___ her journey.","continue"),("Completa: She ___ a ticket for the next day.","bought"),("Completa: The day ended ___.","safely")],
  ["The train company cancel our morning train.","Mia didn't continued her journey.","She buy a ticket for the next day.","The unexpected day end safely."]),
]


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def add_hash(item):
    payload = {key: value for key, value in item.items() if key not in {"id", "contentHash"}}
    item["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return item


def accessibility():
    return {"screenReader": True, "highContrast": True, "largeText": True}


def base_item(item_id, fmt, prompt, concept, pool, feedback):
    origin = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided":
        origin["hint"] = {"es": "Vuelve al modelo de la explicación antes de responder."}
    return {"id": item_id, "format": fmt, "prompt": {"es": prompt}, "answer": {}, "choices": [],
            "teaches": [concept] if pool == "practiceGuided" else [],
            "requires": [] if pool == "practiceGuided" else [concept],
            "origin": origin, "accessibility": accessibility()}


def choice(item_id, prompt, correct, wrong, concept, pool):
    item = base_item(item_id, "elegir", prompt, concept, pool, "La forma correcta conserva el tiempo y el orden del modelo.")
    item["choices"] = [{"text": correct}, {"text": wrong}]
    item["answer"] = {"index": 0}
    return add_hash(item)


def completion(item_id, prompt, answer, concept, pool):
    item = base_item(item_id, "completar", prompt, concept, pool, f"{answer} completa correctamente la frase.")
    item["answer"] = {"text": answer, "accepted": [answer]}
    return add_hash(item)


def ordering(item_id, prompt, sentence, concept, pool):
    item = base_item(item_id, "ordenar", prompt, concept, pool, "El orden correcto sigue el patrón presentado en la clase.")
    item["answer"] = {"text": sentence, "tokens": sentence.split()}
    return add_hash(item)


def listening(item_id, prompt, audio, wrong, concept, pool):
    item = base_item(item_id, "escuchar", prompt, concept, pool, "La opción correcta reproduce exactamente la idea del audio.")
    item["choices"] = [{"text": audio}, {"text": wrong}]
    item["answer"] = {"index": 0}
    item["origin"].update({"audio": audio, "audioMode": "tts", "languageCode": "en", "speedOptions": [0.75, 1.0],
                           "maxReplays": 3, "revealTranscriptAfterAttempt": True})
    return add_hash(item)


def matching(item_id, pairs, concept):
    item = base_item(item_id, "relacionar", "Relaciona las expresiones nuevas con su significado.", concept, "review",
                     "Cada expresión queda vinculada con su significado contextual.")
    values = [[left, {"es": right}] for left, right in pairs]
    item["origin"]["pairs"] = values
    item["answer"] = {"pairs": values}
    return add_hash(item)


def segments(en, es):
    en_words, es_words = en.split(), es.split()
    en_mid, es_mid = max(1, len(en_words)//2), max(1, len(es_words)//2)
    return [{"en": " ".join(en_words[:en_mid]), "es": " ".join(es_words[:es_mid])},
            {"en": " ".join(en_words[en_mid:]), "es": " ".join(es_words[es_mid:])}]


def build_class(spec):
    n, concept = spec["number"], spec["concept"]
    cid = f"en.n2.class-{n:02d}"
    previous = "en.n1.class-100" if n == 1 else f"en.n2.class-{n-1:02d}"
    teaching = []
    for i, (en, es, explanation) in enumerate(spec["models"], 1):
        teaching.append({"id": f"{cid}.t{i:02d}", "en": en, "es": es, "explanationEs": explanation,
                         "segments": segments(en, es), "audioText": en, "audioMode": "tts", "languageCode": "en",
                         "patternId": concept})
    models = [entry[0] for entry in spec["models"]]
    extras = [entry[0] for entry in spec["extras"]]
    blanks = spec["blanks"]
    pfx = f"en.n2.c{n:02d}"
    pools = {
        "practiceGuided": [
            choice(f"{pfx}.pg01", "Elige el modelo correcto para la idea trabajada.", models[0], spec["wrongs"][0], concept, "practiceGuided"),
            completion(f"{pfx}.pg02", blanks[0][0], blanks[0][1], concept, "practiceGuided"),
            ordering(f"{pfx}.pg03", "Ordena el tercer modelo de la clase.", models[2], concept, "practiceGuided"),
        ],
        "practice": [
            choice(f"{pfx}.p01", "Elige la frase correcta en el contexto nuevo.", extras[0], spec["wrongs"][1], concept, "practice"),
            completion(f"{pfx}.p02", blanks[1][0], blanks[1][1], concept, "practice"),
            listening(f"{pfx}.p03", "Escucha y elige la oración exacta.", models[4], spec["wrongs"][2], concept, "practice"),
        ],
        "evaluation": [
            choice(f"{pfx}.e01", "Elige la opción gramatical y contextualmente correcta.", extras[3], spec["wrongs"][2], concept, "evaluation"),
            completion(f"{pfx}.e02", blanks[2][0], blanks[2][1], concept, "evaluation"),
            ordering(f"{pfx}.e03", "Ordena una frase nueva de evaluación.", extras[2], concept, "evaluation"),
            listening(f"{pfx}.e04", "Escucha y selecciona la información correcta.", extras[4], spec["wrongs"][3], concept, "evaluation"),
        ],
        "review": [
            matching(f"{pfx}.r01", spec["vocab"][:2], concept),
            completion(f"{pfx}.r02", blanks[3][0], blanks[3][1], concept, "review"),
            ordering(f"{pfx}.r03", "Ordena la frase de repaso espaciado.", extras[5], concept, "review"),
        ],
    }
    cumulative = None
    if n % 5 == 0:
        cumulative = [SPECS[index-1]["concept"] for index in range(n-4, n+1)]
        for index, item in enumerate(pools["evaluation"]):
            item["requires"] = [cumulative[index], concept] if cumulative[index] != concept else [concept]
            item["contentHash"] = ""
            add_hash(item)
        pools["evaluation"][3]["requires"] = list(dict.fromkeys([*pools["evaluation"][3]["requires"], cumulative[4]]))
        pools["evaluation"][3]["contentHash"] = ""
        add_hash(pools["evaluation"][3])
    result = {
        "schema": "onelingo.editorial.class.v1", "course": "en", "level": 2, "scale": SCALE,
        "status": "shadow", "runtimeAi": False,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": {"chronologyTokens": "enforce", "answerReuseAcrossEarlyReserved": "forbid",
                          "answerEvidenceReuseAcrossPools": "forbid"},
        "id": cid, "title": {"en": spec["title_en"], "es": spec["title_es"]},
        "concepts": [concept], "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [previous],
        "usesVocabulary": [value for value, _ in spec["vocab"]], "usesPatterns": [concept],
        "objectives": {"es": [f"Comprender y usar {spec['title_es'].lower()} en situaciones A2.",
                                "Distinguir el patrón en lectura y escucha.",
                                "Producir una respuesta breve sin apoyo dinámico."]},
        "vocabulary": [{"en": en, "es": es} for en, es in spec["vocab"]],
        "teaching": teaching, "pools": pools,
        "remediationMap": {f"{pfx}.e{i:02d}": {"reteach": f"{cid}.t{i:02d}", "review": f"{pfx}.r{min(i,3):02d}"}
                           for i in range(1,5)},
        "accessibility": {"highContrast": True, "largeText": True, "screenReader": True, "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2, "allowAudioReplay": True, "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True},
    }
    if cumulative:
        result["cumulativeEvaluation"] = cumulative
    return result


def build_map():
    classes = []
    number = 0
    for block, (slug, theme, titles) in enumerate(BLOCKS, 1):
        for position, (en, es) in enumerate(titles, 1):
            number += 1
            previous = "en.n1.class-100" if number == 1 else f"en.n2.class-{number-1:02d}"
            classes.append({"id": f"en.n2.class-{number:02d}", "level": 2, "cefr": "A2", "block": block,
                            "position": position, "theme": slug, "themeEs": theme, "title": {"en": en, "es": es},
                            "phase": ["input", "form", "comprehension", "production", "transfer"][position-1],
                            "prerequisites": [previous], "status": "shadow" if number <= 15 else "planned",
                            "runtimeAi": False})
    return {"schema": "onelingo.editorial.map.v2", "course": "en", "level": 2, "cefr": "A2", "scale": SCALE,
            "totalClasses": 100, "totalBlocks": 20, "authority": "editorial-v2",
            "note": "Sustituye la alternancia de destrezas del PDF por secuencias completas de cinco fases.",
            "classes": classes}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    classes = [build_class(spec) for spec in SPECS]
    for cls in classes:
        number = int(cls["id"].rsplit("-", 1)[1])
        (OUT / f"class-{number:02d}.json").write_text(json.dumps(cls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for start in (1, 6, 11):
        selected = classes[start-1:start+4]
        bundle = {"schema": "onelingo.editorial.class-bundle.v1", "course": "en", "level": 2, "scale": SCALE,
                  "status": "shadow", "runtimeAi": False, "classes": selected,
                  "selectionPolicy": {"deterministic": True},
                  "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]}}
        (OUT / f"bundle-{start:02d}-{start+4:02d}.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MAP_OUT.write_text(json.dumps(build_map(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: N2 map 100 classes; authored {len(classes)} classes; {len(classes)*13} exercises; shadow/no-AI")


if __name__ == "__main__":
    main()
