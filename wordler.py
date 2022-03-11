"""
Command line invocation of wordler processing
"""
import argparse
from typing import Set
import wordlertools.pattern_processor as pattern_processor


def perform_processing(locked_pattern: str, floating_patterns: Set[str],
                       excluded_letters: str) -> Set[str]:
    """
    Main entry point to start processing of words that match the restrictions given

    Arguments:
    locked_pattern: string with pattern of letters, locked into the right positions (green)
    floating_patterns: set of strings, covering patterns with letters known to be in word,
    but not in those positions (yellow)
    excluded_letters: string containing letters known to not be in solution

    Returns: set of candidate words that contains the answer
    """
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
    SHOW_POSSIBLE_WORDS = True

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

    param_locked_pattern, param_floating_patterns, param_excluded_letters = parse_arguments(
        args.locked_pattern, args.floating_patterns, args.excluded_letters)

    if (param_locked_pattern is None and
        param_floating_patterns is None and
            param_excluded_letters is None):
        raise Exception(
            'You must specify one valid parameter of locked, floating or excluded')

    candidate_words = perform_processing(
        param_locked_pattern, param_floating_patterns, param_excluded_letters)

    if SHOW_POSSIBLE_WORDS:
        print(candidate_words)
