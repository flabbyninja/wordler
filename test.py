import unittest
import mapper

test_words = ['Fiver', 'Chicken', 'Alone', 'Alive',
              'Irate', 'Banana', 'Tractor', 'Sun']


class TestGetWordsSpecifiedLength(unittest.TestCase):

    def test_non_zero_exists(self):
        filtered_words = mapper.get_words_specified_length(5, test_words)
        self.assertEqual(filtered_words, ['Fiver', 'Alone', 'Alive', 'Irate'])

    def test_non_zero_notexist(self):
        filtered_words = mapper.get_words_specified_length(10, test_words)
        self.assertFalse(filtered_words)

    def test_empty_word_list(self):
        test_words = []
        filtered_words = mapper.get_words_specified_length(5, test_words)
        self.assertFalse(filtered_words)


class TestIsWordPatternMatch(unittest.TestCase):

    def test_valid_word_no_excluded_letters(self):
        self.assertTrue(mapper.is_word_a_pattern_match('___l_', '', 'apple'))
        self.assertTrue(mapper.is_word_a_pattern_match('___L_', '', 'apple'))
        self.assertTrue(mapper.is_word_a_pattern_match('___l_', '', 'appLe'))
        self.assertTrue(mapper.is_word_a_pattern_match(
            'ch_c__n', '', 'chicken'))

    def test_valid_word_excluded_letters(self):
        self.assertTrue(mapper.is_word_a_pattern_match(
            '___l_', 'zxc', 'apple'))
        self.assertTrue(mapper.is_word_a_pattern_match(
            'appl_', 'bzcqwtm', 'apple'))
        self.assertFalse(mapper.is_word_a_pattern_match(
            'appl_', 'e', 'apple'))

    def test_invalid_word_no_excluded_letters(self):
        self.assertFalse(mapper.is_word_a_pattern_match(
            '___l_', '', 'cheese'))

    def test_invalid_word_excluded_letters(self):
        self.assertFalse(mapper.is_word_a_pattern_match(
            '___l_', 'abcdef', 'cheese'))

    def test_valid_word_excluded_skip_char(self):
        self.assertFalse(mapper.is_word_a_pattern_match(
            '___l_', '_', 'cheese'))

    def test_invalid_word_excluded_skip_char(self):
        self.assertTrue(mapper.is_word_a_pattern_match(
            '___l_', '_', 'apple'))

    def test_empty(self):
        self.assertFalse(mapper.is_word_a_pattern_match(
            '___l_', 'abcd', ''))
        self.assertTrue(mapper.is_word_a_pattern_match(
            '___l_', '', 'apple'))
        self.assertFalse(mapper.is_word_a_pattern_match(
            '', 'abcd', 'apple'))
        self.assertFalse(mapper.is_word_a_pattern_match(
            '___l_', '', ''))
        self.assertFalse(mapper.is_word_a_pattern_match(
            '', 'abcd', ''))
        self.assertFalse(mapper.is_word_a_pattern_match(
            '', '', 'apple'))
        self.assertFalse(mapper.is_word_a_pattern_match(
            '', '', ''))

    def test_pattern_too_small_for_word(self):
        self.assertFalse(mapper.is_word_a_pattern_match(
            '___l_', '', 'apples'))

    def test_pattern_too_big_for_word(self):
        self.assertFalse(mapper.is_word_a_pattern_match(
            '___l__', '', 'apple'))

    def test_pattern_full_word(self):
        self.assertTrue(mapper.is_word_a_pattern_match(
            'apple', '', 'apple'))

    def test_full_alphabet_excluded(self):
        self.assertFalse(mapper.is_word_a_pattern_match(
            '___l_', 'abcdefghijklmnopqrstuvwxyz', 'apple'))


class TestGenerateLetterPermutations(unittest.TestCase):

    def test_generate_valid(self):
        permutations = mapper.generate_letter_permutations('ab', 3)
        intended_result = set(
            ['ab_', 'ba_', 'a_b', 'b_a', '_ab', '_ba'])
        self.assertSetEqual(permutations, intended_result)

        permutations = mapper.generate_letter_permutations('a', 2)
        intended_result = set(
            ['a_', '_a'])
        self.assertSetEqual(permutations, intended_result)

        permutations = mapper.generate_letter_permutations('x', 3)
        intended_result = set(
            ['x__', '_x_', '__x'])
        self.assertSetEqual(permutations, intended_result)

    def test_generate_invalid(self):
        permutations = mapper.generate_letter_permutations('', 5)
        intended_result = set(
            ['_____'])
        self.assertSetEqual(permutations, intended_result)

        permutations = mapper.generate_letter_permutations('abcde', 0)
        intended_result = set([])
        self.assertSetEqual(permutations, intended_result)

    def test_truncate_when_too_large(self):
        permutations = mapper.generate_letter_permutations('abcdef', 2)
        intended_result = set(
            ['ab', 'ba'])
        self.assertSetEqual(permutations, intended_result)


if __name__ == '__main__':
    unittest.main()
