# Revisión independiente · N1 francés, bloque 9 (clases 41–45)

- **Archivo:** `tools/contenido/ruta-fr/n1-b09.json` (`fr.n1.c41` … `fr.n1.c45`). Revisor distinto del autor.
- **Fecha:** 2026-10-01
- **Validador:** `python3 tools/validar_ruta.py fr --borrador tools/contenido/ruta-fr/n1-b08.json tools/contenido/ruta-fr/n1-b09.json` → **0 errores** (repetido tras los cambios).
- **Plan:** `python3 tools/curriculo/validar_plan.py fr` → 0 errores; ningún aviso «título de la unidad difiere» para c41–c45 (solo los 10 avisos conocidos de situaciones fuera del bloque del marco; ninguno es de B9).
- **Comprobación propia «nada sin enseñar»** (más estricta que el validador: solo cuentan ejemplos, tarjetas mostradas, patrón y tablas de Fundamentos, B1–B8 y la propia clase; revisa respuestas, opciones, audios, diálogos, tokens, pares y `aceptadas`): 0 faltas. Solo quedan los distractores deliberados `tournes` (c41 e3) y `continues` (c41 g2).
- **Reciclaje** (palabras de ejemplos y diálogos ya enseñadas antes): c41 76 %, c42 81 %, c43 86 %, c44 84 %, c45 87 % (≥ 30 %).
- **Tipografía:** U+202F antes de ? ! : ; en todo el francés (se corrigieron las líneas nuevas), 0 apóstrofos rectos.

## Veredicto

GO

## Contraste con las fichas (c41–c45)

Títulos, objetivos, gramática, vocabulario, sonido y tarea coinciden con `curriculo/fr/n1.json`. No se adelanta nada de c46–c50: no hay passé composé, participios ni «hier» (el único «J’ai que travailler» de c45 es una forma incorrecta usada como distractor de errores frecuentes). venir de + infinitivo (c44) y être en train de (c44) no aparecen antes; en c43 solo se usa «Tu viens comment ? — Je viens en métro», que es venir en presente (c34). Faltaba: nada (c41 tabla de imperativo con va / allez / prenez / faites; c42 sur, sous, devant, derrière, entre, à côté de, en face de, près de, loin de, au bout de + du / de la / de l’ / des y chez moi / toi / lui / elle / nous / le médecin; c43 futur proche con negación «je ne vais pas prendre», en bus / en métro / en voiture / en train / en avion, à pied / à vélo, ce soir / demain / samedi prochain; c44 venir de, être en train de y el contraste de tres momentos; c45 Tu veux… ?, Ça te dit de… ?, On va… ?, Avec plaisir, Volontiers, D’accord, Pourquoi pas, Désolé(e), je ne peux pas / je dois…, Une autre fois ?, Samedi, tu es libre ?).

**Adición del autor «loin» (c41): se mantiene.** La ficha de c41 ya lo exige en su gramática («C’est loin ?»), aunque no figure en la lista de vocabulario. Se enseña con tarjeta, ejemplo y diálogo, y c42 retoma «loin de» sin chocar («Ya viste loin en la clase anterior»). El resto de añadidos de vocabulario (le pont, la rue, le tour…) ya estaban enseñados o se enseñan en el ejemplo donde aparecen.

## Cambios aplicados (clase · ítem · antes → después)

### Coherencia del reparto (hechosDelReparto)

