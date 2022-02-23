from calendar import c
import mapper


def perform_processing():

    english_words = mapper.load_words(test_data)
    five_words = mapper.get_words_specified_length(5, english_words)

    possible_permutations = mapper.generate_letter_permutations(
        floating_letters, word_length)

    # merge permutations and reduce by known letter positions
    valid_permutations = mapper.merge_patterns(
        locked_letters, possible_permutations)
    candidate_words = mapper.get_words_from_pattern(
        valid_permutations, excluded_letters, five_words)

    if show_possible_words:
        print(candidate_words)

    print(mapper.calc_letter_frequency(
        candidate_words, floating_letters, locked_letters))


if __name__ == '__main__':

    # ADD CONFIG HERE #

    # Word specific
    floating_letters = 'i'
    locked_letters = '____d'
    excluded_letters = 'lratepoun'

    # Init and output behaviour
    word_length = 5
    test_data = False
    show_possible_words = False

    # END CONFIG #

    perform_processing()
