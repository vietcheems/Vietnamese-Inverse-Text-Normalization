from nemo_text_processing.inverse_text_normalization.taggers.date import DateFst as T
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.taggers.consec_num import ConsecutiveNumberFst
from nemo_text_processing.inverse_text_normalization.verbalizers.date import DateFst as V
from pynini.lib.rewrite import rewrites, top_rewrite
if __name__ == "__main__":
	tagger = T(CardinalFst(), ConsecutiveNumberFst()).fst
	verbalizer = V().fst
	l = [
		"năm năm mươi",
		"tháng chạp năm hai không hai mươi",
		"ngày mồng chín tháng tám",
		"ngày rằm",
		"tháng giêng"
	]
	for case in l:
		tagged = top_rewrite(case,  tagger)
		print(tagged)
		verbalized = top_rewrite(tagged, verbalizer)
		print(verbalized)