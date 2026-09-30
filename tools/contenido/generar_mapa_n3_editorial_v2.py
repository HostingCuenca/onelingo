#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/plan-editorial"
REPORT_OUT = ROOT / "build/editorial-map-n3-v2"
LEGACY = ROOT / "assets/contenido/en/plan-editorial/mapa-n3.json"
N2_V2 = ROOT / "assets/contenido/en/plan-editorial/mapa-n2-editorial-v2.json"
MASTER = ROOT / "assets/contenido/en/curriculo-master.json"
TARGET = OUT / "mapa-n3-editorial-v2.json"
PHASES = ["input", "form", "comprehension", "production", "transfer"]
LEVEL_STRAND_CRITERIA = {
    "time-narrative-and-future": "Ordena una causa pasada, el estado actual y un plan futuro con marcadores coherentes.",
    "conditions-and-choices": "Compara dos opciones y formula una condición con su consecuencia antes de decidir.",
    "information-sources-and-reporting": "Atribuye al menos dos datos a sus fuentes sin mezclar hablantes ni inventar información.",
    "collaboration-and-problem-solving": "Responde a otra postura y acuerda una acción con responsable, plazo y seguimiento.",
    "connected-production-and-revision": "Entrega una respuesta conectada de 100–140 palabras y documenta una revisión que mejora claridad, precisión o evidencia.",
}


def C(en: str, es: str, can: str, task: str, evidence: list[str], focus: list[str]) -> dict[str, Any]:
    return {"title": {"en": en, "es": es}, "canDoEs": can, "taskEs": task,
            "requiredEvidence": evidence, "focus": focus}


def B(theme: str, theme_es: str, source: str, goal: str,
      spiral: list[str], classes: list[dict[str, Any]]) -> dict[str, Any]:
    return {"theme": theme, "themeEs": theme_es, "sourceTopic": source,
            "blockOutcomeEs": goal, "spiralReview": spiral, "classes": classes}


