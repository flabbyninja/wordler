from calendar import c
import mapper


def perform_processing():

    # Initialise set of words that candidates will be chosen from
    base_words = mapper.load_words(test_data)
    sized_words = mapper.get_words_specified_length(word_length, base_words)

    # Get string with unique floating letters from the floating patterns
    floating_letters = mapper.get_letters_for_permutations(
        floating_patterns, word_length)

    # Generate all permutations from unique characters
    possible_permutations = mapper.generate_letter_permutations(
        floating_letters, word_length)

    # merge permutations and reduce by known letter positions
    valid_permutations = mapper.merge_patterns(
        locked_letters, floating_patterns, possible_permutations)

    # get candidate words matching the reduced set of patterns
    candidate_words = mapper.get_words_from_pattern(
        valid_permutations, excluded_letters, sized_words)

    if show_possible_words:
        print(candidate_words)

    top_letters = mapper.calc_letter_frequency(
        candidate_words, floating_letters, locked_letters)

    if show_top_letter:
        top_letter, _ = top_letters.most_common(1)[0]
        print(top_letter)


if __name__ == '__main__':

    # ADD CONFIG HERE #

    # Word specific
    floating_patterns = []
    locked_letters = '__ant'
    excluded_letters = 'plireks'

    # Init and output behaviour
    word_length = 5
    test_data = False
    show_possible_words = True
    show_top_letter = False

    # END CONFIG #

    perform_processing()
