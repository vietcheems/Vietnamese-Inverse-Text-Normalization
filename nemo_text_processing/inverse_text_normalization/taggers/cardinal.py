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


from os import remove
from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
    NEMO_CHAR,
    NEMO_DIGIT,
    NEMO_SPACE,
    GraphFst,
    delete_space_optional,
    delete_space_compulsory
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
        self.graph_digit_any_non_zero = graph_digit_any_non_zero
        self.graph_digit_any = graph_digit_any

        graph_hundred_end = pynutil.delete("trăm")
        graph_thousands_end = pynutil.delete("nghìn") | pynutil.delete("ngàn")
        graph_million_end = pynutil.delete("triệu")
        graph_billion_end = pynutil.delete("tỉ") | pynutil.delete("tỷ")
        graph_trillion_end = graph_thousands_end + delete_space_optional + graph_billion_end
        graph_quadrillion_end = graph_million_end + delete_space_optional + graph_billion_end
        graph_quintillion_end = graph_billion_end + delete_space_optional + graph_billion_end
        graph_sextillion_end = graph_thousands_end + delete_space_optional + graph_quintillion_end

        graph_ten = pynini.string_file(get_abs_path("data/numbers/ten.tsv")) + pynini.union(delete_space_optional + graph_digit_any, pynutil.insert("0"))
        self.graph_ten = graph_ten

        graph_digit_any_non_zero_no_nam = (pynini.project(graph_digit_any_non_zero, "input") - pynini.accep("năm")) @ graph_digit_any_non_zero
        graph_2_9_muoi = graph_digit_non_zero + delete_space_optional + pynini.union(
            pynutil.delete("mươi") + pynini.union(delete_space_optional + graph_digit_any_non_zero_no_nam, pynutil.insert("0")),
            graph_digit_any_non_zero_no_nam)
        self.graph_2_9_muoi = graph_2_9_muoi

        graph_hundred_component_no_1_digit = pynini.union(graph_digit + delete_space_optional + graph_hundred_end, pynutil.insert("0"))
        graph_hundred_component_no_1_digit += pynini.closure(delete_space_optional, 0, 1) 
        graph_hundred_component_no_1_digit += pynini.union(
            graph_ten | graph_2_9_muoi,
            pynini.union(pynutil.delete("linh"), 
            pynutil.delete("lẻ")) + pynutil.insert("0") + delete_space_optional + graph_digit_any | pynutil.insert("00"))
        graph_hundred_component = pynini.union(graph_hundred_component_no_1_digit, pynutil.insert("00") + graph_digit)
        graph_hundred_component_at_least_one_digit = pynini.difference(pynini.closure(NEMO_CHAR), pynini.accep("")) @ graph_hundred_component
        
        graph_hundred_component_at_least_one_none_zero_digit = graph_hundred_component @ (
            pynini.closure(NEMO_DIGIT) + (NEMO_DIGIT - "0") + pynini.closure(NEMO_DIGIT)
        )
        self.graph_hundred_component_at_least_one_none_zero_digit = (
            graph_hundred_component_at_least_one_none_zero_digit
        )

        graph_thousands = pynini.union(
            graph_hundred_component_at_least_one_digit + pynini.cross(" ", "") + graph_thousands_end,
            pynutil.insert("000"),
        )
        graph_thousands += pynutil.insert(".")

        graph_million = pynini.union(
            graph_hundred_component_at_least_one_digit + delete_space_compulsory + graph_million_end,
            pynutil.insert("000"),
        )
        graph_million += pynutil.insert(".")

        graph_billion = pynini.union(
            graph_hundred_component_at_least_one_digit + delete_space_compulsory + graph_billion_end,
            pynutil.insert("000"),
        )
        graph_billion += pynutil.insert(".")

        graph_trillion = pynini.union(
            graph_hundred_component_at_least_one_digit + delete_space_compulsory + graph_trillion_end,
            pynutil.insert("000"),
        )
        graph_trillion += pynutil.insert(".")

        graph_quadrillion = pynini.union(
            graph_hundred_component_at_least_one_digit + delete_space_compulsory + graph_quadrillion_end,
            pynutil.insert("000"),
        )
        graph_quadrillion += pynutil.insert(".")

        graph_quintillion = pynini.union(
            graph_hundred_component_at_least_one_digit + delete_space_compulsory + graph_quintillion_end,
            pynutil.insert("000"),
        )
        graph_quintillion += pynutil.insert(".")

        graph_sextillion = pynini.union(
            graph_hundred_component_at_least_one_digit + delete_space_compulsory + graph_sextillion_end,
            pynutil.insert("000"),
        )
        graph_sextillion += pynutil.insert(".")

        graph = (
            graph_sextillion
            + delete_space_optional
            + graph_quintillion
            + delete_space_optional
            + graph_quadrillion
            + delete_space_optional
            + graph_trillion
            + delete_space_optional
            + graph_billion
            + delete_space_optional
            + graph_million
            + delete_space_optional
            + graph_thousands
            + delete_space_optional
            + graph_hundred_component_no_1_digit
        )
        graph |= graph_digit

        self.graph_before_remove_zero = graph
        remove_leading_zero_graph = pynini.union(
            pynini.closure(pynutil.delete("000" + ".")) + pynutil.delete(pynini.closure("0")) 
            + pynini.difference(NEMO_DIGIT, "0") + pynini.closure(NEMO_DIGIT, 0, 2) 
            + pynini.closure("." + pynini.closure(NEMO_DIGIT, 3, 3)),
            pynini.cross(pynini.closure("000" + ".") + pynini.closure("0", 1, 3), "0")
        )
        self.remove_leading_zero_graph = remove_leading_zero_graph
        graph = graph @ remove_leading_zero_graph



        # graph = pynini.cdrewrite(pynutil.delete("and"), NEMO_SPACE, NEMO_SPACE, NEMO_SIGMA) @ graph

        self.graph_no_exception = graph
        remove_dot = pynini.closure(pynini.closure(NEMO_DIGIT) + pynutil.delete(".")) + pynini.closure(NEMO_DIGIT)
        self.graph_no_exception_remove_dot = graph @ remove_dot

        optional_minus_graph = pynini.closure(
            pynutil.insert("negative: ") + pynini.union(pynini.cross("âm", "\"true\""), pynini.cross("trừ", "\"true\"")) + NEMO_SPACE, 0, 1
        )
        self.optional_minus_graph = optional_minus_graph
        graph = optional_minus_graph + pynutil.insert("integer: \"") + graph + pynutil.insert("\"")

        self.graph_with_negative = graph

        labels_exception = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "bẩy", "tám", "chín"]
        graph_exception = pynini.union(*labels_exception)
        graph = (pynini.project(graph, "input") - graph_exception.arcsort()) @ graph

        final_graph = self.add_tokens(graph)
        self.fst = final_graph.optimize()
