# Revisión del plan N7 (portugués de Brasil)

Veredicto: GO

Validadores sobre `curriculo/pt/n7.json`: `validar_plan.py pt` → 0 errores (1.470 avisos de vocabulario repetido en todo el idioma, esperables); `validar_plan_detallado.py pt curriculo/pt/n7.json` → 0 errores · 50 clases · 673 ejercicios · 673 consignas únicas · 673 ejemplos únicos; `validar_outline_nivel.py pt 7` → 0 errores · 48 claves nuevas · 329 previos. Los 50 ids están en estado `planificado` y los campos congelados coinciden con el esqueleto.

Revisión independiente de los 10 lotes (C01–C50). Se aplicaron **68 correcciones puntuales** en `tools/curriculo/pt/n7-lote-*.json` (41 clases tocadas) y se consolidó el nivel. Se editó también `tools/curriculo/pt/n7-outline.json` (tarea de C21, C41 y C43, y la grafía «custo-benefício» de C47) porque el validador congela esos campos contra el esqueleto. Copias originales en el scratchpad (`pt/r7/orig/`).

## Cambios por tipo

### Canon y personajes (10)

- C30: el orador inventado «Marina Duarte» chocaba con Dona Marina → «Letícia Moura» (se evita también «Prado», apellido de un cliente de N6). Afecta a SIT, s0, s1, e0, e1, e2 y e4.
- C04: «Rafael Duarte» (cliente) → «Otávio Duarte». Así «Rafael» deja de usarse como cliente en N7 y no choca con el proveedor del mismo nombre que prevé N9 ni con «Rafael Prado» (cliente de N6). C31 también tenía un «Rafael, o fiador»: ahora es solo «o fiador». En todo N7 ya no aparece «Rafael».
- C31: la propuesta de renovación iba dirigida a «Camila e Ana», pero Ana vive en Lisboa desde N4 → «Camila e Larissa» (Larissa ocupa el cuarto de Ana en Graças, MAPA N4); g2 «inquilinas de Ana» → Larissa.
- C41: «Marina disse: Estou cansada» (el nombre canónico de Dona Marina en un ejemplo sin relación) → «Luana».
- C08: aviso de obra «Edifício Boa Viagem» con «seu Pedro, o porteiro» (el edificio y el portero de Dona Marina, donde Camila ya no vive) → el prédio de Camila en Graças, «o porteiro» sin nombre.
- C44: «Lucas, que estuda Computação na UFPE» (en 2032 ya está graduado, N6 B5) → «trabalha com programação». C26: «meu colega Lucas chega à UFPE» → «um colega meu».
- C20: Iara le habla a Camila de «a senhora» (en el MAPA ella la tutea con você) → «você».
- C35: «Prezada Helga» (gerente a quien Camila llama «a senhora») → «Prezada Sra. Helga».

### Hechos reales, fuentes ficticias y atribuciones (9)

