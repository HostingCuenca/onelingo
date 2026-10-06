GO

# Revisión independiente N5 (B2), c01–c50

Archivo: `curriculo/de/n5.json` (50 fichas `planificado`) contra `tools/curriculo/de/n5-outline.json`. Solo se editó `ejercicios` (campos del outline y raíz comprobados idénticos al original). Validadores: `validar_plan_detallado.py de curriculo/de/n5.json` = 0 errores (50 clases, 703 ejercicios); `validar_plan.py de` = 0 errores.

## Veredicto por criterio
1. **Alemán correcto:** muy bueno. No hubo errores gramaticales graves (Konjunktiv I/II, participio ampliado, genitivo, Vorfeld correctos). Solo hubo fallos en consignas con caso o género equivocado (c44: `mit` + dativo etiquetado «acusativo»; c32 «el foto»; c44 «das mail»).
2. **Una sola respuesta:** el problema principal. Había 9 `ordenar` con dos órdenes válidos (adverbio móvil o temporal: c01, c10, c17, c34, c42, c43; Vorfeld/sujeto-objeto femeninos c33; «so … auch» + principal c20) y ~25 `completar`/`escribir` con sinónimos válidos (Obgleich/Wenngleich, wegen/aufgrund, Zudem/Ferner, wenn/falls/sofern, Somit/Folglich…) o final abierto («Es gelingt uns, ___», «Zudem ist es sehr gut»). Fijados con inicio dado o con la letra inicial en la consigna.
3. **Nada sin enseñar:** corregido léxico adelantado o raro (Streik, Bewerbung, Fälscher, Teig, Geduld, Hotline, Benzin/leihen, bestochen, gelogen, Quartal, Vertrag, Frist einhalten, Gesundheitsamt, verstößt, vertrauen, Karte). Se evitó el plural Konj. I «seien» (c33, c50) y «könnten» (c26) antes de enseñarlos; «Partizip-Vorfeld» no enseñado en c33 sustituido.
4. **Cobertura:** cada clave de `introduce` está en la evaluación de las 48 clases; c50 cubre 7 claves (≥5) con 7 ítems y 6 formatos. c49 pasa a 8 ítems.
5. **Consignas es/en:** corregidas las ambiguas, las erróneas (c24 «aumento» con «sank», c44, c32) y las garabateadas (c47 «usa Beginn no», c50 «con Wegen no»).
6. **Sin Lumo/Ecuador/Quito:** comprobado. Nombres genéricos sin continuidad (Anna, Jonas, Frau Becker, Herr Wolf, Frau Keller, Herr Lenz…).

## Claves de niveles «anteriores» en c49–c50 (pregunta del encargo)
Confirmado: `konnektoren-b2-schriftlich` (se enseña en c46), `distanzierung` (c31) y `konjunktiv1-praesens` (c26) son claves del propio N5, enseñadas antes de c49/c50, y las tres figuran en `recicla` de ambas. Las usan los ítems de c49/c50 sin adelantarse. `da-correlate-clause` (c50 gui) es de un nivel anterior y está en `recicla` de c50. Sin problema.

