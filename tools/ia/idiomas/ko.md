# Ficha de idioma: coreano (ko)

Esta ficha se inserta en todos los prompts de `tools/ia/prompts/`. Es la única fuente de reglas propias del coreano.

## Alumno y variedad
- **Alumno:** adulto hispanohablante de EE. UU. o Latinoamérica.
- **Idiomas de apoyo:** español latino neutro con «tú» (ustedes, celular, carro o auto, computadora, departamento, manejar, boleto, jugo, papa, lentes) e inglés americano.
- **Coreano estándar de Seúl** (표준어), hangul con ortografía oficial. Sin dialectos (satoori) ni jerga de internet como respuesta esperada; el coloquial se marca «coloquial».
- **Examen de referencia:** TOPIK (I: niveles 1–2, II: niveles 3–6). La c50 de cada nivel imita el formato del TOPIK de su nivel, sin nombrar marcas en las consignas.
- **Escritura:** hangul; nada de hanja ni de japonés/chino. Los números en cifras solo en consignas de apoyo; en el texto coreano y en `audio` van en palabras (ver Ortografía).

## Romanización (`rom`)
- **Sistema único: Romanización Revisada (RR) oficial de Corea (2000).** Nunca McCune-Reischauer (ŏ, ŭ, ’), Yale ni grafías «de pasaporte» (Kim, Lee, Park, Seoul con «ou»). RR transcribe la pronunciación real (감사합니다 → gamsahamnida, 실례 → sillye), sin tildes ni signos diacríticos.
- **Dónde va:** en todos los textos coreanos de N1–N4 (vocabulario, ejemplos, diálogos, celdas de tabla). Desde N5, solo en vocabulario. En f0 y Nivel 0 siempre.
- **Formato:** `rom` en minúsculas, una palabra romanizada por cada eojeol del hangul (misma segmentación que el hangul, partículas pegadas: 저는 → `jeoneun`). Mayúscula solo en nombres propios (Seoul, Busan, Gim Ji-eun). Sin mayúscula de inicio de frase. Misma puntuación que el hangul.
- **Nombres de persona:** apellido + espacio + nombre; el nombre en dos sílabas con guion: `Gim Ji-eun`, `Bak Min-jun`.

**Tabla RR completa**

| Vocales | RR | | Consonantes | inicial | final (받침) |
|---|---|---|---|---|---|
| ㅏ | a | | ㄱ | g | k |
| ㅐ | ae | | ㄲ | kk | k |
| ㅑ | ya | | ㅋ | k | k |
| ㅒ | yae | | ㄴ | n | n |
| ㅓ | eo | | ㄷ | d | t |
| ㅔ | e | | ㄸ | tt | — |
| ㅕ | yeo | | ㅌ | t | t |
| ㅖ | ye | | ㄹ | r | l |
| ㅗ | o | | ㅁ | m | m |
| ㅘ | wa | | ㅂ | b | p |
| ㅙ | wae | | ㅃ | pp | — |
| ㅚ | oe | | ㅍ | p | p |
| ㅛ | yo | | ㅅ | s | t |
| ㅜ | u | | ㅆ | ss | t |
| ㅝ | wo | | ㅇ | (mudo) | ng |
| ㅞ | we | | ㅈ | j | t |
| ㅟ | wi | | ㅉ | jj | — |
| ㅠ | yu | | ㅊ | ch | t |
| ㅡ | eu | | ㅎ | h | t |
| ㅢ | ui | | | | |
| ㅣ | i | | | | |

- Se transcribe lo que se pronuncia: ㄱ,ㄷ,ㅂ,ㅈ entre vocales o tras ㄴ,ㄹ,ㅁ,ㅇ se escriben g, d, b, j (아기 agi, 고기 gogi, 바다 bada, 한국 hanguk); ㄹ entre vocales = r (사랑 sarang), ante consonante o al final = l (달 dal, 일본 ilbon), ㄹㄹ = ll (칠레 chille).
- Enlace (연음): se transcribe ya enlazado (한국어 hangugeo, 있어요 isseoyo). Nasalización: se transcribe nasalizado (입니다 imnida, 한국말 hangungmal). Tensión de ㄱㄷㅂ tras 받침 no se transcribe (학교 hakgyo).
- ㅅ ante ㅣ y vocales con y = s (시 si, 선생님 seonsaengnim), no «sh».

