import pynini
import sys
from nemo_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer

print(InverseNormalizer().inverse_normalize("hai hai hai blah một tỷ blah blah hai phần ba blah blo hai nghìn phẩy tám", verbose=True))
