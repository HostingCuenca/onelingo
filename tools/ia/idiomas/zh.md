# Ficha de idioma: chino mandarín (zh)

Esta ficha se inserta en todos los prompts de `tools/ia/prompts/`. Es la única fuente de reglas propias del chino.

## Alumno y variedad
- **Alumno:** adulto hispanohablante de EE. UU. o Latinoamérica.
- **Idiomas de apoyo:** español latino neutro con «tú» (ustedes, celular, carro o auto, computadora, departamento, manejar, boleto, jugo, papa, lentes) e inglés americano.
- **Variedad:** mandarín estándar (普通话), **caracteres simplificados** (简体字). Nunca caracteres tradicionales (们, no 們; 说, no 說; 国, no 國). Ni cantonés, ni vocabulario exclusivo de Taiwán o Hong Kong (出租车 y no 的士; 手机 y no 行动电话).
  - Los regionalismos y la erhua (-r) solo aparecen para comprensión, desde N8, y nunca como respuesta esperada. El curso escribe 哪里, no 哪儿.
- **Exámenes de referencia:** HSK 3.0 (niveles 1–9). La c50 de cada nivel imita el formato de la prueba HSK 3.0 de su banda, sin nombrar marcas en las consignas.
- **Tratamiento (la ficha de la clase fija cuál se usa):**
  - «tú» = 你; «usted» = 您; «ustedes» = 你们; «nosotros» = 我们.
  - **您** es singular y de respeto: mayores, clientes, profesores, desconocidos en contexto formal. No existe «您们»: varias personas formales = 你们.
  - **你** con amigos, familia, compañeros y gente joven.
  - **咱们** = «nosotros incluyéndote a ti» (tú y yo; todos los presentes); es coloquial, típico del norte. 我们 puede excluir o incluir al oyente. 咱们 solo se enseña como reconocimiento (nota única en N3 o N4) y nunca es respuesta esperada.
  - 他 (él) y 她 (ella) suenan igual (tā); solo se distinguen por escrito. En `audio` no hay diferencia.
  - Títulos tras el apellido, como palabras sueltas: 王 老师, 张 先生 (señor), 刘 女士 (señora). Nunca 小姐 con desconocidas (ver falsos amigos).

## Texto chino: palabras, rom y tonos (reglas duras, valen para todo el curso)
**1. Separación de palabras.** Todo texto chino del contenido se escribe con **espacios entre palabras**: «我 是 学生。». La app quita los espacios al leerlo en voz alta; en `ordenar`, los tokens son esas palabras.
- La puntuación china se pega a la palabra anterior, sin espacio antes ni después: «你 好 吗？» (no «你 好 吗 ？»).
- Se segmenta como en un diccionario moderno (现代汉语词典), con esta granularidad fija:
  - Palabras compuestas léxicas = una palabra: 学生, 老师, 朋友, 手机, 名字, 中文, 认识, 高兴, 没有, 我们, 你们, 中国, 美国人.
  - Fórmulas fijas = una palabra: 谢谢, 再见, 对不起, 没关系, 请问. **不 客气 = dos palabras** (不 + 客气, «bú kèqi»).
  - **Saludo 你 好 = dos palabras**, igual que 您 好, 你们 好, 早上 好, 晚上 好, 大家 好 (pronombre o momento + 好).
  - Partículas y clasificadores siempre sueltos: 的, 吗, 呢, 了, 个, 本, 杯 («我 的 书», «三 本 书», «你 好 吗»).
  - 不, 没, 很, 也, 都, 在 sueltos: «我 不 是 学生», «我 很 忙». (Excepciones léxicas, una palabra: 没有, 没关系, 不错, 对不起.)
  - **Número + clasificador + sustantivo = tres palabras**: 三 个 学生. Los numerales compuestos se escriben juntos: 十五, 二十三, 九十九 (nunca «二 十 三»).
  - 这 / 那 / 哪 + clasificador, sueltos: 这 个, 那 本 书, 哪 国 人.
  - **Nombres de persona: apellido y nombre, dos palabras** («王 芳»). Los nombres de pila de la lista cerrada tienen un solo carácter.
  - Topónimos y países, una palabra: 北京, 墨西哥. Nacionalidad = país + 人, una palabra: 墨西哥人, 中国人.
- Los números van en caracteres chinos en todo texto chino y en `audio` (我 二十 岁; 九 月 二十五 号; 三 点 半). Las cifras solo aparecen en el texto de apoyo.

