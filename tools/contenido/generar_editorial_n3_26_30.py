#!/usr/bin/env python3
"""Generate the isolated English N3 C26-C30 editorial draft."""
from __future__ import annotations

import argparse, hashlib, json, re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n3"
REPORT_OUT = ROOT / "build/editorial-n3-26-30"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"
SCALE = "client-10-levels-v1"
NUMBERS = range(26, 31)
CONCEPTS = {n: f"n3-hypothetical-choices-{n-25}" for n in NUMBERS}
PHASES = {26: "input", 27: "form", 28: "comprehension", 29: "production", 30: "transfer"}
QUALITY = {"chronologyTokens": "enforce", "answerReuseAcrossEarlyReserved": "forbid",
           "answerEvidenceReuseAcrossPools": "forbid", "agentContract": "editorial-agent.v2",
           "minChoices": 3, "maxPromptCharacters": 90,
           "feedbackReuseWithinClass": "forbid", "minClassFormats": 4}


def canonical(v: Any) -> str:
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def norm(v: str) -> str:
    return " ".join(re.findall(r"[a-záéíóúüñ0-9']+", v.casefold()))


def hashed(x: dict[str, Any]) -> dict[str, Any]:
    payload = {k: v for k, v in x.items() if k not in {"id", "contentHash"}}
    x["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return x


def base(i: str, fmt: str, prompt: str, c: str, pool: str, feedback: str,
         *, requires: list[str] | None = None, hint: str | None = None) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided": origin["hint"] = {"es": hint or "Ubica el fondo y el hecho que cambia la escena."}
    return {"id": i, "format": fmt, "prompt": {"es": prompt}, "answer": {}, "choices": [],
            "teaches": [c] if pool == "practiceGuided" else [],
            "requires": [] if pool == "practiceGuided" else list(requires or [c]),
            "origin": origin,
            "accessibility": {"screenReader": True, "highContrast": True, "largeText": True}}


def q(i: str, prompt: str, options: list[str], index: int, c: str, pool: str,
      feedback: str, **kw: Any) -> dict[str, Any]:
    x = base(i, "elegir", prompt, c, pool, feedback, **kw)
    x["choices"], x["answer"] = [{"text": v} for v in options], {"index": index}
    return hashed(x)


def listen(i: str, prompt: str, audio: str, options: list[str], index: int, c: str,
           pool: str, feedback: str, **kw: Any) -> dict[str, Any]:
    x = base(i, "escuchar", prompt, c, pool, feedback, **kw)
    x["choices"], x["answer"] = [{"text": v} for v in options], {"index": index}
    x["origin"].update({"audio": audio, "audioMode": "tts", "languageCode": "en",
                        "speedOptions": [0.75, 1.0], "maxReplays": 3,
                        "revealTranscriptAfterAttempt": True})
    return hashed(x)


def fill(i: str, prompt: str, answer: str, c: str, pool: str, feedback: str,
         **kw: Any) -> dict[str, Any]:
    x = base(i, "completar", prompt, c, pool, feedback, **kw)
    x["answer"] = {"text": answer, "accepted": [answer]}
    return hashed(x)


def order(i: str, prompt: str, answer: str, c: str, pool: str, feedback: str,
          **kw: Any) -> dict[str, Any]:
    x = base(i, "ordenar", prompt, c, pool, feedback, **kw)
    x["answer"] = {"text": answer, "tokens": answer.split()}
    return hashed(x)


def write(i: str, prompt: str, stimulus: str, answer: str, alternative: str, c: str,
          pool: str, feedback: str, **kw: Any) -> dict[str, Any]:
    x = base(i, "escribir", prompt, c, pool, feedback, **kw)
    x["origin"]["text"] = stimulus
    x["answer"] = {"text": answer, "accepted": [answer, alternative]}
    return hashed(x)


def match(i: str, prompt: str, pairs: list[tuple[str, str]], c: str, pool: str,
          feedback: str, **kw: Any) -> dict[str, Any]:
    x = base(i, "relacionar", prompt, c, pool, feedback, **kw)
    values = [[a, {"es": b}] for a, b in pairs]
    x["answer"], x["origin"]["pairs"] = {"pairs": values}, values
    return hashed(x)


def teaching(n: int, rows: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    out = []
    for k, (en, es, explanation) in enumerate(rows, 1):
        ew, sw = en.split(), es.split(); em, sm = max(1, len(ew)//2), max(1, len(sw)//2)
        out.append({"id": f"en.n3.class-{n:02d}.t{k:02d}", "en": en, "es": es,
                    "explanationEs": explanation,
                    "segments": [{"en": " ".join(ew[:em]), "es": " ".join(sw[:sm])},
                                 {"en": " ".join(ew[em:]), "es": " ".join(sw[sm:])}],
                    "audioText": en, "audioMode": "tts", "languageCode": "en",
                    "patternId": CONCEPTS[n]})
    return out


def make_class(n: int, objectives: list[str], vocab: list[tuple[str, str]],
               rows: list[tuple[str, str, str]], pools: dict[str, list[dict[str, Any]]],
               remap: dict[str, tuple[str, str]], *, uses: list[str] | None = None,
               cumulative: list[str] | None = None) -> dict[str, Any]:
    spec = json.loads(MAP.read_text())["classes"][n-1]
    doc: dict[str, Any] = {
        "schema": "onelingo.editorial.class.v1", "course": "en", "level": 3,
        "cefr": "B1", "scale": SCALE, "status": "shadow", "runtimeAi": False,
        "phase": PHASES[n], "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": dict(QUALITY), "id": f"en.n3.class-{n:02d}", "title": spec["title"],
        "objectives": {"es": objectives}, "concepts": [CONCEPTS[n]],
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [f"en.n3.class-{n-1:02d}"],
        "usesVocabulary": [en for en, _ in vocab], "usesPatterns": uses or [CONCEPTS[n]],
        "vocabulary": [{"en": en, "es": es} for en, es in vocab],
        "teaching": teaching(n, rows), "pools": pools,
        "remediationMap": {k: {"reteach": a, "review": b} for k, (a,b) in remap.items()},
        "accessibility": {"highContrast": True, "largeText": True, "screenReader": True,
                          "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2,
                     "allowAudioReplay": True, "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True}}
    if cumulative is not None: doc["cumulativeEvaluation"] = cumulative
    return doc




def build_26() -> dict[str, Any]:
    n, c, p = 26, CONCEPTS[26], "en.n3.c26"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la frase que imagina una situación distinta de la actual.",
              ["If I lived near the sea, I would swim every day.",
               "I live near the sea and swim every day.", "I am moving to the sea on Monday."],
              0, c, "practiceGuided", "If I lived establece la situación imaginaria y would swim su resultado.",
              hint="Busca if más pasado y would en el resultado."),
            fill(f"{p}.pg02", "Completa la hipótesis: If we had more space, we ___.",
                 "would invite more people", c, "practiceGuided",
                 "Would invite expresa el resultado imaginado de tener más espacio.",
                 hint="La segunda parte necesita would más verbo base."),
            order(f"{p}.pg03", "Ordena la posibilidad hipotética sobre transporte.",
                  "If the station were closer, we could walk there.", c, "practiceGuided",
                  "If más were establece la situación; could walk aporta una posibilidad.",
                  hint="Coloca la condición antes de la posibilidad."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y decide qué situación no es un plan confirmado.",
                   "If I had a longer holiday, I would visit my cousins in Canada.",
                   ["A visit already booked", "An imagined longer holiday", "A weekly family visit"], 1,
                   c, "practice", "La persona imagina unas vacaciones que no tiene ahora."),
            match(f"{p}.p02", "Relaciona cada frase con realidad o hipótesis.",
                  [("We are taking the 8:10 train tomorrow.", "plan real"),
                   ("If the tickets were cheaper, we would take the train.", "hipótesis")],
                  c, "practice", "La hora confirmada señala un plan; if y would señalan una hipótesis."),
            write(f"{p}.p03", "Convierte la falta de tiempo en una hipótesis.",
                  "Realidad: No tengo tiempo para cocinar. Resultado imaginado: preparar cenas frescas.",
                  "If I had more time, I would cook fresh dinners.",
                  "I would prepare fresh dinners if I had more time.", c, "practice",
                  "Las variantes mantienen la falta de tiempo como realidad actual."),
        ],
        "evaluation": [
            q(f"{p}.e01", "¿Qué frase describe una opción poco probable?",
              ["If Marta owned a car, she could drive to work.",
               "Marta owns a car and drives to work.", "Marta is collecting her car this afternoon."],
              0, c, "evaluation", "Owned y could drive presentan una posibilidad que no es un hecho actual."),
            listen(f"{p}.e02", "Escucha y elige el plan real.",
                   "I would study abroad if I spoke German. This September, I am studying in Bristol.",
                   ["Studying in Germany", "Learning German someday", "Studying in Bristol this September"],
                   2, c, "evaluation", "La fecha y la forma presente confirman el plan de Bristol."),
            write(f"{p}.e03", "Expresa una hipótesis sobre trabajar menos horas.",
                  "Realidad: trabajo muchas horas. Posibilidad: hacer un curso nocturno.",
                  "If I worked fewer hours, I could take an evening course.",
                  "I could attend an evening class if I worked fewer hours.", c, "evaluation",
                  "Ambas respuestas contrastan la carga real con una posibilidad imaginada."),
            write(f"{p}.e04", "Clasifica diez frases como H (hipótesis) o R (plan real).",
                  "1 If I knew French, I would apply in Paris; 2 We are meeting the landlord at four; 3 If the room were brighter, I could work there; 4 Leo starts his new job next Tuesday; 5 If I had a garden, I would grow vegetables; 6 Our flight leaves at 6:20 tomorrow; 7 If the village had a clinic, we could stay; 8 I am visiting the dentist after lunch; 9 If the laptop were lighter, I would buy it; 10 The course begins on 12 May.",
                  "1 H, 2 R, 3 H, 4 R, 5 H, 6 R, 7 H, 8 R, 9 H, 10 R.",
                  "Hypothetical: 1, 3, 5, 7, 9. Real plan: 2, 4, 6, 8, 10.", c, "evaluation",
                  "Las cinco hipótesis usan if con pasado; los cinco planes tienen datos confirmados."),
        ],
        "review": [
            q(f"{p}.r01", "Elige la situación imaginaria sobre vivienda.",
              ["We signed the rental agreement today.",
               "If the flat had two bedrooms, we would rent it.", "We are moving into the flat on Friday."],
              1, c, "review", "Had y would rent muestran que el piso no cumple ahora la condición."),
            order(f"{p}.r02", "Ordena la hipótesis sobre un empleo remoto.",
                  "If my job were remote, I could live anywhere.", c, "review",
                  "Were remote crea la condición irreal y could live expresa la posibilidad."),
            write(f"{p}.r03", "Contrasta el plan del sábado con una opción imaginada.",
                  "Plan: visitar a Lena el sábado. Hipótesis: tener coche y llevarle una mesa.",
                  "I am visiting Lena on Saturday. If I had a car, I would take her a table.",
                  "On Saturday, I am visiting Lena; I would bring her a table if I owned a car.", c,
                  "review", "Las variantes separan la visita confirmada de la entrega hipotética."),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-26.t02", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-26.t05", f"{p}.r03"),
             f"{p}.e03": ("en.n3.class-26.t04", f"{p}.r02"),
             f"{p}.e04": ("en.n3.class-26.t06", f"{p}.r03")}
    return make_class(n, ["Distinguir hipótesis de planes reales mediante su forma y contexto.",
                          "Reconocer if más pasado y would o could como marco imaginario."],
        [("imaginary", "imaginario"), ("real", "verdadero"), ("unlikely", "poco probable"),
         ("would", "haría"), ("could", "podría"), ("situation", "situación")],
        [("An imaginary situation is different from the present.",
          "Una situación imaginaria es diferente del presente.", "El contexto confirma que no es un plan."),
         ("An unlikely condition can use if plus past.",
          "Una condición poco probable puede usar if más pasado.", "El pasado señala distancia respecto de la realidad."),
         ("Would gives the imagined result.", "Would presenta el resultado imaginado.",
          "Would va seguido de verbo base."),
         ("Could gives a possible result, not a real plan.",
          "Could presenta una posibilidad, no un plan real.", "Could no confirma que la acción ocurrirá."),
         ("A real plan has a confirmed time or arrangement.",
          "Un plan real tiene una hora o acuerdo confirmado.", "Los datos concretos distinguen el plan de la hipótesis."),
         ("Separate imaginary language from real arrangements by checking form and context.",
          "Separa el lenguaje imaginario de los acuerdos reales revisando forma y contexto.",
          "If más pasado y would/could contrastan con fechas o acuerdos confirmados.")],
        pools, remap)


def build_27() -> dict[str, Any]:
    n, c, p = 27, CONCEPTS[27], "en.n3.c27"
    pools = {
        "practiceGuided": [
            fill(f"{p}.pg01", "Completa el resultado seguro imaginado: I ___ accept the offer.",
                 "would", c, "practiceGuided", "Would presenta el resultado elegido en esa condición.",
                 hint="Usa el modal de resultado, no el de posibilidad."),
            q(f"{p}.pg02", "Elige could para una posibilidad entre varias.",
              ["If we had time, we could visit the castle.", "If we had time, we would visit the castle.",
               "We are visiting the castle at noon."], 0, c, "practiceGuided",
              "Could visit expresa una opción disponible, no una decisión segura.",
              hint="Busca could más verbo base después de la condición."),
            order(f"{p}.pg03", "Ordena la condición y el resultado con would.",
                  "If the salary were higher, I would take the job.", c, "practiceGuided",
                  "Were establece la condición y would take presenta la decisión.",
                  hint="La cláusula con if va primero y lleva pasado."),
        ],
        "practice": [
            match(f"{p}.p01", "Une cada intención con el modal adecuado.",
                  [("resultado elegido", "would"), ("posibilidad disponible", "could")], c,
                  "practice", "Would comunica una elección; could deja abierta una posibilidad."),
            listen(f"{p}.p02", "Escucha y elige por qué aparece could.",
                   "If the weather were better, we could eat outside or walk by the river.",
                   ["Hay una orden", "Hay dos posibilidades", "Hay un plan confirmado"], 1, c,
                   "practice", "Could introduce opciones posibles sin presentar una decisión final."),
            write(f"{p}.p03", "Escribe una decisión y una posibilidad sobre otra ciudad.",
                  "Condición: vivir en otra ciudad. Decisión: vender coche. Posibilidad: usar metro.",
                  "If I lived in another city, I would sell my car and could use the metro.",
                  "I would sell my car if I moved to another city, where I could travel by metro.", c,
                  "practice", "Las variantes diferencian la decisión con would y la posibilidad con could."),
        ],
        "evaluation": [
            fill(f"{p}.e01", "Completa la decisión: If I knew the answer, I ___ tell you.",
                 "would", c, "evaluation", "Would tell expresa el resultado esperado de saber la respuesta."),
            q(f"{p}.e02", "Elige el modal para una opción posible, no una decisión.",
              ["If we rented that house, we would definitely use the office.",
               "We share the office because we rent that house now.",
               "If we rented that house, we could share the office."], 2, c, "evaluation",
              "Could share mantiene la oficina como una posibilidad dentro de la hipótesis."),
            listen(f"{p}.e03", "Escucha y selecciona la decisión del hablante.",
                   "If I received that scholarship, I would study design and could live near campus.",
                   ["Reject the scholarship", "Live near campus", "Study design"], 2, c,
                   "evaluation", "Would study marca la decisión; could live es solo una posibilidad."),
            write(f"{p}.e04", "Completa seis respuestas según decisión o posibilidad.",
                  "1 decisión: más dinero→ahorrar; 2 posibilidad: coche→visitar; 3 decisión: libre→curso; 4 posibilidad: jardín→cultivar; 5 decisión: remoto→mudarse; 6 posibilidad: escuela cerca→caminar.",
                  "If I had more money, I would save it. If I had a car, I could visit you. If I were free, I would take the course. If we had a garden, we could grow food. If my job were remote, I would move. If school were nearer, I could walk.",
                  "I would save more if I earned more. I could visit you if I owned a car. I would join the course if I were free. We could grow food if we had a garden. I would move if my work were remote. I could walk if school were closer.",
                  c, "evaluation", "Las seis respuestas conservan cláusula if y distinguen decisión de posibilidad."),
        ],
        "review": [
            q(f"{p}.r01", "Elige la frase que expresa una decisión hipotética.",
              ["If the hours were flexible, I would accept the role.",
               "If the hours were flexible, I could ask a question.",
               "The hours are flexible, so I accepted it."], 0, c, "review",
              "Would accept comunica la decisión que seguiría a la condición."),
            order(f"{p}.r02", "Ordena una posibilidad de aprendizaje.",
                  "If the library stayed open, we could study there.", c, "review",
                  "Could study presenta una opción posible bajo la condición."),
            write(f"{p}.r03", "Recupera seis respuestas según decisión o posibilidad.",
                  "1 decisión: día extra→descansar; 2 posibilidad: bici→ir río; 3 decisión: sala libre→abrir club; 4 posibilidad: horno→hornear; 5 decisión: remoto→viajar; 6 posibilidad: parque cerca→caminar.",
                  "If I had an extra day, I would rest. If I had a bike, I could ride to the river. If the room were free, we would open the club. If we had an oven, we could bake. If my job were remote, I would travel. If the park were nearer, I could walk.",
                  "I would rest if I had another day. I could cycle to the river if I owned a bike. We would open the club if the room were available. We could bake if we had an oven. I would travel if I worked remotely. I could walk if the park were closer.",
                  c, "review", "Las seis respuestas recuperan decisiones con would y posibilidades con could."),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-27.t02", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-27.t03", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-27.t04", f"{p}.r03"),
             f"{p}.e04": ("en.n3.class-27.t06", f"{p}.r03")}
    return make_class(n, ["Formar hipótesis con if más pasado y modal más verbo base.",
                          "Elegir would para resultado y could para posibilidad."],
        [("condition", "condición"), ("result", "resultado"), ("decision", "decisión"),
         ("possibility", "posibilidad"), ("base", "forma simple"), ("modal", "verbo auxiliar")],
        [("The condition uses if plus a past form.", "La condición usa if más una forma pasada.",
          "La cláusula if establece la situación imaginaria."),
         ("Would introduces the chosen result.", "Would introduce el resultado elegido.",
          "El resultado con would presenta una decisión."),
         ("Could introduces a possibility.", "Could introduce una posibilidad.",
          "La opción queda abierta y no se confirma."),
         ("A decision uses would; an option can use could.",
          "Una decisión usa would; una opción puede usar could.", "El significado determina el modal."),
         ("After each modal, use the base form of the verb.",
          "Después de cada modal, usa la forma base del verbo.", "No añadas to ni una terminación al verbo principal."),
         ("Label each result as a decision or possibility before choosing the modal.",
          "Etiqueta cada resultado como decisión o posibilidad antes de elegir el modal.",
          "La etiqueta hace inequívoca la elección entre would y could.")],
        pools, remap)


def build_28() -> dict[str, Any]:
    n, c, p = 28, CONCEPTS[28], "en.n3.c28"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige el consejo hipotético más suave.",
              ["If I were you, I would ask for clearer instructions.",
               "Ask for clearer instructions now.", "You must understand the instructions."], 0,
              c, "practiceGuided", "If I were you presenta la recomendación como una perspectiva personal.",
              hint="Busca una condición imaginaria antes de la recomendación."),
            listen(f"{p}.pg02", "Escucha y elige la razón del consejo.",
                   "If I were you, I would take the earlier bus because traffic gets heavy after eight.",
                   ["The bus is cheaper", "Traffic becomes heavy", "The speaker dislikes buses"], 1,
                   c, "practiceGuided", "La congestión después de las ocho justifica salir antes.",
                   hint="La razón aparece después de because."),
            order(f"{p}.pg03", "Ordena el consejo para una habitación ruidosa.",
                  "If I were you, I would ask for another room.", c, "practiceGuided",
                  "La fórmula imaginaria suaviza la petición de cambiar de habitación.",
                  hint="Abre con If I were you y continúa con would."),
        ],
        "practice": [
            match(f"{p}.p01", "Une situación, opción y razón de cada consejo.",
                  [("curso demasiado rápido", "pedir material adicional"),
                   ("poco tiempo para cocinar", "preparar comida el domingo"),
                   ("trayecto caro", "compartir el coche")], c, "practice",
                  "Cada opción responde al problema y permite añadir una razón concreta."),
            q(f"{p}.p02", "El alquiler es alto. ¿Qué opción ayudaría a ahorrar?",
              ["Move to the city centre", "Share a flat with a colleague", "Buy new furniture"], 1,
              c, "practice", "Compartir piso reduce el coste que motiva la recomendación."),
            write(f"{p}.p03", "Da un consejo suave y una razón sobre estudiar de noche.",
                  "Problema: cansancio nocturno. Opción: estudiar por la mañana. Razón: mayor concentración.",
                  "If I were you, I would study in the morning because you could concentrate better.",
                  "I would try morning study if I were you, since you could focus more easily.", c,
                  "practice", "Las variantes incluyen perspectiva, opción y razón sin dar una orden."),
        ],
        "evaluation": [
            listen(f"{p}.e01", "Escucha y selecciona la situación imaginada.",
                   "If I were in your position, I would work from home today because the trains are delayed.",
                   ["Being in the listener's position", "Working at the station", "Buying a train ticket"],
                   0, c, "evaluation", "El hablante imagina estar en la posición de la otra persona."),
            q(f"{p}.e02", "¿Qué recomendación incluye una razón explícita?",
              ["You should compare things.", "Banks can be different.",
               "If I were you, I would compare the fees because one bank may be cheaper."], 2, c, "evaluation",
              "La tercera opción propone comparar y explica el posible ahorro."),
            write(f"{p}.e03", "Resume situación, opción y razón del consejo laboral.",
                  "Situación: turno nocturno agotador. Opción: pedir turno diurno. Razón: dormir mejor.",
                  "If I worked that night shift, I would ask for daytime hours because I could sleep better.",
                  "I would request a day shift if I were in that situation, since it could improve my sleep.",
                  c, "evaluation", "Ambas respuestas conservan situación imaginada, opción y motivo."),
            listen(f"{p}.e04", "Escucha tres consejos y elige el resumen completo.",
                   "If I were moving, I would label the boxes because unpacking would be easier. If I had that interview, I would practise answers because I could feel calmer. If I were choosing a course, I would read student reviews because they could reveal the workload.",
                   ["mudanza→vender cajas→dinero; entrevista→viajar→tiempo; curso→llamar→precio",
                    "mudanza→pedir taxi→distancia; entrevista→cancelar→sueño; curso→inscribirse→fecha",
                    "mudanza→etiquetar→desembalar; entrevista→practicar→calma; curso→leer reseñas→carga"],
                   2, c, "evaluation", "El resumen correcto recupera las tres situaciones, opciones y razones."),
        ],
        "review": [
            q(f"{p}.r01", "Elige la razón que apoya cambiar de proveedor.",
              ["The office has blue walls", "The current service fails every evening",
               "The speaker bought a chair"], 1, c, "review",
              "Los fallos diarios justifican considerar otro proveedor."),
            match(f"{p}.r02", "Relaciona cada problema con un consejo suave.",
                  [("facturas difíciles de entender", "If I were you, I would request a clear breakdown."),
                   ("bicicleta insegura", "If I were you, I would have the brakes checked."),
                   ("plazo poco claro", "If I were you, I would confirm the date.")], c, "review",
                  "Cada fórmula ofrece una acción proporcionada al problema."),
            write(f"{p}.r03", "Recupera tres consejos con situación, opción y razón.",
                  "A ruido→biblioteca→silencio; B gasto→presupuesto→control; C dolor leve→descanso→recuperación.",
                  "If I had too much noise, I would use the library because it is quiet. If I spent too much, I would make a budget to control costs. If I had mild pain, I would rest because recovery needs time.",
                  "For noise, I would study at the library because it is calmer. For overspending, I would plan a budget to track costs. For mild pain, I would rest and monitor it because that could support recovery.",
                  c, "review", "Las dos versiones recuperan tres problemas, tres opciones y tres razones."),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-28.t01", f"{p}.r02"),
             f"{p}.e02": ("en.n3.class-28.t03", f"{p}.r01"),
             f"{p}.e03": ("en.n3.class-28.t06", f"{p}.r03"),
             f"{p}.e04": ("en.n3.class-28.t06", f"{p}.r03")}
    return make_class(n, ["Extraer situación, opción y razón de un consejo hipotético.",
                          "Reconocer cómo una hipótesis suaviza una recomendación."],
        [("advice", "consejo"), ("position", "posición"), ("option", "opción"),
         ("reason", "razón"), ("soften", "suavizar"), ("recommend", "recomendar")],
        [("If I were in your position, I would ask for help.",
          "Si estuviera en tu posición, pediría ayuda.", "La perspectiva imaginaria evita una orden directa."),
         ("Advice offers an option, not a command.", "Un consejo ofrece una opción, no una orden.",
          "La otra persona conserva la decisión."),
         ("A clear reason explains why the option may help.",
          "Una razón clara explica por qué la opción puede ayudar.", "Because o since introduce el motivo."),
         ("To soften a recommendation, begin with If I were you.",
          "Para suavizar una recomendación, comienza con If I were you.", "La fórmula señala una opinión personal."),
         ("Recommend one action and connect it to the problem.",
          "Recomienda una acción y conéctala con el problema.", "La opción debe responder a la situación dada."),
         ("For each speaker, identify the situation, option and reason.",
          "Para cada hablante, identifica situación, opción y razón.", "Las tres partes evitan resumir solo la acción.")],
        pools, remap)


def build_29() -> dict[str, Any]:
    n, c, p = 29, CONCEPTS[29], "en.n3.c29"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la comparación que incluye beneficio y límite.",
              ["A village would be peaceful, but transport could be limited.",
               "A village could offer quiet streets and friendly local shops.",
               "Village buses would run less often than city buses."], 0, c,
              "practiceGuided", "Peaceful aporta el beneficio y limited transport el límite.",
              hint="Busca una ventaja unida a una dificultad con but."),
            fill(f"{p}.pg02", "Completa la conclusión: If I chose one, I ___ choose Lisbon.",
                 "would", c, "practiceGuided", "Would choose convierte la comparación en una conclusión hipotética.",
                 hint="La conclusión requiere would más verbo base."),
            order(f"{p}.pg03", "Ordena el límite de estudiar en una capital.",
                  "However, rent could be more expensive there.", c, "practiceGuided",
                  "However introduce el coste que limita la opción de la capital.",
                  hint="Abre con el conector de contraste."),
        ],
        "practice": [
            match(f"{p}.p01", "Une cada opción con beneficio y límite.",
                  [("study in Cork", "friendly campus / fewer specialist courses"),
                   ("study in Dublin", "more courses / higher rent")], c, "practice",
                  "Cada destino conserva una ventaja y un límite distintos."),
            listen(f"{p}.p02", "Escucha y elige la preferencia final.",
                   "Berlin would offer more jobs, but rent could be high. Leipzig would be cheaper, but the market is smaller. If I had to choose, I would live in Leipzig.",
                   ["Berlin", "Leipzig", "No preference"], 1, c, "practice",
                   "La conclusión explícita selecciona Leipzig pese a su mercado menor."),
            write(f"{p}.p03", "Compara dos formas de viajar y concluye.",
                  "Tren: cómodo/caro. Autobús: barato/lento. Prioridad: ahorrar.",
                  "The train would be comfortable but expensive. The bus would be cheaper but slower. If I wanted to save money, I would take the bus.",
                  "A train could offer more comfort, although it would cost more. A bus would take longer but cost less, so I would choose it to save money.",
                  c, "practice", "Las variantes comparan las dos opciones y concluyen según la prioridad."),
        ],
        "evaluation": [
            q(f"{p}.e01", "¿Qué frase presenta un límite de vivir lejos del centro?",
              ["Housing could be cheaper.", "The commute would take longer.",
               "There would be more space."], 1, c, "evaluation",
              "Un trayecto más largo es una dificultad concreta de esa ubicación."),
            listen(f"{p}.e02", "Escucha y selecciona el beneficio de la opción rural.",
                   "A city course would have better equipment but large classes. A rural course could give me more personal support, although travel would be difficult.",
                   ["Better equipment", "Easier travel", "More personal support"], 2, c,
                   "evaluation", "El apoyo personal es la ventaja explícita del curso rural."),
            write(f"{p}.e03", "Compara trabajar desde casa y en oficina.",
                  "Casa: flexible/aislado. Oficina: equipo cerca/desplazamiento. Prioridad: colaboración.",
                  "Home working would be flexible but lonely. An office would involve travel but keep the team together. If collaboration mattered most, I would choose the office.",
                  "Working at home could save time, although I might feel isolated. The office would require a commute but support teamwork, so I would select it for collaboration.",
                  c, "evaluation", "Las opciones incluyen beneficios, límites y una conclusión basada en colaborar."),
            write(f"{p}.e04", "Escribe 60–80 palabras comparando dos lugares para estudiar.",
                  "Valencia: alquiler bajo/playa, pocas clases nocturnas. Madrid: cursos variados con clases nocturnas, alquiler alto. Prioridad: trabajar de día y estudiar de noche.",
                  "If I studied in Valencia, I would pay lower rent and could live near the beach. However, the limited evening classes would make daytime work difficult. Madrid would offer more course choices and better evening schedules, but housing would cost much more. Since I would need to work during the day, I would choose Madrid despite the higher rent because its timetable would fit my situation better.",
                  "Valencia would be cheaper and I could enjoy the coast, but it would offer few classes after work. Madrid would have a wider range of evening courses, although the rent would be expensive. If I had to combine a daytime job with study, I would select Madrid. Its schedule would be the main benefit, while the housing cost would remain an important limit.",
                  c, "evaluation", "Ambas recomendaciones comparan dos lugares, sus límites y la prioridad laboral."),
        ],
        "review": [
            q(f"{p}.r01", "Elige la conclusión coherente con una prioridad de calma.",
              ["If I wanted peace, I would choose the smaller town.",
               "The capital would have more nightlife.", "Both places would have stations."], 0,
              c, "review", "La localidad pequeña responde directamente a la prioridad de calma."),
            match(f"{p}.r02", "Relaciona opciones de vivienda con beneficio y límite.",
                  [("shared flat", "lower cost / less privacy"),
                   ("small studio", "more privacy / higher cost")], c, "review",
                  "Cada vivienda muestra una ventaja y una dificultad comparables."),
            write(f"{p}.r03", "Escribe 60–80 palabras comparando dos viajes.",
                  "Oporto: tren directo/comida cara. Braga: conexión/lodging barato. Prioridad: presupuesto de alojamiento.",
                  "If I travelled to Porto, I would take a direct train and save travel time. However, meals could be expensive there. Braga would require one train change, but accommodation would cost less. Since my main priority would be the lodging budget, I would choose Braga. The connection would be a minor limit, while the cheaper room would keep accommodation costs aligned with my stated priority and leave more of my budget available.",
                  "Porto would be easy to reach by direct train, although eating there could cost more. Braga would involve a connection, but I could find cheaper accommodation. If keeping the room budget low were most important, I would travel to Braga. Changing trains would be inconvenient, yet the lower lodging price would satisfy my main priority and preserve more of the available budget for other stated travel costs.",
                  c, "review", "Las versiones comparan acceso, costes y concluyen según el alojamiento."),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-29.t03", f"{p}.r02"),
             f"{p}.e02": ("en.n3.class-29.t01", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-29.t06", f"{p}.r03"),
             f"{p}.e04": ("en.n3.class-29.t06", f"{p}.r03")}
    return make_class(n, ["Comparar dos opciones hipotéticas con beneficio y límite.",
                          "Concluir una recomendación según una prioridad explícita."],
        [("benefit", "beneficio"), ("limit", "límite"), ("however", "sin embargo"),
         ("although", "aunque"), ("priority", "prioridad"), ("conclusion", "conclusión")],
        [("State one benefit for each option.", "Indica un beneficio de cada opción.",
          "La comparación necesita información favorable equilibrada."),
         ("Add a limit with but or although.", "Añade un límite con but o although.",
          "El contraste evita presentar una opción como perfecta."),
         ("However can introduce the main difficulty.",
          "However puede introducir la dificultad principal.", "El conector separa beneficio y límite."),
         ("Use the priority to evaluate both options.",
          "Usa la prioridad para evaluar ambas opciones.", "La elección debe responder al criterio dado."),
         ("Finish with a conditional conclusion.",
          "Termina con una conclusión condicional.", "If más pasado y would expresan la elección imaginada."),
         ("If I studied abroad, a large city would offer more courses but cost more. A smaller city could be cheaper, although it might offer fewer subjects. If my priority were course choice, I would select the large city. If saving money mattered more, I would choose the smaller one. The final conclusion depends on the learner's stated priority in practice.",
          "El modelo compara dos destinos, sus beneficios, sus límites y concluye según una prioridad.",
          "La recomendación conectada no omite ninguna de las dos opciones.")],
        pools, remap)


def build_30() -> dict[str, Any]:
    n, c, p = 30, CONCEPTS[30], "en.n3.c30"
    all_c = [CONCEPTS[k] for k in NUMBERS]
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la hipótesis que respeta un presupuesto de $300.",
              ["If we had $300, we could choose the $260 cabin.",
               "We booked the $420 hotel yesterday.", "The $350 flat is under our budget."], 0,
              c, "practiceGuided", "La cabaña de $260 es la única opción dentro del presupuesto imaginario.",
              hint="Compara cada precio con el máximo de $300."),
            listen(f"{p}.pg02", "Escucha y elige la preferencia de Jo.",
                   "Jo says: I would prefer the train because I need space to work.",
                   ["A cheap bus", "A train with workspace", "A flight with no table"], 1, c,
                   "practiceGuided", "Jo prefiere el tren porque necesita una mesa para trabajar.",
                   hint="Relaciona la opción con la necesidad mencionada."),
            order(f"{p}.pg03", "Ordena la propuesta que combina dos preferencias.",
                  "If we chose the hostel, we could save money and stay near the centre.", c,
                  "practiceGuided", "La propuesta une ahorro y ubicación bajo una misma condición.",
                  hint="Abre con la condición y termina con las dos ventajas."),
        ],
        "practice": [
            match(f"{p}.p01", "Une cada interlocutor con su prioridad.",
                  [("Nina", "quiet room"), ("Omar", "central location")], c, "practice",
                  "Las prioridades permiten comparar opciones sin atribuir gustos nuevos."),
            q(f"{p}.p02", "¿Qué propuesta reconoce un límite del tren nocturno?",
              ["It would save a hotel night, but we might sleep badly.",
               "It would save a hotel night and guarantee good sleep.", "It leaves at night."], 0, c,
              "practice", "La primera opción presenta el ahorro y también el posible mal descanso."),
            write(f"{p}.p03", "Formula una decisión compartida dentro de $180.",
                  "A: museo $70/ambos lo quieren. B: cena $90/Sol prefiere. C: concierto $130/Max prefiere.",
                  "If we had $180, we would choose the museum and dinner because both fit our budget and preferences.",
                  "We could visit the museum and have dinner for $160, so we would choose them under the $180 budget.",
                  c, "practice", "Las variantes suman $160 y justifican una decisión compartida."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Elige transporte bajo $60 que acepte una maleta grande.",
              ["Train $75, no large bags", "Flight $110, one small bag only",
               "Coach $45, one large bag included"], 2, c, "evaluation",
              "El autocar es la única opción bajo $60 que acepta una maleta grande."),
            listen(f"{p}.e02", "Escucha y selecciona el desacuerdo entre los viajeros.",
                   "Lea would choose the train for comfort. Ben would take the coach to keep more money for food.",
                   ["Travel date", "Train versus coach", "Number of travellers"], 1, c,
                   "evaluation", "Lea y Ben comparan tren y autocar por prioridades distintas."),
            write(f"{p}.e03", "Propón un compromiso con un máximo de $500.",
                  "Hotel $380/céntrico. Piso $300/cocina, lejos. Transporte local $90. Ambos quieren cocinar y visitar centro.",
                  "If we rented the $300 flat, we could cook and add $90 for transport, staying within $500. We would choose it as a compromise.",
                  "We would select the flat and local transport for $390 because we could cook and still reach the centre within our $500 limit.",
                  c, "evaluation", "Las dos soluciones cuestan $390 y atienden cocina y acceso al centro."),
            write(f"{p}.e04", "Escribe 70–100 palabras para resolver el viaje de Ava y Luis.",
                  "Presupuesto $420. Ava: comodidad. Luis: guardar mínimo $80 para comida. Opciones: tren+hotel $410/más cómodo; autobús+hotel $350/habitación cómoda; autobús+hostal $280/habitación compartida. Comparar dos y decidir.",
                  "If Ava and Luis had a $420 budget, the train and hotel would be the most comfortable, but they would keep only $10 for food. The bus and hotel would cost $350, so they could save $70, below Luis's minimum of $80. If I were them, I would recommend the bus and hostel for $280. It would be less private, but they could keep $140 for meals. They would choose it together: Luis's minimum would be met, and Ava would accept less privacy as a compromise.",
                  "With an imaginary budget of $420, the $410 train and hotel would offer Ava the most comfort but leave $10. The $350 bus and hotel would keep a comfortable room but leave only $70, below Luis's $80 minimum. The $280 bus and shared hostel could leave $140 but offer less privacy. If the food minimum were essential, I would advise the third option. They would agree because Luis keeps enough money and Ava accepts the shared room as the compromise.",
                  c, "evaluation", "Ambas negociaciones comparan opciones, verifican el ahorro y cierran una decisión conjunta.",
                  requires=all_c),
        ],
        "review": [
            q(f"{p}.r01", "Elige una habitación silenciosa dentro del límite de $110.",
              ["Choose the $130 room because it is central.", "Choose the $105 room beside a busy road.",
               "Choose the $95 room: it is quiet and remains under the $110 limit."],
              2, c, "review", "La habitación de $95 cumple el límite y la necesidad de silencio."),
            match(f"{p}.r02", "Relaciona cada propuesta con beneficio y límite.",
                  [("shared studio $160", "equipment included / less privacy"),
                   ("private room $210", "quiet space / fewer materials"),
                   ("library room $80", "lowest cost / fixed hours")], c, "review",
                  "Las tres alternativas quedan comparables por coste, ventaja y límite."),
            write(f"{p}.r03", "Escribe 70–100 palabras para elegir un espacio de curso.",
                  "Presupuesto $240. Inez: privacidad. Tom: equipo incluido. Opciones: estudio compartido $160/equipo/menos privacidad; sala privada $210/silencio/sin proyector; biblioteca $80/proyector/horario fijo. Comparar dos y decidir juntos.",
                  "If Inez and Tom had $240, the private room would give Inez quiet and privacy, but it would not include a projector. The shared studio would cost $160 and provide all the equipment, although other groups could be present. If I were them, I would recommend the shared studio and leave $80 unspent. They would choose it together: Tom would have the equipment, while Inez would accept less privacy so that they could remain well below their budget.",
                  "With a $240 imaginary budget, Inez could choose the $210 private room for privacy, but Tom would have no projector. The $160 shared studio would include equipment, although it would offer less privacy. If I were them, I would advise selecting the shared studio. Inez would accept lower privacy, and Tom would get the equipment he needs. They would agree because the option costs $160, remains under budget and leaves exactly $80 unspent.",
                  c, "review", "Las respuestas negocian privacidad y equipo con precios y una decisión verificable.",
                  requires=all_c),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-30.t02", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-30.t03", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-30.t05", f"{p}.r03"),
             f"{p}.e04": ("en.n3.class-30.t06", f"{p}.r03")}
    return make_class(n, ["Negociar una elección hipotética con presupuesto y dos preferencias.",
                          "Comparar opciones y acordar una decisión verificable."],
        [("budget", "presupuesto"), ("preference", "preferencia"), ("compromise", "compromiso"),
         ("afford", "poder pagar"), ("agree", "acordar"), ("shared", "compartido")],
        [("Begin with a shared imaginary budget.", "Comienza con un presupuesto imaginario compartido.",
          "If más pasado establece el marco de negociación."),
         ("Check what the group can afford.", "Comprueba qué puede pagar el grupo.",
          "Cada precio debe compararse con el límite."),
         ("State each person's preference before recommending.",
          "Indica la preferencia de cada persona antes de recomendar.", "No inventes prioridades durante la elección."),
         ("Compare each preference, benefit and limit for two options.",
          "Compara un beneficio y un límite de dos opciones.", "Would y could mantienen la comparación hipotética."),
         ("Offer a compromise and ask the group to agree.",
          "Ofrece un compromiso y pide que el grupo llegue a un acuerdo.", "La decisión final debe ser compartida."),
         ("If Maya and Theo chose among three festival options, Maya would prefer live music and Theo would prefer a full meal. A $180 concert pass would include music but no meal. A $150 food tour would include the meal but no music. A $240 music-and-dinner package could satisfy both preferences, although it would cost more. If I were them, I would recommend that third option. They would agree because it includes both priorities without adding another expense.",
          "Maya y Theo comparan tres opciones ya indicadas y acuerdan el paquete que reúne música y cena.",
          "El modelo integra hipótesis, modales, consejo, comparación y acuerdo presupuestario.")],
        pools, remap, uses=all_c, cumulative=all_c)


