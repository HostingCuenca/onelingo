/// Contenido del Nivel 1 por idioma meta (unidades 1-6 reales; 7-20 con banco de
/// apoyo hasta que el pipeline genere el contenido definitivo).
///
/// Convención: en idiomas con escritura no latina el texto nativo lleva la
/// romanización entre paréntesis en el mismo campo: `你好 (nǐ hǎo)`.
/// En chino y japonés las frases van con espacios entre palabras (niveles 1-3).
library;

typedef Par = (String, String);
typedef BancoUnidad = ({List<Par> vocab, List<Par> frases});

/// Idiomas cuya escritura no es latina (se muestra romanización).
const idiomasNoLatinos = {'zh', 'ja', 'ko', 'ru'};

/// Idiomas que no separan palabras con espacios (las frases del banco sí lo hacen).
const idiomasSinEspacios = {'zh', 'ja'};

/// Locale de voz por idioma.
const localeVoz = {
  'en': 'en-US', 'es': 'es-ES', 'fr': 'fr-FR', 'de': 'de-DE', 'pt': 'pt-BR',
  'it': 'it-IT', 'zh': 'zh-CN', 'ja': 'ja-JP', 'ko': 'ko-KR', 'ru': 'ru-RU',
};

/// Quita la romanización "(…)" para hablar/escribir solo el texto nativo.
String soloNativo(String s) => s.replaceAll(RegExp(r'\s*\([^)]*\)'), '').trim();

BancoUnidad _b(List<Par> v, List<Par> f) => (vocab: v, frases: f);