- C18: «Fonte A: guia turístico antigo; Fonte B: estudo universitário» sobre un puente del Capibaribe con fechas (1860/1840) e ingeniero inglés, presentados como reales → ahora Renata los «inventa» y el texto lo dice («dados fictícios, só para praticar», «fictício»); no se atribuye ningún dato inventado a la historia de Recife. i0: «Conta a lenda que… acredita-se que seja só uma lenda» (la respuesta aparecía en el enunciado) → «só uma história» y la consigna pide «palabra», no «verbo».
- C16 e0: «Em 1637 construiu-se uma nova cidade ao lado do povoado do porto» → «uma nova cidade, Maurícia, na ilha de Antônio Vaz» (hecho: Maurício de Nassau, 1637). Se verificaron C16–C17: poblado del puerto (s. XVI), invasión de 1630 (Olinda atacada y Recife ocupado), Nassau en 1637, expulsión en 1654, reforma del barrio a inicios del s. XX, Porto Digital creado en 2000, rosa dos ventos del Marco Zero, Paço do Frevo: sin errores.
- C21, C41: la tarea decía «texto de Manuel Bandeira» / «fragmento de Clarice Lispector» pero los versos y el trecho eran inventados para la clase. Se corrigen SIT y tarea (outline incluido): «poema breve de ejemplo» y «fragmento escrito al estilo de Clarice Lispector».
- C43: tarea «cuento de João Cabral» → «fragmento de «Morte e Vida Severina», de João Cabral de Melo Neto» (es poema dramático; outline incluido). El contenido (retirante que sigue el Capibaribe, nacimiento al final) ya era correcto.
- C06: la biografía de «Aurélio Lemos, escritor pernambucano» podía leerse como real → «escritor pernambucano imaginário (texto fictício que a professora Renata preparou para a aula)»; g1 decía «em Paris» cuando la biografía dice Salvador.
- C19: «mirante» y «azulejos da fachada… são originais» (infraestructura/dato no verificable) → «Cais do Sertão» y el piso con rosa dos ventos del Marco Zero (lugares reales del MAPA).
- C09: itinerario imposible (8h + 3h de vuelo + escala de 2h20 no llega a un vuelo a las 14h; São Paulo–Lisboa de ~10h no aterriza a las 5h50) → salida 8h, vuelo de 3h30, escala de 4h30, vuelo a las 16h y llegada 5h50 (hora local); ajustados SIT, g2, s0, s1 y e2.

### Distractores absurdos o que no miden la clave (15)

- C07 g0 «Nunca chegou, mas partia» y i0 «Saímos e chover» (agramatical) → alternativas con sentido: «Chegou, mas só partiu dias depois» y «Saímos e, horas depois, começou a chover».
- C17 i1 «…, e assim ficou» → pasado puro «O porto tornou-se…».
- C19 e1 «o mirante, não olhem para ele» → error real de régimen: «repare o Cais do Sertão» (falta «em»).
- C23 g0 y s0 «rio e ponte» → «fruta e parte do sapato», «praça e instituição financeira»; e4 pedía «castigo e plumagem» y la respuesta decía «tristeza e pluma» (inconsistente) → «castigo e pluma de ave».
- C26 g0 «Ontem choveu no Recife» y e0 «Eu vou à praia» (no son ni tesis ni premisa plausibles) → hechos descriptivos que el estudiante podría confundir con una tesis.
- C31 e1 «…a vaga ontem» → error real: «Se o fiador aceitará…» (futuro tras «se»). C50 e1 igual («aceita… ontem» → «aceitará»).
- C39 g1 «bergamota é o nome do abacaxi» y e1 «mexerica é um sotaque… bergamota, um prato» → confusiones regionales plausibles.
- C43 e1 «só uma discussão de trânsito» → «só uma discussão pessoal, sem relação com a pobreza».
- C15 g2: el ítem atribuía a Yasmin que «Bruno estava viajando», contra la SIT (Bruno estaba en la videochamada) → la hipótesis real de Yasmin sobre Diego («o acesso dele é só de leitura»).

### Lengua, ortografía y registro pt-BR (12)

- C24 e3/e4: «oficina» (= taller; falso amigo, además en un ejercicio sobre una oficina de tecnología) → «escritório».
- C10: «Que dia comprido» → «Que dia longo». C07: «anteriormente à hora marcada» y el pluscuamperfecto torpe del diario → «desde antes da hora marcada», «escrevi… aprendi».
- C47: «custo benefício» → «custo-benefício» (Acordo; outline y vocabulario incluidos).
- C25: e3 (frase sin sentido «Eu quebro o galho feito um relógio») y i2 («caiu feito uma fruta madura») → «Seu prazo parece um elástico» y «caiu como se fosse um castelo de cartas».
- C27 e3: «não vale sempre» (no natural) → «nem sempre vale».
- C21: «Esse feito é o mesmo que como?» → «Esse «feito» é o mesmo que «como»?».
- C33 i0: la respuesta «divergência» no encajaba con la consigna ni con la frase («Nossa ___ é o prazo») → «prioridade».
- C30: «a torcida quer festa» (vocabulario del fútbol en un debate de Carnaval) → «o folião»; i2 con un «isso não procede como argumento final» sin sentido → «o retorno social compensa».
- C29: «¿Qué piden Camila…?» (concordancia en español) → «¿Qué pide…?»; C18 consigna «verbo» → «palabra».

