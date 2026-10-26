import { test } from 'node:test';
import assert from 'node:assert/strict';
import { textoParaVoz } from '../src/lib/voz.js';
import { cardinalFr, ordinalFr, numerosEnPalabrasFr } from '../src/lib/numeros_fr.js';
import { cardinalEs } from '../src/lib/numeros_es.js';
import { cardinalPt } from '../src/lib/numeros_pt.js';
import { cardinaleIt } from '../src/lib/numeros_it.js';
import { cardinalRu, ordinalRu, formaPorNumero } from '../src/lib/numeros_ru.js';

const fr = (t: string) => textoParaVoz(t, 'fr');
const es = (t: string) => textoParaVoz(t, 'es');
const pt = (t: string) => textoParaVoz(t, 'pt');
const it = (t: string) => textoParaVoz(t, 'it');
const ru = (t: string) => textoParaVoz(t, 'ru');

test('francés: cardinales y ordinales', () => {
  const casos: [number, string][] = [[0, 'zéro'], [16, 'seize'], [17, 'dix-sept'], [21, 'vingt et un'], [70, 'soixante-dix'],
    [71, 'soixante et onze'], [74, 'soixante-quatorze'], [80, 'quatre-vingts'], [81, 'quatre-vingt-un'], [91, 'quatre-vingt-onze'],
    [99, 'quatre-vingt-dix-neuf'], [100, 'cent'], [200, 'deux cents'], [201, 'deux cent un'], [280, 'deux cent quatre-vingts'],
    [1000, 'mille'], [2020, 'deux mille vingt'], [1945, 'mille neuf cent quarante-cinq'], [80_000, 'quatre-vingt mille'],
    [200_000, 'deux cent mille'], [2_000_000, 'deux millions']];
  for (const [n, s] of casos) assert.equal(cardinalFr(n), s, String(n));
  assert.equal(ordinalFr(1), 'premier');
  assert.equal(ordinalFr(1, true), 'première');
  assert.equal(ordinalFr(5), 'cinquième');
  assert.equal(ordinalFr(9), 'neuvième');
  assert.equal(ordinalFr(21), 'vingt et unième');
});

test('francés: formatos que la voz leía mal', () => {
  assert.equal(fr('Il a 74 ans.'), 'Il a soixante-quatorze ans.');
  assert.equal(fr('Le train part à 2:45.'), 'Le train part à deux heures quarante-cinq.');
  assert.equal(fr('Rendez-vous à 8 h 15.'), 'Rendez-vous à huit heures quinze.');
  assert.equal(fr('à 8h30 ou à 9 h'), 'à huit heures trente ou à neuf heures');
  assert.equal(fr('après 21 h ?'), 'après vingt et une heures ?');
  assert.equal(fr('18\u202f000 personnes'), 'dix-huit mille personnes');
  assert.equal(fr('de 40\u00a0000 euros'), 'de quarante mille euros');
  assert.equal(fr('Ça coûte 96 €.'), 'Ça coûte quatre-vingt-seize euros.');
  assert.equal(fr('Le menu : 15,90 €.'), 'Le menu : quinze euros quatre-vingt-dix.');
  assert.equal(fr('Du pain : 2,50 euros.'), 'Du pain : deux euros cinquante.');
  assert.equal(fr('Or, 65 % disent non.'), 'Or, soixante-cinq pour cent disent non.');
  assert.equal(fr('Résultat : −30 %.'), 'Résultat : moins trente pour cent.');
  assert.equal(fr('le 1er mars et la 2e fois'), 'le premier mars et la deuxième fois');
  assert.equal(fr('Mon numéro : le 06 12 34 56 78.'), 'Mon numéro : le zéro six, douze, trente-quatre, cinquante-six, soixante-dix-huit.');
  assert.equal(fr('0622335567'), 'zéro six, vingt-deux, trente-trois, cinquante-cinq, soixante-sept');
  assert.equal(fr('Il est né en 1945, à Quito.'), 'Il est né en mille neuf cent quarante-cinq, à Quito.');
  assert.equal(fr('dans les années 1950-1960'), 'dans les années mille neuf cent cinquante à mille neuf cent soixante');
  assert.equal(fr('à 130 km/h sur l’autoroute'), 'à cent trente kilomètres heure sur l’autoroute');
  assert.equal(fr('réalisé 1,2 million d’euros'), 'réalisé un virgule deux million d’euros');
  assert.equal(fr('contravention n° 123'), 'contravention numéro cent vingt-trois');
  assert.equal(fr('Réunion 12/03, projet hall.'), 'Réunion douze mars, projet hall.');
  assert.equal(fr('une heure, 1 fois, 21 personnes'), 'une heure, une fois, vingt et une personnes');
});

