GO

# Revisión N1 · B1 (pt.n1.c01–c05)

Validador: `python3 tools/curriculo/validar_bloque.py pt 1 1` → 0 errores. Unas 22 correcciones directas en `n1-b01.json`.

## Cambios por tipo

**Nombres de las fichas restaurados (13 ítems/unidades)**
- c01: e4 Helena/Paula → Nara/Mia; e5 Lara → Sofia.
- c02: i1 Helena → Júlia (también en erroresFrecuentes); g2 Paulo → Rafael; i2 Paula → Clara; e3 Marina → Carolina; e4 Helena/Igor/Luana (ver abajo).
- c04: situación Joana → Carolina (Joana se mantiene en i2, como en la ficha).
- c05: Helena → Marie, Paula → Rosa en ejemplos, explicación y situación; e5 Pedro → João (+ aceptadas).
- Ninguno choca con el MAPA (Carolina es el nombre de las «otras Camila» de las fichas; Rafael, Clara, Júlia, Sofia, Nara, Mia, Igor, Luana, Marie, Rosa, João son secundarios libres).
- No restaurado: «Laura» (c02 e5, ficha) → se queda «Lara» porque «Laura» no está en `palabrasLibres` (el validador la rechaza). Si el integrador añade «Laura», se puede volver.

**Decisiones del encargo**
- c02 «mexicano»→«argentino»: correcto. «mexicano» se enseña en c05; «argentino» ya está en f0. Además se cambió Diego → Davi en e2, porque en c05 Diego es mexicano (evita dos nacionalidades para el mismo personaje).
- c03 «Até amanhã / Boa viagem» → «Tchau!»: correcto (despedida de f0, distractor inequívoco en una fórmula de bienvenida).
- c04 «a sua» y «o Peru» como frase fija: correcto; la explicación avisa de que «a sua» se estudiará más adelante y no se analiza.
- Formato de relacionar: se ajusta al esquema y al modelo francés (portugués a la izquierda, TextoApoyo a la derecha). El autor invirtió la dirección de la ficha (persona↔frase) en varios ítems; es válido y de una sola respuesta. En c02 e4 se volvió a la idea de la ficha (nombre↔presentación con «ele/ela se chama»), con las fotos Helena/Igor/Luana, en vez de nacionalidades extra («canadense») que no pertenecen a la ficha.
- Hablante «Cliente» en c03: es el papel en portugués y la clienta no tiene nombre en el reparto; correcto (modelo francés usa «Le boulanger»).

**Sonido del día**
- c03: la ficha decía «e final átona em você» (error: «você» es tónica). Validado «ê tónica de você + r final suave de prazer/conhecer». Corregido «vo-SSÊ» → «vo-SÊ» y la guía inglesa «voh-SEH» (sugería vocal abierta) → «voh-SAY» (ê cerrada, sin el deslizamiento inglés).
- c02: «este» tiene «ê» cerrada, no «é» abierta: «éschi/éstchi» → «êstchi».
- c01, c04, c05: correctos (nome → «nômi»; entonación descendente en palabras interrogativas y «qual» ≈ «quau»; «r» simple = «pero», «s» entre vocales = «z»).

**Errores frecuentes incorrectos (2)**
- c03: «Como vai você, colega?» se presentaba como error, pero «Como vai você?» es portugués correcto → sustituido por «Prazer en conhecer você.» → «Prazer em conhecer você.» (error real de hispanohablante).
- c04: «De onde é você?» se presentaba como error, pero es gramatical (inversión con ser) → sustituido por «De donde você é?» → «De onde você é?».

**Otros**
- c03 e6 escribir: aceptadas añade «Prazer em conhecer você».
- c05 s1: feedback «Diego es del México» → «Diego es de México.».
- Sin falsos amigos nuevos que faltaran: ⚠ sobrenome/apelido (c01), ⚠ brasileño (c02, c05) y ⚠ «donde» (c04) están marcados. No se detectó Ecuador ni hechos inventados.

## Revisado y sin cambios
Cobertura de las fichas (introduce/recicla/vocabulario/plan de ejercicios) completa; una sola respuesta por ítem; distractores = errores reales (se/me omitido, género de la nacionalidad, «brasileño», este/esta); apoyo {es, en} exacto; nivel A1; 5 clases con los seis formatos a lo largo del bloque (elegir, escuchar, ordenar, completar, escribir, relacionar).

## Hechos del reparto confirmados
- Camila Ortega conoce a Caio, compañero nuevo, el primer día en la Escola Capibaribe de Português (Graças) (c01, c02): Caio es compañero de curso (secundario libre).
- Camila presenta por foto en su celular a Lucas (brasileño) y Ana (brasileña, amiga) (c02).
- Ana, diseñadora de Maré Digital (Porto Digital), recibe con «a senhora» a una clienta en la recepción (c03); Cliente es un papel sin nombre.
- Carolina es peruana, de Lima, compañera de curso de Camila (c04). Camila es «de Miami» (c04).
- Diego es mexicano, Marie francesa (de Francia), Rosa peruana (c05); Davi es argentino (c02), Laura/Lara y Helena, Igor, Luana solo aparecen en ejercicios sin nacionalidad fija (Lara canadiense ya no se usa).
- Nacionalidades enseñadas en este bloque: brasileiro/a, mexicano/a, francês/francesa, peruano/a (+ argentino/a y canadense desde f0). Fórmulas: eu me chamo, você se chama, este é/esta é, prazer em conhecer, tudo bem?, como vai?, de onde você é?, qual é a sua cidade?
- Trato: «a senhora» con una clienta; você con compañeros.

## Sin resolver
- «Laura» (ficha c02 e5) pendiente de añadirse a `palabrasLibres` si se quiere restaurar (hoy «Lara»).
- Las fichas c02 y c05 pedían «mexicano» en c02 (antes de c05, donde se introduce): el plan debería moverlo.

## Pasada de escucha

Se convirtieron a `escuchar` (audio pt-BR de la frase, opciones es/en, misma clave 0): c01 i1, c02 i1, c03 i1, c04 i1, c05 e1 e i1, y en el bloque 2 c06 g3, c07 e3, c08 g3, c09 g3, c10 g3. Cada clase queda con 2 escuchar (c05 con 2 nuevos). Sin otros cambios.
