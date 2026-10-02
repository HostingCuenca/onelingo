# Revisión N6 · B2 (fr.n6.c06–c10)

GO

Revisor distinto del autor. Contrastado con las 5 fichas de `curriculo/fr/n6.json` (incl. plan de ejercicios), la `nota` del nivel, el reparto de N1–N5 (`personajes`, `hechosDelReparto`), `ENCARGO_RUTA_FR.md` (Por nivel N5–N7 y Calibración 1–11), `ESQUEMA_CONTENIDO.md`, los borradores de N5 y n6-b01, y `revision-n2-*` / `revision-n5-b10` como calibración.

Validación: `python3 tools/validar_ruta.py fr --borrador n5-b01…n5-b10 n6-b01 n6-b02` → **0 errores** (vocabulario estricto activo en `curso.json`; repetida tras los cambios). `python3 tools/curriculo/validar_plan.py fr` → 0 errores, 10 avisos conocidos (N1); ningún «título de la unidad difiere» para c06–c10.

## Contraste con las fichas

- Títulos, objetivos, gramática, vocabulario (todas las palabras de cada ficha + 2–5 extras de apoyo por clase: assureur / convenir / adapté, résilier / renouveler / dépannage / s’appliquer / caché, entrer en vigueur / annexe / figurer / ci-dessus / concerner, banquier / dette) y tareas coinciden con las fichas. Los extras están justificados por la gramática y se enseñan en tarjeta.
- Los ejercicios del plan están todos (mismo formato y clave): guiada 5, independiente 4, situación 2, evaluación 6 por clase; los `escribir` (i4, e6) son `abierta: true`, no puntúan y quedan aparte de los 5 puntuables de cada evaluación (≥ 3 formatos por evaluación). Formatos del bloque: elegir, escuchar, ordenar, completar, escribir y relacionar.
- Nada de clases posteriores: c07 solo recicla au cas où / à supposer que / à condition que; c08 recicla pasiva, participe présent e interrogación cortés; c09 recicla en / y, à condition que y el condicional de cortesía; c10 recicla comparatif / superlatif / evolución de cifras. Las anticipaciones léxicas que había (ver fixes 1 y 2) se quitaron.
- Anatomía: explicaciones → tablas → ejemplos (8) → tarjetas → guiada con `pista` → independiente sin pista → situación (2 ítems) → evaluación; 3–4 `erroresFrecuentes` por clase. Mismo orden que n4/n5/n6-b01.
- Situación: 334 / 336 / 316 / 310 / 325 palabras (300–500 de «Por nivel» N5–N7); comprensión coherente con el texto; hablantes = nombres o papeles/documentos franceses (La conseillère, L’agent, Le conseiller, Le contrat, Le rapport, Les conditions générales), con precedente en N3–N5.
- Tipografía: 0 apóstrofos rectos en francés y U+202F antes de ? ! : ; en todos los textos, ejemplos, ítems, tokens y diálogos (comprobado sobre el crudo, no solo con la normalización del validador).
- Español neutro de América (usted en los diálogos con vous, tú en las explicaciones; camioneta, auto, tasa, aporte, deducible) e inglés americano; sin léxico de España ni británico.

## Registro Ana ↔ Karim (pedido de coordinación)

Comprobado en todas las réplicas de Ana y Karim de c06–c10 (diálogos, contextos, ejemplos, ítems y errores frecuentes): **todo en vous** (vous avez raison, regardez, envoyez, dites-moi, cherchez, lisez, avez-vous trouvé…), y en español usted (mire, envíe, hace bien). No hay tu / ton / ta / te / toi ni imperativos de tú entre Ana y Karim; el único «tu» del bloque está en la tabla de conjugación de s’en tenir à / en venir à (c09), que es un paradigma. Coincide con N2–N4 (Ana y Karim se tratan de vous). Karim usa vous con la asesora, el agente y el asesor del banco, y Ana con Madame Dubois (vous). No fue necesario cambiar nada; se deja constancia porque otro autor reportaba tuteo en c06: en esta versión del archivo no existe.

## Madame Dubois (c08)

Se presenta como **antigua propietaria** de Ana que conoce los contratos de alquiler, nunca como propietaria actual (los de ahora son Monsieur Roux y Madame Lefort, vecina de abajo). Se añadió al contexto que ya no es su propietaria y sigue viviendo cerca (coherente con N4 c11 y N5: «antigua propietaria, vive cerca»). Aceptable.

## Fixes (clase · ítem · antes → después)

1. **c06 · situación, última réplica de Ana.** «il n’y a personne qui puisse lire ces petits caractères !» usaba *les petits caractères*, vocablo de c08 → «il n’y a personne qui puisse comprendre toutes les clauses d’un contrat !» (es y en ajustados; `comprendre` ya está en la tabla de c06).
2. **c07 · situación, Article 1.** «Le présent contrat de location…» usaba *le présent contrat*, vocablo de c08 → «Ce contrat de location…».
3. **c07 · contexto.** Karim alquila una camioneta aunque en N5 c07 ya tiene la camioneta del restaurante (la que chocó) → se aclara «(la del restaurante está en el taller)» / “(the restaurant’s own van is at the repair shop)”.
4. **c08 · g1 (relacionar).** Las glosas de conformément à («de acuerdo con») y en vertu de («en virtud de») eran casi sinónimas y la pista no las separaba → «siguiendo lo que dice un documento o un anexo» / «por efecto de lo que establece una ley» (y en: “following what a document or an appendix says” / “by force of what a law establishes”); `pista` y `feedback` reescritos (conformément → documento, en vertu → ley).
5. **c08 · tarjeta conformément à (nota de pronunciación).** «én = «an»» (error: la sílaba es -ment) → «la terminación -ment = «man»» (es) / “-ment = “mahn”, with no n sound” (en).
6. **c08 · s2 (feedback).** «Los tarifs se fijan» (francés en el español) → «Las tarifas se fijan».
7. **c08 · contexto.** Se aclara que Madame Dubois ya no es su propietaria y vive cerca (ver arriba).
8. **c10 · i1 (ordenar).** Faltaba un orden natural: «C’est la formule de loin la plus souple.» → añadido a `aceptadas` junto a «C’est la formule la plus souple de loin.» (feedback reescrito en es / en).
9. **c10 · traducciones al español.** «cuesta la mitad que el otro» → «cuesta la mitad del otro» (ejemplo del forfait) y «es la mitad de caro que el banco A» → «cuesta la mitad que el banco A» (informe; «mitad de caro» no es español natural).

