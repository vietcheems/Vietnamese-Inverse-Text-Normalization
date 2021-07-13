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

import pynini
from pynini.lib import pynutil
from nemo_text_processing.text_normalization.graph_utils import GraphFst, delete_space_optional, delete_extra_space


class FractionFst(GraphFst):
    """
    Finite state transducer for classifying fraction
        e.g hai phần ba -> fraction { numerator: "2" denominator: "3" }
        e.g hai tư trên bảy -> fraction { numerator: "24" denominator: "7" }

    """

    def __init__(self, cardinal: GraphFst):
        super().__init__(name="fraction", kind="classify")
        cardinal_graph = cardinal.graph_no_exception
        negative = pynini.union(pynini.cross("âm", "true"), pynini.cross("trừ", "true"))
        slash = pynutil.delete("phần") | pynutil.delete("trên")
        graph = (
            pynini.closure(pynutil.insert("negative_numerator: \"")  + negative + pynutil.insert("\"") + delete_extra_space, 0 , 1)
            + pynutil.insert("numerator: \"") + cardinal_graph + pynutil.insert("\"")
            + delete_space_optional + slash + delete_extra_space 
            + pynini.closure(pynutil.insert("negative_denominator: \"")  + negative + pynutil.insert("\"") + delete_extra_space, 0 , 1)
            + pynutil.insert("denominator: \"") + cardinal_graph + pynutil.insert("\"")
        )
        final_graph = self.add_tokens(graph)
        self.fst = final_graph.optimize()

        
