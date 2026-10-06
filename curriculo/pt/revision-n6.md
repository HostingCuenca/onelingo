# Revisión del plan N6 (portugués de Brasil)

Veredicto: GO (con una observación de formato para decidir, ver «Pendiente de decisión»)

Validadores sobre `curriculo/pt/n6.json`: `validar_plan.py pt` → 0 errores (405 avisos en total, 93 de n6: vocabulario repetido, esperable en un nivel B2 de reciclaje); `validar_plan_detallado.py pt curriculo/pt/n6.json` → 0 errores · 50 clases · 654 ejercicios · 654 consignas únicas · 654 ejemplos únicos. Los 50 ids están en estado `planificado`; `previos` y los campos del esqueleto coinciden con `tools/curriculo/pt/n6-outline.json`. Búsqueda de europeísmos y de los topónimos prohibidos: sin resultados.

Revisión independiente de los diez lotes (C01–C50), que resultaron de buena calidad (no hay ejercicios plantilla ni distractores del tipo «ontem»; los ítems de relacionar traen siempre su fuente). Se aplicaron **19 correcciones puntuales** en los lotes de `tools/curriculo/pt/` (28 apariciones de un nombre en el caso de canon) y se consolidó el nivel. Copia de los lotes originales en el scratch del revisor.

## Cambios por tipo

### Canon y personajes (6 correcciones; 31 apariciones)

- C26–C30: «Rafael» era a la vez un cliente (Rafael Prado, dueño de pousadas en Porto de Galinhas, C16–C20) y un diseñador del equipo de Maré Digital (reuniones, actas, organograma). Un mismo nombre con dos oficios contradice la regla del MAPA: el diseñador pasa a **Davi** (nombre secundario ya usado en N2) en 28 apariciones. Antes: «Rafael — designer: responsável pela campanha» → después: «Davi — designer: responsável pela campanha».
- C02: Ana («família grande») → se inventaba un dato familiar que el MAPA deja «no establecido»: «mais penso na minha família grande» → «mais penso em como a vida em família mudou».
- C03: «o dos pais dele» (de Lucas) chocaba con que Dona Marina es viuda → «o dos avós dele».
- C35: seu Paulo «ajudo a levar as caixas até o carro» (Camila usa carros de aplicativo, no hay carro propio en el canon) → «até a entrada da feira».
- C50: la clienta de la prueba era «dona de três pousadas em Porto de Galinhas», casi el mismo caso del cliente de C16 → «três pousadas em Fernando de Noronha» (lugar permitido por el MAPA).
- C11: el informe hablaba de un «app de pedidos» del cliente Diego Salazar, cuando el contrato de Diego (C07, C13, C15) es un app de agendamento → «app de agendamento» y «não encontraram o botão de agendar» (antes «o carrinho»).

### Distractores débiles o absurdos (6)

- C05 g1: «Hoje em dia as famílias são menores. Os avós. O convívio é importante.» (frases sueltas) → un párrafo completo pero con la lógica invertida («menos importante é o convívio; por isso, sustento que os avós devem participar mais»), de modo que solo A es coherente.
- C22 s0: «podem baixar o preço do app» (absurdo) → «podem garantir que o leitor compre o app» (lectura exagerada del texto).
- C36 e3: «Portanto disso, o app funciona sem internet» (agramatical sin error real de hispanohablante) → «Além de isso» (de + eso, error real).
- C39 g1: «Em síntese, eu gosto muito de café.» → «Em síntese: agora vou começar com os dados dos usuários.» (abre en vez de cerrar).
- C40 i1: «Reparem em algo que não está na tela.» → «Reparem em esta barra laranja» (falta la contracción «nesta», error típico del español «en esta»); la consigna pasa a «bien formada».
- C50 e7: «…em três pontos: e pronto, é isso.» → «…em três pontos: pedido, prazo, orçamento e garantia.» (anuncia tres y lista cuatro).

### Lengua, gramática y registro pt-BR (1)

- C10 i2: «Ordem: Você vai sair por último? Desligue o ar-condicionado.» (pregunta + orden, confuso) → «Última pessoa a sair da sala: desligue o ar-condicionado.»

### Ambigüedad, estímulo insuficiente y consignas (5)

