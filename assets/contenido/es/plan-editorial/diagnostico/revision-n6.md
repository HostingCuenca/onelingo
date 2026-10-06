# Revisión independiente · diagnóstico español N6

GO

Revisor: claude-reviewer-dx-es · 2026-10-05 · validador `--idioma es` con `n6.json: OK · 18 ítems`. No se ejecutó `--compilar`.

## Correcciones (ítem: antes → después · gravedad)

| Ítem | Antes | Después | Gravedad |
|---|---|---|---|
| escucha.1 | El audio decía «como si fuera una niña» y la correcta repetía «niña»: se acertaba por eco léxico | Audio «como si no pudiera hacer nada sola»; correcta «La trata como si todavía fuera una niña»; feedback ajustado | media |
| escucha.3 | La correcta era la única más larga (11 vs 9 y 6 palabras); distractor «no tiene ninguna información» muy corto | Opciones de 11 / 10 / 11 palabras; la negativa pasa a «no tiene esa información y no puede ayudar» | media |
| escucha.4 | Sintaxis forzada «no siempre una cuenta grande garantiza»; correcta la única más larga | «una cuenta grande no siempre garantiza»; distractor alargado («casi nunca venden nada de nada») | baja |
| lectura.1 | Distractor «El arrendador debe pagar una penalización» (absurdo: el arrendador no paga) | «Paga la penalización por retraso» (verosímil, apoyado en la penalización por mora del texto); feedback aclara que es otro caso | media |
| lectura.2 | Distractor «No sabe qué opción es mejor» inverosímil; «los viajes salen bien» y «con el hotel y con los boletos» poco naturales; «concedes» en el feedback | Distractor «Dice que viajar solo es más barato y por eso lo recomienda»; texto «todo está organizado», «ni con los boletos»; feedback corregido | media |
| lectura.3 | Valentina enviaba el listado al proveedor, pero el proveedor es el campo de Kenji (MAPA: Kenji = proveedores; Valentina = comunidades); la correcta describía lo que Valentina hace («decirle con tacto…»), no lo que pide | Destinataria: la asociación comunitaria. Consigna «what she asks Kenji to do»; correcta «Que le envíe el listado el viernes antes de las cinco» frente a «después de la hora de cierre» y «que pida una ampliación» | alta |
| lectura.4 | La correcta copiaba la frase del texto («verificar el resultado antes de la publicación»: lectura literal); el feedback citaba «representatividad», que el texto no menciona; «Por eso» repetido | Texto rehecho (63 → ≥65 palabras): la duda sobre la fiabilidad es la causa; correcta «No estaba segura de que el resultado fuera fiable» (inferencia); feedback fiel al texto | alta |
| gramatica.1 | Distractor «incluir» débil; feedback no coincidía con las opciones | Se mantiene «incluir»; la clave pasa a la primera posición; feedback «indicative and the infinitive» | baja |
| gramatica.3 | Distractores poco naturales («Aunque sabemos», «Como sabemos») | «Si ya sabíamos», «Como sabíamos», «Si sabemos»: errores verosímiles para quien confunde la condición real con la irreal; «De haber sabido» sigue siendo la única válida con «habríamos pedido» | media |
| gramatica.4 | Clave en la misma posición que otros ítems | Orden vienen / vengan / vendrán / vinieron | baja |
| vocabulario.2 | Distractor «imprimir» sin relación | «encargar», «reservar», «rebajar» (verbos de c33 y c28 verosímiles en una tienda) | baja |
| vocabulario.4 | Distractores absurdos (infracción, exigencia, rebajita) | «garantía», «cotización», «contraoferta» (vocabulario del taller); la causa «se va hacia un lado» deja una sola respuesta | media |
| escritura.1 | Tercer grupo: lista cerrada de 15 verbos («que abriera», «que apagara»…) | Ampliado a ~1.500 formas: ~110 verbos habituales en imperfecto de subjuntivo (-ara/-iera, -áramos/-aran, irregulares como hiciera, tuviera, pudiera, dijera, trajera) también con «yo, me, nos, lo, la, le, se» tras «que». Modelo y aceptadas siguen pasando | alta |
| escritura.2 | Modelo «Es verdad que ayuda, aun así…» sin sujeto; tema solo «celular» | Modelo «Es verdad que el celular ayuda…»; grupo de tema ampliado (teléfono, teléfono celular, mi/su/tu/un teléfono, celulares) | baja |

Sin cambios: escucha.2 (Kenji «quedó en confirmar con el proveedor», Valentina el listado; consistente con el reparto), gramatica.2, vocabulario.1 y vocabulario.3.

## Comprobaciones

- Una sola respuesta defendible por ítem; claves verificadas contra texto y audio. Escucha: ninguna se resuelve sin oír (paráfrasis de «como si no pudiera», «quedó en», «no sabría decirle con exactitud», «no implica necesariamente»).
- Puntos de N6 evaluados: como si (c01), a menos que (c06), futuro normativo y preaviso (c08), si + pluscuamperfecto (c12), de + infinitivo (c15), «yo diría que» (c16), «¿te importaría que…?» (c18), a más tardar (c27), se acordó / quedó en (c28), luna de miel (c05), rebajar y alineación (c33–c34), reanudar (c37), no sabría decir (c39), es probable que (c42), negación parcial (c43), sondeo y fiabilidad (c43, c45), aun así y estructura del ensayo (c46, c47).
- Reparto: Kenji y Valentina existen en MAPA.md como equipo nuevo de Andes Vivos en N6 (Kenji: datos, presupuesto, proveedores, transporte; Valentina: rutas, comunidades, redes); se tutean con Emma y entre sí. Tras la corrección de lectura.3 ninguna escena contradice esos roles. El empleado de escucha.3 usa «usted» con el viajero.
- Apoyo solo en inglés americano; consignas en ≤ 110 caracteres (máx. 94) y únicas; los feedback explican la regla sin citar posiciones.
- Rúbricas probadas con la normalización de la app: pasan modelo, aceptadas y variantes («yo cerrara», «me sentara», «hiciera», «lo bajáramos», «es cierto que… aun así», «mi teléfono»); fallan indicativo en la petición («que abro»), falta de la petición e inglés.
- Posición de la respuesta (A / B / C / D): 4 / 6 / 4 / 2 en los 16 ítems de opciones. La correcta es la única más larga en 1 ítem por palabras (vocabulario.1, inherente: «luna de miel» frente a palabras sueltas); el validador lo da por bueno.
- Longitudes: textos de lectura dentro de 65–95 palabras y audios dentro de 25–45.

## Sin resolver

- vocabulario.1: «luna de miel» es la única opción de tres palabras; se acepta porque no hay sinónimo de una palabra.
- La rúbrica no ve orden ni sentido: «Yo diría que es largo. ¿Te importaría que yo cerrara?» pasa. El formato (frases por grupo) no permite exigirlo.
- El tercer grupo de escritura.1 admite combinaciones raras (p. ej. «que nos firmáramos»); solo comprueba que haya imperfecto de subjuntivo tras «que».
- El archivo crece a ~45 KB por la lista de formas; si pesara en la compilación, se podría recortar a los 60 verbos más frecuentes.
