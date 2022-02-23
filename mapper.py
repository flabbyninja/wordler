from itertools import permutations
import re


def get_words_specified_length(length, input_data):
    return list(map(lambda x: x.lower(), filter(lambda x: len(x) == length, input_data)))


def get_words_locked_position(finalized_letters, word):
    for i, x in enumerate(word):
        if (finalized_letters[i] != '_') and (finalized_letters[i] != x):
            return False
    return True


def get_words_from_pattern(pattern_list, excluded_letters, word_list, ):
    potential_words = set()
    for pattern in pattern_list:
        potential_words.update(set(
            filter(lambda x: is_word_a_pattern_match(pattern, excluded_letters, x), word_list)))
    return potential_words


def is_word_a_pattern_match(pattern, excluded_letters, word):
    if len(pattern) != len(word):
        return False
    if (len(excluded_letters) > 0) and (re.match('^[^' + excluded_letters + ']+$', word) is None):
        return False
    for i, c in enumerate(pattern):
        if (c != '_') and (c.lower() != word[i].lower()):
            return False
    return True


def generate_letter_permutations(letters, word_length):
    # Get all permutations of candidate letters, padded out to length of word chosen
    if len(letters) < word_length:
        letters += '_' * (word_length - len(letters))
    if len(letters) > word_length:
        letters = letters[:word_length]
    perm = permutations(letters)
    permutation_output = set()

    for i in set(perm):
        permutation_output.add("".join([str(elem) for elem in i]))

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


def load_words(test_data):
    if not test_data:
        with open('./data/words_alpha.txt') as word_file:
            valid_words = set(word_file.read().split())
    else:
        valid_words = ['Fiver', 'Chicken', 'Alone',
                       'Irate', 'Banana', 'Tractor', 'Sun']

    return valid_words
