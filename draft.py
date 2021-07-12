import pynini
import sys
from nemo_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer

print(InverseNormalizer().inverse_normalize("hai ba hai", verbose=True))
