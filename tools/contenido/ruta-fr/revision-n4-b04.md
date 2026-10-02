# Revisión N4 · B4 (fr.n4.c16–c20)

GO

Revisor distinto del autor. Contrasté las 5 clases con sus fichas de `curriculo/fr/n4.json` (incluido el plan de ejercicios), la `nota` del nivel, el reparto de N1–N3, `ENCARGO_RUTA_FR.md` (Por nivel N4 y Calibración 1–10) y `ESQUEMA_CONTENIDO.md`. Los formatos y las claves de los ejercicios planificados están todos presentes; no se enseña nada de clases posteriores.

Validación: `python3 tools/validar_ruta.py fr --borrador n4-b01 … n4-b04` → 0 errores (también con n4-b01…b10 completos). `python3 tools/curriculo/validar_plan.py fr`: sin «título de la unidad difiere» para fr.n4.c16–c20 (solo el aviso previo de fr.n5.c26, ajeno al bloque).

## Correcciones

### fr.n4.c16 (participe présent, banco)
- i1 (escuchar), opciones es: «descubierto» → «sobregiro» (coherente con la glosa del vocabulario y la traducción de la brochure).
- Posiciones de la respuesta correcta en g1, g3, i1, i4, s1, e1, e3, e5 repartidas entre las tres posiciones (antes casi siempre la última o la del medio).

### fr.n4.c17 (carta de reclamación, malgré)
- Situación, «La lettre»: «Personne ne m’a écrit.» contradecía «Suite à votre message du 12 mars» → «Personne ne m’a donné de date.» (es: «Nadie me ha dado una fecha»; en: “Nobody has given me a date”).
- Inglés americano: «Madam, Sir:» → «Dear Sir or Madam:»; «yours faithfully» (británico) → «Awaiting your reply, please accept, Madam, Sir, my respectful regards.» en la carta y en el último ejemplo.
- g3 (elegir): distractor «bien que» → «pendant». «bien que» queda para N5 según la `nota` del nivel y «pendant» ya estaba enseñado.
- i1 y e4 (opciones en): «He …» → «The writer …» (el emisor no tiene género fijado).
- i4 (escribir, práctica): era una frase libre `abierta` → ahora cerrada: «Reescribe con malgré y mes deux appels…: J’ai appelé deux fois, mais personne ne m’a répondu.» → «Malgré mes deux appels, personne ne m’a répondu.» (`aceptadas`: «Personne ne m’a répondu malgré mes deux appels.»).
- e6 (tarea abierta, sigue en la evaluación): el modelo decía «je n’ai reçu aucune réponse» y a la vez «Comme convenu au téléphone» → «le problème n’est pas réglé» (igual que la carta de la situación). Rango de palabras 100–200 → 110–200 (la consigna pide 140–160).
- Vocabulario: glosa en de «la lettre recommandée» → «the registered letter (certified mail)».
- Posiciones de respuesta en g3, g5, i1, s1, s2, e3, e4 repartidas (antes 6 de 7 en la última).

### fr.n4.c18 (reembolsos, infinitif passif)
- Inglés americano: «shop» → «store» (objetivo, contexto de la situación, consigna de e6).
- i4 (escribir, práctica): era `abierta` → cerrada: «Pasa a infinitivo pasivo, empezando por «La cafetière»: Le magasin doit échanger la cafetière.» → «La cafetière doit être échangée.» (`aceptadas`: «… par le magasin.»).
- Posiciones de respuesta en g3, i1, i2, s1, s2, e2, e3, e5 repartidas.

