**GO**

# Revisión independiente · alemán f0 «Fundamentos» + Nivel 0 «Leer y pronunciar»

Fecha: 2026-10-06
Estado: **GO** (revisión editorial independiente hecha; correcciones aplicadas y publicadas)

Alcance: `borrador-f0.json` (8 unidades, 104 ejercicios) y `assets/contenido/de/nivel0/` (10 unidades, 40 lecciones).
Criterios: alemán correcto, es/en naturales, una sola respuesta, nada sin enseñar, sin Ecuador, Lumo solo en la bienvenida del Nivel 0.

## Cambios hechos en f0 (editados en `borrador-f0.json`)

Palabras usadas antes de enseñarse (hier, sind, spreche, kommt) y huecos con más de una respuesta posible:

- F2 (du/Sie): se quitó «Wir sind hier» (sind y hier se enseñan en F3 y F6) de la tabla, los ejemplos y e2. Ahora «Und ihr? — Wir? Gut, danke.» (e2: «Und ihr? — ___? Gut, danke.» → Wir).
- F3 (sein/heißen): ejemplo, i1 y audio de i3 sin «hier»/«auch» («Ihr seid Jan und Lena. Wir sind Mia und Tom.»). Explicación: «la raíz heiß- termina en ß» (antes decía que «heißen» termina en ß).
- F4 (der/die/das): «Der Mann ist hier» → «Der Mann heißt Tom» (ejemplo y e2).
- F5 (origen): la explicación (es/en) da kommen completo (kommt, kommen) porque los ejemplos usan «Lena kommt…».
- F8 (presentarte): la explicación enseña «Ich spreche … (sprechen = hablar / to speak)» antes de tabla, ejemplos y diálogo; en inglés se aclara que el «also» inglés es «auch»; i3 y e5 piden los verbos (heißen/wohnen; heißen/kommen/lernen) para que solo haya una respuesta válida; e2 (auch/also) pasa a «Yo también soy de Perú», porque «Ich komme also aus Peru» también era gramatical.

## Cambios hechos en Nivel 0 (editados en `tools/contenido/nivel0-de/generar.py`, regenerado)

- u01l03 (ee): se quitó «más tensa que la e española» / «tenser than the e in bed» (inexacto); ahora vocal pura y larga, sin el deslizamiento del inglés «say».
- u02l02 (E, I, J): decía «trampa para todos»; la trampa de E/I es solo de angloparlantes. Versión es: E e I como en español, J = «yot» (no «jota»), como la y de «ayer»; versión en: la y de «yes».
- u02l03: «con labios y dientes» → «dientes sobre el labio inferior».
- u03l01 (ä): añadidas referencias («la de perro» / «the e in bed»).
- u06l04 (-ig): el par «zwanzig / zwanzigste» no contrastaba (zwanzigste también lleva [ç]); ahora «König / Könige» (g final = ich; g entre vocales = g).
- u10l03 y evaluación: la pseudopalabra «Pfeuchen» usaba «pf», no enseñado en el Nivel 0; ahora «Zeuchen» (z + eu + ch).
- sonidos.json, sonido «w»: añadido «dientes sobre el labio» al nombre es.

## Comprobado y correcto (sin cambios)

Los ejemplos de los 26 sonidos de `sonidos.json` contienen de verdad el sonido. Descripciones de ich/ach, r de garganta frente a rr, -er vocalizada, ensordecimiento final (Hund/Tag), z/w/v, longitud (Staat/Stadt, Kuh, ß/ss), eu/äu, acento (Hotel, Musik, Elefant) y arranque glotal son correctas para es y en. u10 (evaluación) sin Lumo; Lumo solo en u01l01. Sin Ecuador/Quito en ninguna pieza. Ítems de f0 con una sola opción correcta.

## Verificación

- `python3 tools/contenido/ruta-de/validar.py`: 0 errores · 8 unidades · 118 vocablos · 104 ejercicios.
- `python3 tools/contenido/nivel0-de/generar.py` (validar_nivel0 de --bilingue): 10 unidades, 40 lecciones, 0 errores.
- `python3 tools/contenido/ruta-de/integrar.py`: f0 publicado (`assets/contenido/de/ruta/f0.json` igual al borrador).
- `python3 tools/validar_ruta.py de`: 0 errores en `de.f0.*` (solo los `de.a1.*` legados).
- `flutter test test/nivel0_test.dart test/fundamentos_test.dart`: verde (16 pruebas).

## Sin resolver

- Nombres propios (Brandt, Arnold, Roth, Kraus, Schneider, Ríos, Bremen, Bonn, Argentinien, Peru, Chile) aparecen sin estar enseñados ni en `palabrasLibres`; el validador no los marca (nombres casi transparentes). Para estrictez total, añadirlos a NOMBRES_LIBRES de `integrar.py` y `validar.py`.
- «Freut mich auch!» (F3) usa «auch», que se enseña en F8; se mantiene como fórmula fija con su traducción en la tabla.
- «ihr = ustedes (informal)» asume español americano (en España, «vosotros»); decisión editorial del curso (latino neutro).
- No se pudieron escuchar las pronunciaciones (faltan voces DE); la revisión es solo de texto.
