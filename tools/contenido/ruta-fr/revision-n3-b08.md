# Revisión N3 · B8 (fr.n3.c36–c40)

GO

Revisor independiente (otro agente que el autor). Alcance: `tools/contenido/ruta-fr/n3-b08.json` (único archivo editado, más esta revisión). Verificado contra las fichas de `curriculo/fr/n3.json` (títulos, gramática, introduce/recicla, vocabulario, situación, tarea y plan de ejercicios), `ENCARGO_RUTA_FR.md` (tabla N3 y calibración 1–10), `ESQUEMA_CONTENIDO.md`, el reparto de `n1.json`/`n2.json` y los bloques anteriores de N3 (b01–b07).

Validación final:
- `python3 tools/validar_ruta.py fr --borrador n3-b01 … n3-b08` → **0 errores** (b07 ya valida sin errores; no hizo falta encadenar sin él).
- `python3 tools/curriculo/validar_plan.py fr` → sin «título de la unidad difiere» para fr.n3.c36–c40 (solo avisos antiguos de N1).

Resumen de lo comprobado y correcto (sin cambios): contenido fiel a las fichas, sin gramática de clases posteriores; plan de ejercicios completo en cada clase (guiada, independiente, comprensión de situación y evaluación con el mismo formato y clave); evaluación de 5 ítems puntuables en 5 formatos + 1 `escribir` abierto (`abierta: true`) que no reemplaza a los puntuables; los seis formatos presentes en cada clase; `ordenar` con tokens = respuesta y `aceptadas` con los órdenes naturales (c39 g4/e4); `relacionar` con 3–4 pares de glosas distintas; pistas solo en práctica guiada y útiles; hablantes = nombres o papeles franceses (Le directeur, La conseillère, L’employée, Madame Dubois, Ana, Emma); textos de situación de 154–167 palabras (150–250); notas de pronunciación conformes a la calibración 6 (j/g = «sh»/«zh», nasales = «en»/«an», ü y ö definidos en c36); español neutro (departamento, mensaje de texto, correo electrónico) e inglés americano (apartment, package, sick); tipografía francesa con U+202F en todos los campos franceses.

## Correcciones

### c36
- explicacion p1 (en): «French has no “to” but de + infinitive» confuso → «French uses de + infinitive (like English “to”), never que».
- e3 feedback (es/en): «Venir à huit heures y de ne pas oublier les clés = llevar las llaves» → glosa clara: venir à huit heures + ne pas oublier les clés = llegar a las ocho y no olvidar las llaves (llevarlas).

### c37
- situacion, línea 6 de Ana: «Madame Dubois, elle demande ce que vous voulez.» (ambiguo: parecía que Madame Dubois preguntaba) → «La conseillère demande ce que vous voulez. Elle veut savoir où vous habitez.» (es/en ajustados).

### c38
- situacion, correo del director: «je reste à la maison cette semaine» contradecía proponer la reunión el miércoles → «je reste à la maison lundi et mardi» (es/en ajustados).
- explicacion p1 (es/en): «la misma estructura de demander de de la clase anterior» (la anterior es c37; demander de está en c36) → «que viste dos clases atrás (c36)» / «from two classes ago (c36)».

### c39
- e1 y tabla p4: «c’est le lundi» (= todos los lunes, y no coincide con g4) → «c’est lundi».
- vocabulario `en fait` (en): guía «ahn FEH» contradecía la guía en español (la -t suena) → «ahn FET … the t of fait is pronounced here».
- e2 (elegir): solo 2 opciones (50 % de azar) → se añade la opción «Donc» (3 opciones); feedback ampliado.
- e5 (escribir): `aceptadas` + «Pourriez-vous me dire ce que vous entendez par « référence » ?» (forma cortés enseñada en la clase y válida con la consigna).
- g1 pista: «Es el verbo que sigue a voulez…» (no ayudaba) → «Después de voulez va un infinitivo: el verbo “decir”» (es/en).
- Glosa en inglés de «C’est-à-dire ?» como «That is?» → «Meaning?» (ejemplo 1, línea 4 del diálogo y e2).

