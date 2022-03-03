import wordlertools.pattern_processor as pattern_processor


def perform_processing():

    candidate_words = pattern_processor.get_candidate_words(
        locked_pattern, floating_patterns, excluded_letters, words_file, word_length)

    if show_possible_words:
        print(candidate_words)

    # top_letters = mapper.calc_letter_frequency(
    #     candidate_words, permutation_letters, locked_letters)

    # if show_top_letter:
    #     top_letter, _ = top_letters.most_common(1)[0]
    #     print(top_letter)


if __name__ == '__main__':

    # ADD CONFIG HERE #

    # Word specific
    locked_pattern = '_a_t_'
    floating_patterns = {'__n_s'}
    excluded_letters = 'erip'

    # Init and output behaviour
    words_file = './data/words_alpha.txt'
    word_length = 5
    show_possible_words = True
    show_top_letter = False

    # END CONFIG #

    perform_processing()
