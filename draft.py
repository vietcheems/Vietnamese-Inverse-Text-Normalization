import pynini
import pywrapfst
import sys
import time
from pynini.lib.rewrite import rewrites
from nemo_text_processing.inverse_text_normalization.taggers.decimal import DecimalFst
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer

# graph = DecimalFst(cardinal=CardinalFst()).fst
print(InverseNormalizer().inverse_normalize("không chấm hai mươi", verbose=True))
# print(rewrites("không phẩy hai", graph))