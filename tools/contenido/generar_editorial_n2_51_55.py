#!/usr/bin/env python3
"""Regenera las clases editoriales de Inglés N2 C51-C55."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n2"
SCALE = "client-10-levels-v1"
CONCEPTS = {
    51: "n2-countable-uncountable",
    52: "n2-quantity-a-few-a-little-enough",
    53: "n2-quantity-too-much-too-many",
    54: "n2-event-quantities",
    55: "n2-shopping-problem",
}
TITLES = {
    51: ("Countable and uncountable review", "Repaso de contables e incontables"),
    52: ("A few, a little and enough", "A few, a little y enough"),
    53: ("Too much and too many", "Too much y too many"),
    54: ("Plan quantities for an event", "Planificar cantidades para un evento"),
    55: ("Solve a shopping problem", "Resolver un problema de compras"),
}
PHASES = {51: "input", 52: "form", 53: "comprehension", 54: "production", 55: "transfer"}
CUMULATIVE = [CONCEPTS[number] for number in range(51, 56)]
REMEDIATION = {
    51: {"e01": ("t01", "r02"), "e02": ("t02", "r03"), "e03": ("t05", "r01"), "e04": ("t03", "r01")},
    52: {"e01": ("t03", "r01"), "e02": ("t03", "r01"), "e03": ("t03", "r01"), "e04": ("t01", "r02")},
    53: {"e01": ("t01", "r02"), "e02": ("t02", "r03"), "e03": ("t05", "r03"), "e04": ("t02", "r03")},
    54: {"e01": ("t02", "r03"), "e02": ("t04", "r01"), "e03": ("t01", "r02"), "e04": ("t05", "r01")},
    55: {"e01": ("t04", "r03"), "e02": ("t03", "r03"), "e03": ("t05", "r03"), "e04": ("t02", "r01")},
}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def add_hash(item):
    payload = {key: value for key, value in item.items() if key not in {"id", "contentHash"}}
    item["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return item


def segments(en, es):
    en_words, es_words = en.split(), es.split()
    en_mid = max(1, len(en_words) // 2)
    es_mid = max(1, len(es_words) // 2)
    return [
        {"en": " ".join(en_words[:en_mid]), "es": " ".join(es_words[:es_mid])},
        {"en": " ".join(en_words[en_mid:]), "es": " ".join(es_words[es_mid:])},
    ]


def choice(prompt, choices, index, feedback, requires=None):
    return {"format": "elegir", "prompt": prompt, "choices": choices,
            "answerIndex": index, "feedback": feedback,
            "hint": "Compara la cantidad con el sustantivo que la acompaña.",
            **({"requires": requires} if requires is not None else {})}


def complete(prompt, answer, feedback, requires=None):
    return {"format": "completar", "prompt": prompt, "answer": answer,
            "feedback": feedback,
            "hint": "Identifica si el sustantivo se puede contar o medir.",
            **({"requires": requires} if requires is not None else {})}


def order(prompt, answer, feedback, requires=None):
    return {"format": "ordenar", "prompt": prompt, "answer": answer,
            "feedback": feedback,
            "hint": "Ordena primero el sujeto y después la expresión de cantidad.",
            **({"requires": requires} if requires is not None else {})}


def listen(prompt, audio, choices, index, feedback, requires=None):
    return {"format": "escuchar", "prompt": prompt, "audio": audio,
            "choices": choices, "answerIndex": index, "feedback": feedback,
            "hint": "Escucha la palabra de cantidad y el sustantivo.",
            **({"requires": requires} if requires is not None else {})}


def write(prompt, stimulus, answer, accepted, feedback, requires=None):
    return {"format": "escribir", "prompt": prompt, "stimulus": stimulus,
            "answer": answer, "accepted": accepted, "feedback": feedback,
            "hint": "Revisa la cantidad y si el sustantivo es contable.",
            **({"requires": requires} if requires is not None else {})}


def match(prompt, pairs, feedback, requires=None):
    return {"format": "relacionar", "prompt": prompt, "pairs": pairs,
            "feedback": feedback,
            "hint": "Relaciona cada expresión con su significado.",
            **({"requires": requires} if requires is not None else {})}


def fb(rule, label, answer):
    return f"{rule} En {label}, la respuesta es «{answer}»."


SPECS = {
    51: {
        "rule": "Los sustantivos contables admiten números; los incontables se expresan como cantidades de materia.",
        "vocab": [("chairs", "sillas"), ("rice", "arroz"), ("bottles", "botellas"),
                  ("water", "agua"), ("flour", "harina"), ("apples", "manzanas"),
                  ("milk", "leche"), ("bananas", "plátanos")],
        "teaching": [
            ("We need three chairs for the meeting.", "Necesitamos tres sillas para la reunión.", "Chairs se puede contar con un número."),
            ("There is some rice in the kitchen.", "Hay arroz en la cocina.", "Rice es incontable y se expresa como una cantidad."),
            ("We bought four bottles of water.", "Compramos cuatro botellas de agua.", "Bottles es contable; water es la materia que contienen."),
            ("We have enough flour for the cake.", "Tenemos suficiente harina para el pastel.", "Flour es incontable, aunque puede medirse."),
            ("Apples are countable, but milk is uncountable.", "Las manzanas son contables, pero la leche es incontable.", "Apples se cuenta por unidades y milk se mide como materia."),
        ],
        "pools": {
            "practiceGuided": [
                choice("Elige la frase correcta para tres sillas.", ["There is three chairs.", "There are three chairs.", "There are three chair."], 1, fb("There are acompaña un plural contable.", "la elección guiada", "There are three chairs")),
                complete("Completa la cantidad no contable: There is some ___ in the bowl.", "rice", fb("Rice es incontable y no lleva plural aquí.", "el primer espacio", "rice")),
                order("Ordena la compra de cuatro botellas de agua.", "We bought four bottles of water.", fb("Bottles es plural contable y water nombra la materia.", "el primer orden", "We bought four bottles of water.")),
            ],
            "practice": [
                write("Escribe en inglés: Compré dos manzanas.", "Compré dos manzanas.", "I bought two apples.", ["I bought two apples.", "I bought a pair of apples."], fb("Apples es contable y aparece en plural después de two.", "la primera producción", "I bought two apples.")),
                listen("Escucha y elige la frase sobre la leche.", "There is some milk in the fridge.", ["There are some milk in the fridge.", "There is some milk in the fridge.", "There is a milk in the fridge."], 1, fb("Milk es incontable y usa there is some.", "el primer audio", "There is some milk in the fridge.")),
                match("Relaciona dos materias con su significado.", [("rice", "arroz"), ("flour", "harina")], fb("Rice y flour nombran materias incontables.", "el primer grupo léxico", "rice / flour")),
            ],
            "evaluation": [
                choice("Elige la frase correcta para cuatro bananas.", ["There is four bananas.", "There are four banana.", "There are four bananas."], 2, fb("Bananas es plural contable y necesita there are.", "la primera evaluación", "There are four bananas.")),
                complete("Completa: We need some ___ from the tap for soup.", "water", fb("El dato from the tap identifica water, una materia incontable.", "el segundo espacio", "water")),
                write("Describe la compra: cuatro manzanas y arroz.", "Compramos cuatro manzanas y arroz.", "We bought four apples and some rice.", ["We bought four apples and some rice.", "We purchased four apples and some rice."], fb("Apples se cuenta por unidades y rice se expresa como materia.", "la producción evaluada", "We bought four apples and some rice.")),
                listen("Escucha paquetes contables de harina.", "There are two packages of flour.", ["There is two packages of flour.", "There are two package of flour.", "There are two packages of flour."], 2, fb("Packages es plural contable; flour sigue siendo materia.", "el audio evaluado", "There are two packages of flour.")),
            ],
            "review": [
                match("Relaciona dos palabras de la compra.", [("bottles", "botellas"), ("milk", "leche")], fb("Bottles se cuenta; milk se mide como materia.", "el segundo grupo léxico", "bottles / milk")),
                complete("Completa el plural contable: I bought two ___ for lunch.", "bananas", fb("Two exige el plural contable bananas.", "el orden de repaso", "bananas")),
                write("Escribe en inglés: Hay harina en el cuenco.", "Hay harina en el cuenco.", "There is some flour in the bowl.", ["There is some flour in the bowl.", "Some flour is in the bowl."], fb("Flour es incontable y se presenta con some.", "la producción de repaso", "There is some flour in the bowl.")),
            ],
        },
    },
    52: {
        "rule": "A few acompaña plurales contables, a little acompaña incontables y enough indica cantidad suficiente.",
        "vocab": [("snacks", "aperitivos"), ("juice", "zumo"), ("plates", "platos"),
                  ("time", "tiempo"), ("napkins", "servilletas"), ("water", "agua"),
                  ("space", "espacio"), ("guests", "invitados")],
        "teaching": [
            ("We have a few snacks for the guests.", "Tenemos unos pocos aperitivos para los invitados.", "A few acompaña al plural contable snacks."),
            ("There is a little juice in the jug.", "Hay un poco de zumo en la jarra.", "A little acompaña al incontable juice."),
            ("We need enough plates for everyone.", "Necesitamos suficientes platos para todos.", "Enough indica que la cantidad cubre la necesidad."),
            ("A few napkins are on the table.", "Hay unas pocas servilletas sobre la mesa.", "Napkins es plural contable y usa a few."),
            ("We have enough time and space for the guests.", "Tenemos suficiente tiempo y espacio para los invitados.", "Time y space son incontables en este contexto y usan enough."),
        ],
        "pools": {
            "practiceGuided": [
                choice("Elige la frase correcta para unos pocos platos.", ["We have a little plates.", "We have a few plates.", "We have enough plate."], 1, fb("A few acompaña el plural contable plates.", "la elección guiada", "We have a few plates.")),
                complete("Completa (un poco): There is ___ juice left.", "a little", fb("La pista un poco exige a little con el incontable juice.", "el primer espacio", "a little")),
                order("Ordena la frase sobre tiempo suficiente.", "We have enough time for lunch.", fb("Enough va antes del sustantivo time.", "el primer orden", "We have enough time for lunch.")),
            ],
            "practice": [
                write("Escribe en inglés: Tenemos unas pocas servilletas.", "Tenemos unas pocas servilletas.", "We have a few napkins.", ["We have a few napkins.", "There are a few napkins."], fb("Napkins es plural contable y usa a few.", "la primera producción", "We have a few napkins.")),
                listen("Escucha y elige la frase sobre el zumo restante.", "There is a little juice left.", ["There are a little juice left.", "There is a little juice left.", "There is a few juice left."], 1, fb("Juice es incontable y necesita there is a little.", "el primer audio", "There is a little juice left.")),
                match("Relaciona dos palabras de cantidades pequeñas.", [("snacks", "aperitivos"), ("plates", "platos")], fb("Snacks y plates son plurales contables para cantidades pequeñas.", "el primer grupo léxico", "snacks / plates")),
            ],
            "evaluation": [
                choice("Elige la frase que cubre a todos los invitados.", ["We have enough plates for everyone.", "We have a few plate for everyone.", "We have enough plate for everyone."], 0, fb("Enough plates expresa una cantidad suficiente y plates es plural.", "la primera evaluación", "We have enough plates for everyone.")),
                complete("Completa la cantidad suficiente: We have ___ time for lunch.", "enough", fb("Enough indica que time alcanza para el almuerzo.", "el segundo espacio", "enough")),
                write("Escribe: Necesitamos suficientes vasos para todos.", "Necesitamos suficientes vasos para todos.", "We need enough cups for everyone.", ["We need enough cups for everyone.", "We need enough cups for all the guests."], fb("Cups es plural contable y enough indica suficiencia.", "la producción evaluada", "We need enough cups for everyone.")),
                listen("Escucha y elige la cantidad de aperitivos.", "We have a few snacks for the guests.", ["We have a little snacks for the guests.", "We have enough snack for the guests.", "We have a few snacks for the guests."], 2, fb("Snacks es plural contable y usa a few.", "el audio evaluado", "We have a few snacks for the guests.")),
            ],
            "review": [
                match("Relaciona dos palabras de cantidad suficiente.", [("enough", "suficiente"), ("space", "espacio")], fb("Enough expresa suficiencia y space es la necesidad medida.", "el segundo grupo léxico", "enough / space")),
                complete("Completa el plural: We need ___ more plates.", "a few", fb("A few more acompaña al plural plates.", "el repaso de cantidad", "a few")),
                write("Escribe en inglés: Hay un poco de agua para los invitados.", "Hay un poco de agua para los invitados.", "There is a little water for the guests.", ["There is a little water for the guests.", "We have a little water for the guests."], fb("Water es incontable y se combina con a little.", "la producción de repaso", "There is a little water for the guests.")),
            ],
        },
    },
    53: {
        "rule": "Too much acompaña incontables y too many acompaña plurales contables cuando la cantidad supera lo conveniente.",
        "vocab": [("sugar", "azúcar"), ("boxes", "cajas"), ("noise", "ruido"),
                  ("people", "personas"), ("luggage", "equipaje"), ("bags", "bolsas"),
                  ("waste", "residuos"), ("space", "espacio")],
        "teaching": [
            ("There is too much sugar in the coffee.", "Hay demasiada azúcar en el café.", "Sugar es incontable y usa too much."),
            ("There are too many boxes in the hall.", "Hay demasiadas cajas en el pasillo.", "Boxes es plural contable y usa too many."),
            ("There is too much noise outside.", "Hay demasiado ruido afuera.", "Noise es incontable y se combina con too much."),
            ("There are too many people in the small room.", "Hay demasiadas personas en la sala pequeña.", "People es plural contable en esta frase y usa too many."),
            ("We have too much luggage and too many bags.", "Tenemos demasiado equipaje y demasiadas bolsas.", "Luggage es incontable; bags es plural contable."),
        ],
        "pools": {
            "practiceGuided": [
                choice("Elige la frase correcta para demasiadas cajas.", ["There is too many boxes.", "There are too much boxes.", "There are too many boxes."], 2, fb("Boxes es plural contable y necesita too many.", "la elección guiada", "There are too many boxes.")),
                complete("Completa la cantidad excesiva: There is too ___ sugar.", "much", fb("Sugar es incontable y necesita too much.", "el primer espacio", "much")),
                order("Ordena la frase sobre demasiadas personas.", "There are too many people here.", fb("Too many precede al plural people.", "el primer orden", "There are too many people here.")),
            ],
            "practice": [
                write("Escribe en inglés: Hay demasiado ruido aquí.", "Hay demasiado ruido aquí.", "There is too much noise here.", ["There is too much noise here.", "There is too much noise around here."], fb("Noise es incontable y usa too much.", "la primera producción", "There is too much noise here.")),
                listen("Escucha y elige la frase con equipaje.", "We have too much luggage.", ["We have too many luggage.", "We have too much luggage.", "We has too much luggage."], 1, fb("Luggage es incontable y usa too much.", "el primer audio", "We have too much luggage.")),
                match("Relaciona cantidad y sustantivo.", [("too much", "demasiado"), ("sugar", "azúcar")], fb("Too much mide una materia como sugar.", "el primer grupo léxico", "too much / sugar")),
            ],
            "evaluation": [
                choice("Elige la frase correcta para demasiado equipaje.", ["There are too many luggage at the airport.", "There is too much luggage at the airport.", "There is too much luggages at the airport."], 1, fb("Luggage es incontable y se combina con too much.", "la primera evaluación", "There is too much luggage at the airport.")),
                complete("Completa el plural: There are too ___ people here.", "many", fb("People es plural contable y necesita too many.", "el segundo espacio", "many")),
                write("Escribe: El evento tiene demasiadas bolsas y residuos.", "El evento tiene demasiadas bolsas y residuos.", "The event has too many bags and too much waste.", ["The event has too many bags and too much waste.", "There are too many bags and too much waste at the event."], fb("Bags es contable y waste es incontable; cada uno exige su forma.", "la producción evaluada", "The event has too many bags and too much waste.")),
                listen("Escucha y elige la frase con demasiados paquetes.", "There are too many packages.", ["There is too many packages.", "There are too much packages.", "There are too many packages."], 2, fb("Packages es plural contable y usa too many.", "el audio evaluado", "There are too many packages.")),
            ],
            "review": [
                match("Relaciona dos problemas de cantidad.", [("noise", "ruido"), ("space", "espacio")], fb("Noise y space son incontables en estos problemas.", "el segundo grupo léxico", "noise / space")),
                complete("Completa la materia excesiva: There is too ___ waste.", "much", fb("Waste es incontable y usa too much.", "el repaso de cantidad", "much")),
                write("Escribe en inglés: Hay demasiadas cajas en la tienda.", "Hay demasiadas cajas en la tienda.", "There are too many boxes in the shop.", ["There are too many boxes in the shop.", "The shop has too many boxes."], fb("Boxes es plural contable y usa too many.", "la producción de repaso", "There are too many boxes in the shop.")),
            ],
        },
    },
    54: {
        "rule": "Un plan de evento combina plurales contables, cantidades incontables y una cantidad suficiente para cada necesidad.",
        "vocab": [("event", "evento"), ("guests", "invitados"), ("servings", "porciones"),
                  ("cups", "vasos"), ("plates", "platos"), ("sandwiches", "sándwiches"),
                  ("juice", "zumo"), ("shopping list", "lista de compras")],
        "teaching": [
            ("For twenty guests, each person needs one plate, one sandwich, and one bottle.", "Para veinte invitados, cada persona necesita un plato, un sándwich y una botella.", "Una unidad de cada artículo por invitado fija la capacidad que debe cubrir el plan."),
            ("We need enough plates and cups for everyone.", "Necesitamos suficientes platos y vasos para todos.", "Plates y cups son plurales contables para cada invitado."),
            ("A few extra sandwiches will help.", "Unos pocos sándwiches extra ayudarán.", "A few acompaña al plural sandwiches."),
            ("We should buy a little juice, not too much.", "Debemos comprar un poco de zumo, no demasiado.", "Juice es incontable y necesita a little o too much."),
            ("For twenty guests, we need ten more plates, eight more sandwiches, and eighteen more bottles.", "Para veinte invitados, necesitamos diez platos, ocho sándwiches y dieciocho botellas más.", "La lista compara capacidad e inventario: faltan 10 platos, 8 sándwiches y 18 botellas."),
        ],
        "pools": {
            "practiceGuided": [
                choice("Para veinte invitados, elige el plan correcto.", ["We need enough plates for everyone.", "We need enough plate for everyone.", "We need a little plates for everyone."], 0, fb("Plates es plural y enough expresa una cantidad suficiente.", "la elección guiada", "We need enough plates for everyone.")),
                complete("Completa (sándwiches): We need a few ___ for lunch.", "sandwiches", fb("La traducción entre paréntesis identifica sandwiches, un plural contable.", "el primer espacio", "sandwiches")),
                order("Ordena el plan sobre un poco de zumo.", "We should buy a little juice.", fb("A little precede al incontable juice.", "el primer orden", "We should buy a little juice.")),
            ],
            "practice": [
                write("Escribe: Necesitamos veinte platos y suficientes vasos.", "Necesitamos veinte platos y suficientes vasos.", "We need twenty plates and enough cups.", ["We need twenty plates and enough cups.", "We need twenty plates plus enough cups."], fb("Plates y cups son plurales contables; enough marca suficiencia.", "la primera producción", "We need twenty plates and enough cups.")),
                listen("Escucha y elige el plan de sándwiches.", "We are preparing enough sandwiches for the guests.", ["We are preparing enough sandwich for the guests.", "We are preparing a little sandwiches for the guests.", "We are preparing enough sandwiches for the guests."], 2, fb("Sandwiches es plural y enough cubre la necesidad de invitados.", "el primer audio", "We are preparing enough sandwiches for the guests.")),
                match("Relaciona dos palabras del plan del evento.", [("servings", "porciones"), ("shopping list", "lista de compras")], fb("Servings cuenta porciones y shopping list organiza la compra.", "el primer grupo léxico", "servings / shopping list")),
            ],
            "evaluation": [
                choice("Para doce invitados, elige la cantidad suficiente.", ["We need a little cups for twelve guests.", "We need enough cups for twelve guests.", "We need enough cup for twelve guests."], 1, fb("Cups es plural contable y enough expresa suficiencia.", "la primera evaluación", "We need enough cups for twelve guests.")),
                complete("Completa la cantidad pequeña: We need a ___ juice for the picnic.", "little", fb("Juice es incontable y se combina con a little.", "el segundo espacio", "little")),
                write("Calcula: 20 invitados, 1 plato/sándwich/botella cada uno; hay 10, 12 y 2.", "Para 20 invitados, cada uno necesita 1 plato, 1 sándwich y 1 botella de zumo; hay 10 platos, 12 sándwiches y 2 botellas. Escribe qué comprar.", "For twenty guests, we need ten more plates, eight more sandwiches, and eighteen more bottles of juice.", ["For twenty guests, we need ten more plates, eight more sandwiches, and eighteen more bottles of juice.", "For twenty guests, we need ten extra plates, eight extra sandwiches, and eighteen more bottles of juice."], fb("El plan calcula una unidad por invitado: faltan 10 platos, 8 sándwiches y 18 botellas.", "la producción evaluada", "For twenty guests, we need ten more plates, eight more sandwiches, and eighteen more bottles of juice.")),
                listen("Escucha y elige la cantidad para los invitados.", "We have enough food for the guests.", ["We have enough foods for the guests.", "We has enough food for the guests.", "We have enough food for the guests."], 2, fb("Food es incontable y enough expresa una cantidad suficiente.", "el audio evaluado", "We have enough food for the guests.")),
            ],
            "review": [
                match("Relaciona dos elementos del evento.", [("guests", "invitados"), ("juice", "zumo")], fb("Guests se cuenta; juice se mide como bebida.", "el segundo grupo léxico", "guests / juice")),
                write("Calcula: 12 invitados necesitan 1 de cada artículo; hay 4, 8 y 3.", "Para 12 invitados, cada uno necesita 1 plato, 1 sándwich y 1 botella; hay 4 platos, 8 sándwiches y 3 botellas. Escribe qué falta.", "We need eight more plates, four more sandwiches, and nine more bottles.", ["We need eight more plates, four more sandwiches, and nine more bottles.", "For twelve guests, we need eight extra plates, four extra sandwiches, and nine extra bottles."], fb("Resta el inventario de la capacidad: faltan 8 platos, 4 sándwiches y 9 botellas.", "el cálculo de repaso", "We need eight more plates, four more sandwiches, and nine more bottles.")),
                write("Escribe: Compramos suficientes vasos para todos.", "Compramos suficientes vasos para todos.", "We bought enough cups for everyone.", ["We bought enough cups for everyone.", "We purchased enough cups for all the guests."], fb("Cups es plural y enough expresa que alcanza para todos.", "la producción de repaso", "We bought enough cups for everyone.")),
            ],
        },
    },
    55: {
        "rule": "Una solución de compras identifica el problema y combina cantidades adecuadas con una acción concreta.",
        "vocab": [("receipt", "recibo"), ("missing", "faltante"), ("cashier", "cajero"),
                  ("wrong", "equivocado"), ("replace", "reemplazar"), ("refund", "reembolso"),
                  ("delivery", "entrega"), ("plates", "platos"), ("bread", "pan")],
        "teaching": [
            ("The receipt shows two missing items.", "El recibo muestra dos artículos faltantes.", "Receipt permite comprobar qué artículos faltan."),
            ("The delivery has the wrong plates; the shop will replace them.", "La entrega tiene los platos equivocados; la tienda los reemplazará.", "Wrong plates identifica artículos equivocados y replace them da la solución."),
            ("We have too many large plates and not enough bread.", "Tenemos demasiados platos grandes y no hay suficiente pan.", "Too many acompaña plates y not enough mide bread."),
            ("We need a few more sandwiches, but we have enough bread.", "Necesitamos unos pocos sándwiches más, pero tenemos suficiente pan.", "A few y enough resuelven dos necesidades distintas."),
            ("For our event, eight guests need two servings and two cups each; the receipt lists sixteen cups, but only eight arrived, so eight are missing. We should request a refund.", "Para nuestro evento, ocho invitados necesitan dos porciones (servings) y dos vasos cada uno; el recibo lista dieciséis vasos, pero solo llegaron ocho, así que faltan ocho. Debemos pedir una devolución.", "La guía integra evento, invitados, servings, cantidades faltantes y una única acción de devolución."),
        ],
        "pools": {
            "practiceGuided": [
                choice("Elige la solución con una cantidad contable correcta.", ["We need a little cups.", "We need a few cups.", "We need a few cup."], 1, fb("Cups es plural contable y usa a few.", "la elección guiada", "We need a few cups.")),
                complete("Completa (cambiar por otros): He can ___ the wrong items.", "replace", fb("La pista cambiar por otros identifica replace.", "el primer espacio", "replace")),
                order("Ordena la solución sobre el recibo.", "The receipt shows two missing items.", fb("Receipt introduce la prueba y missing describe los artículos.", "el primer orden", "The receipt shows two missing items.")),
            ],
            "practice": [
                write("Escribe: El recibo muestra dos artículos faltantes.", "El recibo muestra dos artículos faltantes.", "Our receipt lists two missing items.", ["Our receipt lists two missing items.", "The receipt lists two missing items."], fb("Receipt identifica la compra y missing describe los artículos.", "la primera producción", "Our receipt lists two missing items.")),
                listen("Escucha y elige la solución del cajero.", "The cashier can give a refund.", ["The cashier can gives a refund.", "The cashier can give a refund.", "The cashier can give a replace."], 1, fb("Después de can se usa give; refund es la devolución de dinero.", "el primer audio", "The cashier can give a refund.")),
                match("Relaciona dos soluciones de compra.", [("replace", "reemplazar"), ("refund", "reembolso")], fb("Replace cambia el artículo; refund devuelve el dinero.", "el primer grupo léxico", "replace / refund")),
            ],
            "evaluation": [
                choice("Elige la solución con cantidad suficiente.", ["We have enough bread for everyone.", "We have a little bread for everyone.", "We have enough breads for everyone."], 0, fb("Bread es incontable y enough indica que alcanza.", "la primera evaluación", "We have enough bread for everyone."), requires=CUMULATIVE[:2]),
                complete("Completa el exceso contable: There are too ___ bags.", "many", fb("Bags es plural contable y necesita too many.", "el segundo espacio", "many"), requires=[CONCEPTS[53]]),
                write("Evento: 8 invitados, 2 servings c/u; recibo 16, llegan 8: faltan 8. Pide devolución.", "Evento para 8 invitados: cada uno necesita 2 porciones (servings) y 2 vasos; el recibo lista 16 vasos, la entrega trae 8: faltan 8. Hay demasiadas bolsas, pero suficiente comida. Escribe una solución: pide devolución.", "For the event, eight guests need two servings and two cups each; the receipt lists sixteen cups, but the delivery has eight, so eight are missing. There are too many bags, but we have enough food. We should ask for a refund.", ["For the event, eight guests need two servings and two cups each; the receipt lists sixteen cups, but the delivery has eight, so eight are missing. There are too many bags, but we have enough food. We should ask for a refund.", "At our event, each of eight guests needs two servings and two cups. Only eight of the sixteen ordered cups arrived, so eight are missing. Food is enough despite too many bags; we should request a refund."], fb("La respuesta integra evento, invitados, servings, el cálculo de 8 faltantes, comida suficiente, bolsas de más y una única acción de devolución.", "la producción acumulativa", "For the event, eight guests need two servings and two cups each; the receipt lists sixteen cups, but the delivery has eight, so eight are missing."), requires=CUMULATIVE),
                listen("Escucha el caso de artículos equivocados y su solución.", "The delivery has the wrong plates, so the shop will replace them.", ["The delivery has the wrong plates, so the shop will replace them.", "The delivery has the right plates, so the shop will replace them.", "The delivery has the wrong plates, so the shop will keep them."], 0, fb("Wrong plates describen el problema y replace them es la solución escuchada.", "el audio evaluado", "The delivery has the wrong plates, so the shop will replace them."), requires=[CONCEPTS[55]]),
            ],
            "review": [
                match("Relaciona el problema de artículos y su solución.", [("wrong plates", "platos equivocados"), ("replace them", "reemplazarlos")], fb("Wrong plates identifica el error y replace them nombra la solución.", "el segundo grupo léxico", "wrong plates / replace them")),
                complete("Completa (devolver dinero): The shop can give a ___.", "refund", fb("La pista devolver dinero identifica refund.", "el repaso de cantidad", "refund")),
                write("Integra evento, servings y devolución en un problema nuevo.", "Evento para 6 invitados: cada uno necesita 2 porciones (servings) y 2 vasos; el recibo lista 12 vasos, la entrega trae 6: faltan 6. Hay demasiadas bolsas, pero suficiente comida. Pide devolución.", "For the event, six guests need two servings and two cups each; the receipt lists twelve cups, but six arrived, so six are missing. There are too many bags, but we have enough food. We should request a refund.", ["For the event, six guests need two servings and two cups each; the receipt lists twelve cups, but six arrived, so six are missing. There are too many bags, but we have enough food. We should request a refund.", "At our event, each of six guests needs two servings and two cups. Only six of the twelve ordered cups arrived, so six are missing. Food is enough despite too many bags; we should ask for a refund."], fb("El repaso recupera evento, invitados, servings, cantidad faltante, comida suficiente, bolsas y la única acción de devolución.", "la producción de repaso", "For the event, six guests need two servings and two cups each; the receipt lists twelve cups, but six arrived, so six are missing. There are too many bags, but we have enough food. We should request a refund.")),
            ],
        },
    },
}


def make_item(item_id, spec, class_concept, pool):
    fmt = spec["format"]
    requires = spec.get("requires", [class_concept])
    teaches = [class_concept] if pool == "practiceGuided" else []
    origin = {"kind": "editorial", "feedback": {"es": spec["feedback"]}}
    if pool == "practiceGuided":
        origin["hint"] = {"es": spec["hint"]}
        requires = []
    item = {
        "id": item_id, "format": fmt, "prompt": {"es": spec["prompt"]},
        "answer": {}, "choices": [], "teaches": teaches, "requires": requires,
        "origin": origin,
        "accessibility": {"screenReader": True, "highContrast": True, "largeText": True},
    }
    if fmt in {"elegir", "escuchar"}:
        item["choices"] = [{"text": value} for value in spec["choices"]]
        item["answer"] = {"index": spec["answerIndex"]}
        if fmt == "escuchar":
            origin.update({"audio": spec["audio"], "audioMode": "tts", "languageCode": "en",
                           "speedOptions": [0.75, 1.0], "maxReplays": 3,
                           "revealTranscriptAfterAttempt": True})
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
        pairs = [[left, {"es": right}] for left, right in spec["pairs"]]
        item["answer"] = {"pairs": pairs}
        origin["pairs"] = pairs
    else:
        raise ValueError(fmt)
    return add_hash(item)


def normalize_specs(number):
    spec = SPECS[number]
    rule = spec["rule"]
    pools = {}
    for pool_name, item_specs in spec["pools"].items():
        pools[pool_name] = []
        for index, raw in enumerate(item_specs, 1):
            item = dict(raw)
            item["hint"] = raw.get("hint", "Busca el sustantivo y su expresión de cantidad.")
            item["format"] = raw["format"]
            item["feedback"] = raw["feedback"]
            pools[pool_name].append(item)
    return pools


def build_class(number):
    concept = CONCEPTS[number]
    class_id = f"en.n2.class-{number:02d}"
    spec = SPECS[number]
    teaching = []
    for index, (en, es, explanation) in enumerate(spec["teaching"], 1):
        teaching.append({
            "id": f"{class_id}.t{index:02d}", "en": en, "es": es,
            "explanationEs": explanation, "segments": segments(en, es),
            "audioText": en, "audioMode": "tts", "languageCode": "en",
            "patternId": concept,
        })
    prefixes = {"practiceGuided": "pg", "practice": "p", "evaluation": "e", "review": "r"}
    pools = {}
    for pool_name, item_specs in spec["pools"].items():
        pools[pool_name] = [
            make_item(f"en.n2.c{number:02d}.{prefixes[pool_name]}{index:02d}", item, concept, pool_name)
            for index, item in enumerate(item_specs, 1)
        ]
    cumulative = CUMULATIVE if number == 55 else [concept]
    result = {
        "schema": "onelingo.editorial.class.v1", "course": "en", "level": 2,
        "scale": SCALE, "status": "shadow", "runtimeAi": False,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": {
            "chronologyTokens": "enforce", "answerReuseAcrossEarlyReserved": "forbid",
            "answerEvidenceReuseAcrossPools": "forbid", "agentContract": "editorial-agent.v2",
            "minChoices": 3, "maxPromptCharacters": 90,
            "feedbackReuseWithinClass": "forbid", "minClassFormats": 4,
        },
        "id": class_id, "phase": PHASES[number], "title": {"en": TITLES[number][0], "es": TITLES[number][1]},
        "concepts": [concept], "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [f"en.n2.class-{number - 1:02d}"],
        "usesVocabulary": [en for en, _ in spec["vocab"]], "usesPatterns": cumulative,
        "objectives": {"es": [
            f"Reconocer {TITLES[number][1].lower()} en mensajes breves de nivel A2.",
            {
                51: "Distinguir sustantivos contables e incontables en compras sencillas.",
                52: "Elegir a few, a little y enough según la cantidad disponible.",
                53: "Contrastar too much y too many en problemas cotidianos.",
                54: "Calcular cantidades suficientes para invitados y materiales de un evento.",
                55: "Explicar un problema de compra y proponer una solución concreta.",
            }[number],
            f"Producir una respuesta breve sobre {TITLES[number][1].lower()} sin apoyo dinámico.",
        ]},
        "vocabulary": [{"en": en, "es": es} for en, es in spec["vocab"]],
        "teaching": teaching, "pools": pools,
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
    if number == 55:
        result["cumulativeEvaluation"] = CUMULATIVE
    return result


def audit_class(cls):
    prompts = []
    feedback = []
    for pool in cls["pools"].values():
        for item in pool:
            prompts.append(item["prompt"]["es"])
            feedback.append(item["origin"]["feedback"]["es"])
    assert len(prompts) == len(set(prompts))
    assert len(feedback) == len(set(feedback))
    assert max(map(len, prompts)) <= 90
    assert len({item["format"] for pool in cls["pools"].values() for item in pool}) >= 4
    assert any(item["format"] == "escribir" for pool in cls["pools"].values() for item in pool)


def write_class(number):
    cls = build_class(number)
    audit_class(cls)
    path = OUT / f"class-{number:02d}.json"
    path.write_text(json.dumps(cls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)


def write_bundle():
    classes = [json.loads((OUT / f"class-{number:02d}.json").read_text(encoding="utf-8")) for number in range(51, 56)]
    for cls in classes:
        audit_class(cls)
    objectives = [objective for cls in classes for objective in cls["objectives"]["es"]]
    assert len(objectives) == len(set(objectives))
    bundle = {
        "schema": "onelingo.editorial.class-bundle.v1", "course": "en", "level": 2,
        "scale": SCALE, "status": "shadow", "runtimeAi": False, "classes": classes,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
    }
    path = OUT / "bundle-51-55.json"
    path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--class-number", type=int, choices=range(51, 56))
    group.add_argument("--bundle", action="store_true")
    args = parser.parse_args()
    if args.bundle:
        write_bundle()
    else:
        write_class(args.class_number)


if __name__ == "__main__":
    main()
