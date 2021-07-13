import unittest
import pynini
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from pynini.lib.rewrite import top_rewrite
class TestCardinalFst(unittest.TestCase):
    graph = CardinalFst().fst
    leading_zero = CardinalFst().remove_leading_zero_graph
    
    def test_2_digits(self):
        cardinal = CardinalFst()
        word_list = [
            "âm hai",
            "bốn lăm",
            "trừ một tỷ chín triệu sáu trăm nghìn ba trăm hai mốt",
            "một trăm",
            "chín trăm chín chín nghìn tỷ tỷ",
            # "000 100 000"
        ]
        for word in word_list:
            print(word + " | " + top_rewrite(word, self.graph))
            # print(top_rewrite(word, self.leading_zero))

if __name__ == "__main__":
    TestCardinalFst().test_2_digits()
