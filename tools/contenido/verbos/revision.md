# Revisión independiente de verbos-en.json

**Veredicto: GO** (172 verbos revisados + 2 añadidos = 174).

## Resultado por tipo de cambio

| Tipo | Cambios |
|---|---|
| Formas (tercera/pasado/participio/gerundio) | 0 (las 172 ya eran correctas en inglés americano) |
| Campo `tipo` | 0 (regulares: pasado = participio en -ed; irregulares sin excepción) |
| Glosa `es` (más precisa o distinta) | 89 |
| Ejemplo (en/es) | 17 |
| Verbos añadidos | 2 (burn/burned, dream/dreamed) |

Motivos de los 17 ejemplos: quitar phrasal verbs (pick up, wake up, blow out, lie down, deal with), mejorar la traducción (take, pay, throw, ride, shoot, set) o mostrar mejor el sentido (shut, upset, slide, shake).

## Ejemplos antes → después

- do: "hacer" → "hacer (una acción)"; make: "hacer" → "hacer, fabricar"
- shut: "cerrar" → "cerrar (de golpe, con firmeza)"; close se queda en "cerrar"
- lend: "prestar" → "prestar (a alguien)"; borrow: "pedir prestado" → "pedir prestado (de alguien)"
- lie: "recostarse" → "acostarse, recostarse"; lay: "colocar" → "colocar (algo, con cuidado)"
- say: "decir" → "decir (palabras)"; tell: "contar" → "decir (a alguien), contar"
- pick (ejemplo): "Pick up your things, please." → "Pick a number from one to ten." (sin phrasal verb)
- wake (ejemplo): "I wake up at six." → "I woke early today."
- take (ejemplo es): "Toma un paraguas" → "Lleva un paraguas; puede llover."
- upset (ejemplo): "Loud noise upsets the baby." → "The news upset her."
- añadidos: burn (burns/burned/burned/burning), dream (dreams/dreamed/dreamed/dreaming)

## Comprobaciones (Python)

Infinitivos únicos; regulares con pasado = participio terminado en "ed"; irregulares no coinciden con la forma regular; ejemplo ≤ 10 palabras y contiene alguna forma del verbo; glosas `es` sin duplicados. Todo OK.

## Notas

- Sin modales ni phrasal verbs en la lista (ejemplos corregidos).
- Decisiones americanas confirmadas: gotten, traveled/traveling, learned, shone (intransitivo), lit.
- Pendiente opcional: "be" y "have" dependen de formas especiales del generador (no tocado).
