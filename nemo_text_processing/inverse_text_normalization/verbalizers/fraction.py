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

from nemo_text_processing.text_normalization.graph_utils import GraphFst, NEMO_DIGIT, delete_space_optional
from pynini.lib import pynutil
import pynini

class FractionFst(GraphFst):
    """
    Finite state transducer for verbalizing fraction, 
        e.g fraction { numerator: "2" denominator: "3" } -> 2/3
        e.g fraction { numerator: "24" denominator: "7" } -> 24/7

    """

    def __init__(self):
        super().__init__(name="fraction", kind="verbalize")
        negative = pynini.union(pynutil.delete("negative_numerator: \"true\""), pynutil.delete("negative_denominator: \"true\"")) + pynutil.insert("-")
        optional_negative = pynini.closure(negative + delete_space_optional, 0, 1)
        numerator = (
            optional_negative
            + pynutil.delete("numerator:") 
            + delete_space_optional
            + pynutil.delete("\"")
            + pynini.closure(NEMO_DIGIT, 1)
            + pynutil.delete("\"")
        )
        self.numerator = numerator

        denominator = (
            optional_negative
            + pynutil.delete("denominator:") 
            + delete_space_optional
            + pynutil.delete("\"")
            + NEMO_DIGIT
            + pynutil.delete("\"")
        )

        graph = numerator + delete_space_optional + pynutil.insert("/") + denominator
        final_graph = self.delete_tokens(graph)
        self.fst = final_graph.optimize()