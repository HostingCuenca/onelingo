# Revisión independiente · diagnóstico español N10 (C1)

GO

Revisor: claude-reviewer-dx-es · 2026-10-05 · validador `--idioma es`: «n10.json: OK · 18 ítems» (0 errores). No se ejecutó `--compilar`.

## Correcciones (antes → después)

| Ítem | Antes → después | Gravedad |
|---|---|---|
| escucha.1 | El audio decía «Y no dijo nada más… no quiso hablar», y la correcta repetía «no quiso hablar» (se acertaba por eco). Ahora el audio solo muestra la frase suspendida, que mira el reloj y se va; correcta «Que hay una historia larga y no quiere hablar». Distractora «va a contar todo con muchos detalles ahora» (absurda) → «no tiene nada que decir sobre el pendiente» | alta |
| escucha.2 | El audio decía «Nadie lo esperaba» y la correcta era «Nadie esperaba la noticia» (eco literal). Audio: «Nos quedamos todos mudos»; correcta «A todos los tomó por sorpresa»; distractora «Todos esperaban la noticia desde hace meses» | alta |
| escucha.3 | Distractora «Hubo solo un pequeño retraso, nada más» (relleno) → «Solo falló un poco la hora de llegada»; «amable, pero caro» → «amable, pero cobró caro» | baja |
| escucha.4 | Dos distractoras que decían lo mismo (quedarse en casa) → «Esperar en la autopista hasta que abran el paso» y «Cancelar el viaje y quedarse en casa» | baja |
| lectura.1 | Distractora «El comité no leyó la propuesta con atención» (la contradice «con mucho interés») → «La gerente rechaza la propuesta y no piensa firmar nada» (sobrelectura de la crítica); feedback aclara que pide una versión más detallada | media |
| lectura.2 | Distractora «no tienen ningún valor para nadie» (relleno, trivial) → «no tienen ningún valor real» con más peso; el feedback citaba «no conviene generalizar» pero el texto decía «no es bueno generalizar»: citas alineadas. Correcta alargada para que no sea la más larga | media |
| lectura.3 | Distractoras «ella deja a su familia y se va para siempre» (inventada) y «error del montaje» (absurda) → «Es un símbolo claro del abandono de su vida anterior» (primera lectura tomada como única) y «Es una falla de la directora, que no explica qué espera la protagonista»; feedback ampliado | media |
| lectura.4 | Correcta parcial («Cambiar la copia simple por un documento sellado o certificado», más larga) → «Llevar el original sellado o una copia certificada»; distractoras «Pagar la cuenta de luz y olvidarse del contrato» → «Pagar la cuenta de luz, que es lo único que falta» (plausible y falsa), «Esperar una semana…» con relleno → «…sin llevar ningún documento nuevo» | media |
| gramatica.1 | Feedback citaba «aprobara», que no está en la frase → «diera». Distractoras «supone / supones» (supones, trivial por la persona) → «supone / supondrían» (modo e incongruencia de número con «eso») | media |
| gramatica.2 | «Detrás de / Lejos de» (triviales, de lugar) → «A pesar de / Lejos de»; el alumno debe saber que «de cara a» mira a un hecho futuro. (Se descartó «a raíz de» por no estar enseñada) | media |
| gramatica.3 | «mientras / pues» (triviales) → «a menos que / siempre que», que sí podrían leerse con subjuntivo pero invierten el sentido (cedería); «aunque» se excluyó a propósito (segunda correcta) | media |
| gramatica.4 | «soy / seré» (indicativos triviales) → «haya sido / sería», formas que exigen saber que «ni que» pide imperfecto de subjuntivo; texto «¡Ni que yo ___ millonario!» | media |
| vocabulario.1 | «conmovedor / deslumbrante» (no encajan con un guion que se adivina, descartables) → «prescindible / desigual» (léxico de c31, forma parecida a «previsible») | baja |
| vocabulario.3 | «consulado / delito» (absurdas con «médico») → «tratamiento / seguro» (colocaciones médicas que no se «extienden») | baja |
| escritura.1 | Rúbrica estrecha (3.er grupo: «el plan», «el precio», «es caro», «es alto»…); fallaban «este plan», «cuesta mucho», «es una buena inversión», «es muy caro». Ahora 27 variantes de 2+ palabras (el validador no admite evidencias de una palabra); +1 respuesta aceptada | media |
| escritura.2 | Rúbrica estrecha; fallaban «me expresé mal», «no fui clara», «la calle», «se la repito», «voy a repetirle». Ahora 7 variantes de reparación, 8 de dirección/calle y 19 de acción | media |
| Metadatos | `review` pasa de PENDING a GO | — |

Total: 17 filas (2 altas, 11 medias, 4 bajas).

## Comprobaciones

- Una sola respuesta defendible; claves verificadas contra texto y audio; distractoras plausibles pero falsas para quien domina N10. Escucha: las correctas son reformulaciones sin eco del audio (se necesita oír).
- Punto de N10 por ítem: Es que… si yo te contara (c05), y va y dice / de buenas a primeras (c06), es más / encima / para colmo (c19), no queda otra (c40), no es tanto que… sino que (c16), hallazgos / cautela / generalizar (c23, c25), podría leerse (c33), trámites (c39), supondría (c27), de cara a (c29), así concesivo (c17), ni que (c20), previsible (c31), vergüenza vs. embarazo (c42), certificado médico (c43), escabullirse (c10). Escritura: c18 y c38.
- Rúbricas probadas con la normalización de la app: modelo, aceptadas y 4 respuestas plausibles por ejercicio pasan; 9 inválidas (de acuerdo en vez de disentir, sin la fórmula, media tarea, fuera de tema, en inglés) fallan.
- Longitudes: lectura 109–121 palabras (105–150), escucha 48–58 (45–80). Consignas en ≤ 110, únicas, apoyo solo `en`; feedback explicativo y sin citar posiciones.
- Posiciones de la correcta (16 ítems con opciones): A / B / C = 5 / 5 / 6. La correcta es la única más larga solo en 1 ítem (vocabulario.4, una palabra).
- Español latino neutro; Emma tutea a Mateo y amigos y la gerente la trata de usted; el trámite usa usted; sin peninsularismos.
- Léxico: el validador exige que estímulo, opciones y modelo estén enseñados hasta N10; se descartaron «supondrá», «supusiera», «a raíz de» y similares por no estarlo.

## Sin resolver

- gramatica.1: «supondrían» (plural) es una distractora de concordancia más que de modo; el léxico enseñado no deja más formas de «suponer».
- gramatica.3: la consigna en inglés revela que se pide «even if»; sin ella, «a menos que» sería más tentador. Se acepta porque «aunque» no puede ser distractora.
- vocabulario.4: «escabulló» sigue siendo la más larga (palabra única); las alternativas enseñadas no son más largas sin arriesgar ambigüedad.