**2. Romanización (`rom`).** Pinyin con marcas de tono (nǐ hǎo), en minúsculas, con mayúscula inicial solo en nombres propios y al empezar frase.
- **Dónde:** va en todos los textos chinos de N1–N4. Desde N5, solo en vocabulario (y en consignas de pronunciación).
- **Alineación:** una palabra china = un grupo de pinyin separado por espacios; las sílabas de la misma palabra van pegadas (谢谢 → xièxie, 老师 → lǎoshī, 没有 → méiyǒu). Los dos grupos de un nombre llevan mayúscula: 王 芳 → Wáng Fāng. Sin números de tono, sin «v» por «ü».
- **Puntuación en `rom`:** la occidental (. , ? !) pegada a la última sílaba; en el texto chino, la china (。，？！、).
- **Colocación de la marca:** sobre la vocal «a» si hay; si no, sobre «e» u «o»; en «iu» y «ui», sobre la última vocal. Sílabas con vocal inicial tras otra sílaba llevan apóstrofo: shí'èr, Xī'ān.
- **Tono neutro:** sin marca (de, ma, men, xièxie, péngyou, shénme).
- **Convención de sandhi, escrita en superficie (la fijamos así: `rom` refleja lo que se oye):**
  1. **3.er tono + 3.er tono:** el primero se escribe con 2.º tono: 你 好 → ní hǎo; 我 很 好 → wó hén hǎo (en una cadena de 3.º, todos menos el último pasan a 2.º). Dentro de una palabra también: 水果 → shuíguǒ, 哪里 → nálǐ. Los demás 3.º (ante 1.º, 2.º, 4.º o tono neutro) se escriben con 3.º sin cambio: wǒ jiào, nǐmen, hǎo ma. Una pausa (coma, punto, ?) corta la cadena: «Nǐ hǎo, wǒ hěn hǎo.» → Ní hǎo, wǒ hén hǎo.
  2. **不 (bù):** se escribe **bú** ante un 4.º tono (不 是 → bú shì; 不 客气 → bú kèqi; 不 对 → bú duì); **bù** ante 1.º, 2.º y 3.º (bù hē, bù lái, bù hǎo) y solo. En «A 不 A» se vuelve neutro: 是 不 是 → shì bu shì.
  3. **一 (yī):** **yī** solo, contando, en números, ordinales y fechas (十一 shíyī); **yí** ante 4.º (一 个 → yí gè; 一 遍 → yí biàn); **yì** ante 1.º, 2.º y 3.º (一 杯 → yì bēi; 一 年 → yì nián; 一 本 → yì běn; 一点 → yìdiǎn). Entre verbos repetidos es neutro (看 一 看 → kàn yi kàn).
  4. **个** como clasificador se escribe **gè** (4.º), no ge.
  5. 两 (liǎng) sigue la regla 1: 两 本 → liáng běn; 两 个 → liǎng gè.
- El sandhi no se explica en cada clase: se aplica en `rom` y se enseña en Nivel 0 (`tone-sandhi-third`, `yi-bu-sandhi`).

**3. Citación del vocabulario.** Palabra + pinyin + clasificador habitual del sustantivo, en tono de diccionario (el sandhi dentro de la palabra sí se escribe):
- `书` — shū — clasificador 本 (běn)
- `老师` — lǎoshī — 位 (wèi)
- `咖啡` — kāfēi — 杯 (bēi)
- `学生` — xuésheng — 个 (gè)
- Los verbos y adjetivos van sin clasificador (是 shì; 好 hǎo). En el JSON, `texto`, `rom` y, si es sustantivo, `clasificador` («本 běn»). Si el sustantivo no tiene clasificador propio, se cita con el comodín 个 (名字 míngzi — 个 gè).

## Nombres y lugares (lista cerrada)
- **Personas:**
  - Apellidos (10): 王 Wáng, 李 Lǐ, 张 Zhāng, 刘 Liú, 陈 Chén, 杨 Yáng, 黄 Huáng, 赵 Zhào, 吴 Wú, 周 Zhōu.
  - Nombres completos (15), apellido + nombre:
    - Mujeres (8): 王 芳 Wáng Fāng, 李 梅 Lǐ Méi, 张 丽 Zhāng Lì, 刘 敏 Liú Mǐn, 陈 静 Chén Jìng, 杨 雪 Yáng Xuě, 黄 婷 Huáng Tíng, 周 英 Zhōu Yīng.
    - Hombres (7): 赵 伟 Zhào Wěi, 吴 强 Wú Qiáng, 王 磊 Wáng Lěi, 李 涛 Lǐ Tāo, 张 浩 Zhāng Hào, 刘 军 Liú Jūn, 陈 亮 Chén Liàng.
  - Se escriben con espacio entre apellido y nombre; en `ordenar` son dos tokens. Fórmulas: «王 老师», «张 先生», «刘 女士».
  - Si no, se usa el papel en chino: 服务员, 老板, 医生, 学生, 同事.
  - Un nombre no pasa de una clase a otra: no hay historia ni reparto.
