#!/usr/bin/env python3
"""Pruebas de «palabra conocida» en ruso, coreano, japonés y chino
(tools/validar_ruta.py). Uso: python3 tools/test_conocida_cjk.py
Espejo en Dart: test/integridad_cjk_ru_test.dart."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validar_ruta import conocida, conocida_para, palabras  # noqa: E402


def saber(*textos):
    """Lo que enseñan unos vocablos (`texto`), como lo arma el validador."""
    return {w for t in textos for w in palabras(t)}


def todas(idioma, texto, conocidas):
    prueba = conocida_para(idioma)
    return [w for w in palabras(texto) if not prueba(w, conocidas)]


class Japones(unittest.TestCase):
    def test_conocida(self):
        s = saber("わたし", "は", "がくせい", "です")
        self.assertEqual(todas("ja", "わたし は がくせい です。", s), [])

    def test_particula_suelta_debe_ensenarse(self):
        s = saber("わたし", "がくせい", "です")
        self.assertEqual(todas("ja", "わたし は がくせい です。", s), ["は"])

    def test_sin_segmentar(self):
        # Sin espacios no se adivina la partición.
        s = saber("わたし", "は", "がくせい", "です")
        self.assertEqual(todas("ja", "わたしはがくせいです。", s), ["わたしはがくせいです"])

    def test_puntuacion(self):
        self.assertEqual(palabras("「すみません」、『にほん』・マリア（メキシコ）です か？！"),
                         ["すみません", "にほん", "マリア", "メキシコ", "です", "か"])

    def test_vocablo_con_lectura(self):
        s = saber("日本 (にほん)", "何 (なに, なん)")
        self.assertTrue({"日本", "にほん", "何", "なに", "なん"} <= s)
        self.assertEqual(todas("ja", "にほん", s), [])


class Chino(unittest.TestCase):
    def test_conocida(self):
        s = saber("我", "是", "学生")
        self.assertEqual(todas("zh", "我 是 学生。", s), [])

    def test_no_conocida(self):
        s = saber("我", "是")
        self.assertEqual(todas("zh", "我 是 老师。", s), ["老师"])

    def test_particula_suelta(self):
        s = saber("你", "好")
        self.assertEqual(todas("zh", "你 好 吗？", s), ["吗"])

    def test_puntuacion(self):
        self.assertEqual(palabras("书、茶，“水”：（好）；对！"), ["书", "茶", "水", "好", "对"])
        self.assertEqual(todas("zh", "书、茶。", saber("书", "茶")), [])


class Coreano(unittest.TestCase):
    S = saber("저", "학생", "은", "는", "이에요", "서울", "에", "에서", "자다 (자요)")

    def test_eojeol_tal_cual(self):
        self.assertEqual(todas("ko", "자요.", self.S), [])
        self.assertEqual(todas("ko", "자다", self.S), [])

    def test_particula_pegada(self):
        self.assertEqual(todas("ko", "저는 학생이에요.", self.S), [])
        self.assertEqual(todas("ko", "서울에서 자요?", self.S), [])
        self.assertEqual(todas("ko", "서울에는", self.S), [])

    def test_particula_no_ensenada(self):
        # 을 no se enseñó; 도 tampoco (서울에도).
        self.assertEqual(todas("ko", "학생을 서울에도", self.S), ["학생을", "서울에도"])

    def test_raiz_no_ensenada_y_verbo_no_ensenado(self):
        self.assertEqual(todas("ko", "의사는 먹어요.", self.S), ["의사는", "먹어요"])
        # Conjugación distinta de la enseñada: no se deduce.
        self.assertEqual(todas("ko", "잤어요", self.S), ["잤어요"])

    def test_sin_descomponer_ni_doble_particula_libre(self):
        # 학생이가: dos partículas de caso seguidas no cuentan.
        s = self.S | {"이", "가"}
        self.assertEqual(todas("ko", "학생이가", s), ["학생이가"])

    def test_puntuacion(self):
        self.assertEqual(palabras("«저는 학생이에요?»"), ["저는", "학생이에요"])

    def test_numeros_sinocoreanos_compuestos(self):
        # Cada dígito y multiplicador enseñado: el número compuesto vale.
        n = saber("일", "이", "삼", "오", "공", "십", "천", "만")
        for w in ("이십", "십일", "삼천", "십만", "삼십오만", "공일공"):
            self.assertEqual(todas("ko", w, n), [], w)
        # Dos dígitos seguidos sin multiplicador (오삼) no son un número; a 이백 le falta 백.
        self.assertEqual(todas("ko", "오삼", n), ["오삼"])
        self.assertEqual(todas("ko", "이백", n), ["이백"])


class Ruso(unittest.TestCase):
    def test_conocida(self):
        s = saber("я", "читать — прочитать", "книга")
        self.assertEqual(todas("ru", "Я читать книга.", s), [])

    def test_flexion_solo_si_se_enseno(self):
        s = saber("читать — прочитать", "книга")
        self.assertEqual(todas("ru", "читаю книгу", s), ["читаю", "книгу"])
        s = saber("читать (читаю)", "книга (книгу)")
        self.assertEqual(todas("ru", "читаю книгу", s), [])

    def test_e_con_dieresis_y_acento(self):
        s = saber("ещё", "всё")
        self.assertEqual(todas("ru", "Еще все.", s), [])
        s = saber("еще")
        self.assertEqual(todas("ru", "Ещё ещ́е", s), [])

    def test_puntuacion_y_guion(self):
        s = saber("по-русски", "анна", "врач")
        self.assertEqual(todas("ru", "Анна — врач! «По-русски»?", s), [])
        self.assertEqual(todas("ru", "Анна — доктор.", s), ["доктор"])


class SinMorfologiaInglesa(unittest.TestCase):
    def test_solo_idiomas_registrados(self):
        self.assertIs(conocida_para("en"), conocida)
        for idioma in ("ru", "ko", "ja", "zh"):
            self.assertIsNot(conocida_para(idioma), conocida)
        # La regla inglesa quitaría la «s» final; aquí no.
        self.assertFalse(conocida_para("ru")("книгаs", {"книга"}))


if __name__ == "__main__":
    unittest.main()