1. **c45 · situación (contexto, diálogo, s1).** La fiesta del diálogo era de Léa y Hugo la rechazaba; el reparto fija que la fiesta es la de **Hugo, el sábado 5 de mayo** (c28, c45) y el título de la clase es «Tu viens à ma fête ?». Ahora: Hugo invita a Emma, su vecina del mismo edificio («Samedi, le cinq mai, je fais une fête chez moi. Tu veux venir ?»); Emma, que trabaja de noche en un restaurante (c30), rechaza («Désolée, je ne peux pas : je dois travailler. Une autre fois ?»); Hugo propone el domingo y el cine; Emma acepta («Oui, je suis libre. Avec plaisir !»). 5 líneas, modela invitar, rechazar con excusa, proponer otro día y aceptar, con «désolée» en femenino. s1 pasa a «¿Por qué no puede ir Emma a la fiesta?».
2. **c42 · situación (líneas 5–6, s2) y ejemplo 8.** Ana, que vive en el mismo edificio que Hugo (y sabe su piso desde c40), le preguntaba «Et chez toi, c’est où ?». Ahora pregunta por «chez le médecin» (Ana: «Super ! Et chez le médecin, c’est où ?» → Hugo: «Chez le médecin, c’est près du parc.»); s2 pasa a «¿Dónde queda el médico?». Para no perder el modelo de «chez moi, c’est près du parc» (lo pide e4), el ejemplo 8 «Tournez à gauche : le musée est au bout de la rue.» → «Chez moi, c’est près du parc.» («au bout de la rue» sigue en la tabla p4 y en el diálogo).
3. **c44 · situación (contexto y última línea).** La ficha pide el pasado reciente «por ejemplo en un mensaje» (tarea: un mensaje de 3 frases); la situación era una llamada. Contexto → Hugo le escribe un mensaje a Ana y ella contesta. Última línea de Ana «Merci, Hugo ! À bientôt !» (no había nada que agradecer) → «D’accord, à bientôt, Hugo !».

### Contenido y exactitud

4. **c43 · v-billet.** «el boleto, el billete» → «el boleto» (español neutro de América; «billete» fuera).
5. **c42 · g4 (relacionar).** «devant = delante de» y «en face de = frente a» eran casi sinónimos en español (calibración 2). Se sustituye el par de devant por «sous = debajo de»; pista y feedback (es / en) reescritos («Sous es lo contrario de sur; … en face de contiene “face” …»).
6. **c42 · v-devant (traducción).** «delante de, enfrente» (enfrente = en face de) → «delante de».
7. **c44 · g1.** `Nous venons d’___ à la gare.` admitía «arriver» y «aller». La consigna ahora dice «Completa con el verbo arriver (llegar)» (es / en): una sola respuesta.
8. **c43 · e5 (aceptadas).** Se añaden «Demain, je vais aller à pied au cinéma.» y «Je vais aller à pied au cinéma demain.» (orden natural con à pied delante de la meta).
9. **c44 · ejemplos.** «Nous venons d’arriver : le train est à l’heure.» (traducción «el tren está a la hora», poco natural; además 9 ejemplos) → se elimina.

### Anatomía (5–8 ejemplos)

10. c41 tenía 9 ejemplos → se elimina «Faites le tour du parc.» (faites sigue en la tabla del imperativo). c43 9 → se elimina «La station de métro est près de l’hôtel.» (station sigue en las tarjetas). c44 9 → punto 9. c45 9 → se elimina «Je vais inviter Léa et Hugo.» (el futur proche se cita en p2). c42 ya tenía 8.

### Guías de pronunciación (regla 6 y convención ö = e muet, ya usada en B6–B7)

11. **c44 · p1.** Nasales con «y» antes de e: «Viens «vien»» → «vyen»; «bientôt «bien-to»» → «byen-to»; «il vient «il vien»» → «il vyen»; «ils viennent «il vién»» → «il vyenn» (n que suena, convención «nn» de c31); «demain «de-men»» → «dö-men».
12. **c44 · tarjetas.** déjà «de-sha» → «dé-sha»; tout de suite «tu de süit» → «tu dö süit»; en ce moment «an se mo-man» → «an sö mo-man»; téléphoner «te-le-fo-né» → «té-lé-fo-né»; bientôt «bien-to» → «byen-to».
13. **c43 · tarjetas.** ce soir «se suar» → «sö suar»; prochaine «pro-shén» (solo se distinguía por la tilde) → «pro-shenn».
14. **c42 · tarjetas y p1.** e muda = ö: devant «de-van» → «dö-van»; «… de» → «… dö» en à côté de, en face de, près de, loin de, au bout de y l’arrêt de bus; dessus «de-sü» → «dö-sü», dessous «de-su» → «dö-su».
15. **c45 · tarjetas.** désolé «de-zo-lé» → «dé-zo-lé»; ça te dit «sa te di» → «sa tö di»; en inglés inviter «ahn-vee-TAY» → «an-vee-TAY» (misma aproximación de la nasal que c44).
16. **c41 · p1.** le guide «le guid» → «lö guid».