### Coherencia con la historia (6)

- C37: aclarado que Ana «passou o dia a trabalho na cidade do Porto» (si no, «no Porto» se lee como «en el puerto») y que Camila está sola en Lisboa; «todo mundo conversa alto» → «muita gente» (unidad contra los estereotipos).
- C38: el audio de refutación decía «os nordestinos são todos preguiçosos» (estereotipo hiriente repetido en un ítem) → «festeiros».
- C14: «em frente ao Café da Bia» (no está en el testimonio de la SIT) → «da calçada da praça».
- C15: coartada de Ana «reunião das 15h» → «videochamada das 14h às 16h» (coincide con la SIT).
- C09–C10 y B8: la visita a Lisboa se anuncia en B2 (itinerario y nota de voz) y se vive en B8; se deja explícito en `hechosDelReparto` que es la misma visita (dos semanas, C40).

## Límites aceptados

- El esqueleto es el mismo en las 50 clases (3 guiados + 3 independientes + 2 de situación + 5–7 de evaluación, un relacionar con pistas cruzadas por clase): formato aprobado y exigido por el validador.
- Las lecturas de B9 son textos de ejemplo escritos para la clase; los únicos textos reales citados son el verso «Vou-me embora pra Pasárgada» (Bandeira) y el título de «Morte e Vida Severina» (João Cabral).
- El diálogo de C26–C30 usa personajes de rol («orador», «ciclistas», «autora») sin nombres reales; las cifras (40 % de abandono, 60 % de clientes recurrentes) son datos ficticios del caso de Maré Digital.
- «Sr. Salazar» (C01, C03) y «Prezado Diego» (C46) conviven: ambos son habituales en el correo comercial brasileño.

## Hechos del reparto confirmados

- Camila cumple 33 años el 14 de marzo de 2032, lleva seis años en Recife, es gerente de producto en Maré Digital (Porto Digital, Recife Antigo), vive en Graças en el apartamento de seu Alberto con Larissa y estudia con la profesora Renata (você). Moneda: R$.
- Ana vive en Lisboa desde N4; en B8 Camila la visita (dos semanas). Las diferencias Brasil–Portugal son cultura, sin clave de gramática (pt-PT entra en N8 B4).
- Camila investiga la historia de Recife (holandeses 1630–1654, puerto, puentes) para una ruta guiada (B4); lee a Clarice Lispector, Manuel Bandeira y João Cabral (B9).
- Dona Marina (68, Boa Viagem), Lucas (28, ya graduado), Bruno (coordinador), Bia (Café da Bia), Iara (a senhora), Diego Salazar (cliente mexicano), Yasmin (desarrolladora) y seu Alberto (o senhor) conservan sus roles del MAPA.

## Hechos nuevos a confirmar

- Personajes secundarios nuevos de N7: Otávio Duarte (cliente, C04), Letícia Moura y Rui Pessoa (debate del Carnaval, C30), Helga Moreira (gerente del hotel, C35), Henrique (grupo de brasileños en Lisboa, C38), Dona Cecília (ejemplo literario, C45), Luana, Marta y Caio (ejemplos). Ninguno repite nombre ni apellido canónico ni de otros niveles.
- Camila sigue en el apartamento de Graças con Larissa en 2032 (C08, C31): el contrato se renueva por 24 meses con reajuste del 6 % (en N6 ya se había negociado un 6 %; aquí se trata de la renovación siguiente).
- Lucas trabaja en programación en 2032 (graduado en N6 B5); no se dice dónde.
- Bia Santos es clienta de Maré Digital en C49 (app de fidelidad), no solo amiga y dueña del café.
- El proyecto de visitas guiadas (N5 B9) sigue activo en 2032: reserva de grupo de 30 personas y flujo de registro del app de reservas (C32, C35, C47).