- **Ciudades (10):** 北京 Běijīng, 上海 Shànghǎi, 广州 Guǎngzhōu, 深圳 Shēnzhèn, 成都 Chéngdū, 杭州 Hángzhōu, 西安 Xī'ān, 南京 Nánjīng, 武汉 Wǔhàn, 重庆 Chóngqìng, sin datos verificables (ni líneas de metro, direcciones, precios reales o comercios reales).
  - Lugares genéricos: 火车站, 药店, 邮局, 学校, 饭馆, 超市.
- **Países permitidos:** 中国 Zhōngguó, 美国 Měiguó, 墨西哥 Mòxīgē, 哥伦比亚 Gēlúnbǐyà, 阿根廷 Āgēntíng, 智利 Zhìlì, 秘鲁 Bìlǔ, 西班牙 Xībānyá, 新加坡 Xīnjiāpō.
  - **Nunca Ecuador (厄瓜多尔), Quito (基多), Guayaquil (瓜亚基尔), Cuenca (昆卡) ni «ecuatoriano»**, en ningún idioma ni campo.
- Dinero: 块 (kuài) en el habla; no se escriben «¥», «RMB» ni cifras en el texto chino.

## Guías de pronunciación (copiar, no inventar otras)
**ES:**
- **Cuatro tonos y neutro** (en «ma»): 1.º mā, alto y plano, como sostener una nota; 2.º má, sube, como el «¿qué?» de sorpresa; 3.º mǎ, baja y sube (al hablar rápido solo baja: «medio tercero»); 4.º mà, cae de golpe, como un «¡ya!» o una orden; neutro, sílaba breve y ligera, sin marca (ma, de). No uses la entonación española de pregunta: en chino la pregunta no sube el tono de la última sílaba.
  - Pares que cambian el sentido: mā 妈 (mamá), má 麻 (cáñamo), mǎ 马 (caballo), mà 骂 (regañar); mǎi 买 (comprar) / mài 卖 (vender); wèn 问 / wén 文; sì 四 / sǐ 死.
- **Sandhi:** dos 3.º seguidos → el primero sube (nǐ hǎo se dice «ní hǎo»); 不 bù se vuelve bú ante un 4.º (bú shì); 一 yī se vuelve yí ante 4.º (yí gè) y yì ante 1.º, 2.º y 3.º (yì bēi).
- **Aspiradas y no aspiradas:** b, d, g **no son sonoras como en español**: se dicen como la «p», «t» y «c/k» españolas de «paso», «tela», «casa», sin soplo. p, t, k llevan un soplo fuerte de aire (acerca una hoja de papel: se mueve con p, t, k y no con b, d, g). Lo mismo: z ≠ c, zh ≠ ch, j ≠ q.
- **h:** como la «j» española suave («jamón»), más ligera.
- **zh, ch, sh, r (retroflejas):** la punta de la lengua se curva hacia atrás, hacia el paladar. zh ≈ «ch» sin soplo, con la lengua atrás; ch = lo mismo con soplo; sh ≈ «sh» del inglés «she», con la lengua atrás; r = «r» del inglés «red» con zumbido, entre «sh» sonora y «r»; nunca la «r» española de «pero» ni la «rr». La «i» de zhi, chi, shi, ri no es «i»: es un zumbido de la misma consonante («shr»).
- **z, c, s:** z ≈ «ts» sin soplo («ds»); c = «ts» con soplo fuerte; s = la «s» española. Contraste con las retroflejas: sān (三) / shān (山).
- **j, q, x (solo ante i, ü):** lengua plana tras los dientes de abajo, labios en sonrisa. j ≈ «ch» suave y sin soplo (no es la «j» española); q = lo mismo con soplo, más suave que la «ch» española; x ≈ «s» suave que roza «sh» (como la «si» de «sí» con sonrisa); no es la «x» española.
- **Finales:**
  - ü: di «i» con los labios en posición de «u» (como la «u» del francés): nǚ 女, lǜ 绿. Tras j, q, x, y se escribe «u» pero suena ü (qù 去, xué 学, yuè 月); tras n y l se escribe «ü» (nǚ, lǜ).
  - -n: lengua en las encías, como la «n» de «pan» (shēn 身). -ng: la «n» de «banco» o «tengo», sin g aparte (shēng 生, zhōng 中). Pares: xīn 新 / xīng 星; fàn 饭 / fàng 放.
  - ian ≈ «ien» (tiān ≈ «tien»); yuan ≈ «üen»; iu = «iou» (jiǔ ≈ «jiou»); ui = «uei» (guì ≈ «guei»); un = «uen»; ong ≈ «ung» (dōng ≈ «dung»); e ≈ «o» con los labios estirados (hē, de); -ie, -üe ≈ «ié», «üe».
  - er (二 èr, 儿): vocal con la lengua curvada hacia atrás, como la «er» de «her» en inglés americano. La erhua (花儿 huār) se reconoce, no se exige.
