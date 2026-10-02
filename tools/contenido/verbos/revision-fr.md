# Revisión independiente de verbos-fr.json

**Veredicto: GO** (120 verbos revisados, 0 añadidos, 0 quitados).

## Método

Las 3.000 formas (120 × 5 tiempos × 6 personas) se compararon con un conjugador escrito aparte por el revisor: tablas irregulares propias, cambios ortográficos (-ger, -cer, -eler/-eter, è/é, -yer), auxiliar être con concordancia «(e)», «(e)s», «(e)(s)» y pronombres reflexivos con elisión (m’, t’, s’). Coincidieron en todo salvo `passer` (ver abajo). Traducciones, ejemplos y niveles se revisaron uno por uno.

## Recuento

| Tipo | Verbos |
|---|---|
| regular (-er, incluidos los de cambio ortográfico, y -ir tipo finir) | 68 |
| irregular | 52 |
| de ellos, reflexivos | 10 |
| nivel 1 / 2 / 3 | 40 / 45 / 35 |

## Cambios

| Tipo de cambio | Nº |
|---|---|
| Formas conjugadas | 0 (todas correctas; futur simple tradicional «préférera», «achètera», «appellera», «jettera», «paiera», «essaiera», «enverra»…) |
| Campo `tipo` | 0 (envoyer y aller irregulares; payer, essayer y nettoyer como -er regulares con cambio ortográfico) |
| Espacio fino U+202F antes de ? y ! | 17 ejemplos |
| Ejemplo reescrito | 1 (aider) |
| Nivel ajustado 3 → 2 | 5 (monter, revenir, perdre, rencontrer, entendre) |

`passer` se queda con avoir («ai passé»): la glosa es «pasar (tiempo)» y el ejemplo es «Nous avons passé un bon week-end», así que el auxiliar coincide con ese uso. Los demás verbos de movimiento (entrer, sortir, monter, descendre, rentrer…) llevan être.

Las horas («14 h», «18 h») siguen con espacio normal, como en el resto de `assets/contenido/fr`.

## Ejemplos antes → después

1. faire: «Qu’est-ce que tu fais ce soir ?» (espacio normal) → «…ce soir ?» con U+202F
2. pouvoir: «Tu peux m’aider ?» → U+202F antes de «?»
3. tomber: «Attention, tu vas tomber !» → U+202F antes de «!»
4. sentir: «Ça sent bon ici !» → U+202F antes de «!»
5. se dépêcher: «Dépêche-toi, on est en retard !» → U+202F antes de «!»
6. répéter: «Vous pouvez répéter, s’il vous plaît ?» → U+202F antes de «?»
7. aider: «Mon frère m’aide avec les devoirs.» (calco) → «Mon frère m’aide à faire mes devoirs.»; es «…me ayuda con la tarea.» → «…me ayuda a hacer la tarea.»
8. monter: nivel 3 → 2 (igual que descendre)
9. revenir: nivel 3 → 2 (muy frecuente desde A1-A2: «Je reviens dans cinq minutes»)
10. perdre / rencontrer / entendre: nivel 3 → 2 (vocabulario básico de A2)

## Comprobación

`python3 tools/contenido/verbos/generar_verbos.py --comprobar` no muestra líneas ERROR; solo avisa «verbos.json desactualizado (fr)», que se arregla volviendo a generar.
