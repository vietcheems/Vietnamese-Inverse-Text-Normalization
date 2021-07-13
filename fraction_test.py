import unittest
import pynini
from nemo_text_processing.inverse_text_normalization.verbalizers.fraction import FractionFst as V
from nemo_text_processing.inverse_text_normalization.taggers.fraction import FractionFst as T
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from pynini.lib.rewrite import rewrites

if __name__ == "__main__":
	# print(rewrites("fraction { numerator: \"24\" denominator: \"7\" }", FractionFst().fst))
	# print(rewrites("hai phần âm ba", FractionFst(CardinalFst()).fst))
	s = "âm hai phần bốn"
	s = rewrites(s, T(CardinalFst()).fst)[0]
	print(s)
	s = rewrites(s, V().fst)[0]
	print(s)