### fr.n4.c19 (encargar un servicio) — corrección de cronología
- **Ana y Emma ya se mudaron en c11 (b03, propietario Monsieur Roux); c19 no las muda otra vez.** Situación reescrita: ya viven en el departamento nuevo, compraron un sofá y una estantería para libros en una tienda que no entrega y Ana llama a una empresa de mudanzas (Le déménageur) para que los recojan y los entreguen. Mantiene la gramática de la ficha: mettre / il faut / ça prend + duración + pour, en + duración, faire causatif, futur antérieur («à onze heures, nous aurons tout livré»), forfait, à domicile, sur rendez-vous, en urgence. Plazo: dos horas; forfait: 80 €; entrega el sábado a las 9 h. El texto sube a 160 palabras (≥ 150).
- s1 y s2 ajustados a la nueva llamada: «Combien de temps faut-il pour tout livrer ?» → «Deux heures»; «¿Qué día queda fijada la entrega?».
- Explicación p3: ejemplo de futur antérieur «À midi, nous aurons tout déménagé» → «À onze heures, nous aurons tout livré» (es y en), para no sugerir otra mudanza.
- i4 (escribir, práctica): era `abierta` → cerrada: «Responde con ça prend + duración: Vous mettez combien de temps pour changer la serrure ? (una hora)» → «Ça prend une heure.» (`aceptadas`: «Ca prend une heure.»).
- e5 (completar): la consigna «preposición de duración» admitía también «pendant» → «la preposición que da el tiempo total que tardó en terminar la tarea» (respuesta: en).
- El modelo de e6 (tarea abierta) sigue siendo genérico: el alumno elige mudanza, cerrajero o catering.
- Posiciones de respuesta en g3, g4, i1, i3, s1, s2, e2, e3 repartidas.

### fr.n4.c20 (firme y cortés)
- Explicación p1: «Primero demandas» (falso amigo: «demandar» = poner una demanda) → «Primero pides». Se añade el quinto escalón (intimar: Je vous mets en demeure de me rembourser), que ya figuraba en la tabla; y se ordena la enumeración.
- Tabla p2: título «Cuatro niveles» → «Cinco niveles» (en: Five levels), pues la tabla tiene cinco.
- Traducción en de la línea de Ana: «(yours faithfully)» → «(a formal closing, like “Sincerely”)».
- i1 (opciones y feedback en): «He …» → «The writer …».
- e4 (ordenar): «Je vous demande de rembourser sous huit jours.» no tenía complemento → «Je vous demande de me rembourser sous huit jours.» (token y respuesta).
- i4 (escribir, práctica): era `abierta` y repetía i3 (la respuesta modelo era exactamente la opción correcta de i3) → cerrada y distinta: «Reescribe con «Il serait souhaitable que…» (subjuntivo): Répondez sous huit jours.» → «Il serait souhaitable que vous répondiez sous huit jours.»
- e6 (tarea abierta): el modelo mezclaba «aucune réponse» con «Comme convenu au téléphone» → «Malgré mes deux appels, le problème n’est pas réglé.» Rango 60–160 → 90–150 (la consigna pide 120 palabras).
- Posiciones de respuesta en g3, i1, i3, s1, s2, e2, e3 repartidas.

### Transversal
- Los `escribir` abiertos (`abierta: true`) quedan solo en la evaluación (e6 de c16–c20); cada evaluación tiene 5 ítems puntuables en ≥ 4 formatos. Ningún `escribir` de práctica es abierto: c17–c20 i4 son cerrados con `aceptadas` donde hay más de una forma natural.
- Reparto final de la respuesta correcta en elegir/escuchar del bloque: posición 1 = 15, 2 = 13, 3 = 10 (antes casi todas en la 2.ª y la 3.ª).
- Revisado sin cambios: francés de Francia y tipografía (U+202F antes de ? ! : ; y apóstrofo ’, sin errores), concordancias (reconnaissant/e, remboursé/e/s/es), guías de pronunciación es/en (sh/zh, an/en nasales, ü y ö definidos en c16 p3), distintas glosas de los `relacionar`, pistas específicas de cada ítem, longitud de las situaciones (170 / 190 / 164 / 160 / 160 palabras, 150–250 pedidas), español neutro (sobregiro, cajero automático, departamento, ustedes) e inglés americano.
- Aviso para el coordinador (no se toca el plan): el objetivo en inglés de la ficha c18 dice «in a shop» (el borrador usa «store») y los títulos de c19/c20 llevan U+0020 antes de «?» y «:» (igual que los títulos ya publicados; el validador exige que coincidan con el plan).
- Palabras francesas eliminadas del bloque: de la situación de c19 solo `cartons`, `devis` y el diálogo de la mudanza. Ningún bloque posterior de N4 (b05–b10) las usa: la validación con n4-b01…b10 da 0 errores.

