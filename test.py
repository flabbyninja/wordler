from cgi import test
import unittest
import mapper


class TestGetWordsSpecifiedLength(unittest.TestCase):

    def setUp(self):
        self.test_words = ['Fiver', 'Chicken', 'Alone', 'Alive',
                           'Irate', 'Banana', 'Tractor', 'Sun']

    def test_non_zero_exists(self):
        filtered_words = mapper.get_words_specified_length(5, self.test_words)
        self.assertEqual(filtered_words, ['Fiver', 'Alone', 'Alive', 'Irate'])

    def test_non_zero_notexist(self):
        filtered_words = mapper.get_words_specified_length(10, self.test_words)
        self.assertFalse(filtered_words)

    def test_empty_word_list(self):
        filtered_words = mapper.get_words_specified_length(5, [])
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


class TestMergePatterns(unittest.TestCase):
    def setUp(self):
        self.test_permutations = set(
            ['_ct', '_tc', 'c_t', 't_c', 'ct_', 'tc_'])

    def test_merge_valid(self):
        self.assertSetEqual(mapper.merge_patterns(
            '_a_', self.test_permutations), set(['tac', 'cat']))
        self.assertSetEqual(mapper.merge_patterns(
            'a__', self.test_permutations), set(['act', 'atc']))

    def test_merge_inequal_length(self):
        self.assertSetEqual(mapper.merge_patterns(
            '___a', self.test_permutations), self.test_permutations)
        self.assertSetEqual(mapper.merge_patterns(
            'a_', self.test_permutations), set(['act', 'atc']))

    def test_merge_empty_permutations(self):
        self.assertSetEqual(mapper.merge_patterns('_a_', set()), set(['_a_']))

    def test_merge_all_locked_letters(self):
        self.assertSetEqual(mapper.merge_patterns(
            'cat', self.test_permutations), set(['cat']))

    def test_merge_no_locked_letters(self):
        self.assertSetEqual(mapper.merge_patterns(
            '___', self.test_permutations), self.test_permutations)


class TestCalcLetterFrequency(unittest.TestCase):
    def setUp(self):
        self.test_words_for_calc = set(
            ['cat', 'bat', 'rat', 'car', 'far', 'fat', 'baa'])

    def test_no_floating_or_locked_no_remove(self):
        self.assertDictEqual(dict(mapper.calc_letter_frequency(
            self.test_words_for_calc, '', '', False)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})
        self.assertDictEqual(dict(mapper.calc_letter_frequency(
            self.test_words_for_calc, '', '')), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})
        self.assertDictEqual(dict(mapper.calc_letter_frequency(
            self.test_words_for_calc, '', '_____', False)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    def test_no_floating_or_locked_remove(self):
        self.assertDictEqual(dict(mapper.calc_letter_frequency(
            self.test_words_for_calc, '', '', True)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    # def test_floating_remove(self):
    #     self.assertDictEqual(dict(mapper.calc_letter_frequency(
    #         self.test_words_for_calc, '', '', True)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    # def test_floating_no_remove(self):
    #     self.assertDictEqual(dict(mapper.calc_letter_frequency(
    #         self.test_words_for_calc, '', '', True)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    # def test_locked_remove(self):
    #     self.assertDictEqual(dict(mapper.calc_letter_frequency(
    #         self.test_words_for_calc, '', '_a_', True)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    # def test_locked_no_remove(self):
    #     self.assertDictEqual(dict(mapper.calc_letter_frequency(
    #         self.test_words_for_calc, '', '', False)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    # def test_floating_and_locked_remove(self):
    #     self.assertDictEqual(dict(mapper.calc_letter_frequency(
    #         self.test_words_for_calc, '', '', True)),{'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    def test_over_under_empty_locked_length(self):
        self.assertDictEqual(dict(mapper.calc_letter_frequency(
            self.test_words_for_calc, '', '_______', False)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})
        self.assertDictEqual(dict(mapper.calc_letter_frequency(
            self.test_words_for_calc, '', '___', False)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})


if __name__ == '__main__':
    unittest.main()
