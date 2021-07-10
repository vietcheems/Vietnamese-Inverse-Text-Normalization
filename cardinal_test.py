import unittest
import pynini
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from pynini.lib.rewrite import top_rewrite
class TestCardinalFst(unittest.TestCase):
    graph = CardinalFst().fst
    
    def test_2_digits(self):
        cardinal = CardinalFst()
        word_list = [
            "âm hai",
            "mười hai",
            "mười lăm",
            "hai mươi",
            "bốn mươi lăm",
            "chín bảy",
            "âm ba mốt",
            "hai năm"
        ]
        for word in word_list:
            print(word + " | " + top_rewrite(word, self.graph))

if __name__ == "__main__":
    TestCardinalFst().test_2_digits()
