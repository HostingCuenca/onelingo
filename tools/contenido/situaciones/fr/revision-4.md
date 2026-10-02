# Revisión lote 4 (situaciones 31–40, francés)

**Veredicto: GO** (tras correcciones directas en `lote-4.json`; `validar_situaciones.py` → 10 situaciones, 0 errores).

## Resumen
- Objetivos, ids, estructura (3/10/4 por tramo) y progresión de nivel correctos; los objetivos no se repiten entre tramos.
- Tipografía: U+202F antes de ? ! : ; y apóstrofo ’ verificados en todos los campos franceses (0 incidencias).
- Tutoiement/vouvoiement coherente con el contexto (amigos tú, servicios y profesores vous).
- Cambios: 19 entradas corregidas (francés 9, vocabulario/ejemplos 6, traducciones 5; algunas cuentan en más de un tipo). Sin cambios de ids ni de intención.

## Cambios por tipo
- **Francés:** calcos o ejemplos poco naturales (borne, match nul, se replier, vaut le coup, avec tout mon respect, première course de dix kilomètres, ejemplo de «avoir du mal avec» y «être à la hauteur»).
- **Vocabulario:** error del validador en s34-a-v5 (más de 5 palabras); s40-a-v6 no coincidía con «loose ends»; s37-i-v2 calco («entraîneur personnel») sustituido por «suivi personnalisé»; s38-a-v1 pasa a «navré» con ejemplo correcto.
- **Traducciones:** EN de s31-a-v6, s32-a-v5, s36-b-v10, s38-b-v6/o2, s39-a-v7, s40-a3; ES de s35-i-v1 y s40-b-f3.
- **Nivel / cultura:** «distributeur de billets» (cajero automático en Francia) sustituido por «borne automatique» en contexto SNCF.

## Ejemplos antes → después
1. s32-i-v3: «le distributeur de billets» → «la borne automatique» (en Francia el primero es el cajero).
2. s34-a-v5: «ne pas être à la hauteur» (6 palabras, error del validador; además duplicaba s40-a-v8) → «bâcler un travail», EN «to rush a job».
3. s36-i-v5: «l’égalité» → «le match nul», ejemplo «On a fait match nul, un partout.»
4. s36-a1: «reculer trop bas» → «se replier trop bas».
5. s37-i-f3: «mes premiers dix kilomètres» → «ma première course de dix kilomètres».
6. s40-a-v6: «des pistes inexploitées» (≠ loose ends) → «des questions sans réponse».
7. s40-a3: «vaut l’effort» → «vaut le coup»; EN «worth the effort» → «worth it».
8. s35-a-v6: «sauf votre respect» (arcaico/irónico) → «avec tout mon respect».
9. s31-a-v6 EN: «bear with us» → «thank you for your patience».
10. s38-a-v1: «être navré» con ejemplo «Je vais être navré…» (ilógico) → «navré», «Je suis navré de vous déranger encore.»
