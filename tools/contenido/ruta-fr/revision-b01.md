# Revisión independiente · N1 francés, bloque 1 (clases 1–5)

- **Archivo:** `tools/contenido/ruta-fr/n1-b01.json` (`fr.n1.c01` … `fr.n1.c05`)
- **Revisor:** IA independiente (no autora), perfil profesor A1 de francés de Francia, con español latinoamericano e inglés americano.
- **Fecha:** 2026-10-01
- **Validador:** `python3 tools/validar_ruta.py fr --borrador tools/contenido/ruta-fr/n1-b01.json` → **0 errores**, sin advertencias.

## Veredicto: **GO** (después de las correcciones aplicadas en el archivo)

Es un bloque sólido. El francés está bien, el registro tu/vous es coherente y las tablas están completas (s'appeler y être con las 9 personas). Las explicaciones son cortas y bilingües. Los 6 formatos aparecen en el bloque. No había errores graves de francés. Los cambios corrigen una afirmación fonética falsa, varios ítems con más de una respuesta defendible y detalles de naturalidad. La anatomía cumple el encargo, salvo el formato «Repite», que el esquema todavía no admite.

## Recuentos

| Clase | Concepto | Vocablos | Errores frecuentes | Ítems | Reciclaje aprox. (palabras de clases N1 previas) |
|---|---|---|---|---|---|
| c01 | saludos | 10 | 2 | 16 | recicla Fundamentos (merci, ça va, très bien, comment allez-vous) |
| c02 | nombre | 10 | 2 | 15 | 35 % |
| c03 | estados | 10 | 2 | 16 | 59 % |
| c04 | deletrear | 8 | 2 | 16 | 45 % |
| c05 | nacionalidades | 10 | 3 | 17 | 43 % |

- **Ítems por formato (80):** elegir 20 · completar 19 · escuchar 12 · ordenar 10 · escribir 10 · relacionar 9.
- **Pasos:** explicación 10 · ejemplos 5 · vocabulario 5 · tabla 6 · patrón 2 · guiada 5 · independiente 5 · situación 5 · evaluación 5 (≥ 4 ítems y ≥ 3 formatos en cada una).
- **Tipografía meta:** 0 apóstrofos rectos y 0 signos sin U+202F en los campos en francés.

## Cambios aplicados (8 ejemplos antes → después)

1. **c01 · sonido del día: afirmación falsa.**
   Antes: «la consonante final casi nunca suena: «salut» = «salü», «bonjour» = «bonyur»» (da a entender que la r de bonjour es muda; además usa «ü» antes de definirla).
   Después: «…«salut» se dice «salü», sin t (ü = la u de «tu»). Pero la r final sí suena: «bonjour», «au revoir».» (lo mismo en inglés).

2. **c01 · situación: faltaba el modelo «Et vous ?».**
   Antes: Ana responde al panadero «Très bien, merci. Au revoir, bonne journée !» sin devolver la pregunta.
   Después: «Très bien, merci. Et vous ?» / Martin: «Très bien ! Au revoir, madame. Bonne journée !». Así el diálogo contrasta «Et vous ?» con «et toi ?», que es el objetivo de la clase. Se ajustó el feedback de s1.

3. **c01 i1 · ordenar con más de un orden válido.**
   Antes: solo «Au revoir, madame. Bonne journée !».
   Después: `aceptadas` + «Au revoir. Bonne journée, madame !» y «Bonne journée, madame. Au revoir !». Lo mismo en c01 e4 («À demain, salut !»), c03 i1 («Merci, ça va très bien.»), c04 i2 y e5 («S'il vous/te plaît, … ?»).

4. **c02 · nota de la tabla engañosa.**
   Antes: «je, tu, il y ils suenan igual («apel»)», aunque la tabla muestra «mapel», «tapel» y «sapel».
   Después: «appelle, appelles y appellent suenan igual («apel»); solo nous y vous cambian («aplon», «aplé»)».

5. **c02 · ejemplo redundante.**
   Antes: «Je te présente Léa. Elle s'appelle Léa.»
   Después: «Hugo, je te présente Léa !». «Enchanté, Léa !» lleva ahora una nota: una mujer escribe «Enchantée».

6. **c03 e6 · relacionar ambiguo.**
   Antes: «bof» = «regular» y «pas très bien» = «no muy bien», dos significados casi iguales en español.
   Después: «bof» se sustituye por «malade» = «enfermo / enferma».

7. **c03 g4 · pista que no sirve.**
   Antes: «¿Oyes la t al final?». Las tres opciones son femeninas, así que la t no distingue contenta de cansada o enferma.
   Después: ««content» se parece al español «contento»» / “content” looks like English “content” (happy).

8. **c04 · ejemplo poco natural.**
   Antes: «Mon nom, ça s'écrit comment ?» = «¿Cómo se escribe mi apellido?» (nadie pregunta cómo se escribe su propio apellido).
   Después: «Et le nom, ça s'écrit comment ?» = «¿Y el apellido, cómo se escribe?».

**Otros cambios:**
- c03: el error «Je suis bien» ahora aclara que la frase existe y significa «estoy cómodo».
- c03: el ejemplo de dos hablantes lleva raya («Tu vas bien ? — Je suis un peu fatigué.»).
- c03: la situación termina con Léa respondiendo al jefe «Ça va, merci. Et vous ?», y s2 se reformuló para que tenga una sola respuesta.
- c03 i3: acepta también «Ça va, comme ci, comme ça.» y «Bof…».
- c01 i2: acepta también «Salut, Léa ! Ça va ?».
- c05 g2: Emma pasa a ser Chloé, porque en la situación Emma es estadounidense.
- Textos de apoyo: las 80 citas en francés con espacio normal antes de ? o ! llevan ahora U+202F, para que el signo no quede solo al saltar la línea. Los apóstrofos rectos de los textos de apoyo siguen el estilo de `a1-1.json`.

## Notas de calibración para los autores de B2–B10

1. **Ordenar = varias respuestas.** En francés, las fórmulas de cortesía y los vocativos se mueven («Bonne journée, madame. Au revoir !», «S'il vous plaît, vous pouvez répéter ?»). En cada `ordenar`, prueba las permutaciones naturales y ponlas en `aceptadas`. La app ya admite `aceptadas` en ordenar.
2. **Una pista tiene que ayudar a resolver ESE ítem.** Si las opciones solo se distinguen por el significado, una pista de pronunciación o de género no sirve. Y en `relacionar`, las glosas tienen que diferenciarse claramente en los dos idiomas: nada de «regular» frente a «no muy bien».
3. **Fonética aproximada con cuidado.** No afirmes «la consonante final no suena» con una palabra que la pronuncia (bonjour, CaReFuL). Define «ü», «ö» y similares con el ancla del Nivel 0 («la u de tu») la primera vez que aparecen. Y cuando digas «X e Y suenan igual», que la columna de pronunciación lo muestre.
4. **Diálogos que modelen el objetivo.** Si la clase enseña a devolver la pregunta o a contrastar tu/vous, el diálogo tiene que mostrarlo en las dos formas. Cuida también la cortesía francesa: devolver «Et vous ?» y despedirse.
5. **Coherencia de personajes y una sola respuesta en comprensión.** Mantén estables los datos de cada personaje (Emma estadounidense, Martin el profesor o el jefe…). Al añadir líneas al diálogo, vuelve a comprobar que cada pregunta de comprensión siga teniendo una sola respuesta. Con hablantes femeninas, usa la forma femenina (enchantée, fatiguée) o añade una nota.
