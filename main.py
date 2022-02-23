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


def get_words_locked_position(finalized_letters, word):
    for i, x in enumerate(word):
        if (finalized_letters[i] != '_') and (finalized_letters[i] != x):
            return False
    return True


def get_words_from_pattern(pattern_list, word_list):
    potential_words = []
    for pattern in pattern_list:
        potential_words += list(
            filter(lambda x: is_word_a_pattern_match(pattern, x), word_list))
    return potential_words


def is_word_a_pattern_match(pattern, word):
    if len(pattern) != len(word):
        return False
    for i, c in enumerate(pattern):
        if (c != '_') and (c.lower() != word[i].lower()):
            return False
    return True


def generate_letter_permutations(letters, word_length):
    # Get all permutations of [1, 2, 3]
    if len(letters) < word_length:
        letters += '_' * (word_length - len(letters))
    if len(letters) > word_length:
        letters = letters[:word_length]
    perm = permutations(letters)
    permutation_output = []

    # Print the obtained permutations
    for i in set(perm):
        permutation_output.append("".join([str(elem) for elem in i]))

    return permutation_output


def merge_patterns(locked_letters, permutation):
    merged_permutations = set()
    for perm in permutation:
        accept = True
        for i, c in enumerate(perm):
            if locked_letters[i] != '_':
                if c != '_':
                    accept = False
                    break
                else:
                    perm = perm[:i] + locked_letters[i] + perm[i+1:]
        if accept:
            merged_permutations.add(perm)
    return merged_permutations


if __name__ == '__main__':
    test_data = False
    english_words = load_words(test_data)
    five_words = get_words_specified_length(5, english_words)

    floating_letters = 'o'
    locked_letters = 't__r_'
    word_length = 5

    possible_permutations = generate_letter_permutations(
        floating_letters, word_length)

    # merge permutations and reduce by known letter positions
    valid_permutations = merge_patterns(locked_letters, possible_permutations)

    print(get_words_from_pattern(valid_permutations, five_words))