/// Banco por idioma → unidad (1..20). Las unidades ausentes usan `_apoyo`.
final Map<String, Map<int, BancoUnidad>> _n1 = {
  'es': {
    1: _b([('Hola', 'Hola'), ('Buenos días', 'Buenos días'), ('Adiós', 'Adiós'), ('Por favor', 'Por favor'), ('Gracias', 'Gracias'), ('Me llamo', 'Me llamo')],
        [('Me llamo Ana.', 'Me llamo Ana.'), ('Mucho gusto.', 'Mucho gusto.'), ('¿Cómo estás hoy?', '¿Cómo estás hoy?')]),
  },
  'fr': {
    1: _b([('Bonjour', 'Hola / Buenos días'), ('Bonsoir', 'Buenas tardes'), ('Au revoir', 'Adiós'), ("S'il vous plaît", 'Por favor'), ('Merci', 'Gracias'), ("Je m'appelle", 'Me llamo')],
        [("Je m'appelle Ana.", 'Me llamo Ana.'), ('Enchanté.', 'Mucho gusto.'), ('Comment ça va ?', '¿Cómo estás?')]),
    2: _b([('Je', 'Yo'), ('Tu', 'Tú'), ('Il', 'Él'), ('Elle', 'Ella'), ('Nous', 'Nosotros'), ('Ils', 'Ellos')],
        [('Je suis étudiant.', 'Yo soy estudiante.'), ('Elle est mon amie.', 'Ella es mi amiga.'), ('Ils sont à la maison.', 'Ellos están en casa.')]),
    3: _b([('Lettre', 'Letra'), ('Voyelle', 'Vocal'), ('Mot', 'Palabra'), ('Son', 'Sonido'), ('Épeler', 'Deletrear'), ('Répéter', 'Repetir')],
        [('Comment ça s\'écrit ?', '¿Cómo se escribe?'), ('Répétez, s\'il vous plaît.', 'Repita, por favor.'), ('Le mot a cinq lettres.', 'La palabra tiene cinco letras.')]),
    4: _b([('Un', 'Uno'), ('Deux', 'Dos'), ('Trois', 'Tres'), ('Dix', 'Diez'), ('Vingt', 'Veinte'), ('Cent', 'Cien')],
        [('J\'ai deux frères.', 'Tengo dos hermanos.'), ('Ça coûte dix euros.', 'Cuesta diez euros.'), ('Il y a trois chaises.', 'Hay tres sillas.')]),
    5: _b([('Rouge', 'Rojo'), ('Bleu', 'Azul'), ('Vert', 'Verde'), ('Jaune', 'Amarillo'), ('Noir', 'Negro'), ('Blanc', 'Blanco')],
        [('La voiture est rouge.', 'El coche es rojo.'), ('J\'aime le bleu.', 'Me gusta el azul.'), ('Le chat est noir.', 'El gato es negro.')]),
    6: _b([('Lundi', 'Lunes'), ('Vendredi', 'Viernes'), ('Dimanche', 'Domingo'), ('Janvier', 'Enero'), ('Mois', 'Mes'), ('Aujourd\'hui', 'Hoy')],
        [('Aujourd\'hui c\'est lundi.', 'Hoy es lunes.'), ('Mon anniversaire est en janvier.', 'Mi cumpleaños es en enero.'), ('À vendredi !', '¡Hasta el viernes!')]),
  },
  'de': {
    1: _b([('Hallo', 'Hola'), ('Guten Morgen', 'Buenos días'), ('Auf Wiedersehen', 'Adiós'), ('Bitte', 'Por favor'), ('Danke', 'Gracias'), ('Ich heiße', 'Me llamo')],
        [('Ich heiße Ana.', 'Me llamo Ana.'), ('Freut mich.', 'Mucho gusto.'), ('Wie geht es dir?', '¿Cómo estás?')]),
    2: _b([('Ich', 'Yo'), ('Du', 'Tú'), ('Er', 'Él'), ('Sie', 'Ella'), ('Wir', 'Nosotros'), ('Sie (pl.)', 'Ellos')],
        [('Ich bin Student.', 'Yo soy estudiante.'), ('Sie ist meine Freundin.', 'Ella es mi amiga.'), ('Sie sind zu Hause.', 'Ellos están en casa.')]),
    3: _b([('Buchstabe', 'Letra'), ('Vokal', 'Vocal'), ('Wort', 'Palabra'), ('Laut', 'Sonido'), ('Buchstabieren', 'Deletrear'), ('Wiederholen', 'Repetir')],
        [('Wie schreibt man das?', '¿Cómo se escribe?'), ('Bitte wiederholen Sie.', 'Repita, por favor.'), ('Das Wort hat fünf Buchstaben.', 'La palabra tiene cinco letras.')]),
    4: _b([('Eins', 'Uno'), ('Zwei', 'Dos'), ('Drei', 'Tres'), ('Zehn', 'Diez'), ('Zwanzig', 'Veinte'), ('Hundert', 'Cien')],
        [('Ich habe zwei Brüder.', 'Tengo dos hermanos.'), ('Das kostet zehn Euro.', 'Cuesta diez euros.'), ('Es gibt drei Stühle.', 'Hay tres sillas.')]),
    5: _b([('Rot', 'Rojo'), ('Blau', 'Azul'), ('Grün', 'Verde'), ('Gelb', 'Amarillo'), ('Schwarz', 'Negro'), ('Weiß', 'Blanco')],
        [('Das Auto ist rot.', 'El coche es rojo.'), ('Ich mag Blau.', 'Me gusta el azul.'), ('Die Katze ist schwarz.', 'El gato es negro.')]),
    6: _b([('Montag', 'Lunes'), ('Freitag', 'Viernes'), ('Sonntag', 'Domingo'), ('Januar', 'Enero'), ('Monat', 'Mes'), ('Heute', 'Hoy')],
        [('Heute ist Montag.', 'Hoy es lunes.'), ('Mein Geburtstag ist im Januar.', 'Mi cumpleaños es en enero.'), ('Bis Freitag!', '¡Hasta el viernes!')]),
  },
  'pt': {
    1: _b([('Olá', 'Hola'), ('Bom dia', 'Buenos días'), ('Tchau', 'Adiós'), ('Por favor', 'Por favor'), ('Obrigado', 'Gracias'), ('Meu nome é', 'Me llamo')],
        [('Meu nome é Ana.', 'Me llamo Ana.'), ('Prazer em conhecer.', 'Mucho gusto.'), ('Como você está hoje?', '¿Cómo estás hoy?')]),
    2: _b([('Eu', 'Yo'), ('Você', 'Tú'), ('Ele', 'Él'), ('Ela', 'Ella'), ('Nós', 'Nosotros'), ('Eles', 'Ellos')],
        [('Eu sou estudante.', 'Yo soy estudiante.'), ('Ela é minha amiga.', 'Ella es mi amiga.'), ('Eles estão em casa.', 'Ellos están en casa.')]),
    3: _b([('Letra', 'Letra'), ('Vogal', 'Vocal'), ('Palavra', 'Palabra'), ('Som', 'Sonido'), ('Soletrar', 'Deletrear'), ('Repetir', 'Repetir')],
        [('Como se escreve?', '¿Cómo se escribe?'), ('Repita, por favor.', 'Repita, por favor.'), ('A palavra tem cinco letras.', 'La palabra tiene cinco letras.')]),
    4: _b([('Um', 'Uno'), ('Dois', 'Dos'), ('Três', 'Tres'), ('Dez', 'Diez'), ('Vinte', 'Veinte'), ('Cem', 'Cien')],
        [('Eu tenho dois irmãos.', 'Tengo dos hermanos.'), ('Custa dez reais.', 'Cuesta diez reales.'), ('Há três cadeiras.', 'Hay tres sillas.')]),
    5: _b([('Vermelho', 'Rojo'), ('Azul', 'Azul'), ('Verde', 'Verde'), ('Amarelo', 'Amarillo'), ('Preto', 'Negro'), ('Branco', 'Blanco')],
        [('O carro é vermelho.', 'El coche es rojo.'), ('Eu gosto de azul.', 'Me gusta el azul.'), ('O gato é preto.', 'El gato es negro.')]),
    6: _b([('Segunda-feira', 'Lunes'), ('Sexta-feira', 'Viernes'), ('Domingo', 'Domingo'), ('Janeiro', 'Enero'), ('Mês', 'Mes'), ('Hoje', 'Hoy')],
        [('Hoje é segunda-feira.', 'Hoy es lunes.'), ('Meu aniversário é em janeiro.', 'Mi cumpleaños es en enero.'), ('Até sexta!', '¡Hasta el viernes!')]),
  },
  'it': {
    1: _b([('Ciao', 'Hola'), ('Buongiorno', 'Buenos días'), ('Arrivederci', 'Adiós'), ('Per favore', 'Por favor'), ('Grazie', 'Gracias'), ('Mi chiamo', 'Me llamo')],
        [('Mi chiamo Ana.', 'Me llamo Ana.'), ('Piacere.', 'Mucho gusto.'), ('Come stai oggi?', '¿Cómo estás hoy?')]),
    2: _b([('Io', 'Yo'), ('Tu', 'Tú'), ('Lui', 'Él'), ('Lei', 'Ella'), ('Noi', 'Nosotros'), ('Loro', 'Ellos')],
        [('Io sono studente.', 'Yo soy estudiante.'), ('Lei è la mia amica.', 'Ella es mi amiga.'), ('Loro sono a casa.', 'Ellos están en casa.')]),
    3: _b([('Lettera', 'Letra'), ('Vocale', 'Vocal'), ('Parola', 'Palabra'), ('Suono', 'Sonido'), ('Fare lo spelling', 'Deletrear'), ('Ripetere', 'Repetir')],
        [('Come si scrive?', '¿Cómo se escribe?'), ('Ripeta, per favore.', 'Repita, por favor.'), ('La parola ha cinque lettere.', 'La palabra tiene cinco letras.')]),
    4: _b([('Uno', 'Uno'), ('Due', 'Dos'), ('Tre', 'Tres'), ('Dieci', 'Diez'), ('Venti', 'Veinte'), ('Cento', 'Cien')],
        [('Ho due fratelli.', 'Tengo dos hermanos.'), ('Costa dieci euro.', 'Cuesta diez euros.'), ('Ci sono tre sedie.', 'Hay tres sillas.')]),
    5: _b([('Rosso', 'Rojo'), ('Blu', 'Azul'), ('Verde', 'Verde'), ('Giallo', 'Amarillo'), ('Nero', 'Negro'), ('Bianco', 'Blanco')],
        [('La macchina è rossa.', 'El coche es rojo.'), ('Mi piace il blu.', 'Me gusta el azul.'), ('Il gatto è nero.', 'El gato es negro.')]),
    6: _b([('Lunedì', 'Lunes'), ('Venerdì', 'Viernes'), ('Domenica', 'Domingo'), ('Gennaio', 'Enero'), ('Mese', 'Mes'), ('Oggi', 'Hoy')],
        [('Oggi è lunedì.', 'Hoy es lunes.'), ('Il mio compleanno è a gennaio.', 'Mi cumpleaños es en enero.'), ('A venerdì!', '¡Hasta el viernes!')]),
  },
  'zh': {
    1: _b([('你好 (nǐ hǎo)', 'Hola'), ('早上好 (zǎoshang hǎo)', 'Buenos días'), ('再见 (zàijiàn)', 'Adiós'), ('请 (qǐng)', 'Por favor'), ('谢谢 (xièxie)', 'Gracias'), ('我叫 (wǒ jiào)', 'Me llamo')],
        [('我 叫 安娜。', 'Me llamo Ana. (wǒ jiào Ānnà)'), ('很 高兴 认识 你。', 'Mucho gusto. (hěn gāoxìng rènshi nǐ)'), ('你 今天 好 吗？', '¿Cómo estás hoy? (nǐ jīntiān hǎo ma)')]),
    2: _b([('我 (wǒ)', 'Yo'), ('你 (nǐ)', 'Tú'), ('他 (tā)', 'Él'), ('她 (tā)', 'Ella'), ('我们 (wǒmen)', 'Nosotros'), ('他们 (tāmen)', 'Ellos')],
        [('我 是 学生。', 'Yo soy estudiante. (wǒ shì xuésheng)'), ('她 是 我 的 朋友。', 'Ella es mi amiga. (tā shì wǒ de péngyou)'), ('他们 在 家。', 'Ellos están en casa. (tāmen zài jiā)')]),
    3: _b([('拼音 (pīnyīn)', 'Pinyin'), ('声调 (shēngdiào)', 'Tono'), ('字 (zì)', 'Carácter'), ('词 (cí)', 'Palabra'), ('读 (dú)', 'Leer'), ('重复 (chóngfù)', 'Repetir')],
        [('这个 字 怎么 读？', '¿Cómo se lee este carácter? (zhège zì zěnme dú)'), ('请 再 说 一遍。', 'Repita, por favor. (qǐng zài shuō yí biàn)'), ('汉语 有 四 个 声调。', 'El chino tiene cuatro tonos. (Hànyǔ yǒu sì gè shēngdiào)')]),
    4: _b([('一 (yī)', 'Uno'), ('二 (èr)', 'Dos'), ('三 (sān)', 'Tres'), ('十 (shí)', 'Diez'), ('二十 (èrshí)', 'Veinte'), ('一百 (yìbǎi)', 'Cien')],
        [('我 有 两 个 哥哥。', 'Tengo dos hermanos. (wǒ yǒu liǎng gè gēge)'), ('这个 十 块 钱。', 'Esto cuesta diez yuanes. (zhège shí kuài qián)'), ('有 三 把 椅子。', 'Hay tres sillas. (yǒu sān bǎ yǐzi)')]),
    5: _b([('红色 (hóngsè)', 'Rojo'), ('蓝色 (lánsè)', 'Azul'), ('绿色 (lǜsè)', 'Verde'), ('黄色 (huángsè)', 'Amarillo'), ('黑色 (hēisè)', 'Negro'), ('白色 (báisè)', 'Blanco')],
        [('车 是 红色 的。', 'El coche es rojo. (chē shì hóngsè de)'), ('我 喜欢 蓝色。', 'Me gusta el azul. (wǒ xǐhuan lánsè)'), ('猫 是 黑色 的。', 'El gato es negro. (māo shì hēisè de)')]),
    6: _b([('星期一 (xīngqīyī)', 'Lunes'), ('星期五 (xīngqīwǔ)', 'Viernes'), ('星期天 (xīngqītiān)', 'Domingo'), ('一月 (yīyuè)', 'Enero'), ('月 (yuè)', 'Mes'), ('今天 (jīntiān)', 'Hoy')],
        [('今天 是 星期一。', 'Hoy es lunes. (jīntiān shì xīngqīyī)'), ('我 的 生日 在 一月。', 'Mi cumpleaños es en enero. (wǒ de shēngrì zài yīyuè)'), ('星期五 见！', '¡Hasta el viernes! (xīngqīwǔ jiàn)')]),
  },
  'ja': {
    1: _b([('こんにちは (konnichiwa)', 'Hola'), ('おはよう (ohayō)', 'Buenos días'), ('さようなら (sayōnara)', 'Adiós'), ('おねがいします (onegai shimasu)', 'Por favor'), ('ありがとう (arigatō)', 'Gracias'), ('わたしは…です (watashi wa … desu)', 'Me llamo…')],
        [('わたし は アナ です。', 'Me llamo Ana. (watashi wa Ana desu)'), ('はじめまして。', 'Mucho gusto. (hajimemashite)'), ('きょう は げんき です か？', '¿Cómo estás hoy? (kyō wa genki desu ka)')]),
    2: _b([('わたし (watashi)', 'Yo'), ('あなた (anata)', 'Tú'), ('かれ (kare)', 'Él'), ('かのじょ (kanojo)', 'Ella'), ('わたしたち (watashitachi)', 'Nosotros'), ('かれら (karera)', 'Ellos')],
        [('わたし は がくせい です。', 'Yo soy estudiante. (watashi wa gakusei desu)'), ('かのじょ は ともだち です。', 'Ella es mi amiga. (kanojo wa tomodachi desu)'), ('かれら は いえ に います。', 'Ellos están en casa. (karera wa ie ni imasu)')]),
    3: _b([('ひらがな (hiragana)', 'Hiragana'), ('カタカナ (katakana)', 'Katakana'), ('かんじ (kanji)', 'Kanji'), ('ことば (kotoba)', 'Palabra'), ('よむ (yomu)', 'Leer'), ('もういちど (mō ichido)', 'Otra vez')],
        [('これ は なん と よみます か？', '¿Cómo se lee esto? (kore wa nan to yomimasu ka)'), ('もういちど おねがいします。', 'Otra vez, por favor. (mō ichido onegai shimasu)'), ('ひらがな は 46 もじ です。', 'El hiragana tiene 46 caracteres. (hiragana wa 46 moji desu)')]),
    4: _b([('いち (ichi)', 'Uno'), ('に (ni)', 'Dos'), ('さん (san)', 'Tres'), ('じゅう (jū)', 'Diez'), ('にじゅう (nijū)', 'Veinte'), ('ひゃく (hyaku)', 'Cien')],
        [('あに が ふたり います。', 'Tengo dos hermanos mayores. (ani ga futari imasu)'), ('これ は ひゃくえん です。', 'Esto cuesta cien yenes. (kore wa hyaku en desu)'), ('いす が みっつ あります。', 'Hay tres sillas. (isu ga mittsu arimasu)')]),
    5: _b([('あか (aka)', 'Rojo'), ('あお (ao)', 'Azul'), ('みどり (midori)', 'Verde'), ('きいろ (kiiro)', 'Amarillo'), ('くろ (kuro)', 'Negro'), ('しろ (shiro)', 'Blanco')],
        [('くるま は あかい です。', 'El coche es rojo. (kuruma wa akai desu)'), ('あお が すき です。', 'Me gusta el azul. (ao ga suki desu)'), ('ねこ は くろい です。', 'El gato es negro. (neko wa kuroi desu)')]),
    6: _b([('げつようび (getsuyōbi)', 'Lunes'), ('きんようび (kin\'yōbi)', 'Viernes'), ('にちようび (nichiyōbi)', 'Domingo'), ('いちがつ (ichigatsu)', 'Enero'), ('つき (tsuki)', 'Mes'), ('きょう (kyō)', 'Hoy')],
        [('きょう は げつようび です。', 'Hoy es lunes. (kyō wa getsuyōbi desu)'), ('たんじょうび は いちがつ です。', 'Mi cumpleaños es en enero. (tanjōbi wa ichigatsu desu)'), ('きんようび に また！', '¡Hasta el viernes! (kin\'yōbi ni mata)')]),
  },
  'ko': {
    1: _b([('안녕하세요 (annyeonghaseyo)', 'Hola'), ('좋은 아침 (joeun achim)', 'Buenos días'), ('안녕히 가세요 (annyeonghi gaseyo)', 'Adiós'), ('주세요 (juseyo)', 'Por favor (deme)'), ('감사합니다 (gamsahamnida)', 'Gracias'), ('제 이름은 (je ireumeun)', 'Mi nombre es')],
        [('제 이름은 아나예요.', 'Me llamo Ana. (je ireumeun Ana-yeyo)'), ('만나서 반갑습니다.', 'Mucho gusto. (mannaseo bangapseumnida)'), ('오늘 어떻게 지내세요?', '¿Cómo estás hoy? (oneul eotteoke jinaeseyo)')]),
    2: _b([('저 (jeo)', 'Yo'), ('당신 (dangsin)', 'Tú / usted'), ('그 (geu)', 'Él'), ('그녀 (geunyeo)', 'Ella'), ('우리 (uri)', 'Nosotros'), ('그들 (geudeul)', 'Ellos')],
        [('저는 학생이에요.', 'Yo soy estudiante. (jeoneun haksaeng-ieyo)'), ('그녀는 제 친구예요.', 'Ella es mi amiga. (geunyeoneun je chingu-yeyo)'), ('그들은 집에 있어요.', 'Ellos están en casa. (geudeureun jibe isseoyo)')]),
    3: _b([('한글 (hangeul)', 'Hangul'), ('자음 (jaeum)', 'Consonante'), ('모음 (moeum)', 'Vocal'), ('단어 (daneo)', 'Palabra'), ('읽다 (ikda)', 'Leer'), ('다시 (dasi)', 'Otra vez')],
        [('이거 어떻게 읽어요?', '¿Cómo se lee esto? (igeo eotteoke ilgeoyo)'), ('다시 말해 주세요.', 'Repita, por favor. (dasi malhae juseyo)'), ('한글은 24 글자예요.', 'El hangul tiene 24 letras. (hangeureun 24 geulja-yeyo)')]),
    4: _b([('하나 (hana)', 'Uno'), ('둘 (dul)', 'Dos'), ('셋 (set)', 'Tres'), ('열 (yeol)', 'Diez'), ('스물 (seumul)', 'Veinte'), ('백 (baek)', 'Cien')],
        [('형이 두 명 있어요.', 'Tengo dos hermanos. (hyeong-i du myeong isseoyo)'), ('이거 천 원이에요.', 'Esto cuesta mil wones. (igeo cheon won-ieyo)'), ('의자가 세 개 있어요.', 'Hay tres sillas. (uijaga se gae isseoyo)')]),
    5: _b([('빨간색 (ppalgansaek)', 'Rojo'), ('파란색 (paransaek)', 'Azul'), ('초록색 (choroksaek)', 'Verde'), ('노란색 (noransaek)', 'Amarillo'), ('검은색 (geomeunsaek)', 'Negro'), ('흰색 (huinsaek)', 'Blanco')],
        [('차가 빨간색이에요.', 'El coche es rojo. (chaga ppalgansaek-ieyo)'), ('저는 파란색을 좋아해요.', 'Me gusta el azul. (jeoneun paransaegeul joahaeyo)'), ('고양이가 검은색이에요.', 'El gato es negro. (goyangiga geomeunsaek-ieyo)')]),
    6: _b([('월요일 (woryoil)', 'Lunes'), ('금요일 (geumyoil)', 'Viernes'), ('일요일 (iryoil)', 'Domingo'), ('일월 (irwol)', 'Enero'), ('달 (dal)', 'Mes'), ('오늘 (oneul)', 'Hoy')],
        [('오늘은 월요일이에요.', 'Hoy es lunes. (oneureun woryoil-ieyo)'), ('제 생일은 일월이에요.', 'Mi cumpleaños es en enero. (je saengireun irwol-ieyo)'), ('금요일에 봐요!', '¡Hasta el viernes! (geumyoire bwayo)')]),
  },
  'ru': {
    1: _b([('Привет (privet)', 'Hola'), ('Доброе утро (dobroye utro)', 'Buenos días'), ('До свидания (do svidaniya)', 'Adiós'), ('Пожалуйста (pozhaluysta)', 'Por favor'), ('Спасибо (spasibo)', 'Gracias'), ('Меня зовут (menya zovut)', 'Me llamo')],
        [('Меня зовут Анна.', 'Me llamo Ana. (menya zovut Anna)'), ('Очень приятно.', 'Mucho gusto. (ochen priyatno)'), ('Как дела сегодня?', '¿Cómo estás hoy? (kak dela segodnya)')]),
    2: _b([('Я (ya)', 'Yo'), ('Ты (ty)', 'Tú'), ('Он (on)', 'Él'), ('Она (ona)', 'Ella'), ('Мы (my)', 'Nosotros'), ('Они (oni)', 'Ellos')],
        [('Я студент.', 'Yo soy estudiante. (ya student)'), ('Она моя подруга.', 'Ella es mi amiga. (ona moya podruga)'), ('Они дома.', 'Ellos están en casa. (oni doma)')]),
    3: _b([('Буква (bukva)', 'Letra'), ('Гласная (glasnaya)', 'Vocal'), ('Слово (slovo)', 'Palabra'), ('Звук (zvuk)', 'Sonido'), ('Читать (chitat)', 'Leer'), ('Повторить (povtorit)', 'Repetir')],
        [('Как это читается?', '¿Cómo se lee esto? (kak eto chitayetsya)'), ('Повторите, пожалуйста.', 'Repita, por favor. (povtorite, pozhaluysta)'), ('В алфавите 33 буквы.', 'El alfabeto tiene 33 letras. (v alfavite 33 bukvy)')]),
    4: _b([('Один (odin)', 'Uno'), ('Два (dva)', 'Dos'), ('Три (tri)', 'Tres'), ('Десять (desyat)', 'Diez'), ('Двадцать (dvadtsat)', 'Veinte'), ('Сто (sto)', 'Cien')],
        [('У меня два брата.', 'Tengo dos hermanos. (u menya dva brata)'), ('Это стоит сто рублей.', 'Cuesta cien rublos. (eto stoit sto rubley)'), ('Здесь три стула.', 'Hay tres sillas. (zdes tri stula)')]),
    5: _b([('Красный (krasnyy)', 'Rojo'), ('Синий (siniy)', 'Azul'), ('Зелёный (zelyonyy)', 'Verde'), ('Жёлтый (zhyoltyy)', 'Amarillo'), ('Чёрный (chyornyy)', 'Negro'), ('Белый (belyy)', 'Blanco')],
        [('Машина красная.', 'El coche es rojo. (mashina krasnaya)'), ('Мне нравится синий.', 'Me gusta el azul. (mne nravitsya siniy)'), ('Кот чёрный.', 'El gato es negro. (kot chyornyy)')]),
    6: _b([('Понедельник (ponedelnik)', 'Lunes'), ('Пятница (pyatnitsa)', 'Viernes'), ('Воскресенье (voskresenye)', 'Domingo'), ('Январь (yanvar)', 'Enero'), ('Месяц (mesyats)', 'Mes'), ('Сегодня (segodnya)', 'Hoy')],
        [('Сегодня понедельник.', 'Hoy es lunes. (segodnya ponedelnik)'), ('Мой день рождения в январе.', 'Mi cumpleaños es en enero. (moy den rozhdeniya v yanvare)'), ('До пятницы!', '¡Hasta el viernes! (do pyatnitsy)')]),
  },
};