- Nunca se dice que un sonido es «igual» al español si no lo es: se avisa de la diferencia (aspiración, retroflejas, j/q/x, ü).

**EN:**
- **Four tones and neutral** (on «ma»): 1st mā high and level; 2nd má rising, like «what?»; 3rd mǎ dipping (in fast speech just low); 4th mà falling sharply, like a command; neutral is short and light, no mark. Do not use English question intonation: a Chinese question does not rise on the last syllable. Pairs: mǎi 买 (buy) / mài 卖 (sell); mā 妈 / mǎ 马; sì 四 / sǐ 死.
- **Sandhi:** two 3rd tones in a row → the first becomes 2nd (nǐ hǎo is said «ní hǎo»); 不 bù becomes bú before a 4th tone; 一 yī becomes yí before a 4th and yì before 1st, 2nd and 3rd.
- **Aspirated vs. unaspirated:** b, d, g are unaspirated and voiceless, like the p, t, k in «spin», «sty», «sky» (not like English b, d, g). p, t, k are aspirated, with a strong puff of air, as in initial «pin», «tie», «kite». Same contrast: z / c, zh / ch, j / q.
- **h** like a light, raspy «h» (closer to Spanish «j» or German «ch» in «Bach»).
- **zh, ch, sh, r (retroflex):** curl the tongue tip back. zh ≈ «j» in «jam» without voicing, tongue back; ch like «ch» in «church», tongue back, with a puff; sh like «sh» in «she», tongue back; r like English «r» in «red» with a buzz. The «i» in zhi, chi, shi, ri is not «ee»: it is a buzzed continuation of the consonant.
- **z, c, s:** z ≈ «ds» in «kids» without voicing, no puff; c like «ts» in «cats» with a strong puff; s like «s» in «see». Contrast sān 三 / shān 山.
- **j, q, x (before i, ü only):** tongue flat behind the lower teeth, lips spread. j ≈ «j» in «jeep» but unvoiced and tenser; q ≈ «ch» in «cheese» with a puff; x ≈ «sh» in «she» but with the tongue flat and the lips spread.
- **Finals:** ü like the French «u» or German «ü» (say «ee» with rounded lips); it is written «u» after j, q, x, y (qù, xué) and «ü» after n, l (nǚ, lǜ). -n like «n» in «pan»; -ng like «ng» in «sing» (no separate g). ian ≈ «yen»; iu = «iou»; ui = «way»; ong ≈ «ung»; e ≈ unrounded «uh» from the back of the mouth. er like «er» in American «her» (二 èr); erhua (花儿 huār) is recognized, not required.
- Never say a sound is the «same» as in English if it is not: flag the difference (aspiration, retroflexes, j/q/x, ü).