test('francés: códigos y siglas no se tocan', () => {
  assert.equal(fr('le DELF B2 et le DALF C1'), 'le DELF B2 et le DALF C1');
  assert.equal(fr('sur l’autoroute A6, place 14B'), 'sur l’autoroute A6, place 14B');
  assert.equal(numerosEnPalabrasFr('Voir https://exemple.fr/page2024 ou www.site42.fr, 3 pages'), 'Voir https://exemple.fr/page2024 ou www.site42.fr, trois pages');
});

test('español: cardinales con apócope y género', () => {
  const casos: [number, string][] = [[0, 'cero'], [15, 'quince'], [16, 'dieciséis'], [21, 'veintiuno'], [22, 'veintidós'],
    [31, 'treinta y uno'], [100, 'cien'], [101, 'ciento uno'], [500, 'quinientos'], [1000, 'mil'], [1200, 'mil doscientos'],
    [2035, 'dos mil treinta y cinco'], [21_000, 'veintiún mil'], [1_000_000, 'un millón'], [2_500_000, 'dos millones quinientos mil']];
  for (const [n, s] of casos) assert.equal(cardinalEs(n), s, String(n));
  assert.equal(es('Tengo 21 años y 1 hermano.'), 'Tengo veintiún años y un hermano.');
  assert.equal(es('Son 21 personas en 1 hora.'), 'Son veintiuna personas en una hora.');
  assert.equal(es('Vinieron 300 personas a 412 sesiones.'), 'Vinieron trescientas personas a cuatrocientas doce sesiones.');
  assert.equal(es('¿Cuántas visitas? Las 340 al mes.'), '¿Cuántas visitas? Las trescientas cuarenta al mes.');
  assert.equal(es('En 2031 coordinaba el grupo.'), 'En dos mil treinta y uno coordinaba el grupo.');
  assert.equal(es('uno de cada 21 de ellos'), 'uno de cada veintiuno de ellos');
});

test('español: formatos que la voz leía mal', () => {
  assert.equal(es('Escribe unas 60 palabras.'), 'Escribe unas sesenta palabras.');
  assert.equal(es('Tenemos 1.200 visitas.'), 'Tenemos mil doscientas visitas.');
  assert.equal(es('Llego a las 8:15 y salgo a las 16:40.'), 'Llego a las ocho y quince y salgo a las dieciséis cuarenta.');
  assert.equal(es('a las 9:00 o a la 1:30'), 'a las nueve o a la una y treinta');
  assert.equal(es('El 82 % de los clientes.'), 'El ochenta y dos por ciento de los clientes.');
  assert.equal(es('En 2035 todo cambia.'), 'En dos mil treinta y cinco todo cambia.');
  assert.equal(es('Entre 1930–1939 hubo crisis.'), 'Entre mil novecientos treinta a mil novecientos treinta y nueve hubo crisis.');
  assert.equal(es('Cuesta 1.250,50 dólares.'), 'Cuesta mil doscientos cincuenta dólares con cincuenta.');
  assert.equal(es('Cuesta $60.'), 'Cuesta sesenta dólares.');
  assert.equal(es('El 1 de mayo es feriado.'), 'El primero de mayo es feriado.');
  assert.equal(es('la 3.ª persona y el 1.er piso'), 'la tercera persona y el primer piso');
  assert.equal(es('Mi número es 099 123 456.'), 'Mi número es cero nueve nueve, uno dos tres, cuatro cinco seis.');
  assert.equal(es('Llama al 0990000042.'), 'Llama al cero nueve nueve cero cero cero cero cero cuatro dos.');
  assert.equal(es('Llame al 911.'), 'Llame al nueve once.');
  assert.equal(es('crece un 4,8 % al año'), 'crece un cuatro coma ocho por ciento al año');
  assert.equal(es('Tengo el DELE A2 y veo el error E3.'), 'Tengo el DELE A2 y veo el error E3.');
});

test('portugués: cardinales con «e» y género', () => {
  const casos: [number, string][] = [[14, 'catorze'], [16, 'dezesseis'], [19, 'dezenove'], [100, 'cem'], [101, 'cento e um'],
    [1100, 'mil e cem'], [1250, 'mil duzentos e cinquenta'], [1999, 'mil novecentos e noventa e nove'], [2024, 'dois mil e vinte e quatro'],
    [2500, 'dois mil e quinhentos'], [4500, 'quatro mil e quinhentos'], [1_000_000, 'um milhão']];
  for (const [n, s] of casos) assert.equal(cardinalPt(n), s, String(n));
  assert.equal(cardinalPt(1200, 'f'), 'mil e duzentas');
  assert.equal(pt('São 2 pessoas e 1 hora.'), 'São duas pessoas e uma hora.');
  assert.equal(pt('Tem 400 palavras.'), 'Tem quatrocentas palavras.');
});

