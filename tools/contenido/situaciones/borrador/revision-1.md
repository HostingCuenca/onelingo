# Revisión lote 1 (situaciones 1–10)

**Veredicto: GO**

Validador: `python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/borrador/lote-1.json` → 10 situaciones, 0 errores (antes: 22).
Ids y estructura intactos. Los objetivos básicos s<id>-o1..o3 conservan su significado original.

## Cambios (365 campos editados en 212 entradas)

| Tipo | Campos | Qué se tocó |
|---|---|---|
| Inglés americano (ortografía y léxico) | 169 | bill→check, starter→appetizer, trousers→pants, trainers→sneakers, lift→elevator, zip→zipper, overhead locker→bin, queue→line, till→register, faulty→defective, car park→parking lot, kilo→pound, etc. |
| Naturalidad | 119 | colocaciones rígidas o poco usadas por un nativo (p. ej. «Is this seat free?», «Is this coffee for takeaway?», «Do you sell…?») |
| Vocabulario | 49 | entradas que eran frases enteras («Can I have it decaf?», «Could I have some water?») o repetían otra, cambiadas por palabras o colocaciones útiles de la situación |
| Español neutro/precisión | 26 | peninsularismos y traducciones imprecisas (manta→cobija, recogida de equipaje→reclamo de equipaje, «frutos secos»→nueces, medium rare, «vale la pena» en vez del que marca el validador) |
| Progresión de nivel | 2 | objetivos avanzados reformulados con más matiz (grupo de doce, retraso con conexión); el resto de la progresión ya era correcta |

Verificado además: ningún `en` se repite entre tramos de la misma situación y cada «ejemplo» contiene el `en` exacto.
Situaciones sensibles (alergias, salud a bordo, migración): solo lenguaje, sin consejos profesionales.

## Ejemplos antes → después

1. s1-b-v1/v2 `bill` → `check` ("Could we have the check, please?"); también s1-o3 «Could I see the bill?» → «Could we have the check, please?».
2. s1-b-v4 `starter` / «We would like a starter…» → `appetizer` / «We'd like an appetizer before our meals.»
3. s2-o3 «Is this coffee for takeaway?» → «That's one small latte to go, right?» (`takeaway` → `to go`).
4. s2-b-f4 «Is this seat free?» → «Is this seat taken?»
5. s3-o2 «How much is a kilo of apples?» → «How much is a pound of apples?» (US).
6. s3-a1 «…it's already gone off. Would it be possible to get a refund?» → «…it's already spoiled. Could I get a refund?»; ES «Siento molestarlo» → «Disculpe la molestia».
7. s5-b-v4 `trousers` → `pants`; s5-i-o1 «something smart but comfortable» → «something professional but comfortable».
8. s7-b-v9 `hand luggage` → `carry-on`; s7-a-v10 `at short notice` → `at the last minute`.
9. s8-b-v10 `Could I have some water?` (repetía el objetivo) → `headphones`; s8-b-v3 ES «manta» → «cobija».
10. s10-b-v5 `lift` → `elevator`; s10-o3-a3 «car park» → «parking lot»; s10-a-v10 `lodge a complaint` → `file a complaint`.

## Notas
- Tratamiento «usted» con personal de servicio (mesero, vendedor, agente), coherente con el resto del lote; el validador solo exige no usar peninsularismos.
- Sin pendientes para otro revisor.
