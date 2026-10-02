# Revisión independiente de los textos "en" — ruta francesa (f0 y a1-1)

Veredicto: **GO**

Alcance: 2.233 mapas TextoApoyo (964 en f0.json, 1.269 en a1-1.json), 1.877 pares únicos (es, en). Se leyeron todos. Solo se tocaron valores "en"; "es", texto francés, ids y estructura intactos (formato 2 espacios, ensure_ascii=False). `python3 tools/validar_ruta.py` → 10 idiomas, 0 errores.

## Resultado
La traducción base era de buena calidad: 20 textos únicos corregidos (20 ocurrencias, ~0,9 % de los pares únicos).

| Tipo | Corregidos |
|---|---|
| Respelling figurativo sustituido por descripción del sonido o ancla corta (mer-SEE, uh-PLAY, ay-kwah-toh-RYEN, van(t)) | 6 |
| Ancla ortográfica inglesa mal formada («lo» → «loh», 4 apariciones) | 4 |
| Referencia al español o ambigüedad de lengua (tilde española, «ou» = «nuestra u», «Spanish oo» confuso, «mesa» en pista) | 4 |
| Gramática/hecho incorrecto en inglés (nacionalidad sin artículo "unlike English", "one extra word", «any cat») | 3 |
| Inglés poco natural / terminología (r francesa, «Gender doesn't follow logic», título de adjetivo) | 3 |

## 10 ejemplos antes → después
1. «mersí» (nota): "It sounds like “mer-SEE”, with the r at the back of the throat." → "Stress falls on the last syllable, and the r is made at the back of the throat."
2. Pista merci: "It sounds close to “mer-SEE”." → "Its last syllable sounds like “see”."
3. «Suena eplé»: "“eh-play”" → "“uh-PLAY”" (schwa inicial correcta).
4. Nota feminino: "In the feminine the n is pronounced: “ay-kwah-toh-RYEN”." → "In the feminine the final n is pronounced."
5. Tilde: "In Spanish the accent mark shows the stressed syllable. In French it doesn't…" → "Don't read French accents as stress marks: the stress almost always falls on the last syllable. …"
6. «ou» vs «u»: "“ou” is our “oo”" → "“ou” is the English “oo”" (+ "The French “u” doesn't exist in English").
7. «tout»: "It sounds like “too” with the English “oo”; …" → "It sounds like “too”; the final t is silent."
8. Pista «table»: "“Table” is a feminine noun." → "Hint: “table” is a feminine noun in French."
9. Être + profesión: "Unlike English, profession and nationality go without an article…" → "After être, a profession goes without an article (unlike English “a doctor”), and so does a nationality: …" (en inglés la nacionalidad tampoco lleva artículo).
10. Negación: "English needs just one extra word (“do not” / “am not”)" → "English just adds “not” or “n't” (“I don't speak”)".
Otros: "l'eau “lo”" → "“loh”"; "nasal “van(t)”" → "nasal “van” (the g and t are silent)"; "Gender doesn't always follow logic" → "Gender can't be guessed from the meaning"; "The adjective agrees" → "The adjective agrees with the noun"; "It's like saying “I don't have any cat”" → "… “a single cat”".

## Criterio sobre pronunciación (PLAN_FRANCES §5)
Se conservaron anclas cortas útiles y las tablas "Sounds like (approx.)" (letras, números, conjugaciones de être/avoir, enlaces) porque son el único modo de mostrar enlaces y mudas; se eliminó el respelling suelto en notas y pistas. Terminología revisada y consistente: gender, article (definite/indefinite), agreement, conjugation, subject / stressed pronoun, liaison.

## Observaciones fuera de alcance (texto francés/es, no modificado)
- Varios ejercicios del texto francés/es usan «espagnol» y «Quito/Ecuador» (p. ej. "¿Cómo se dice «merci» en español?", "Je parle espagnol"). El "en" los traduce fielmente ("in Spanish"); un hablante de inglés sería más natural con «anglais», pero eso exige cambiar el francés. Recomendado para una revisión de localización del contenido base.
- Nota de proceso: durante la revisión se ejecutó por error un `git status` de solo lectura (sin efectos) pese a la instrucción de no usar git.
