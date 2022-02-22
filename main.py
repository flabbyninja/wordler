from itertools import permutations


def load_words(test_data):
    if not test_data:
        with open('data/words_alpha.txt') as word_file:
            valid_words = set(word_file.read().split())
    else:
        valid_words = ['Fiver', 'Chicken', 'Alone',
                       'Irate', 'Banana', 'Tractor', 'Sun']

    return valid_words


def get_words_specified_length(length, input_data):
    return list(map(lambda x: x.lower(), filter(lambda x: len(x) == length, input_data)))


def get_words_confirmed_position(finalized_letters, word):
    for i, x in enumerate(word):
        if (finalized_letters[i] is not None) and (finalized_letters[i] != x):
            return False
    return True


def get_words_loose_pattern(pattern_list, word_list):
    potential_words = []
    for pattern in pattern_list:
        potential_words += list(filter(lambda x: is_match(pattern, x), word_list))
    return potential_words


def is_match(pattern, word):
    if len(pattern) != len(word):
        return False
    for i, c in enumerate(pattern):
        if (c != '_') and (c.lower() != word[i].lower()):
            return False
    return True


def generate_letter_permutations(letters):
    # Get all permutations of [1, 2, 3]
    perm = permutations(letters)
    pattern_output = []

    # Print the obtained permutations
    for i in list(perm):
        pattern_output.append("".join([str(elem) for elem in i]))

    return pattern_output


def initialise_words():
    return


if __name__ == '__main__':
    test_data = False
    english_words = load_words(test_data)
    five_words = get_words_specified_length(5, english_words)

    test_data = [None for x in range(5)]
    test_data[1] = 'l'
    test_data[4] = 'e'

    # filtered_words = list(
    #     filter(lambda x: get_words_confirmed(test_data, x), five_words))

    # print(is_match('a_p_e', 'apple'))
    # print(is_match('r_al', 'apple'))
    # print(is_match('a__l_lll', 'apple'))
    # print(is_match('_p_l_', 'apple'))
    # print(is_match('apple', 'apple'))
    # print(is_match('_____', 'apple'))
    # print(filtered_words)

    # print(generate_letter_permutations(['a', '_', 'p', '_', 'e']))
    print(get_words_loose_pattern(['a_p_e'], five_words))