## Registro y tratamiento
- **Registro por defecto: 해요체** (cortés informal, terminado en -요) en todas las clases y diálogos.
- **합니다체** (formal, -습니다/-ㅂ니다) solo cuando la ficha de la clase lo enseñe; las fórmulas fijas 감사합니다, 죄송합니다, 안녕하십니까 se enseñan como bloque.
- **반말** (informal sin -요) solo desde la clase en que se enseñe y solo entre amigos, familia o menores; nunca como respuesta esperada con desconocidos ni en el trabajo. No se mezclan registros dentro de una misma conversación.
- **Honorífico -(으)시-:** solo en fórmulas fijas (안녕하세요, 가세요, 계세요, 주세요, 어떻게 지내세요) hasta que la ficha lo enseñe; nunca se aplica al propio hablante.
- **«Tú» y «usted»:** el coreano evita los pronombres de 2.ª persona. 너 es solo 반말 (brusco con adultos) y 당신 suena a reproche o es de pareja: no se usan como respuesta esperada. En su lugar:
  - nombre completo o nombre de pila + 씨 (김지은 씨, 지은 씨); nunca apellido solo + 씨;
  - cargo o título (선생님, 사장님, 의사 선생님);
  - o sin pronombre (el sujeto se sobreentiende: «¿Eres estudiante?» → 학생이에요?).
- **«Yo»:** 저 (humilde, por defecto en 해요체), 제 (mi); 나 solo en 반말.
- **«Ustedes»:** 여러분 (a un grupo, en presentaciones y avisos); en conversación, se nombra al grupo o se omite.
- **«Nosotros»:** 우리 (neutro) o 저희 (humilde, hacia un mayor o un cliente).
- **«Él/ella/ellos»:** casi nunca; se usa el nombre o 그 사람 («esa persona»). 그/그녀 solo en lectura escrita.

## Nombres y lugares (lista cerrada)
- **Personas** (nombre completo, apellido + nombre; hangul y RR):
  - Mujeres: 김지은 Gim Ji-eun, 박서연 Bak Seo-yeon, 최민지 Choe Min-ji, 정수빈 Jeong Su-bin, 강하윤 Gang Ha-yun, 조예린 Jo Ye-rin, 윤소희 Yun So-hui, 장유진 Jang Yu-jin.
  - Hombres: 김민준 Gim Min-jun, 박도윤 Bak Do-yun, 최지훈 Choe Ji-hun, 정현우 Jeong Hyeon-u, 강준호 Gang Jun-ho, 홍성민 Hong Seong-min, 송동현 Song Dong-hyeon.
  - **Apellidos (10):** 김 Gim, 박 Bak, 최 Choe, 정 Jeong, 강 Gang, 조 Jo, 윤 Yun, 장 Jang, 홍 Hong, 송 Song. No uses 이 (Lee/I), 오 ni 한 como apellidos: chocan con la partícula 이, el número 오 y el determinante 한 («un»).
  - Nombre de pila solo con 씨 (지은 씨, 민준 씨). Con nombre terminado en consonante, 이에요 se une: 민준이에요 (minjunieyo).
  - Fórmulas: «김 선생님», «박지은 씨», 의사 선생님. Si no, se usa el papel en coreano: 점원, 의사, 학생, 회사원, 직원.
  - Un nombre no pasa de una clase a otra: no hay historia ni reparto.
- **Ciudades:** 서울 Seoul, 부산 Busan, 인천 Incheon, 대구 Daegu, 대전 Daejeon, 광주 Gwangju, 수원 Suwon, 울산 Ulsan, 전주 Jeonju, 제주 Jeju; sin datos verificables (ni líneas de metro, direcciones, precios reales o comercios reales).
  - Lugares genéricos: 역, 약국, 우체국, 식당, 가게, 은행.
- **Países permitidos:** 멕시코, 콜롬비아, 아르헨티나, 칠레, 페루, 스페인, 미국, 한국, 일본, 스위스.
  - **Nunca Ecuador (에콰도르), Quito, Guayaquil, Cuenca ni «ecuatoriano»**, en ningún idioma ni campo.

## Guías de pronunciación (copiar, no inventar otras)
**ES:**
- **Consonantes lisas, aspiradas y tensas** (tres series, se distinguen por aire y tensión de la garganta):
  - lisas ㄱ ㄷ ㅂ ㅈ: suaves, con poco aire; al inicio suenan entre «k/g», «t/d», «p/b», «ch/y» (가 ≈ «ga/ka» suave); entre vocales suenan sonoras (아기 ≈ «agui»).
  - aspiradas ㅋ ㅌ ㅍ ㅊ: con un soplo fuerte de aire, como la «k», «t», «p», «ch» del inglés al inicio de palabra (kite, top). Pon la mano frente a la boca: debe sentirse el aire.
  - tensas ㄲ ㄸ ㅃ ㅆ ㅉ: garganta apretada, sin aire y más cortas e intensas (까 ≈ «kka» seco, 빵 ≈ «ppang» seco); no existen en español, se parecen a la «k», «t», «p» españolas muy secas.
  - Pares que cambian el significado: 달 (luna) / 탈 (máscara) / 딸 (hija); 불 (fuego) / 풀 (hierba) / 뿔 (cuerno).