### Español neutro

17. **c43 · tabla p3 y c44 · tablas p3 y p4, c45 · ejemplo vous.** «Va(n) a hablar», «Acaba(n) de leer», «Está(n) hablando», «¿Quiere(n) venir…?» (formas con paréntesis, no neutras) → «Ustedes van a hablar francés», «Ustedes acaban de leer un mensaje», «Ustedes están hablando francés», «¿Quieren venir a nuestra fiesta?».

## Revisión punto por punto

1. **Francés de Francia.** Imperativo sin -s en tourne / continue / traverse / va frente a prends / fais; allez, prenez, faites; jusqu’à / jusqu’au; à gauche / à droite sin artículo; du / de la / de l’ / des tras à côté de, en face de, près de, loin de, au bout de; sur / sous / devant / derrière / entre sin de; chez moi / toi / lui / elle / nous / Hugo / le médecin; en bus / en métro / en voiture / en train / en avion y à pied / à vélo; futur proche con «je ne vais pas prendre», «nous n’allons pas» y marcadores; venir de + inf. con d’ ante vocal; être en train de; fórmulas de invitación y rechazo cortés con désolé / désolée y occupé / occupée. Todo correcto.
2. **Explicaciones es / en.** Claras y cortas; es con tú y léxico neutro (boleto, auto, departamento, ustedes); en compara con el inglés donde ayuda (un solo imperativo en inglés, «I’m going to»). No hay «coger» ni «billete».
3. **Una respuesta defendible; `aceptadas`.** Revisados todos los `ordenar` (marcador al inicio o al final: c41 g5 y e4, c43 g2 y e3, c45 g5 y e3; c42 e3 con «S’il vous plaît» inicial), `escribir` (variantes con continuez, et / puis, soirée / fête, Ma maison / Chez moi) y `completar`. Un solo orden natural en c44 g2 y e3.
4. **Pistas y relacionar.** Cada pista ayuda al ítem (g1 c41 «vous → -ez»; g2 c41 «tu → sin -s»; g3 c42 «dev- / der-»; g3 c45 «dé-»). Pares con glosas distintas tras el punto 5.
5. **Sonidos del día.** c41 g / gu, c42 u / ou (sur / sous, dessus / dessous), c43 vocales puras (taxi, métro, vélo), c44 in / ain / ien, c45 liaison (vous‿êtes, on‿y va, les‿amis): exactos y coherentes con las fichas. ü y ö se definen en c41 p1 y se reutilizan después.
6. **Hablantes.** Solo nombres del reparto (Ana, Hugo, Emma) o «Le chauffeur».
7. **Personajes.** Ana (nueva en París, vive en el edificio de Hugo), Hugo (bicicleta, café, tercer piso), Emma (trabaja de noche en un restaurante). Formas femeninas para Ana y Emma. Cada comprensión tiene una sola respuesta. La fiesta de Hugo es el 5 de mayo.
8. **Anatomía.** Sonido → explicaciones → tablas → ejemplos (8) → tarjetas → guiada (5) → independiente (4) → situación (5–6 líneas, 2 ítems) → evaluación (6 ítems, 5 formatos en cada clase). `erroresFrecuentes`: 3 por clase. Los 6 formatos aparecen en el bloque.

## Observaciones no bloqueantes

- c43 y c44: en inglés «tren» / «train» se aproxima con «tran» y, en español, con «tren» (regla 6); se mantiene.
- c41 g2 (`opciones`: continue / continues / continuez): «va» también sería correcto con tu, pero no figura como opción y la pista fija continuer.
- c43 s1 / s2: la escena del bus (Ana toma el tren a las diez) y c44 (Ana llega en tren y toma un taxi) son escenas independientes; no hay contradicción.
- B8 (c40) fija «Hugo, tercer piso; Ana, primer piso»; B9 es coherente (c42 y c44 ya no sugieren que Ana ignore dónde vive Hugo).

## Sin resolver

Nada. Validación final: 0 errores.