test('portugués: formatos que a voz lia mal', () => {
  assert.equal(pt('A nota subiu para 4,8.'), 'A nota subiu para quatro vírgula oito.');
  assert.equal(pt('O ônibus sai às 6h.'), 'O ônibus sai às seis horas.');
  assert.equal(pt('Chegamos às 5h50, hora local.'), 'Chegamos às cinco e cinquenta, hora local.');
  assert.equal(pt('das 7h às 21h'), 'das sete horas às vinte e uma horas');
  assert.equal(pt('Às 21:00, boa noite.'), 'Às vinte e uma horas, boa noite.');
  assert.equal(pt('O aluguel é R$ 4.500.'), 'O aluguel é quatro mil e quinhentos reais.');
  assert.equal(pt('O plano custa R$ 19,90.'), 'O plano custa dezenove reais e noventa centavos.');
  assert.equal(pt('Faturamos R$ 84 mil.'), 'Faturamos oitenta e quatro mil reais.');
  assert.equal(pt('Ganhamos R$ 1 mil.'), 'Ganhamos mil reais.');
  assert.equal(pt('Cerca de 60% dos alunos.'), 'Cerca de sessenta por cento dos alunos.');
  assert.equal(pt('No dia 1 de maio e no 1.º escrito.'), 'No dia primeiro de maio e no primeiro escrito.');
  assert.equal(pt('Prazo: 16/05.'), 'Prazo: dezesseis de maio.');
  assert.equal(pt('Seu protocolo é 48213907.'), 'Seu protocolo é quatro oito dois um três nove zero sete.');
  assert.equal(pt('protocolo 4521'), 'protocolo quatro cinco dois um');
  assert.equal(pt('Ingredientes: 250 g de açúcar e 1,5 xícara de leite.'), 'Ingredientes: duzentos e cinquenta gramas de açúcar e um vírgula cinco xícara de leite.');
  assert.equal(pt('Em 1630, os holandeses chegaram.'), 'Em mil seiscentos e trinta, os holandeses chegaram.');
  assert.equal(pt('O portfólio B2 tem o número REC48213.'), 'O portfólio B2 tem o número REC48213.');
});

test('italiano: cardinales y cifras con punto de miles', () => {
  const casos: [number, string][] = [[21, 'ventuno'], [23, 'ventitré'], [28, 'ventotto'], [108, 'centotto'], [180, 'centottanta'],
    [1300, 'milletrecento'], [2020, 'duemilaventi'], [21_000, 'ventunmila'], [400_000, 'quattrocentomila'], [1_000_000, 'un milione']];
  for (const [n, s] of casos) assert.equal(cardinaleIt(n), s, String(n));
  assert.equal(it('Chi spende 800 euro per una visita.'), 'Chi spende ottocento euro per una visita.');
  assert.equal(it('Il progetto costerà 400.000 euro, di cui 200.000 già disponibili.'), 'Il progetto costerà quattrocentomila euro, di cui duecentomila già disponibili.');
  assert.equal(it('90.000 euro'), 'novantamila euro');
  assert.equal(it('Ci vediamo alle 8:30.'), 'Ci vediamo alle otto e trenta.');
  assert.equal(it('Costa 12,50 euro e 1 euro di mancia.'), 'Costa dodici euro e cinquanta e un euro di mancia.');
  assert.equal(it('Il 20 % dei soci.'), 'Il venti per cento dei soci.');
});

test('ruso: cardinales, ordinales y concordancia', () => {
  assert.equal(cardinalRu(1147), 'тысяча сто сорок семь');
  assert.equal(cardinalRu(2030), 'две тысячи тридцать');
  assert.equal(cardinalRu(21_000), 'двадцать одна тысяча');
  assert.equal(cardinalRu(5_000), 'пять тысяч');
  assert.equal(cardinalRu(2, 'f'), 'две');
  assert.equal(ordinalRu(1911, 'prep'), 'тысяча девятьсот одиннадцатом');
  assert.equal(ordinalRu(2030, 'dat'), 'две тысячи тридцатому');
  assert.equal(ordinalRu(1990, 'gen'), 'тысяча девятьсот девяностого');
  assert.equal(ordinalRu(2000, 'prep'), 'двухтысячном');
  assert.equal(ordinalRu(2003, 'nom'), 'две тысячи третий');
  assert.equal(ordinalRu(1940, 'prep'), 'тысяча девятьсот сороковом');
  const pct: readonly [string, string, string] = ['процент', 'процента', 'процентов'];
  assert.deepEqual([1, 2, 4, 5, 11, 14, 21, 22, 25, 111].map((n) => formaPorNumero(n, pct)),
    ['процент', 'процента', 'процента', 'процентов', 'процентов', 'процентов', 'процент', 'процента', 'процентов', 'процентов']);
});

