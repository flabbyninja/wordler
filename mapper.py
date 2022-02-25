import collections
from itertools import permutations
import re


def get_words_specified_length(length, input_data):
    return list(map(lambda x: x, filter(lambda x: len(x) == length, input_data)))


def get_words_from_pattern(pattern_list, excluded_letters, word_list, ):
    potential_words = set()
    for pattern in pattern_list:
        potential_words.update(set(
            filter(lambda x: is_word_a_pattern_match(pattern, excluded_letters, x), word_list)))
    return potential_words


def is_word_a_pattern_match(pattern, excluded_letters, word):
    if (len(pattern) == 0) or (len(word) == 0) or (len(pattern) != len(word)):
        return False
    if (len(excluded_letters) > 0) and (re.match('^[^' + excluded_letters + ']+$', word) is None):
        return False
    for i, c in enumerate(pattern):
        if (c != '_') and (c.lower() != word[i].lower()):
            return False
    return True


def generate_letter_permutations(letters, word_length):
    # Get all permutations of candidate letters, padded out to length of word chosen
    permutation_output = set()
    if len(letters) < word_length:
        letters += '_' * (word_length - len(letters))
    if len(letters) > word_length:
        letters = letters[:word_length]
    if len(letters) > 0:
        perm = permutations(letters)
        perms_to_process = set(perm)
        for i in perms_to_process:
            permutation_output.add("".join([str(elem) for elem in i]))

    return permutation_output


def merge_patterns(locked_letters, floating_patterns, permutations):

    if not floating_patterns and not locked_letters:
        return permutations

    if not permutations:
        return set([locked_letters])

    merged_permutations = set()

    for perm in permutations:
        accept = True

        if not locked_letters:
            locked_letters = ''

        # Overlay locked letter pattern
        if not locked_letters or len(locked_letters) < len(perm):
            locked_letters += '_' * (len(perm) - len(locked_letters))
        for i, c in enumerate(perm):
            if locked_letters[i] != '_':
                if c != '_' and c != locked_letters[i]:
                    accept = False
                    break
                else:
                    perm = perm[:i] + locked_letters[i] + perm[i+1:]

        for floater in floating_patterns:
            if not accept:
                break

            if len(floater) < len(perm):
                floater += '_' * (len(perm) - len(floater))

            if len(floater) > len(perm):
                floater = floater[:len(perm)]

            # overlay floating_patterns if permutation hasn't been rejected by locked overlay
            if accept:
                for i, c in enumerate(floater):
                    if perm[i] != '_':
                        if c == perm[i]:
                            accept = False
                            break
                if not accept:
                    break

        if accept:
            merged_permutations.add(perm)

    return merged_permutations


def get_letters_for_permutations(floating_patterns, word_length):
    return "".join([str(elem) for elem in collect_floating_letters(
        floating_patterns, word_length)])


def load_words(test_data):
    if not test_data:
        with open('./data/words_alpha.txt') as word_file:
            valid_words = set(word_file.read().split())
    else:
        valid_words = ['Fiver', 'Chicken', 'Alone',
                       'Irate', 'Banana', 'Tractor', 'Sun']

    return valid_words


def calc_letter_frequency(word_list, floating_letters, locked_letters, remove_known=False):
    # build one string of all characters from potential valid words
    response_for_collection = ''
    for word in word_list:
        response_for_collection += word

    if remove_known:
        # Assemble all letters that are already known
        total_to_remove = floating_letters + locked_letters
        total_to_remove = total_to_remove.replace('_', '')

        # remove known from all characters to give those that should be guessed
        for l in total_to_remove:
            response_for_collection = response_for_collection.replace(l, '')

    return collections.Counter(response_for_collection)


def collect_floating_letters(floating_patterns, pattern_size):
    if floating_patterns is None:
        return None

    all_patterns_counted = []

    # ensure all the floating patterns are truncated to the right length
    truncated_patterns = map(lambda x: x[:pattern_size], floating_patterns)

    processed_patterns = process_all_patterns(truncated_patterns)
    reduced_patterns = reduce_patterns(processed_patterns)

    collected_letters = []
    for key in reduced_patterns:
        for x in range(reduced_patterns[key]):
            collected_letters.append(key)

    return collected_letters


def process_all_patterns(floating_patterns):
    if floating_patterns is None:
        return None

    processed_patterns = []

    for pattern in floating_patterns:
        alpha_chars = pattern.replace('_', '')

        if not alpha_chars:
            break

        unique_chars_in_pattern = set([c for c in alpha_chars])

        # build ongoing dict of characters against max times they appear in a pattern
        pattern_dict = {k: alpha_chars.count(k)
                        for k in unique_chars_in_pattern}

        processed_patterns.append(pattern_dict)

    return processed_patterns


def reduce_patterns(pattern_dicts):
    if pattern_dicts is None:
        return None

    merged_dict = {}

    # all_count = [{'a': 1, 'b': 2}, {'c':2, 'b':1}, {'a':4, 'z': 1}]
    # reduced {'a': 4, 'b': 2, 'c':2, 'z':1}
    for instance in pattern_dicts:
        for key in instance:
            if key in merged_dict:
                if instance[key] > merged_dict[key]:
                    merged_dict[key] = instance[key]
            else:
                merged_dict[key] = instance[key]

    return merged_dict
