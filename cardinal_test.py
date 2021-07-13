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
            "bốn lăm",
            "trừ một tỷ chín triệu sáu trăm nghìn ba trăm hai mốt",
            "trừ một tỷ chín triệu sáu trăm nghìn ba trăm hai mốt",
            "một nghìn tỷ",
            "một nghìn tỷ tỷ",
            "chín trăm chín chín nghìn tỷ tỷ"
        ]
        for word in word_list:
            print(word + " | " + top_rewrite(word, self.graph))

if __name__ == "__main__":
    TestCardinalFst().test_2_digits()
