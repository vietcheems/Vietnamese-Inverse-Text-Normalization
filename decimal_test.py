from nemo_text_processing.inverse_text_normalization.taggers.decimal import DecimalFst
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst

from pynini.lib.rewrite import rewrites

if __name__ == "__main__":
	l = [
		"một phẩy hai ba",
		"năm phẩy năm triệu",
		"năm trăm bốn bốn phẩy bảy ba một",
		"không phẩy một"
	]
	for e in l:
		print(rewrites(e, DecimalFst(CardinalFst()).fst))
		# print(rewrites(e, CardinalFst().graph_no_exception))