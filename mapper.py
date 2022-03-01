import collections
from itertools import permutations
import re
from typing import Dict, List, Set


def load_words(filename) -> List[str]:
    """Load words from file

    File format should be one word per line

    Arguments:
    filename: the file containing words to load

    Return: list of words
    """
    with open(filename) as word_file:
        valid_words = set(word_file.read().split())

    return valid_words


def get_words_specified_length(length, input_data) -> List[str]:
    """Get words of a specific size

    Filter and return input list of words, only returning those of a given size

    Arguments:
    length: length of words to return
    input_data: list of words to be filtered    

    Return: list of filtered words of specified length
    """
    return list(map(lambda x: x, filter(lambda x: len(x) == length, input_data)))


def get_words_from_pattern(pattern_list, excluded_letters, word_list) -> Set[str]:
    """Return words that match patterns, without any of the excluded letters

    For each of the list of patterns provided, check which words in the word list can provide a match.
    Candidate words will have none of the excluded letters in them.

    Arguments:
    pattern_list: list of patterns that possible words can meet e.g. c_t would match cat, cut, cot etc
    excluded_letters: a string containing letters that cannot be in any candidate words
    word_list: list of valid candidate words that will be filtered down

    Return: list of words that match
    """
    potential_words = set()
    for pattern in pattern_list:
        potential_words.update(set(
            filter(lambda x: is_word_a_pattern_match(pattern, excluded_letters, x), word_list)))
    return potential_words


def is_word_a_pattern_match(pattern, excluded_letters, word) -> bool:
    """Check that a specific pattern, excluding letters, matches word

    Arguments:
    pattern: pattern to be validated
    excluded_letters: string of character to be excluded from potential matches
    word: the word to be validated    

    Return: True if word is a match, otherwise False
    """
    if (len(pattern) == 0) or (len(word) == 0) or (len(pattern) != len(word)):
        return False
    if (len(excluded_letters) > 0) and (re.match('^[^' + excluded_letters + ']+$', word) is None):
        return False
    for i, c in enumerate(pattern):
        if (c != '_') and (c.lower() != word[i].lower()):
            return False
    return True


def generate_letter_permutations(letters, word_length) -> Set[str]:
    """Generate possible permutations of word patterns

    Take a set of possible letters and a word length and generate possible word masks for all combinations.
    If word_length is larger than letters provided, will be padded out with the mask character showing where
    letters can be replaced

    Arguments:
    letters: string containing letters to be present in final word
    word_length: lenght of word patterns to be generated

    Returns: list of words patterns for candidate words e.g. c_t that could match cat, cot, cut etc 
    """
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


def merge_patterns(locked_letters, floating_patterns, permutations) -> List[str]:
    """Merge a list of candidate patterns with known letter positions and known incorrect positions

    Take a list of permutations, overlaying locked letters where they are blank. If permutation has 
    different letter in locked position, discard that permutation. Look at all floating patterns. Discard all
    permutations which use valid letters in positions they're known not to occur. Return the list of permutations left.

    Arguments:
    locked_letters: pattern of letters with known positions e.g. ___l_
    floating_patterns: list of patterns where known letters are known to not occur e.g. _a_e_
    permutations: list of possible permutations of all letters

    Return: list of valid permutations
    """
    if not floating_patterns and not locked_letters:
        return permutations

    if not permutations:
        return set([locked_letters])

    merged_permutations = set()

    for perm in permutations:
        accept = True

        if not locked_letters:
            locked_letters = ''

        # overlay locked letters
        # count number of each letter in pattern

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


def get_letters_for_permutations(floating_patterns, locked_pattern, word_length) -> str:
    """Get string of valid letters for permutations 

    Retrieve from floating patterns and locked pattern. If letter has been excluded from all floating pattern
    positions except the locked position, this will still count extra instances. It is not valid config as the
    situation can't happen. Fix the input.

    Arguments:
    floating_patterns: list of floating patterns for word
    word_length: length of word to be matched

    Return: a string containing all the letters to be used for permutations
    """
    final_letters = locked_pattern.replace('_', '')
    return final_letters.join([str(elem) for elem in collect_floating_letters(
        floating_patterns, word_length)])


def collect_floating_letters(floating_patterns, pattern_size) -> List[str]:
    """Collect all letters from a set of patterns

    If pattern is larger than word, truncate it. Include all unique letters the number of times
    they were in the pattern that contained them the most.

    Arguments:
    floating_patterns: list of floating patterns e.g. ['_a_', 'bu_']
    pattern_size: the length of word the patterns are being reduced for

    Return: list of collected letters

    Exception: if number of letters collected is larger than the pattern size
    """
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
            if len(collected_letters) >= pattern_size:
                raise Exception
            collected_letters.append(key)

    return collected_letters


def process_all_patterns(floating_patterns) -> List[Dict[str, int]]:
    """Convert list of floating patterns to a list of dictionaries containing a count of letters

    Arguments:
    floating_patterns: list of string patterns e.g. ['a_b_c', 'bb_a']

    Return: list of dictionaries containing letter frequency [{'a':1, 'b':1, 'c':1}, {'b':2, 'a':1}]
    """
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


def reduce_patterns(pattern_dicts) -> Dict[str, int]:
    """Merge multiple character count dictionaries

    Reduce a list of character count dictionaries from pattern strings, merging so that one resulting dictionary
    is created that contains each letter, and number of occurrences from the pattern that had the maximum 

    Arguments:
    pattern_dicts: list of pattern dictionaries with character counts e.g. [{'a': 1, 'b': 2}, {'c':2, 'b':1}, {'a':4, 'z': 1}]

    Return: dictionary containing max count of each letters across all occurrences e.g. {'a': 4, 'b': 2, 'c':2, 'z':1}
    """
    if pattern_dicts is None:
        return None

    merged_dict = {}

    for instance in pattern_dicts:
        for key in instance:
            if key in merged_dict:
                if instance[key] > merged_dict[key]:
                    merged_dict[key] = instance[key]
            else:
                merged_dict[key] = instance[key]

    return merged_dict


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
