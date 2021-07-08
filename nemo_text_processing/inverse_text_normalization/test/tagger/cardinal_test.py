import unittest
import pynini
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
class TestCardinalFst(unittest.TestCase):
    graph = CardinalFst().fst
    
    def test_2_digits(self):
        cardinal = CardinalFst()
        word_list = [
            "mười",
            "mười hai",
            "mười lăm",
            "hai mươi",
            "bốn mươi lăm",
            "chín bảy",
            "ba mốt"
        ]
        for word in word_list:
            self.assertEqual(word, convert_str)
    
    def convert_str(self, s):
        return pynini.project(self.graph @ pynini.accep(s), "output")