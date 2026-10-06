# Revisión independiente · diagnóstico español N1

GO

Revisor: claude-reviewer-dx-es · 2026-10-05 · validador `--idioma es`: «n1.json: OK · 18 ítems».

## Correcciones (antes → después)

| Ítem | Antes → después | Gravedad |
|---|---|---|
| escucha.1 | Distractor «Veinte años» (la correcta era la más larga por 3 letras) → «Diecinueve años»: ahora el ítem exige distinguir dieciocho/diecinueve por el oído; feedback lo explica (c13) | media |
| escucha.4 | Opciones con actividad y acompañante distintos (la correcta era la más larga y la única con «hermana», pista del audio) → las tres terminan en «con su hermana», solo cambia la actividad (cine / descansar / museo); feedback ajustado (c43) | media |
| lectura.3 | Distractor «De Emma» (descartable: el mensaje va dirigido a Emma) → «De una amiga de Daniela»; feedback ajustado (c44) | baja |
| lectura.4 | «Comí una empanada y tomé fotos», opciones helado/pastel/empanada: se resolvía emparejando la única palabra del texto → texto con «comí una empanada y bebí un jugo de naranja»; opciones empanada / jugo de naranja / helado de fresa. Ahora hay que distinguir «comí» de «bebí» (c47); la correcta deja de ser la opción más corta de la misma longitud que las demás | alta |
| vocabulario.4 | Sin cambio de texto; consigna precisada («comes right after October and November») para que la respuesta sea única (se probó «Después de…» y el validador rechaza «después», no enseñada) | baja |
| escritura.1 | Aceptada «Me despierto a las ocho…» y evidencia «me despierto» (despertarse ≠ levantarse, consigna «get up») → «Me levanto a las ocho…»; se quita la evidencia «temprano todos los días» (no da hora); se añaden horas (cuatro, once, 4, 11) y desayunos (huevos, fruta, té, leche, agua) para no fallar respuestas correctas; feedback «eat or drink» | media |
| escritura.2 | Evidencias que no responden «what you ate or drank» («tomé fotos», «recibí un/una», «comí con») eliminadas; añadidas «bebí una», «comí helado», «comí un sándwich»; aceptada con «El sábado pasado» (la consigna dice sábado pasado) | media |

Total: 7 ítems tocados (1 alta, 4 medias, 2 bajas).

## Comprobaciones

- Una sola respuesta defendible por ítem; claves verificadas contra audio/texto. gramatica.4: «sigues» no cabe porque la frase sigue con «gira» (imperativo).
- Escucha: ninguna se resuelve leyendo consigna ni opciones (edades 18/19, cincuenta centavos vs cinco dólares vs un dólar del pan, 7:45/8:15/8:45, actividad del sábado). Distractores numéricos de escucha.1 y escucha.3 son sonoramente cercanos.
- Frente a N0 (nivel-0.json solo enseña números 0–10, «yo tengo», «me gustan los gatos» como ejemplo): ningún ítem se resuelve solo con N0; tener/dormir/gustar/seguir exigen conjugaciones de c13, c29, c30, c42.
- Reparto: inicio (c08, c11, c13), mitad (c22, c25, c26, c29, c30, c33, c38, c45), final (c42, c43, c44, c46–c47).
- Español latino neutro, tildes, ¿? y concordancias correctos; Daniela tutea a Emma («¿Te gustaría venir?»); jugo, libra, cumpleaños, celular sin peninsularismos. Apoyo solo `en`, inglés americano; consigna.en ≤ 110 y única; el feedback explica y no cita posiciones.
- Rúbricas de escritura probadas con la normalización de la app: modelo y aceptadas pasan.
- Posiciones de la respuesta: 5 / 5 / 6 en A / B / C; la correcta es la única más larga en 1 de 16 ítems.

## Sin resolver

- lectura.1: «Mi madre es profesora» — en el reparto Rosa es profesora jubilada; se deja porque «jubilada» no está enseñada y el dato es compatible (fue profesora).
- vocabulario.3: «una ___ de tomates» deja fuera «litro» (masculino) por género además de por sentido; no afecta la unicidad de la respuesta.
