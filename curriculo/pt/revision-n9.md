# Revisión del plan N9 (portugués de Brasil)

Veredicto: GO

Validadores sobre `curriculo/pt/n9.json`: `validar_plan.py pt` → 0 errores (avisos de vocabulario repetido, esperables en C1 y en los repasos); `validar_plan_detallado.py pt curriculo/pt/n9.json` → 0 errores · 50 clases · 650 ejercicios · 650 consignas únicas · 650 ejemplos únicos. Los 50 ids están en estado `planificado`.

Revisión independiente de los 10 lotes (C01–C50, escritos en parte por script). Se aplicaron unas **150 correcciones puntuales** (≈124 sustituciones en ejercicios y situaciones, 5 normalizaciones de «correio/correo» → «e-mail» y 8 claves de integración nuevas) en los lotes de `tools/curriculo/pt/` y se consolidó el nivel. Los lotes originales están copiados en el scratchpad del revisor.

## Cambios por tipo

### Canon y personajes (≈40)

- **Contacto de feria «Paulo» (C02)**: seu Paulo Gomes es el feirante canónico; el compañero de mesa pasa a **Davi** (consigna, situación, ítems g2 y s1, estímulo de i2). Además el contacto «Rafael» de la feria (C01, C03, C04, C05; 14 apariciones) pasa a **Henrique** para que no choque con el proveedor ni con «Rafael Duarte» de N7.
- **Proveedor «Rafael Duarte» (C41–C45)**: en N7 C01 «Rafael Duarte» es un cliente de una tienda de apps. Se mantiene una sola identidad por nombre: en N9 el proveedor de Nordeste Componentes pasa a **Otávio Ramos** (situaciones de C41, C43, C44, C45 y todos los ítems con «Rafael:»; ≈25 apariciones).
- **Lucas Lins** hacía de «Lucas, do suporte» y de responsable de un acta (C17, C19) y de revisor de gráficos (C26): Lucas es amigo, estudiante y futuro cofundador de Travessia, no empleado de Maré. Pasan a **Murilo** (personaje de rol de soporte) y a **Yasmin** (colega canónica). En C27 el borrador de informe lo escribía «Rafael»; ahora lo escribe Yasmin.
- **Bruno como «Responsável de segurança»** (C32, C35): contradice su oficio (coordinador de producto) y la construcción no es idiomática → «Responsável pelo aviso / pelo plano: Camila Ortega».
- **C24 y C25**: Camila ya es directora de producto desde antes de C01, pero se postulaba y negociaba «a una vaga de diretora de produto». Se reencuadra como **nuevo cargo de diretora regional de produto** (ascenso interno) en C22, C24 y C25; se quita «A senhora Iara apresenta» (narración con «senhora»).
- **C37**: la conversación ocurría «na Escola Capibaribe, depois da aula», pero en 2034 Camila ya no estudia allí → encuentro con Tomás, «amigo do curso de preparação do Celpe-Bras» (canon N8).
- **C22**: «público hispanohablante» (palabra española dentro de la situación portuguesa) → «hispanofalante».

### Hechos, fechas y cronología (≈14)

- Fechas en fin de semana en 2034 (se comprobó el día real de la semana): C14 «6 de maio» (sábado) → «8 de maio» (segunda), «1º de abril» → «3 de abril»; C15 «3 de junho» → «5 de junho», «20 de maio» → «22 de maio»; C19 «14/05» (domingo) → «16/05» y «20/05» (sábado) → «19/05»; C41 entrega prevista «10 de junho» (sábado) → «9 de junho».
- C14 g1 decía «as entregas serão às quartas-feiras» cuando la situación mueve las entregas a las quintas → «quintas-feiras».
- C18 i2: las posturas estaban invertidas respecto a la situación (Ana prioriza los pagos y Bruno el rediseño) → corregido.
- C49 i1: «o projeto começa em agosto» contradecía el resumen («início em setembro») → «começa em setembro… a partir de outubro».
- C07 i0: «publicamos a versão para os usuários» a las 22 h contradice una noche anterior al lanzamiento → «versão de teste».
- C27 e0: se citaba al Inep con una muestra inventada → «um levantamento do setor (2031)» (el Inep solo aparece como emisor del Celpe-Bras, hecho del MAPA).
- C36–C40: texto normativo, Polícia Federal y Celpe-Bras emitido por el Inep coherentes con el MAPA; C38 g0 decía «O primeiro passo é protocolar» cuando protocolar es el paso 4 → «O quarto passo».

