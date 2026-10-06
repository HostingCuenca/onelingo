# Revisión independiente · Nivel 0 español (U1–U5)

Revisor: fonética del español latino neutro (Quito) para anglohablantes.
Archivos: `cabecera.json`, `u01-u03.json`, `u04-u05.json`, `assets/contenido/es/nivel0/sonidos.json`.
Validador tras las correcciones: `integrar.py` + `validar_nivel0.py es --bilingue` → 5 unidades, 18 lecciones, **0 errores**.

## Veredicto: **GO**

La fonética y el marcado eran sólidos: seseo, ll/y = «y» de «yes», r simple = «tt» de «butter», rr, j/ge/gi = «strong h», d suave, b = v, h muda, gu/qu con u muda, ü que suena, vocales puras, todo bien. Los pares de escucha_elige/cambia se distinguen de verdad al oído (nada de casa/caza ni vaca/baca). Las fallas estaban en 3 pasos «construye» ambiguos por oído, una explicación falsa y piezas pedagógicas que faltaban. Ya están corregidas.

## Correcciones (antes → después, gravedad)

| # | Dónde | Antes → después | Gravedad |
|---|---|---|---|
| 1 | u05.l01 mira «aire» | «It is never the English "eye"» (falso: ai ≈ «eye») → «sounds close to the English word eye: EYE-reh», más ei ≈ «ay» de day y oi ≈ «oy» de boy | **Alta** (explicación falsa) |
| 2 | u01.l02 construye «uva» | fichas con `b` (uva/«uba» suenan igual, respuesta ambigua por oído) → fichas u,v,a,o,e | **Alta** |
| 3 | u03.l03 construye «barco» | ficha `v` («varco» suena igual) → fichas b,a,r,c,o,t,p | **Alta** |
| 4 | u05.l01 construye «reina» | ficha `y` («reyna» suena igual) → fichas r,e,i,n,a,o,u | **Alta** |
| 5 | u04.l02 | papa/papá solo aparecían como par de escucha sin explicar → nuevo paso Lumo: papa (PA-pa) = papas fritas/potato, papá (pa-PÁ) = dad | Media |
| 6 | u04.l02 | no se nombraban aguda/llana/esdrújula ni que la esdrújula siempre lleva tilde → nuevo paso Lumo con ejemplos (ca-FÉ, ME-sa, MÚ-si-ca, te-LÉ-fo-no) | Media |
| 7 | u04.l03 lee | «Emma es amiga de la familia Andrade» contradice el canon (Emma vive con los Andrade) → «Emma vive con la familia Andrade», pregunta «Who does Emma live with?», opciones familia / escuela | Media |
| 8 | u04.l03 mira y Lumo | «Your voice goes up at the end» para «¿Cómo estás?» (falso: las preguntas con palabra interrogativa suelen bajar) → solo las preguntas sí/no suben; la exclamación lleva energía | Media |
| 9 | u04.l03 Lumo | «Question words always carry a tilde» → «when they ask a question or begin an exclamation», con el contraste que/como/donde/quien en afirmaciones | Baja |
| 10 | u03.l04 lee | «El perro de Emma come queso» (Emma acaba de llegar; el perro es de la familia) → «El perro de los Andrade come queso» | Baja |
| 11 | u01.l02 escucha | «lima» con emoji de limón (1f34b) → «mapa» con 1f5fa | Baja |
| 12 | u02.l02 escucha | «gelatina» con emoji de flan (1f36e) → sin emoji | Baja |
| 13 | u01.l04 Lumo | decía que m,n,p,l,t,f son como el inglés pero las frases usan s, c, v, d → aviso de que s, c, v, d tienen lección propia en la unidad 3 | Baja |
| 14 | u04.l02 escucha | «plátano = banana» (en Ecuador es plátano verde) → «banana (plantain in some countries)» | Baja |
| 15 | u05.l03 Lumo final | «Ya lees español!» sin ¡ → «¡Ya lees español!» | Baja |

Total: **15** (4 altas, 4 medias, 7 bajas). Marcado fonético: 0 cambios (ningún id de sonido estaba mal).

## Comprobaciones hechas

- Marcado: c=s ante e/i, c=k ante a/o/u, z=s, qu=k con u muda, gu=g con u muda, ü=u, ll/y=y, y final/sola=i, h muda, ñ, ch, g=jota ante e/i, rr inicial y tras n/l/s. Todo correcto.
- Ningún sonido de consonante coloreado antes de su unidad (script propio sobre sonidos.json); el color aparece dentro de la unidad 3 antes de su lección, lo cual cumple la regla por unidad.
- toca_sonido: una sola opción con el sonido (lo comprueba el validador). escucha_elige: audio = opción correcta. cambia: una sola letra y una sola respuesta plausible por oído.
- Pares mínimos reales y audibles: pera/para, mono/mano, luna/lana, me/mi, ojo/oso, gente/mente, pollo/polo, uña/una, niño/nido, perro/pero, carro/caro, queso/beso, sol/col, vaso/paso, barco/parque, gato/pato, calor/color, auto/alto, reina/rana, hielo/helado, huevo/nuevo, cuatro/cuarto, piña/pila, guitarra/guerra.
- Reglas de acento: terminada en vocal/n/s → penúltima; otra consonante → última; tilde cuando se rompe la regla; ejemplos con sílaba fuerte correcta (ca-FÉ, a-VIÓN, ÁR-bol, LÁ-piz, MÚ-si-ca, te-LÉ-fo-no, pa-ÍS, ma-ÍZ). si/sí, tu/tú, el/él bien explicados.
- Inglés americano en todo el apoyo; sin clave «es»; Lumo siempre solo; voz «narradora».
- Frases con Emma/Andrade coherentes con curriculo/es/MAPA.md (Emma vive en Quito con los Andrade, perro de la familia).
- Emoji: todos de Noto y el validador no reporta faltantes.

## Sin resolver

1. **Audio TTS de papa/papá** (u04.l02): el par depende de que el TTS acentúe bien. Conviene escucharlo una vez en la app.
2. **`d` tras n o inicial** (donde, Andrade) comparte el id `d` del sonido suave; la enseñanza lo explica (inicial = d inglesa). Aceptable, sin id aparte.
3. **ll = y** es yeísmo, normal en Quito; no hay aviso de variantes (es el criterio «latino neutro»).
4. **«hielo»/«hierba»** se marcan con i aunque suenan como «ye»; la lección ya explica que la i débil actúa como «y».
5. **«huevo»** aparece en u02 antes de enseñar diptongos (u05); suena u+e sin problema y se retoma en u05.
6. **«be larga / ve corta»** es habitual en Ecuador pero hay variantes (be alta/ve baja); no es crítico.
