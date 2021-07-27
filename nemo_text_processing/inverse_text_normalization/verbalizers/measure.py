# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright 2015 and onwards Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from nemo_text_processing.text_normalization.graph_utils import NEMO_CHAR, GraphFst, delete_space_compulsory, NEMO_SPACE
from nemo_text_processing.inverse_text_normalization.verbalizers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.verbalizers.decimal import DecimalFst

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):

    PYNINI_AVAILABLE = False


class MeasureFst(GraphFst):
    """
    Finite state transducer for verbalizing measure, e.g.
        measure { negative: "true" cardinal { integer: "12" } units: "kg" } -> -12 kg

    Args:
        decimal: DecimalFst
        cardinal: CardinalFst
    """

    def __init__(self, decimal: DecimalFst, cardinal: CardinalFst):
        super().__init__(name="measure", kind="verbalize")
        unit = (
            pynutil.delete("unit: \"")
            + pynini.closure(NEMO_CHAR, 1, 7)
            + pynutil.delete("\"")
        )
        graph = (cardinal.final_graph | decimal.final_graph) + NEMO_SPACE + unit
        delete_tokens = self.delete_tokens(graph)
        self.fst = delete_tokens.optimize()
