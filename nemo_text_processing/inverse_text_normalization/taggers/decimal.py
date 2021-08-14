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

from collections import defaultdict
from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from nemo_text_processing.text_normalization.graph_utils import NEMO_DIGIT, GraphFst, delete_extra_space, delete_space_optional, delete_space_compulsory

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False


def get_quantity(decimal: 'pynini.FstLike', cardinal_up_to_hundred: 'pynini.FstLike') -> 'pynini.FstLike':
    """
    Returns FST that transforms either a cardinal or decimal followed by a quantity into a numeral,
    e.g. one million -> integer_part: "1" quantity: "million"
    e.g. one point five million -> integer_part: "1" fractional_part: "5" quantity: "million"

    Args: 
        decimal: decimal FST
        cardinal_up_to_hundred: cardinal FST
    """
    numbers = cardinal_up_to_hundred @ (
        pynutil.delete(pynini.closure("0")) + pynini.difference(NEMO_DIGIT, "0") + pynini.closure(NEMO_DIGIT)
    )
    suffix = pynini.union("nghìn", "ngàn", "triệu", "tỉ", "tỷ")
    # res = (
    #     pynutil.insert("integer_part: \"")
    #     + numbers
    #     + pynutil.insert("\"")
    #     + delete_extra_space
    #     + pynutil.insert("quantity: \"")
    #     + suffix
    #     + pynutil.insert("\"")
    # )
    res = decimal + delete_extra_space + pynutil.insert("quantity: \"") + suffix + pynutil.insert("\"")
    return res

def _convert_quantity(graph_1_digit, num_zeros):
    all_num_zero_case = graph_1_digit + pynini.closure(pynutil.insert("0"), num_zeros - 1, num_zeros - 1)
    for num_decimal in range(2, num_zeros + 1):
        decimal = pynini.closure(graph_1_digit + delete_space_compulsory, num_decimal - 1, num_decimal - 1) + graph_1_digit
        if num_decimal != num_zeros:
            trailing_zero = pynini.closure(pynutil.insert("0"), num_zeros - num_decimal, num_zeros - num_decimal)
            decimal += trailing_zero
        all_num_zero_case |= decimal
    return all_num_zero_case

class DecimalFst(GraphFst):
    """
    Finite state transducer for classifying decimal
        e.g. minus twelve point five o o six billion -> decimal { negative: "true" integer_part: "12" dot: "false" fractional_part: "5006" quantity: "billion" }
        e.g. one billion -> decimal { integer_part: "1" quantity: "billion" }
    Args:
        cardinal: CardinalFst
    """

    def __init__(self, cardinal: CardinalFst, keep_quantity=True):
        super().__init__(name="decimal", kind="classify")

        cardinal_graph = cardinal.graph_no_exception
        graph_2_9_muoi = cardinal.graph_2_9_muoi

        graph_1_digit = pynini.string_file(get_abs_path("data/numbers/digit.tsv"))
        graph_1_digit |= pynini.string_file(get_abs_path("data/numbers/digit_var.tsv"))

        graph_decimal = pynini.closure(graph_1_digit + delete_space_optional) + graph_1_digit
        graph_decimal |= graph_2_9_muoi
        self.graph = graph_decimal

        delete_comma = pynutil.delete("phẩy") 
        delete_comma_tagged = delete_comma + pynutil.insert("dot: \"false\"")
        delete_dot = pynutil.delete("chấm")
        delete_dot_tagged = delete_dot + pynutil.insert("dot: \"true\"")
        delete_fractional_sep = delete_comma | delete_dot
        delete_fractional_sep_tagged = delete_comma_tagged | delete_dot_tagged

        optional_graph_negative = pynini.closure(
            pynutil.insert("negative: ") + pynini.union(pynini.cross("âm", "\"true\""), pynini.cross("trừ", "\"true\"")) + delete_extra_space, 0, 1
        )

        graph_fractional = pynutil.insert("fractional_part: \"") + graph_decimal + pynutil.insert("\"")
        graph_integer = pynutil.insert("integer_part: \"") + cardinal_graph + pynutil.insert("\"")
        final_graph_wo_sign = (
            graph_integer + delete_extra_space + delete_fractional_sep_tagged + delete_extra_space + graph_fractional
        )
        final_graph = optional_graph_negative + final_graph_wo_sign
        if keep_quantity:
            self.final_graph_wo_negative = final_graph_wo_sign | get_quantity(
                final_graph_wo_sign, cardinal.graph_hundred_component_at_least_one_none_zero_digit
            )
            final_graph |= optional_graph_negative + get_quantity(
                final_graph_wo_sign, cardinal.graph_hundred_component_at_least_one_none_zero_digit
            )
        else:
            quantity_dic = {}
            with open(get_abs_path("data/numbers/quantity.tsv")) as f:
                for row in f:
                    items = row.split("\t")
                    quantity_dic[items[0]] = items[1].replace("\n", "")

            grouped_quantity = defaultdict(list)
            for key, val in quantity_dic.items():
                grouped_quantity[val].append(key)
            
            num_after_comma_list = []
            for num_zeros in grouped_quantity.keys():
                first = True
                for quantity in grouped_quantity[num_zeros]:
                    # print(quantity)
                    if first:
                        delete_quantity = pynutil.delete(quantity)
                        first = False
                    else:
                        delete_quantity = pynini.union(delete_quantity, pynutil.delete(quantity))
                self.test_convert_quantity = _convert_quantity(graph_1_digit, int(num_zeros))
                num_after_comma_list.append(_convert_quantity(graph_1_digit, int(num_zeros)) + delete_space_compulsory + delete_quantity)
                # print("num_zeros:" + num_zeros)
                # break

            first = True
            for graph in num_after_comma_list:
                if first:
                    num_after_sep = graph
                    first = False
                else:
                    num_after_sep |= graph
            
            self.num_after_comma = num_after_sep
            graph_convert_quantity = (
                pynutil.insert("integer_part: \"") 
                + cardinal_graph 
                + delete_space_compulsory 
                + delete_fractional_sep 
                + delete_space_compulsory 
                + num_after_sep
                + pynutil.insert("\"")
            )
            self.graph_convert_quantity = graph_convert_quantity
            self.final_graph_wo_negative = final_graph_wo_sign | graph_convert_quantity
            final_graph |= optional_graph_negative + graph_convert_quantity
        self.graph_with_negative = final_graph
        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
