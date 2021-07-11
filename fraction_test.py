import unittest
import pynini
from nemo_text_processing.inverse_text_normalization.verbalizers.fraction import FractionFst
from pynini.lib.rewrite import rewrites

if __name__ == "__main__":
	print(rewrites("fraction { numerator: \"24\" denominator: \"7\" }", FractionFst().fst))