- **ㅓ / ㅗ:** ㅓ (eo) = «o» abierta con la boca bien abierta y labios sin redondear (≈ «o» de «hot»); ㅗ (o) = «o» española redondeada. 서 (seo) ≠ 소 (so).
- **ㅡ / ㅜ:** ㅡ (eu) = «u» con labios estirados, sin redondear (ni «i» ni «u»); ㅜ (u) = «u» española con labios redondeados. 음 (eum) ≠ 움 (um).
- **ㅐ / ㅔ:** hoy se pronuncian casi igual (una «e» española); solo la ortografía los distingue (내/네). El audio y los ejercicios de escucha nunca dependen de esa diferencia; se enseña como dato de escritura.
- **ㅣ, ㅏ:** como «i» y «a» españolas; vocales siempre plenas.
- **ㅇ:** al inicio no suena (아 = «a»); al final suena «ng» como en «tango» (강 = «gang»).
- **ㅅ:** ante ㅣ y vocales con y suena entre «s» y «sh» (시 ≈ «shi»); no cambia el significado.
- **받침 (finales):** solo 7 sonidos en posición final y siempre sin soltar el aire: ㄱ(ㄱㅋㄲ) = «k», ㄴ = «n», ㄷ(ㄷㅅㅆㅈㅊㅌㅎ) = «t», ㄹ = «l», ㅁ = «m», ㅂ(ㅂㅍ) = «p», ㅇ = «ng». Ejemplos: 밖 → «bak», 옷 → «ot», 꽃 → «kkot», 앞 → «ap», 부엌 → «bueok». La consonante final se «traba» sin vocal extra: 학 = «hak», no «hakú».
- **Enlace (연음):** una 받침 seguida de ㅇ inicial pasa a la sílaba siguiente: 한국어 → han-gu-geo; 음악 → eu-mak; 있어요 → i-sseo-yo.
- **Asimilación (solo las básicas):**
  - nasalización: ㄱ/ㅂ + ㄴ/ㅁ → ㅇ/ㅁ + ㄴ/ㅁ: 감사합니다 → «gamsahamnida» (ㅂ+ㄴ → «mn»); 한국말 → «hangungmal»; 국물 → «gungmul».
  - ㄴ+ㄹ → «ll»: 실례 → «sillye».
  - Nada más (tensión, ㅎ débil, ㄹ+ㄴ) hasta que la clase lo enseñe.
- **ㄹ (r/l):** entre vocales = «r» simple como en «pero» (사랑 → «sarang»); al inicio de sílaba tras pausa, entre «r» y «l»; ante consonante o al final = «l» (달 → «dal», 일본 → «ilbon»); ㄹㄹ = «ll» larga (칠레 → «chille»). Nunca vibrante múltiple como «rr».
- **Ritmo y entonación:** cada sílaba dura casi lo mismo y no hay acento de intensidad como en español: no marques la sílaba «fuerte». En las preguntas con -요 la entonación final sube (학생이에요?); en afirmaciones baja.
- Nunca se dice que un sonido es «igual» al español si no lo es: se avisa de la diferencia (tres series, ㅓ, ㅡ, 받침).

**EN:**
- **Plain, aspirated, tense:** plain ㄱ ㄷ ㅂ ㅈ are soft and low-air (between «k/g», «t/d», «p/b», «ch/j»); aspirated ㅋ ㅌ ㅍ ㅊ carry a strong puff of air like English «k», «t», «p», «ch» at the start of a word; tense ㄲ ㄸ ㅃ ㅆ ㅉ have a tight throat and no air, shorter and sharper.
- **ㅓ** like «u» in «cup» with a wide-open mouth and unrounded lips; **ㅗ** like «o» in «go», lips rounded; **ㅡ** like «oo» in «good» with lips spread flat; **ㅜ** like «oo» in «boot», lips rounded; **ㅐ/ㅔ** both ≈ «e» in «bed» (nearly the same today).
- **ㅇ** is silent at the start of a syllable and sounds «ng» as in «sing» at the end.
- **받침 (final consonants):** only 7 sounds and always unreleased: k, n, t, l, m, p, ng.
- **Linking:** a final consonant moves to an empty ㅇ in the next syllable (한국어 → han-gu-geo); 합니다 sounds «hamnida» (nasalization).
- **ㄹ:** a single tap like the middle of «butter» between vowels (사랑); like «l» at the end of a syllable (달); ㄹㄹ = long «ll».
- **Rhythm:** syllable-timed, no stressed syllables; questions with -요 rise at the end.

