# Ficha de idioma: japonés (ja)

Esta ficha se inserta en todos los prompts de `tools/ia/prompts/`. Es la única fuente de reglas propias del japonés.

## Alumno y variedad
- **Alumno:** adulto hispanohablante de EE. UU. o Latinoamérica.
- **Idiomas de apoyo:** español latino neutro con «tú» (ustedes, celular, carro o auto, computadora, departamento, manejar, boleto, jugo, papa, lentes) e inglés americano.
- **Japonés estándar** (hyōjungo, base de Tokio). Sin dialectos (kansai-ben y otros) como respuesta esperada; solo para comprensión, desde N8.
- **Examen de referencia:** JLPT (N5 → N1). La c50 de cada nivel imita el formato del JLPT de su nivel, sin nombrar marcas en las consignas.
- **Registro por defecto:** cortés, です/ます (teineigo) en todo el contenido. La forma llana (diccionario, た, ない) solo aparece cuando la clase la enseña, y se avisa de que es «llana, con amigos y familia».

## Escritura por nivel (fija)
- **Fundamentos y N1–N2:** solo hiragana y katakana.
  - Kanji únicamente en este puñado de palabras muy frecuentes, cada una enseñada explícitamente como entrada de vocabulario con su lectura en kana: 日本 (にほん), 人 (じん, ひと), 私 (わたし), 先生 (せんせい), 学生 (がくせい), 円 (えん), 水 (みず), 駅 (えき), 何 (なに, なん), 今 (いま).
  - En Fundamentos (`ja.f0.*`) no hay ningún kanji: todo va en kana.
  - Una palabra con kanji aún no enseñado se escribe en kana.
- **N3–N4:** kanji progresivo hasta ≈ 100 (nivel JLPT N5). **N5–N6:** hasta ≈ 300 (JLPT N4). **N7–N8:** hasta ≈ 650 (JLPT N3). **N9–N10:** hasta ≈ 1000, sin salir de lo enseñado.
  - Cada kanji entra primero en una entrada de vocabulario con su lectura en kana (campo `lectura`); después puede usarse en cualquier texto.
  - Los apellidos y ciudades de la lista cerrada pasan a kanji solo cuando todos sus kanji están enseñados. Los nombres de pila se quedan siempre en hiragana.
- **`rom`** (rōmaji Hepburn modificado):
  - N1–N4: toda palabra nueva y todo ejemplo de vocabulario llevan `rom`, y el texto japonés de los ejercicios puede ofrecer `rom` como ayuda.
  - Desde N5: `rom` solo en las entradas de vocabulario. Nunca en el texto de ejercicios.
  - Hepburn modificado:
    - Vocales largas con macrón: ā, ū, ē, ō. おう y おお → ō; ええ → ē; うう → ū; ああ → ā. いい → ii; えい → ei (sensei, no sensē). La ー del katakana alarga la vocal anterior (ビール bīru, コーヒー kōhī).
    - し shi, ち chi, つ tsu, ふ fu, じ ji, しゃ sha, ちゃ cha, じゃ ja. っ dobla la consonante siguiente (kitte, zasshi) y ante ch es tch (matcha).
    - ん siempre n, también ante b/m/p (shinbun, sanpo). Ante vocal o y lleva apóstrofo recto: kin'en, hon'ya.
    - Partículas según se pronuncian: は wa, へ e, を o.
    - Minúscula salvo inicio de frase y nombres propios.
- Cifras arábigas: no se escriben en texto japonés en N1–N2 (los números van en kana: ごひゃくえん). Desde N3 pueden verse en pantalla, pero nunca en `audio`.

## Separación de palabras (crítico)
En todo el contenido, **el texto japonés se escribe con un espacio entre palabras y las partículas como palabra aparte**: «わたし は がくせい です。». La app quita los espacios al leerlo en voz alta. En `ordenar`, los tokens son esas palabras. Reglas de partición:
- **Palabra aparte:** cada sustantivo, pronombre, adjetivo, adverbio, verbo conjugado y partícula (は, が, を, に, で, へ, と, も, の, か, ね, よ, から, まで, より), además de です, でした y ありません.
- **Pegado a su palabra (una sola):**
  - sufijos de persona y de lugar: さん, せんせい tras el nombre cuando es tratamiento (たなかさん, やまもとせんせい), 〜じん (メキシコじん), 〜ご (にほんご);
  - contadores y unidades a su número (さんにん, じゅうごさい, ごひゃくえん);
  - la forma ます completa (たべます, たべません, たべました, たべませんでした);
  - un adjetivo い con su negación o pasado (おおきくない, おおきかった); luego です va aparte («おおきくない です»);
  - じゃない es una sola palabra («がくせい じゃない です»).
