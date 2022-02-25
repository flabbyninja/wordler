import unittest
import mapper


class TestGetWordsSpecifiedLength(unittest.TestCase):

    def setUp(self):
        self.test_words = ['Fiver', 'Chicken', 'Alone', 'Alive',
                           'Irate', 'Banana', 'Tractor', 'Sun']

    def test_non_zero_exists(self):
        filtered_words = mapper.get_words_specified_length(5, self.test_words)
        self.assertEqual(filtered_words, ['Fiver', 'Alone', 'Alive', 'Irate'])
        filtered_words = mapper.get_words_specified_length(3, self.test_words)
        self.assertEqual(filtered_words, ['Sun'])

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
            ['_ct_', '_tc_', 'c_t_', 't_c_', 'ct__', 'tc__'])

    def test_merge_all_valid(self):
        self.assertSetEqual(mapper.merge_patterns(
            '___a', set(['c___', '_t__']), self.test_permutations), set(['_cta', 't_ca', 'tc_a']))

    def test_merge_inequal_length(self):
        self.assertSetEqual(
            mapper.merge_patterns('____a', set(
                ['c_', '_t_____']), self.test_permutations), set(['_ct_', 't_c_', 'tc__'])
        )
        self.assertSetEqual(
            mapper.merge_patterns(
                'a_', set(['c_', '_t_____']), self.test_permutations), set(['act_']))

    def test_merge_empty_permutations(self):
        self.assertSetEqual(mapper.merge_patterns(
            '_a_', set(), set()), set(['_a_']))

    def test_merge_empty_floating(self):
        self.assertSetEqual(mapper.merge_patterns(
            '_a_', set(), self.test_permutations), set(['cat_', 'tac_']))

    def test_merge_empty_locked_floating(self):
        self.assertSetEqual(mapper.merge_patterns(
            '', set(), self.test_permutations), self.test_permutations)

    def test_merge_floating_locked_overlap(self):
        self.assertSetEqual(mapper.merge_patterns(
            'ca__', set(['___c', '_t__']), self.test_permutations), set(['cat_']))

    def test_merge_empty_locked(self):
        self.assertSetEqual(mapper.merge_patterns('', set(
            ['c__', '_t__']), self.test_permutations), set(['_ct_', 't_c_', 'tc__']))
        self.assertSetEqual(mapper.merge_patterns(None, set(
            ['c__', '_t__']), self.test_permutations), set(['_ct_', 't_c_', 'tc__']))

    def test_merge_all_locked_letters(self):
        self.assertSetEqual(mapper.merge_patterns(
            'cate', set(), self.test_permutations), set(['cate']))


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


class TestCollectFloatingLetters(unittest.TestCase):
    def setUp(self):
        self.floating_patterns = ['i____', '____s', '_r_m_']

    def test_collect_standard(self):
        self.assertListEqual(sorted(mapper.collect_floating_letters(self.floating_patterns, 5)),
                             ['i', 'm', 'r', 's'])

    def test_collect_multi_same_letter(self):
        multi_patterns = self.floating_patterns.copy()
        multi_patterns.append('__i_i')
        self.assertListEqual(sorted(mapper.collect_floating_letters(multi_patterns, 5)),
                             ['i', 'i', 'm', 'r', 's'])

    def test_collect_patterns_blank(self):
        self.assertListEqual(
            mapper.collect_floating_letters(['_____'], 5), [])
        self.assertListEqual(mapper.collect_floating_letters([], 5), [])

    def test_collect_patterns_none(self):
        self.assertIsNone(mapper.collect_floating_letters(None, 5), [])

    def test_collect_pattern_size_smaller_than_template(self):
        self.assertListEqual(sorted(mapper.collect_floating_letters(
            ['_a_b_c'], 5)), ['a', 'b'])

    def test_collect_zero_pattern_size(self):
        self.assertListEqual(mapper.collect_floating_letters(
            ['_a_b_c'], 0), [])

    def test_collect_pattern_size_larger_than_template(self):
        self.assertListEqual(sorted(mapper.collect_floating_letters(
            ['_a_b_c'], 10)), ['a', 'b', 'c'])


class TestProcessAllPatterns(unittest.TestCase):
    def setUp(self):
        self.input_patterns = ['a__b_', '_aa_c', 'b__bz', 'z__c_']

    def test_process_standard(self):
        self.assertListEqual(
            mapper.process_all_patterns(self.input_patterns),
            [{'a': 1, 'b': 1}, {'a': 2, 'c': 1}, {'b': 2, 'z': 1}, {'z': 1, 'c': 1}])

    def test_process_empty(self):
        self.assertListEqual(
            mapper.process_all_patterns([]), [])

    def test_process_all_blank(self):
        self.assertListEqual(
            mapper.process_all_patterns(['_____', '_____', '_____']),  [])

    def test_process_none(self):
        self.assertIsNone(mapper.process_all_patterns(None))


class TestReducePatterns(unittest.TestCase):
    def setUp(self):
        self.input_patterns = [{'a': 1, 'b': 2},
                               {'c': 2, 'b': 1}, {'a': 4, 'z': 1}]

    def test_reduce_standard(self):
        self.assertDictEqual(mapper.reduce_patterns(self.input_patterns), {
                             'a': 4, 'b': 2, 'c': 2, 'z': 1})

    def test_reduce_none(self):
        self.assertIsNone(mapper.reduce_patterns(None))

    def test_reduce_empty(self):
        self.assertDictEqual(mapper.reduce_patterns([{}, {}, {}]),
                             {})
        self.assertDictEqual(mapper.reduce_patterns([]),
                             {})


if __name__ == '__main__':
    unittest.main()
