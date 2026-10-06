# Revisión independiente · diagnóstico español N7

GO

Revisor: claude-reviewer-dx-es · 2026-10-05 · validador `--idioma es` sin errores (18 ítems, léxico contra la ruta publicada hasta N7). No se ejecutó `--compilar`.

## Correcciones (antes → después)

| Ítem | Antes | Después | Gravedad |
|---|---|---|---|
| escucha.1 | El feedback decía que el restaurante iba al final, pero en el audio iba segundo; la respuesta salía solo del orden de mención («dejó… y salió…») sin necesitar «nada más llegar». | Audio nuevo: la cena se menciona primero («comió… una vez que tomó una ducha»), y «nada más llegar al hotel llamó a Daniela, y seguidamente subió». Hay que entender «nada más llegar» y «seguidamente». Feedback corregido. | alta |
| escucha.2 | «De aquí a un mes» ↔ «Dentro de un mes»: se resolvía por repetición de «un mes». | La fecha de salida es «dentro de un mes» (señuelo); la hoja de ruta, «de aquí a una quincena»; correcta «En unos quince días». | media |
| escucha.3 | «Jorge dice que debe de haber sido el semáforo»: «Jorge dice» daba la respuesta sin la construcción. | Daniela propone «igual hay un accidente» y Jorge discrepa: «Según él, debe de haber sido el semáforo». Opciones: accidente (Daniela) / carro averiado / semáforo apagado. | media |
| escucha.4 | Feedback con «known fact being discussed, not asserted», confuso. | Feedback reescrito; la opción incorrecta lleva ahora «porque perdieron la final» (la correcta ya no es la más larga). | baja |
| lectura.1 | La correcta repetía «vestigio» del texto («Nadie ha visto ningún vestigio»): se resolvía por coincidencia de palabras. «Gentío en la bocacalle» poco natural. | Correcta «Es solo una leyenda sin pruebas»; distractores «Los historiadores ya lo confirmaron» / «Los visitantes pueden entrar los domingos». «En el atrio». | media |
| lectura.2 | Inés escribía «Quedo a su disposición» a Emma: contradice el reparto (Inés tutea a Emma). La pregunta «qué le preocupa» admitía también el cargo por anulación. Los distractores se descartaban por «la tarifa es buena». | Emma escribe a Inés («Estimada Inés… Cordialmente, Emma García»). Consigna «qué propone hacer antes de firmar»; correcta «Fijar las fechas de los pagos» (paráfrasis de «concretar el cronograma de pagos»); distractores del texto (adelanto, tarifa). | alta |
| lectura.3 | «La cena se canceló» era descartable de plano; «tuvo desconcierto» poco natural. | Correcta «Llegar puntual sería raro» (paráfrasis de «llegar a la hora exacta… desajuste»); distractor «Emma se equivocó de día»; «se sorprendió al principio». | baja |
| lectura.4 | El feedback nombraba a «Tomás», personaje inexistente en la escena. | «Mateo». | alta |
| gramatica.1 | «recorriendo» (llevar + gerundio, de N6) era defendible. | Opciones «recorridos» (error de concordancia) / «recorridas» / «recorrer»; feedback sobre la concordancia con «etapas». | media |
| gramatica.3 | «nos haga una tarifa» poco natural. | «nos dé una tarifa» (dé / da / dio / daría; todas con léxico enseñado). | baja |
| vocabulario.1 | «depender de tres empleados» y «hablar de tres empleados» eran defendibles con «por el recorte». | «la empresa ya no podía pagar tantos sueldos y tuvo que ___ de tres empleados»; opciones hablar / burlarse / prescindir (solo la última encaja). | alta |
| vocabulario.2 | Feedback falso: «las otras no forman expresión fija con la pata» («dar la pata», «estirar la pata» existen). | «The other verbs do not give that meaning with “la pata”». | media |
| vocabulario.3 | «una ___» con «rayo» y «hielo» (masculinos) los descartaba por concordancia, sin conocer la comparación. | El artículo entra en las opciones: una mula / una tortuga / un rayo / el hielo. | alta |
| escritura.1 | Rúbrica con formas agramaticales («puede que hay», «puede que hubo»), listas duplicadas y sin cubrir órdenes como «estaríamos ahora en casa» o «de haber salido». | Rúbrica regenerada: «igual» + verbo, «puede que» + subjuntivo, es probable / posible que; «si hubiéramos / hubiésemos / hubiera / hubiese / hubieras / hubieran» + 40 participios y «de haber» + participio; apódosis en -ría + palabra siguiente o previa. | alta |
| escritura.2 | Aceptada agramatical («la reserva fue una anulación»); el modelo («hubo una anulación del vuelo», «la agencia») poco natural; faltaban «lamento tener que informarle», «nos disculpe». | Modelo con «la salida tuvo un aplazamiento de dos días… por el trastorno… Andes Vivos»; aceptada «su reserva fue anulada por un trastorno técnico»; rúbrica ampliada. | media |

