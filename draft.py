import pynini
import sys
from nemo_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer

print(InverseNormalizer().inverse_normalize("hai triệu all the way baby hai tư trên bảy", verbose=True))