## Gramática: lo que más falla en hispanohablantes (úsalo en `erroresFrecuentes` y distractores)
- **은/는 frente a 이/가:**
  - 은/는 marca el tema (lo que se comenta, contraste): 저는 학생이에요. 이/가 marca el sujeto nuevo o foco y va con 아니에요 y 있어요/없어요: 학생이 아니에요, 책이 있어요.
  - Forma por sonido final: 는/가 tras vocal, 은/이 tras consonante: \*저은 → 저는; \*책는 → 책은; \*학생가 → 학생이.
  - \*저가 → 제가 (제가 = 저 + 가, forma irregular, solo cuando la clase lo enseñe).
- **Orden SOV y verbo al final:** \*학생이에요 저는 → 저는 학생이에요; \*먹어요 사과를 → 사과를 먹어요. Los complementos van antes del verbo; la pregunta no invierte el orden, solo cambia la entonación o lleva palabra interrogativa en su sitio: 어디에 있어요?
- **Copula:** 이에요 tras consonante, 예요 tras vocal: \*의사이에요 → 의사예요; \*학생예요 → 학생이에요. Negación: 이/가 아니에요 (\*학생 안 이에요 → 학생이 아니에요).
- **Registro de cortesía:** \*안녕! con un desconocido → 안녕하세요; mezclar 반말 con 해요체; olvidar -요 al final (\*학생이야 con un adulto → 학생이에요).
- **Números:** sinocoreanos (일, 이, 삼) para dinero, fechas, teléfono, minutos, pisos; nativos (하나, 둘, 셋) para contar con contadores, horas y edad. \*삼 개 → 세 개; \*하나 원 → 일 원; \*다섯 천 원 → 오천 원. Ante contador, nativos se acortan: 하나 → 한, 둘 → 두, 셋 → 세, 넷 → 네, 스물 → 스무.
- **Contadores:** el contador es obligatorio y va tras el número y después del sustantivo: \*두 학생 → 학생 두 명; \*사과 두 → 사과 두 개. Personas = 명, cosas = 개. Espacio entre número y contador (한 개, 두 명).
- **Omitir el sujeto:** el hablante calca el «yo/tú/él» obligatorio del español: \*저는 저는 학생이에요, \*당신은 학생이에요? → 학생이에요? Si el sujeto es evidente, se omite; 너 y 당신 no se usan con adultos.
- **있어요/없어요:** 있어요 = hay / tiene / está en un lugar (책이 있어요, 서울에 있어요); 없어요 es su opuesto, no se niega con 안: \*안 있어요 → 없어요. No confundir con 이에요 («es»): \*책이에요 por «hay un libro» → 책이 있어요. El lugar lleva 에: \*서울 있어요 → 서울에 있어요.
- **에 / 에서:** 에 (destino, ubicación con 있어요, 살아요: 서울에 살아요); 에서 (origen o lugar de acción: 미국에서 왔어요, 식당에서 먹어요). \*미국에 왔어요 → 미국에서 왔어요.
- **Posesivo:** \*저의 이름 se entiende, pero natural es 제 이름 («mi nombre»); \*저는 이름은 → 제 이름은.
- **Pronunciación leída como se escribe:** \*감사함니다 (escrito) → 감사합니다; leer 값 como «gap-s». Se evalúa solo cuando la clase trata esas reglas.

## Falsos amigos (⚠ obligatoria, con contraste, solo estos o equivalentes igual de reales)
- **Con el español:**
  - 말 (mal = palabra, habla o caballo ≠ «mal» = malo), 보다 (boda = ver ≠ «boda»), 소 (so = vaca), 이 (i = diente, dos, este: homófonos que se distinguen por contexto).
  - 사이다 (saida = gaseosa transparente tipo Sprite ≠ sidra / cider).
