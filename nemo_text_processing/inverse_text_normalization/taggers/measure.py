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

from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.taggers.decimal import DecimalFst
from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
    NEMO_SIGMA,
    GraphFst,
    delete_extra_space,
    delete_space_compulsory,
    optional,
    optional
)

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False


class MeasureFst(GraphFst):
    """
    Finite state transducer for classifying measure
        e.g. minus twelve kilograms -> measure { negative: "true" cardinal { integer: "12" } units: "kg" }

    Args:
        cardinal: CardinalFst
        decimal: DecimalFst
    """

    def __init__(self, cardinal: CardinalFst, decimal: DecimalFst):
        super().__init__(name="measure", kind="classify")

        cardinal_graph = cardinal.graph_with_negative
        decimal_graph = decimal.graph_with_negative

        graph_unit = pynini.string_file(get_abs_path("data/measurements.tsv"))
        graph_per = delete_space_compulsory + pynini.cross("trên", "/") + delete_space_compulsory
        graph_unit = graph_unit + optional(graph_per + graph_unit)
        graph_unit = pynutil.insert("unit: \"") + graph_unit + pynutil.insert("\"")

        graph_number = cardinal_graph | decimal_graph

        graph = graph_number + delete_extra_space + graph_unit
        final_graph = self.add_tokens(graph)
        self.fst = final_graph.optimize()
