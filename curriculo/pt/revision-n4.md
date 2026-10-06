# Revisión del plan N4 (portugués de Brasil)

Veredicto: GO

Validadores sobre `curriculo/pt/n4.json`: `validar_plan.py pt` → 0 errores en N4 (113 avisos de vocabulario repetido, esperables en un nivel de reciclaje); `validar_plan_detallado.py pt curriculo/pt/n4.json` → 0 errores · 50 clases · 650 ejercicios · 650 consignas únicas · 650 ejemplos únicos. Los 50 ids están en estado `planificado` y los campos congelados coinciden con `tools/curriculo/pt/n4-outline.json`.

Revisión independiente de los 10 lotes (C01–C50). A diferencia de N2, los lotes de N4 llegaron en buen estado de lengua (no hay europeísmos graves, las consignas son bilingües y los distractores son casi siempre errores reales de hispanohablante). El problema serio fue de historia: desde B3 los lotes seguían con Ana en el apartamento de Graças, cuando B2 ya cuenta su partida a Lisboa. Se aplicaron **60 correcciones puntuales (cadenas de texto) en 21 clases** de `tools/curriculo/pt/n4-lote-*.json` (copia de los originales en la carpeta de scratch) y se consolidó el nivel.

## Cambios por tipo

### Canon, cronología y hechos (41)

- **Ana ya vive en Lisboa desde B3 (C11–C16, C19, C22, C23, C25; 33 cadenas).** B2 (C06–C10) cuenta su despedida y su embarque; C26, C28, C30, C31, C36, C38, C41, C45, C46 y C48 ya la tratan como «em Lisboa». Pero C11, C12, C14, C15, C16, C19, C22, C23 y C25 la dejaban compartiendo apartamento, leyendo borradores o repartiendo tareas en persona (y C15 pedía «nueva compañera»). Ahora la persona que comparte el piso es **Larissa** (colega, secundaria, sin apellido; no choca con ningún nombre ni apellido del reparto), que ya anuncia C09 («Talvez eu more sozinha um tempo»). Ana solo aparece por videollamada, mensaje o audio.
  - C11: «Camila e Ana ainda gostam do apartamento» → «Depois da partida da Ana, a colega Larissa vai dividir o apartamento com Camila. As duas ainda gostam…»; «Lista de Ana / Ana: Prefiro…» → Larissa.
  - C12: 6 ítems con «Camila e Ana se ajudam / se entendem / não se falam» → «Camila e Larissa».
  - C14: «Na sala, Camila leu o rascunho com seu Alberto» + «—Claro, nós três juntos» (¿qué tres?) → «Camila e a nova colega de apartamento, Larissa, leram…».
  - C15: «Camila e Ana resolveram organizar a casa… perguntou Ana… Ana escreveu a escala» → Larissa; i1 daba «segunda – Camila, lixo» pero la situación dice «terças e sextas» → «terça»; i0 hacía a Camila responsable de «luz e internet» cuando en la situación paga «internet e gás».
  - C16/C19/C22/C23/C25: «Ana leu o rascunho», «Camila conferiu a fatura com Ana», «Ana leu o texto», «comentou com Ana», «Ana leu a lista» → Larissa (en C16 también el mensaje informal «Ana, queria te pedir… me empresta o seu roteador?», imposible desde Lisboa).
- **C06: Porto de Galinhas.** «E eu que perdi a oportunidade de ir com você a Porto de Galinhas no ano passado» contradecía N2 (Camila y Ana ya fueron a Porto de Galinhas). → «a Caruaru no São João do ano passado» (consistente con C36, su primera visita a Caruaru). Afecta situación, consigna de s0 y ejemplo de e4 (3).
- **C11: amueblado.** El anuncio decía «Preferimos um imóvel que não seja mobiliado, porque já temos os nossos móveis», pero en N2 el apartamento era mobiliado y el aluguel incluía los muebles → «que seja mobiliado, porque ainda não temos móveis»; s0 y e2 ajustados (4 de las 13 cadenas anteriores). C11 i0 pedía «queremos um que tenha garagem» cuando el anuncio dice «Garagem não é necessária» → «cozinha pequena / cozinha grande».
- **Contrato (C14 y C46).** C14 firmaba «30 meses, a partir de 1º de março» y C46 decía «o contrato termina em 31 de março»: imposibles a la vez. → C14: «12 meses, a partir de 1º de janeiro»; C46: «31 de dezembro» (situación e i2). Así la renovación de B10 cae en el mismo año 2029.
- **C49:** «Prezado seu Alberto» (mezcla de tratamiento) → «Prezado Sr. Alberto».

### Distractores absurdos o agramaticales (9)

- C38 g1: «Só por precaução, esqueça o carregador» (sin sentido) → «Só por precaución, leve um carregador extra» (calco del español); consigna ajustada.
- C45 i2: «Desculpe, pode reformular o mangue?» → «Se entendi bem, o número é cinco?» (otra función, una sola respuesta).
- C46 i2: «…por isso o contrato não existe» → «…embora preciso responder logo» (embora + indicativo).
- C47 e0: «Em primeiro lugar, o reajuste pode ser negociado por fim» (ininteligible) → «Em primeiro lugar, o reajuste pode ser negociado» (organizador mal elegido).
- C48 g1: «Mudar é caro; portanto, é muito caro» (tautología) → «portanto, pode ser uma oportunidade» (conector equivocado); e0: «contudo, é caro» → «portanto, é muito tranquilo»; s0: «Que a mudança é grátis» → «Que o seu Alberto vai baixar o aluguel».
- C50 g1: «Chego a Recife em 2026 e continuei estudando amanhã» → «agora vou continuar estudei» (ir + finito, error real).
- C27 e0: «Talvez, quem sabe, de repente, o botão…» (frase rota) → «Esse botão confunde os usuários e ponto final» (versión directa, no suavizada).