Total: 15 ítems tocados; 6 altas, 5 medias, 4 bajas. Sin cambio: gramatica.2 y 4, vocabulario.4.

## Comprobaciones

- Una sola respuesta defendible por ítem; claves verificadas contra texto y audio. Escucha: ninguna se resuelve sin oír (orden inverso a la mención, quincena, atribución de la hipótesis, conclusión del hablante).
- Puntos N7 por ítem: nada más llegar + seguidamente (c07), de aquí a (c08), igual + deber de haber (c12-c13), el que + subjuntivo (c28), según cuenta la leyenda + a principios/mediados/finales (c16, c19), en cuanto a + concretar (c35), por lo general + usanza (c37), estilo indirecto libre (c42), llevar + participio (c10), condicional mixta (c11), a condición de que (c31), me chocó que (c38), prescindir de (c03), meter la pata (c22), más terco que una mula (c25), -azo (c24), lamentamos informarle (c02).
- Español latino neutro (carro, trancón, cancha); sin vosotros ni peninsularismos. Trato: Emma de usted a Inés y a los Andrade en trámites; narración y escenas con Mateo/Daniela en tuteo; sin errores de tildes ni de signos.
- Apoyo solo `en`, inglés estadounidense; consigna.en ≤ 110 y única; feedback sin citar posiciones.
- Rúbricas probadas con `_normalizar_app` y 22 respuestas: pasan (modelo, aceptadas, variantes con «puede que haya», «de haber salido», «si hubiésemos», «lamento tener que informarle», «nos disculpe»). Fallan: sin condicional mixto, indicativo tras «si», sin fórmula de lamento, tuteo («informarte»), inglés, sin disculpas.
- Posiciones de la respuesta: 5 en A, 5 en B, 4 en C, 2 en D (los ítems de 3 opciones no usan D). La correcta no es la única más larga en ningún ítem.
- Longitudes: textos 75–81 palabras (rango 75–110), audios 35–39 (30–55).

## Sin resolver

- escucha.4: «no significa que sean un mal equipo» se entiende por la negación sin dominar «el que + subjuntivo»; es una prueba de comprensión y el ítem de gramática 4 cubre el subjuntivo.
- lectura.1 y lectura.3 tienen distractores contradichos con claridad por el texto; un alumno de N6 puede acertar por descarte, aunque la correcta exige leer «leyenda sin pruebas» / «hora exacta».
- gramatica.3: «da» frente a «dé» difieren solo en la forma verbal; es lo que se mide, pero un error de tilde del alumno no existe (se elige entre opciones).
- Las rúbricas no ven orden ni sentido: «Igual hay x. Si hubiéramos salido y. Estaríamos z» sin coherencia pasa. El formato (frases por grupo) no permite exigirlo.
- El léxico del validador es de forma exacta: «ofrezca», «recorrerlo», «cenó» no están enseñadas; se evitaron en los ítems.