### Distractores absurdos o agramaticales (≈18)

Ejemplos antes → después: C04 e0 «conhecer ele ontem, certo» → «conhecê-la ontem» (error de género); C05 i2 «Busco um café agora» → «Busco com parceiros que distribuam…» (preposición); C06 e0 «Você já passa por isso ontem?» → «Você já passou isso?» (falta «por»); C09 g1 «Aprendo que ouvir o usuário ontem» → «Aprendi de que…» (dequeísmo); C10 g1 «A lição é que cansei» → «A lição é que a galera curtiu muito a noite» (registro); C14 i1 «e já vimos» → «sem mais explicações»; C15 i1 «Também o teste» → «Além disso, o teste…»; C21 i1 «Decidiu o dia que a entrega» → «Decidi de que…»; C24 i1 «Fale mais baixo» → «passo a palavra de você para a proposta»; C29 i1 «A curva voa muito» → «A curva se sobe…» (reflexivo); C31 g1 «a sala ficaria muito bonita» → «O impacto seria baixo: o sistema ficaria fora do ar por dias» (incoherencia gravedad/consecuencia); C36 g1 y C37 g1 y C39 i1: pares «facultado/vedado» y «direito/dever» reescritos con construcciones jurídicas estándar.

### Ambigüedad, estímulo insuficiente y ordenar (≈30)

- **relacionar sin base**: C31 e3 (la solución contradecía la situación: «queda de energia: probabilidade baixa, impacto baixo») ahora trae datos y una solución con los mismos elementos; C32 e3 (consecuencias arbitrarias) → fórmula↔función; C48 e3 (interlocutor↔respuesta sin criterio) → premisas explícitas.
- **Completar con varias respuestas válidas**: se añade pista entre paréntesis o inicial: C15 i0/e1 «(parecer)», C18 e1 «(deduzir)», C23 i0/e1/C25 e1 «(lidar)» + marco pasado, C26 i0 «(revisar)», C27 g0/i0/e1 «(s…)/(c…)» (Segundo/Conforme), C29 i0 y C30 e1, C33 g0 «(a f… de)» (a fim de/para), C48 i0 «(mueble para guardar cosas)», C17 e1 («certo»).
- **ordenar con varias soluciones o sin gramática**: C03 g2 («…parcerias agora»), C04 g2 («fico no aguardo seu retorno», faltaba «do»), C07 g2 («último teste final»), C12 g2 (tres acciones intercambiables → se fija el orden en la consigna), C16 e3 (faltaba «:»), C19 g2, C20 g2/e3 (puntuación), C24 g2 y C25 g2 (consigna decía «pedir contrapartida/tiempo» y la frase no lo hacía), C30 g2 («amostra curta» → «pequena»), C42 g2 («Vamos com calma e fazer…» agramatical).

### Lengua pt-BR y registro (≈14)

- «correio / correo» usado como e-mail (C11 s1 «ao correio», C13 situación y ejemplos, «Linha do correo»): 5 normalizaciones automáticas + C11 → «e-mail».
- «altofalante» → «alto-falante» (C34); «escreve» imperativo → «escreva» (C12); «cotização» → «cotação» (C47); «Asunto: lanzamento» → «Assunto: lançamento» (C11); «mal-entendido»/«dados concretos» (C42, «datos» en un ejemplo); «Se o senhor cortar o prazo» dirigido a Iara → «Se a senhora…» (C48); «tela de pago» en una consigna española (C12); «tactful» en una consigna española (C17); «Prezada Iara, Prezados Senhores Diretores» (C46) → «Prezados Senhores Diretores».
- Fórmulas: «Responsável de segurança» → «Responsável pelo aviso/plano».

### Estructura del nivel (8 claves de integración)