### Lengua, gramática y registro pt-BR (4)

- C18 g1: el distractor «até ao dia 15» (portugués europeo, no previsto en N4) → «hasta o dia 15» (mezcla con el español); consigna «la otra se usa en Portugal» → «la otra mezcla el español».
- C10: «de repente a Ana encontra um namorado português» usaba «de repente» con valor «talvez», que un B1 leerá como «de pronto» (y el ítem g1 lo daba como «talvez» frente a «de forma súbita»). → «quem sabe a Ana encontra…» y g1 pregunta ahora por «palpite».
- C22 e0: la consigna decía «en español diríamos “cuida al gato”» (no es el contraste útil) → «“de” + artículo, la contracción que pide “cuidar”».

### Ambigüedad y estímulo insuficiente (6)

- C08 e2: la pista «o Lucas mandou um emoji de risada ↔ ele deve ter trazido o pacote» no deducía nada → «o Lucas sempre faz os favores da mãe».
- C14 i1: «Cláusulas marcadas: 6 (caução) e 9 (vistoria)» pero la situación solo tiene cláusulas 3, 4, 6 y 8 → «6 (caução) e 8 (rescisão)» y respuesta con multa por rescisión.
- C10 g1 (2): ver arriba; C38 g1 consigna.

## Límites aceptados

- El esqueleto de ejercicios es el mismo en las 50 clases (3 guiados + 3 independientes + 2 de situación + 5 de evaluación, un relacionar con pistas cruzadas por clase), formato que exige el validador. Cada clase mantiene datos, escena y distractores propios.
- Aún no hay tareas integradas tipo Celpe-Bras completas (insumo + propósito + interlocutor + producto); C49 y C50 las preparan para N5 con correo + texto de opinión + mensaje a Iara.
- Nombres de apoyo reutilizados en contextos distintos (Rafael, Luana, Carolina como vecinos en C12 y como compañeros del grupo de carrera en C31–C34): son secundarios sin canon, aceptados.
- `n4-outline.json` C06 trae en `vocabulario` «mala sorte» (el pt-BR dice «má sorte»). El campo está congelado y no se tocó; el lote mantiene la lista original y el ítem i2 de C06 enseña «Que má sorte!» frente a «Que mala sorte!». Conviene corregir el esqueleto a «má sorte» cuando se pueda.
- MAPA: «Ana se va a Lisboa (B6)» frente al esqueleto, que pone la despedida en B2 (C06–C10) y a Ana ya en Lisboa en B3+. Se tomó la lectura del esqueleto (B6 solo trae sus mensajes desde Lisboa); conviene aclararlo en MAPA.

## Hechos del reparto confirmados

- Camila cumple 30 años el 14 de marzo de 2029; líder de producto desde 2028 en Maré Digital (Porto Digital, Recife Antigo); vive en Graças; sigue con la profesora Renata. Moneda: R$.
- B1: llegada el sábado 5 de septiembre de 2026, primer día el martes 8, primer Carnaval en febrero de 2027 (Galo da Madrugada el día 6), mudanza a Graças con Ana, 2028 como líder (visita de sus padres, viaje a Fernando de Noronha). Dona Marina la esperó en el aeropuerto con una placa.
- B2: Ana viaja a una maestría en Lisboa (despedida en el Café da Bia con Bia y Lucas; bolo de rolo de Dona Marina; embarque a las 22h en el aeropuerto de Recife).
- B3: Larissa comparte el apartamento de Graças; seu Alberto Tavares (o senhor, vive en Casa Forte) sube el alquiler; contrato nuevo de 12 meses desde el 1 de enero, IPCA, caución de tres meses, vistoria, multa proporcional; infiltración y grifo, encanador el jueves 14h; tareas con Larissa.
- B4: reclamación a la empresa de internet (protocolo 48213907, factura de mayo R$ 68,60 corregida); banco: dirección, extracto y tarifa de R$ 19,90.
- B5–B6: Iara Menezes (fundadora y directora, «a senhora», «Prezada Iara») abre la vacante de gerente de producto; entrevista; CLT, 40 h, híbrido, plan de salud y vale-refeição; semana de pruebas defendida en la reunión de lanzamiento (septiembre). El resultado no se resuelve en N4.
- B7–B9: grupo de carrera junto al Capibaribe (domingos 6h), maracatu con Lucas (alfaia), viaje a Caruaru y al sertão, São João del barrio (23→30 de junio), mutirão en Boa Viagem, frevo Patrimonio Inmaterial desde 2012.
- B10: el contrato vence el 31 de diciembre; reajuste de 8 % frente a 5 % propuesto; correo por infiltración (2 de marzo, plazo de diez días).
- Trato: o senhor con seu Alberto y seu Pedro; a senhora con Iara, Dona Marina y la Dra. Helena; você con Ana, Bruno, Bia, Lucas, Larissa y Renata.

Hechos nuevos inventados por los autores o por esta revisión, a confirmar: Larissa (nombre y papel de compañera de piso), contrato de 12 meses desde el 1 de enero y reajuste de 8 %, cifras de la factura (R$ 99,90 / 33,30 / 2,00), protocolo 48213907, salario y beneficios del cargo (CLT, 40 h, plan de salud, vale-refeição), apodo «Cami», fiesta de São João del barrio con fechas del 23 y 30 de junio, normas de la pousada de Caruaru, y que Camila no pudo ir a Caruaru con Ana en el São João de 2028.
