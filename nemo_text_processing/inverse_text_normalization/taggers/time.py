from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.utils import get_abs_path, num_to_word
from nemo_text_processing.text_normalization.graph_utils import (
    GraphFst,
    delete_extra_space,
    delete_space_optional,
)

class TimeFst(GraphFst):
	"""
	Finite state transducer for classifying time
	e.g mười hai giờ ba mươi -> time { hours: "12" minutes: "30" }
	"""
	def __init__(self, cardinal: CardinalFst):
		super().__init__(name="time", kind="classify")
		