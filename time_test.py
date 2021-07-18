from nemo_text_processing.inverse_text_normalization.taggers.time import TimeFst as T
from nemo_text_processing.inverse_text_normalization.verbalizers.time import TimeFst as V
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst

from pynini.lib.rewrite import top_rewrite
if __name__ == "__main__":
	tagger = T(CardinalFst()).fst
	verbalizer = V().fst
	l = [
		"một giờ rưỡi",
		"hai rưỡi",
		"sáu giờ kém năm",
		"ba giờ kém hai mươi phút",
		"bốn giờ bốn mươi",
		"mười chín giờ",
		"ba giờ ba phút ba giây",
		"tám giờ"
	]
	for case in l:
		s = top_rewrite(case, tagger)
		print(s)
		s = top_rewrite(s, verbalizer)
		print(s)