from nemo_text_processing.inverse_text_normalization.taggers.decimal import DecimalFst as T
from nemo_text_processing.inverse_text_normalization.verbalizers.decimal import DecimalFst as V
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst

from pynini.lib.rewrite import rewrites

if __name__ == "__main__":
	l = [
		"một phẩy hai ba",
		"năm phẩy năm triệu",
		"năm nghìn bảy trăm bốn bốn phẩy bảy ba một",
		"không phẩy một",
		"một phẩy một ba năm nghìn"
	]
	for e in l:
		tagged = rewrites(e, T(CardinalFst(), keep_quantity=True).fst)[0]
		print(tagged)
		print(rewrites(tagged, V().fst))

		# print(rewrites(e, CardinalFst().graph_no_exception))