Sin cambios (revisado y correcto): subjuntivo / indicativo en relativas y tablas de c06 (qui soit / ait / puisse / sache / fasse / convienne / comprenne); si jamais + présent / imparfait, pour peu que + subjuntivo, dans l’hypothèse où + condicional y la tabla de formas de c07 (renouvelleriez, payiez, résiliiez…); locuciones contractuales, pasiva y garantir que + indicativo de c08; s’en tenir à / en venir à / s’en sortir / y tenir / s’y prendre / en vouloir à, concordancia en sommes venus y tabla de c09; intensificadores, tout aussi / tout autant y proporciones (deux fois moins cher = la mitad) de c10. Cada `ordenar` tiene sus órdenes alternativos donde son naturales (c07 i2 y e5 con la consecuente al inicio; c10 i1 ampliado); los `completar` / `elegir` tienen una sola respuesta defendible (en s2 de c10 se aceptan bien / beaucoup / nettement); las pistas ayudan a su ítem; las guías de sonido siguen las reglas de Calibración 6 (sh para j, in / an / on, ü y ö definidos al aparecer, r final de «sinistre», x y t finales mudas).

## Hechos del reparto confirmados

- Karim asegura el segundo restaurante: pide a una aseguradora un contrato que cubra el robo, sin franquicia y con protección jurídica para sus proveedores (su local abre hasta tarde); ya tiene con esa aseguradora un seguro de vivienda (c06). / Karim insures his second restaurant: he asks an insurer for a contract that covers theft, with no deductible and with legal protection for his suppliers (the place is open late at night); he already has a home insurance policy with that insurer (c06).
- Karim alquila una camioneta (la del restaurante está en el taller) para recoger material del segundo local; ha leído las condiciones generales con Ana y firma al día siguiente si todo está claro; Ana y Karim se tratan de vous (c07). / Karim rents a van (the restaurant’s own van is at the repair shop) to pick up supplies for his second location; he reads the general terms with Ana and signs the next day if everything is clear; Ana and Karim use vous (c07).
- Ana coordina el alquiler de una sala para una reunión de equipo del hotel (fecha 3 de mayo, contrato de la empresa propietaria de la sala) y lo revisa con Madame Dubois, su antigua propietaria, que sigue viviendo cerca y conoce los contratos de alquiler; se tratan de vous (c08). / Ana coordinates the rental of a room for a hotel team meeting (May 3, contract from the company that owns the room) and goes over it with Madame Dubois, her former landlady, who still lives nearby and knows rental contracts; they use vous (c08).
- Karim, que alquilaba el local de su segundo restaurante desde hacía dos años, negocia en el banco un crédito hipotecario para comprarlo (200 000 € a 20 años, tasa fija del 3 %, aporte propio de 40 000 € que sube a 50 000 € a cambio de gastos de trámite más bajos); sin tasa fija no firma, leerá la simulación con Ana (c09). / Karim, who had been renting the premises of his second restaurant for two years, negotiates a mortgage at the bank to buy it (200,000 euros over 20 years, 3 % fixed rate, a 40,000-euro down payment that rises to 50,000 in exchange for lower processing fees); without a fixed rate he won’t sign, and he will read the simulation with Ana (c09).
- Ana compara tres ofertas bancarias para la cuenta del equipo (el fondo común de su proyecto en el hotel) y recomienda el banco B (5 euros al mes; el A cuesta 10 y el C 12; B abre la cuenta en dos días); Karim, que ha comparado bancos para su crédito, llega a la misma conclusión sobre B y C; Ana y Karim se tratan de vous (c10). / Ana compares three bank offers for the team account (the shared fund for her hotel project) and recommends bank B (5 euros a month; A costs 10 and C 12; B opens the account in two days); Karim, who compared banks for his loan, reaches the same conclusion about B and C; Ana and Karim use vous (c10).

## Sin resolver (no bloquea)

- **Dependencias de B3:** `n6-b03.json` tiene c06–c10 como prerrequisito (c10). No se quitó ni renombró ninguna palabra francesa enseñada: solo se sustituyeron usos de *petits caractères* (c06) y *présent contrat* (c07), que siguen enseñados en c08. Validado encadenado: 0 errores.
- El contexto de c09 dice «hasta ahora lo alquilaba» y la ficha pide «financiar el local de su segundo restaurante»: es compatible (N4 c06 abre el segundo local; han pasado ≥ 2 años), pero conviene que los bloques siguientes no hablen de él como recién abierto.
- Las dos situaciones de c06 y c07 combinan el texto formal (correo / condiciones generales) con un diálogo corto; como el contrato o el correo se rotulan como hablante («Les conditions générales», «Le contrat», «Le rapport»), la comprensión se apoya en esos bloques: es la misma convención que N4–N5.
