#!/usr/bin/env python3
"""Aplica apoyos pedagógicos deterministas al piloto N1 y recalcula hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FILE = ROOT / "assets/contenido/en/editorial/n1/pilot-classes-01-05.json"
SCALE = ROOT / "assets/contenido/en/plan-editorial/escala-cliente.json"


EXTRA_TEACHING = {
    1: ("I am a student.", "Soy estudiante.", "I + am + información personal", "identity-be"),
    2: ("He is a teacher.", "Él es profesor.", "he/she + is + descripción", "pronouns-be"),
    3: ("The chair is blue.", "La silla es azul.", "the + objeto + is + color", "classroom-description"),
    4: ("They are my parents.", "Ellos son mis padres.", "they + are + relación", "family-be"),
    5: ("My grandfather is kind.", "Mi abuelo es amable.", "my + familiar + is + adjetivo", "family-description"),
}

CLASS_CONCEPTS = {
    1: ["identity", "identity-be"],
    2: ["pronouns-be"],
    3: ["classroom-objects"],
    4: ["family-relations", "family-be", "family-vocabulary"],
    5: ["family-description"],
}


def content_hash(item: dict) -> str:
    content = {key: value for key, value in item.items() if key not in {"id", "contentHash"}}
    raw = json.dumps(content, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(raw.encode()).hexdigest()


def feedback(item: dict) -> str:
    fmt = item["format"]
    if fmt == "ordenar":
        return "Comprueba el orden sujeto + verbo + complemento y vuelve a leer la frase completa."
    if fmt == "relacionar":
        return "Compara cada palabra inglesa con su significado antes de confirmar todas las parejas."
    if fmt == "escuchar":
        return "Escucha de nuevo y localiza primero las palabras clave antes de elegir."
    if fmt == "completar":
        return "Revisa el patrón enseñado y comprueba que la palabra encaje en toda la oración."
    if fmt == "escribir":
        return "Revisa el patrón enseñado: sujeto, forma de be y complemento."
    return "Compara sujeto, verbo y significado con el modelo enseñado."


def hint(item: dict) -> str:
    fmt = item["format"]
    return {
        "elegir": "Descarta primero las opciones que no responden a la consigna.",
        "escuchar": "Escucha una vez la frase completa y otra vez buscando la palabra clave.",
        "ordenar": "Empieza por el sujeto y coloca después la forma verbal.",
        "completar": "Lee la oración entera y busca el patrón visto en los ejemplos.",
        "escribir": "Apóyate en el modelo enseñado y cambia solo la información necesaria.",
        "relacionar": "Resuelve primero la pareja que recuerdes con seguridad.",
    }[fmt]


def main() -> int:
    data = json.loads(FILE.read_text(encoding="utf-8"))
    scale = json.loads(SCALE.read_text(encoding="utf-8"))
    data["scale"] = scale["id"]
    data["selectionPolicy"] = {
        "deterministic": True,
        "selectionIdGeneratedAtAttempt": True,
        "excludeRecentFamilies": True,
    }
    data["evidencePolicy"] = {
        "attemptRecords": ["variantId", "libraryVersion", "selectionId"],
        "resumeUsesFrozenSelection": True,
    }
    for number, cls in enumerate(data["classes"], 1):
        cls["prerequisites"] = [] if number == 1 else [f"en.n1.class-{number - 1:02d}"]
        cls["concepts"] = CLASS_CONCEPTS[number]
        cls["skills"] = ["lectura", "escucha", "escritura-controlada"]
        cls["accessibility"] = {
            "shortSpanishInstructions": True,
            "audioSpeedOptions": [0.75, 1.0],
            "audioMaxReplays": 3,
            "revealTranscriptAfterAttempt": True,
            "acceptCaseAndTerminalPunctuationVariants": True,
            "lowLoadMode": "one_item_at_a_time",
            "orderAndWriteSegmentation": True,
            "guidedChoiceAlternativeBeforeWriting": True,
        }
        cls["recovery"] = {
            "afterTwoErrors": "reteach_then_guided_variant",
            "preserveAttemptEvidence": True,
            "reviewTargetsFailedConcepts": True,
            "maxIndependentAttemptsBeforeReteach": 2,
        }
        for lesson_number, lesson in enumerate(cls["teaching"], 1):
            lesson["explanationEs"] = (
                f"Observa el modelo y sus partes. Practica primero la frase {lesson_number} "
                "con apoyo antes de producirla sin ayuda."
            )
            lesson["segments"] = lesson["en"].replace(".", "").split()
            lesson["audioText"] = lesson["en"]
            lesson["audioMode"] = "tts"
            lesson["languageCode"] = "en"
        en, es, explanation, pattern = EXTRA_TEACHING[number]
        extra_id = f"en.n1.class-{number:02d}.t04"
        cls["teaching"] = [lesson for lesson in cls["teaching"] if lesson["id"] != extra_id]
        cls["teaching"].append(
            {
                "id": extra_id,
                "en": en,
                "es": es,
                "explanationEs": explanation,
                "segments": en.replace(".", "").split(),
                "audioText": en,
                "audioMode": "tts",
                "languageCode": "en",
                "patternId": pattern,
            }
        )
        if number == 5:
            cls["teaching"][2].update(
                en="My home is in this photo.",
                es="Mi casa está en esta foto.",
            )
            cls["pools"]["practiceGuided"][2].update(
                prompt={"es": "Completa: My home is in this ___."},
                answer={"text": "photo", "accepted": ["photo"]},
            )
            evaluation = cls["pools"]["evaluation"]
            evaluation[0].update(
                format="escuchar",
                prompt={"es": "¿Qué frase sirve para presentarte con tu nombre?"},
                answer={"index": 0},
                choices=[
                    {"text": "Hello, my name is Ana."},
                    {"text": "The chair is blue."},
                    {"text": "They are my parents."},
                ],
                teaches=[],
                requires=["identity-be"],
                origin={"kind": "editorial", "audio": "Hello, my name is Ana."},
            )
            evaluation[1].update(
                prompt={"es": "Ordena la frase que presenta a los padres."},
                answer={"text": "They are my parents.", "tokens": ["They", "are", "my", "parents."]},
                choices=[],
                teaches=[],
                requires=["pronouns-be", "family-be"],
                origin={"kind": "editorial"},
            )
            evaluation[2].update(
                prompt={"es": "Traduce: «Esto es un libro»."},
                answer={"text": "This is a book.", "accepted": ["This is a book.", "This is a book"]},
                choices=[],
                teaches=[],
                requires=["classroom-objects"],
                origin={"kind": "editorial", "text": "Transferencia acumulativa de objetos del aula."},
            )
            evaluation[3]["requires"] = ["family-vocabulary"]
            cls["cumulativeEvaluation"] = [
                "identity-be", "pronouns-be", "classroom-objects", "family-vocabulary"
            ]
        for pool_name, items in cls["pools"].items():
            for item in items:
                origin = item["origin"]
                origin["feedback"] = {"es": feedback(item)}
                if pool_name == "practiceGuided":
                    origin["hint"] = {"es": hint(item)}
                else:
                    origin.pop("hint", None)
                if item["format"] == "escuchar":
                    origin.update(
                        audioMode="tts",
                        languageCode="en",
                        speedOptions=[0.75, 1.0],
                        maxReplays=3,
                        revealTranscriptAfterAttempt=True,
                    )
                if item["format"] in {"completar", "escribir"}:
                    answer = item["answer"]
                    text = answer["text"]
                    variants = [text, text.rstrip("."), text.casefold(), text.rstrip(".").casefold()]
                    answer["accepted"] = list(dict.fromkeys(variants))
                item["contentHash"] = content_hash(item)
        cls["remediationMap"] = {
            exercise["id"]: {
                "reteach": cls["teaching"][min(index, len(cls["teaching"]) - 1)]["id"],
                "review": cls["pools"]["review"][min(index, len(cls["pools"]["review"]) - 1)]["id"],
            }
            for index, exercise in enumerate(cls["pools"]["evaluation"])
        }
        semantic_review = {1: "r02", 3: "r02", 4: "r02", 5: "r01"}.get(number)
        if semantic_review:
            cls["remediationMap"][f"en.n1.c{number:02d}.e04"]["review"] = (
                f"en.n1.c{number:02d}.{semantic_review}"
            )
    FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK: piloto reforzado, 5 clases; hashes recalculados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
