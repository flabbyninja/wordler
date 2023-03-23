from typing import Set
from flask import Flask, request, jsonify

import wordlertools.pattern_processor as pattern_processor

app = Flask(__name__)


def create_floating_patterns(input_string: str) -> Set[str]:
    if input_string is None:
        return set()
    return set(input_string.split(","))


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/wordler", methods=["GET"])
def do_wordler():
    args = request.args
    param_dict = args.to_dict()

    locked_pattern = ""
    floating_patterns = set()
    excluded_letters = ""

    if "l" in param_dict:
        locked_pattern = param_dict["l"]

    if "f" in param_dict:
        floating_patterns = create_floating_patterns(param_dict["f"])

    if "x" in param_dict:
        excluded_letters = param_dict["x"]

    if (
        locked_pattern is None
        and floating_patterns is None
        and excluded_letters is None
    ):
        return "No processing required. All parameters empty."

    words_file = "./data/words_alpha.txt"
    word_length = 5
    candidate_words = pattern_processor.get_candidate_words(
        locked_pattern, floating_patterns, excluded_letters, words_file, word_length
    )

    return jsonify(list(candidate_words))


@app.errorhandler(Exception)
def basic_error(error):
    return jsonify({"error": "Bad parameters " + str(error)}), 500