## Gramática: lo que más falla en hispanohablantes (úsalo en `erroresFrecuentes` y distractores)
- **Tonos:** \*usar la entonación española de pregunta; \*confundir 妈 mā / 马 mǎ / 吗 ma o 买 mǎi / 卖 mài. Cada sílaba lleva su tono; el tono es parte de la palabra, como una letra.
- **是 con adjetivos:** \*我 是 高 → 我 很 高; \*她 是 漂亮 → 她 很 漂亮. 是 solo une sustantivos o equivalentes: 我 是 学生. El adjetivo funciona como verbo (adjetivo predicativo) y lleva 很 («muy» debilitado) o se niega con 不: 我 不 高. Un adjetivo suelto («我 高») suena a comparación.
- **了:** no es un «pasado». \*我 昨天 很 忙 了 → 我 昨天 很 忙 (estado pasado sin 了); \*我 每天 去 了 学校 → 我 每天 去 学校 (hábito sin 了); 了 marca acción realizada o situación nueva: 我 买 了 一 本 书; 我 累 了. Se evalúa solo cuando la clase trata 了.
- **Clasificadores:** número y demostrativo exigen clasificador: \*三 书 → 三 本 书; \*这 书 → 这 本 书; \*一 学生 → 一 个 学生; 杯 (líquidos en taza o vaso), 本 (libros), 张 (superficies planas: papel, boleto, mesa), 只 (animales), 件 (ropa, asuntos), 条 (largos: pantalón, río), 位 (personas, con respeto), 个 (comodín). El 个 comodín no sustituye a 本 ni 杯 si la clase los enseñó. No hay plural en el sustantivo: \*三 个 学生们 → 三 个 学生 (们 solo tras pronombres y personas sin número).
- **Orden tiempo-lugar-verbo:** sujeto + tiempo + lugar + verbo + objeto: \*我 学 中文 在 学校 → 我 在 学校 学 中文; \*我 去 学校 昨天 → 我 昨天 去 学校. El tiempo puede ir antes del sujeto: 明天 我 去 (variante aceptada).
- **吗 frente a palabra interrogativa:** 吗 va al final de una afirmación: 你 学 中文 吗？ Con 什么, 谁, 哪, 几 y 多少 no se usa 吗 y la palabra interrogativa ocupa el lugar de la respuesta: \*你 叫 什么 名字 吗？ → 你 叫 什么 名字？; \*你 吃 什么 吗？ → 你 吃 什么？ Se responde repitiendo el verbo o el adjetivo: «你 忙 吗？ — 忙。 / 不 忙。» (no «是»).
- **不 frente a 没:** 不 niega hábitos, presente, futuro, 是 y adjetivos: 我 不 是 学生; 我 不 喝 茶. 没(有) niega 有 y acciones ya ocurridas: \*我 不 有 钱 → 我 没有 钱; \*我 昨天 不 去 → 我 昨天 没 去. Nunca \*没 是.
- **的:** posesivo con objetos y personas ajenas: 我 的 书, 老师 的 手机; \*我 书 → 我 的 书. Con familia cercana y colectivos lo natural es sin 的: 我 妈妈, 我 家, 我们 学校 (con 的 suena forzado). Adjetivo de una sílaba + sustantivo, sin 的: 好 朋友, 大 房子; adjetivo con 很 o dos sílabas, con 的: 很 大 的 房子.
- **Posición de adverbios:** 也, 都, 很, 不 van antes del verbo o adjetivo: \*我 是 也 学生 → 我 也 是 学生; \*我们 是 都 学生 → 我们 都 是 学生; \*我 很 也 好 → 我 也 很 好.
- **«Llamarse»:** \*我 是 叫 王 芳 → 我 叫 王 芳. El apellido va primero: \*我 叫 芳 王 → 我 叫 王 芳. 贵姓 solo se dice del otro: \*我 贵姓 王 → 我 姓 王.
- **Edad:** \*我 有 二十 岁 → 我 二十 岁. Sin verbo «tener».
- **和:** solo une sustantivos: \*我 吃 饭 和 喝 水 → 我 吃 饭, 也 喝 水.
- **Verbos sin conjugar:** no hay persona, número ni tiempo en el verbo; el tiempo se marca con palabras (昨天, 明天, 已经) o con partículas. No hay artículos: 书 = libro, el libro, los libros.
- **Pinyin leído como español:** x ≠ «x», q ≠ «k», c ≠ «c», z ≠ «z», j ≠ «j», e ≠ «e», h = «j»; la «i» de shi y si no es «i»; ang, eng, ing, ong no llevan g aparte.