test('ruso: años con caso, artículos, listas y porcentajes', () => {
  assert.equal(ru('В 1911 году она отправляется в Индию.'), 'В тысяча девятьсот одиннадцатом году она отправляется в Индию.');
  assert.equal(ru('К 2030 году строительство завершится.'), 'К две тысячи тридцатому году строительство завершится.');
  assert.equal(ru('Основанный в 1147 году, город Москва очень большой.'), 'Основанный в тысяча сто сорок седьмом году, город Москва очень большой.');
  assert.equal(ru('с 1990 года до 2000 года'), 'с тысяча девятьсот девяностого года до двухтысячного года');
  assert.equal(ru('2020 год был трудным.'), 'две тысячи двадцатый год был трудным.');
  assert.equal(ru('в 2020 г. и к 2030 г.'), 'в две тысячи двадцатом году и к две тысячи тридцатому году');
  assert.equal(ru('Статья 2. Допуск.'), 'Статья вторая. Допуск.');
  assert.equal(ru('Статья 1, пункт 2, подпункт а)'), 'Статья первая, пункт второй, подпункт а)');
  assert.equal(ru('В пункте 2 нужна сфера действия. Ссылаясь на статью 2.'), 'В пункте втором нужна сфера действия. Ссылаясь на статью вторую.');
  assert.equal(ru('4 · 5 · 6 · 7'), 'четыре, пять, шесть, семь');
  assert.equal(ru('1 · 2–4 · 5–20'), 'один, от двух до четырёх, от пяти до двадцати');
  assert.equal(ru('1 %, 3 %, 5 %, 11 %, 21 %'), 'один процент, три процента, пять процентов, одиннадцать процентов, двадцать один процент');
  assert.equal(ru('Рост 2,5 %.'), 'Рост две целых пять десятых процента.');
  assert.equal(ru('Средний балл 4,8.'), 'Средний балл четыре целых восемь десятых.');
  assert.equal(ru('стоянка 45 мин.'), 'стоянка сорок пять минут.');
  assert.equal(ru('1 минута и 2 недели'), 'одна минута и две недели');
  assert.equal(ru('Поезд в 9:00, обратно в 18:05.'), 'Поезд в девять ноль-ноль, обратно в восемнадцать ноль пять.');
  assert.equal(ru('в 1990-х'), 'в тысяча девятьсот девяностых');
});

test('ja, zh, ko: la notación de patrones no deja cifras sueltas; los números se quedan', () => {
  assert.equal(textoParaVoz('N1 は N2 に 例えられる', 'ja'), 'AはBに例えられる');
  assert.equal(textoParaVoz('A 比 B 好', 'zh'), 'A比B好');
  assert.equal(textoParaVoz('N1 を N2 に 例える', 'ja'), 'AをBに例える');
  assert.equal(textoParaVoz('N1 は N2 のよう だ / みたい だ', 'ja'), 'AはBのようだ、みたいだ');
  assert.equal(textoParaVoz('V1 + V2', 'ko'), '');
  assert.equal(textoParaVoz('Adj + 게 되다', 'ko'), '게 되다.');
  assert.equal(textoParaVoz('料理 の 会 は 30 人 を 超えた。', 'ja'), '料理の会は30人を超えた。');
  assert.equal(textoParaVoz('제가 119에 신고하겠습니다', 'ko'), '제가 119에 신고하겠습니다');
  assert.equal(textoParaVoz('제3조 제2항', 'ko'), '제3조 제2항');
  assert.equal(textoParaVoz('I have 21 apples at 8:15.', 'en'), 'I have 21 apples at 8:15.');
});

test('ja: un vocablo suelto se lee con la lectura en kana que enseña el curso', () => {
  assert.equal(textoParaVoz('星 (ほし)', 'ja'), 'ほし。');
  assert.equal(textoParaVoz('星', 'ja'), 'ほし。');
  assert.equal(textoParaVoz('今日', 'ja'), 'きょう。');
  // La lectura del vocablo manda también con varios kanji: 検疫 sola salía «かんい».
  assert.equal(textoParaVoz('検疫 (けんえき)', 'ja'), 'けんえき');
  // Frases: la voz lee el kanji con su contexto.
  assert.equal(textoParaVoz('星 が きれい です。', 'ja'), '星がきれいです。');
  assert.equal(textoParaVoz('会社', 'ja'), '会社。');
  assert.equal(textoParaVoz('ありがとう (arigatou)', 'ja'), 'ありがとう');
});

test('ru: las palabras que la voz leía mal llevan el acento escrito', () => {
  assert.equal(textoParaVoz('А что говорили другие зрители в фойе?', 'ru'), 'А что говорили другие зрители в фойе́?');
  assert.equal(textoParaVoz('Фойе', 'ru'), 'Фойе́');
  assert.equal(textoParaVoz('фойе', 'es'), 'фойе');
});
