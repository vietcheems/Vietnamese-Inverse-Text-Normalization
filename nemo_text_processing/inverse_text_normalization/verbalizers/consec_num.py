from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
    NEMO_DIGIT,
    GraphFst,
    delete_space_optional,
)
import pynini
from pynini.lib import pynutil

class ConsecutiveNumberFst(GraphFst):
    """
    Finite state transducer for verbalizing consecutive single digit number such as telephone number etc.
        e.g một hai ba bốn -> consecutive { number: "01234" }
    """
    def __init__(self):
        super().__init__(name="consecutive", kind="verbalize")
        graph = pynutil.delete("number: \"") + pynini.closure(NEMO_DIGIT, 2) + pynutil.delete("\"")
        final_graph = self.delete_tokens(graph)
        self.fst = final_graph.optimize()

