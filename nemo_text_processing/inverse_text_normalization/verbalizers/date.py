from nemo_text_processing.text_normalization.graph_utils import (
	GraphFst,
	NEMO_DIGIT,
	delete_space_compulsory
)
import pynini
from pynini.lib import pynutil

class DateFst(GraphFst):
	"""
	Finite state transducer for verbalizing date
		e.g date { day: "10" month: "1" year: "2001" } -> 10/1/2001
	"""
	def __init__(self):
		super().__init__(name="date", kind="verbalize")
		translator = (
			pynini.cross("day", "ngày")
			| pynini.cross("month", "tháng")
			| pynini.cross("year", "năm")
		)
		remover = (
			pynutil.delete("day")
			| pynutil.delete("month")
			| pynutil.delete("year")
		)
		single_graph = translator + pynutil.insert(" ") + pynutil.delete(": \"") + pynini.closure(NEMO_DIGIT, 1) + pynutil.delete("\"")
		single_graph_no_begin_word = remover + pynutil.delete(": \"") + pynini.closure(NEMO_DIGIT, 1) + pynutil.delete("\"")
		
		slash_graph = (
			single_graph 
			+ delete_space_compulsory 
			+ pynutil.insert("/") 
			+ pynini.closure(single_graph_no_begin_word + delete_space_compulsory + pynutil.insert("/"), 0, 1)
			+ single_graph_no_begin_word
		)
	
		graph = single_graph | slash_graph
		final_graph = self.delete_tokens(graph)
		self.fst = final_graph.optimize()