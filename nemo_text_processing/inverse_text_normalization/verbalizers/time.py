from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
    NEMO_DIGIT,
    GraphFst,
    delete_space_compulsory,
	optional
)
import pynini
from pynini.lib import pynutil

class TimeFst(GraphFst):
	"""
	Finite state transducer for verbalizing time
	e.g. time { hours: "12" to: "true" minutes: "20" } -> 11h40
	"""
	def __init__(self):
		super().__init__(name="time", kind="verbalize")
		hour = (
			pynutil.delete("hours: \"") 
			+ pynini.closure(NEMO_DIGIT, 1, 2) 
			+ pynutil.delete("\"") 
			+ pynutil.insert("h")
		)
		minute = (
			pynutil.delete("minutes: \"") 
			+ pynini.closure(NEMO_DIGIT, 1, 2) 
			+ pynutil.delete("\"") 
		)
		second = (
			pynutil.insert("p")
			+ pynutil.delete("seconds: \"") 
			+ pynini.closure(NEMO_DIGIT, 1, 2) 
			+ pynutil.delete("\"") 
			+ pynutil.insert("s")
		)
		hour_to = pynini.string_file(get_abs_path("data/time/hour_to.tsv"))
		hour_to = (
			pynutil.delete("hours: \"") 
			+ hour_to
			+ pynutil.delete("\"") 
			+ pynutil.insert("h")
		)
		minute_to = pynini.string_file(get_abs_path("data/time/minute_to.tsv"))
		minute_to = (
			pynutil.delete("minutes: \"") 
			+ minute_to
			+ pynutil.delete("\"") 
		)
		graph_without_to = (
			hour 
			+ optional(delete_space_compulsory + minute) 
			+ optional(delete_space_compulsory + second)
		)
		graph_with_to = (
			hour_to 
			+ optional(
				delete_space_compulsory 
				+ pynutil.delete("to: \"true\"") 
				+ delete_space_compulsory 
				+ minute_to
			) 
			+ optional(delete_space_compulsory + second)
		)
		graph = graph_without_to | graph_with_to
		final_graph = self.delete_tokens(graph)
		self.fst = final_graph.optimize()