- **Palabras separadas:** です y でした siguen a su palabra con espacio («がくせい です», «がくせい でした»); じゃ ありません son dos palabras; て-forma y su auxiliar son dos palabras («たべて います», «みて ください»); ありがとう ございます y おはよう ございます son dos palabras.
- **Expresiones fijas** muy cortas que se aprenden de golpe (こんにちは, こんばんは, さようなら, すみません, ごめんなさい, おやすみなさい, おねがいします, どういたしまして, はじめまして) son una palabra.
- **Puntuación pegada** a la palabra anterior, sin espacio antes: «です。», «です か？», «みなさん、». Tras 、 y tras 。 se deja un espacio, como entre cualquier palabra. Nunca espacio antes de 。 、 ？ ！. La か de pregunta es palabra aparte («です か？»).
- Ningún token pasa de unas 9 moras salvo nombres propios.

## Tratamiento y registro
- **«Tú» y «usted» = nombre + さん** (たなかさん, ゆきさん), o el cargo: せんせい, しゃちょう. Evita **あなた** al hablarle a alguien: suena distante o brusco con desconocidos y, entre pareja, íntimo. Solo se explica como «existe, pero no lo uses», y no aparece en diálogos.
  - Si no sabes el nombre, **omite** el sujeto; el japonés no lo necesita.
  - **Nunca さん para ti mismo ni para tu familia:** «たなか です» y no *«たなかさん です».
- **«Ustedes» = みなさん.** **«Nosotros» = わたしたち.** **«Yo» = わたし** (neutro, para cualquier género; ぼく y おれ no se enseñan).
- かれ y かのじょ significan también «novio» y «novia»: no sirven de «él/ella» neutro; se usa el nombre + さん.
- くん y ちゃん solo cuando la clase los enseñe; en Fundamentos solo さん.
- El sujeto y el tema obvios se **omiten** (ver gramática).

## Nombres y lugares (lista cerrada)
- **Personas** (nombre en hiragana, `rom`, orden japonés: apellido + nombre):
  - **Femeninos (8):** さくら Sakura, ゆき Yuki, あおい Aoi, めぐみ Megumi, ようこ Yōko, みさき Misaki, あやか Ayaka, ななこ Nanako.
  - **Masculinos (7):** けんた Kenta, たくや Takuya, ゆうた Yūta, だいすけ Daisuke, りょう Ryō, しょうた Shōta, ひろし Hiroshi.
  - **Apellidos (10):** たなか Tanaka (田中), すずき Suzuki (鈴木), わたなべ Watanabe (渡辺), たかはし Takahashi (高橋), いとう Itō (伊藤), やまもと Yamamoto (山本), なかむら Nakamura (中村), こばやし Kobayashi (小林), かとう Katō (加藤), よしだ Yoshida (吉田). No uses apellidos que sean palabras corrientes (さとう «azúcar», はやし «bosque»).
  - Fórmulas: «たなかさん», «やまもとせんせい», «すずきさん は かいしゃいん です».
  - Si no, se usa el papel en japonés: «てんいん», «かいしゃいん», «せんせい», «がくせい».
  - Un nombre no pasa de una clase a otra: no hay historia ni reparto.
- **Ciudades (10):** とうきょう Tōkyō (東京), おおさか Ōsaka (大阪), きょうと Kyōto (京都), なごや Nagoya (名古屋), ふくおか Fukuoka (福岡), さっぽろ Sapporo (札幌), よこはま Yokohama (横浜), こうべ Kōbe (神戸), ひろしま Hiroshima (広島), せんだい Sendai (仙台). Sin datos verificables (ni líneas de tren, direcciones, precios reales ni comercios reales).
  - Lugares genéricos: «えき», «ぎんこう», «ゆうびんきょく», «コンビニ», «びょういん».