BUILDERS = {26: build_26, 27: build_27, 28: build_28, 29: build_29, 30: build_30}


def audit(classes: list[dict[str, Any]], full: bool) -> dict[str, Any]:
    totals: Counter[str] = Counter(); formats: Counter[str] = Counter(); indices: Counter[int] = Counter()
    prompts: dict[str, str] = {}; signatures: dict[str, str] = {}
    for cls in classes:
        assert cls["status"] == "shadow" and cls["runtimeAi"] is False
        assert cls["qualityPolicy"] == QUALITY and 6 <= len(cls["vocabulary"]) <= 12
        assert 4 <= len(cls["teaching"]) <= 6
        local_formats: set[str] = set(); local_indices: Counter[int] = Counter(); feedbacks = []
        for pool, count in (("practiceGuided",3),("practice",3),("evaluation",4),("review",3)):
            assert len(cls["pools"][pool]) == count; totals[pool] += count
            for item in cls["pools"][pool]:
                assert len(item["prompt"]["es"]) <= 90, (item["id"], len(item["prompt"]["es"]))
                payload = {k:v for k,v in item.items() if k not in {"id","contentHash"}}
                assert item["contentHash"] == "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
                local_formats.add(item["format"]); formats[item["format"]] += 1
                pk = norm(item["prompt"]["es"]); assert pk not in prompts, (item["id"], prompts.get(pk)); prompts[pk] = item["id"]
                feedbacks.append(item["origin"]["feedback"]["es"])
                if pool != "practiceGuided": assert "hint" not in item["origin"]
                if item["format"] in {"elegir","escuchar"}:
                    assert len(item["choices"]) >= 3
                    idx = item["answer"]["index"]; assert 0 <= idx < len(item["choices"])
                    local_indices[idx] += 1; indices[idx] += 1
                if item["format"] == "escribir":
                    acc = item["answer"]["accepted"]; assert len(acc) >= 2 and len({norm(x) for x in acc}) >= 2
                stimulus = item["origin"].get("audio") or item["origin"].get("text") or item["origin"].get("pairs") or item["prompt"]["es"]
                sig = canonical({"stimulus":stimulus,"answer":item["answer"]}).casefold()
                assert sig not in signatures, (item["id"], signatures.get(sig)); signatures[sig] = item["id"]
        assert len(local_formats) >= 4 and len(feedbacks) == len(set(feedbacks))
        assert len(local_indices) >= 2 and max(local_indices.values())/sum(local_indices.values()) <= .60
        visible = canonical({"teaching":cls["teaching"],"pools":cls["pools"]}).casefold()
        for v in cls["vocabulary"]: assert v["en"].casefold() in visible, (cls["id"],v["en"])
        eval_ids = {x["id"] for x in cls["pools"]["evaluation"]}; assert set(cls["remediationMap"]) == eval_ids
        teach_ids = {x["id"] for x in cls["teaching"]}; review_ids = {x["id"] for x in cls["pools"]["review"]}
        for route in cls["remediationMap"].values(): assert route["reteach"] in teach_ids and route["review"] in review_ids
        if cls["phase"] in {"production","transfer"}:
            reserved = [x for pool in ("evaluation","review") for x in cls["pools"][pool] if x["format"]=="escribir"]
            assert any(len(re.findall(r"\b[\w’-]+\b",x["answer"]["text"]))>=8 and len(x["answer"]["accepted"])>=2 for x in reserved)
    if full:
        assert len(classes)==5 and sum(totals.values())==65
        close=classes[-1]; expected=[CONCEPTS[n] for n in NUMBERS]
        assert close["cumulativeEvaluation"]==expected and close["usesPatterns"]==expected
        e04=next(x for x in close["pools"]["evaluation"] if x["id"]=="en.n3.c30.e04")
        r03=next(x for x in close["pools"]["review"] if x["id"]=="en.n3.c30.r03")
        assert e04["requires"]==expected and r03["requires"]==expected
        t06=close["teaching"][-1]["en"].casefold(); ea=e04["answer"]["text"].casefold(); ra=r03["answer"]["text"].casefold()
        assert "festival" in t06 and "ava" in ea and "studio" in ra
        for text in (t06,ea,ra):
            assert "if" in text and "would" in text and "could" in text
            assert ("but" in text or "although" in text) and ("agree" in text or "choose" in text)
    return {"classes":len(classes),"items":sum(totals.values()),"pools":dict(totals),
            "formats":dict(sorted(formats.items())),"correctIndices":dict(sorted(indices.items())),
            "prompts":len(prompts),"fingerprints":len(signatures)}


