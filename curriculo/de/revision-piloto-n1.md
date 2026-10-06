GO

# Revisión independiente del piloto N1 c01–c10 (plan de alemán, método ligero)

Revisor distinto del autor. Archivos: `curriculo/de/n1.json` (c01–c10, estado `planificado`), contra `tools/curriculo/de/n1-outline.json` y `curriculo/de/f0.json`.
Validadores tras las correcciones: `validar_plan_detallado.py de curriculo/de/n1.json --parcial` = 0 errores (133 ejercicios); `validar_plan.py de` = 0 errores.
Campos congelados del outline: sin tocar. Solo se editó `ejercicios` (31 cambios, ver abajo).

## Veredicto por criterio

1. **Progresión A1 c01–c10:** sensata (saludo formal, nacionalidad, presente regular, correo, ihr, profesión, e de unión, cambio vocálico, gern, mögen). Reservas de outline (no modificables aquí): c01 repite casi todo f0 (greetings, Herr/Frau, Wie geht es Ihnen) y la `tarea` de c08 pide «cómo van al trabajo», lo que a este nivel exige dativo (mit dem Auto/Fahrrad); se resolvió con «Fährst du Auto? — Nein, ich fahre kein Auto» (todo ya enseñado). c04 (correo) es una clase de micro-habilidad útil pero muy estrecha.
2. **Alemán:** correcto en todo lo revisado (género de profesiones, -in, Deutscher/Deutsche sin artículo, V2, mayúsculas, ä/ö/ü/ß, ihr seid / du wartest / du fährst). No hay errores de lengua graves; los problemas eran de pedagogía y de ambigüedad (ver abajo).
3. **Una sola respuesta:** había 3 `ordenar` con dos órdenes válidos (vocativo al final: «Wie geht es Ihnen, Frau Neumann?» / «Wo wohnen Sie, Frau Berger?»; «Seid ihr zusammen hier?» / «…hier zusammen?») y varios `escribir` demasiado abiertos (c01 devolver la pregunta, c03 dos verbos + «Deutsch» que no estaba en el estímulo, c05 «Seid ihr» vs «Kommt ihr»). Corregidos.
4. **Consignas es/en:** claras; una consigna errónea («tú (ich)», c03: ich es «yo») corregida; la consigna de c05 ahora fija el verbo (sein / kommen).
5. **Errores frecuentes reales:** no hay campo para ellos en la ficha; los ítems ya cubren los típicos: *«Ich bin ein Lehrerin / Ich bin eine Lehrerin» (artículo con profesión), *«Ich bin mexicano/Mexikano», *«Ich nicht tanze gern», *«Ich mögen», *«Du fahrst», *«Du wartst», *«Seid ihr…» vs «Sind Sie…», *«Spricht du». Los autores de bloque deben añadirlos en `erroresFrecuentes`.
6. **Autonomía y personajes:** cada clase es una situación aislada; nombres genéricos sin continuidad (Jonas, Lena, Anna reaparecen solo como etiquetas, sin hechos). Sin Lumo, sin Ecuador/Quito (comprobado).

## Cambios (31)

- **Situaciones reescritas (10):** 1) con **etiqueta de hablante** («Herr Wolf: …») en todas, porque el diálogo con «—» sin etiqueta no permitía saber quién habla ni formular las preguntas sin ambigüedad (c05, c06, c07 eran confusas, c09 tenía una pregunta mal atribuida: «Completa lo que dice Lena» cuando lo decía Felix); 2) se quitó la línea de escenario en alemán («Am Empfang einer Firma in Köln», «Im Sprachkurs füllt die Gruppe eine Liste aus», «Zwei Personen warten am Bahnhof»…): traía palabras no enseñadas (Empfang, Firma, ausfüllen, fragt, am, einem, Hostel) y dativos; 3) se sustituyó vocabulario no enseñado: Chile/Peru/Argentinien/Madrid/Santiago por países de f0 (c05); «Musik» (c03, aparece en c10); «aber», «nicht so», «noch», «viel», «nach Hamburg», «mit dem Auto/Fahrrad», «im Büro/Krankenhaus», «am Bahnhof», «Alles klein», «mit z» (todos no enseñados o dativo prematuro); «Was machst du?» (ambiguo, = «¿qué haces?») por «Was bist du von Beruf?» / «Was seid ihr von Beruf?».
- **Ítems (21):** c01 ×2, c02 ×1, c03 ×3, c04 ×2, c05 ×6, c08 ×5, c09 ×1, c10 ×1: orden único, consignas aclaradas, distractores absurdos sustituidos («ein Kolumbianerin» → «Kolumbianerin»; «Punkt» como letra → «Zet»), cues completos en `escribir` (c08 «ein bisschen»), «schreibe» (no enseñado) sustituido por «wohnst» (c04), «Wasser» (no enseñado) por «Kaffee» (f0), `escuchar` sin «aber».
- Sin cambios: c06 (solo situación), c07 (solo situación): ejercicios sueltos correctos.

