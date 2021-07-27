from pynini.lib.rewrite import rewrites, top_rewrite
import pynini
import os
import argparse

def parse_args():
	parser = argparse.ArgumentParser(description="Inverse normalize text")
	parser.add_argument("input", type=str, help="input text")
	return parser.parse_args()


def inverse_normalize(s: str, verbose=False) -> str:
	dir_path = os.path.dirname(os.path.realpath(__file__))
	reader_classifier = pynini.Far(os.path.join(dir_path, "far/classify/tokenize_and_classify.far"))
	reader_verbalizer = pynini.Far(os.path.join(dir_path, "far/verbalize/verbalize.far"))
	classifier = reader_classifier.get_fst()
	verbalizer = reader_verbalizer.get_fst()
	token = top_rewrite(s, classifier)
	if verbose:
		print(token)
	return top_rewrite(token, verbalizer)

if __name__ == "__main__":
	arg = parse_args()
	print(inverse_normalize(arg.input))

