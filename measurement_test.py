from pynini.lib.utf8 import VALID_UTF8_CHAR
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst as TC
from nemo_text_processing.inverse_text_normalization.taggers.decimal import DecimalFst as TD
from nemo_text_processing.inverse_text_normalization.verbalizers.cardinal import CardinalFst as VC
from nemo_text_processing.inverse_text_normalization.verbalizers.decimal import DecimalFst as VD
from nemo_text_processing.inverse_text_normalization.taggers.measure import MeasureFst as T
from nemo_text_processing.inverse_text_normalization.verbalizers.measure import MeasureFst as V

from pynini.lib.rewrite import top_rewrite

tagger = T(TC(), TD(TC())).fst
verbalizer = V(VD(), VC()).fst
tagged = top_rewrite("ba mươi phút", tagger)
print(tagged)
verbalized = top_rewrite(tagged, verbalizer)
print(verbalized)


