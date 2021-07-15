from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
    GraphFst,
    delete_space_optional,
)
import pynini
from pynini.lib import pynutil

class ConsecutiveNumberFst(GraphFst):
    """
    Finite state transducer for classifying consecutive single digit number such as telephone number etc.
        e.g một hai ba bốn -> consecutive { number: "01234" }
    """
    def __init__(self):
        super().__init__(name="consecutive", kind="classify")
        graph_digit = pynini.string_file(get_abs_path("data/numbers/digit.tsv"))
        graph_digit_var = pynini.string_file(get_abs_path("data/numbers/digit_var.tsv"))
        graph_digit_any = graph_digit | graph_digit_var
        graph = graph_digit + pynini.closure(delete_space_optional + graph_digit_any, 1)
        self.graph_2_or_more = graph
        graph = pynutil.insert("number: \"") + graph + pynutil.insert("\"")
        final_graph = self.add_tokens(graph)
        self.fst = final_graph.optimize()