- **Países permitidos** (katakana o hiragana): メキシコ, コロンビア, アルゼンチン, チリ, ペルー, スペイン, アメリカ, にほん, イタリア, スイス. Gentilicio: país + じん (メキシコじん, にほんじん).
  - **Nunca Ecuador, Quito, Guayaquil, Cuenca ni «ecuatoriano»**, en ningún idioma ni campo.

## Guías de pronunciación (copiar, no inventar otras)
**ES:**
- **5 vocales**, siempre puras, sin diptongar y sin reducirse: あ «a» de «casa»; い «i» de «ir»; う «u» con los labios sin redondear ni proyectar (menos «u» que la española); え «e» de «mesa»; お «o» de «foto».
- **Moras:** cada kana es un golpe de igual duración. きょ es un golpe, きよ son dos. ん, っ y la vocal larga cuentan un golpe cada uno. No hay sílaba tónica fuerte como en español.
- **Vocales largas** = dos golpes: おばさん «tía» ≠ おばあさん «abuela»; おじさん ≠ おじいさん; ビル «edificio» ≠ ビール «cerveza»; ゆき «nieve» ≠ ゆうき «valor». Se escriben con la vocal repetida en hiragana (おう suena «oo», えい suena «ee») y con ー en katakana.
- **っ** (consonante doble): pausa de un golpe antes de k, s, t, p, con la consonante «sostenida»: さか «cuesta» ≠ さっか «escritor»; きて ≠ きって «sello». El español no tiene este sonido; se avisa de que dura.
- **ん:** un golpe propio, nasal. Ante p, b, m suena «m»; ante k, g suena «ng» de «banco»; ante t, d, n, r, s, z suena «n»; al final de palabra y ante vocal es nasal sin llegar a «ne».
- **r japonesa** (ら り る れ ろ): una «r» simple y rápida, la de «pero» o «aro». Nunca la «rr» vibrante múltiple de «perro», ni «l», ni «d» inglesa. Entre «r» y «d» suave.
- **ふ** no es «fu» con los dientes sobre el labio: se sopla el aire entre los dos labios, como al apagar una vela (entre «fu» y «ju»).
- **つ** = «tsu» en una sola sílaba (como el inicio de «tsunami»); nunca «tu» ni «chu». **ち** «chi» de «chico». **し** «shi»: «sh» inglesa, no «si». **じ** y **ぢ** «yi» fuerte (como «ye» en «yeso» muy tenso). **ず** y **づ** «dsu».
- **Ensordecimiento:** i y u entre consonantes sordas o al final tras sorda casi no suenan: です «des», ます «mas», すき «ski», ひとつ «htotsu». Solo se avisa; no se evalúa por escrito.
- **Acento tonal:** el japonés usa alto/bajo en vez de intensidad. はし «palillos» (alto-bajo) ≠ はし «puente» (bajo-alto); あめ «lluvia» ≠ あめ «caramelo». Solo como conciencia: no se marca en el texto ni se evalúa.
- **Partículas:** は se lee «wa», へ se lee «e», を se lee «o» solo como partícula.

**EN:**
- **5 pure vowels**, never reduced to «uh»: あ «a» as in «father»; い «ee» as in «see» but shorter; う «oo» but with unrounded lips; え «e» as in «bed»; お «o» as in «more», without the glide.
- **Moras:** every kana is one equal beat. きょ is one beat, きよ is two. ん, っ and a long vowel each take one beat. There is no heavy stressed syllable.
- **Long vowels** take two beats and change meaning: おばさん «aunt» / おばあさん «grandmother»; ビル «building» / ビール «beer».
- **っ** (double consonant): hold the closure for one beat, as in «hot-tub» but longer: さか / さっか, きて / きって.
- **ん:** its own beat, nasal. Like «m» before p, b, m; like «ng» in «sing» before k, g; like «n» elsewhere.
- **Japanese r:** a quick tap, like the tt in American «butter» or «ladder». Not an English r, not a trilled rr.
- **ふ** is not «foo»: blow air between both lips, as if blowing out a candle. **つ** is «tsu» as in «cats». **し** «shi». **ち** «chi». **じ** «ji».
- **Devoicing:** i and u between voiceless consonants or at the end after one are nearly silent: です «des», ます «mas». Awareness only.
- **Pitch accent:** high/low pitch, not stress: はし «chopsticks» / はし «bridge»; あめ «rain» / あめ «candy». Awareness only: not marked, not tested.
- **Particles:** は is read «wa», へ is read «e», を is read «o» only as a particle.

