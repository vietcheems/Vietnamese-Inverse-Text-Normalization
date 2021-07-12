from pynini.lib.rewrite import rewrites
from nemo_text_processing.inverse_text_normalization.taggers.consec_num import ConsecutiveNumberFst as classify
from nemo_text_processing.inverse_text_normalization.verbalizers.consec_num import ConsecutiveNumberFst as verbalize

if __name__ == "__main__":
    classify_graph = classify().fst
    verbalize_graph = verbalize().fst
    s = "hai lăm"
    s = rewrites(s, classify_graph)[0]
    print(s)
    s = rewrites(s, verbalize_graph)[0]
    print(s)