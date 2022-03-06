import wordlertools.pattern_processor as pattern_processor
import argparse
from typing import Set


def perform_processing(locked_pattern, floating_patterns, excluded_letters) -> Set[str]:

    # Init and output behaviour
    words_file = './data/words_alpha.txt'
    word_length = 5

    return pattern_processor.get_candidate_words(
        locked_pattern, floating_patterns, excluded_letters, words_file, word_length)


def parse_arguments(locked_pattern, floating_patterns, excluded_letters):
    """Parse command line parameters passed for processing

    Strip out any extra spaces from command lines parameters passed in.

    Arguments:
    locked_pattern: string of letters locked into word
    floating_patterns: list of strings covering letters in word, but not in those positions
    excluded_letters: string covering letters not in word

    Returns: versions of all parameters with extra spaces stripped out
    """
    if locked_pattern:
        locked_pattern = locked_pattern.replace(' ', '')

    if floating_patterns:
        floating_patterns = [x.replace(' ', '') for x in floating_patterns]

    if excluded_letters:
        excluded_letters = excluded_letters.replace(' ', '')

    return [locked_pattern, floating_patterns, excluded_letters]


if __name__ == '__main__':

    # ADD CONFIG HERE #
    show_possible_words = True

    # END CONFIG #

    # get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--locked_pattern',
                        help='string of known letters in the right position')
    parser.add_argument('-f', '--floating_patterns', action='append',
                        help='list of patterns of valid letters in the wrong position')
    parser.add_argument('-x', '--excluded_letters',
                        help='string of letters not in the word')
    args = parser.parse_args()

    locked_pattern, floating_patterns, excluded_letters = parse_arguments(
        args.locked_pattern, args.floating_patterns, args.excluded_letters)

    if locked_pattern is None and floating_patterns is None and excluded_letters is None:
        raise Exception(
            'You must specify one valid parameter of locked, floating or excluded')

    candidate_words = perform_processing(
        locked_pattern, floating_patterns, excluded_letters)

    if show_possible_words:
        print(candidate_words)