/// Banco de apoyo por idioma para las unidades sin contenido real todavía.
final Map<String, BancoUnidad> _apoyo = {
  'es': _b([('Casa', 'Casa'), ('Familia', 'Familia'), ('Comida', 'Comida'), ('Agua', 'Agua'), ('Trabajo', 'Trabajo'), ('Tiempo', 'Tiempo')],
      [('Vivo en una casa grande.', 'Vivo en una casa grande.'), ('Quiero un café, por favor.', 'Quiero un café, por favor.'), ('Trabajo por la mañana.', 'Trabajo por la mañana.')]),
  'fr': _b([('Maison', 'Casa'), ('Famille', 'Familia'), ('Nourriture', 'Comida'), ('Eau', 'Agua'), ('Travail', 'Trabajo'), ('Temps', 'Tiempo')],
      [('J\'habite dans une grande maison.', 'Vivo en una casa grande.'), ('Je voudrais un café, s\'il vous plaît.', 'Quiero un café, por favor.'), ('Je travaille le matin.', 'Trabajo por la mañana.')]),
  'de': _b([('Haus', 'Casa'), ('Familie', 'Familia'), ('Essen', 'Comida'), ('Wasser', 'Agua'), ('Arbeit', 'Trabajo'), ('Zeit', 'Tiempo')],
      [('Ich wohne in einem großen Haus.', 'Vivo en una casa grande.'), ('Ich möchte einen Kaffee, bitte.', 'Quiero un café, por favor.'), ('Ich arbeite am Morgen.', 'Trabajo por la mañana.')]),
  'pt': _b([('Casa', 'Casa'), ('Família', 'Familia'), ('Comida', 'Comida'), ('Água', 'Agua'), ('Trabalho', 'Trabajo'), ('Tempo', 'Tiempo')],
      [('Eu moro em uma casa grande.', 'Vivo en una casa grande.'), ('Eu quero um café, por favor.', 'Quiero un café, por favor.'), ('Eu trabalho de manhã.', 'Trabajo por la mañana.')]),
  'it': _b([('Casa', 'Casa'), ('Famiglia', 'Familia'), ('Cibo', 'Comida'), ('Acqua', 'Agua'), ('Lavoro', 'Trabajo'), ('Tempo', 'Tiempo')],
      [('Vivo in una casa grande.', 'Vivo en una casa grande.'), ('Vorrei un caffè, per favore.', 'Quiero un café, por favor.'), ('Lavoro la mattina.', 'Trabajo por la mañana.')]),
  'zh': _b([('家 (jiā)', 'Casa'), ('家人 (jiārén)', 'Familia'), ('食物 (shíwù)', 'Comida'), ('水 (shuǐ)', 'Agua'), ('工作 (gōngzuò)', 'Trabajo'), ('时间 (shíjiān)', 'Tiempo')],
      [('我 住 在 大 房子。', 'Vivo en una casa grande. (wǒ zhù zài dà fángzi)'), ('请 给 我 一 杯 咖啡。', 'Un café, por favor. (qǐng gěi wǒ yì bēi kāfēi)'), ('我 早上 工作。', 'Trabajo por la mañana. (wǒ zǎoshang gōngzuò)')]),
  'ja': _b([('いえ (ie)', 'Casa'), ('かぞく (kazoku)', 'Familia'), ('たべもの (tabemono)', 'Comida'), ('みず (mizu)', 'Agua'), ('しごと (shigoto)', 'Trabajo'), ('じかん (jikan)', 'Tiempo')],
      [('おおきい いえ に すんで います。', 'Vivo en una casa grande. (ōkii ie ni sunde imasu)'), ('コーヒー を おねがいします。', 'Un café, por favor. (kōhī o onegai shimasu)'), ('あさ しごと を します。', 'Trabajo por la mañana. (asa shigoto o shimasu)')]),
  'ko': _b([('집 (jip)', 'Casa'), ('가족 (gajok)', 'Familia'), ('음식 (eumsik)', 'Comida'), ('물 (mul)', 'Agua'), ('일 (il)', 'Trabajo'), ('시간 (sigan)', 'Tiempo')],
      [('저는 큰 집에 살아요.', 'Vivo en una casa grande. (jeoneun keun jibe sarayo)'), ('커피 한 잔 주세요.', 'Un café, por favor. (keopi han jan juseyo)'), ('저는 아침에 일해요.', 'Trabajo por la mañana. (jeoneun achime ilhaeyo)')]),
  'ru': _b([('Дом (dom)', 'Casa'), ('Семья (semya)', 'Familia'), ('Еда (yeda)', 'Comida'), ('Вода (voda)', 'Agua'), ('Работа (rabota)', 'Trabajo'), ('Время (vremya)', 'Tiempo')],
      [('Я живу в большом доме.', 'Vivo en una casa grande. (ya zhivu v bolshom dome)'), ('Кофе, пожалуйста.', 'Un café, por favor. (kofe, pozhaluysta)'), ('Я работаю утром.', 'Trabajo por la mañana. (ya rabotayu utrom)')]),
};

