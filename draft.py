import pynini
import pywrapfst
import sys
import time
from pynini.lib.rewrite import rewrites
from nemo_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer

print(InverseNormalizer().inverse_normalize("hai rưỡi ngày mùng một tháng hai năm hai không hai mươi", verbose=True))
