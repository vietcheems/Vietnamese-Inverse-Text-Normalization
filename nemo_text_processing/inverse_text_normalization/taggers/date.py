from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
	NEMO_DIGIT,
    GraphFst,
    delete_space_compulsory,
	delete_extra_space
)
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.taggers.consec_num import ConsecutiveNumberFst
import pynini
from pynini.lib import pynutil

class DateFst(GraphFst):
	"""
	Finite state transducer for classifying date, 
    	e.g. january fifth twenty twelve -> date { month: "january" day: "5" year: "2012" preserve_order: true }
    	e.g. the fifth of january twenty twelve -> date { day: "5" month: "january" year: "2012" preserve_order: true }
    	e.g. twenty twenty -> date { year: "2012" preserve_order: true }

	Args:
        cardinal: CardinalFst
		consec_num: ConsecutiveNumberFst
    """
	def __init__(self, cardinal: CardinalFst, consec_num: ConsecutiveNumberFst):
		super().__init__(name="date", kind="classify")
		cardinal_graph = cardinal.graph_no_exception_remove_dot
		consec_num_graph = consec_num.graph_2_or_more
		graph_2_9_muoi = cardinal.graph_2_9_muoi
		graph_ten = cardinal.graph_ten
		graph_2_digit = graph_ten | graph_2_9_muoi
		graph_digit_any_non_zero = cardinal.graph_digit_any_non_zero
		lunar_month = pynini.string_file(get_abs_path("data/lunar_months.tsv"))

		graph_day_num = (pynutil.insert("0") + graph_digit_any_non_zero) | pynini.cross("rằm", "15")
		graph_day_num |= graph_2_digit

		graph_month_num = pynutil.insert("0") + graph_digit_any_non_zero
		graph_month_num |= graph_ten
		graph_month_num |= lunar_month

		graph_year_num = cardinal_graph | consec_num_graph
		graph_year_num |= consec_num_graph + delete_space_compulsory + graph_2_digit

		day_graph = (
			pynutil.insert("day: \"") 
			+ pynutil.delete("ngày ") 
			+ pynini.closure((pynutil.delete("mồng") | pynutil.delete("mùng")) + delete_space_compulsory, 0, 1)
			+ graph_day_num 
			+ pynutil.insert("\"")
		)

		month_graph = (
			pynutil.insert("month: \"")
			+ pynutil.delete("tháng ")
			+ graph_month_num
			+ pynutil.insert("\"")
		)

		year_graph = (
			pynutil.insert("year: \"")
			+ pynutil.delete("năm ")
			+ graph_year_num
			+ pynutil.insert("\"")
		)

		# context_graph = self._context_graph()

		graph = day_graph + delete_extra_space + month_graph + delete_extra_space + year_graph
		graph |= day_graph + delete_extra_space + month_graph
		graph |= month_graph + delete_extra_space + year_graph
		graph |= day_graph
		graph |= month_graph
		graph |= year_graph
		# graph |= context_graph + delete_extra_space + year_graph

		final_graph = self.add_tokens(graph)
		self.fst = final_graph.optimize()

	# def _context_graph(self): FAILED
	# 	"""
	# 	Context for dealing with ambiguity between year and consecutive single digits
	# 	e.g năm hai không hai hai -> năm 2022 vs 50202
	# 	"""
		# preceding_digit = pynini.union(
		# 	pynini.string_file(get_abs_path("data/numbers/digit.tsv")),
		#  	pynini.string_file(get_abs_path("data/numbers/digit_var.tsv"))
		# )
		# preceding_digit = pynutil.add_weight(preceding_digit, 0.1)

		# context_graph = preceding_digit
		# return context_graph

