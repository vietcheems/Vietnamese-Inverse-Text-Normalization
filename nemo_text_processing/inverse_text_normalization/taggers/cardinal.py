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


from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
    NEMO_DIGIT,
    NEMO_SPACE,
    GraphFst,
    delete_space,
)

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False


class CardinalFst(GraphFst):
    """
    Finite state transducer for classifying cardinals
        e.g. minus twenty three -> cardinal { integer: "23" negative: "-" } }
    """

    def __init__(self):
        super().__init__(name="cardinal", kind="classify")
        graph_digit = pynini.string_file(get_abs_path("data/numbers/digit.tsv"))
        graph_digit_var = pynini.string_file(get_abs_path("data/numbers/digit_var.tsv"))
        graph_digit_any = graph_digit | graph_digit_var
        graph_digit_non_zero = graph_digit @ pynini.difference(NEMO_DIGIT, '0')
        graph_digit_any_non_zero = graph_digit_any @ pynini.difference(NEMO_DIGIT, '0')

        graph_hundred_end = pynutil.delete("trăm")
        graph_thousands_end = pynutil.delete("nghìn")
        graph_million_end = pynutil.delete("triệu")
        graph_billion_end = pynini.union(pynutil.delete("tỉ"), pynutil.delete("tỷ"))

        graph_ten = pynini.string_file(get_abs_path("data/numbers/ten.tsv")) + pynini.union(delete_space + graph_digit_any, pynutil.insert("0"))

        graph_2_9_muoi = graph_digit_non_zero + delete_space + pynini.union(
            pynutil.delete("mươi") + pynini.union(delete_space + graph_digit_any, pynutil.insert("0")),
            graph_digit_any_non_zero)

        graph_hundred_component = pynini.union(graph_digit + delete_space + graph_hundred_end, pynutil.insert("0"))
        graph_hundred_component += pynini.closure(delete_space, 0, 1) 
        graph_hundred_component += pynini.union(
            graph_ten | graph_2_9_muoi,
            pynini.union(pynutil.delete("linh"), 
            pynutil.delete("lẻ")) + pynutil.insert("0") + delete_space + graph_digit_any | pynutil.insert("00"))
        graph_hundred_component = pynini.union(graph_hundred_component, pynutil.insert("00") + graph_digit)
        
        graph_hundred_component_at_least_one_none_zero_digit = graph_hundred_component @ (
            pynini.closure(NEMO_DIGIT) + (NEMO_DIGIT - "0") + pynini.closure(NEMO_DIGIT)
        )
        self.graph_hundred_component_at_least_one_none_zero_digit = (
            graph_hundred_component_at_least_one_none_zero_digit
        )

        graph_thousands = pynini.union(
            graph_hundred_component + delete_space + graph_thousands_end,
            pynutil.insert("000", weight=0.1),
        )

        graph_million = pynini.union(
            graph_hundred_component + delete_space + graph_million_end,
            pynutil.insert("000", weight=0.1),
        )

        graph_billion = pynini.union(
            graph_hundred_component + delete_space + graph_billion_end,
            pynutil.insert("000", weight=0.1),
        )
        # graph_trillion = pynini.union(
        #     graph_hundred_component_at_least_one_none_zero_digit + delete_space + pynutil.delete("trillion"),
        #     pynutil.insert("000", weight=0.1),
        # )
        # graph_quadrillion = pynini.union(
        #     graph_hundred_component_at_least_one_none_zero_digit + delete_space + pynutil.delete("quadrillion"),
        #     pynutil.insert("000", weight=0.1),
        # )
        # graph_quintillion = pynini.union(
        #     graph_hundred_component_at_least_one_none_zero_digit + delete_space + pynutil.delete("quintillion"),
        #     pynutil.insert("000", weight=0.1),
        # )
        # graph_sextillion = pynini.union(
        #     graph_hundred_component_at_least_one_none_zero_digit + delete_space + pynutil.delete("sextillion"),
        #     pynutil.insert("000", weight=0.1),
        # )

        # graph = graph_sextillion 
        # graph += delete_space
        # graph += graph_quintillion
        # graph += delete_space
        # graph += graph_quadrillion
        # graph += delete_space
        # graph += graph_trillion
        # graph += delete_space
        graph = graph_billion
        graph += delete_space
        graph += graph_million
        graph += delete_space
        graph += graph_thousands
        graph += delete_space
        graph += graph_hundred_component

        graph = graph @ pynini.union(
            pynutil.delete(pynini.closure("0")) + pynini.difference(NEMO_DIGIT, "0") + pynini.closure(NEMO_DIGIT), 
            pynutil.delete(pynini.closure("0")) + pynutil.insert("0")
        )



        # graph = pynini.cdrewrite(pynutil.delete("and"), NEMO_SPACE, NEMO_SPACE, NEMO_SIGMA) @ graph

        self.graph_no_exception = graph


        optional_minus_graph = pynini.closure(
            pynutil.insert("negative: ") + pynini.union(pynini.cross("âm", "\"-\""), pynini.cross("trừ", "\"-\"")) + NEMO_SPACE, 0, 1
        )
        graph = optional_minus_graph + pynutil.insert("integer: \"") + graph + pynutil.insert("\"")

        labels_exception = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "bẩy", "tám", "chín"]
        graph_exception = pynini.union(*labels_exception)
        graph = (pynini.project(graph, "input") - graph_exception.arcsort()) @ graph

        final_graph = self.add_tokens(graph)
        self.fst = final_graph.optimize()