Nunca se dice que un sonido es «igual» al español si no lo es: se avisa de la diferencia (う, r, ふ, つ, ん, vocales largas, っ).

## Ortografía y forma (reglas duras)
- **Puntuación japonesa de ancho completo:** 。 (fin de enunciado), 、 (pausa, tras expresiones de tiempo y entre cláusulas), ？ (fin de pregunta, tras か), ！ (exclamación), 「…」 (comillas dentro del japonés). Nunca «.», «,», «?», «!» ASCII dentro del texto japonés, ni espacio de ancho completo (U+3000).
- Comillas en el español de apoyo: «…» (caporali). En `respuesta` no van comillas.
- **Katakana** para préstamos (コーヒー, ホテル, テレビ), nombres extranjeros, países y ciudades extranjeras. En katakana la vocal larga se escribe con **ー** (chōon): コーヒー, ケーキ, ラーメン; nunca con la vocal repetida (no *コオヒイ). En hiragana la vocal larga se escribe con vocales (おかあさん, おとうさん, ありがとう).
- っ y ゃゅょ pequeños siempre pequeños; ッ y ャュョ también en katakana (ベッド, シャツ).
- Katakana extendido (ファ, ティ, ウィ, チェ) solo cuando la clase lo enseñe.
- Pares dakuten/handakuten bien escritos: ば ぱ, じ ぢ, ず づ (ぢ y づ casi nunca; se enseñan solo como curiosidad).
- Partícula **は** (se lee «wa») y **を** (se lee «o») y **へ** (se lee «e») se escriben con su kana de partícula, no con わ, お, え.
- En `audio`, números, precios y horas se escriben en kana, nunca en cifras ni con «円»: «ごひゃくえん», «じゅうごさい». Nunca se escriben «¥», «%», «/», «_» ni «→» en el audio. Los espacios del audio los quita la app.
- Nombre completo: apellido y luego nombre («たなか さくら», «すずき ゆうた»); con tratamiento, «たなかさん» (sin espacio). El nombre de pila solo, «さくらさん».
- `aceptadas` recoge las variantes reales:
  - sujeto explícito u omitido («がくせい です» / «わたし は がくせい です»);
  - じゃない です ↔ じゃ ありません;
  - orden alternativo correcto de elementos (tiempo / lugar / objeto) solo si el verbo sigue al final;
  - kana de lectura equivalente (ゼロ ↔ れい, よん ↔ し, なな ↔ しち, きゅう ↔ く) solo cuando la clase las enseña como alternativas.
  - Nunca se añaden variantes con rom, ni con otra forma de escribir el mismo kana: esa tolerancia la pone la app.

## Gramática: lo que más falla en hispanohablantes (úsalo en `erroresFrecuentes` y distractores)
- **は frente a が:** は marca el tema («de eso hablamos»): «わたし は がくせい です». が marca el sujeto nuevo o con pregunta (だれ が, すき, あります) y no aparece en Fundamentos. *«これ が ほん です» → «これ は ほん です». Cuando llegue が, el error típico es usarlo siempre porque «el sujeto se marca».
- **Partículas を / に / で / へ:**
  - を = objeto directo: *«コーヒー に のみます» → «コーヒー を のみます».
  - に = destino, tiempo puntual, lugar de existencia: «がっこう に いきます», «うち に います».
  - で = lugar de la acción o medio: «レストラン で たべます», *«レストラン に たべます».
  - へ = dirección (= に de destino). No se evalúa la diferencia entre に y へ.
  - Los hispanohablantes traducen «en» y «a» a una sola preposición: *«うち で います» → «うち に います».
- **Orden SOV:** el verbo (o です) va **al final**, siempre. *«です わたし がくせい» → «わたし は がくせい です». Los adjetivos y las cláusulas van antes del sustantivo: «あたらしい くるま», no *«くるま あたらしい» como modificador.
- **Contadores:**
  - No se dice un número suelto: «りんご を さんこ», no *«りんご を さん».
  - Contador por forma: にん (personas), さい (años), まい (cosas planas), こ (cosas pequeñas), ほん (cosas largas), だい (máquinas).
  - Irregulares: ひとり, ふたり (personas); ひとつ, ふたつ, みっつ (cosas); さんぼん, ろっぽん (cosas largas).