### c40
- situacion, `contexto`: decía que Ana ya le había dicho a Emma lo importante, pero el texto («je le lui ai dit») se refiere a Madame Dubois → contexto reescrito (Ana ya contestó a Madame Dubois y ahora transmite el recado a Emma).
- situacion, última línea de Ana: «Je fais passer ton message à Madame Dubois» (Emma no manda ningún mensaje) → «Je fais passer le message à Madame Dubois» (es/en).

### Todo el bloque
- Tipografía: en los textos de apoyo (es/en) los fragmentos franceses llevaban espacio normal antes de ? ! : y en « » → sustituido por U+202F (como en N2 publicado). No se tocaron `titulo`/`objetivo` de las unidades (coinciden con el plan).
- Posición de la respuesta correcta en `elegir`/`escuchar`: casi todas estaban en la 1.ª opción → redistribuida (33 ítems: 11 / 11 / 11 en posiciones 0 / 1 / 2). Sin otras diferencias de contenido.

## Hechos del reparto confirmados

- El director del hotel donde trabaja Ana (en la recepción) deja un mensaje de voz: está en reunión todo el día y pide que lo llame antes del mediodía, que su compañero llegue a las 8 mañana, que no se vaya antes de las 6 y que le envíe la lista de reservas (c36) / The hotel director (Ana works at the front desk) leaves a voicemail: he’s in a meeting all day and asks her to call back before noon, her colleague to arrive at 8 tomorrow, her not to leave before 6, and to send him the reservations list (c36).
- El director está enfermo y se queda en casa lunes y martes; aplaza la reunión del lunes al miércoles a las 10; el jefe de recepción está ausente el miércoles; promete enviar los horarios y se queja de que muchos olvidan firmar la lista (c38) / The director is sick and stays home Monday and Tuesday; he postpones Monday’s meeting to Wednesday at ten; the head of the front desk is absent Wednesday; he promises to send the schedule and complains many forget to sign the list (c38).
- Madame Dubois (propietaria, vive en la planta baja, se trata de vous con Ana) llama a la compañía de electricidad con la línea mala; su número de cliente es 305, firmó el contrato en marzo y la electricidad de su cocina ya no funciona; Ana hace de intermediaria (c37) / Madame Dubois (landlady, ground floor, vous with Ana) calls the electric company on a bad line; her customer number is 305, she signed the contract in March and the kitchen electricity no longer works; Ana acts as go-between (c37).
- Ana espera un paquete desde hace diez días (dice «una semana» y se corrige); plazo de 48 horas, gastos de trámite de 10 euros, el número de referencia está en la etiqueta del paquete (c39) / Ana has been waiting for a package for ten days (says “a week” and corrects herself); 48-hour deadline, 10-euro processing fee, the reference number is on the package label (c39).
- Madame Dubois deja un petit mot en la puerta: nada de ruido después de las 22 h (coincide con las normas de N2 c45), nada grave, duerme mal; mañana a las 9 alguien revisa la calefacción; Ana y Emma se tutean y Ana ya le respondió a Madame Dubois que harán caso (c40) / Madame Dubois leaves a note on the door: no noise after 10 p.m. (matches N2 c45 house rules), nothing serious, she sleeps badly; someone will check the heating tomorrow at nine; Ana and Emma use tu and Ana has already told Madame Dubois they will comply (c40).
- Coherencia previa: Ana vive en el primer piso francés (second floor) sobre Madame Dubois, comparte departamento con Emma y trabaja en el hotel (N2/N3 nota, N3 b01/b07); ningún hecho nuevo contradice N1–N2 ni b01–b07. El director y el jefe de recepción son personajes nuevos sin nombre.

## Pendiente / sin resolver

- Ninguna palabra francesa enseñada fue eliminada o renombrada: los bloques posteriores (b09–b10) no se ven afectados.
- Nota para el integrador: el borrador usa `situacion` con 2–15 turnos de diálogo (c36 y c38 con dos turnos largos: mensaje + resumen de Ana); es intencional (mensaje de voz/correo + transmisión) y cumple 150–250 palabras.
