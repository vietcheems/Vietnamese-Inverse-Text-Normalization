import pynini
import sys
from nemo_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer

print(InverseNormalizer().inverse_normalize("hai mươi giờ kém hai mươi ngày mùng một tháng hai năm một", verbose=True))