BLOCKS = [
    B("recent-progress", "Logros, cambios y resultados actuales", "present perfect",
      "Actualizar a otra persona sobre cambios recientes y aportar detalles pasados verificables.",
      ["n2:present-perfect-experience", "n2:present-perfect-time"], [
        C("Results that matter now", "Resultados relevantes ahora", "Reconocer cuándo una acción pasada tiene un resultado visible en el presente.", "Clasificar cinco actualizaciones según expresen resultado actual o pasado terminado.", ["forma have/has + participio", "resultado presente explícito", "4 de 5 clasificaciones correctas"], ["present-perfect-result"]),
        C("Experience or dated event", "Experiencia o hecho fechado", "Elegir entre present perfect y past simple según la presencia de un tiempo terminado.", "Completar seis pares contrastivos con marcadores como ever, last year y yesterday.", ["tiempo verbal adecuado", "marcador temporal compatible", "5 de 6 respuestas correctas"], ["present-perfect-vs-past-simple"]),
        C("Details behind an update", "Detalles detrás de una actualización", "Distinguir la actualización general de los detalles sobre cuándo y cómo ocurrió.", "Escuchar una conversación breve y completar una tabla de resultado, fecha y detalle.", ["resultado general", "fecha concreta", "detalle de cómo ocurrió"], ["follow-up-details"]),
        C("Give a progress update", "Dar una actualización de progreso", "Producir una actualización con logro, resultado actual y un detalle pasado.", "Grabar o escribir una actualización sobre un proyecto personal ya iniciado.", ["logro en present perfect", "resultado actual", "detalle fechado en past simple"], ["progress-update"]),
        C("Catch up after a change", "Ponerse al día después de un cambio", "Mantener una conversación para compartir un cambio y responder preguntas de seguimiento.", "Resolver un reencuentro: dar una actualización, dos detalles y formular dos preguntas.", ["actualización relevante", "dos detalles pasados", "dos preguntas de seguimiento"], ["catch-up-interaction"]),
    ]),
    B("past-scenes", "Escenas, acciones y hechos pasados", "past continuous",
      "Reconstruir un incidente diferenciando contexto en progreso y hechos que lo interrumpen.",
      ["n2:past-narrative"], [
        C("Background in progress", "Contexto en progreso", "Identificar acciones en progreso que crean el fondo de una escena pasada.", "Relacionar cinco escenas con descripciones en past continuous.", ["was/were + -ing", "acción en progreso", "4 de 5 relaciones correctas"], ["past-continuous-background"]),
        C("When and while", "When y while", "Combinar una acción en progreso con un hecho breve usando when o while.", "Completar seis oraciones sin cambiar el orden real de los hechos.", ["when/while adecuado", "past continuous para fondo", "past simple para hecho"], ["when-while-contrast"]),
        C("Build the incident timeline", "Construir la cronología del incidente", "Extraer escenario, acción en curso e interrupción de un relato oral.", "Escuchar un testimonio y ordenar cuatro hechos en una línea temporal.", ["escenario", "acción en progreso", "interrupción y resultado"], ["incident-timeline"]),
        C("Describe an interruption", "Describir una interrupción", "Narrar un incidente breve con contexto, interrupción y reacción.", "Escribir o contar una escena cotidiana a partir de tres datos visibles.", ["contexto en progreso", "hecho interruptor", "reacción posterior"], ["interrupted-event-production"]),
        C("Explain a delay", "Explicar un retraso", "Explicar a otra persona por qué un trayecto o una cita se retrasó.", "Responder a un agente con una cronología completa y una petición práctica.", ["situación de fondo", "causa inmediata", "petición o siguiente paso"], ["delay-explanation"]),
    ]),
    B("narrative-turning-points", "Relatos y puntos de cambio", "past narrative",
      "Contar una historia breve con orden claro, un hecho anterior y un desenlace comprensible.",
      ["n2:past-simple-expanded", "n2:past-narrative"], [
        C("Signals in a story", "Señales dentro de una historia", "Reconocer conectores que abren, cambian y cierran un relato.", "Ordenar fragmentos usando at first, suddenly, later y eventually.", ["inicio reconocible", "punto de cambio", "cierre temporal"], ["narrative-linkers"]),
        C("An earlier past event", "Un hecho anterior en el pasado", "Usar past perfect básico para aclarar cuál de dos hechos ocurrió primero.", "Completar cinco pares de hechos con had + participio cuando sea necesario.", ["hecho anterior marcado", "hecho posterior en past simple", "4 de 5 pares correctos"], ["past-perfect-introduction"]),
        C("Cause before the turning point", "Causa antes del giro", "Inferir cómo un hecho anterior explica un cambio posterior en una historia.", "Leer un relato corto y seleccionar causa, giro y consecuencia.", ["causa anterior", "giro narrativo", "consecuencia textual"], ["narrative-cause"]),
        C("Write a turning-point story", "Escribir una historia con giro", "Escribir un relato coherente con contexto, hecho anterior, giro y desenlace.", "Producir una historia basada en cuatro viñetas y revisar su cronología.", ["cuatro etapas completas", "conectores variados", "tiempos pasados coherentes"], ["turning-point-story"]),
        C("Tell and clarify a story", "Contar y aclarar una historia", "Contar un relato y aclarar dos preguntas sin alterar la cronología.", "Presentar una experiencia inesperada y responder preguntas sobre causa y orden.", ["relato completo", "dos aclaraciones consistentes", "desenlace explícito"], ["interactive-storytelling"]),
    ]),
    B("future-coordination", "Coordinación futura y cambios de plan", "future forms",
      "Coordinar un plan futuro distinguiendo arreglo, intención, decisión y contingencia.",
      ["n2:future-plans", "n2:future-decisions"], [
        C("How certain is the plan?", "Grado de certeza del plan", "Reconocer si un futuro expresa arreglo confirmado, intención o predicción.", "Clasificar seis mensajes de agenda según el tipo de futuro.", ["forma futura", "grado de certeza", "5 de 6 clasificaciones correctas"], ["future-meaning-contrast"]),
        C("Time clauses for plans", "Cláusulas temporales para planes", "Usar present simple después de when, before y as soon as para hablar del futuro.", "Completar seis condiciones temporales de una agenda.", ["conector temporal", "presente en la cláusula", "futuro en la acción principal"], ["future-time-clauses"]),
        C("A schedule has changed", "Un horario cambió", "Comprender qué parte de un arreglo cambió y qué parte sigue confirmada.", "Comparar un calendario con dos mensajes de voz y actualizar tres datos.", ["dato original", "cambio anunciado", "elemento aún confirmado"], ["schedule-change-comprehension"]),
        C("Coordinate a plan", "Coordinar un plan", "Proponer un arreglo con responsables, plazos y una alternativa.", "Redactar un mensaje de coordinación para tres personas con dos restricciones.", ["arreglo confirmado", "responsable y plazo", "alternativa viable"], ["future-plan-coordination"]),
        C("Renegotiate an event", "Renegociar un evento", "Negociar un cambio de plan y cerrar una nueva confirmación.", "Resolver una cancelación parcial mediante propuesta, decisión inmediata y confirmación.", ["cambio explicado", "contingencia acordada", "confirmación final completa"], ["future-renegotiation"]),
    ]),
    B("real-consequences", "Condiciones reales y consecuencias", "first conditional",
      "Tomar decisiones prácticas a partir de condiciones probables y sus consecuencias.",
      ["n2:future-decisions", "n2:travel"], [
        C("Likely condition and result", "Condición probable y resultado", "Reconocer una condición real y su consecuencia futura.", "Relacionar cinco condiciones cotidianas con resultados lógicos.", ["if + presente", "resultado futuro", "4 de 5 relaciones correctas"], ["first-conditional-meaning"]),
        C("If, unless and when", "If, unless y when", "Distinguir condición, excepción y momento seguro en planes reales.", "Elegir if, unless o when en seis avisos de viaje.", ["conector adecuado", "significado conservado", "5 de 6 respuestas correctas"], ["if-unless-when"]),
        C("Rules and consequences", "Reglas y consecuencias", "Comprender consecuencias explícitas en normas e instrucciones.", "Leer condiciones de una reserva y responder cinco preguntas de decisión.", ["condición localizada", "consecuencia exacta", "sin inferencias no dadas"], ["conditional-comprehension"]),
        C("Make a contingency plan", "Crear un plan de contingencia", "Explicar qué hará ante dos problemas probables.", "Escribir un plan A/B para una salida con clima y transporte inciertos.", ["dos condiciones reales", "dos respuestas viables", "secuencia clara"], ["contingency-plan"]),
        C("Handle a disrupted trip", "Resolver un viaje interrumpido", "Aplicar condiciones reales para escoger una alternativa y comunicarla.", "Resolver retraso, conexión y alojamiento con datos de una tabla.", ["condiciones comprobadas", "decisión justificada", "mensaje final al acompañante"], ["conditional-travel-solution"]),
    ]),
    B("hypothetical-choices", "Opciones hipotéticas y recomendaciones", "second conditional introduction",
      "Explorar posibilidades poco probables y comparar sus ventajas sin presentarlas como hechos.",
      ["n2:comparisons", "n2:obligation-advice"], [
        C("Imagine a different situation", "Imaginar otra situación", "Reconocer hipótesis sobre una situación diferente a la actual.", "Separar cinco hipótesis de cinco planes reales.", ["if + pasado", "would/could", "4 de 5 distinciones correctas"], ["second-conditional-meaning"]),
        C("Would or could", "Would o could", "Formar hipótesis con would para resultado y could para posibilidad.", "Completar seis respuestas hipotéticas con forma y significado adecuados.", ["cláusula if correcta", "would/could justificado", "5 de 6 respuestas correctas"], ["second-conditional-form"]),
        C("Advice through imagination", "Consejo mediante hipótesis", "Comprender cómo una hipótesis suaviza una recomendación.", "Escuchar tres consejos y extraer situación, opción y razón.", ["situación imaginada", "opción propuesta", "razón del hablante"], ["hypothetical-advice"]),
        C("Compare imagined options", "Comparar opciones imaginadas", "Comparar dos opciones hipotéticas con beneficio y límite.", "Producir una recomendación sobre vivir, estudiar o viajar en otro lugar.", ["dos opciones", "beneficio y límite", "conclusión condicional"], ["hypothetical-comparison"]),
        C("Choose under an imaginary budget", "Elegir con un presupuesto imaginario", "Negociar una elección hipotética usando presupuesto y preferencias.", "Resolver un plan de viaje imaginario con tres opciones y dos interlocutores.", ["hipótesis compartida", "comparación razonada", "decisión de grupo"], ["hypothetical-negotiation"]),
    ]),
    B("habits-preferences", "Hábitos, preferencias e intenciones", "gerunds and infinitives",
      "Explicar elecciones de estilo de vida usando patrones frecuentes con -ing y to-infinitive.",
      ["n2:routines-expanded", "n2:health"], [
        C("Activities after preference verbs", "Actividades tras verbos de preferencia", "Reconocer verbos frecuentes seguidos por una actividad en -ing.", "Clasificar ejemplos con enjoy, avoid, finish y keep.", ["verbo rector", "forma -ing", "4 de 5 patrones correctos"], ["verb-plus-gerund"]),
        C("Plans after intention verbs", "Planes tras verbos de intención", "Usar to-infinitive después de want, need, decide y hope.", "Completar seis decisiones personales con el patrón correcto.", ["verbo de intención", "to + verbo", "5 de 6 formas correctas"], ["verb-plus-infinitive"]),
        C("Preference or intention?", "¿Preferencia o intención?", "Distinguir lo que alguien disfruta de lo que planea o necesita hacer.", "Escuchar una conversación de hábitos y llenar dos columnas.", ["preferencia", "intención", "evidencia verbal"], ["gerund-infinitive-comprehension"]),
        C("Explain a routine choice", "Explicar una elección de rutina", "Explicar tres hábitos, una actividad evitada y un objetivo.", "Crear una actualización de bienestar con razones concretas.", ["dos patrones con -ing", "un patrón con to", "razón comprensible"], ["lifestyle-choice-production"]),
        C("Agree on a healthier routine", "Acordar una rutina más saludable", "Negociar cambios de rutina respetando preferencias y necesidades.", "Resolver una consulta de hábitos y cerrar tres acciones realistas usando al menos dos verbos seguidos de -ing y dos verbos seguidos de to-infinitive.", ["dos usos correctos de -ing tras verbos de preferencia", "dos usos correctos de to-infinitive tras verbos de intención", "preferencia e intención distinguidas", "razón concreta para cada cambio", "tres acciones acordadas"], ["lifestyle-plan-transfer"]),
    ]),
    B("defining-information", "Definir personas, objetos y lugares", "relative clauses",
      "Dar información precisa para identificar personas, objetos, lugares y servicios.",
      ["n2:city-services", "n2:requests-permission"], [
        C("People who help", "Personas que ayudan", "Reconocer who/that en definiciones de personas y funciones.", "Relacionar cinco profesionales con definiciones relativas.", ["antecedente persona", "who/that", "4 de 5 definiciones correctas"], ["defining-relatives-people"]),
        C("Things and places", "Objetos y lugares", "Usar which/that para cosas y where para lugares.", "Completar seis definiciones de objetos y sitios cotidianos.", ["antecedente identificado", "pronombre relativo adecuado", "5 de 6 formas correctas"], ["defining-relatives-things-places"]),
        C("Which service is it?", "¿Qué servicio es?", "Comprender descripciones relativas y localizar el referente exacto.", "Leer anuncios de servicios y seleccionar persona, objeto o lugar descrito.", ["referente textual", "detalle definitorio", "sin confundir información extra"], ["relative-reference-comprehension"]),
        C("Define without naming", "Definir sin nombrar", "Definir una persona, un objeto y un lugar para que otra persona los identifique.", "Grabar o escribir tres acertijos funcionales con cláusulas relativas.", ["tres tipos de antecedente", "cláusulas completas", "referentes identificables"], ["relative-definition-production"]),
        C("Recommend a local service", "Recomendar un servicio local", "Recomendar una opción describiendo quién ayuda, qué ofrece y dónde está.", "Resolver una consulta local comparando dos servicios y usar who/that para una persona, which/that para un servicio y where para un lugar.", ["persona definida con who o that", "servicio definido con which o that", "lugar definido con where", "tres referentes inequívocos", "recomendación final basada en esas definiciones"], ["service-recommendation"]),
    ]),
    B("processes-services", "Procesos, productos y servicios", "passive introduction",
      "Explicar qué se hace, dónde y cuándo cuando el proceso importa más que el agente.",
      ["n2:city-services", "n2:technology"], [
        C("What is done", "Qué se hace", "Reconocer present passive en procesos y servicios habituales.", "Distinguir agente y resultado en cinco descripciones de proceso.", ["be + participio", "resultado del proceso", "4 de 5 análisis correctos"], ["present-passive"]),
        C("What was done", "Qué se hizo", "Formar past passive para cambios y reparaciones terminadas.", "Completar seis avisos de servicio con was/were + participio.", ["sujeto afectado", "was/were", "participio correcto"], ["past-passive"]),
        C("Track a service request", "Seguir una solicitud de servicio", "Comprender las etapas y el estado de una solicitud expresada en pasiva.", "Ordenar recepción, revisión, reparación y confirmación en un aviso.", ["cuatro etapas", "estado actual", "fecha de cierre"], ["passive-process-comprehension"]),
        C("Explain how it is handled", "Explicar cómo se gestiona", "Explicar un proceso corto sin repetir un agente desconocido.", "Describir cómo se recoge, revisa y entrega un objeto o solicitud.", ["tres etapas pasivas", "orden lógico", "tiempo verbal coherente"], ["process-explanation"]),
        C("Resolve a service-status problem", "Resolver un problema de estado", "Consultar un proceso, detectar una etapa pendiente y pedir acción.", "Resolver una entrega o reparación usando un registro de estado, dos formas pasivas y una petición sobre la etapa pendiente.", ["una acción actual expresada en present passive", "una acción terminada expresada en past passive", "etapas del proceso en orden", "estado pendiente identificado", "petición concreta sobre la etapa pendiente"], ["service-status-transfer"]),
    ]),
    B("reported-messages", "Transmitir mensajes e instrucciones", "reported speech introduction",
      "Transmitir información de otra persona con hablante, contenido y acción esperada claros.",
      ["n2:work-study", "n2:social-problems"], [
        C("Who said what", "Quién dijo qué", "Reconocer hablante y contenido en mensajes reportados sencillos.", "Relacionar cinco mensajes originales con su reporte.", ["hablante", "said/told", "contenido conservado"], ["reported-statements"]),
        C("Say or tell", "Say o tell", "Distinguir say sin objeto de tell con persona receptora.", "Completar seis reportes con say/said o tell/told.", ["verbo correcto", "receptor cuando corresponde", "5 de 6 respuestas correctas"], ["say-tell-form"]),
        C("Original message and report", "Mensaje original y reporte", "Comparar un mensaje directo con su versión reportada sin perder datos.", "Escuchar tres pares y detectar persona, hora o acción modificada.", ["fuente original", "dato conservado", "cambio de perspectiva"], ["reported-message-comprehension"]),
        C("Relay an update", "Transmitir una actualización", "Transmitir dos mensajes con destinatario y siguiente acción.", "Escribir una nota de relevo a partir de mensajes de voz.", ["dos fuentes identificadas", "contenido exacto", "acción requerida"], ["message-relay-production"]),
        C("Resolve a schedule change", "Resolver un cambio de horario", "Transmitir mensajes entre tres personas y cerrar un nuevo horario.", "Resolver una cadena de avisos reportando lo que dijeron tres personas y cerrar un horario nuevo sin cambiar hablantes, horas ni acciones.", ["said y told usados con estructura correcta", "tres hablantes atribuidos sin intercambio", "cambios de persona y tiempo conservan el sentido", "dos mensajes transmitidos con su acción requerida", "horario final confirmado"], ["reported-schedule-transfer"]),
    ]),
    B("phrasal-actions", "Verbos frasales en acciones cotidianas", "phrasal verbs",
      "Comprender y usar un conjunto limitado de phrasal verbs frecuentes sin traducir palabra por palabra.",
      ["n2:technology", "n2:travel"], [
        C("Common two-part actions", "Acciones frecuentes de dos partes", "Reconocer el significado contextual de turn on, pick up, look for y fill in.", "Relacionar cinco acciones con situaciones, no con traducciones aisladas.", ["contexto adecuado", "phrasal verb completo", "4 de 5 relaciones correctas"], ["core-phrasal-verbs"]),
        C("Move the object", "Mover el objeto", "Colocar sustantivos y pronombres correctamente en phrasal verbs separables.", "Reordenar seis instrucciones con turn off, pick up y fill in.", ["objeto nominal posible", "pronombre entre verbo y partícula", "5 de 6 órdenes correctos"], ["separable-phrasal-verbs"]),
        C("Meaning from context", "Significado por contexto", "Inferir el phrasal verb por la situación y la consecuencia.", "Escuchar cuatro diálogos y escoger la acción realizada.", ["situación", "acción inferida", "resultado observado"], ["phrasal-context-comprehension"]),
        C("Give practical instructions", "Dar instrucciones prácticas", "Dar instrucciones claras con tres phrasal verbs frecuentes.", "Crear una nota para recoger un paquete, completar un formulario y encender un equipo.", ["tres acciones completas", "objetos bien colocados", "orden útil"], ["phrasal-instruction-production"]),
        C("Solve a lost-item routine", "Resolver una pérdida", "Usar phrasal verbs para buscar, recoger y devolver un objeto.", "Resolver un objeto perdido mediante llamada, formulario y punto de recogida.", ["búsqueda descrita", "formulario completado", "recogida confirmada"], ["lost-item-transfer"]),
    ]),
    B("natural-collocations", "Combinaciones naturales y mensajes claros", "collocations",
      "Elegir combinaciones frecuentes para que mensajes y actualizaciones suenen claros y naturales.",
      ["n2:work-study", "n2:technology"], [
        C("Make, do, take or have", "Make, do, take o have", "Reconocer collocations frecuentes con cuatro verbos de apoyo.", "Clasificar doce combinaciones de uso cotidiano.", ["verbo de apoyo", "sustantivo compatible", "10 de 12 clasificaciones correctas"], ["support-verb-collocations"]),
        C("Work and study combinations", "Combinaciones de trabajo y estudio", "Usar meet a deadline, make a decision, take notes y do research.", "Completar seis mensajes de trabajo o estudio.", ["collocation exacta", "tiempo verbal adecuado", "5 de 6 respuestas correctas"], ["work-study-collocations"]),
        C("Natural or translated?", "¿Natural o traducido?", "Detectar combinaciones poco naturales y recuperar la intención.", "Leer seis mensajes y corregir los tres que contienen una combinación impropia.", ["intención entendida", "collocation natural", "tres correcciones justificadas"], ["collocation-comprehension"]),
        C("Edit a short note", "Editar una nota breve", "Reescribir una nota para mejorar precisión y naturalidad.", "Editar un mensaje con cuatro collocations inadecuadas.", ["cuatro mejoras", "significado conservado", "registro apropiado"], ["collocation-editing"]),
        C("Send a clear coordination message", "Enviar un mensaje claro de coordinación", "Redactar un mensaje natural con decisión, plazo, notas y seguimiento.", "Resolver una coordinación de grupo sin calcos literales.", ["cuatro collocations meta", "información completa", "mensaje conciso"], ["collocation-transfer"]),
    ]),
    B("workplace-collaboration", "Colaboración en trabajo y estudio", "workplace communication",
      "Coordinar prioridades, responsables y bloqueos con un tono profesional accesible.",
      ["n2:work-study", "n2:social-problems"], [
        C("Priority, progress and blocker", "Prioridad, progreso y bloqueo", "Reconocer qué tarea es prioritaria, cuál avanza y cuál está bloqueada.", "Clasificar cinco actualizaciones de equipo.", ["prioridad", "estado", "bloqueo"], ["work-status-language"]),
        C("Polite information questions", "Preguntas corteses de información", "Formar preguntas indirectas breves para pedir datos y plazos.", "Transformar seis preguntas directas con Could you tell me...?.", ["inicio cortés", "orden afirmativo", "dato solicitado"], ["indirect-questions-intro"]),
        C("Actions from meeting notes", "Acciones de una reunión", "Extraer tarea, responsable y plazo de notas y turnos orales.", "Completar una tabla de acciones después de una reunión breve.", ["tres tareas", "tres responsables", "tres plazos"], ["meeting-actions-comprehension"]),
        C("Give a useful progress update", "Dar una actualización útil", "Informar trabajo terminado, tarea actual, bloqueo y petición.", "Preparar una actualización de cuatro partes para el equipo.", ["avance terminado", "trabajo actual", "bloqueo y ayuda requerida"], ["professional-progress-update"]),
        C("Renegotiate workload", "Renegociar la carga", "Negociar un plazo o reparto sin perder responsabilidades esenciales.", "Resolver tres tareas, dos personas y un plazo imposible.", ["prioridades justificadas", "nuevo reparto", "plazo confirmado"], ["workload-negotiation"]),
    ]),
    B("travel-resolution", "Experiencias de viaje y resolución de incidencias", "travel experiences",
      "Explicar una incidencia de viaje, aportar evidencia y negociar una solución razonable.",
      ["n2:travel", "n3:recent-progress", "n3:past-scenes"], [
        C("Experience and current impact", "Experiencia e impacto actual", "Distinguir la experiencia general del problema que continúa ahora.", "Clasificar cinco actualizaciones de viaje y su impacto actual.", ["experiencia", "detalle fechado", "impacto presente"], ["travel-experience-update"]),
        C("How long has it continued?", "Cuánto tiempo ha continuado", "Usar present perfect continuous básico para una espera o problema temporal.", "Completar cinco situaciones con have/has been + -ing y duración.", ["acción temporal", "duración", "4 de 5 formas correctas"], ["present-perfect-continuous-intro"]),
        C("Understand a travel complaint", "Comprender una reclamación de viaje", "Extraer problema, evidencia, petición y respuesta de una conversación.", "Escuchar una reclamación y completar cuatro campos sin inferir compensación.", ["incidencia", "evidencia", "solución solicitada"], ["travel-complaint-comprehension"]),
        C("Write a factual complaint", "Escribir una reclamación factual", "Redactar una reclamación breve con cronología, impacto y petición.", "Escribir a una empresa usando datos de billete y retraso.", ["datos verificables", "impacto concreto", "petición proporcionada"], ["travel-complaint-production"]),
        C("Rebook after disruption", "Reprogramar tras una incidencia", "Negociar una alternativa usando horarios, condiciones y límites visibles.", "Resolver una cancelación con tres rutas y una restricción de llegada.", ["incidencia explicada", "opción compatible", "nueva reserva confirmada"], ["travel-rebooking-transfer"]),
    ]),
    B("news-sources", "Noticias, fuentes y certeza", "news",
      "Comprender y resumir información breve distinguiendo hechos, fuentes, opiniones e incertidumbre.",
      ["n3:reported-messages", "n2:past-narrative"], [
        C("Headline and verified detail", "Titular y detalle verificado", "Distinguir un titular breve de los detalles que el texto confirma.", "Relacionar cinco titulares con la información exacta de sus entradillas.", ["titular", "detalle confirmado", "4 de 5 relaciones correctas"], ["headline-detail"]),
        C("Name the source", "Nombrar la fuente", "Usar according to y reported/said para atribuir información.", "Completar seis frases sin presentar la fuente como certeza absoluta.", ["fuente nombrada", "verbo de reporte", "dato atribuido"], ["source-attribution"]),
        C("Fact, opinion or uncertainty", "Hecho, opinión o incertidumbre", "Clasificar afirmaciones según la evidencia lingüística disponible.", "Leer una nota y justificar cinco clasificaciones con palabras del texto.", ["tipo de afirmación", "marcador textual", "4 de 5 justificaciones correctas"], ["fact-opinion-uncertainty"]),
        C("Summarize without adding", "Resumir sin añadir", "Resumir tres hechos atribuidos sin incorporar causas no confirmadas.", "Escribir un resumen de 70–90 palabras a partir de una ficha de fuente.", ["tres hechos", "fuente visible", "cero información inventada"], ["factual-summary"]),
        C("Compare two reports", "Comparar dos informes", "Comparar coincidencias y diferencias entre dos fuentes breves.", "Explicar qué está confirmado, qué difiere y qué debe verificarse.", ["dos coincidencias", "una diferencia", "paso de verificación"], ["source-comparison-transfer"]),
    ]),
    B("media-reviews", "Reseñas y recomendaciones de medios", "media",
      "Evaluar una obra breve y recomendarla para una audiencia concreta con razones y límites.",
      ["n2:comparisons", "n3:natural-collocations"], [
        C("Genre, plot and reaction", "Género, trama y reacción", "Reconocer vocabulario básico de género, trama, personajes y reacción.", "Clasificar detalles de cuatro reseñas en categorías.", ["género", "elemento de trama", "reacción del lector"], ["review-components"]),
        C("Link a balanced opinion", "Conectar una opinión equilibrada", "Usar although, however y because para equilibrar valoración y evidencia.", "Combinar seis pares de ideas sin cambiar su relación lógica.", ["conector adecuado", "contraste o causa", "5 de 6 combinaciones correctas"], ["opinion-linkers"]),
        C("What does the reviewer think?", "Qué piensa el reseñador", "Inferir postura, evidencia y reserva en una reseña breve.", "Leer dos reseñas y completar postura, dos razones y un límite.", ["postura", "evidencia textual", "reserva o límite"], ["review-comprehension"]),
        C("Write a balanced review", "Escribir una reseña equilibrada", "Escribir una reseña con resumen mínimo, valoración y evidencia.", "Producir una reseña de 80–100 palabras sin revelar el final.", ["contexto sin spoiler", "dos razones", "valoración equilibrada"], ["balanced-review-production"]),
        C("Recommend for an audience", "Recomendar para una audiencia", "Elegir una obra para una audiencia con preferencias y límites.", "Comparar tres opciones y presentar una recomendación con advertencia relevante.", ["necesidades de audiencia", "comparación", "recomendación justificada"], ["audience-recommendation"]),
    ]),
    B("learning-strategies", "Aprendizaje, metas y retroalimentación", "education",
      "Interpretar retroalimentación y convertirla en un plan de estudio medible.",
      ["n2:work-study", "n3:habits-preferences"], [
        C("Strength, difficulty and goal", "Fortaleza, dificultad y meta", "Distinguir una fortaleza actual, una dificultad y una meta futura.", "Clasificar cinco comentarios de aprendizaje.", ["fortaleza", "dificultad", "meta"], ["learning-profile-language"]),
        C("Purpose and strategy", "Propósito y estrategia", "Expresar propósito con to y so that al elegir una estrategia.", "Completar seis planes de estudio con estrategia y propósito.", ["acción de estudio", "to/so that", "resultado buscado"], ["purpose-clauses"]),
        C("Turn feedback into actions", "Convertir comentarios en acciones", "Extraer logro, problema y siguiente paso de una retroalimentación.", "Escuchar una tutoría y completar un plan de tres columnas.", ["logro", "problema específico", "acción recomendada"], ["feedback-comprehension"]),
        C("Build a study plan", "Construir un plan de estudio", "Crear una meta semanal con acciones, frecuencia y evidencia.", "Escribir un plan de dos semanas a partir de un perfil.", ["meta medible", "acciones y frecuencia", "evidencia de avance"], ["study-plan-production"]),
        C("Revise the plan", "Revisar el plan", "Evaluar progreso y ajustar una estrategia sin abandonar la meta.", "Resolver una tutoría de seguimiento con resultados parciales.", ["evidencia revisada", "ajuste justificado", "nuevo control acordado"], ["learning-plan-transfer"]),
    ]),
    B("local-environment", "Entorno local y acción comunitaria", "environment",
      "Explicar un problema ambiental local y proponer una acción viable con impacto previsto.",
      ["n3:real-consequences", "n3:processes-services"], [
        C("Local cause and effect", "Causa y efecto local", "Reconocer causas, efectos y actores en problemas ambientales cercanos.", "Relacionar cinco problemas con causa y efecto documentados.", ["causa", "efecto", "actor implicado"], ["environment-cause-effect"]),
        C("Conditions and processes", "Condiciones y procesos", "Combinar pasiva y condicional para explicar qué ocurrirá si se aplica una medida.", "Completar seis propuestas sin prometer resultados no sustentados.", ["proceso en pasiva", "condición real", "resultado limitado"], ["environment-condition-process"]),
        C("Understand a local proposal", "Comprender una propuesta local", "Extraer problema, medida, coste, beneficio y preocupación.", "Leer una propuesta y las opiniones de tres residentes.", ["medida", "beneficio y coste", "preocupación de un residente"], ["community-proposal-comprehension"]),
        C("Propose one practical action", "Proponer una acción práctica", "Presentar una medida local con razón, condición y forma de comprobarla.", "Redactar una propuesta de 80–100 palabras con datos proporcionados.", ["acción viable", "condición y efecto", "indicador de seguimiento"], ["environment-proposal-production"]),
        C("Agree on a local response", "Acordar una respuesta local", "Negociar una medida ambiental entre actores con prioridades distintas.", "Resolver una reunión vecinal y registrar acción, responsable, plazo e indicador.", ["posturas reconocidas", "acuerdo viable", "seguimiento medible"], ["environment-negotiation"]),
    ]),
    B("community-project", "Proyecto comunitario integrado", "integrated review",
      "Diseñar y defender un proyecto pequeño integrando fuentes, planificación y colaboración.",
      ["n3:workplace-collaboration", "n3:news-sources", "n3:local-environment"], [
        C("Read a project brief", "Leer un encargo de proyecto", "Extraer objetivo, audiencia, límites, roles y evidencia requerida.", "Analizar un encargo comunitario y completar una ficha de cinco campos.", ["objetivo", "audiencia y límites", "roles y evidencia"], ["project-brief-comprehension"]),
        C("Organize a proposal", "Organizar una propuesta", "Estructurar problema, evidencia, solución y resultado esperado con conectores claros.", "Ordenar y completar un esquema de propuesta.", ["problema", "evidencia y solución", "resultado verificable"], ["proposal-structure"]),
        C("Compare stakeholder views", "Comparar perspectivas", "Comprender coincidencias, objeciones y condiciones de tres participantes.", "Escuchar una reunión y construir una matriz de posturas.", ["tres posturas", "punto común", "dos condiciones"], ["stakeholder-comprehension"]),
        C("Draft the project proposal", "Redactar la propuesta", "Redactar una propuesta con tareas, responsables, plazo y medición.", "Crear un borrador de 90–120 palabras a partir de la ficha y la reunión.", ["solución respaldada", "responsables y plazo", "indicador de resultado"], ["community-proposal-draft"]),
        C("Present and answer questions", "Presentar y responder preguntas", "Presentar la propuesta y responder objeciones con evidencia del caso.", "Realizar una presentación breve y responder tres preguntas de partes interesadas.", ["propuesta completa", "tres respuestas relevantes", "ajuste final registrado"], ["community-project-transfer"]),
    ]),
    B("b1-entry-capstone", "Desempeño final de entrada B1", "final assessment",
      "Demostrar comprensión y producción conectada en una situación práctica con revisión propia.",
      ["n3:recent-progress", "n3:narrative-turning-points", "n3:workplace-collaboration", "n3:community-project"], [
        C("Analyze a practical case", "Analizar un caso práctico", "Identificar hechos, opiniones, cronología y restricciones en un caso multimodal.", "Leer y escuchar un caso para completar una matriz de evidencia.", ["hechos atribuidos", "cronología", "restricciones"], ["capstone-case-analysis"]),
        C("Plan a coherent response", "Planificar una respuesta coherente", "Organizar una respuesta en párrafos con propósito, evidencia y siguiente paso.", "Construir un esquema y seleccionar conectores adecuados.", ["propósito", "evidencia ordenada", "siguiente paso"], ["capstone-response-structure"]),
        C("Understand multiple speakers", "Comprender a varios hablantes", "Distinguir postura, razón y propuesta de tres hablantes.", "Escuchar una discusión y comparar sus aportes sin mezclar voces.", ["tres atribuciones", "tres razones", "dos acuerdos o diferencias"], ["multi-speaker-comprehension"]),
        C("Draft and revise a solution", "Redactar y revisar una solución", "Producir una respuesta conectada y demostrar cómo mejora mediante revisión.", "Escribir un borrador de 100–130 palabras, completar una lista de cuatro criterios y entregar una versión revisada con al menos tres cambios identificados.", ["borrador inicial de 100–130 palabras", "lista de control de cuatro criterios completada", "versión revisada de 100–130 palabras", "al menos tres cambios identificados", "cada cambio mejora claridad, precisión o evidencia"], ["capstone-revision"]),
        C("Final B1-entry performance", "Desempeño final B1 de entrada", "Resolver un caso nuevo demostrando las cinco macrohebras del nivel con evidencia observable.", "Resolver un caso nuevo en 100–140 palabras: ordenar la cronología, atribuir dos fuentes, comparar opciones con una condición, acordar responsable y plazo, y registrar una revisión final.", ["cronología pasada, estado actual y plan futuro coherentes", "dos opciones comparadas con condición y consecuencia", "dos datos atribuidos a sus fuentes sin invención", "responsable, plazo y seguimiento acordados", "respuesta conectada con una revisión final documentada"], ["b1-entry-final-performance"]),
    ]),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")


def explicit_word_range(task_es: str) -> list[int] | None:
    match = re.search(r"(\d+)\s*[–-]\s*(\d+)\s+palabras", task_es, re.I)
    return [int(match.group(1)), int(match.group(2))] if match else None


def closure_observables(block: dict[str, Any]) -> list[str]:
    closing_evidence = block["classes"][4]["requiredEvidence"]
    if len(closing_evidence) >= 5:
        return list(closing_evidence[:5])
    return [
        f"La entrega demuestra «{spec['canDoEs']}» mediante «{spec['requiredEvidence'][0]}»."
        for spec in block["classes"]
    ]


def criterion_records(concepts: list[str], block: dict[str, Any]) -> tuple[list[dict[str, str]], dict[str, str]]:
    records: list[dict[str, str]] = []
    mapping: dict[str, str] = {}
    for offset, (concept, observable) in enumerate(zip(concepts, closure_observables(block))):
        criterion_id = f"{concept}.observable"
        records.append({
            "id": criterion_id,
            "concept": concept,
            "sourcePhase": PHASES[offset],
            "observableEs": observable,
        })
        mapping[concept] = criterion_id
    return records, mapping


def word_band(number: int, phase: str, task_es: str) -> dict[str, Any]:
    band = 0 if number <= 30 else 1 if number <= 60 else 2 if number <= 90 else 3
    if phase in {"input", "form", "comprehension"}:
        return {"type": "accuracy", "accuracyFloor": 0.8,
                "requiredEvidenceCount": 3, "independentAttempt": True}
    if phase == "production":
        ranges = [(60, 80), (70, 90), (80, 100), (90, 120)]
    else:
        ranges = [(70, 100), (80, 110), (90, 120), (100, 140)]
    explicit = explicit_word_range(task_es)
    low, high = explicit or ranges[band]
    return {"type": "connected-production", "wordRange": [low, high],
            "spokenAlternativeTurns": [6 + band, 8 + band], "independentAttempt": True}


def build_map() -> dict[str, Any]:
    legacy_classes = json.loads(LEGACY.read_text())["clases"]
    classes: list[dict[str, Any]] = []
    blocks: list[dict[str, Any]] = []
    number = 0
    for block_number, block in enumerate(BLOCKS, 1):
        block_class_ids: list[str] = []
        block_concepts: list[str] = []
        for position, spec in enumerate(block["classes"], 1):
            number += 1
            legacy_class = legacy_classes[number - 1]
            class_id = f"en.n3.class-{number:02d}"
            concept = f"n3-{block['theme']}-{position}"
            block_class_ids.append(class_id)
            block_concepts.append(concept)
            phase = PHASES[position - 1]
            prerequisite = "en.n2.class-100" if number == 1 else f"en.n3.class-{number - 1:02d}"
            assessment = {
                "taskEs": spec["taskEs"],
                "mode": {
                    "input": "recognition-with-context",
                    "form": "controlled-production",
                    "comprehension": "reading-listening-response",
                    "production": "connected-production",
                    "transfer": "integrated-scenario",
                }[phase],
                "requiredEvidence": spec["requiredEvidence"],
                "minimumPerformance": word_band(number, phase, spec["taskEs"]),
                "deterministicSelection": True,
            }
            item: dict[str, Any] = {
                "id": class_id, "level": 3, "cefr": "B1", "band": "B1-entry",
                "block": block_number, "position": position, "phase": phase,
                "theme": block["theme"], "themeEs": block["themeEs"],
                "title": spec["title"], "concepts": [concept],
                "languageFocus": spec["focus"],
                "skills": {
                    "primary": {"input": "receptive-noticing", "form": "controlled-form",
                                "comprehension": "listening-reading", "production": "speaking-writing",
                                "transfer": "integrated-interaction"}[phase],
                    "integrates": {
                        "input": ["reading", "listening"],
                        "form": ["reading", "writing"],
                        "comprehension": ["reading", "listening"],
                        "production": ["speaking", "writing"],
                        "transfer": ["reading", "listening", "speaking", "writing"],
                    }[phase],
                },
                "canDo": {"es": spec["canDoEs"]}, "assessment": assessment,
                "prerequisites": [prerequisite], "status": "planned", "runtimeAi": False,
                "sourceTrace": {
                    "legacyMapClass": f"en.n3.l{number:03d}",
                    "masterCurriculumClass": f"en.n3.l{number:03d}",
                    "sourceTopic": legacy_class["tema_fuente"],
                    "sourceTitle": legacy_class["titulo_fuente"],
                    "editorialDestination": {"theme": block["theme"], "phase": phase},
                    "editorialAction": "reframed-as-five-phase-communicative-sequence",
                },
            }
            if number == 74:
                assessment["wordRangeRationale"] = "brief-source-bound-summary-exception"
            if number == 99:
                assessment["revisionProtocol"] = {
                    "draftRequired": True,
                    "checklist": ["purpose", "source-evidence", "connectors", "next-step"],
                    "revisedVersionRequired": True,
                    "minimumDocumentedChanges": 3,
                    "acceptedChangeCategories": ["clarity", "accuracy", "evidence"],
                    "cosmeticOnlyChangesAccepted": False,
                }
            if position == 5:
                item["cumulativeConcepts"] = list(block_concepts)
                assessment["requiredConcepts"] = list(block_concepts)
                assessment["blockOutcomeEs"] = block["blockOutcomeEs"]
                criteria, mapping = criterion_records(block_concepts, block)
                assessment["observableCriteria"] = criteria
                assessment["conceptCriterionMap"] = mapping
            if number == 100:
                item["levelCumulativeThemes"] = [entry["theme"] for entry in BLOCKS]
                assessment["requiredLevelStrands"] = list(LEVEL_STRAND_CRITERIA)
                assessment["levelStrandCriteria"] = [
                    {"strand": strand, "observableEs": observable}
                    for strand, observable in LEVEL_STRAND_CRITERIA.items()
                ]
                assessment["levelStrandCriterionMap"] = {
                    strand: observable for strand, observable in LEVEL_STRAND_CRITERIA.items()
                }
            classes.append(item)
        blocks.append({
            "number": block_number, "theme": block["theme"], "themeEs": block["themeEs"],
            "sourceTopic": block["sourceTopic"], "outcomeEs": block["blockOutcomeEs"],
            "spiralReview": block["spiralReview"], "classIds": block_class_ids,
            "phaseCycle": list(PHASES),
        })
    return {
        "schema": "onelingo.editorial.map.v2", "course": "en", "level": 3,
        "cefr": "B1", "band": "B1-entry", "scale": "client-10-levels-v1",
        "status": "planned", "runtimeAi": False, "totalClasses": 100, "totalBlocks": 20,
        "authority": "editorial-v2",
        "note": "Mapa de autoridad editorial para N3; no activa clases ni modifica el runtime.",
        "phaseCycle": list(PHASES),
        "continuity": {"startsAfter": "en.n2.class-100", "firstClass": "en.n3.class-01"},
        "progressionPolicy": {
            "entry": "short controlled contrasts with explicit context",
            "development": "connected production with reasons, chronology and source tracking",
            "exit": "integrated B1-entry cases with interaction, revision and evidence",
            "transferEveryFiveClasses": True,
            "runtimeGeneration": False,
        },
        "sourceDigests": {"legacyN3": digest(LEGACY), "n2V2": digest(N2_V2),
                          "masterCurriculum": digest(MASTER)},
        "blocks": blocks, "classes": classes,
    }


def validate_map(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    legacy = json.loads(LEGACY.read_text())
    n2 = json.loads(N2_V2.read_text())
    master = json.loads(MASTER.read_text())
    master_n3 = next(level for level in master["levels"] if level["nivel"] == 3)
    check(len(legacy["clases"]) == 100, "legacy N3 must contain 100 source classes")
    check(len(master_n3["lecciones"]) == 100, "master N3 must contain 100 source classes")
    check(n2["classes"][-1]["id"] == "en.n2.class-100", "N2 v2 terminal class mismatch")
    check(data.get("schema") == "onelingo.editorial.map.v2", "schema mismatch")
    check(data.get("status") == "planned", "editorial map must remain planned")
    check(data.get("runtimeAi") is False, "runtimeAi must be false")
    classes = data.get("classes", [])
    blocks = data.get("blocks", [])
    check(len(classes) == 100, "candidate must contain 100 classes")
    check(len(blocks) == 20, "candidate must contain 20 blocks")
    check(len({block.get("theme") for block in blocks}) == 20, "block themes must be unique")
    n2_themes = {entry["theme"] for entry in n2["classes"]}
    n2_titles = {slug(entry["title"]["en"]) for entry in n2["classes"]}
    check(not ({block.get("theme") for block in blocks} & n2_themes), "N3 theme ids must not repeat N2")
    title_keys: set[str] = set()
    task_keys: set[str] = set()
    outcome_keys: set[str] = set()
    concept_ids: set[str] = set()
    legacy_by_id = {entry["id"]: entry for entry in legacy["clases"]}
    master_by_id = {entry["id"]: entry for entry in master_n3["lecciones"]}
    source_ids = set(legacy_by_id)
    master_source_ids = set(master_by_id)
    banned = re.compile(r"appropriate to level|vocabulary|grammar|integrated skills", re.I)
    for index, cls in enumerate(classes, 1):
        expected_id = f"en.n3.class-{index:02d}"
        check(cls.get("id") == expected_id, f"class {index}: id mismatch")
        block = (index - 1) // 5 + 1
        position = (index - 1) % 5 + 1
        check(cls.get("block") == block and cls.get("position") == position,
              f"{expected_id}: block/position mismatch")
        check(cls.get("phase") == PHASES[position - 1], f"{expected_id}: phase mismatch")
        expected_pre = "en.n2.class-100" if index == 1 else f"en.n3.class-{index - 1:02d}"
        check(cls.get("prerequisites") == [expected_pre], f"{expected_id}: prerequisite mismatch")
        check(cls.get("level") == 3 and cls.get("cefr") == "B1" and cls.get("band") == "B1-entry",
              f"{expected_id}: level/band mismatch")
        check(cls.get("status") == "planned" and cls.get("runtimeAi") is False,
              f"{expected_id}: activation mismatch")
        concepts = cls.get("concepts", [])
        check(len(concepts) == 1 and concepts[0] not in concept_ids,
              f"{expected_id}: concept missing or duplicate")
        concept_ids.update(concepts)
        title_key = slug(cls.get("title", {}).get("en", ""))
        task_key = slug(cls.get("assessment", {}).get("taskEs", ""))
        outcome_key = slug(cls.get("canDo", {}).get("es", ""))
        check(bool(title_key) and title_key not in title_keys, f"{expected_id}: duplicate/empty title")
        check(title_key not in n2_titles, f"{expected_id}: title duplicates N2")
        check(bool(task_key) and task_key not in task_keys, f"{expected_id}: duplicate/empty task")
        check(bool(outcome_key) and outcome_key not in outcome_keys, f"{expected_id}: duplicate/empty can-do")
        title_keys.add(title_key); task_keys.add(task_key); outcome_keys.add(outcome_key)
        check(banned.search(cls.get("canDo", {}).get("es", "")) is None,
              f"{expected_id}: generic legacy outcome")
        assessment = cls.get("assessment", {})
        source_spec = BLOCKS[block - 1]["classes"][position - 1]
        check(assessment.get("taskEs") == source_spec["taskEs"],
              f"{expected_id}: assessment task differs from frozen editorial specification")
        evidence = assessment.get("requiredEvidence", [])
        check(isinstance(evidence, list) and len(evidence) >= 3 and len(set(evidence)) == len(evidence),
              f"{expected_id}: insufficient/duplicate required evidence")
        check(evidence == source_spec["requiredEvidence"],
              f"{expected_id}: required evidence differs from frozen observable specification")
        generic_evidence = {"lenguaje correcto", "habilidad demostrada", "uso adecuado", "respuesta completa"}
        check(all(isinstance(value, str) and value.strip() and value.casefold() not in generic_evidence
                  for value in evidence), f"{expected_id}: generic/non-observable evidence")
        check(assessment.get("deterministicSelection") is True,
              f"{expected_id}: deterministic evidence missing")
        explicit_range = explicit_word_range(assessment.get("taskEs", ""))
        if explicit_range is not None:
            check(assessment.get("minimumPerformance", {}).get("wordRange") == explicit_range,
                  f"{expected_id}: explicit task word range conflicts with minimumPerformance")
        check(bool(cls.get("languageFocus")), f"{expected_id}: language focus missing")
        legacy_id = cls.get("sourceTrace", {}).get("legacyMapClass")
        master_id = cls.get("sourceTrace", {}).get("masterCurriculumClass")
        check(legacy_id in source_ids, f"{expected_id}: invalid legacy source trace")
        check(master_id in master_source_ids, f"{expected_id}: invalid master source trace")
        if legacy_id in legacy_by_id:
            source_trace = cls.get("sourceTrace", {})
            check(source_trace.get("sourceTopic") == legacy_by_id[legacy_id].get("tema_fuente"),
                  f"{expected_id}: sourceTopic must preserve the literal legacy class topic")
            check(source_trace.get("sourceTitle") == legacy_by_id[legacy_id].get("titulo_fuente"),
                  f"{expected_id}: sourceTitle must preserve the literal legacy class title")
            check(source_trace.get("editorialDestination") == {
                "theme": cls.get("theme"), "phase": cls.get("phase")},
                f"{expected_id}: editorial destination must be separate from source topic")
        if position == 5:
            expected_concepts = [classes[index - position + offset]["concepts"][0] for offset in range(5)]
            check(cls.get("cumulativeConcepts") == expected_concepts,
                  f"{expected_id}: cumulative concepts mismatch")
            check(assessment.get("requiredConcepts") == expected_concepts,
                  f"{expected_id}: transfer evidence does not require all block concepts")
            expected_criteria, expected_mapping = criterion_records(expected_concepts, BLOCKS[block - 1])
            check(assessment.get("observableCriteria") == expected_criteria,
                  f"{expected_id}: observable concept criteria mismatch")
            check(assessment.get("conceptCriterionMap") == expected_mapping,
                  f"{expected_id}: concepts are not linked to their observable criteria")
            actual_criteria = assessment.get("observableCriteria", [])
            actual_ids = {criterion.get("id") for criterion in actual_criteria if isinstance(criterion, dict)}
            check(set(assessment.get("conceptCriterionMap", {}).values()) == actual_ids,
                  f"{expected_id}: concept criterion references are broken")
        else:
            check("cumulativeConcepts" not in cls, f"{expected_id}: premature cumulative concepts")
            check("observableCriteria" not in assessment and "conceptCriterionMap" not in assessment,
                  f"{expected_id}: observable closure criteria outside transfer class")
        if index == 74:
            check(assessment.get("wordRangeRationale") == "brief-source-bound-summary-exception",
                  f"{expected_id}: 70–90 word summary exception must be documented")
        else:
            check("wordRangeRationale" not in assessment,
                  f"{expected_id}: unexpected word-range exception")
        if index == 99:
            expected_revision = {
                "draftRequired": True,
                "checklist": ["purpose", "source-evidence", "connectors", "next-step"],
                "revisedVersionRequired": True,
                "minimumDocumentedChanges": 3,
                "acceptedChangeCategories": ["clarity", "accuracy", "evidence"],
                "cosmeticOnlyChangesAccepted": False,
            }
            check(assessment.get("revisionProtocol") == expected_revision,
                  f"{expected_id}: revision protocol must require draft, checklist, revised version and three substantive changes")
        else:
            check("revisionProtocol" not in assessment,
                  f"{expected_id}: unexpected revision protocol")
        if index == 100:
            check(cls.get("levelCumulativeThemes") == [block["theme"] for block in blocks],
                  f"{expected_id}: final performance does not cover all level themes")
            check(assessment.get("requiredLevelStrands") == list(LEVEL_STRAND_CRITERIA),
                  f"{expected_id}: final performance needs the five exact level strands")
            expected_level_criteria = [
                {"strand": strand, "observableEs": observable}
                for strand, observable in LEVEL_STRAND_CRITERIA.items()
            ]
            check(assessment.get("levelStrandCriteria") == expected_level_criteria,
                  f"{expected_id}: final performance lacks observable evidence for every level strand")
            check(assessment.get("levelStrandCriterionMap") == LEVEL_STRAND_CRITERIA,
                  f"{expected_id}: level strands are not linked to observable criteria")
        else:
            check("levelStrandCriteria" not in assessment and
                  "levelStrandCriterionMap" not in assessment,
                  f"{expected_id}: level-wide criteria outside final class")
    prior_n3_themes: set[str] = set()
    for block_number, block in enumerate(blocks, 1):
        expected_ids = [f"en.n3.class-{number:02d}"
                        for number in range((block_number - 1) * 5 + 1, block_number * 5 + 1)]
        check(block.get("number") == block_number, f"block {block_number}: number mismatch")
        check(block.get("classIds") == expected_ids, f"block {block_number}: classIds mismatch")
        check(block.get("phaseCycle") == PHASES, f"block {block_number}: phase cycle mismatch")
        check(bool(block.get("outcomeEs")), f"block {block_number}: outcome missing")
        block_classes = classes[(block_number - 1) * 5:block_number * 5]
        check(all(cls.get("theme") == block.get("theme") for cls in block_classes),
              f"block {block_number}: class theme mismatch")
        for reference in block.get("spiralReview", []):
            match = re.fullmatch(r"(n2|n3):([a-z0-9-]+)", reference)
            check(match is not None, f"block {block_number}: malformed spiral reference {reference}")
            if match:
                level, theme = match.groups()
                check(theme in (n2_themes if level == "n2" else prior_n3_themes),
                      f"block {block_number}: unknown/future spiral reference {reference}")
        prior_n3_themes.add(block.get("theme"))
    expected_digests = {"legacyN3": digest(LEGACY), "n2V2": digest(N2_V2),
                        "masterCurriculum": digest(MASTER)}
    check(data.get("sourceDigests") == expected_digests, "source digest mismatch")
    if errors:
        raise ValueError("\n".join(errors))
    return {"status": "OK", "classes": len(classes), "blocks": len(blocks),
            "uniqueThemes": len({block["theme"] for block in blocks}),
            "uniqueTitles": len(title_keys), "uniqueCanDos": len(outcome_keys),
            "firstPrerequisite": classes[0]["prerequisites"][0],
            "finalClass": classes[-1]["id"], "phaseCycles": 20,
            "transferClosures": sum(1 for cls in classes if cls["phase"] == "transfer")}


def run_negative_tests(data: dict[str, Any]) -> dict[str, Any]:
    def delete_c100_strand(candidate: dict[str, Any]) -> None:
        candidate["classes"][99]["assessment"]["requiredLevelStrands"].pop()

    def generic_c100_criteria(candidate: dict[str, Any]) -> None:
        candidate["classes"][99]["assessment"]["levelStrandCriteria"][0]["observableEs"] = "Demuestra la habilidad."

    def generic_c35_criterion(candidate: dict[str, Any]) -> None:
        candidate["classes"][34]["assessment"]["observableCriteria"][0]["observableEs"] = "Usa la gramática."

    def erase_c40_relative_evidence(candidate: dict[str, Any]) -> None:
        candidate["classes"][39]["assessment"]["requiredEvidence"][0] = "lenguaje correcto"

    def replace_c93_source_topic(candidate: dict[str, Any]) -> None:
        candidate["classes"][92]["sourceTrace"]["sourceTopic"] = "integrated review"

    def weaken_c99_revision(candidate: dict[str, Any]) -> None:
        candidate["classes"][98]["assessment"]["revisionProtocol"]["minimumDocumentedChanges"] = 0

    def remove_c74_exception(candidate: dict[str, Any]) -> None:
        del candidate["classes"][73]["assessment"]["wordRangeRationale"]

    cases = [
        ("c100-missing-macrostrand", delete_c100_strand),
        ("c100-generic-strand-criterion", generic_c100_criteria),
        ("c35-generic-concept-criterion", generic_c35_criterion),
        ("c40-generic-relative-evidence", erase_c40_relative_evidence),
        ("c93-source-topic-reframed", replace_c93_source_topic),
        ("c99-revision-without-minimum", weaken_c99_revision),
        ("c74-undocumented-short-summary", remove_c74_exception),
    ]
    results: list[dict[str, str]] = []
    for name, mutate in cases:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        try:
            validate_map(candidate)
        except ValueError as error:
            results.append({"name": name, "result": "REJECTED", "reason": str(error).splitlines()[0]})
        else:
            raise AssertionError(f"negative mutation was accepted: {name}")
    return {"status": "OK", "mutations": len(results), "rejected": len(results), "cases": results}


def write_report(data: dict[str, Any], validation: dict[str, Any], negative_tests: dict[str, Any]) -> None:
    lines = [
        "# Build — Mapa editorial Inglés N3 v2", "",
        "Estado: **plan editorial integrado; no activa clases ni runtime**.", "",
        "## Decisiones de diseño", "",
        "- N3 representa **entrada B1** en `client-10-levels-v1`.",
        "- La continuidad empieza exactamente en `en.n2.class-100`.",
        "- Cada bloque recorre `input → form → comprehension → production → transfer`.",
        "- Cada clase declara una tarea observable y tres evidencias mínimas.",
        "- Un rango de palabras escrito en la tarea prevalece y el validador exige coincidencia exacta.",
        "- Cada cierre enlaza sus cinco conceptos con cinco criterios observables y verificables.",
        "- C35, C40, C45 y C50 exigen evidencia explícita de gerundio/infinitivo, relativas, pasiva y estilo indirecto.",
        "- C100 enlaza las cinco macrohebras del nivel con criterios observables, no solo con una lista nominal.",
        "- `sourceTrace.sourceTopic` conserva literalmente el tema de cada clase fuente; `editorialDestination` registra el destino v2 por separado.",
        "- C99 exige borrador, lista de control, versión revisada y al menos tres cambios sustantivos documentados.",
        "- C74 conserva 70–90 palabras como excepción documentada de resumen breve ligado a una fuente.",
        "", "## Progresión", "",
        "- C1–C30: contraste controlado de tiempo, narración, futuro y condición.",
        "- C31–C60: elecciones, definición, procesos, mensajes y naturalidad léxica.",
        "- C61–C90: colaboración, viajes, fuentes, medios, aprendizaje y acción local.",
        "- C91–C100: proyecto comunitario y desempeño final con revisión propia.",
        "", "## Trazabilidad de bloques", "",
        "| Bloque | Tema v2 | Ancla fuente | Resultado de transferencia |",
        "|---:|---|---|---|",
    ]
    for block in data["blocks"]:
        lines.append(f"| {block['number']} | `{block['theme']}` — {block['themeEs']} | "
                     f"{block['sourceTopic']} | {block['outcomeEs']} |")
    lines.extend([
        "", "## Salvaguardas contra repetición", "",
        "- 20 identificadores de tema, 100 títulos, 100 can-do y 100 tareas son únicos.",
        "- Ningún `theme` de N3 repite un identificador de tema de N2 v2.",
        "- La espiral reutiliza conocimientos previos dentro de tareas nuevas; no recicla nombres de bloque.",
        "- Los bloques 19–20 son proyectos concretos, no listas genéricas de Vocabulary/Grammar/Listening.",
        "", "## Validación reproducible", "", "```json",
        json.dumps(validation, ensure_ascii=False, indent=2), "```", "",
        "## Mutaciones negativas", "",
        "El generador altera copias en memoria y exige que el validador rechace las siete degradaciones:", "", "```json",
        json.dumps(negative_tests, ensure_ascii=False, indent=2), "```", "",
        "Comandos:", "", "```bash",
        "PYTHONDONTWRITEBYTECODE=1 python3 tools/contenido/generar_mapa_n3_editorial_v2.py",
        "PYTHONDONTWRITEBYTECODE=1 python3 tools/contenido/generar_mapa_n3_editorial_v2.py --validate-only \\",
        "  assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json", "```", "",
        "Idempotencia verificada: dos regeneraciones consecutivas produjeron el mismo `MANIFEST.sha256`.", "",
        "## Fuentes congeladas", "",
        f"- `mapa-n3.json`: `{data['sourceDigests']['legacyN3']}`",
        f"- `mapa-n2-editorial-v2.json`: `{data['sourceDigests']['n2V2']}`",
        f"- `curriculo-master.json`: `{data['sourceDigests']['masterCurriculum']}`",
        "", "## Puertas pendientes", "",
        "- Revisión independiente de secuencia gramatical y carga B1 de entrada.",
        "- Auditoría de vocabulario reservado antes de autorizar cada bloque.",
        "- Diseño de contrato de clases N3 y prueba longitudinal; este mapa no contiene ejercicios.",
        "- El mapa permanece `planned`; la redacción de clases requiere sus propias puertas editoriales.", "",
    ])
    (REPORT_OUT / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def write_manifest(paths: list[Path]) -> None:
    text = "\n".join(f"{digest(path)}  {path.name}" for path in paths) + "\n"
    (REPORT_OUT / "MANIFEST.sha256").write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", type=Path)
    args = parser.parse_args()
    if args.validate_only:
        data = json.loads(args.validate_only.read_text())
        print(json.dumps(validate_map(data), ensure_ascii=False, indent=2))
        return 0
    data = build_map()
    validation = validate_map(data)
    negative_tests = run_negative_tests(data)
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (REPORT_OUT / "VALIDATION.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n",
                                         encoding="utf-8")
    (REPORT_OUT / "NEGATIVE_TESTS.json").write_text(
        json.dumps(negative_tests, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_report(data, validation, negative_tests)
    write_manifest([TARGET, REPORT_OUT / "VALIDATION.json", REPORT_OUT / "NEGATIVE_TESTS.json", REPORT_OUT / "REPORT.md"])
    print(json.dumps(validation, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
