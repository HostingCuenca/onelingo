# Revisión independiente de verbos-pt.json

**Veredicto: GO** (125 verbos revisados, 0 añadidos, 0 quitados; `generar_verbos.py --comprobar` = 0 errores).

## Método

Las 5.250 formas (125 × 7 tiempos × 6 personas) y los 125 participios (5.375 comprobaciones) se compararon con un conjugador escrito aparte por el revisor: reglas regulares -ar/-er/-ir, tablas irregulares propias (ser, estar, ter, vir, ir, fazer, dizer, trazer, poder, querer, saber, caber, dar, ver, pôr, propor, manter, ler, crer, rir, sorrir, sair, cair, construir, valer, perder), cambios ortográficos (c→qu, g→gu, ç→c, c→ç, g→j, gu→g), cambios vocálicos de la 1.ª persona (dormir→durmo, pedir→peço, sentir→sinto, vestir→visto, medir→meço, servir→sirvo, ouvir→ouço), subir→sobe, fugir→foge, cobrir→cubro/cobre, y participios irregulares del uso brasileño (ganho, gasto, pago, aceito, entregue, pego, aberto, escrito, feito, dito, posto, visto, vindo, coberto, morto). Ortografía post-Acordo (pôr, pôde, vêm, veem, leem, creem, dão, constrói). Se comprobó también que «você» copia «ele/ela» y «vocês» copia «eles/elas» en los 7 tiempos, y el campo `tipo` con la regla del LEEME.

## Discrepancias

| Verbo | Antes | Después |
|---|---|---|
| começar | começei; presente do subjuntivo começe… | comecei; comece, comecemos, comecem |
| dançar | dançei; dançe… | dancei; dance, dancemos, dancem |
| descer | desco; desca, descamos, descam | desço; desça, desçamos, desçam |
| começar, dançar, descer | `tipo` regular | irregular (cambio ortográfico) |

Todo lo demás coincidió: 0 diferencias en pretéritos fuertes, futuros irregulares (farei, direi, trarei, porei, virei), formas con hiato (leem, veem, saíamos, construíamos) ni participios. produzir queda `irregular` (3.ª persona «produz» sin -e).

## Traducciones y ejemplos

| Verbo | Cambio |
|---|---|
| pegar | es «tomar, agarrar, coger» → «tomar, agarrar» (coger es vulgar en parte de Latinoamérica) |
| dirigir | es «conducir, dirigir» → «manejar, conducir; dirigir»; ejemplo «Dirijo para o trabalho.» (poco natural) → «Dirijo até o trabalho.» / «Manejo hasta el trabajo.» |
| aceitar | ejemplo con persona distinta en cada lengua (pt «Aceito», es «Aceptamos») → «Aceito o convite.» / «Acepto la invitación.» / «I accept the invitation.» |
| partir | es «El tren parte a las diez» → «El tren sale a las diez.» |

Niveles 1–4: sin cambios; la asignación es coherente con la frecuencia (ser, ter, ir, fazer, comer… en 1; valer, caber, crer, cumprir, mexer… en 4). Ningún contenido menciona Ecuador, Quito ni Guayaquil.

## Notas

- jogar, trocar, buscar, ligar, chegar, ficar y pagar son `irregular` por ortografía (g→gu, c→qu): correcto.
- Los ejemplos de trazer, seguir, olhar y repetir usan el imperativo (= forma del subjuntivo, que está en la tabla); se dejaron porque son el uso natural del verbo.
- Copia previa al cambio: scratchpad del revisor (`verbos-pt.bak.json`).
