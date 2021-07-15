from nemo_text_processing.inverse_text_normalization.taggers.date import DateFst
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.taggers.consec_num import ConsecutiveNumberFst
from pynini.lib.rewrite import rewrites
if __name__ == "__main__":
	graph = DateFst(CardinalFst(), ConsecutiveNumberFst()).fst
	l = [
		"năm năm mươi",
		"tháng chạp năm chín mươi",
		"ngày hai chín tháng tám"
	]
	for case in l:
		print(rewrites(case,  graph))