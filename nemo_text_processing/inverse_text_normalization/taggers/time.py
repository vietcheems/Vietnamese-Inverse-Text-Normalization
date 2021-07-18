from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
    GraphFst,
    delete_extra_space,
	optional,
	delete_space_compulsory,
	insert_space
)
import pynini
from pynini.lib import pynutil

class TimeFst(GraphFst):
	"""
	Finite state transducer for classifying time
	e.g mười hai giờ ba mươi -> time { hours: "12" minutes: "30" }
	"""
	def __init__(self, cardinal: CardinalFst):
		super().__init__(name="time", kind="classify")
		graph_digit = cardinal.graph_digit_any
		graph_digit_leading_zero = pynutil.insert("0") + graph_digit

		graph_ten = cardinal.graph_ten
		graph_2_9_muoi = cardinal.graph_2_9_muoi
		graph_2_digit = graph_ten | graph_2_9_muoi

		graph_hour_alone = pynutil.insert("hours: \"") + (graph_digit | graph_2_digit) + pynutil.insert("\"") + pynutil.delete(" giờ")
		graph_time_num = graph_digit_leading_zero | graph_2_digit

		graph_hour = (
			pynutil.insert("hours: \"") 
			+ graph_time_num 
			+ pynutil.insert("\"") 
			+ delete_space_compulsory 
			+ pynutil.delete("giờ")
		)
		graph_minute = (
			pynutil.insert("minutes: \"") 
			+ graph_time_num 
			+ pynutil.insert("\"") 
			+ optional(delete_space_compulsory + pynutil.delete("phút"))
		)
		graph_second = (
			pynutil.insert("seconds: \"") 
			+ graph_time_num 
			+ pynutil.insert("\"") 
			+ delete_space_compulsory
			+ pynutil.delete("giây")
		)
		graph_ruoi = (
			pynutil.insert("hours: \"") 
			+ graph_time_num 
			+ pynutil.insert("\"") 
			+ optional(pynutil.delete(" giờ"))
			+ pynutil.delete(" rưỡi")
			+ insert_space
			+ pynutil.insert("minutes: \"30\"")
		)

		graph_to = delete_space_compulsory + pynutil.delete("kém") + insert_space + pynutil.insert("to: \"true\"")
		graph = (
			graph_hour 
			+ optional(graph_to) 
			+ delete_extra_space + graph_minute
			+ optional(delete_extra_space + graph_second)
		)
		graph |= graph_hour_alone
		graph |= graph_ruoi


		final_graph = self.add_tokens(graph)
		self.fst = final_graph.optimize()