## Falsos amigos y transliteraciones (⚠ obligatoria, con contraste, solo estos o equivalentes igual de reales)
- **Con el español** (⚠ en `es`):
  - 四 sì (cuatro) ≠ «sí»; y 死 sǐ es «morir» (por eso 4 evita ciertos números en la cultura china).
  - 米 mǐ (arroz; también «metro») ≠ «mi».
  - 汤 tāng (sopa), 面 miàn (fideos o harina), 饭 fàn (arroz cocido; comida).
  - 小姐 xiǎojie (señorita) ≠ trato cortés: en China continental puede sonar mal con una desconocida; se usa 女士 o 您.
  - 爱人 àiren (esposo o esposa) ≠ «amante».
  - 先生 xiānsheng (señor; también «esposo»), 老师 lǎoshī (profesor o profesora de cualquier nivel).
  - 酒店 jiǔdiàn (hotel; literalmente «tienda de licor» por 酒) ≠ bar; 书房 shūfáng (cuarto de estudio) ≠ librería (书店 shūdiàn); 东西 dōngxi (cosa) ≠ 东西 dōngxī (este y oeste, con otro tono).
  - 大方 dàfang (generoso; natural) ≠ «grande y cuadrado»; 马上 mǎshàng (enseguida; literalmente «sobre el caballo») ≠ montar a caballo.
- **Solo con el inglés** (⚠ solo en `en`):
  - 同学 tóngxué (classmate) ≠ «same study»; 学院 xuéyuàn (college, institute) ≠ «academy»; 汉堡 hànbǎo (hamburger; de Hamburgo).
  - 经理 jīnglǐ (manager) ≠ «economy»; 小心 xiǎoxīn (be careful) ≠ «small heart».
- **Préstamos fonéticos (no son trampas, sin ⚠):** 咖啡 kāfēi, 沙发 shāfā, 巧克力 qiǎokèlì, 可乐 kělè, 沙拉 shālā, 酷 kù, 汉堡 hànbǎo. Se adaptan a la fonología china (sin consonantes finales ni grupos); se leen con tonos, y los caracteres elegidos suenan, no significan: no se busca sentido en ellos.
- **Jerga o registro** (哥们儿, 靠, 土豪): se marca «coloquial», sin ⚠, y no es respuesta esperada.

## Ortografía y forma (reglas duras)
- **Caracteres simplificados** siempre; cada carácter se escribe a mano con el orden de trazos estándar (de arriba abajo, de izquierda a derecha; horizontales antes que verticales cuando se cruzan; el cierre de un cuadro al final). Los trazos y radicales solo se evalúan en Nivel 0.
- **Puntuación china, de ancho completo:** 。 (punto), ， (coma), ？ (interrogación, un solo signo al final), ！ (exclamación, un solo signo al final), 、 (enumeración: 书、茶、水), ； ： y ……. No hay signo de apertura (¿ ¡). Sin espacio antes ni después de la puntuación.
- **Comillas:** “…” en el texto chino; «…» en el texto español o inglés. En `respuesta` no van comillas.
- **ü:** en pinyin se escribe «ü» solo tras n y l (nǚ, lǜ, lüè); tras j, q, x, y se escribe «u» (qù, xué, yuè). Nunca «v».
- **Mayúsculas en pinyin:** solo nombres propios y primera palabra de frase.
- **Mayúsculas en el texto de apoyo:** nombres de idiomas y gentilicios van en minúscula en español (chino, mexicano) y en mayúscula en inglés (Chinese).
- En `audio`, números, horas y fechas van en caracteres chinos (二十 块, 三 点 半, 九 月 二十五 号); sin «¥», «%», «/», «_» ni «→». El `audio` lleva solo el texto chino, sin `rom`; la app quita los espacios al leerlo.
- `aceptadas` recoge las variantes reales:
  - orden alternativo correcto (tiempo antes o después del sujeto);
  - sujeto explícito u omitido («我 是 学生。» / «是 学生。» solo si la clase lo enseñó);
  - 你 / 您 según lo fije la clase, y 谢谢 / 谢谢 你;
  - sinónimos del vocabulario de la clase (多少 钱 / 几 块 钱 solo si ambos se enseñaron).
  - Nunca se añaden variantes sin espacios, sin tonos ni en tradicional: esa tolerancia la pone la app.

## Fundamentos y Nivel 0
Las claves previas (`previos`) y los ids de Fundamentos (`zh.f0.*`) vienen en el contexto. El Nivel 0 es «Pinyin, tonos y caracteres» (4 tonos, neutro, sandhi, iniciales, finales, ü, -n/-ng, er, qué es un carácter, radicales, trazos). N1 c01 parte de lo que enseña f0: saludos (你 好, 您 好), cortesía, presentarse (我 叫…, 我 是…人), números 0–99 y 多少 钱.
