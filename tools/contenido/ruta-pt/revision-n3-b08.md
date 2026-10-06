GO

# Revisión pt N3 B8 (pt.n3.c36–c40)

Validador: `python3 tools/curriculo/validar_bloque.py pt 3 8` → 0 errores. Borrador del autor respaldado en el scratch (`rev-n3-b08/n3-b08.autor.json`). Total aproximado de correcciones: 75 (≈65 filas de tablas «Para ler» quitadas, 33 filas reescritas/añadidas y ~16 ediciones de contenido).

## Contraste con las fichas
- Las 5 clases enseñan su `introduce` y nada más: estilo indirecto con disse que + ia / estava / tinha (c36), perguntou se / onde / quando (c37), pediu para eu + infinitivo (c38), fórmulas de recado pode avisar que… / deixa recado / fala pra ele que… (c39), aclaraciones como assim? / quer dizer que…? / pode repetir o nome? (c40). Vocabulario de la ficha completo (8 por clase); ejercicios, claves y tareas siguen el plan; los `relacionar` de la ficha (e4 en c36, c38; e5 en c37, c39; e4 en c40) se conservan; sin menciones de Ecuador.
- ESCUCHA: 2 `escuchar` por clase (g4 y e3), con opciones en portugués y una sola respuesta.
- Guiadas con 4 ítems y `pista`; independientes con 3; evaluaciones con 5–6 ítems y ≥4 formatos.
- Lecturas (situación) de 155 / 148 / 149 / 149 / 149 palabras (el autor tenía 144 / 133 / 135 / 136 / 132; el validador exige ≥130, el rango B1 es 150–250): alargadas con frases naturales del diálogo, sin vocabulario nuevo.
- Campo `es` de todos los contextos en español, `en` en inglés: correcto en las 5 clases.

## Cambios por tipo
**Tablas «Para ler» (≈65 filas quitadas, rehechas)**
- Método (como en B7): se vació cada tabla «Para ler» y se corrió el validador; solo quedan las palabras no enseñadas en N1–N3 B7 ni en la propia clase, en forma base. Quedan: c36 2 filas (arquivo, seguinte), c37 4 (suporte, atualização, baixar, offline), c38 8 (contrato, assinatura, cor, texto, principal, rápido, pauta, ah), c39 3 (dele, momento, instalação), c40 9 (informar, segurança, bloqueado, conclusão, constar, pendência, faltar, chamado, deletreo «O, R, T, E, G, A»). Además cada clase conserva su tabla gramatical.
- Formas flexionadas quitadas del autor: mandou, deixou, vinha, anotei, instalava, baixava, funcionava, saía, podia/podiam, perguntei, respondi, insistiu, lembrou, sugeriu, prometi, respondo, esperarmos/mandarmos, revise, fechou, mandei, mudou, avisou/avisem, aviso, aguardo, oferece, transfere, liguei, ligando, paguei/paga, informe, consta, falta/faltava…
- Palabras ya enseñadas quitadas: dúvida, longa, mesmo, pressa, sobre, urgente, ligação, agência, sistema, feliz, saber, cheio, combinado, almoçar, corrigir, empresa, etc.
- Antes → después: «informe» → «informar»; «consta» → «constar»; «bloqueada» → «bloqueado»; «falta / faltava» → «faltar»; «baixava» → «baixar»; «rápida» → «rápido».
- La tabla «Más palabras y formas» de c38 (todo formas flexionadas) se eliminó y se renumeraron los ids de paso (p1–p11).
- Fila de deletreo «O, R, T, E, G, A» (decisión de la duda de la ficha): la fila está en la tabla de c40 y el deletreo ya se usa en i1 y en el diálogo.

**Duda «nós instalávamos» → «a gente instalava»**: aprobado. c37 usa «a gente instalava / trabalhava» en i1, ejemplos y errores frecuentes («nós» solo en infinitivo personal de c38 y c40, ya enseñado); el hispanohablante ve la forma coloquial con a gente, que es la de las lecciones previas.

**Falsos amigos (⚠)**: senha (c40: vocabulario y explicación p2) y combinar (c38: nota del vocabulario) marcados, como pedía la ficha. «Mensagem» (g/j) y «resposta» (sin «u») llevan nota de ortografía, no ⚠.

**Gramática, explicaciones y coherencia (6)**
- c36: Carolina «disse que o totem já estava pronto e que ia mandar o manual na segunda» contradecía el reparto (el tótem lo instala Maré Digital el lunes y lo construye el equipo de Camila; c37 dice que Carolina pregunta por el manual) → «disse que ia esperar o totem na segunda e que tinha uma dúvida sobre o manual».
- c37 p2: «En español «preguntó que…» se oye a veces» (impreciso) → «a veces se oye «preguntó que si…»».
- c38 e4 (relacionar): «Camila prometió una respuesta para mañana» no aparece en el mensaje; Camila prometió que Ana iba a verlo → «prometió que Ana iba a verlo al día siguiente».
- c39 g3 (ordenar): «O senhor quer deixar recado» sin saber quién llama → consigna fija que quien llama es un señor.
- c40 diálogo: Camila le pedía a Jonas que deletreara la calle (sin sentido para ella: Jonas es quien confirma su dirección) → Jonas confirma «Rua da Aurora, número 100», pide que Camila deletree su nombre, Camila deletrea «Camila Ortega: O, R, T, E, G, A», pide repetir el nombre de Jonas y confirma el protocolo 58213 con «Só para confirmar…» y «Quer dizer que ele vem amanhã?». e3 (escuchar) pasa a «qué le pide el atendente a Camila». Validador: «Ortega» solo exige acompañarse de «Camila».
- c40 e6: restaurado «visita do Moacir» de la ficha («Seu pedido virou chamado técnico, protocolo 7730, visita do Moacir.») y la respuesta modelo «Pode repetir o nome do técnico?»; Moacir está en `palabrasLibres`.