/// Devuelve el banco (vocab, frases) de la unidad `n` del Nivel 1 para `idioma`,
/// o null si el idioma es inglés (que tiene su propio banco completo).
BancoUnidad? bancoNivel1(String idioma, int n) {
  if (idioma == 'en') return null;
  final real = _n1[idioma]?[n];
  if (real != null) return real;
  final ap = _apoyo[idioma] ?? _apoyo['es']!;
  // Rota el banco de apoyo para que cada unidad no repita exactamente el mismo orden.
  final v = [...ap.vocab.skip(n % ap.vocab.length), ...ap.vocab.take(n % ap.vocab.length)];
  final f = [...ap.frases.skip(n % ap.frases.length), ...ap.frases.take(n % ap.frases.length)];
  return (vocab: v, frases: f);
}

/// Saludo de apertura del tutor y sugerencias para el chat (Nivel 1-3).
({String apertura, List<String> sugerencias}) chatNivelBajo(String idioma) => switch (idioma) {
      'es' => (apertura: '¡Hola! Bienvenido. ¿Qué desea pedir?', sugerencias: ['Sí, por favor.', 'Quiero un café.', 'La carta, por favor.']),
      'fr' => (apertura: 'Bonjour ! Bienvenue. Vous désirez ?', sugerencias: ['Oui, s\'il vous plaît.', 'Je voudrais un café.', 'La carte, s\'il vous plaît.']),
      'de' => (apertura: 'Hallo! Willkommen. Was möchten Sie?', sugerencias: ['Ja, bitte.', 'Ich möchte einen Kaffee.', 'Die Karte, bitte.']),
      'pt' => (apertura: 'Olá! Bem-vindo. O que vai querer?', sugerencias: ['Sim, por favor.', 'Quero um café.', 'O cardápio, por favor.']),
      'it' => (apertura: 'Ciao! Benvenuto. Cosa desidera?', sugerencias: ['Sì, per favore.', 'Vorrei un caffè.', 'Il menù, per favore.']),
      'zh' => (apertura: '你好！欢迎。你 要 点 什么？ (nǐ hǎo! huānyíng. nǐ yào diǎn shénme?)', sugerencias: ['好 的 (hǎo de)', '我 要 一 杯 咖啡 (wǒ yào yì bēi kāfēi)', '请 给 我 菜单 (qǐng gěi wǒ càidān)']),
      'ja' => (apertura: 'いらっしゃいませ。ごちゅうもん は？ (irasshaimase. gochūmon wa?)', sugerencias: ['はい、おねがいします (hai, onegai shimasu)', 'コーヒー を ください (kōhī o kudasai)', 'メニュー を ください (menyū o kudasai)']),
      'ko' => (apertura: '안녕하세요! 어서 오세요. 주문하시겠어요? (annyeonghaseyo! eoseo oseyo. jumunhasigesseoyo?)', sugerencias: ['네, 주세요 (ne, juseyo)', '커피 주세요 (keopi juseyo)', '메뉴 주세요 (menyu juseyo)']),
      'ru' => (apertura: 'Здравствуйте! Что будете заказывать? (zdravstvuyte! chto budete zakazyvat?)', sugerencias: ['Да, пожалуйста (da, pozhaluysta)', 'Кофе, пожалуйста (kofe, pozhaluysta)', 'Меню, пожалуйста (menyu, pozhaluysta)']),
      _ => (apertura: 'Hello! Welcome. Are you ready to order?', sugerencias: ['Yes, please.', 'I want a coffee.', 'The menu, please.']),
    };
