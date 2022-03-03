import wordlertools.pattern_processor as pattern_processor

from typing import Set


def perform_processing() -> Set[str]:

    # Init and output behaviour
    words_file = './data/words_alpha.txt'
    word_length = 5

    return pattern_processor.get_candidate_words(
        locked_pattern, floating_patterns, excluded_letters, words_file, word_length)


if __name__ == '__main__':

    # ADD CONFIG HERE #
    show_possible_words = True

    # Word specific
    locked_pattern = '_a_t_'
    floating_patterns = {'__n_s'}
    excluded_letters = 'erip'

    # END CONFIG #

    candidate_words = perform_processing()

    if show_possible_words:
        print(candidate_words)