**Dirección «Rua da Aurora, número 100» (duda)**: decidido. Es una calle real de Recife (Boa Vista, junto al Capibaribe); el número se menciona solo una vez para confirmar el cadastro y no se identifica un edificio ni un lugar; es dato ficticio del apartamento de Camila y Ana. No se pone en la ficha de hechos como dirección real.

**Distractores y errores frecuentes**: revisados, todos errores reales de hispanohablante o calcos (preguntó que / se onde; para mim; eu chegar; ocupado; aqui sou; como así / nombre / decir). Una sola respuesta por ítem; sin cambios.

**ES neutro latino**: sin «coche», «móvil», «ordenador», «vale». «El internet» queda (uso latinoamericano). Traducción de «pendência» corregida («una pendiente» → «una pendencia»).

## Dudas del autor, decididas
1. Tablas «Para ler» deduplicadas contra N1–N2 y N3 B1–B7: hecho (ver arriba), todas ≤9 filas. Situaciones alargadas a ≥130 palabras (de hecho 148–155).
2. «nós instalávamos» → «a gente instalava»: aprobado, ambas válidas; el borrador usa «a gente».
3. Deletreo «O, R, T, E, G, A» como fila: hecho (tabla de c40).
4. Hechos de recados (Rafael Moura, Carolina, Ana), Jonas protocolo 58213 con técnico mañana, dirección Rua da Aurora 100: confirmados abajo.
5. ⚠ senha y combinar: presentes.

## Correcciones de ficha
- Ninguna sustancial. Observación: pt.n3.c37 usa «Ele perguntou ___ nós instalávamos…» en el ejemplo de la ficha; el borrador usa «a gente instalava» (decisión del revisor, la ficha no se toca). pt.n3.c40: el ejemplo de la ficha «Desculpe, pode ___ o seu nome?» se queda igual.

## Hechos del reparto confirmados
- c36 (recados): Camila vuelve a Maré Digital tras una reunión larga en la agencia de Carolina Dias; Ana (esperando) transmite tres recados: Bruno pasó a las dos, tenía prisa porque iba al aeropuerto, tenía una duda sobre el presupuesto del tótem y iba a devolver la llamada a las seis; un cliente nuevo llamó, quería cambiar el tema de la reunión de mañana (urgente) y pide el contacto directo de Camila; Carolina mandó un mensaje (iba a esperar el tótem el lunes, duda sobre el manual). Ana anotó el contacto del cliente nuevo. Camila devuelve la llamada.
- c37 (preguntas): Carolina llama a atención al cliente de Maré Digital: pregunta si el tótem ya está listo, cuándo lo instalan en la agencia (el lunes), dónde está el manual en español, si los guías pueden consultar el soporte el fin de semana (sí), cuánto sale el servicio (la propuesta aún se manda) y si trabajan el sábado (no); dice que mandará un mensaje el viernes. Un turista pregunta en el chat si el paseo sale a las 8 y dónde es el punto de encuentro.
- c38 (peticiones): Ana se queda en casa con fiebre; Bruno pidió a Camila presentar el tótem en la reunión del viernes y sugirió una reunión rápida a las diez; Carolina insistió en cambiar el color del botón principal y recordó que el contrato necesita la firma de Ana (Camila prometió que Ana lo vería mañana); Bruno mandará la pauta esta noche; el cliente pidió que lo llamen el jueves y Carolina el viernes; Ana pide a Carolina que mande el contrato hoy. Dona Marina pide a Camila que vaya a almorzar el domingo.
- c39 (fórmulas de recado): Camila llama a la empresa de seu Rafael Moura (o senhor, cliente); la recepcionista (sin nombre) transfiere al ramal, la línea está ocupada; Camila deja recado: avisar que llamó por la propuesta y pedir un retorno hasta mañana (tiene su número, el del correo de la propuesta); Rafael está en reunión y sale a las tres; la recepcionista avisará y anotará el celular de Camila. Mensaje de voz formal sobre la fecha de la instalación.
- c40 (aclaraciones): el internet del apartamento de Camila y Ana (Graças) cayó anoche; la central de atención atiende Jonas (a senhora): consta una pendencia (falta confirmar el endereço: Rua da Aurora, número 100; la cuenta está paga); Camila deletrea «Ortega»; protocolo 58213; el técnico pasa mañana y avisa por teléfono antes de llegar. «Chamado técnico, protocolo 7730, visita do Moacir» solo aparece como ejemplo del e6.
- Nombres: Camila, Ana, Bruno, Carolina Dias, Rafael Moura (o senhor), Jonas (central), Moacir (técnico, solo e6), Dona Marina. Anónimos: Recepcionista (c39), «cliente novo» (c36). Ningún nombre secundario nuevo.

## Sin resolver
- Ninguno.
