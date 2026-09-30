#!/usr/bin/env python3
"""Regenera Inglés N2 C31-C45 bajo el contrato editorial-agent.v2."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import generar_editorial_n2_26_30 as base


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n2"
SCALE = "client-10-levels-v1"
PHASES = {number: ("input", "form", "comprehension", "production", "transfer")[(number - 31) % 5]
          for number in range(31, 46)}
TITLES = {
    31: ("Have and has with experiences", "Have y has con experiencias"),
    32: ("Ever and never", "Ever y never"),
    33: ("Been and gone", "Been y gone"),
    34: ("Ask follow-up questions", "Hacer preguntas de seguimiento"),
    35: ("Experience interview", "Entrevista sobre experiencias"),
    36: ("Present perfect or past simple", "Present perfect o pasado simple"),
    37: ("Already, yet and just", "Already, yet y just"),
    38: ("For and since foundations", "Bases de for y since"),
    39: ("Recent news and details", "Noticias recientes y detalles"),
    40: ("Personal update", "Actualización personal"),
    41: ("Short comparative adjectives", "Adjetivos comparativos cortos"),
    42: ("Long comparative adjectives", "Adjetivos comparativos largos"),
    43: ("Irregular comparatives", "Comparativos irregulares"),
    44: ("Compare two choices", "Comparar dos opciones"),
    45: ("Recommend the better option", "Recomendar la mejor opción"),
}
CONCEPTS = {
    31: "n2-present-perfect-have-has-experience",
    32: "n2-present-perfect-ever-never",
    33: "n2-present-perfect-been-gone",
    34: "n2-experience-follow-up-questions",
    35: "n2-experience-interview",
    36: "n2-present-perfect-past-simple-choice",
    37: "n2-present-perfect-already-yet-just",
    38: "n2-present-perfect-for-since",
    39: "n2-recent-news-details",
    40: "n2-personal-update",
    41: "n2-short-comparatives",
    42: "n2-long-comparatives",
    43: "n2-irregular-comparatives",
    44: "n2-compare-two-choices",
    45: "n2-recommend-better-option",
}

# Cada especificación conserva ejemplos de enseñanza y evidencias reservadas distintas.
# Los generadores no llaman servicios externos ni modelos en tiempo de ejecución.
SPECS = {
    31: {
        "rule": "Have acompaña I, you, we y they; has acompaña he, she e it en experiencias.",
        "vocab": [("tried", "probado"), ("visited", "visitado"), ("ridden", "montado"),
                  ("cooked", "cocinado"), ("climbed", "escalado"), ("experience", "experiencia")],
        "teaching": [
            ("I have tried Indian food.", "He probado comida india."),
            ("She has visited Bogotá twice.", "Ella ha visitado Bogotá dos veces."),
            ("We have ridden horses near the farm.", "Hemos montado caballos cerca de la granja."),
            ("Leo has climbed a mountain and cooked outdoors.", "Leo ha escalado una montaña y cocinado al aire libre."),
            ("That experience has changed my plans.", "Esa experiencia ha cambiado mis planes."),
        ],
        "choice": [("Maya habla de una comida que probó alguna vez.", "Maya has tried ceviche.",
                    ["Maya have tried ceviche.", "Maya has try ceviche."]),
                   ("El profesor cuenta un logro sin indicar una fecha terminada.", "Our teacher has climbed Cotopaxi.",
                    ["Our teacher have climbed Cotopaxi.", "Our teacher has climb Cotopaxi."])],
        "complete": [("Completa el auxiliar: My brother ___ flown in a small plane.", "has"),
                     ("Completa el auxiliar: We ___ seen an English play.", "have")],
        "order": ["They have visited Quito twice.", "Sara has visited three museums."],
        "write": [("Yo he probado comida japonesa.", "I have tried Japanese food."),
                  ("Él ha escalado dos montañas este año.", "He has climbed two mountains this year."),
                  ("Hemos cocinado para nuestros vecinos.", "We have cooked for our neighbors.")],
        "listen": [("Daniel has ridden a horse before.", ["Daniel have ridden a horse before.", "Daniel has ride a horse before."]),
                   ("I have cooked pasta for my family.", ["I has cooked pasta for my family.", "I have cook pasta for my family."])],
    },
    32: {
        "rule": "Ever pregunta si ocurrió alguna vez; never niega una experiencia sin usar not.",
        "vocab": [("ever", "alguna vez"), ("never", "nunca"), ("abroad", "en el extranjero"),
                  ("contest", "concurso"), ("met", "conocido"), ("unusual", "inusual")],
        "teaching": [
            ("Have you ever traveled abroad?", "¿Has viajado alguna vez al extranjero?"),
            ("I have never entered a singing contest.", "Nunca he participado en un concurso de canto."),
            ("Has Eva ever met a famous actor?", "¿Eva ha conocido alguna vez a un actor famoso?"),
            ("We have never eaten anything unusual there.", "Nunca hemos comido nada inusual allí."),
        ],
        "choice": [("Ana pregunta por una experiencia de toda la vida.", "Have you ever slept in a tent?",
                    ["Did you ever slept in a tent?", "Have you never sleep in a tent?"]),
                   ("Luis afirma que esa experiencia no ha ocurrido.", "Luis has never flown alone.",
                    ["Luis hasn't never flown alone.", "Luis has never fly alone."])],
        "complete": [("Completa la pregunta: Have they ___ won a contest?", "ever"),
                     ("Completa la experiencia negativa: I have ___ seen snow.", "never")],
        "order": ["Has Marta ever worked abroad?", "We have never met your cousin."],
        "write": [("¿Alguna vez has visitado una isla?", "Have you ever visited an island?"),
                  ("Nunca he participado en un concurso de cocina.", "I have never entered a cooking contest."),
                  ("¿Él ha probado alguna vez algo inusual?", "Has he ever tried anything unusual?")],
        "listen": [("I have never traveled abroad alone.", ["I haven't never traveled abroad alone.", "I never have travel abroad alone."]),
                   ("Have you ever met someone famous?", ["Did you ever met someone famous?", "Have you ever meet someone famous?"])],
    },
    33: {
        "rule": "Been indica visita con regreso; gone indica que la persona todavía está fuera.",
        "vocab": [("been", "estado y regresado"), ("gone", "ido y aún ausente"), ("returned", "regresado"),
                  ("away", "fuera"), ("trip", "viaje"), ("location", "ubicación")],
        "teaching": [
            ("Eva has been to Loja and returned home.", "Eva ha estado en Loja y regresó a casa."),
            ("Tom has gone to the bank, so he is away.", "Tom ha ido al banco, así que está fuera."),
            ("Have you ever been on a business trip?", "¿Has estado alguna vez en un viaje de negocios?"),
            ("Maya has gone to Cuenca, so her current location is there.", "Maya ha ido a Cuenca, así que esa es su ubicación actual."),
        ],
        "choice": [("Nora visitó Perú y ya volvió.", "Nora has been to Peru.",
                    ["Nora has gone to Peru and she is here.", "Nora have been to Peru."]),
                   ("Pablo no está en casa porque fue a la farmacia.", "Pablo has gone to the pharmacy.",
                    ["Pablo has been to the pharmacy and is still there.", "Pablo have gone to the pharmacy."])],
        "complete": [("Ya regresó. Completa: Mia has ___ to Canada twice.", "been"),
                     ("Sigue en la oficina. Completa: Leo has ___ to work.", "gone")],
        "order": ["My parents have been to Chile.", "The manager has gone to lunch."],
        "write": [("Sara ha estado en esa ciudad y regresó.", "Sara has been to that city."),
                  ("Elena ha ido al mercado y todavía está allí.", "Elena has gone to the market and is still there."),
                  ("Hemos estado en tres países durante este viaje.", "We have been to three countries during this trip.")],
        "listen": [("Ben has gone to the airport.", ["Ben has been to the airport and is there now.", "Ben have gone to the airport."]),
                   ("I have been to that location before.", ["I went to that location yesterday.", "I have gone there and I am still away."])],
    },
    34: {
        "rule": "Una pregunta de seguimiento pide un detalle concreto después de conocer la experiencia.",
        "vocab": [("when", "cuándo"), ("where", "dónde"), ("who", "quién"),
                  ("how long", "cuánto tiempo"), ("why", "por qué"), ("details", "detalles")],
        "teaching": [
            ("When did you go?", "¿Cuándo fuiste?"),
            ("Where did you stay?", "¿Dónde te alojaste?"),
            ("Who did you travel with?", "¿Con quién viajaste?"),
            ("When did you go, where did you stay, and how long were you there?", "¿Cuándo fuiste, dónde te alojaste y cuánto tiempo estuviste?"),
            ("Why did you choose it? Ask for details after the first answer.", "¿Por qué lo elegiste? Pide detalles después de la primera respuesta."),
        ],
        "choice": [("Alguien dice que visitó Londres; pregunta por el momento.", "When did you visit London?",
                    ["When have you visit London?", "Where did you visit London?"]),
                   ("Una amiga cuenta que viajó con alguien; pregunta por la persona.", "Who did you travel with?",
                    ["Who you traveled with?", "Why did you travel with?"])],
        "complete": [("Completa la pregunta sobre duración: ___ did you stay?", "How long"),
                     ("Completa la pregunta sobre motivo: ___ did she choose Rome?", "Why")],
        "order": ["Where did they stay in Lima?", "Where did she stay, when did she arrive, and how long was her visit?"],
        "write": [("¿Con quién fuiste al concierto?", "Who did you go to the concert with?"),
                  ("Pregunta cuándo fue, dónde se alojó y cuánto tiempo estuvo allí.",
                   "When did you go? Where did you stay? How long were you there?"),
                  ("¿Por qué elegiste ese lugar para tus vacaciones?", "Why did you choose that place for your vacation?")],
        "listen": [("Where did you learn to cook?", ["When did you learn to cook?", "Where have you learned that recipe?"]),
                   ("How long did the course last?", ["How long the course did last?", "How many did the course last?"])],
        "review_pairs": [("who", "quién"), ("travel companion", "acompañante de viaje")],
        "write_variant": "When did you travel? Where did you sleep? How long did the visit last?",
        "review_variant": "Why was that place your choice for the vacation?",
        "remediation": {1: (3, 1), 2: (5, 3), 3: (4, 2), 4: (4, 2)},
    },
    35: {
        "rule": "Una entrevista enlaza experiencia, respuesta y seguimiento sin revelar la respuesta antes.",
        "vocab": [("interview", "entrevista"), ("guest", "invitado"), ("answer", "respuesta"),
                  ("question", "pregunta"), ("notes", "notas"), ("experience", "experiencia")],
        "teaching": [
            ("The interview begins: Have you ever been to Peru?", "La entrevista empieza: ¿Has estado alguna vez en Perú?"),
            ("The guest answers: I have been there. My sister has gone there and is still away.", "El invitado responde: He estado allí. Mi hermana ha ido y todavía está fuera."),
            ("The follow-up question is: Who went with you, and how long did it take?", "La pregunta de seguimiento es: ¿Quién fue contigo y cuánto duró?"),
            ("Interview notes: Have you ever been to Loja? Yes. Who went with you? Ana. How long? Three days.", "Notas: ¿Has estado en Loja? Sí. ¿Con quién? Ana. ¿Cuánto tiempo? Tres días."),
        ],
        "choice": [("La invitada corrió una maratón; pregunta cuándo.", "When did you run it?",
                    ["Where did you run it?", "Who did you run with?"]),
                   ("El invitado nunca acampó; pregunta si alguna vez viajó solo.", "Have you ever traveled alone?",
                    ["Did you travel alone last year?", "Have you never traveled alone?"])],
        "complete": [("Completa el inicio de la entrevista: ___ you ever won a prize?", "Have"),
                     ("El invitado regresó. Completa: He has ___ to Japan twice.", "been")],
        "order": ["What experience are you most proud of?", "My guest has been to Japan, but her sister has gone there."],
        "write": [("Pregunta si alguna vez conoció a un músico y luego pregunta dónde.",
                   "Have you ever met a musician? Where did you meet them?"),
                  ("Datos: Loja, Ana, 3 días. Pregunta, respuesta, seguimiento y notas.",
                   "Have you ever been to Loja? Yes, I have. Who did you go with, and how long did you stay? With Ana, for three days. Notes: Loja, Ana, three days."),
                  ("Datos: Quito, Leo, 2 días. Escribe otra mini entrevista con notas.",
                   "Have you ever been to Quito? Yes, I have. Who did you go with? I went with Leo. How long did you stay? Two days. Notes: Quito, Leo, two days.")],
        "listen": [("Have you ever performed on stage?", ["Did you ever performed on stage?", "Have you ever perform on stage?"]),
                   ("Who did you share that experience with?", ["Who you shared that experience with?", "Who have you share that experience with?"])],
        "review_pairs": [("Who did you go with?", "¿Con quién fuiste?"), ("How long did you stay?", "¿Cuánto tiempo estuviste?")],
        "write_variant": "Have you ever visited Loja? Yes. Who was with you, and how long was the visit? I went with Ana for three days. Notes: Loja, Ana, three days.",
        "review_variant": "Have you ever visited Quito? Yes. Who was with you? Leo. How long was the visit? Two days. Notes: Quito, Leo, two days.",
        "remediation": {1: (1, 3), 2: (2, 2), 3: (4, 3), 4: (3, 1)},
    },
    36: {
        "rule": "Past simple acompaña un tiempo terminado; present perfect conecta el hecho con ahora.",
        "vocab": [("finished", "terminado"), ("date", "fecha"), ("yesterday", "ayer"),
                  ("recently", "recientemente"), ("specific", "específico"), ("still", "todavía")],
        "teaching": [
            ("I finished the report yesterday.", "Terminé el informe ayer."),
            ("She has recently changed jobs.", "Ella ha cambiado de trabajo recientemente."),
            ("A specific date requires the past simple.", "Una fecha específica requiere pasado simple."),
            ("We have not received the package; it is still missing.", "No hemos recibido el paquete; todavía falta."),
        ],
        "choice": [("La acción ocurrió ayer.", "I called Marta yesterday.",
                    ["I have called Marta yesterday.", "I has called Marta yesterday."]),
                   ("La noticia reciente importa ahora y no incluye fecha terminada.", "They have recently moved house.",
                    ["They recently move house.", "They has recently moved house."])],
        "complete": [("Completa con fecha terminada: We ___ the museum in 2024.", "visited"),
                     ("Sigue sin encontrarlas. Completa: Leo ___ his keys.", "has lost")],
        "order": ["Maya started the course last Monday.", "Our team has won three games this season."],
        "write": [("Compré este teléfono el mes pasado.", "I bought this phone last month."),
                  ("Ella ha encontrado recientemente un nuevo apartamento.", "She has recently found a new apartment."),
                  ("No hemos terminado el proyecto todavía.", "We have not finished the project yet.")],
        "listen": [("I saw that film on Friday.", ["I have seen that film on Friday.", "I seen that film on Friday."]),
                   ("The bus has just arrived.", ["The bus just arrive.", "The bus have just arrived."])],
    },
    37: {
        "rule": "Already indica logro temprano, yet pregunta o niega hasta ahora y just señala algo reciente.",
        "vocab": [("already", "ya"), ("yet", "todavía o ya"), ("just", "acabar de"),
                  ("completed", "completado"), ("recently", "recientemente"), ("waiting", "esperando")],
        "teaching": [
            ("I have already completed the form.", "Ya he completado el formulario."),
            ("Have you called the clinic yet?", "¿Ya llamaste a la clínica?"),
            ("The train has just left.", "El tren acaba de salir."),
            ("We are still waiting because the doctor has not arrived yet.", "Seguimos esperando porque el doctor todavía no ha llegado."),
            ("She has recently started a new course.", "Ella ha empezado un curso recientemente."),
        ],
        "choice": [("El correo salió hace un momento.", "I have just sent the email.",
                    ["I have yet sent the email.", "I just have send the email."]),
                   ("La tarea se completó antes de lo esperado.", "Nora has already finished the task.",
                    ["Nora has yet finished the task.", "Nora have already finish the task."])],
        "complete": [("Completa la pregunta: Has the taxi arrived ___?", "yet"),
                     ("Completa la noticia inmediata: We have ___ heard the result.", "just")],
        "order": ["They have already booked the tickets.", "I have not read the message yet."],
        "write": [("Elena acaba de llegar a la oficina.", "Elena has just arrived at the office."),
                  ("Ya hemos completado las dos primeras tareas.", "We have already completed the first two tasks."),
                  ("¿El gerente ha respondido todavía?", "Has the manager replied yet?")],
        "listen": [("The children have just fallen asleep.", ["The children have yet fallen asleep.", "The children has just fall asleep."]),
                   ("Have you packed your suitcase yet?", ["Have you already packed yet your suitcase?", "Did you packed your suitcase yet?"])],
    },
    38: {
        "rule": "For introduce una duración; since introduce el punto en que comenzó una situación.",
        "vocab": [("for", "durante"), ("since", "desde"), ("duration", "duración"),
                  ("starting point", "punto de inicio"), ("lived", "vivido"), ("worked", "trabajado")],
        "teaching": [
            ("I have lived here for five years.", "He vivido aquí durante cinco años."),
            ("She has worked at the clinic since June.", "Ella ha trabajado en la clínica desde junio."),
            ("For answers a duration question.", "For responde una pregunta de duración."),
            ("Since introduces a starting point such as Monday.", "Since introduce un punto de inicio como el lunes."),
        ],
        "choice": [("La frase expresa una duración de tres meses.", "We have studied together for three months.",
                    ["We have studied together since three months.", "We studied together for Monday."]),
                   ("La situación comenzó en 2022 y continúa.", "Ana has worked here since 2022.",
                    ["Ana has worked here for 2022.", "Ana worked here since three years."])],
        "complete": [("Completa con duración: I have known Sam ___ ten years.", "for"),
                     ("Completa con inicio: They have lived there ___ April.", "since")],
        "order": ["He has waited for forty minutes.", "Maya has studied French since January."],
        "write": [("Hemos vivido aquí durante seis meses.", "We have lived here for six months."),
                  ("Ella ha trabajado desde el lunes por la mañana.", "She has worked since Monday morning."),
                  ("Conozco a Julia desde la escuela primaria.", "I have known Julia since primary school.")],
        "listen": [("The shop has been open for two hours.", ["The shop has been open since two hours.", "The shop have been open for two hours."]),
                   ("I have used this laptop since May.", ["I have used this laptop for May.", "I has used this laptop since May."])],
    },
    39: {
        "rule": "Una noticia reciente usa present perfect; los detalles terminados pasan a past simple.",
        "vocab": [("news", "noticia"), ("happened", "ocurrió"), ("details", "detalles"),
                  ("just", "acabar de"), ("when", "cuándo"), ("where", "dónde")],
        "teaching": [
            ("I have some news: Marta has just won a prize.", "Tengo una noticia: Marta acaba de ganar un premio."),
            ("What happened after the ceremony?", "¿Qué ocurrió después de la ceremonia?"),
            ("Ask when the event took place.", "Pregunta cuándo ocurrió el evento."),
            ("Add details about where the event happened.", "Añade detalles sobre dónde ocurrió el evento."),
        ],
        "choice": [("Abre una noticia reciente sin fecha terminada.", "Our neighbors have just had a baby.",
                    ["Our neighbors just has a baby.", "Our neighbors have had a baby yesterday."]),
                   ("Después de la noticia, pregunta por el momento terminado.", "When did the accident happen?",
                    ["When has the accident happened?", "When did the accident happened?"])],
        "complete": [("Completa la noticia: The city ___ a new bridge.", "has opened"),
                     ("Completa el detalle: Where ___ they hold the ceremony?", "did")],
        "order": ["The school has just announced the results.", "Who gave you the good news?"],
        "write": [("Tengo noticias: Paula acaba de conseguir trabajo.", "I have news: Paula has just found a job."),
                  ("El equipo ha ganado; pregunta cuándo y dónde jugó.",
                   "The team has won. When did it play, and where was the match?"),
                  ("La tienda ha cerrado; pregunta qué ocurrió esta mañana.",
                   "The shop has closed. What happened there this morning?")],
        "listen": [("Leo has broken his arm.", ["Leo has broke his arm.", "Leo broke his arm tomorrow."]),
                   ("Where did the firefighters find the dog?", ["Where have the firefighters found the dog yesterday?", "Where did the firefighters found the dog?"])],
        "review_pairs": [("ceremony", "ceremonia"), ("result", "resultado")],
        "write_variant": "The team has won. When was the game, and where did they play?",
        "review_variant": "The shop has closed. What took place there earlier this morning?",
    },
    40: {
        "rule": "Una actualización personal resume cambios recientes y añade tiempos o detalles verificables.",
        "vocab": [("update", "actualización"), ("lately", "últimamente"), ("since", "desde"),
                  ("already", "ya"), ("challenge", "desafío"), ("progress", "progreso")],
        "teaching": [
            ("Here is a short update about my new job.", "Aquí tienes una actualización breve sobre mi nuevo trabajo."),
            ("I have felt more confident lately.", "Me he sentido más seguro últimamente."),
            ("I have worked there since May and have already made progress.", "Trabajo allí desde mayo y ya he progresado."),
            ("My first challenge happened during the opening week.", "Mi primer desafío ocurrió durante la semana inicial."),
        ],
        "choice": [("Resume un cambio reciente que sigue siendo relevante.", "I have started a new evening course.",
                    ["I have started a new evening course last Tuesday.", "I has started a new evening course."]),
                   ("La segunda unidad ya está terminada y el resultado importa ahora.", "I have already finished unit two.",
                    ["I already finish unit two.", "I have yet finished unit two."])],
        "complete": [("Completa la duración: I have made progress ___ two months.", "for"),
                     ("Completa el inicio: I have lived here ___ September.", "since")],
        "order": ["I have made good progress lately.", "My main challenge began last month."],
        "write": [("Actualiza: empezaste un curso y ya terminaste dos unidades.",
                   "I have started a course and I have already finished two units."),
                  ("Cuenta desde cuándo vives allí, un logro reciente y un desafío de ayer.",
                   "I have lived here since March. I have recently made new friends, but my first challenge happened yesterday when I missed the bus."),
                  ("Has progresado últimamente y aprobaste una prueba el lunes.",
                   "I have made progress lately, and I passed an important test on Monday.")],
        "listen": [("I have not completed the final task yet.", ["I did not completed the final task yet.", "I have not complete the final task yet."]),
                   ("I joined the gym in June and have trained there since then.", ["I have joined the gym in June and trained tomorrow.", "I joined the gym since June and have train there."])],
        "write_variant": "I have been here since March and have made friends lately, but yesterday I faced a challenge after missing the bus.",
        "review_variant": "Lately, I have made good progress, and on Monday I passed an important test.",
    },
    41: {
        "rule": "Los adjetivos cortos forman el comparativo con -er y usan than para el segundo elemento.",
        "vocab": [("taller", "más alto"), ("shorter", "más corto"), ("faster", "más rápido"),
                  ("cheaper", "más barato"), ("quieter", "más silencioso"), ("heavier", "más pesado")],
        "teaching": [
            ("This building is taller than the library.", "Este edificio es más alto que la biblioteca."),
            ("The blue route is shorter and faster.", "La ruta azul es más corta y rápida."),
            ("That café is cheaper than this one.", "Ese café es más barato que este."),
            ("My street is quieter, but this suitcase is heavier.", "Mi calle es más silenciosa, pero esta maleta es más pesada."),
        ],
        "choice": [("Compara la altura de dos edificios.", "Tower A is taller than Tower B.",
                    ["Tower A is more tall than Tower B.", "Tower A is tallier that Tower B."]),
                   ("Compara el precio de dos billetes.", "The bus ticket is cheaper than the train ticket.",
                    ["The bus ticket is more cheap than the train ticket.", "The bus ticket is cheapest that the train ticket."])],
        "complete": [("Completa la velocidad: A train is ___ than a bicycle.", "faster"),
                     ("Completa el peso: This box is ___ than that bag.", "heavier")],
        "order": ["My new walk to work is shorter.", "The back room is quieter than the hall."],
        "write": [("Mi hermano es más alto que yo.", "My brother is taller than me."),
                  ("Esta ruta es más rápida y corta que la anterior.", "This route is faster and shorter than the old one."),
                  ("El mercado es más barato que el supermercado.", "The market is cheaper than the supermarket.")],
        "listen": [("Today is colder than yesterday.", ["Today is more cold than yesterday.", "Today is colder that yesterday."]),
                   ("The red suitcase is heavier than mine.", ["The red suitcase is heavyer than mine.", "The red suitcase is more heavier than mine."])],
    },
    42: {
        "rule": "Los adjetivos largos forman el comparativo con more y conservan el adjetivo sin cambios.",
        "vocab": [("comfortable", "cómodo"), ("interesting", "interesante"),
                  ("expensive", "caro"), ("reliable", "fiable"),
                  ("convenient", "conveniente"), ("crowded", "concurrido")],
        "teaching": [
            ("The armchair is more comfortable than the stool.", "El sillón es más cómodo que el taburete."),
            ("The history tour is more interesting than the bus ride.", "El recorrido histórico es más interesante que el viaje en bus."),
            ("This model is more expensive but more reliable.", "Este modelo es más caro pero más fiable."),
            ("The morning train is more convenient but more crowded.", "El tren matutino es más conveniente pero más concurrido."),
        ],
        "choice": [("Compara la comodidad de dos habitaciones.", "Room A is more comfortable than Room B.",
                    ["Room A is comfortabler than Room B.", "Room A is more comfortable that Room B."]),
                   ("Compara la fiabilidad de dos servicios.", "The local service is more reliable than the app.",
                    ["The local service is reliabler than the app.", "The local service is more reliable that the app."])],
        "complete": [("Completa el interés: The book is ___ than the film.", "more interesting"),
                     ("Completa el costo: This hotel is ___ than the hostel.", "more expensive")],
        "order": ["Online booking is more convenient for us.", "The evening market is more crowded than this one."],
        "write": [("Este sofá es más cómodo que esa silla.", "This sofa is more comfortable than that chair."),
                  ("La segunda propuesta es más interesante y fiable.", "The second proposal is more interesting and more reliable."),
                  ("El vuelo directo es más conveniente pero más caro.", "The direct flight is more convenient but more expensive.")],
        "listen": [("The science museum is more interesting than the gallery.", ["The science museum is interestinger than the gallery.", "The science museum is more interesting that the gallery."]),
                   ("This neighborhood is more crowded than ours.", ["This neighborhood is crowdeder than ours.", "This neighborhood is more crowded that ours."])],
    },
    43: {
        "rule": "Good, bad y far usan formas irregulares: better, worse y farther.",
        "vocab": [("better", "mejor"), ("worse", "peor"), ("farther", "más lejos"),
                  ("less", "menos"), ("more", "más"), ("comparison", "comparación")],
        "teaching": [
            ("This plan is better than the first one.", "Este plan es mejor que el primero."),
            ("Traffic is worse on Friday evening.", "El tráfico es peor el viernes por la tarde."),
            ("The north beach is farther from town.", "La playa norte está más lejos del pueblo."),
            ("This comparison shows more space and less noise.", "Esta comparación muestra más espacio y menos ruido."),
        ],
        "choice": [("Compara dos resultados con good.", "Today's result is better than yesterday's.",
                    ["Today's result is gooder than yesterday's.", "Today's result is more good than yesterday's."]),
                   ("Compara dos condiciones con bad.", "The weather is worse in the mountains.",
                    ["The weather is badder in the mountains.", "The weather is more bad in the mountains."])],
        "complete": [("Completa la distancia: The airport is ___ than the station.", "farther"),
                     ("Completa la cantidad: This room has ___ light than the kitchen.", "less")],
        "order": ["Your second idea is better than mine.", "The traffic became worse after six."],
        "write": [("Este restaurante es mejor que el anterior.", "This restaurant is better than the previous one."),
                  ("La conexión es peor, pero tenemos más espacio.", "The connection is worse, but we have more space."),
                  ("La otra parada está más lejos y tiene menos tráfico.", "The other stop is farther away and has less traffic.")],
        "listen": [("The blue screen looks better than the gray one.", ["The blue screen looks gooder than the gray one.", "The blue screen looks more good than the gray one."]),
                   ("This headache feels worse than this morning.", ["This headache feels badder than this morning.", "This headache feels more bad than this morning."])],
    },
    44: {
        "rule": "Una comparación útil presenta criterios, ventajas y desventajas antes de expresar preferencia.",
        "vocab": [("option", "opción"), ("advantage", "ventaja"), ("disadvantage", "desventaja"),
                  ("while", "mientras que"), ("both", "ambos"), ("prefer", "preferir")],
        "teaching": [
            ("The first option is cheaper.", "La primera opción es más barata."),
            ("Its main advantage is the central location.", "Su principal ventaja es la ubicación céntrica."),
            ("The disadvantage is that the room is smaller.", "La desventaja es que la habitación es más pequeña."),
            ("Both are comfortable, while I prefer the quieter hotel.", "Ambos son cómodos, mientras que prefiero el hotel más silencioso."),
        ],
        "choice": [("Contrasta precio y comodidad de dos hoteles.", "Hotel A is cheaper, while Hotel B is more comfortable.",
                    ["Hotel A is cheapest, while Hotel B more comfortable.", "Hotel A cheaper that Hotel B is comfortable."]),
                   ("Expresa una preferencia después de comparar velocidad y costo.", "Both are fast, but I prefer the cheaper train.",
                    ["Both is fast, but I prefer the cheapest than train.", "Both are faster, but I prefer cheap train than."])],
        "complete": [("Completa el contraste: This phone is lighter, ___ that one is faster.", "while"),
                     ("Completa la valoración: The main ___ is the high price.", "disadvantage")],
        "order": ["The first apartment has a better location.", "Both routes are safe, but this one is shorter."],
        "write": [("La opción A es más barata, pero la B es más fiable.",
                   "Option A is cheaper, but option B is more reliable."),
                  ("Buscas aula. A: online, $40, 6 semanas; B: aula, $80, 10. Compara.",
                   "Course A is cheaper and shorter, but I prefer course B because I want classroom learning."),
                  ("La ventaja del bus es el precio; la desventaja es la duración.",
                   "The advantage of the bus is its price, while the disadvantage is the duration.")],
        "listen": [("This laptop is lighter, but the other one is faster.", ["This laptop is faster, but the other one is lighter.", "Both laptops are equally light and fast."]),
                   ("I prefer the blue chair because it is more comfortable.", ["I prefer the blue chair because it is comfortabler.", "I prefer blue chair because more comfortable than."])],
        "write_variant": "Course A costs less and takes fewer weeks; however, course B is my choice because I need classroom lessons.",
        "review_variant": "The price is the bus's advantage, whereas the longer duration is its disadvantage.",
    },
    45: {
        "rule": "Una recomendación conecta necesidades y criterios con una opción mediante because.",
        "vocab": [("recommend", "recomendar"), ("suitable", "adecuado"), ("budget", "presupuesto"),
                  ("needs", "necesidades"), ("because", "porque"), ("overall", "en general")],
        "teaching": [
            ("I recommend the quieter room because it is more suitable.", "Recomiendo la habitación más silenciosa porque es más adecuada."),
            ("This course is better and more suitable because it has clear lessons.", "Este curso es mejor y más adecuado porque tiene lecciones claras."),
            ("Compare each hotel with the traveler's needs and budget.", "Compara cada hotel con las necesidades y el presupuesto del viajero."),
            ("Choose the train because it is better overall.", "Elige el tren porque es mejor en general."),
        ],
        "choice": [("La persona necesita ahorrar; recomienda la alternativa económica.", "I recommend the bus because it is cheaper.",
                    ["I recommend the bus because it is more cheap.", "I recommend bus because cheaper than."]),
                   ("La persona prioriza comodidad; recomienda la opción adecuada.", "The larger room is more suitable because it is quieter.",
                    ["The smaller room is more suitable because it is noisier.", "Both rooms are equally quiet and suitable."])],
        "complete": [("Completa la razón: Choose this plan ___ it is more reliable.", "because"),
                     ("Completa la comparación: This route is ___ than the other one.", "better")],
        "order": ["This option is more suitable for your needs.", "The train is better overall and fits our budget."],
        "write": [("Recomienda el tren porque es más rápido y fiable.",
                   "I recommend the train because it is faster and more reliable."),
                  ("Necesita 3 cuartos y ahorrar. A: $600, lejos, 3. B: $750, cerca, 2.",
                   "Home A is cheaper than home B and more suitable for this family. Overall, it is the better option because it has three bedrooms and fits their budget."),
                  ("En general, elige el hotel tranquilo porque ofrece mejor descanso.",
                   "Overall, choose the quieter hotel because it offers better rest for everyone.")],
        "listen": [("The local shop is better for a small budget.", ["The local shop is farther from a small market.", "The large store is better for an unlimited budget."]),
                   ("I recommend this route because it is shorter and safer.", ["I recommend the other route because it is longer.", "I avoid this route because it is less safe."])],
        "review_pairs": [("quieter room", "habitación más silenciosa"), ("more suitable", "más adecuada")],
        "write_variant": "I recommend home A: it is the better and more suitable choice because it costs less than home B and provides the three bedrooms they need.",
        "review_variant": "In general, I recommend the quieter hotel because everyone can rest better there.",
    },
}


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def arrange(correct: str, wrong: list[str], index: int) -> list[str]:
    values = list(wrong)
    values.insert(index, correct)
    return values


def feedback(rule: str, label: str, evidence: str) -> str:
    return f"{rule} En {label}, la evidencia correcta es «{evidence}»."


def build(number: int) -> dict:
    spec = SPECS[number]
    concept = CONCEPTS[number]
    prefix = f"en.n2.c{number:02d}"
    title_es = TITLES[number][1].lower()
    choice_a, choice_b = spec["choice"]
    complete_a, complete_b = spec["complete"]
    order_a, order_b = spec["order"]
    write_a, write_b, write_c = spec["write"]
    listen_a, listen_b = spec["listen"]
    vocab = spec["vocab"]
    review_pairs = spec.get("review_pairs", [vocab[4], vocab[5]])
    rule = spec["rule"]

    pools = {
        "practiceGuided": [
            base.choice(f"{prefix}.pg01", f"{choice_a[0]} Elige la forma correcta.",
                        arrange(choice_a[1], choice_a[2], 0), 0, concept, "practiceGuided",
                        feedback(rule, "la selección guiada", choice_a[1]),
                        hint=f"Aplica esta regla: {rule}"),
            base.complete(f"{prefix}.pg02", complete_a[0], complete_a[1], concept, "practiceGuided",
                          feedback(rule, "el primer espacio", complete_a[1]),
                          hint=f"Busca la forma que cumple esta regla: {rule}"),
            base.order(f"{prefix}.pg03", f"Ordena un ejemplo de {title_es}.", order_a,
                       concept, "practiceGuided", feedback(rule, "el primer orden", order_a),
                       hint="Localiza primero el sujeto y la forma verbal principal."),
        ],
        "practice": [
            base.write(f"{prefix}.p01", f"Escribe en inglés: {write_a[0]}", write_a[0], write_a[1],
                       concept, "practice", feedback(rule, "la primera producción", write_a[1])),
            base.listen(f"{prefix}.p02", f"Escucha y reconoce un ejemplo de {title_es}.", listen_a[0],
                        arrange(listen_a[0], listen_a[1], 1), 1, concept, "practice",
                        feedback(rule, "el primer audio", listen_a[0])),
            base.match(f"{prefix}.p03", f"Relaciona vocabulario inicial de {title_es}.",
                       [vocab[0], vocab[1]], concept, "practice",
                       feedback(rule, "el primer grupo léxico", f"{vocab[0][0]} / {vocab[1][0]}")),
        ],
        "evaluation": [
            base.choice(f"{prefix}.e01", f"{choice_b[0]} Elige la forma correcta.",
                        arrange(choice_b[1], choice_b[2], 2), 2, concept, "evaluation",
                        feedback(rule, "la primera evaluación", choice_b[1])),
            base.complete(f"{prefix}.e02", complete_b[0], complete_b[1], concept, "evaluation",
                          feedback(rule, "el segundo espacio", complete_b[1])),
            base.write(f"{prefix}.e03", f"Escribe en inglés: {write_b[0]}", write_b[0], write_b[1],
                       concept, "evaluation", feedback(rule, "la producción evaluada", write_b[1])),
            base.listen(f"{prefix}.e04", f"Escucha y verifica otro ejemplo de {title_es}.", listen_b[0],
                        arrange(listen_b[0], listen_b[1], 1), 1, concept, "evaluation",
                        feedback(rule, "el audio evaluado", listen_b[0])),
        ],
        "review": [
            base.match(f"{prefix}.r01", f"Relaciona vocabulario de repaso de {title_es}.",
                       review_pairs, concept, "review",
                       feedback(rule, "el segundo grupo léxico", f"{review_pairs[0][0]} / {review_pairs[1][0]}")),
            base.order(f"{prefix}.r02", f"Ordena una oración de repaso sobre {title_es}.", order_b,
                       concept, "review", feedback(rule, "el orden de repaso", order_b)),
            base.write(f"{prefix}.r03", f"Escribe en inglés: {write_c[0]}", write_c[0], write_c[1],
                       concept, "review", feedback(rule, "la producción de repaso", write_c[1])),
        ],
    }

    if "write_variant" in spec:
        pools["evaluation"][2]["answer"]["accepted"] = [write_b[1], spec["write_variant"]]
        base.add_hash(pools["evaluation"][2])
    if "review_variant" in spec:
        pools["review"][2]["answer"]["accepted"] = [write_c[1], spec["review_variant"]]
        base.add_hash(pools["review"][2])

    block_start = number - ((number - 31) % 5)
    cumulative = [CONCEPTS[i] for i in range(block_start, number + 1)] if number % 5 == 0 else None
    if cumulative:
        pools["evaluation"][0]["requires"] = cumulative[:2]
        pools["evaluation"][1]["requires"] = [cumulative[2]]
        pools["evaluation"][2]["requires"] = cumulative
        pools["evaluation"][3]["requires"] = [cumulative[-1]]
        for item in pools["evaluation"]:
            item["contentHash"] = base.add_hash(item)["contentHash"]

    objectives = [
        f"Reconocer {title_es} en mensajes breves de nivel A2.",
        f"Aplicar la regla de {title_es} en contextos nuevos y sin pistas.",
        f"Producir una respuesta propia que demuestre {title_es}.",
    ]
    lessons = [(en, es, f"{rule} Este ejemplo muestra el patrón en un contexto completo.")
               for en, es in spec["teaching"]]
    result = base.common_class(number, objectives, vocab, lessons, pools, cumulative=cumulative)
    if cumulative:
        result["usesPatterns"] = cumulative
    if "remediation" in spec:
        result["remediationMap"] = {
            f"{prefix}.e{evaluation:02d}": {
                "reteach": f"en.n2.class-{number:02d}.t{teaching:02d}",
                "review": f"{prefix}.r{review:02d}",
            }
            for evaluation, (teaching, review) in spec["remediation"].items()
        }
    return result


def audit(classes: list[dict], start: int, end: int) -> dict:
    assert [int(c["id"].rsplit("-", 1)[1]) for c in classes] == list(range(start, end + 1))
    prompts: dict[str, str] = {}
    feedbacks: dict[str, str] = {}
    semantics: dict[str, str] = {}
    indices = Counter()
    formats = Counter()
    for cls in classes:
        number = int(cls["id"].rsplit("-", 1)[1])
        assert cls["phase"] == PHASES[number]
        assert sum(len(items) for items in cls["pools"].values()) == 13
        for pool, items in cls["pools"].items():
            for item in items:
                prompt = item["prompt"]["es"]
                assert len(prompt) <= 90, (item["id"], len(prompt), prompt)
                normalized_prompt = re.sub(r"\W+", " ", prompt.casefold()).strip()
                normalized_feedback = re.sub(r"\W+", " ", item["origin"]["feedback"]["es"].casefold()).strip()
                assert normalized_prompt not in prompts, (item["id"], prompts.get(normalized_prompt))
                assert normalized_feedback not in feedbacks, (item["id"], feedbacks.get(normalized_feedback))
                prompts[normalized_prompt] = item["id"]
                feedbacks[normalized_feedback] = item["id"]
                signature = canonical({"prompt": item["prompt"], "answer": item["answer"],
                                       "stimulus": item["origin"].get("audio") or item["origin"].get("text") or item["origin"].get("pairs")})
                assert signature not in semantics, (item["id"], semantics.get(signature))
                semantics[signature] = item["id"]
                formats[item["format"]] += 1
                if item["format"] in {"elegir", "escuchar"}:
                    assert len(item["choices"]) == 3
                    indices[item["answer"]["index"]] += 1
        assert len({item["format"] for values in cls["pools"].values() for item in values}) >= 4
        if cls["phase"] in {"production", "transfer"}:
            writings = [item for pool in ("evaluation", "review") for item in cls["pools"][pool]
                        if item["format"] == "escribir"]
            assert any(len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", item["answer"]["text"])) >= 8
                       for item in writings), cls["id"]
    return {"classes": len(classes), "items": len(classes) * 13,
            "formats": dict(sorted(formats.items())),
            "correctIndices": dict(sorted(indices.items())),
            "uniquePrompts": len(prompts), "uniqueFeedback": len(feedbacks)}


def write_class(number: int) -> Path:
    # common_class usa estos mapas del módulo base; se amplían sin tocar lotes anteriores.
    base.CONCEPTS.update(CONCEPTS)
    base.PHASES.update(PHASES)
    base.TITLES.update(TITLES)
    document = build(number)
    audit([document], number, number)
    path = OUT / f"class-{number:02d}.json"
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def bundle_document(start: int, end: int) -> dict:
    classes = [json.loads((OUT / f"class-{number:02d}.json").read_text(encoding="utf-8"))
               for number in range(start, end + 1)]
    audit(classes, start, end)
    return {
        "schema": "onelingo.editorial.class-bundle.v1",
        "course": "en",
        "level": 2,
        "scale": SCALE,
        "status": "shadow",
        "runtimeAi": False,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "range": {"start": start, "end": end},
        "classes": classes,
    }


def write_bundle(start: int, end: int) -> Path:
    document = bundle_document(start, end)
    path = OUT / f"bundle-{start:02d}-{end:02d}.json"
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--class-number", type=int, choices=range(31, 46))
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    base.CONCEPTS.update(CONCEPTS)
    base.PHASES.update(PHASES)
    base.TITLES.update(TITLES)
    if args.class_number is not None:
        print(write_class(args.class_number))
    elif args.all:
        for number in range(31, 46):
            print(write_class(number))
        for start in (31, 36, 41):
            path = write_bundle(start, start + 4)
            print(f"{path} sha256:{digest(path)}")
    elif args.audit:
        classes = [json.loads((OUT / f"class-{number:02d}.json").read_text(encoding="utf-8"))
                   for number in range(31, 46)]
        print(json.dumps(audit(classes, 31, 45), ensure_ascii=False, sort_keys=True))
    else:
        parser.error("choose --class-number, --all, or --audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
