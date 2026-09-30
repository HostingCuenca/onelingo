#!/usr/bin/env python3
"""Regenera las clases editoriales de Inglés N2 C61-C65."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n2"
SCALE = "client-10-levels-v1"
CONCEPTS = {
    61: "n2-can-could-requests",
    62: "n2-may-can-permission",
    63: "n2-can-shall-offers",
    64: "n2-polite-responses",
    65: "n2-service-conversation",
}
TITLES = {
    61: ("Can and could for requests", "Can y could para peticiones"),
    62: ("May and can for permission", "May y can para permiso"),
    63: ("Offers with can and shall", "Ofrecimientos con can y shall"),
    64: ("Respond politely", "Responder con cortesía"),
    65: ("Service conversation", "Conversación de servicio"),
}
PHASES = {61: "input", 62: "form", 63: "comprehension", 64: "production", 65: "transfer"}
CUMULATIVE = [CONCEPTS[n] for n in range(61, 66)]
# Routes follow the failed function/polarity instead of item ordinal.
REMEDIATION = {
    61: {"e01": ("t04", "r01"), "e02": ("t02", "r03"), "e03": ("t01", "r01"), "e04": ("t04", "r01")},
    62: {"e01": ("t01", "r03"), "e02": ("t04", "r01"), "e03": ("t02", "r03"), "e04": ("t03", "r02")},
    63: {"e01": ("t04", "r01"), "e02": ("t03", "r02"), "e03": ("t02", "r03"), "e04": ("t04", "r01")},
    64: {"e01": ("t03", "r03"), "e02": ("t01", "r01"), "e03": ("t04", "r03"), "e04": ("t02", "r01")},
    65: {"e01": ("t02", "r01"), "e02": ("t04", "r02"), "e03": ("t05", "r03"), "e04": ("t05", "r03")},
}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def add_hash(item):
    payload = {k: v for k, v in item.items() if k not in {"id", "contentHash"}}
    item["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return item


def segments(en, es):
    ew, sw = en.split(), es.split()
    em, sm = max(1, len(ew) // 2), max(1, len(sw) // 2)
    return [{"en": " ".join(ew[:em]), "es": " ".join(sw[:sm])},
            {"en": " ".join(ew[em:]), "es": " ".join(sw[sm:])}]


def ch(prompt, choices, index, feedback, requires=None):
    return {"format": "elegir", "prompt": prompt, "choices": choices,
            "answerIndex": index, "feedback": feedback,
            "hint": "Observa quién pide, permite, ofrece o responde.", **({"requires": requires} if requires is not None else {})}


def co(prompt, answer, feedback, requires=None):
    return {"format": "completar", "prompt": prompt, "answer": answer,
            "feedback": feedback, "hint": "Completa solo la palabra o fragmento ausente.", **({"requires": requires} if requires is not None else {})}


def order(prompt, answer, feedback, requires=None):
    return {"format": "ordenar", "prompt": prompt, "answer": answer,
            "feedback": feedback, "hint": "Ordena primero el sujeto y después el verbo modal.", **({"requires": requires} if requires is not None else {})}


def listen(prompt, audio, choices, index, feedback, requires=None):
    return {"format": "escuchar", "prompt": prompt, "audio": audio,
            "choices": choices, "answerIndex": index, "feedback": feedback,
            "hint": "Escucha la forma modal y la intención de la frase.", **({"requires": requires} if requires is not None else {})}


def write(prompt, stimulus, answer, accepted, feedback, requires=None):
    return {"format": "escribir", "prompt": prompt, "stimulus": stimulus,
            "answer": answer, "accepted": accepted, "feedback": feedback,
            "hint": "Escribe la petición o respuesta con cortesía.", **({"requires": requires} if requires is not None else {})}


def match(prompt, pairs, feedback, requires=None):
    return {"format": "relacionar", "prompt": prompt, "pairs": pairs,
            "feedback": feedback, "hint": "Relaciona cada expresión con su significado.", **({"requires": requires} if requires is not None else {})}


def fb(rule, label, answer):
    return f"{rule} En {label}, la respuesta es «{answer}»."


SPECS = {
    61: {
        "rule": "Can y could piden una acción; could suele sonar más suave o formal que can.",
        "vocab": [("request", "petición"), ("help", "ayuda"), ("books", "libros"),
                  ("carry", "llevar"), ("open", "abrir"), ("explain", "explicar"),
                  ("box", "caja"), ("window", "ventana")],
        "teaching": [
            ("Can you help me with this box, please?", "¿Puedes ayudarme con esta caja, por favor?", "Can formula una petición directa y amable."),
            ("Could you open the window, please?", "¿Podrías abrir la ventana, por favor?", "Could hace la petición más suave."),
            ("Can you carry these books?", "¿Puedes llevar estos libros?", "Can pide una acción concreta."),
            ("Could you explain the form?", "¿Podrías explicar el formulario?", "Could introduce una petición cortés de información."),
            ("A request asks someone to do an action.", "Una petición pide a alguien que haga una acción.", "Request nombra el acto de pedir una acción."),
        ],
        "pools": {
            "practiceGuided": [
                ch("Elige la petición correcta para abrir la ventana.", ["Could you open the window, please?", "Could you opens the window?", "Could open you the window?"], 0, fb("Could you inicia una petición cortés.", "la elección guiada", "Could you open the window, please?")),
                co("Completa la petición: Can you ___ me with this box?", "help", fb("Can you va seguido del verbo base help.", "el primer espacio", "help")),
                order("Ordena una petición para llevar los libros.", "Can you carry these books?", fb("La pregunta coloca can antes del sujeto you.", "el primer orden", "Can you carry these books?")),
            ],
            "practice": [
                write("Escribe: ¿Podrías explicar el formulario, por favor?", "¿Podrías explicar el formulario, por favor?", "Could you explain the form, please?", ["Could you explain the form, please?", "Could you please explain the form?"], fb("Could you y could you please expresan una petición cortés.", "la primera producción", "Could you explain the form, please?")),
                listen("Escucha y elige la petición para pedir ayuda con una caja.", "Could you carry this box, please?", ["Could you carry this box, please?", "Could you carries this box?", "Could carry you this box?"], 0, fb("Could you carry pide a otra persona una acción y carry queda en forma base.", "el primer audio", "Could you carry this box, please?")),
                match("Relaciona una función y una acción de petición.", [("request", "petición"), ("carry", "llevar")], fb("Request nombra el acto y carry la acción que se puede pedir.", "el primer grupo léxico", "request / carry")),
            ],
            "evaluation": [
                ch("Elige la petición más cortés para una explicación.", ["Can you explains this rule?", "Could you explain this rule, please?", "Could explain you this rule?"], 1, fb("Could you explain es una petición cortés con verbo base.", "la primera evaluación", "Could you explain this rule, please?")),
                co("Completa: Could you ___ the door, please?", "open", fb("Could you va seguido del verbo base open.", "el segundo espacio", "open")),
                write("Escribe: ¿Puedes ayudarme con estas cajas?", "¿Puedes ayudarme con estas cajas?", "Can you help me with these boxes?", ["Can you help me with these boxes?", "Can you help me with the boxes?"], fb("Can you help formula una petición directa y clara.", "la producción evaluada", "Can you help me with these boxes?")),
                listen("Escucha y elige la petición de información.", "Could you explain this map, please?", ["Could you explains this map?", "Could explain you this map?", "Could you explain this map, please?"], 2, fb("Could you explain usa sujeto y verbo base en ese orden.", "el audio evaluado", "Could you explain this map, please?")),
            ],
            "review": [
                match("Relaciona dos acciones que se pueden pedir.", [("help", "ayudar"), ("explain", "explicar")], fb("Help y explain son acciones que otra persona puede hacer tras una petición.", "el segundo grupo léxico", "help / explain")),
                co("Completa la petición: Can you ___ these books?", "carry", fb("Can you se completa con el verbo base carry.", "el repaso modal", "carry")),
                write("Escribe: ¿Podrías abrir la puerta?", "¿Podrías abrir la puerta?", "Could you open the door?", ["Could you open the door?", "Could you please open the door?"], fb("Could you open es una petición suave y completa.", "la producción de repaso", "Could you open the door?")),
            ],
        },
    },
    62: {
        "rule": "May y can piden permiso; may suele ser más formal y can es común en situaciones cotidianas.",
        "vocab": [("permission", "permiso"), ("phone", "teléfono"), ("seat", "asiento"),
                  ("enter", "entrar"), ("bring", "traer"), ("visitor", "visitante"),
                  ("museum", "museo"), ("polite", "cortés")],
        "teaching": [
            ("May I use your phone, please?", "¿Puedo usar tu teléfono, por favor?", "May I pide permiso de manera formal."),
            ("Can I sit in this seat?", "¿Puedo sentarme en este asiento?", "Can I pide permiso en una situación cotidiana."),
            ("You may enter the museum now.", "Puedes entrar al museo ahora.", "You may también concede permiso."),
            ("Can visitors bring a small bag?", "¿Pueden los visitantes traer una bolsa pequeña?", "Can pregunta por una regla o permiso general."),
            ("May sounds more polite than can for permission.", "May suena más cortés que can para pedir permiso.", "La elección depende del grado de cortesía."),
        ],
        "pools": {
            "practiceGuided": [
                ch("Elige el permiso formal para usar el teléfono.", ["May I use your phone, please?", "May I uses your phone?", "May use I your phone?"], 0, fb("May I use pide permiso formalmente y use queda en forma base.", "la elección guiada", "May I use your phone, please?")),
                co("Completa el permiso cotidiano: Can I ___ here?", "sit", fb("Can I va seguido del verbo base sit.", "el primer espacio", "sit")),
                order("Ordena el permiso para entrar al museo.", "You may enter the museum now.", fb("You may concede permiso antes del verbo enter.", "el primer orden", "You may enter the museum now.")),
            ],
            "practice": [
                write("Escribe: ¿Puedo traer una bolsa pequeña?", "¿Puedo traer una bolsa pequeña?", "Can I bring a small bag?", ["Can I bring a small bag?", "May I bring a small bag?"], fb("Can I y may I pueden pedir permiso; may es más formal.", "la primera producción", "Can I bring a small bag?")),
                listen("Escucha y elige el permiso para sentarse.", "May I sit in this seat?", ["May I sit in this seat?", "May I sits in this seat?", "May sit I in this seat?"], 0, fb("May I sit mantiene el verbo base después de may.", "el primer audio", "May I sit in this seat?")),
                match("Relaciona dos palabras sobre permiso.", [("permission", "permiso"), ("visitor", "visitante")], fb("Permission nombra la autorización y visitor a quien la pide.", "el primer grupo léxico", "permission / visitor")),
            ],
            "evaluation": [
                ch("Elige la pregunta formal para entrar al museo.", ["Can I enters the museum?", "May I enter the museum, please?", "May enter I the museum?"], 1, fb("May I enter es la petición formal y usa verbo base.", "la primera evaluación", "May I enter the museum, please?")),
                co("Completa la regla: Can visitors ___ a small bag?", "bring", fb("Can visitors va seguido del verbo base bring.", "el segundo espacio", "bring")),
                write("Escribe: ¿Puedo sentarme en este asiento, por favor?", "¿Puedo sentarme en este asiento, por favor?", "May I sit in this seat, please?", ["May I sit in this seat, please?", "Can I sit in this seat, please?"], fb("May I sit pide permiso con un registro formal.", "la producción evaluada", "May I sit in this seat, please?")),
                listen("Escucha y elige el único permiso concedido.", "Visitors may enter the museum now.", ["Visitors must enter the museum now.", "Visitors may enter the museum now.", "Visitors may enters the museum now."], 1, fb("Visitors may enter concede permiso; must expresa obligación y enters rompe el verbo base.", "el audio evaluado", "Visitors may enter the museum now.")),
            ],
            "review": [
                match("Relaciona dos palabras del museo.", [("phone", "teléfono"), ("museum", "museo")], fb("Phone y museum forman contextos visibles de permiso.", "el segundo grupo léxico", "phone / museum")),
                co("Completa el permiso: You may ___ now.", "enter", fb("You may se completa con el verbo base enter.", "el repaso modal", "enter")),
                write("Escribe: ¿Pueden los visitantes traer bolsas?", "¿Pueden los visitantes traer bolsas?", "Can visitors bring bags?", ["Can visitors bring bags?", "May visitors bring bags?"], fb("Can visitors bring pregunta por una regla general.", "la producción de repaso", "Can visitors bring bags?")),
            ],
        },
    },
    63: {
        "rule": "Can I y shall I ofrecen ayuda; shall we propone una acción conjunta.",
        "vocab": [("offer", "ofrecimiento"), ("bag", "bolsa"), ("door", "puerta"),
                  ("water", "agua"), ("cab", "taxi"), ("lift", "ascensor"),
                  ("umbrella", "paraguas"), ("wait", "esperar")],
        "teaching": [
            ("Can I carry your bag?", "¿Puedo llevar tu bolsa?", "Can I ofrece ayuda a otra persona."),
            ("Shall I open the door?", "¿Abro la puerta?", "Shall I ofrece hacer una acción."),
            ("We can bring some water.", "Podemos traer agua.", "Can también ofrece una posibilidad de ayuda."),
            ("Shall we call a cab?", "¿Llamamos a un taxi?", "Shall we propone una acción conjunta."),
            ("Can and shall both introduce an offer.", "Can y shall pueden introducir un ofrecimiento.", "La forma cambia según quién ofrece la acción."),
        ],
        "pools": {
            "practiceGuided": [
                ch("Elige el ofrecimiento para llevar la bolsa.", ["Can I carry your bag?", "Can I carries your bag?", "Carry I can your bag?"], 0, fb("Can I carry ofrece ayuda con el verbo base carry.", "la elección guiada", "Can I carry your bag?")),
                co("Completa el ofrecimiento: Shall I ___ the door?", "open", fb("Shall I va seguido del verbo base open.", "el primer espacio", "open")),
                order("Ordena la propuesta de llamar a un taxi.", "Shall we call a cab?", fb("Shall we propone una acción compartida.", "el primer orden", "Shall we call a cab?")),
            ],
            "practice": [
                write("Escribe: ¿Puedo traerte agua?", "¿Puedo traerte agua?", "Can I bring you some water?", ["Can I bring you some water?", "Shall I bring you some water?"], fb("Can I bring ofrece ayuda con un verbo base.", "la primera producción", "Can I bring you some water?")),
                listen("Escucha y elige el ofrecimiento de esperar.", "Shall I wait for you?", ["Shall I wait for you?", "Shall I waits for you?", "Wait I shall for you?"], 0, fb("Shall I wait ofrece hacer la acción de esperar.", "el primer audio", "Shall I wait for you?")),
                match("Relaciona dos palabras de ofrecimientos.", [("offer", "ofrecimiento"), ("umbrella", "paraguas")], fb("Offer nombra la ayuda y umbrella es un objeto que se puede ofrecer.", "el primer grupo léxico", "offer / umbrella")),
            ],
            "evaluation": [
                ch("Elige la propuesta para usar el ascensor.", ["Shall we uses the lift?", "Shall we use the lift?", "Use we shall the lift?"], 1, fb("Shall we use propone una acción conjunta.", "la primera evaluación", "Shall we use the lift?")),
                co("Ofrezco agua a una persona: Can I ___ you some water?", "bring", fb("Can I bring you ofrece una acción a otra persona; bring queda en forma base.", "el segundo espacio", "bring")),
                write("Escribe: ¿Abro la puerta por ti?", "¿Abro la puerta por ti?", "Shall I open the door for you?", ["Shall I open the door for you?", "Can I open the door for you?"], fb("Shall I open ofrece hacer la acción por otra persona.", "la producción evaluada", "Shall I open the door for you?")),
                listen("Escucha y elige la propuesta de llamar un taxi.", "Shall we call a cab for them?", ["Shall we calls a cab for them?", "Shall call we a cab for them?", "Shall we call a cab for them?"], 2, fb("Shall we call propone una acción conjunta con verbo base.", "el audio evaluado", "Shall we call a cab for them?")),
            ],
            "review": [
                match("Relaciona dos palabras de ayuda.", [("taxi", "taxi"), ("wait", "esperar")], fb("Taxi y wait aparecen en ofrecimientos de ayuda.", "el segundo grupo léxico", "taxi / wait")),
                co("Ofrezco agua a Ana: Shall I ___ you some water?", "bring", fb("Shall I bring you ofrece una acción a Ana; bring queda en forma base.", "el repaso de ofrecimiento", "bring")),
                write("Ofrece llevar dos bolsas pesadas por otra persona.", "Veo que llevas dos bolsas pesadas. Ofrece: ¿Llevo esas bolsas por ti?", "Shall I carry those bags for you?", ["Shall I carry those bags for you?", "Can I carry those bags for you?"], fb("Shall I carry y can I carry ofrecen hacer una acción para otra persona.", "la producción de repaso", "Shall I carry those bags for you?")),
            ],
        },
    },
    64: {
        "rule": "Una respuesta cortés acepta, rechaza o agradece la petición sin perder claridad.",
        "vocab": [("certainly", "por supuesto"), ("course", "supuesto"), ("sorry", "lo siento"),
                  ("right now", "ahora mismo"), ("thanks", "gracias"), ("available", "disponible"),
                  ("problem", "problema"), ("request", "petición")],
        "teaching": [
            ("Yes, of course. I can help you.", "Sí, por supuesto. Puedo ayudarte.", "Of course acepta una petición con cortesía."),
            ("Certainly, I can explain the form.", "Por supuesto, puedo explicar el formulario.", "Certainly confirma la ayuda de manera formal."),
            ("Sorry, I can't help right now.", "Lo siento, no puedo ayudar ahora mismo.", "Sorry y can't rechazan con una explicación breve."),
            ("Thanks for asking, but I am not available.", "Gracias por preguntar, pero no estoy disponible.", "Thanks suaviza una respuesta negativa."),
            ("A polite response answers the request clearly.", "Una respuesta cortés contesta la petición con claridad.", "La cortesía no debe ocultar si se acepta o rechaza."),
        ],
        "pools": {
            "practiceGuided": [
                ch("Elige la respuesta cortés que acepta ayuda.", ["Yes, of course. I can help you.", "Yes, of course. I can helps you.", "Of course I helping you."], 0, fb("Of course acepta y can help mantiene el verbo base.", "la elección guiada", "Yes, of course. I can help you.")),
                co("Completa la respuesta: Sorry, I ___ help right now.", "can't", fb("Can't expresa una negativa cortés con can.", "el primer espacio", "can't")),
                order("Ordena la respuesta de agradecimiento.", "Thanks for asking, but I am not available.", fb("Thanks for asking agradece antes de explicar la negativa.", "el primer orden", "Thanks for asking, but I am not available.")),
            ],
            "practice": [
                write("Escribe: Por supuesto, puedo explicarlo.", "Por supuesto, puedo explicarlo.", "Certainly, I can explain it.", ["Certainly, I can explain it.", "Of course, I can explain it."], fb("Certainly y of course aceptan la petición con cortesía.", "la primera producción", "Certainly, I can explain it.")),
                listen("Escucha y elige la respuesta negativa cortés.", "Sorry, I can't help right now.", ["Sorry, I can't help right now.", "Sorry, I can't helps right now.", "Sorry, I not can help right now."], 0, fb("Sorry suaviza la negativa y can't va con help en forma base.", "el primer audio", "Sorry, I can't help right now.")),
                match("Relaciona dos expresiones de cortesía.", [("certainly", "por supuesto"), ("thanks", "gracias")], fb("Certainly acepta; thanks agradece la petición.", "el primer grupo léxico", "certainly / thanks")),
            ],
            "evaluation": [
                ch("Elige el rechazo realmente cortés.", ["I can't help you right now.", "Certainly, I can help you.", "Sorry, I can't help you right now."], 2, fb("Sorry suaviza el rechazo; la primera opción rechaza sin marcador de cortesía y certainly acepta.", "la primera evaluación", "Sorry, I can't help you right now.")),
                co("Completa la aceptación: Yes, of ___ .", "course", fb("Of course es una aceptación cortés.", "el segundo espacio", "course")),
                write("Escribe una respuesta cortés: No puedes ayudar ahora.", "No puedes ayudar ahora.", "Sorry, I am not available right now.", ["Sorry, I am not available right now.", "Sorry, I am unavailable right now."], fb("Sorry y not available explican una negativa cortés.", "la producción evaluada", "Sorry, I am not available right now.")),
                listen("Escucha y elige la respuesta formal afirmativa.", "Certainly, I can explain the problem.", ["Certainly, I can explains the problem.", "Certainly, I can explain the problem.", "Certainly I explain can the problem."], 1, fb("Certainly acepta y can explain usa el verbo base.", "el audio evaluado", "Certainly, I can explain the problem.")),
            ],
            "review": [
                match("Relaciona dos aceptaciones corteses.", [("course", "aceptación"), ("certainly", "afirmación formal")], fb("Of course acepta y certainly confirma una respuesta afirmativa formal.", "el segundo grupo léxico", "course / certainly")),
                co("Completa la disponibilidad: I am not ___ right now.", "available", fb("Available completa la idea de no estar disponible.", "el repaso modal", "available")),
                write("Escribe: Gracias por preguntar, no estoy disponible hoy.", "Gracias por preguntar, no estoy disponible hoy.", "Thanks for asking, but I am unavailable today.", ["Thanks for asking, but I am unavailable today.", "Thank you for asking, but I am unavailable today."], fb("Thanks for asking suaviza la respuesta negativa y today la sitúa.", "la producción de repaso", "Thanks for asking, but I am unavailable today.")),
            ],
        },
    },
    65: {
        "rule": "Una conversación de servicio combina petición, permiso, ofrecimiento y respuesta cortés para resolver una necesidad.",
        "vocab": [("service", "servicio"), ("service ticket", "ticket de servicio"), ("receipt", "recibo"),
                  ("change", "cambiar"), ("colleague", "colega"), ("solve", "resolver"),
                  ("counter", "mostrador"), ("customer", "cliente"), ("help", "ayuda"), ("problem", "problema")],
        "teaching": [
            ("Good morning. How can I help you?", "Buenos días. ¿Cómo puedo ayudarle?", "How can I help inicia una atención de servicio."),
            ("Could you change this service ticket, please?", "¿Podría cambiar este ticket de servicio, por favor?", "Could you change formula una petición del cliente a otra persona."),
            ("Certainly. May I see your receipt?", "Por supuesto. ¿Puedo ver su recibo?", "May I see pide permiso de forma formal."),
            ("Shall I call a colleague?", "¿Llamo a un colega?", "Shall I call ofrece una solución."),
            ("Customer: Could you update this service ticket, please? Clerk: May I see your order number? Customer: Certainly. Can I wait here? Clerk: Shall I call a supervisor? Customer: Yes, please. Thank you. That solves my problem.", "Cliente: ¿Podría actualizar este ticket de servicio, por favor? Empleado: ¿Puedo ver su número de pedido? Cliente: Claro. ¿Puedo esperar aquí? Empleado: ¿Llamo a un supervisor? Cliente: Sí, por favor. Gracias. Eso resuelve mi problema.", "Este escenario de pedido integra petición, permiso, respuesta cortés, ofrecimiento aceptado y resolución."),
        ],
        "pools": {
            "practiceGuided": [
                ch("Elige la apertura correcta de un servicio.", ["How can I help you?", "How can I helps you?", "How I can help you?"], 0, fb("How can I help inicia el servicio con verbo base.", "la elección guiada", "How can I help you?")),
                co("Completa la petición: Could I ___ this ticket?", "change", fb("Could I se completa con el verbo base change.", "el primer espacio", "change")),
                order("Ordena el permiso para ver el recibo.", "May I see your receipt?", fb("May I see pide permiso formalmente.", "el primer orden", "May I see your receipt?")),
            ],
            "practice": [
                write("Escribe una petición para explicar el ticket de servicio.", "¿Podría explicar este ticket de servicio, por favor?", "Could you explain this service ticket, please?", ["Could you explain this service ticket, please?", "Can you explain this service ticket, please?"], fb("Could you explain y can you explain piden a otra persona una acción concreta.", "la primera producción", "Could you explain this service ticket, please?")),
                listen("Escucha y elige el ofrecimiento del empleado.", "Shall I call a colleague?", ["Shall I call a colleague?", "Shall I calls a colleague?", "Call I shall a colleague?"], 0, fb("Shall I call ofrece una acción con verbo base.", "el primer audio", "Shall I call a colleague?")),
                match("Relaciona dos palabras del servicio.", [("ticket", "billete"), ("counter", "mostrador")], fb("Ticket y counter aparecen en una atención al cliente.", "el primer grupo léxico", "ticket / counter")),
            ],
            "evaluation": [
                ch("Elige la petición de cambio del cliente.", ["May I see this service ticket, please?", "Could change you this service ticket?", "Could you change this service ticket, please?"], 2, fb("Could you change pide al empleado una acción; May I see pediría permiso y la segunda rompe el orden.", "la primera evaluación", "Could you change this service ticket, please?"), requires=[CONCEPTS[61]]),
                co("Completa el ofrecimiento: Shall I call a ___?", "colleague", fb("Shall I call ofrece llamar a un colleague.", "el segundo espacio", "colleague"), requires=[CONCEPTS[63]]),
                write("Redacta un diálogo de corrección con aceptación y resolución.", "Cliente: ¿Podrías corregir este ticket de servicio, por favor? Empleado: ¿Puedo ver tu recibo? Cliente: Claro. ¿Puedo sentarme aquí? Empleado: ¿Llamo a un colega? Cliente: Sí, por favor. Gracias. Eso resuelve mi problema.", "Customer: Could you correct this service ticket, please? Clerk: May I see your receipt? Customer: Of course. Can I sit here? Clerk: Shall I call a colleague? Customer: Yes, please. Thank you. That solves my problem.", ["Customer: Could you correct this service ticket, please? Clerk: May I see your receipt? Customer: Of course. Can I sit here? Clerk: Shall I call a colleague? Customer: Yes, please. Thank you. That solves my problem.", "Customer: Can you correct this service ticket, please? Clerk: Can I see your receipt? Customer: Certainly. May I sit here? Clerk: Can I call a colleague? Customer: Yes, please. Thanks. That solves my problem."], fb("Este escenario distinto conserva roles, petición, permiso, respuesta cortés, ofrecimiento aceptado y resolución.", "la producción acumulativa", "Customer: Could you correct this service ticket, please? Clerk: May I see your receipt? Customer: Of course. Can I sit here? Clerk: Shall I call a colleague? Customer: Yes, please. Thank you. That solves my problem."), requires=CUMULATIVE),
                listen("Escucha y elige el cierre del problema.", "Thank you. That solves my problem.", ["Thank you. That solve my problem.", "Thank you. That solves my problem.", "Thank you. Solves that my problem."], 1, fb("That solves my problem cierra la atención con claridad.", "el audio evaluado", "Thank you. That solves my problem."), requires=[CONCEPTS[65]]),
            ],
            "review": [
                match("Relaciona dos funciones del diálogo de servicio.", [("Could you explain this service ticket?", "petición"), ("Can I wait here?", "permiso")], fb("Could you explain pide una acción y Can I wait solicita permiso.", "el segundo grupo léxico", "request / permission")),
                co("Completa el ofrecimiento: Can I ___ a colleague?", "call", fb("Can I call ofrece una acción para resolver el servicio.", "el repaso de ofrecimiento", "call")),
                write("Redacta un diálogo de impresión con aceptación y resolución.", "Cliente: ¿Puedes imprimir este ticket de servicio? Empleado: ¿Puedo revisar tu pedido? Cliente: Claro. ¿Puedo esperar aquí? Empleado: ¿Puedo llamar a un gerente? Cliente: Sí, por favor. Gracias, mi problema está resuelto.", "Customer: Can you print this service ticket, please? Clerk: Can I check your order? Customer: Certainly. May I wait here? Clerk: Can I call a manager? Customer: Yes, please. Thanks, my problem is solved.", ["Customer: Can you print this service ticket, please? Clerk: Can I check your order? Customer: Certainly. May I wait here? Clerk: Can I call a manager? Customer: Yes, please. Thanks, my problem is solved.", "Customer: Could you print this service ticket, please? Clerk: May I check your order? Customer: Of course. Can I wait here? Clerk: Shall I call a manager? Customer: Yes, please. Thank you, my problem is solved."], fb("Este tercer escenario conserva roles, petición, permiso, respuesta cortés, ofrecimiento aceptado y resolución.", "la producción de repaso", "Customer: Can you print this service ticket, please? Clerk: Can I check your order? Customer: Certainly. May I wait here? Clerk: Can I call a manager? Customer: Yes, please. Thanks, my problem is solved.")),
            ],
        },
    },
}


def make_item(item_id, spec, concept, pool):
    fmt = spec["format"]
    requires = spec.get("requires", [concept])
    origin = {"kind": "editorial", "feedback": {"es": spec["feedback"]}}
    teaches = [concept] if pool == "practiceGuided" else []
    if pool == "practiceGuided":
        requires = []
        origin["hint"] = {"es": spec["hint"]}
    item = {"id": item_id, "format": fmt, "prompt": {"es": spec["prompt"]},
            "answer": {}, "choices": [], "teaches": teaches, "requires": requires,
            "origin": origin, "accessibility": {"screenReader": True, "highContrast": True, "largeText": True}}
    if fmt in {"elegir", "escuchar"}:
        item["choices"] = [{"text": x} for x in spec["choices"]]
        item["answer"] = {"index": spec["answerIndex"]}
        if fmt == "escuchar":
            origin.update({"audio": spec["audio"], "audioMode": "tts", "languageCode": "en",
                           "speedOptions": [0.75, 1.0], "maxReplays": 3, "revealTranscriptAfterAttempt": True})
    elif fmt == "completar":
        item["answer"] = {"text": spec["answer"], "accepted": [spec["answer"]]}
        origin["text"] = spec["prompt"]
    elif fmt == "ordenar":
        item["answer"] = {"text": spec["answer"], "tokens": spec["answer"].split()}
        origin["text"] = spec["prompt"]
    elif fmt == "escribir":
        item["answer"] = {"text": spec["answer"], "accepted": spec["accepted"]}
        origin["text"] = spec["stimulus"]
    elif fmt == "relacionar":
        pairs = [[a, {"es": b}] for a, b in spec["pairs"]]
        item["answer"] = {"pairs": pairs}
        origin["pairs"] = pairs
    else:
        raise ValueError(fmt)
    return add_hash(item)


def build_class(number):
    spec, concept = SPECS[number], CONCEPTS[number]
    class_id = f"en.n2.class-{number:02d}"
    teaching = [{"id": f"{class_id}.t{i:02d}", "en": en, "es": es,
                 "explanationEs": ex, "segments": segments(en, es), "audioText": en,
                 "audioMode": "tts", "languageCode": "en", "patternId": concept}
                for i, (en, es, ex) in enumerate(spec["teaching"], 1)]
    prefixes = {"practiceGuided": "pg", "practice": "p", "evaluation": "e", "review": "r"}
    pools = {pool: [make_item(f"en.n2.c{number:02d}.{prefixes[pool]}{i:02d}", item, concept, pool)
                    for i, item in enumerate(items, 1)] for pool, items in spec["pools"].items()}
    uses_patterns = CUMULATIVE if number == 65 else [concept]
    class_obj = {
        "schema": "onelingo.editorial.class.v1", "course": "en", "level": 2,
        "scale": SCALE, "status": "shadow", "runtimeAi": False,
        "selectionPolicy": {"deterministic": True}, "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": {"chronologyTokens": "enforce", "answerReuseAcrossEarlyReserved": "forbid", "answerEvidenceReuseAcrossPools": "forbid", "agentContract": "editorial-agent.v2", "minChoices": 3, "maxPromptCharacters": 90, "feedbackReuseWithinClass": "forbid", "minClassFormats": 4},
        "id": class_id, "phase": PHASES[number], "title": {"en": TITLES[number][0], "es": TITLES[number][1]},
        "concepts": [concept], "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [f"en.n2.class-{number - 1:02d}"], "usesVocabulary": [a for a, _ in spec["vocab"]], "usesPatterns": uses_patterns,
        "objectives": {"es": {
            61: ["Reconocer peticiones con can y could en diálogos breves.", "Distinguir el grado de cortesía de una petición.", "Producir peticiones claras para acciones cotidianas."],
            62: ["Reconocer permisos con may y can en situaciones comunes.", "Elegir may o can según el registro de la situación.", "Pedir y conceder permiso con una fórmula completa."],
            63: ["Comprender ofrecimientos con can y shall.", "Distinguir ayuda individual de una propuesta compartida.", "Ofrecer acciones concretas con cortesía."],
            64: ["Comprender respuestas afirmativas y negativas corteses.", "Relacionar cortesía con aceptación o rechazo claro.", "Responder a una petición sin ocultar la decisión."],
            65: ["Integrar peticiones, permisos y ofrecimientos en un servicio.", "Resolver una necesidad del cliente con lenguaje cortés.", "Producir una conversación de servicio breve y clara."],
        }[number]},
        "vocabulary": [{"en": a, "es": b} for a, b in spec["vocab"]], "teaching": teaching, "pools": pools,
        "remediationMap": {
            f"en.n2.c{number:02d}.{error_id}": {
                "reteach": f"{class_id}.{targets[0]}",
                "review": f"en.n2.c{number:02d}.{targets[1]}",
            }
            for error_id, targets in REMEDIATION[number].items()
        },
        "accessibility": {"highContrast": True, "largeText": True, "screenReader": True, "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2, "allowAudioReplay": True, "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True},
    }
    if number == 65:
        class_obj["cumulativeEvaluation"] = CUMULATIVE
    return class_obj


def audit(cls):
    prompts = [item["prompt"]["es"] for pool in cls["pools"].values() for item in pool]
    feedback = [item["origin"]["feedback"]["es"] for pool in cls["pools"].values() for item in pool]
    assert len(prompts) == len(set(prompts)) and len(feedback) == len(set(feedback))
    assert max(map(len, prompts)) <= 90
    assert len({item["format"] for pool in cls["pools"].values() for item in pool}) >= 4


def write_class(number):
    cls = build_class(number); audit(cls)
    path = OUT / f"class-{number:02d}.json"
    path.write_text(json.dumps(cls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)


def write_bundle():
    classes = [json.loads((OUT / f"class-{n:02d}.json").read_text(encoding="utf-8")) for n in range(61, 66)]
    for cls in classes: audit(cls)
    objectives = [x for cls in classes for x in cls["objectives"]["es"]]
    assert len(objectives) == len(set(objectives))
    bundle = {"schema": "onelingo.editorial.class-bundle.v1", "course": "en", "level": 2, "scale": SCALE, "status": "shadow", "runtimeAi": False, "classes": classes, "selectionPolicy": {"deterministic": True}, "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]}}
    path = OUT / "bundle-61-65.json"
    path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)


def main():
    parser = argparse.ArgumentParser(); group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--class-number", type=int, choices=range(61, 66)); group.add_argument("--bundle", action="store_true")
    args = parser.parse_args(); write_bundle() if args.bundle else write_class(args.class_number)


if __name__ == "__main__":
    main()