- **Préstamos del inglés engañosos (konglish, ⚠ con contraste; ya no son ingleses):**
  - 아파트 (apateu = departamento en un edificio alto, ≠ «apartment» como unidad), 맨션 (maensyeon = bloque de departamentos, ≠ mansión), 빌라 (billa = bloque bajo, ≠ villa).
  - 노트북 (noteubuk = laptop, ≠ cuaderno / notebook), 핸드폰 (haendeupon = celular), 샤프 (syapeu = portaminas, ≠ afilado / sharp), 콘센트 (konsenteu = enchufe de pared, ≠ consentimiento / consent), 서비스 (seobiseu = obsequio gratis, ≠ servicio), 화이팅 (hwaiting = ¡ánimo!, ≠ pelear / fighting).
  - 원피스 (wonpiseu = vestido, ≠ «one piece» de baño), 오토바이 (otobai = moto), 에어컨 (eeokeon = aire acondicionado), 핸들 (haendeul = volante, ≠ asa / handle), 컨닝 (keoning = copiar en un examen, ≠ astuto / cunning), 미팅 (miting = cita grupal, ≠ reunión de trabajo), 더치페이 (deochipei = pagar a medias).
- **No son falsos amigos** (sin ⚠, se escriben en hangul tal cual): 커피, 호텔, 버스, 택시, 컴퓨터, 텔레비전, 피자, 아이스크림, 카메라, 라디오.
- **Jerga o registro** (대박, 짱, 헐): se marca «coloquial», sin ⚠.

## Ortografía y forma (reglas duras)
- **Espaciado (띄어쓰기):** se separa por eojeol (unidad entre espacios = palabra + partículas/terminación). Las partículas van pegadas a la palabra anterior (저는, 학생이, 서울에서); el verbo/adjetivo conjugado forma un eojeol (학생이에요).
  - Contador y unidad de medida separados del número: 한 개, 두 명, 오천 원. Los números compuestos hasta mil van pegados: 이십, 이십삼, 삼백오십; desde 만 se separa por grupo: 삼만 오천 원.
  - Nombre + 씨 separado: 김지은 씨. Apellido + nombre pegado: 김지은.
  - Fórmulas fijas con espacio normativo: 안녕히 가세요, 안녕히 계세요, 또 봐요, 다시 말해 주세요, 만나서 반가워요.
- **`ordenar`:** los tokens son los eojeol, con las partículas pegadas; la puntuación va pegada al eojeol final. «저는 학생이에요.» → tokens ["학생이에요.", "저는"]. Nunca se parte una partícula o terminación en un token aparte.
- **Puntuación:** «.», «?», «!», «,» occidentales; comillas «…» en el texto coreano. En `respuesta` no van comillas.
- **Mayúsculas:** no existen en hangul. En `rom`, solo nombres propios.
- En `audio`, números, precios y horas se escriben en palabras («오천 원», «이십일»). Nunca «₩», «%», «/», «_» ni «→» en el audio.
- `aceptadas` recoge las variantes reales:
  - orden alternativo correcto (complementos de tiempo y lugar movibles; el verbo no);
  - sujeto explícito u omitido («저는 학생이에요» / «학생이에요»);
  - partículas intercambiables solo cuando la clase las enseñe (-은/는 vs -도).
  - Nunca se añaden variantes sin espacios ni con otro registro: esa tolerancia la pone la app (puntuación y mayúsculas).
- **Contracciones habladas** (전 = 저는, 난 = 나는, 이거 = 이것): no se aceptan en N1–N4 salvo que la ficha de la clase las enseñe.

## Formas de citación del vocabulario
- **Sustantivos, partículas, adverbios:** tal cual (학생, 은, 천천히).
- **Verbos y adjetivos:** forma de diccionario en -다 y, entre paréntesis, la forma 해요: `texto` = «먹다 (먹어요)», `rom` = «meokda (meogeoyo)»; adjetivos igual: «좋다 (좋아요)», «괜찮다 (괜찮아요)». Una sola forma por entrada, con espacio antes del paréntesis. No uses «/» dentro de `texto` (la copulativa son dos entradas: «이에요» y «예요»).
- Expresiones fijas se citan completas en su forma real (안녕하세요, 감사합니다, 만나서 반가워요).
- Los verbos irregulares (ㅂ: 고맙다 → 고마워요; 르: 모르다 → 몰라요; ㅡ: 쓰다 → 써요; ㄹ: 살다 → 살아요) llevan nota breve con la irregularidad.

## Fundamentos y Nivel 0
Las claves previas (`previos`) y los ids de Fundamentos (`ko.f0.*`) vienen en el contexto. El Nivel 0 es «Leer y pronunciar coreano» (hangul, 받침, enlace, asimilación básica). N1 c01 parte de lo que enseña f0: saludos, cortesía, presentarse, 이에요/예요, 은/는, números sinocoreanos 0–20 y nativos 1–10, 있어요/없어요. Todo texto coreano de f0 y N1–N4 va con `rom` en RR.
