#!/usr/bin/env python3
"""Build isolated editorial drafts for English N2 classes 86-90."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n2"
SCALE = "client-10-levels-v1"
CONCEPTS = {
    86: "n2-digital-devices-actions",
    87: "n2-digital-messages-plans",
    88: "n2-digital-tech-problems",
    89: "n2-digital-step-instructions",
    90: "n2-digital-communication-task",
}
TITLES = {
    86: ("Devices and basic actions", "Dispositivos y acciones básicas"),
    87: ("Messages and online plans", "Mensajes y planes en línea"),
    88: ("Explain a simple technical problem", "Explicar un problema técnico sencillo"),
    89: ("Give step-by-step instructions", "Dar instrucciones paso a paso"),
    90: ("Digital communication task", "Tarea de comunicación digital"),
}
PHASES = {86: "input", 87: "form", 88: "comprehension", 89: "production", 90: "transfer"}
CUMULATIVE = [CONCEPTS[n] for n in range(86, 91)]
REMEDIATION = {
    86: {"e01": ("t03", "r02"), "e02": ("t04", "r03"), "e03": ("t02", "r01"), "e04": ("t03", "r02")},
    87: {"e01": ("t05", "r02"), "e02": ("t04", "r03"), "e03": ("t05", "r02"), "e04": ("t05", "r01")},
    88: {"e01": ("t05", "r01"), "e02": ("t04", "r01"), "e03": ("t04", "r01"), "e04": ("t03", "r02")},
    89: {"e01": ("t02", "r03"), "e02": ("t06", "r03"), "e03": ("t06", "r03"), "e04": ("t04", "r02")},
    90: {"e01": ("t05", "r03"), "e02": ("t05", "r02"), "e03": ("t05", "r03"), "e04": ("t06", "r01")},
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
            "hint": "Observa la acción digital y el contexto.",
            **({"requires": requires} if requires is not None else {})}


def co(prompt, answer, feedback, requires=None, accepted=None):
    return {"format": "completar", "prompt": prompt, "answer": answer,
            "feedback": feedback, "hint": "Completa solo el fragmento ausente.",
            **({"accepted": accepted} if accepted is not None else {}),
            **({"requires": requires} if requires is not None else {})}


def order(prompt, answer, feedback, requires=None):
    return {"format": "ordenar", "prompt": prompt, "answer": answer,
            "feedback": feedback, "hint": "Ordena la acción paso a paso.",
            **({"requires": requires} if requires is not None else {})}


def listen(prompt, audio, choices, index, feedback, requires=None):
    return {"format": "escuchar", "prompt": prompt, "audio": audio,
            "choices": choices, "answerIndex": index, "feedback": feedback,
            "hint": "Escucha la acción y el dispositivo.",
            **({"requires": requires} if requires is not None else {})}


def write(prompt, stimulus, answer, accepted, feedback, requires=None):
    return {"format": "escribir", "prompt": prompt, "stimulus": stimulus,
            "answer": answer, "accepted": accepted, "feedback": feedback,
            "hint": "Escribe una instrucción o mensaje completo.",
            **({"requires": requires} if requires is not None else {})}


def match(prompt, pairs, feedback, requires=None):
    return {"format": "relacionar", "prompt": prompt, "pairs": pairs,
            "feedback": feedback, "hint": "Relaciona la acción con su función.",
            **({"requires": requires} if requires is not None else {})}


def fb(rule, label, answer):
    return f"{rule} En {label}, la respuesta es «{answer}»."


SPECS = {
    86: {
        "vocab": [("tablet", "tableta"), ("charger", "cargador"), ("screen", "pantalla"), ("app", "aplicación"), ("headphones", "auriculares"), ("laptop", "portátil"), ("button", "botón"), ("plug", "enchufar"), ("battery", "batería"), ("calendar", "calendario")],
        "teaching": [
            ("Turn on the tablet with the power button.", "Enciende la tableta con el botón de encendido.", "Turn on inicia el dispositivo."),
            ("Plug the charger into the phone.", "Enchufa el cargador en el teléfono.", "Plug describe conectar el cargador."),
            ("Tap the app icon to open it.", "Toca el icono de la aplicación para abrirla.", "Tap the app icon indica tocar el icono visible para abrirlo."),
            ("Turn off the tablet after class.", "Apaga la tableta después de clase.", "Turn off termina el uso del dispositivo."),
            ("Connect the headphones to the laptop.", "Conecta los auriculares al portátil.", "Connect une dos dispositivos."),
        ],
        "pools": {
            "practiceGuided": [
                ch("Elige la acción correcta para iniciar la tableta.", ["Turn on the tablet.", "Turn off the tablet.", "Tap the tablet."], 0, fb("Turn on inicia un dispositivo.", "la acción guiada", "Turn on the tablet.")),
                co("Completa: Plug the ___ into the phone.", "charger", fb("Charger es el objeto que se enchufa.", "el primer fragmento", "charger")),
                order("Ordena la acción de abrir una aplicación.", "Tap the app icon to open it.", fb("Tap the app icon va antes de la finalidad open it.", "el primer orden", "Tap the app icon to open it.")),
            ],
            "practice": [
                write("Escribe: Conecta los auriculares al portátil.", "Conecta los auriculares al portátil.", "Connect the headphones to the laptop.", ["Connect the headphones to the laptop.", "Connect your headphones to the laptop."], fb("Connect une headphones con laptop.", "la primera producción", "Connect the headphones to the laptop.")),
                listen("Escucha y elige la acción para apagar la tableta.", "Turn off the tablet after class.", ["Turn on the tablet after class.", "Turn off the tablet after class.", "Tap the tablet after class."], 1, fb("Turn off termina el uso de la tableta.", "el audio guiado", "Turn off the tablet after class.")),
                match("Relaciona dos objetos digitales.", [("screen", "pantalla"), ("button", "botón")], fb("Screen y button son partes observables del dispositivo.", "el primer grupo", "screen / button")),
            ],
            "evaluation": [
                ch("La aplicación de calendario está cerrada. Elige cómo abrirla.", ["Swipe the screen to find the calendar.", "Hold the power button to open the calendar.", "Tap the calendar app icon to open it."], 2, fb("Tap the calendar app icon abre la aplicación cerrada.", "la primera evaluación", "Tap the calendar app icon to open it.")),
                co("Después de la clase, completa: Turn ___ the laptop to save battery.", "off", fb("Después de la clase y para ahorrar batería, la acción es turn off.", "el segundo fragmento", "off")),
                write("En el aeropuerto, conecta el teléfono al cargador antes de embarcar.", "En el aeropuerto, conecta el teléfono al cargador antes de embarcar.", "Connect the phone to the charger before boarding.", ["Connect the phone to the charger before boarding.", "Plug the phone into the charger before boarding."], fb("Connect or plug the phone to the charger expresa la acción contextual.", "la producción evaluada", "Connect the phone to the charger before boarding.")),
                listen("Escucha qué abre la persona en el portátil antes de clase.", "Open the music app on the laptop before class.", ["Open the music app on the tablet before class.", "Open the music app on the laptop before class.", "Connect the headphones to the laptop before class."], 1, fb("Open the music app describe la acción que sigue al inicio del portátil.", "el audio evaluado", "Open the music app on the laptop before class.")),
            ],
            "review": [
                match("Relaciona dos acciones del dispositivo.", [("turn on", "encender"), ("plug", "enchufar")], fb("Turn on inicia y plug conecta un dispositivo.", "el repaso de acciones", "turn on / plug")),
                co("La aplicación está cerrada. Completa: Tap the app ___ to open it.", "icon", fb("La aplicación cerrada se abre al tocar el app icon.", "el repaso de icono", "icon")),
                write("Escribe: Apaga la tableta antes de la cena.", "Apaga la tableta antes de la cena.", "Turn off the tablet before dinner.", ["Turn off the tablet before dinner.", "Please turn off the tablet before dinner."], fb("Turn off the tablet expresa el cierre del uso.", "la producción de repaso", "Turn off the tablet before dinner.")),
            ],
        },
    },
    87: {
        "vocab": [("message", "mensaje"), ("reply", "responder"), ("online", "en línea"), ("meeting", "reunión"), ("link", "enlace"), ("group", "grupo"), ("schedule", "horario"), ("invite", "invitar")],
        "teaching": [
            ("Send a message to the group about tomorrow's meeting.", "Envía un mensaje al grupo sobre la reunión de mañana.", "Send a message comunica información al grupo."),
            ("Please reply before six o'clock.", "Responde antes de las seis.", "Reply indica contestar un mensaje."),
            ("The online meeting starts at ten.", "La reunión en línea empieza a las diez.", "Online meeting nombra una reunión digital."),
            ("Share the link with the invited students.", "Comparte el enlace con los estudiantes invitados.", "Share the link permite que otros entren."),
            ("We can plan the call in the group chat.", "Podemos planificar la llamada en el chat del grupo.", "Plan the call organiza una actividad futura."),
        ],
        "pools": {
            "practiceGuided": [
                ch("Elige el mensaje sobre la reunión de mañana.", ["Send a message about tomorrow's meeting.", "Delete tomorrow's meeting.", "Turn off the meeting."], 0, fb("Send a message comunica el plan al grupo.", "la elección guiada", "Send a message about tomorrow's meeting.")),
                co("Completa: Please ___ before six o'clock.", "reply", fb("Reply significa responder el mensaje.", "el primer fragmento", "reply")),
                order("Ordena el plan de la llamada en línea.", "We can plan the call in the group chat.", fb("We can plan organiza una acción futura en el chat.", "el primer orden", "We can plan the call in the group chat.")),
            ],
            "practice": [
                write("Escribe: Comparte el enlace con los estudiantes.", "Comparte el enlace con los estudiantes invitados.", "Share the link with the invited students.", ["Share the link with the invited students.", "Please share the link with the invited students."], fb("Share the link permite acceder al plan en línea.", "la primera producción", "Share the link with the invited students.")),
                listen("Escucha el horario de la reunión en línea.", "The online meeting starts at ten.", ["The online meeting ends at ten.", "The online meeting starts at ten.", "The offline meeting starts at ten."], 1, fb("Starts at ten fija cuándo comienza la reunión.", "el audio guiado", "The online meeting starts at ten.")),
                match("Relaciona dos palabras de planificación.", [("schedule", "horario"), ("invite", "invitar")], fb("Schedule organiza la hora e invite incorpora participantes.", "el primer grupo", "schedule / invite")),
            ],
            "evaluation": [
                ch("La clase tiene invitados y falta fijar el plan. Elige el mensaje útil.", ["Schedule the online meeting for Tuesday at ten.", "Share the meeting link for Tuesday at ten.", "Reply to the invited students after Tuesday."], 0, fb("Schedule the online meeting fija una acción futura para los invitados.", "la primera evaluación", "Schedule the online meeting for Tuesday at ten.")),
                ch("El mensaje muestra una URL para la reunión. ¿Qué dato copias al chat?", ["The link", "The meeting time", "The reply"], 0, fb("Una URL corresponde a the link, que se copia al chat.", "la segunda evaluación", "The link")),
                write("Escribe: Confirma la hora de la llamada en el chat del grupo.", "Confirma la hora de la llamada en el chat del grupo.", "Confirm the call time in the group chat.", ["Confirm the call time in the group chat.", "Please confirm the call time in the group chat."], fb("Confirm the call time comunica un plan concreto.", "la producción evaluada", "Confirm the call time in the group chat.")),
                listen("Escucha qué confirmación necesita la profesora.", "Please confirm the meeting time with the teacher.", ["Please share the meeting time with the teacher.", "Please confirm the meeting time with the teacher.", "Please change the meeting time with the teacher."], 1, fb("Confirm the meeting time responde a la necesidad de la profesora.", "el audio evaluado", "Please confirm the meeting time with the teacher.")),
            ],
            "review": [
                match("Relaciona cada situación con una acción comunicativa.", [("The meeting is at ten.", "confirmar la hora"), ("The link is ready.", "compartirlo con el grupo"), ("A question arrives.", "responderla")], fb("Confirm, share and reply son acciones comunicativas según la situación.", "el repaso funcional", "confirm / share / reply")),
                write("Confirma: la llamada en línea es el viernes a las diez.", "La organizadora pide confirmar que la llamada en línea es el viernes a las diez.", "The online call is on Friday at ten.", ["The online call is on Friday at ten.", "The online call is Friday at ten."], fb("La respuesta confirma día y hora de la llamada.", "el repaso de planificación", "The online call is on Friday at ten.")),
                write("Escribe una respuesta: la clase nueva necesita el enlace antes del mediodía.", "The new class needs the link before noon.", "I will send the link to the new class before noon.", ["I will send the link to the new class before noon.", "I'll send the link to the new class before noon."], fb("La respuesta comparte el link con la clase y conserva el límite de tiempo.", "el repaso de enlace", "I will send the link to the new class before noon.")),
            ],
        },
    },
    88: {
        "vocab": [("problem", "problema"), ("charge", "cargar"), ("cable", "cable de carga"), ("battery", "batería"), ("frozen", "bloqueada"), ("restart", "reiniciar"), ("signal", "señal"), ("connect", "conectar"), ("Wi-Fi", "conexión inalámbrica"), ("keyboard", "teclado"), ("type", "escribir")],
        "teaching": [
            ("My phone is not charging because the cable is loose.", "Mi teléfono no carga porque el cable está suelto.", "Not charging describe el problema y because da la causa."),
            ("The screen is frozen, so I cannot open the app.", "La pantalla está bloqueada, así que no puedo abrir la aplicación.", "Frozen explica por qué la acción no funciona."),
            ("The battery is low, so charge the phone; the signal is strong.", "La batería está baja, así que carga el teléfono; la señal es fuerte.", "Battery low leads to charge the phone, while signal describes connection."),
            ("Please restart the tablet and check the keyboard.", "Reinicia la tableta y revisa el teclado.", "Restart and check are actions for a keyboard problem."),
            ("The Wi-Fi signal is weak, so move closer to the router.", "La señal de Wi-Fi es débil, así que acércate al enrutador.", "Weak Wi-Fi has a visible solution: move closer to the router."),
        ],
        "pools": {
            "practiceGuided": [
                ch("Elige la causa de un teléfono que no carga.", ["The cable is loose.", "The signal is strong.", "The screen is bright."], 0, fb("A loose cable puede impedir que el teléfono cargue.", "la causa guiada", "The cable is loose.")),
                co("Completa: The screen is ___.", "frozen", fb("Frozen describe una pantalla que no responde.", "el primer problema", "frozen")),
                order("Ordena la solución del portátil.", "Please restart the laptop and check the cable.", fb("Restart y check son dos pasos de solución.", "el primer orden", "Please restart the laptop and check the cable.")),
            ],
            "practice": [
                write("Escribe: No puedo conectarme a la reunión en línea.", "No puedo conectarme a la reunión en línea.", "I cannot connect to the online meeting.", ["I cannot connect to the online meeting.", "I can't connect to the online meeting."], fb("Cannot connect explica el problema de acceso.", "la primera producción", "I cannot connect to the online meeting.")),
                listen("Escucha el estado de la batería y la señal.", "The battery is low, but the signal is strong.", ["The battery is strong, but the signal is low.", "The battery is low, but the signal is strong.", "The battery is frozen, but the signal is loose."], 1, fb("Low describe battery y strong describe signal.", "el audio guiado", "The battery is low, but the signal is strong.")),
                match("Relaciona dos acciones de solución.", [("restart", "reiniciar"), ("check", "revisar")], fb("Restart y check son acciones para diagnosticar.", "el primer grupo", "restart / check")),
            ],
            "evaluation": [
                ch("La señal de Wi-Fi es débil y la llamada se detiene. Elige la explicación.", ["The Wi-Fi signal is weak, so the call keeps stopping.", "The Wi-Fi signal is strong, so the call keeps stopping.", "The battery is low, so the call keeps stopping."], 0, fb("Weak Wi-Fi explica por qué la llamada keeps stopping.", "la primera evaluación", "The Wi-Fi signal is weak, so the call keeps stopping.")),
                co("El portátil se bloqueó. Completa: Please ___ it before checking the cable.", "restart", fb("Como el portátil se bloqueó, restart es la acción previa a revisar el cable.", "el segundo problema", "restart")),
                write("Escribe: El teclado no funciona, así que no puedo escribir el mensaje.", "El teclado no funciona, así que no puedo escribir el mensaje.", "The keyboard does not work, so I cannot type the message.", ["The keyboard does not work, so I cannot type the message.", "The keyboard doesn't work, so I can't type the message."], fb("A keyboard problem explains why I cannot type the message.", "la producción evaluada", "The keyboard does not work, so I cannot type the message.")),
                listen("Escucha la solución para una batería baja.", "The phone shows five percent, so charge it before the call.", ["The phone shows five percent, so unplug it before the call.", "The phone shows five percent, so charge it before the call.", "The phone shows five percent, so open the meeting app without charging."], 1, fb("Five percent indicates that the phone must be charged before the call.", "el audio evaluado", "The phone shows five percent, so charge it before the call.")),
            ],
            "review": [
                match("Relaciona cada fallo con una acción útil.", [("Wi-Fi signal weak", "acercarse al router"), ("keyboard does not work", "reiniciar la tableta"), ("battery low", "cargar el teléfono")], fb("A weak Wi-Fi signal needs a better position, a keyboard fault needs a restart and a low battery needs charging.", "el repaso técnico", "Wi-Fi signal weak / keyboard fault / battery low")),
                co("El teléfono muestra 5% de batería. Completa: I need to ___ it before the call.", "charge", fb("Con 5% de batería, charge es la acción necesaria antes de la llamada.", "el repaso de batería", "charge")),
                write("Escribe: El cable está suelto.", "El cable está suelto y el teléfono no carga.", "The cable is loose, so the phone is not charging.", ["The cable is loose, so the phone is not charging.", "The phone is not charging because the cable is loose."], fb("Loose cable explica por qué el phone is not charging.", "la producción de repaso", "The cable is loose, so the phone is not charging.")),
            ],
        },
    },
    89: {
        "vocab": [("first", "primero"), ("next", "después"), ("then", "luego"), ("finally", "finalmente"), ("click", "hacer clic"), ("select", "seleccionar"), ("save", "guardar"), ("icon", "icono"), ("type", "escribir"), ("support", "soporte"), ("ticket", "incidencia")],
        "teaching": [
            ("First, turn on the laptop.", "Primero, enciende el portátil.", "First marca el inicio de una secuencia."),
            ("Next, click the meeting app icon.", "Después, haz clic en el icono de la aplicación de reuniones.", "Next presenta el paso siguiente y icon nombra el objetivo visible."),
            ("Then select the group chat.", "Luego selecciona el chat del grupo.", "Then continúa la secuencia."),
            ("Type the message and click send.", "Escribe el mensaje y haz clic en enviar.", "Type y click describen dos acciones concretas."),
            ("Finally, save the plan and close the app.", "Finalmente, guarda el plan y cierra la aplicación.", "Finally señala el último paso."),
            ("Open the help icon, select the support chat, type the announcement, and click send.", "Abre el icono de ayuda, selecciona el chat de soporte, escribe el aviso y haz clic en enviar.", "Esta secuencia integra abrir, seleccionar, escribir y enviar en una tarea de soporte."),
        ],
        "pools": {
            "practiceGuided": [
                ch("Elige la palabra para iniciar una secuencia.", ["First, turn on the laptop.", "Finally, turn on the laptop.", "Next, turn off the laptop."], 0, fb("First presenta el primer paso.", "la secuencia guiada", "First, turn on the laptop.")),
                co("Completa: Next, ___ the meeting app.", "click", fb("Click es la acción de abrir la aplicación.", "el primer paso", "click")),
                order("Ordena el paso de seleccionar el chat.", "Then select the group chat.", fb("Then va antes de la acción select.", "el primer orden", "Then select the group chat.")),
            ],
            "practice": [
                write("Escribe: Introduce el mensaje y haz clic en enviar.", "Introduce el mensaje y haz clic en enviar.", "Enter the message and click send.", ["Enter the message and click send.", "Enter the message, then click send."], fb("Enter y click send forman dos pasos claros.", "la primera producción", "Enter the message and click send.")),
                listen("Escucha el último paso del plan.", "Finally, save the plan and close the app.", ["First, save the plan and close the app.", "Finally, save the plan and close the app.", "Finally, delete the plan and open the app."], 1, fb("Finally introduce el cierre: save y close.", "el audio guiado", "Finally, save the plan and close the app.")),
                match("Relaciona tres conectores de orden.", [("first", "primero"), ("next", "después"), ("finally", "finalmente")], fb("First inicia, next continúa y finally cierra la secuencia.", "el primer grupo", "first / next / finally")),
            ],
            "evaluation": [
                ch("La aplicación está cerrada y necesitas abrir el chat del grupo. Elige la secuencia.", ["First click the meeting app icon, then select the group chat.", "First select the group chat, then click the meeting app icon.", "First click the meeting app icon, then select the teacher chat."], 0, fb("First click y then select muestran los pasos necesarios para abrir el chat correcto.", "la primera evaluación", "First click the meeting app icon, then select the group chat.")),
                write("Redacta una operación nueva para publicar un aviso.", "Selecciona el chat de soporte y escribe el aviso para el grupo.", "Select the support chat and type the announcement for the group.", ["Select the support chat and type the announcement for the group.", "Choose the support chat and write the group announcement."], fb("Select and type describen las dos operaciones necesarias para el aviso.", "la producción evaluada", "Select the support chat and type the announcement for the group.")),
                write("Escribe una secuencia para añadir una cita al calendario.", "Primero abre el icono del calendario, luego selecciona el viernes y finalmente guarda la cita.", "First open the calendar icon, then select Friday, and finally save the appointment.", ["First open the calendar icon, then select Friday, and finally save the appointment.", "First, open the calendar icon. Next, choose Friday. Finally, save the appointment."], fb("First, then y finally organizan abrir, seleccionar y guardar en un contexto distinto.", "la producción evaluada", "First open the calendar icon, then select Friday, and finally save the appointment.")),
                listen("Escucha el último paso para enviar un mensaje de soporte.", "Finally, send the group message to the teacher.", ["First, save the group message and then close the app.", "Finally, send the group message to the teacher.", "Finally, send the teacher a blank message and open the app."], 1, fb("Finally señala el cierre: send the group message to the teacher.", "el audio evaluado", "Finally, send the group message to the teacher.")),
            ],
            "review": [
                match("Relaciona dos acciones de instrucciones.", [("select", "seleccionar"), ("save", "guardar")], fb("Select elige y save conserva el plan.", "el repaso de acciones", "select / save")),
                co("El texto de soporte está listo. Completa: click the ___ icon to send it.", "send", fb("El icono send publica el texto de soporte que ya está listo.", "el repaso final", "send")),
                write("Recupera otra secuencia de soporte con cuatro pasos.", "El usuario debe abrir el icono de soporte, elegir el chat del ticket, escribir la actualización y enviarla.", "First open the support icon, then select the ticket chat, type the update, and finally click send.", ["First open the support icon, then select the ticket chat, type the update, and finally click send.", "First, open the support icon. Next, select the ticket chat, type the update, and finally click send."], fb("Los conectores recuperan abrir, seleccionar, escribir y enviar en otro caso de soporte.", "la producción de repaso", "First open the support icon, then select the ticket chat, type the update, and finally click send.")),
            ],
        },
    },
    90: {
        "vocab": [("device", "dispositivo"), ("message", "mensaje"), ("meeting", "reunión"), ("cable", "cable de carga"), ("restart", "reiniciar"), ("first", "primero"), ("link", "enlace"), ("reply", "responder"), ("battery", "batería"), ("charger", "cargador"), ("signal", "señal"), ("router", "enrutador")],
        "teaching": [
            ("Turn on the device and open the meeting app.", "Enciende el dispositivo y abre la aplicación de reuniones.", "Device action introduces the digital task."),
            ("Send the group message with the meeting time.", "Envía el mensaje del grupo con la hora de la reunión.", "The message communicates the online plan."),
            ("If the device is not charging, check the cable and restart it.", "Si el dispositivo no carga, revisa el cable y reinícialo.", "The problem has a clear troubleshooting response."),
            ("First connect the headphones; then share the link.", "Primero conecta los auriculares; luego comparte el enlace.", "First and then organize the instructions."),
            ("The phone battery is low. Turn on the phone and open the meeting app. First connect the charger, then send the group the time and link; finally reply to confirm.", "La batería del teléfono está baja. Enciende el teléfono y abre la aplicación. Primero conecta el cargador, luego envía la hora y el enlace al grupo; finalmente responde para confirmar.", "This complete task combines low battery, the device, plan, ordered steps and confirmation."),
            ("If the meeting app is frozen, close it and restart the phone.", "Si la aplicación de reuniones está bloqueada, ciérrala y reinicia el teléfono.", "A frozen meeting app has a clear recovery: close it and restart the phone."),
        ],
        "pools": {
            "practiceGuided": [
                ch("Elige la acción inicial de la tarea digital.", ["Turn on the device and open the meeting app.", "Delete the device and close the app.", "Turn off the device and send no message."], 0, fb("Turn on and open inician la tarea digital.", "la acción acumulativa", "Turn on the device and open the meeting app."), requires=CUMULATIVE[:1]),
                co("Completa el mensaje: Send the group ___ with the meeting time.", "message", fb("Message es lo que comunica la hora.", "el fragmento acumulativo", "message"), requires=CUMULATIVE[:2]),
                order("Ordena el paso para compartir el enlace.", "First connect the headphones; then share the link.", fb("First y then ordenan connect y share.", "el orden acumulativo", "First connect the headphones; then share the link."), requires=CUMULATIVE[:4]),
            ],
            "practice": [
                write("Escribe: Si no carga, revisa el cable y reinicia el dispositivo.", "Si el dispositivo no carga, revisa el cable y reinícialo.", "If the device is not charging, check the cable and restart it.", ["If the device is not charging, check the cable and restart it.", "If the device won't charge, check the cable and restart the device."], fb("The problem, check and restart forman una solución clara.", "la primera producción", "If the device is not charging, check the cable and restart it."), requires=CUMULATIVE[:3]),
                listen("Escucha cómo termina la comunicación digital.", "After the meeting starts, reply to the group.", ["Before the meeting starts, send the group a link.", "After the meeting starts, reply to the group.", "After the meeting starts, open the app and wait."], 1, fb("After the meeting starts, reply to the group cierra la comunicación.", "el audio acumulativo", "After the meeting starts, reply to the group."), requires=CUMULATIVE),
                match("Relaciona dos piezas de la tarea digital.", [("meeting", "reunión"), ("reply", "responder")], fb("Meeting es el plan y reply cierra la comunicación.", "el grupo acumulativo", "meeting / reply"), requires=CUMULATIVE),
            ],
            "evaluation": [
                ch("El dispositivo está apagado y el grupo no tiene el enlace. Elige el primer plan.", ["Turn on the device, open the meeting app, and send the group the link.", "Open the meeting app, send the link, and turn on the device.", "Turn on the device, send the link to the teacher, and open the meeting app."], 0, fb("Turn on, open and send the link resuelven los dos datos faltantes en orden.", "la primera evaluación acumulativa", "Turn on the device, open the meeting app, and send the group the link."), requires=[CONCEPTS[86], CONCEPTS[87]]),
                co("Completa: Please ___ to the group message before six.", "reply", fb("Reply comunica la respuesta al mensaje; respond también es válido.", "la evaluación de comunicación", "reply"), requires=[CONCEPTS[87]], accepted=["reply", "respond"]),
                write("Redacta el diálogo digital con una solución completa.", "Mia: Enciende la tableta y abre la aplicación de llamadas. Leo: La llamada es a las cuatro; envía al grupo la hora y el enlace. Ana: La aplicación de llamadas está bloqueada. Leo: Primero cerraré la aplicación, luego reiniciaré el teléfono y finalmente responderé para confirmar.", "Mia: Turn on the tablet and open the call app. Leo: The call is at four; I will send the group the time and link. Ana: The call app is frozen. Leo: First I will close the app, then restart the phone, and finally reply to confirm.", ["Mia: Turn on the tablet and open the call app. Leo: The call is at four; I will send the group the time and link. Ana: The call app is frozen. Leo: First I will close the app, then restart the phone, and finally reply to confirm.", "Mia: Start the tablet and open the call app. Leo: The call is at four; I will message the group with the time and link. Ana: The call app is frozen. Leo: First I will close the app, then restart the phone, and finally reply to confirm."], fb("El chat incluye iniciar y abrir el dispositivo, comunicar hora y enlace, resolver una aplicación de llamadas congelada con orden y confirmar.", "la producción acumulativa", "Mia: Turn on the tablet and open the call app. Leo: The call is at four; I will send the group the time and link. Ana: The call app is frozen. Leo: First I will close the app, then restart the phone, and finally reply to confirm."), requires=CUMULATIVE),
                listen("Escucha cómo resuelven una aplicación que no responde.", "On the tablet, the call app is not responding. Close the app, then restart the tablet.", ["The call app is slow, so wait and open the link again.", "Close the unresponsive call app, then restart the tablet.", "Send the group link again before restarting the tablet."], 1, fb("La solución cierra la aplicación que no responde y reinicia explícitamente la tableta.", "el audio de resolución", "Close the unresponsive call app, then restart the tablet."), requires=[CONCEPTS[88], CONCEPTS[89]]),
            ],
            "review": [
                match("Relaciona cada fallo con una solución técnicamente coherente.", [("phone is not charging", "enchufar el cable"), ("app is frozen", "reiniciar la aplicación")], fb("A charging failure needs the cable and a frozen app needs a restart.", "el repaso acumulativo", "phone not charging / app frozen"), requires=CUMULATIVE),
                co("Completa: Finally, ___ to confirm the digital plan.", "reply", fb("Reply confirma el plan digital al final; respond también es válido.", "el repaso de comunicación", "reply"), requires=[CONCEPTS[87], CONCEPTS[89]], accepted=["reply", "respond"]),
                write("Recupera este caso digital con los cinco pasos.", "Lista para Jo: 1) Enciende el teléfono y abre la aplicación de reuniones. 2) La llamada es a las seis: envía al grupo la hora y el enlace. 3) Si la señal está débil, acércate al router. 4) Sigue los pasos y responde para confirmar.", "Checklist for Jo: First turn on the phone and open the meeting app. Then send the group the time and link for the six o'clock call. If the signal is weak, move closer to the router. Finally follow the steps and reply to confirm.", ["Checklist for Jo: First turn on the phone and open the meeting app. Then send the group the time and link for the six o'clock call. If the signal is weak, move closer to the router. Finally follow the steps and reply to confirm.", "Jo's checklist: Start the phone and open the meeting app. Next send the group the six o'clock time and link. If the signal is weak, go closer to the router. Finally follow the steps and reply to confirm."], fb("Esta lista recupera iniciar/abrir, plan y enlace, señal débil, pasos ordenados y confirmación en una organización distinta.", "la producción de repaso", "Checklist for Jo: First turn on the phone and open the meeting app. Then send the group the time and link for the six o'clock call. If the signal is weak, move closer to the router. Finally follow the steps and reply to confirm."), requires=CUMULATIVE),
            ],
        },
    },
}


def make_item(item_id, spec, concept, pool):
    fmt = spec["format"]
    requires = spec.get("requires", [concept])
    teaches = [concept] if pool == "practiceGuided" else []
    origin = {"kind": "editorial", "feedback": {"es": spec["feedback"]}}
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
            origin.update({"audio": spec["audio"], "audioMode": "tts", "languageCode": "en", "speedOptions": [0.75, 1.0], "maxReplays": 3, "revealTranscriptAfterAttempt": True})
    elif fmt == "completar":
        item["answer"] = {"text": spec["answer"], "accepted": spec.get("accepted", [spec["answer"]])}
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
    return add_hash(item)


def build_class(number):
    spec, concept = SPECS[number], CONCEPTS[number]
    class_id = f"en.n2.class-{number:02d}"
    teaching = [{"id": f"{class_id}.t{i:02d}", "en": en, "es": es, "explanationEs": ex,
                 "segments": segments(en, es), "audioText": en, "audioMode": "tts", "languageCode": "en", "patternId": concept}
                for i, (en, es, ex) in enumerate(spec["teaching"], 1)]
    prefixes = {"practiceGuided": "pg", "practice": "p", "evaluation": "e", "review": "r"}
    pools = {pool: [make_item(f"en.n2.c{number:02d}.{prefixes[pool]}{i:02d}", item, concept, pool)
                    for i, item in enumerate(items, 1)] for pool, items in spec["pools"].items()}
    uses_patterns = CUMULATIVE if number == 90 else [concept]
    obj = {
        "schema": "onelingo.editorial.class.v1", "course": "en", "level": 2, "scale": SCALE,
        "status": "shadow", "runtimeAi": False, "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": {"chronologyTokens": "enforce", "answerReuseAcrossEarlyReserved": "forbid", "answerEvidenceReuseAcrossPools": "forbid", "agentContract": "editorial-agent.v2", "minChoices": 3, "maxPromptCharacters": 90, "feedbackReuseWithinClass": "forbid", "minClassFormats": 4},
        "id": class_id, "phase": PHASES[number], "title": {"en": TITLES[number][0], "es": TITLES[number][1]},
        "concepts": [concept], "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [f"en.n2.class-{number - 1:02d}"], "usesVocabulary": [a for a, _ in spec["vocab"]], "usesPatterns": uses_patterns,
        "objectives": {"es": {
            86: ["Reconocer dispositivos y acciones digitales básicas.", "Relacionar cada acción con su dispositivo.", "Describir acciones sencillas con tecnología."],
            87: ["Comprender mensajes y planes en línea.", "Identificar información de hora, grupo y enlace.", "Escribir mensajes breves sobre una reunión."],
            88: ["Explicar un problema técnico sencillo.", "Relacionar causa, estado y solución.", "Describir fallos y acciones de recuperación."],
            89: ["Reconocer conectores de secuencia.", "Ordenar instrucciones digitales.", "Dar pasos claros para completar una tarea."],
            90: ["Integrar acciones, mensajes, problemas y pasos digitales.", "Resolver una tarea de comunicación en línea.", "Escribir una instrucción digital completa y clara."],
        }[number]}, "vocabulary": [{"en": a, "es": b} for a, b in spec["vocab"]], "teaching": teaching, "pools": pools,
        "remediationMap": {f"en.n2.c{number:02d}.{eid}": {"reteach": f"{class_id}.{route[0]}", "review": f"en.n2.c{number:02d}.{route[1]}"} for eid, route in REMEDIATION[number].items()},
        "accessibility": {"highContrast": True, "largeText": True, "screenReader": True, "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2, "allowAudioReplay": True, "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True},
    }
    if number == 90:
        obj["cumulativeEvaluation"] = CUMULATIVE
    return obj


def audit(cls):
    prompts = [x["prompt"]["es"] for a in cls["pools"].values() for x in a]
    feedback = [x["origin"]["feedback"]["es"] for a in cls["pools"].values() for x in a]
    assert len(prompts) == len(set(prompts)) and len(feedback) == len(set(feedback))
    assert max(map(len, prompts)) <= 90
    assert len({x["format"] for a in cls["pools"].values() for x in a}) >= 4

    def norm(value):
        return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))

    def selected(item):
        if item["format"] in {"elegir", "escuchar"}:
            return item["choices"][item["answer"]["index"]]["text"]
        return item["answer"].get("text", "")

    teaching_answers = {norm(item["en"]) for item in cls["teaching"]}
    early_answers = {
        norm(selected(item))
        for pool in ("practiceGuided", "practice")
        for item in cls["pools"][pool]
        if selected(item)
    }
    evaluation_answers = {
        norm(selected(item))
        for item in cls["pools"]["evaluation"]
        if selected(item)
    }
    # Reserved evaluation evidence cannot repeat a complete teaching or early answer.
    assert not evaluation_answers & teaching_answers
    assert not evaluation_answers & early_answers

    # Keep known distractor failure modes out of regenerated drafts.
    forbidden = ("charge the group", "plug the music app", "delete the phone", "delete the battery icon")
    for item in (x for pool in cls["pools"].values() for x in pool):
        for choice in item.get("choices", []):
            assert not any(fragment in choice["text"].casefold() for fragment in forbidden)

    expected_routes = {
        "en.n2.class-86": {"e01": ("t03", "r02"), "e02": ("t04", "r03"), "e03": ("t02", "r01"), "e04": ("t03", "r02")},
        "en.n2.class-88": {"e01": ("t05", "r01"), "e03": ("t04", "r01"), "e04": ("t03", "r02")},
        "en.n2.class-89": {"e02": ("t06", "r03"), "e03": ("t06", "r03"), "e04": ("t04", "r02")},
        "en.n2.class-90": {"e01": ("t05", "r03"), "e02": ("t05", "r02"), "e04": ("t06", "r01")},
    }
    base_item_id = cls["id"].replace("class-", "c")
    for suffix, (reteach, review) in expected_routes.get(cls["id"], {}).items():
        route = cls["remediationMap"][f"{base_item_id}.{suffix}"]
        assert route["reteach"].endswith(reteach) and route["review"].endswith(review)

    if cls["id"] == "en.n2.class-87":
        r02 = cls["pools"]["review"][1]
        assert norm(r02["origin"]["text"]) != norm(r02["answer"]["text"])
        e02 = cls["pools"]["evaluation"][1]
        assert e02["format"] == "elegir"
        assert "url" in e02["prompt"]["es"].casefold()
        assert e02["choices"][e02["answer"]["index"]]["text"] == "The link"
    if cls["id"] == "en.n2.class-86":
        e01 = cls["pools"]["evaluation"][0]
        e03 = cls["pools"]["evaluation"][2]
        e04 = cls["pools"]["evaluation"][3]
        assert norm(selected(e01)) not in {norm(cls["teaching"][0]["en"]), norm(selected(cls["pools"]["practiceGuided"][0]))}
        assert norm(selected(e03)) != norm(cls["teaching"][1]["en"])
        assert norm(e04["origin"]["audio"]) != norm(cls["teaching"][4]["en"])
        assert cls["teaching"][2]["en"] == "Tap the app icon to open it."
        assert cls["pools"]["review"][1]["answer"]["text"] == "icon"
        assert "calendar" in norm(selected(e01))
        assert cls["remediationMap"]["en.n2.c86.e01"]["reteach"].endswith("t03")
    if cls["id"] == "en.n2.class-87":
        e02 = cls["pools"]["evaluation"][1]
        assert "url" in e02["prompt"]["es"].casefold()
        assert e02["choices"][e02["answer"]["index"]]["text"] == "The link"
    if cls["id"] == "en.n2.class-88":
        e01 = cls["pools"]["evaluation"][0]
        e03 = cls["pools"]["evaluation"][2]
        e04 = cls["pools"]["evaluation"][3]
        assert norm(selected(e01)) != norm(cls["teaching"][0]["en"])
        assert norm(selected(e03)) != norm(cls["teaching"][1]["en"])
        assert "charge" in norm(e04["origin"]["audio"])
        assert "charge" in norm(e04["origin"]["audio"])
        assert norm(e04["origin"]["audio"]) != norm(cls["teaching"][4]["en"])
        assert "battery is low" in norm(cls["teaching"][2]["en"])
        assert "charge the phone" in norm(cls["teaching"][2]["en"])
        assert cls["remediationMap"]["en.n2.c88.e01"]["reteach"].endswith("t05")
        assert "Wi-Fi signal is weak" in cls["pools"]["evaluation"][0]["choices"][0]["text"]
    if cls["id"] == "en.n2.class-89":
        e04 = cls["pools"]["evaluation"][3]
        assert norm(e04["origin"]["audio"]) != norm(cls["teaching"][4]["en"])
        assert "support chat" in norm(cls["teaching"][5]["en"])
        assert cls["remediationMap"]["en.n2.c89.e02"]["reteach"].endswith("t06")
        assert cls["remediationMap"]["en.n2.c89.e03"]["reteach"].endswith("t06")
        assert "calendar icon" in norm(cls["pools"]["evaluation"][2]["answer"]["text"])
        assert norm(cls["pools"]["evaluation"][2]["answer"]["text"]) != norm(cls["teaching"][5]["en"])
    if cls["id"] == "en.n2.class-90":
        t05 = cls["teaching"][4]["en"]
        e02 = cls["pools"]["evaluation"][1]
        e03 = cls["pools"]["evaluation"][2]
        e04 = cls["pools"]["evaluation"][3]
        r03 = cls["pools"]["review"][2]
        assert {norm(t05), norm(e03["answer"]["text"]), norm(r03["answer"]["text"])}.__len__() == 3
        for phrase in ("turn on", "open", "group", "time", "link", "reply"):
            assert phrase in norm(e03["answer"]["text"])
            assert phrase in norm(r03["answer"]["text"])
        assert "battery" in norm(t05) and "connect the charger" in norm(t05)
        assert "call app" in norm(e03["answer"]["text"]) and "frozen" in norm(e03["answer"]["text"]) and "restart" in norm(e03["answer"]["text"])
        assert "signal is weak" in norm(r03["answer"]["text"]) and "router" in norm(r03["answer"]["text"])
        assert "redacta el diálogo" in e03["prompt"]["es"].casefold()
        assert "Enciende" in e03["origin"]["text"] and "Lista" in r03["origin"]["text"]
        assert "reply" in e02["answer"]["accepted"] and "respond" in e02["answer"]["accepted"]
        assert cls["pools"]["review"][1]["answer"]["accepted"] == ["reply", "respond"]
        assert cls["teaching"][5]["en"] == "If the meeting app is frozen, close it and restart the phone."
        assert cls["remediationMap"]["en.n2.c90.e04"]["reteach"].endswith("t06")
        assert "restart the tablet" in norm(e04["origin"]["audio"])
        assert norm(e04["origin"]["audio"]) != norm(cls["teaching"][5]["en"])
        assert not ("link" in norm(e04["origin"]["audio"]) and "cable" in norm(e04["origin"]["audio"]))
        assert norm(selected(cls["pools"]["evaluation"][0])) != norm(cls["teaching"][0]["en"])
        assert norm(e04["origin"]["audio"]) != norm(cls["teaching"][2]["en"])
        assert norm(e04["origin"]["audio"]) != norm(cls["pools"]["practice"][0]["answer"]["text"])


def write_class(number):
    cls = build_class(number); audit(cls)
    path = OUT / f"class-{number:02d}.json"
    path.write_text(json.dumps(cls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)


def write_bundle():
    classes = [json.loads((OUT / f"class-{n:02d}.json").read_text(encoding="utf-8")) for n in range(86, 91)]
    for cls in classes: audit(cls)
    objectives = [x for cls in classes for x in cls["objectives"]["es"]]
    assert len(objectives) == len(set(objectives))
    bundle = {"schema": "onelingo.editorial.class-bundle.v1", "course": "en", "level": 2, "scale": SCALE, "status": "shadow", "runtimeAi": False, "classes": classes, "selectionPolicy": {"deterministic": True}, "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]}}
    (OUT / "bundle-86-90.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT / "bundle-86-90.json")


def main():
    parser = argparse.ArgumentParser(); group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--class-number", type=int, choices=range(86, 91)); group.add_argument("--bundle", action="store_true")
    args = parser.parse_args(); write_bundle() if args.bundle else write_class(args.class_number)


if __name__ == "__main__":
    main()
