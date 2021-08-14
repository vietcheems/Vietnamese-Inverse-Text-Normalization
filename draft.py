import pynini
import pywrapfst
import sys
import time
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
from pynini.lib.rewrite import rewrites
from nemo_text_processing.inverse_text_normalization.taggers.decimal import DecimalFst
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer

# graph = DecimalFst(cardinal=CardinalFst()).fst
# print(InverseNormalizer().inverse_normalize("năm nghìn bảy trăm bốn bốn chấm bảy ba một", verbose=True))
# print(rewrites("không phẩy hai", graph))