## Cambios (104 ítems/situaciones, 44 clases; script `scratchpad/de/fichas/rev-n5.py` + `rev-n5b.py`)
- c01: ordenar (im Mai al inicio), escribir (inicio fijado). c02: escribir (tiempo perfecto, «Kaum war sie»). c04: Bewerbung→Anmeldung, «vom Amt/gültig» sustituido, relativo con «wurde». c05: ordenar sin «bald».
- c06 escribir (referente claro). c07 completar (w…). c08 consigna. c09 «bestochen», «lügt» sustituidos. c10 ordenar/escribir/escuchar. c11 «Zelt». c12 Streik, pronombre, «hoy». c13, c14 (distractor, orden), c15 (Karte→Frühstück, «gelogen»), c16 (Geduld, Teig, escribir), c17 (ordenar sin «dort», «Hotline»), c18 (pasado).
- c19 relacionar (je nachdem/abhängig von eran sinónimos). c20 completar (Wenn-) y ordenar (principal tras «so…auch»). c21 (Gesundheitsamt, distractor). c24 consignas. c25 artículo definido. c26 «könnten».
- c27 («Zahlen vorschlagen»), c30 (Konj. I perfecto-pasivo, «según»), c31 («missseriös», Fälscher/Fachmann, escribir con «meldet»), c32 consigna, c33 (Partizip-Vorfeld, sujeto/objeto femeninos, «seien»), c34 (hingegen en posición 3, woh-).
- c35 Vertrag→Bericht. c36 (Zugegeben, zweifle, dass). c37 (sofern, leihen). c38 (Ethik/vertrauen, distractor absurdo). c39 (distractor, sofern). c41 (telefonieren, Frist, Vertrag). c42 (Quartal, relacionar con sinónimos, steigen, orden).
- c43 (binnen, gültig, ordenar, fecha «30»). c44 (relacionar basado en personaje ausente, casos, dativo vs acusativo). c45 escribir abierto. c46 (5 consignas con sinónimos, 2 escribir abiertos). c47 consigna. c48 relacionar (dos pares permutables). c49 (referente «Er», «Verkauf», Aufgrund/wegen, +2 ítems de reciclaje). c50 (consigna, «seien», modal).

## Sin resolver
- **Reciclaje parcial sistemático:** casi todas las clases usan solo 1 de 3–4 claves de `recicla` en la evaluación (el último ítem `completar`). Es lo que exige el validador; no se amplió salvo c49 (límite de 8 ítems). Varias claves de `recicla` son de otros niveles y no verificables o con nombre inusual (`modal-subjective`, `wer-der`, `text-connectors-opinion`, `zustandspassiv`…).
- **Outline c48:** `recicla` con 12 claves (es un listado de repaso y no una clase de gramática nueva); un solo ítem puede cubrirlo. Se dejó.
- **c20:** «so … auch» admite tras la subordinada tanto orden con sujeto primero («die Preise sind hoch») como verbo primero; la situación y los ítems de elegir usan el primero. Se evitó en `ordenar`.
- **c17, c46:** `situacion.texto` de c17 sin diálogo (solo datos): válido por formato.
- Verificación de audio de-DE de `escuchar` (Umlaut, ch) pendiente.

## Avisos para autores de bloque (errores frecuentes reales del nivel)
1. **Orden de palabras:** *«Kaum dass ich war angekommen»; *«Während es dort warm ist, es ist hier kalt»; *«Dennoch das Ergebnis ist gut» (verbo siempre en 2.ª posición tras dennoch/zudem/somit/folglich); *«Hinzu kommt, dass ist …».
2. **Caso:** *«Infolge die Impfung», *«Gemäß des Gesetzes» (gemäß + dativo), *«Anders als mir», *«Ich bin mich einverstanden». *«Obgleich» y «wenngleich» con verbo al final.
3. **Participio ampliado:** *«der eingereicht Antrag» (terminación -e), sin confundir con relativa («der Antrag, der eingereicht hat»).
4. **Pasiva:** *«Ich werde den Brief zugeschickt» (bekommen-Passiv, no werden), *«vermeiden werden müssen» (participio, no infinitivo), *«geworden» por «worden».
5. **Konjunktiv I:** *«Er sagte, er hat keine Zeit»; confusión de sei/ist y de `will`/`soll` (afirmación propia vs rumor); no usar «seien» ni «wäre» antes de enseñarlos.
6. **Preposiciones nominales:** *«Wegen Problemen» por «Bei Problemen»; *«Ohne der Einnahme»; «um/auf» en steigen (*«um 120» como resultado).
7. **Cuantificadores:** *«viele neuen Ideen» / *«alle neue Kollegen» (viele → -e; alle/beide → -en).
8. **Falsos amigos a marcar con ⚠:** Chef, Termin, Karte, Handy (en c32), Bescheid (≠ «bescheid» español), Lokal.