## Hechos del reparto confirmados

- Ana tiene una cuenta corriente en su banco desde hace tres años (coherente con N3 c01, donde lleva dos años en París) y trabaja en un hotel; en la sucursal abre una cuenta de ahorros para ahorrar 50 euros al mes para un viaje a Quito; trata de vous al asesor, sin nombre (c16). / Ana has had a checking account at her bank for three years (consistent with N3 c01, where she has been in Paris for two years) and works in a hotel; at the branch she opens a savings account to put aside 50 euros a month for a trip to Quito; she addresses the unnamed advisor with vous (c16).
- Emma pidió tres libros por internet el 5 de marzo con entrega prevista el 10; no llegaron. Llamó dos veces al servicio de atención al cliente, la empresa le escribió el 12 de marzo y ella redactó una carta de reclamación fechada el 20 de marzo; Ana le aconseja enviarla certificada con acuse de recibo; se tutean (c17). / Emma ordered three books online on March 5 with delivery scheduled for the 10th; they never arrived. She called customer service twice, the company wrote to her on March 12 and she wrote a complaint letter dated March 20; Ana advises sending it by registered mail with an acknowledgment of receipt; they use tu (c17).
- Ana compró una cafetera hace una semana que no funciona (defecto de fabricación, en garantía); en la tienda pide ser reembolsada (o cambiada), prefiere el reembolso, que se hará en cinco días, y devolverá el paquete al día siguiente; trata de vous al vendedor, sin nombre (c18). / Ana bought a coffee maker a week ago that doesn’t work (manufacturing defect, under warranty); at the store she asks to be refunded (or exchanged), prefers the refund, which will be made within five days, and will send the package back the next day; she addresses the unnamed salesperson with vous (c18).
- Ana y Emma ya viven en el departamento nuevo. Compraron un sofá y una estantería en una tienda que no entrega; Ana contrata a una empresa de mudanzas (vous) para recogerlos y entregarlos el sábado a las 9 h (dos horas, 80 euros, pago al terminar); Emma trabaja por la noche (c19). / Ana and Emma already live in the new apartment. They bought a sofa and a bookcase at a store that doesn’t deliver; Ana hires a moving company (vous) to pick them up and deliver them on Saturday at 9 a.m. (two hours, 80 euros, payment when finished); Emma works in the evening (c19).
- El wifi de Emma no funciona desde hace un mes; Emma escribe un mensaje muy informal a la compañía y Ana, que se tutea con ella, lo reescribe en versión firme y cortés (Je vous serais reconnaissante de…, Il serait souhaitable que…, Sans réponse de votre part…, asociación de consumidores como último recurso); Emma lo envía esa noche (c20). / Emma’s wifi hasn’t worked for a month; Emma writes a very informal message to the company and Ana, who uses tu with her, rewrites it in a firm, polite version (Je vous serais reconnaissante de…, Il serait souhaitable que…, Sans réponse de votre part…, consumer association as a last resort); Emma sends it that night (c20).

## Pendiente

Nada pendiente en el bloque. Fuera de él: el coordinador decide si ajusta en el plan el «in a shop» de c18 y el texto de la situación de c19 (la ficha aún dice que preparan la mudanza al departamento nuevo; el borrador ya sigue la cronología de c11).
