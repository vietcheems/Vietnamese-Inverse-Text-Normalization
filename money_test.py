from nemo_text_processing.inverse_text_normalization.verbalizers import verbalize
from nemo_text_processing.inverse_text_normalization.taggers.money import MoneyFst as T
from nemo_text_processing.inverse_text_normalization.verbalizers.money import MoneyFst as V
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst as TC
from nemo_text_processing.inverse_text_normalization.taggers.decimal import DecimalFst as TD
from nemo_text_processing.inverse_text_normalization.verbalizers.decimal import DecimalFst as VD
from nemo_text_processing.inverse_text_normalization.verbalizers.cardinal import CardinalFst as VC
from pynini.lib.rewrite import rewrites

s = "một phẩy hai triệu bảng anh"
tagger = T(TC(), TD(TC(),keep_quantity=False)).fst
verbalizer = V(decimal=VD(), cardinal=VC()).fst
tagged = rewrites(s, tagger)[0]
print(tagged)
print(rewrites(tagged, verbalizer))