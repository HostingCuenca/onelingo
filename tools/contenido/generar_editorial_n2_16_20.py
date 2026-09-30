#!/usr/bin/env python3
"""Regenera las clases editoriales de Inglés N2 C16-C20."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n2"
SCALE = "client-10-levels-v1"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def add_hash(item):
    payload = {key: value for key, value in item.items() if key not in {"id", "contentHash"}}
    item["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return item


def accessibility():
    return {"screenReader": True, "highContrast": True, "largeText": True}


def segments(en, es):
    en_words, es_words = en.split(), es.split()
    en_mid, es_mid = max(1, len(en_words) // 2), max(1, len(es_words) // 2)
    return [
        {"en": " ".join(en_words[:en_mid]), "es": " ".join(es_words[:es_mid])},
        {"en": " ".join(en_words[en_mid:]), "es": " ".join(es_words[es_mid:])},
    ]


def make_item(item_id, spec, class_concept, pool):
    fmt = spec["format"]
    requires = spec.get("requires", [class_concept])
    origin = {
        "kind": "editorial",
        "feedback": {"es": spec["feedback"]},
    }
    teaches = []
    if pool == "practiceGuided":
        teaches = [class_concept]
        requires = []
        origin["hint"] = {"es": spec["hint"]}

    item = {
        "id": item_id,
        "format": fmt,
        "prompt": {"es": spec["prompt"]},
        "answer": {},
        "choices": [],
        "teaches": teaches,
        "requires": requires,
        "origin": origin,
        "accessibility": accessibility(),
    }

    if fmt in {"elegir", "escuchar"}:
        item["choices"] = [{"text": value} for value in spec["choices"]]
        item["answer"] = {"index": spec["answerIndex"]}
        if fmt == "escuchar":
            origin.update({
                "audio": spec["audio"],
                "audioMode": "tts",
                "languageCode": "en",
                "speedOptions": [0.75, 1.0],
                "maxReplays": 3,
                "revealTranscriptAfterAttempt": True,
            })
    elif fmt in {"completar", "escribir"}:
        accepted = spec.get("accepted", [spec["answer"]])
        item["answer"] = {"text": spec["answer"], "accepted": accepted}
        if fmt == "escribir":
            origin["text"] = spec["stimulus"]
    elif fmt == "ordenar":
        sentence = spec["answer"]
        item["answer"] = {"text": sentence, "tokens": sentence.split()}
    elif fmt == "relacionar":
        pairs = [[left, {"es": right}] for left, right in spec["pairs"]]
        item["answer"] = {"pairs": pairs}
        origin["pairs"] = pairs
    else:
        raise ValueError(fmt)
    return add_hash(item)


def ch(prompt, choices, answer, feedback, hint="Compara el sujeto con la forma verbal del modelo.", requires=None):
    data = {"format": "elegir", "prompt": prompt, "choices": choices, "answerIndex": answer,
            "feedback": feedback, "hint": hint}
    if requires is not None:
        data["requires"] = requires
    return data


def co(prompt, answer, feedback, hint="Localiza el sujeto y completa solo el fragmento ausente.", accepted=None, requires=None):
    data = {"format": "completar", "prompt": prompt, "answer": answer,
            "feedback": feedback, "hint": hint}
    if accepted is not None:
        data["accepted"] = accepted
    if requires is not None:
        data["requires"] = requires
    return data


def order(prompt, answer, feedback, hint="Busca primero el sujeto y después la forma verbal.", requires=None):
    data = {"format": "ordenar", "prompt": prompt, "answer": answer,
            "feedback": feedback, "hint": hint}
    if requires is not None:
        data["requires"] = requires
    return data


def listen(prompt, audio, choices, answer, feedback, requires=None):
    data = {"format": "escuchar", "prompt": prompt, "audio": audio, "choices": choices,
            "answerIndex": answer, "feedback": feedback, "hint": "Escucha otra vez a velocidad lenta y atiende a la forma verbal."}
    if requires is not None:
        data["requires"] = requires
    return data


def match(prompt, pairs, feedback, requires=None):
    data = {"format": "relacionar", "prompt": prompt, "pairs": pairs,
            "feedback": feedback, "hint": "Relaciona cada palabra con el contexto de la historia."}
    if requires is not None:
        data["requires"] = requires
    return data


def write(prompt, stimulus, answer, feedback, accepted=None, requires=None):
    data = {"format": "escribir", "prompt": prompt, "stimulus": stimulus, "answer": answer,
            "feedback": feedback, "hint": "Identifica primero el sujeto y el tiempo de la situación."}
    if accepted is not None:
        data["accepted"] = accepted
    if requires is not None:
        data["requires"] = requires
    return data


SPECS = {
    16: {
        "title": ("Was, were and past descriptions", "Was, were y descripciones pasadas"),
        "concept": "n2-was-were-descriptions",
        "vocabulary": [("tired", "cansado"), ("quiet", "tranquilo"), ("crowded", "lleno de gente"),
                       ("empty", "vacío"), ("ready", "listo"), ("late", "tarde"),
                       ("station", "estación"), ("weather", "clima")],
        "teaching": [
            ("I was tired after the journey.", "Estaba cansado después del viaje.", "Was acompaña a I para describir un estado pasado."),
            ("The hotel room was quiet at night.", "La habitación del hotel estaba tranquila por la noche.", "Was acompaña a un sujeto singular."),
            ("Maya was at the station before nine.", "Maya estaba en la estación antes de las nueve.", "Was también expresa ubicación pasada."),
            ("The streets were empty after midnight.", "Las calles estaban vacías después de medianoche.", "Were acompaña a un sujeto plural."),
            ("We were ready for the early bus.", "Estábamos listos para el autobús temprano.", "Were acompaña a we, you y they."),
        ],
        "pools": {
            "practiceGuided": [
                ch("Después del almuerzo el café estaba lleno. Elige la descripción correcta.",
                   ["The café were crowded after lunch.", "The café was crowded after lunch.", "The café is crowded after lunch."], 1,
                   "The café es singular y la situación es pasada, por eso corresponde was."),
                co("Completa la descripción pasada: My suitcase ___ very heavy.", "was",
                   "My suitcase es singular; was marca su estado en el pasado."),
                order("Ordena una descripción plural del lugar en el pasado.", "The streets were quiet at midnight.",
                      "Were sigue al sujeto plural the streets."),
            ],
            "practice": [
                ch("Leo y Nina llegaron tarde ayer. Elige la frase que describe su estado.",
                   ["Leo and Nina was late yesterday.", "Leo and Nina are late yesterday.", "Leo and Nina were late yesterday."], 2,
                   "Dos personas forman un sujeto plural; were concuerda con Leo and Nina."),
                co("Completa con la forma pasada de be: The weather ___ cold and windy.", "was",
                   "Weather funciona como singular, así que requiere was."),
                listen("Escucha y elige exactamente la frase sobre la preparación antes del taxi.",
                       "I was ready before the taxi arrived.",
                       ["I were ready before the taxi arrived.", "I was ready before the taxi arrived.", "I am ready before the taxi arrived."], 1,
                       "El audio usa was con I y mantiene ambas acciones en el pasado."),
            ],
            "evaluation": [
                ch("Ayer no había visitantes. Elige la descripción correcta del museo.",
                   ["The museum was empty yesterday.", "The museum were empty yesterday.", "The museum is empty yesterday."], 0,
                   "Museum es singular y yesterday exige was."),
                co("Completa la descripción de dos habitaciones: Our rooms ___ clean but small.", "were",
                   "Rooms es plural; la forma pasada correcta es were."),
                order("Ordena la descripción de una sala vacía antes del amanecer.",
                      "The waiting room was empty before sunrise.",
                      "Waiting room es singular y usa was para describir su estado pasado."),
                listen("Escucha y selecciona la descripción correcta de los autobuses después del concierto.",
                       "The buses were crowded after the concert.",
                       ["The buses was crowded after the concert.", "The buses are crowded after the concert.", "The buses were crowded after the concert."], 2,
                       "Buses es plural y el relato está en pasado, por eso se oye were."),
            ],
            "review": [
                match("Relaciona dos adjetivos de descripción con su significado.", [("crowded", "lleno de gente"), ("empty", "vacío")],
                      "Crowded y empty expresan estados opuestos de un lugar."),
                co("Completa el repaso: The street ___ quiet after the storm.", "was",
                   "Street es singular; was describe su estado después de la tormenta."),
                write("Escribe en inglés cómo se sentía el grupo después del viaje.",
                      "El grupo estaba cansado después del largo viaje.", "We were tired after the long journey.",
                      "We requiere were para describir un estado pasado."),
            ],
        },
    },
    17: {
        "title": ("There was and there were", "There was y there were"),
        "concept": "n2-there-was-were",
        "vocabulary": [("entrance", "entrada"), ("queue", "fila"), ("notices", "avisos"),
                       ("lift", "ascensor"), ("fountain", "fuente"), ("bench", "banco"),
                       ("noise", "ruido"), ("lights", "luces")],
        "teaching": [
            ("There was a long queue at the entrance.", "Había una fila larga en la entrada.", "There was presenta una existencia singular en el pasado."),
            ("There were two notices beside the door.", "Había dos avisos junto a la puerta.", "There were presenta elementos plurales."),
            ("There was some noise outside.", "Había algo de ruido fuera.", "Noise es incontable y usa there was."),
            ("There wasn't a lift in the old building.", "No había ascensor en el edificio antiguo.", "There wasn't niega una existencia singular."),
            ("There weren't any lights in the hall.", "No había luces en el pasillo.", "There weren't niega una existencia plural."),
        ],
        "pools": {
            "practiceGuided": [
                ch("Una sola fila esperaba junto a la puerta. Elige la frase correcta.",
                   ["There were a long queue beside the door.", "There was a long queue beside the door.", "There is a long queue beside the door yesterday."], 1,
                   "A long queue es singular, de modo que la existencia pasada usa there was."),
                co("Completa la existencia plural: There ___ two notices near reception.", "were",
                   "Two notices es plural; corresponde were."),
                order("Ordena la frase sobre una fuente que existía en el parque.", "There was a fountain in the park.",
                      "There was introduce una fuente singular en el pasado."),
            ],
            "practice": [
                ch("En la sala había varios asientos libres. Elige la opción correcta.",
                   ["There was several empty seats in the room.", "There are several empty seats in the room yesterday.", "There were several empty seats in the room."], 2,
                   "Several seats es plural y requiere there were."),
                co("Completa con la forma singular: There ___ some noise behind the wall.", "was",
                   "Noise es incontable, por eso se construye con there was."),
                listen("Escucha y elige la frase exacta sobre el pasillo oscuro.",
                       "There weren't any lights in the corridor.",
                       ["There wasn't any lights in the corridor.", "There weren't any lights in the corridor.", "There weren't some lights in the corridor."], 1,
                       "Lights es plural y la negación correcta es there weren't any."),
            ],
            "evaluation": [
                ch("El vestíbulo tenía un solo mostrador de información. Elige la descripción correcta.",
                   ["There was an information desk in the lobby.", "There were an information desk in the lobby.", "There was information desks in the lobby."], 0,
                   "An information desk es singular; la forma correcta es there was."),
                co("Completa la existencia plural: There ___ three shelves behind the counter.", "were",
                   "Three shelves necesita there were."),
                order("Ordena la negación sobre los servicios cerca de la estación.",
                      "There wasn't a bench near the entrance.",
                      "A bench es singular y la ausencia pasada se expresa con there wasn't."),
                listen("Escucha y selecciona cuántos bancos había junto a la entrada.",
                       "There were two benches beside the entrance.",
                       ["There was two benches beside the entrance.", "There were a bench beside the entrance.", "There were two benches beside the entrance."], 2,
                       "Two benches es plural y se presenta con there were."),
            ],
            "review": [
                match("Relaciona dos elementos de un edificio con su significado.", [("entrance", "entrada"), ("notices", "avisos")],
                      "Entrance nombra el acceso y notices nombra varios avisos visibles."),
                co("Completa el repaso plural negativo: There ___ no buses after midnight.", "were",
                   "No buses sigue siendo plural, así que corresponde were."),
                write("Escribe en inglés qué había cerca del andén.",
                      "Cerca del andén había un café pequeño.", "There was a small café near the platform.",
                      "A small café es singular y se introduce con there was."),
            ],
        },
    },
    18: {
        "title": ("Past continuous foundations", "Bases del pasado continuo"),
        "concept": "n2-past-continuous-foundations",
        "vocabulary": [("raining", "lloviendo"), ("waiting", "esperando"), ("driving", "conduciendo"),
                       ("carrying", "llevando"), ("sleeping", "durmiendo"), ("studying", "estudiando"),
                       ("talking", "hablando"), ("cooking", "cocinando")],
        "teaching": [
            ("I was waiting for the bus at seven.", "Estaba esperando el autobús a las siete.", "Was más verbo en -ing describe una acción en progreso con I."),
            ("They were driving home at midnight.", "Estaban conduciendo a casa a medianoche.", "Were más verbo en -ing concuerda con they."),
            ("It was raining all morning.", "Estuvo lloviendo toda la mañana.", "Was raining presenta una acción meteorológica en desarrollo."),
            ("She wasn't sleeping at eleven.", "Ella no estaba durmiendo a las once.", "Wasn't niega una acción singular en progreso."),
            ("Were you studying after dinner?", "¿Estabas estudiando después de cenar?", "Were inicia la pregunta con you."),
        ],
        "pools": {
            "practiceGuided": [
                ch("A las seis Nora llevaba unas cajas. Elige la acción en progreso correcta.",
                   ["Nora carried some boxes at six.", "Nora was carrying some boxes at six.", "Nora was carry some boxes at six."], 1,
                   "At six enfoca una acción en desarrollo; con Nora se usa was carrying."),
                co("Completa la acción plural en progreso: The children ___ near the door.", "were talking",
                   "The children es plural; el pasado continuo requiere were talking."),
                order("Ordena lo que estaba haciendo la persona a las siete.", "I was cooking dinner at seven.",
                      "El orden del pasado continuo es sujeto, was y verbo en -ing."),
            ],
            "practice": [
                ch("A las ocho la conversación del equipo seguía en curso. Elige la frase adecuada.",
                   ["At eight, the team discussed the problem.", "At eight, the team was discussing the problem.", "At eight, the team were discuss the problem."], 1,
                   "El punto temporal muestra una acción en curso: was discussing."),
                co("Completa la acción en progreso: We ___ for the bus at nine.", "were waiting",
                   "We necesita were más waiting."),
                listen("Escucha y elige la negación exacta sobre Sam a medianoche.",
                       "Sam wasn't sleeping at midnight.",
                       ["Sam weren't sleeping at midnight.", "Sam wasn't sleep at midnight.", "Sam wasn't sleeping at midnight."], 2,
                       "Sam es singular y la acción negada conserva sleeping."),
            ],
            "evaluation": [
                ch("A las seis la lluvia seguía cayendo. Elige la descripción en progreso.",
                   ["At six, the rain was falling steadily.", "At six, the rain were falling steadily.", "At six, the rain was fall steadily."], 0,
                   "Rain es singular; la forma progresiva correcta es was falling."),
                co("Completa la acción de Mina a las diez: Mina ___ home at ten.", "was driving",
                   "Mina es singular; was driving describe la acción en desarrollo."),
                order("Ordena la pregunta sobre la actividad en la biblioteca.", "Were they studying in the library?",
                      "La pregunta plural empieza con were, seguida de they y studying."),
                listen("Escucha y selecciona qué hacían los pasajeros cerca de la puerta.",
                       "The passengers were standing near the gate.",
                       ["The passengers was standing near the gate.", "The passengers were stand near the gate.", "The passengers were standing near the gate."], 2,
                       "Passengers es plural y la acción en progreso usa were standing."),
            ],
            "review": [
                match("Relaciona dos acciones en progreso con su significado.", [("raining", "lloviendo"), ("studying", "estudiando")],
                      "Raining describe lluvia en curso y studying describe estudio en curso."),
                co("Completa el repaso: At noon, I ___ to my manager.", "was talking",
                   "I requiere was talking para una acción en progreso al mediodía."),
                write("Escribe en inglés qué estaba haciendo el perro.",
                      "El perro estaba durmiendo debajo de la mesa.", "The dog was sleeping under the table.",
                      "The dog es singular y usa was sleeping."),
            ],
        },
    },
    19: {
        "title": ("Interrupted actions", "Acciones interrumpidas"),
        "concept": "n2-interrupted-actions",
        "vocabulary": [("while", "mientras"), ("when", "cuando"), ("rang", "sonó"),
                       ("dropped", "dejó caer"), ("alarm", "alarma"), ("went out", "se apagaron"),
                       ("interrupted", "interrumpió"), ("suddenly", "de repente")],
        "teaching": [
            ("I was making dinner when the phone rang.", "Estaba preparando la cena cuando sonó el teléfono.", "La acción larga usa pasado continuo; el evento breve usa pasado simple."),
            ("While we were walking, it started to rain.", "Mientras caminábamos, empezó a llover.", "While introduce la acción que ya estaba en curso."),
            ("She dropped her keys while she was getting off the bus.", "Dejó caer las llaves mientras bajaba del autobús.", "Dropped marca el evento puntual dentro de la acción en progreso."),
            ("The lights went out while they were studying.", "Las luces se apagaron mientras estudiaban.", "Went out interrumpe la actividad expresada con were studying."),
            ("What were you doing when the alarm sounded?", "¿Qué estabas haciendo cuando sonó la alarma?", "La pregunta pide la acción en progreso al ocurrir otro evento."),
        ],
        "pools": {
            "practiceGuided": [
                ch("La comida estaba en curso cuando sonó el timbre. Elige la combinación correcta.",
                   ["We ate when the doorbell was ringing.", "We were eating when the doorbell rang.", "We was eating when the doorbell rang."], 1,
                   "Were eating expresa la acción larga y rang el evento breve."),
                co("Completa la acción en curso: While I ___ to work, I saw an accident.", "was walking",
                   "While introduce la acción larga, por eso se usa was walking."),
                order("Ordena la relación entre la alarma y el sueño de Maya.", "The alarm sounded while Maya was sleeping.",
                      "Sounded es el evento puntual; was sleeping es la acción en curso."),
            ],
            "practice": [
                ch("El partido estaba en curso cuando comenzó a llover. Elige la frase correcta.",
                   ["They played tennis when it was starting to rain.", "They were playing tennis when it started to rain.", "They were play tennis when it started to rain."], 1,
                   "Were playing presenta el fondo y started presenta la interrupción."),
                co("Completa el evento breve: I was reading when the lights ___.", "went out",
                   "Went out es el pasado simple del evento que interrumpió la lectura."),
                listen("Escucha y distingue la acción en curso del evento puntual.",
                       "While Sara was driving, her phone rang.",
                       ["While Sara drove, her phone was ringing.", "While Sara was driving, her phone rang.", "While Sara were driving, her phone rang."], 1,
                       "Was driving es el fondo durativo y rang es el evento breve."),
            ],
            "evaluation": [
                ch("El autobús llegó durante la espera. Elige el contraste temporal correcto.",
                   ["The bus arrived while we were waiting.", "The bus was arriving while we waited.", "The bus arrived while we were wait."], 0,
                   "Arrived es el evento puntual y were waiting la acción en curso."),
                co("Completa el evento breve: He ___ his cup while he was talking.", "dropped",
                   "Dropped expresa el evento breve dentro de was talking."),
                write("Escribe en inglés la acción en curso y la interrupción.",
                      "Cuando entró la profesora, los estudiantes se estaban riendo.",
                      "When the teacher entered, the students were laughing.",
                      "Entered es puntual; were laughing describe la acción ya en curso.",
                      accepted=["When the teacher entered, the students were laughing.",
                                "The students were laughing when the teacher entered."]),
                listen("Escucha y elige la frase con interrupción correctamente construida.",
                       "I was taking a shower when the alarm sounded.",
                       ["I took a shower when the alarm was sounding.", "I was take a shower when the alarm sounded.", "I was taking a shower when the alarm sounded."], 2,
                       "Was taking es la acción larga y sounded la interrupción."),
            ],
            "review": [
                match("Relaciona dos palabras que organizan una interrupción narrativa.", [("interrupted", "interrumpió"), ("suddenly", "de repente")],
                      "Interrupted nombra el corte y suddenly anuncia un evento inesperado."),
                co("Completa el fondo narrativo: While we ___ home, it began to snow.", "were walking",
                   "Were walking expresa la acción en curso antes de began."),
                order("Ordena la interrupción durante la escritura de Leo.", "The computer stopped while Leo was writing.",
                      "Stopped es el evento breve; was writing es la acción en curso."),
            ],
        },
    },
    20: {
        "title": ("A short personal story", "Una historia personal breve"),
        "concept": "n2-personal-story-integration",
        "vocabulary": [("campsite", "campamento"), ("tent", "tienda de campaña"), ("path", "sendero"),
                       ("flashlight", "linterna"), ("noticed", "notó"), ("missing", "perdido"),
                       ("returned", "regresó"), ("relieved", "aliviado")],
        "teaching": [
            ("Last Saturday, Mia and Ben were at a campsite.", "El sábado pasado, Mia y Ben estaban en un campamento.", "Were establece quiénes estaban en el lugar y cuándo."),
            ("There was a narrow path behind their tent.", "Había un sendero estrecho detrás de su tienda.", "There was presenta un elemento singular del escenario."),
            ("As the sun was setting, they were searching the campsite for a missing flashlight.", "Cuando se ponía el sol, buscaban una linterna perdida por el campamento.", "Were searching presenta la búsqueda en progreso mientras cae el sol."),
            ("While Ben was checking the path, Mia noticed the flashlight beside a tree.", "Mientras Ben revisaba el sendero, Mia notó la linterna junto a un árbol.", "Was checking crea el fondo y noticed resuelve la búsqueda con un hallazgo puntual."),
            ("They returned to the campsite and felt relieved.", "Regresaron al campamento y se sintieron aliviados.", "Returned y felt cierran de manera coherente la búsqueda."),
        ],
        "cumulative": ["n2-was-were-descriptions", "n2-there-was-were", "n2-past-continuous-foundations",
                       "n2-interrupted-actions", "n2-personal-story-integration"],
        "pools": {
            "practiceGuided": [
                ch("Amir estaba junto al lago, había una señal y miraba el mapa. Elige el relato correcto.",
                   ["At dusk, Amir were near the lake. There were a sign. He was check the map.",
                    "At dusk, Amir was near the lake. There was a sign. He was checking the map.",
                    "At dusk, Amir is near the lake. There was a sign. He checked the map now."], 1,
                   "El relato concuerda Amir con was, presenta a sign con there was y usa was checking para el fondo."),
                co("Completa el evento breve: While Eva was following the path, she ___ a blue scarf.", "found",
                   "Found es el evento puntual que ocurre durante was following."),
                order("Ordena el cierre de la búsqueda en el campamento.", "Finally, they returned to the campsite together.",
                      "Finally abre el cierre y returned mantiene el pasado simple."),
            ],
            "practice": [
                ch("Había niebla y los excursionistas esperaban ayuda. Elige el relato coherente.",
                   ["The hikers were tired. There was thick fog. They were waiting for help.",
                    "The hikers was tired. There were thick fog. They waited for help at that moment.",
                    "The hikers are tired yesterday. There was thick fog. They were wait for help."], 0,
                   "El sujeto plural usa were, fog usa there was y la actividad de fondo usa were waiting."),
                co("Completa la actividad en curso: They ___ dinner when they heard a noise.", "were cooking",
                   "Were cooking presenta la actividad que estaba en curso antes de heard."),
                listen("Escucha y elige la oración que distingue el descanso de la llegada del guía.",
                       "While the group was resting, a guide arrived.",
                       ["While the group rested, a guide was arriving.", "While the group were resting, a guide arrived.", "While the group was resting, a guide arrived."], 2,
                       "Was resting es el fondo y arrived es el evento puntual."),
            ],
            "evaluation": [
                ch("Lena y Tom terminaron una caminata larga. Elige su descripción pasada correcta.",
                   ["Lena and Tom was tired after the hike.", "Lena and Tom were tired after the hike.", "Lena and Tom are tired after the hike yesterday."], 1,
                   "Lena and Tom es plural y requiere were.", requires=["n2-was-were-descriptions"]),
                co("Completa el escenario plural: There ___ two flashlights inside the tent.", "were",
                   "Two flashlights se presenta con there were.", requires=["n2-there-was-were"]),
                order("Ordena la acción en curso y el evento que la interrumpió.", "While Ava was carrying the tent, she dropped a pole.",
                      "Was carrying forma el fondo; dropped marca el evento puntual.",
                      requires=["n2-past-continuous-foundations", "n2-interrupted-actions"]),
                write("Escribe en inglés el cierre del relato a partir de la situación.",
                      "Era tarde en el campamento y no había luces. Buscábamos la linterna cuando Mia la encontró junto al sendero.",
                      "It was late at the campsite, and there were no lights. We were looking for the flashlight when Mia found it beside the path.",
                      "El relato integra descripción, escenario, búsqueda en curso y hallazgo puntual.",
                      accepted=[
                          "It was late at the campsite, and there were no lights. We were looking for the flashlight when Mia found it beside the path.",
                          "It was late at the campsite, and there were no lights. We were searching for the flashlight when Mia found it next to the path.",
                      ],
                      requires=["n2-personal-story-integration"]),
            ],
            "review": [
                match("Relaciona dos lugares de la historia con su significado.", [("campsite", "campamento"), ("path", "sendero")],
                      "Campsite es el lugar de acampada y path es el sendero."),
                co("Completa la acción de fondo: The campers ___ to the tent when the rain started.", "were returning",
                   "Were returning presenta el regreso al campamento antes de started."),
                listen("Escucha y selecciona el cierre emocional después de la llegada del guía.",
                       "Finally, everyone felt relieved after the guide arrived.",
                       ["Finally, everyone feel relieved after the guide arrived.",
                        "Finally, everyone was feeling relieved before the guide arrived.",
                        "Finally, everyone felt relieved after the guide arrived."], 2,
                       "Finally señala el cierre y ambos verbos quedan en pasado simple."),
            ],
        },
    },
}


OBJECTIVES = {
    16: [
        "Describir estados, lugares y personas del pasado con was o were.",
        "Reconocer la concordancia singular y plural en lectura y escucha.",
        "Producir descripciones pasadas breves sin apoyo dinámico.",
    ],
    17: [
        "Indicar qué había o no había en un lugar del pasado.",
        "Distinguir there was de there were según el elemento presentado.",
        "Reconstruir escenarios pasados con referentes singulares, plurales e incontables.",
    ],
    18: [
        "Expresar acciones que estaban en progreso en un momento pasado.",
        "Formar afirmaciones, negaciones y preguntas con was o were más -ing.",
        "Identificar actividades de fondo mediante lectura y audio breve.",
    ],
    19: [
        "Contrastar una acción en progreso con un evento pasado puntual.",
        "Interpretar when y while en relatos de interrupciones cotidianas.",
        "Narrar una interrupción breve con pasado continuo y pasado simple.",
    ],
    20: [
        "Comprender una historia personal con escenario, fondo, evento y cierre.",
        "Integrar was/were, there was/were y acciones interrumpidas sin pistas.",
        "Producir y evaluar un relato A2 corto con secuencia temporal coherente.",
    ],
}


def build_class(number):
    spec = SPECS[number]
    class_id = f"en.n2.class-{number:02d}"
    concept = spec["concept"]
    teaching = []
    for index, (en, es, explanation) in enumerate(spec["teaching"], 1):
        teaching.append({
            "id": f"{class_id}.t{index:02d}",
            "en": en,
            "es": es,
            "explanationEs": explanation,
            "segments": segments(en, es),
            "audioText": en,
            "audioMode": "tts",
            "languageCode": "en",
            "patternId": concept,
        })

    pools = {}
    prefixes = {"practiceGuided": "pg", "practice": "p", "evaluation": "e", "review": "r"}
    for pool_name, item_specs in spec["pools"].items():
        pools[pool_name] = [
            make_item(f"en.n2.c{number:02d}.{prefixes[pool_name]}{index:02d}", item_spec, concept, pool_name)
            for index, item_spec in enumerate(item_specs, 1)
        ]

    result = {
        "schema": "onelingo.editorial.class.v1",
        "course": "en",
        "level": 2,
        "scale": SCALE,
        "status": "shadow",
        "runtimeAi": False,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": {
            "chronologyTokens": "enforce",
            "answerReuseAcrossEarlyReserved": "forbid",
            "answerEvidenceReuseAcrossPools": "forbid",
            "agentContract": "editorial-agent.v2",
            "minChoices": 3,
            "maxPromptCharacters": 90,
            "feedbackReuseWithinClass": "forbid",
            "minClassFormats": 4,
        },
        "id": class_id,
        "phase": {16: "input", 17: "form", 18: "comprehension", 19: "production", 20: "transfer"}[number],
        "title": {"en": spec["title"][0], "es": spec["title"][1]},
        "concepts": [concept],
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [f"en.n2.class-{number - 1:02d}"],
        "usesVocabulary": [en for en, _ in spec["vocabulary"]],
        "usesPatterns": spec.get("cumulative", [concept]) if number == 20 else [concept],
        "objectives": {"es": OBJECTIVES[number]},
        "vocabulary": [{"en": en, "es": es} for en, es in spec["vocabulary"]],
        "teaching": teaching,
        "pools": pools,
        "remediationMap": {
            f"en.n2.c{number:02d}.e{index:02d}": {
                "reteach": f"{class_id}.t{index:02d}",
                "review": f"en.n2.c{number:02d}.r{min(index, 3):02d}",
            }
            for index in range(1, 5)
        },
        "accessibility": {"highContrast": True, "largeText": True, "screenReader": True, "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2, "allowAudioReplay": True, "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True},
    }
    if number == 20:
        result["cumulativeEvaluation"] = spec["cumulative"]
    return result


def audit_agent_contract(cls):
    prompts = []
    feedback = []
    formats = set()
    for items in cls["pools"].values():
        for item in items:
            prompt = item["prompt"]["es"]
            prompts.append(prompt)
            feedback.append(item["origin"]["feedback"]["es"])
            formats.add(item["format"])
            if item["format"] in {"elegir", "escuchar"}:
                assert len(item["choices"]) >= 3, f"{item['id']}: fewer than 3 choices"
    assert max(map(len, prompts)) <= 90, f"{cls['id']}: prompt exceeds 90 characters"
    assert len(feedback) == len(set(feedback)), f"{cls['id']}: repeated feedback"
    assert len(formats) >= 4, f"{cls['id']}: fewer than 4 formats"
    assert "escribir" in formats, f"{cls['id']}: escritura skill lacks an escribir item"
    forbidden = ("idea trabajada", "modelo de la clase", "contexto nuevo", "frase indicada")
    assert not any(term in prompt.casefold() for term in forbidden for prompt in prompts), f"{cls['id']}: deictic prompt"
    expected_phase = {16: "input", 17: "form", 18: "comprehension", 19: "production", 20: "transfer"}
    number = int(cls["id"].rsplit("-", 1)[1])
    assert cls["phase"] == expected_phase[number], f"{cls['id']}: wrong phase"


def write_class(number):
    target = OUT / f"class-{number:02d}.json"
    cls = build_class(number)
    audit_agent_contract(cls)
    target.write_text(json.dumps(cls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(target)


def write_bundle():
    classes = [json.loads((OUT / f"class-{number:02d}.json").read_text(encoding="utf-8")) for number in range(16, 21)]
    for cls in classes:
        audit_agent_contract(cls)
    objectives = [objective for cls in classes for objective in cls["objectives"]["es"]]
    assert len(objectives) == len(set(objectives)), "objectives repeated across classes"
    bundle = {
        "schema": "onelingo.editorial.class-bundle.v1",
        "course": "en",
        "level": 2,
        "scale": SCALE,
        "status": "shadow",
        "runtimeAi": False,
        "classes": classes,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
    }
    target = OUT / "bundle-16-20.json"
    target.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(target)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--class-number", type=int, choices=range(16, 21))
    group.add_argument("--bundle", action="store_true")
    args = parser.parse_args()
    if args.bundle:
        write_bundle()
    else:
        write_class(args.class_number)


if __name__ == "__main__":
    main()