Las clases C05, C10, C15, C20, C25, C30, C35 y C45 (cierre de bloque temático) tenían `introduce: []`, lo que `validar_plan.py` rechaza para bloques temáticos (y obligaba a reciclar claves sin sentido, p. ej. C35 evaluaba «nivel de riesgo» con la clave de cautela). Se añade una clave de integración por clase, siguiendo el patrón de N2 (`routine-work-transfer`) y N10 (`conversation-natural-transfer`):

`networking-transfer` (C05), `storytelling-integrated-transfer` (C10), `executive-email-transfer` (C15), `meeting-integrated-transfer` (C20), `selection-process-transfer` (C25), `report-integrated-transfer` (C30), `risk-plan-transfer` (C35), `negotiation-integrated-transfer` (C45).

Cada una se aplica a 4 ítems integradores (el último independiente, la primera pregunta de situación, y evaluación e3 y e4), de modo que la evaluación cubre la clave nueva. Para que los validadores pasen, se tocaron además: `tools/curriculo/pt/n9-outline.json` (campo `introduce` de esas 8 clases) y `curriculo/pt/MAPA.md` (una línea «Integración: …» al final de los bloques 1–7 y 9 de N9, igual que ya tenía N10). No cambia ningún contenido canónico.

Sobre los puntos que señalaron los autores: C35 queda resuelto con la clave de integración; C47 y C48 reciclan `academic-citation-formulas`, `plain-language-explanation-formulas`, `interest-based-negotiation-formulas` y `adapt-to-interlocutor-formulas` con sentido (citar fuente de una cifra, explicar un rubro, volver al interés, adaptar la respuesta) y no requieren cambios de clave.

## Hechos del reparto confirmados

- Camila Ortega (nació el 14 de marzo de 1999) cumple 35 años en marzo de 2034 y es directora de producto en Maré Digital (Porto Digital, Recife Antigo), con Iara como fundadora y Bruno como coordinador del equipo de producto.
- Trato: Camila usa «o senhor / a senhora» con el director Almeida, un patrocinador y un recurso formal; você con Ana, Bruno, Yasmin y Lucas; Iara se trata por su nombre sin «você» forzado en tercera persona («sua posição, Iara»).
- Yasmin Farias es desarrolladora del equipo (N6); Tomás Aguirre, argentino, del curso del Celpe-Bras (N8); Lucas Lins, amigo de Camila.
- El certificado Celpe-Bras, emitido por el Inep, es comprobante de lengua para la naturalización (MAPA, N9 B8); el trámite se presenta en la Polícia Federal.
- La temporada fuerte de lluvias de Recife va de abril a agosto (riesgos y simulacro de B7).
- Moneda: real (R$). Se usan solo lugares del reparto (oficina del Porto Digital); no se nombran hospitales, líneas del metrô ni calles.

## Hechos nuevos a confirmar

1. Camila se postula en N9 a un **nuevo cargo regional de dirección de producto** (ascenso interno, con entrevista STAR, negociación con Iara y e-mail de seguimiento; C21–C25). Si no se quiere, hay que reencuadrar B5 como «Camila entrevista candidatos» (C23) y quitar C21, C22, C24.
2. Personajes de rol/secundarios nuevos: Henrique (logística), Carolina (expositora), Davi, Valentina, señor Almeida (director de red de tiendas), Marta (empresa socia), Murilo (soporte), **Otávio Ramos** (proveedor de Nordeste Componentes, B9; sustituye a «Rafael Duarte»). Los nombres Rafael, Valentina y Carolina siguen como hablantes genéricos en ítems de completar.
3. Cifras ficticias (retención 31 % → 36 %, presupuesto de R$ 240 mil, descuento del 8 %, multa de 1 % semanal, renovación de seis meses, entrega del 30 de junio de 2034) y el proyecto de «redesenho do cadastro» son inventadas.
4. Trámite de naturalización: se menciona una «taxa» y el plazo legal; el texto de los artículos 3.º–4.º es un fragmento simplificado y ficticio. Conviene revisar con un hablante o un jurista que «protocolar na Polícia Federal», la exigencia de traducción juramentada para documentos en otra lengua y la existencia de una tasa se ajustan al procedimiento vigente en 2034 antes de publicar.
5. La feria de tecnología de São Paulo es genérica (sin nombre propio).