- **Omitir sujeto:** el hispanohablante tiende a llenar «わたし» en cada frase (como el inglés) o a olvidar el tema nuevo. Lo natural: «（わたし は） がくせい です»; se omite lo obvio.
- **«ser» y «estar»:** です es solo «ser/es» de identidad y atributo. «Estar/hay» de ubicación usa います (seres vivos) y あります (cosas): no se enseña en Fundamentos.
- **Sin artículos, género ni plural:** *«これ は una ほん»: se omiten. «ほん» sirve para uno y para varios; el plural se infiere o se usa un contador.
- **Vocales largas y っ:** olvidar la duración cambia la palabra: おばさん / おばあさん, ここ / こうこう. Se evalúan solo cuando la clase trata la duración.
- **ん:** pronunciada como sílaba con vocal («ほんや» → *«ほなや») se oye mal; no se evalúa por escrito.
- **Registro:**
  - mezclar です/ます y forma llana en la misma frase: *«たべる ます», *«いく です» → «いきます»;
  - usar «ありがとう» (llano) con un desconocido en vez de «ありがとう ございます»;
  - *«たなかさん です» al presentarse a uno mismo → «たなか です»;
  - あなた al hablar con alguien.
- **Calcos léxicos:** *«おはよう» por la tarde (se dice «こんにちは»); *«すみません» como «lo siento» en todo (también «gracias» y «disculpe»).
- **Pregunta sin か:** *«これ は ほん です？» → «これ は ほん です か？». La entonación sola solo vale en lenguaje llano.

## Falsos amigos (⚠ obligatoria, con contraste, solo estos o equivalentes igual de reales)
Son **wasei-eigo** o préstamos que cambiaron de sentido:
- **Con el español y con el inglés** (⚠ en `es` y en `en`):
  - マンション (departamento/condominio de concreto ≠ mansión), アパート (departamento pequeño, a menudo de madera ≠ apartamento de lujo), ノート (cuaderno ≠ nota).
  - サイン (firma, autógrafo ≠ señal), コンセント (enchufe ≠ consentimiento), ハンドル (volante ≠ asa), ガソリンスタンド (gasolinera).
  - クレーム (queja ≠ reclamo legal), スマート (delgado ≠ inteligente), ナイーブ (sensible ≠ ingenuo).
  - テンション (ánimo, energía ≠ tensión), ストーブ (calefactor), ホッチキス (engrapadora), シール (calcomanía).
  - バイキング (buffet ≠ vikingo), ワンピース (vestido ≠ una pieza), パンツ (ropa interior o pantalón), リフォーム (remodelar ≠ reformar una ley).
  - カンニング (copiar en un examen ≠ astucia), ライブ (concierto en vivo), サービス (algo gratis o atención ≠ servicio genérico).
- **Solo con el inglés** (⚠ solo en `en`): トランプ (naipes ≠ Trump), アルバイト (trabajo de medio tiempo, del alemán), ドライブスルー (se escribe igual).
- **No son falsos amigos** (sin ⚠): パン, ボタン, テレビ, ホテル, レストラン, コーヒー, テーブル, カメラ, タクシー, ビール. Se explican como préstamos fieles.
- **Jerga o registro** (やばい, マジ, めっちゃ, うまい «delicioso, para hombres»): se marca «coloquial», sin ⚠.

## Fundamentos y Nivel 0
Las claves previas (`previos`) y los ids de Fundamentos (`ja.f0.*`) vienen en el contexto. N1 c01 parte de lo que enseña f0: saludos, cortesía, presentarse, はです, números 0–20, これ・それ・あれ, か y の. Nivel 0 «Leer y pronunciar japonés» enseña hiragana por filas (vocales, k, s, t, n, h, m, y, r, w, ん), dakuten y handakuten, combinaciones ゃゅょ, っ, vocales largas, katakana básica y préstamos, y acento tonal como conciencia. Todo el Nivel 0 y Fundamentos va en kana, sin kanji.