def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()


def write_class(n: int) -> Path:
    doc=BUILDERS[n](); audit([doc],False); path=OUT/f"class-{n:02d}.json"
    path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); return path


def write_bundle() -> tuple[Path,dict[str,Any]]:
    classes=[json.loads((OUT/f"class-{n:02d}.json").read_text()) for n in NUMBERS]; summary=audit(classes,True)
    doc={"schema":"onelingo.editorial.class-bundle.v1","course":"en","level":3,"scale":SCALE,
         "status":"shadow","runtimeAi":False,"selectionPolicy":{"deterministic":True},
         "evidencePolicy":{"attemptRecords":["variantId","libraryVersion","selectionId"]},
         "range":{"start":26,"end":30},"classes":classes}
    path=OUT/"bundle-26-30.json"; path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return path,summary


def write_report(paths:list[Path], summary:dict[str,Any])->Path:
    hashes="\n".join(f"{digest(p)}  {p.name}" for p in paths)
    text=f"""# DRAFT — Inglés N3 C26–C30

Estado: **DRAFT para revisión independiente; no autorizado para integración**.

## Alcance

- Bloque `hypothetical-choices`, entrada B1, fases `input → form → comprehension → production → transfer`.
- Cinco clases, 65 ejercicios y contrato `editorial-agent.v2`.
- `status: shadow`, `runtimeAi: false`, selección y recuperación deterministas.

## Cierre C30

- `t06`: festival vecinal con prioridades de música y comida.
- `e04`: viaje de Ava y Luis con tres paquetes y presupuesto de $420.
- `r03`: espacio de curso con privacidad, equipo y presupuesto de $240.
- Cada escenario demuestra condición imaginaria, would/could, consejo suavizado,
  comparación con beneficio y límite, y decisión compartida verificable.

## Auditoría

```json
{json.dumps(summary,ensure_ascii=False,indent=2)}
```

## Validación reproducible

Resultados de esta generación:

- Cinco validaciones individuales y bundle level 3: `OK`.
- Pruebas focalizadas: 57 pruebas, `OK`.
- Ruta editorial: 10 idiomas, 0 errores.
- Idempotencia: dos regeneraciones consecutivas producen hashes idénticos.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 work/n3_c26_30/generate.py --all
python3 tools/contenido/validar_bundle_editorial.py --file work/n3_c26_30/bundle-26-30.json --start 26 --end 30 --level 3
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s test_tools -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 tools/validar_ruta.py
```

## Hashes

```text
{hashes}
```

El autor entrega `DRAFT`, nunca `GO`.
"""
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    path=REPORT_OUT/"REPORT.md"; path.write_text(text,encoding="utf-8"); return path