## Problemas sistemáticos que deben evitar los autores de las 490 fichas restantes

1. **Palabras no enseñadas en la situación, la cabecera de escena y los distractores.** La mayor fuente de errores: la línea de escenario y las ciudades/países/profesiones «de color». Solo vocabulario de f0, de clases anteriores y de la propia ficha; el resto, nombres propios.
2. **Gramática que aún no se enseñó colándose por el entorno:** dativo (im, am, mit dem, bei der, zur), acusativo masculino (keinen, einen), «aber/denn/und» antes de su clase, nach/zu. Mientras el nivel no los introduzca, usar nominativo y estructuras de la ficha. Atención futura: «Ich mag keinen Sport» (acusativo de kein) antes de la clase de acusativo.
3. **Vocativo/orden libre en `ordenar`:** «…, Frau X» al final y adverbios (heute, zusammen, hier, gern) permiten varios órdenes válidos; elegir frases donde el orden sea único o declarar las variantes en `aceptadas`.
4. **`escribir` demasiado abierto:** el estímulo debe contener todas las palabras de la respuesta salvo la forma evaluada; la consigna fija el verbo («con sein», «con kommen»).
5. **Diálogos sin etiquetas** (quién habla) en situaciones de 3+ personas; preguntas atribuidas a quien no habla.
6. **Reciclaje:** comprobar que cada clave de `recicla` aparece al menos una vez (en c06 no se usa `email-address`; es un hueco menor aceptado).
7. **Falsos amigos:** el piloto no tocó ninguno (c01–c10 no los activan); los bloques con Chef, Termin, Karte, etc. deben marcarlos con ⚠ según el encargo.

## Formato de ficha: ¿ligero y completo?

Sí: lo bastante ligero y no ambiguo para clases de 10–12 min. Con esto un autor puede escribir la clase sin consultar nada más. Carencias detectadas, en orden de importancia:

1. **Formalizar etiquetas de hablante:** exigir «Nombre: texto» (o rol alemán) en cada línea de `situacion.texto` y prohibir línea de escenario en alemán en N1–N2 (o limitarla a palabras ya enseñadas). El validador ya acepta «:» (≥ 2 por texto).
2. **Campo corto `error` (1 por ficha):** el típico de hispanohablante que la clase debe corregir («*Ich bin eine Lehrerin»). Hoy se inventa en el bloque; con el campo el revisor lo comprueba contra los ítems.
3. **Regla `ordenar`:** añadir al formato «solución única; si el Vorfeld admite otra, listarla en `aceptadas` al escribir el bloque».
4. **Validador (sugerido):** aviso cuando una palabra de situación, opciones o ejemplos no figura en f0 ni en `vocabulario` de la clase actual o anteriores (la regla «nada sin enseñar» hoy solo la comprueba `validar_ruta.py` en el bloque, tarde y con coste de reescritura); aviso cuando una situación de ≥ 3 líneas carece de etiquetas.
5. **Encargo:** corregir la calibración: «Anotar errores del piloto» → remitir a este acta.

## Sin resolver

- Outline c01: no introduce nada nuevo respecto a f0 (decisión de diseño; el bloque debería enfatizar Herr/Frau + apellido y el golpe de glotis).
- Outline c08 (`tarea` «cómo van al trabajo») y c07 («bei + empresa», vocabulario `im Büro`): el bloque debe enseñar «im» como bloque fijo o evitarlo.
- Verificación de audio de-DE (Umlaut, ich/ach) pendiente según el Encargo (calibración 1).