- C08 g2: la consigna decía «pregunta de Camila» pero el ítem es una afirmación de la atendente → «afirmación de la atendente sobre la cobertura de la batería».
- C08 e1 (2 campos): hablaba de «el celular» y de «segundo mês» cuando la situación es un notebook con la pantalla que se apaga → «O notebook apresentou um defeito de fabricação: a tela apaga sozinha».
- C26 g2: el orden «Só um minuto deixa eu concluir» admitía otras ordenaciones → la consigna añade «(empieza por «só»)».
- C40 e2: «curva proyectada» sin proyección en el texto → «curva del gráfico».

### Cronología y hechos (1)

- C32 i1: el «teto» de Diego era R$ 80 mil en el ítem y R$ 78 mil en la situación → R$ 78 mil en ambos.

### Lo que se revisó y se dejó (decisiones)

- Ênclise formal frente a próclisis: en C18 se marca «Lhe envio…» solo como inadecuada al inicio de un correo formal y con la nota explícita en la consigna; no se marca ninguna forma estándar como error fuera de ese contexto. La mesóclise es solo reconocimiento (C18 i1).
- Falsos amigos bien tratados y dejados: pauta, palco, legenda, estorno/estorbo, boleto, parcela, assinatura, esquisito, sob/sobre, cobre/cobra.
- Cifras comprobadas: 2.200 → 2.420 es un 10 %; 30 % de 84.000 = 25.200; 7.200 con 10 % = 6.480 y 12 × 600 = 7.200; 4.500/10 = 450 y 9.000/30 = 300; 15 días desde el 4 de junio = 19 de junio; viernes 12 de diciembre de 2031 cae en viernes; 62 + 18 + 20 = 100 %.
- Rafael Prado (C16–C20), Carolina (C29), Luana (C26) y Davi (C26–C30) son personajes secundarios de rol, sin choque con el reparto.
- La charla, el app de visitas guiadas (proyecto de N5 B9) y las fechas de la lluvia (abril–agosto) respetan el MAPA y los hechos de Recife.

## Pendiente de decisión (no corregido)

- **Longitud de las situaciones.** El ENCARGO (`docs/claude-educacion/ENCARGO_RUTA_PT.md`) fija 300–500 palabras de lectura para N5–N7; las situaciones de este nivel miden 54–119 palabras (de C31 en adelante, entre 54 y 89). El validador solo exige 24. Ampliar las 50 situaciones y sus preguntas es un trabajo de reescritura, no de corrección; se recomienda decidirlo al pasar a los bloques de la ruta (lectura de bloque) o al revisar N5 y N7 con el mismo criterio.
- Tarea integrada tipo Celpe-Bras: C46–C49 y C50 la cumplen (insumo + propósito + interlocutor + producto); en los demás bloques las tareas son de producción acotada.

## Hechos del reparto confirmados

- Camila Ortega: 32 años desde el 14 de marzo de 2031, gerente de producto en Maré Digital (Porto Digital), vive en Graças (alquila a seu Alberto); trata de «o senhor» a seu Alberto y a seu Paulo y de «a senhora» a Dona Marina e Iara.
- Dona Marina Lins (67, Boa Viagem), Lucas Lins (27, se gradúa en la UFPE y empieza a trabajar en software en B5, coherente con el MAPA), Ana Beltrão (34, vive en Lisboa desde N4), Bruno Cavalcanti (43, coordinador), Bia Santos (31, Café da Bia), seu Paulo Gomes (69, feriante), profesora Renata Souza (45, você).
- Personajes nuevos del nivel según el MAPA: Diego Salazar (cliente mexicano, você, habla español con Camila) y Yasmin Farias (desarrolladora nueva). Iara Menezes (directora, a senhora) viene de N4; seu Alberto Tavares, de N2.
- Recife: lluvias de abril a agosto; Porto Digital; Boa Viagem; Fernando de Noronha y Porto de Galinhas como lugares reales. Moneda: el real.

### Hechos nuevos a confirmar

- Camila sigue en 2031 en el apartamento de Graças que alquila a seu Alberto (contrato que vence en abril, C31) y vive sola (C01), ya sin Ana.
- Renata sigue siendo la profesora de Camila en 2031 y le pide el portafolio B2 (viernes 12 de diciembre de 2031).
- Rafael Prado (pousadas, B4), Carolina (equipo técnico de Diego), Davi y Luana (equipo de producto) como nombres secundarios.
- Cifras fijadas por el nivel: contrato de Diego de R$ 84 mil, 10 semanas, sinal del 30 %; soporte de R$ 4.500 al mes; app de visitas guiadas con 12 mil a 18 mil usuarios (enero–junio de 2031), México y Colombia como mercados principales.