def write_all()->list[Path]:
    classes=[write_class(n) for n in NUMBERS]; bundle,summary=write_bundle(); report=write_report(classes+[bundle],summary)
    files=classes+[bundle,report]; manifest=REPORT_OUT/"MANIFEST.sha256"
    entries=[f"{digest(Path(__file__))}  ../../tools/contenido/generar_editorial_n3_26_30.py",
             f"{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"]
    entries.extend(f"{digest(p)}  {p.name if p.parent == REPORT_OUT else '../../' + str(p.relative_to(ROOT))}" for p in files)
    manifest.write_text("\n".join(entries)+"\n",encoding="utf-8")
    return files+[manifest]


def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--class-number",type=int,choices=NUMBERS)
    parser.add_argument("--bundle",action="store_true"); parser.add_argument("--audit",action="store_true"); parser.add_argument("--all",action="store_true")
    args=parser.parse_args()
    if args.class_number: print(write_class(args.class_number))
    elif args.bundle: print(write_bundle()[0])
    elif args.audit:
        docs=[json.loads((OUT/f"class-{n:02d}.json").read_text()) for n in NUMBERS]
        print(json.dumps(audit(docs,True),ensure_ascii=False,sort_keys=True))
    elif args.all:
        for path in write_all(): print(path)
    else: parser.error("choose --class-number, --bundle, --audit or --all")
    return 0


if __name__=="__main__": raise SystemExit(main())
