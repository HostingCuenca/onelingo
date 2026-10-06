GO

# Revisión independiente de N10 (alemán C1, método ligero), c01–c50

Archivos: `curriculo/de/n10.json` (50 fichas, `planificado`) contra `tools/curriculo/de/n10-outline.json`. Solo se editó `ejercicios`; campos del outline intactos. Script: `scratchpad/de/fichas/rev-n10.py` (parte del n10.json actual; respaldo previo en el scratchpad).
Validadores tras las correcciones: `validar_plan_detallado.py de curriculo/de/n10.json` = 0 errores (50 clases, 682 ejercicios, ejemplos y consignas únicos); `validar_plan.py de` = 0 errores (los avisos de vocabulario repetido son del outline).

## Veredicto por criterio

1. **Alemán correcto:** muy bueno. Un solo error de lengua real: c10 g0 «dass sie lügte» (Präteritum inexistente) → reescrito. Además c43 situación («sofern … beantragt worden wäre», Konjunktiv II mal formado) → «beantragt wurde»; c48 situación («Autoevaluation», no es alemán) → «Selbstevaluation»; c22 g0 («ist … entwickelt», Zustandspassiv inadecuado) → «wurde … entwickelt»; c14 i2 («die Leiter» como «directora») → «director (hombre)»; c15 consigna i2 vaga.
2. **Una sola respuesta:** el problema dominante del nivel (la gran mayoría de los ~107 ítems tocados). Tres tipos:
   - `completar` con varios sinónimos válidos (also/halt/eben, sagt/meint, Jahre/Monate, herausgestellt/gezeigt, desto/umso, wohingegen/während, beheben/reparieren…): se fijó con la forma del verbo, la letra inicial o «el sustantivo/verbo de…».
   - `ordenar` con dos órdenes (adverbios móviles: heute, gern, bitte, bald, gerade, herzlich; «klar und sachlich»; «jetzt/alles»): se cambió el ítem o se quitó el adverbio.
   - `escribir` abiertos cuya respuesta no se deduce del estímulo (c23 e4/e5, c25 e4/e5, c26 e4, c27 i0/e4/e5, c28 e4/e5, c33 e4, c42, c45 i0/e4…): estímulo completado con los datos que faltaban (o ítem sustituido por uno cerrado).
   - `relacionar` ambiguos (c04 i0, c06 i0, c10 i0, c11 i0, c17 i0, c18 i0, c43 i1, c38 i2): redefinidos con pares funcionalmente distintos.
3. **Nada sin enseñar:** a C1 el léxico es amplio y las situaciones usan vocabulario de clase; no hay adelantos gramaticales graves. Corregido el falso amigo temático «Autoevaluation». Sin cambios necesarios en el resto.
4. **Cobertura:** cada `introduce` (una clave por clase) está evaluada en todas las clases; c49 (6 ítems, 5+ claves) y c50 (8 ítems de evaluación, 6 formatos, 11 claves en la ficha) cumplen FORMATO.
5. **Consignas es/en:** coherentes con el ítem. Se corrigieron consignas contradictorias: c06 e3 («verbo al inicio de la subordinada» cuando va al final), c40 e4 («primero el trámite, después la cita» al revés del ítem), c21 e5 (colega dice «zu lang» y la consigna «gar nicht lang»), c32 e5 («sustantivo» con un adjetivo).
6. **Sin Lumo/Ecuador/continuidad:** limpio. Nombres genéricos (Jonas, Lena, Anna, Frau Berger, Herr Wolf…) sin hechos que se arrastren.

## Cambios por clase (≈107 ítems / 42 fichas; sin cambios: c01, c09, c16, c20, c31, c34, c35, c46)

- c02 i2 · c03 g0, e0 · c04 i0, i1, e0 · c05 g1, e1, e3, e4 · c06 g0, i0, e0, e3 · c07 g0, e0 · c08 i2, e0
- c10 g0, i0, e0 · c11 g0, i0, e3, e4 · c12 e0, e3 · c13 i2 · c14 i2, e1, e4 · c15 g0, i2, e3
- c17 i0 · c18 i0, e0, e4 · c19 e3 · c21 e5 · c22 g0, i1, e5 · c23 e4, e5 · c24 i1, i2, e4, e5
- c25 g0, e4, e5 · c26 g0, i0, e2, e4, e5 · c27 i0, e2, e4, e5 · c28 e4, e5 · c29 e1, e4, e5 · c30 i0, e5
- c32 e5 · c33 e1, e4, situación (pregunta completar) · c36 e1, e4 · c37 e2 · c38 i1, i2 · c39 e1 · c40 e1, e4 · c41 i1, e1
- c42 i1, i2, e1 · c43 situación, g1, i0, i1, i2 · c44 i1, e1 · c45 i0, e1, e4 · c47 i0, e1 · c48 g0, i1, situación · c49 i1, e1, e4 · c50 g1, i1, e1, e7

## Sin resolver (outline u otros)

- **c35:** el título es «Der Neue Deutsche Film» (cine de 1962–1982) pero objetivo, vocabulario y situación giran en torno al Expressionismus (años 20). Está congelado; el bloque debería corregir el título o la situación en el redactado.
- **c46/c48:** nueve de las doce `recicla` de c48 (y varias de c49/c50) están cubiertas solo con un ítem «de paso»; es una carga de repaso, no un error.
- Registro «Frau Becker/Herr Wolf» con «du» (c02): se dejó; el bloque puede unificar a «Sie» al redactar.
- La verificación de audio de-DE (Umlaut, ich/ach) sigue pendiente.

## Avisos para autores de bloque (`erroresFrecuentes` reales de N10)

1. **Sinónimos que compiten en un hueco:** also/na ja/tja/halt/eben; sagt/meint; dass/ob; wohingegen/während; desto/umso; übersehen/verkennen; beheben/reparieren; ausgerechnet/sogar. En cada ítem dar la letra inicial, la forma o la nota de uso.
2. **Verbos fuertes con Präteritum inventado:** *lügte (log); revisar toda forma de Präteritum irregular antes de usarla en un hueco.
3. **Konjunktiv I:** «Er sagte, dass er müde sei» vs indicativo tras dass; con «sagt, dass» el indicativo es normal. *«Er sagt, sie ist krank» (informal) frente a «sei».
4. **Nominalstil:** *«Die Durchführung von der Untersuchung» (genitivo, no von), *«Nach die Erhebung» (dativo), olvido del artículo en «Laut der Quelle».
5. **sein zu + infinitivo:** *«Der Antrag ist abzugeben zu» (zu va tras el prefijo: einzureichen, vorzulegen).
6. **Orden en subordinadas formales:** *«Bevor Sie stellen den Antrag», *«vorausgesetzt, wir …» sin dass.
7. **«Wenn» sin sollte:** *«Wenn sollte der Kredit …» (sollte ocupa la primera posición sin wenn).
8. **Registro:** ironía y slang (Alter, krass, Kohle) solo entre amigos; marcar siempre contexto (jefa, colega) para que el ítem tenga una respuesta.
9. **Palabras compuestas y falsos amigos:** Schloss (castillo/cerradura), Bank (banco/banquillo), Leiter (der/die), Termin = cita (no término); Handy, Beamer, Oldtimer pseudo-anglicismos.
10. **Mediación (Sprachmittlung):** transmitir con «möchte wissen, ob/wo …» (verbo al final); no mezclar «sagt» con indicativo y Konjunktiv I en la misma cadena.
