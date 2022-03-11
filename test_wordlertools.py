import unittest
import wordlertools.pattern_processor as pattern_processor


class TestGetWordsSpecifiedLength(unittest.TestCase):

    def setUp(self):
        self.test_words = {'Fiver', 'Chicken', 'Alone', 'Alive',
                           'Irate', 'Banana', 'Tractor', 'Sun'}

    def test_non_zero_exists(self):
        filtered_words = pattern_processor.get_words_specified_length(
            5, self.test_words)
        self.assertEqual(filtered_words, {'Fiver', 'Alone', 'Alive', 'Irate'})
        filtered_words = pattern_processor.get_words_specified_length(
            3, self.test_words)
        self.assertEqual(filtered_words, {'Sun'})

    def test_non_zero_notexist(self):
        filtered_words = pattern_processor.get_words_specified_length(
            10, self.test_words)
        self.assertFalse(filtered_words)

    def test_empty_word_list(self):
        filtered_words = pattern_processor.get_words_specified_length(5, set())
        self.assertFalse(filtered_words)


class TestIsWordPatternMatch(unittest.TestCase):

    def test_valid_word_no_excluded_letters(self):
        self.assertTrue(
            pattern_processor.is_word_a_pattern_match('___l_', '', 'apple'))
        self.assertTrue(
            pattern_processor.is_word_a_pattern_match('___L_', '', 'apple'))
        self.assertTrue(
            pattern_processor.is_word_a_pattern_match('___l_', '', 'appLe'))
        self.assertTrue(pattern_processor.is_word_a_pattern_match(
            'ch_c__n', '', 'chicken'))

    def test_valid_word_excluded_letters(self):
        self.assertTrue(pattern_processor.is_word_a_pattern_match(
            '___l_', 'zxc', 'apple'))
        self.assertTrue(pattern_processor.is_word_a_pattern_match(
            'appl_', 'bzcqwtm', 'apple'))
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            'appl_', 'e', 'apple'))

    def test_invalid_word_no_excluded_letters(self):
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            '___l_', '', 'cheese'))

    def test_invalid_word_excluded_letters(self):
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            '___l_', 'abcdef', 'cheese'))

    def test_valid_word_excluded_skip_char(self):
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            '___l_', '_', 'cheese'))

    def test_invalid_word_excluded_skip_char(self):
        self.assertTrue(pattern_processor.is_word_a_pattern_match(
            '___l_', '_', 'apple'))

    def test_empty(self):
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            '___l_', 'abcd', ''))
        self.assertTrue(pattern_processor.is_word_a_pattern_match(
            '___l_', '', 'apple'))
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            '', 'abcd', 'apple'))
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            '___l_', '', ''))
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            '', 'abcd', ''))
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            '', '', 'apple'))
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            '', '', ''))

    def test_pattern_too_small_for_word(self):
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            '___l_', '', 'apples'))

    def test_pattern_too_big_for_word(self):
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            '___l__', '', 'apple'))

    def test_pattern_full_word(self):
        self.assertTrue(pattern_processor.is_word_a_pattern_match(
            'apple', '', 'apple'))

    def test_full_alphabet_excluded(self):
        self.assertFalse(pattern_processor.is_word_a_pattern_match(
            '___l_', 'abcdefghijklmnopqrstuvwxyz', 'apple'))


class TestGenerateLetterPermutations(unittest.TestCase):

    def test_generate_valid(self):
        permutations = pattern_processor.generate_letter_permutations('ab', 3)
        intended_result = {'ab_', 'ba_', 'a_b', 'b_a', '_ab', '_ba'}
        self.assertSetEqual(permutations, intended_result)

        permutations = pattern_processor.generate_letter_permutations('a', 2)
        intended_result = {'a_', '_a'}
        self.assertSetEqual(permutations, intended_result)

        permutations = pattern_processor.generate_letter_permutations('x', 3)
        intended_result = {'x__', '_x_', '__x'}
        self.assertSetEqual(permutations, intended_result)

    def test_generate_invalid(self):
        permutations = pattern_processor.generate_letter_permutations('', 5)
        intended_result = {'_____'}
        self.assertSetEqual(permutations, intended_result)

        permutations = pattern_processor.generate_letter_permutations(
            'abcde', 0)
        intended_result = set()
        self.assertSetEqual(permutations, intended_result)

    def test_truncate_when_too_large(self):
        permutations = pattern_processor.generate_letter_permutations(
            'abcdef', 2)
        intended_result = {'ab', 'ba'}
        self.assertSetEqual(permutations, intended_result)


class TestGetLettersForPermutations(unittest.TestCase):
    def test_get_letters_permutations_distinct(self):
        self.assertListEqual(sorted([c for c in pattern_processor.get_letters_for_permutations(
            {'a___', '_b__'}, '___c', 4)]), sorted([c for c in 'abc']))

    def test_get_letters_permutations_overlap(self):
        self.assertListEqual(sorted([c for c in pattern_processor.get_letters_for_permutations(
            {'a___', '_b__'}, '_c__', 4)]), sorted([c for c in 'abc']))

    def test_get_letters_permutations_multiple(self):
        self.assertListEqual(sorted([c for c in pattern_processor.get_letters_for_permutations(
            {'aa__', '_b__'}, '___c', 4)]), sorted([c for c in 'aabc']))
        self.assertListEqual(sorted([c for c in pattern_processor.get_letters_for_permutations(
            {'a___', '_b_b'}, '___c', 4)]), sorted([c for c in 'abbc']))

    def test_get_letters_permutations_all_floating_except_locked(self):
        self.assertListEqual(sorted([c for c in pattern_processor.get_letters_for_permutations(
            {'a___', '_a__', '__a_'}, '___a', 4)]), ['a'])
        self.assertListEqual(sorted([c for c in pattern_processor.get_letters_for_permutations(
            {'a___', '_a__'}, '___a', 4)]), [c for c in 'aa'])

    def test_get_letters_permutations_empty_locked(self):
        self.assertListEqual(sorted([c for c in pattern_processor.get_letters_for_permutations(
            {'a___', '_b__'}, '', 4)]), sorted([c for c in 'ab']))
        self.assertListEqual(sorted([c for c in pattern_processor.get_letters_for_permutations(
            {'a___', '_b__'}, None, 4)]), sorted([c for c in 'ab']))

    def test_get_letters_permutations_empty_floating(self):
        self.assertListEqual(sorted([c for c in pattern_processor.get_letters_for_permutations(
            set(), '___c', 4)]), sorted([c for c in 'c']))
        self.assertListEqual(sorted([c for c in pattern_processor.get_letters_for_permutations(
            None, '___c', 4)]), sorted([c for c in 'c']))

    def test_get_letters_permutations_length_smaller(self):
        self.assertListEqual(sorted([c for c in pattern_processor.get_letters_for_permutations(
            {'a_', '_b'}, '___c', 4)]), sorted([c for c in 'abc']))

    def test_get_letters_permutations_length_larger(self):
        self.assertListEqual(sorted([c for c in pattern_processor.get_letters_for_permutations(
            {'a_____', '_b__qz'}, '___c', 4)]), sorted([c for c in 'abc']))


class TestIsLockedOnlyOneLeft(unittest.TestCase):

    def test_normal(self):
        self.assertTrue(pattern_processor.is_locked_only_one_left(
            'a', {'a___', '_a__', '___a'}, '__a_'))
        self.assertFalse(pattern_processor.is_locked_only_one_left(
            'a', {'a___', '_a__'}, '__a_'))

    def test_floating_empty(self):
        self.assertFalse(
            pattern_processor.is_locked_only_one_left('a', set(), '__a_'))

    def test_locked_empty(self):
        self.assertFalse(pattern_processor.is_locked_only_one_left(
            'a', {'a___', '_a__', '___a'}, ''))

    def test_letter_in_one_not_other(self):
        self.assertFalse(pattern_processor.is_locked_only_one_left(
            'a', {'b___', '_c__', '___d'}, '__a_'))


class TestMergePatterns(unittest.TestCase):
    def setUp(self):
        self.test_permutations = {
            '_cta', '_tca', 'c_ta', 't_ca', 'ct_a', 'tc_a'}

    def test_merge_all_valid(self):
        self.assertSetEqual(pattern_processor.merge_patterns(
            '___a', {'c___', '_t__'}, self.test_permutations), {'_cta', 't_ca', 'tc_a'})

    def test_merge_inequal_length(self):
        with self.assertRaises(Exception):
            _ = pattern_processor.merge_patterns('____a', {'c_', '_t_____'}, self.test_permutations), {
                '_cta', 't_ca', 'tc_a'}

        with self.assertRaises(Exception):
            _ = pattern_processor.merge_patterns(
                'a_', {'c_', '_t_____'}, self.test_permutations), {'act_'}

    def test_merge_empty_permutations(self):
        self.assertSetEqual(pattern_processor.merge_patterns(
            '_a_', set(), set()), {'_a_'})

    def test_merge_empty_floating(self):
        self.assertSetEqual(pattern_processor.merge_patterns(
            '_c__', set(), self.test_permutations), {'_cta', 'tc_a'})
        self.assertSetEqual(pattern_processor.merge_patterns(
            '_c__', {''}, self.test_permutations), {'_cta', 'tc_a'})

    def test_merge_empty_locked_floating(self):
        self.assertSetEqual(pattern_processor.merge_patterns(
            '', set(), self.test_permutations), self.test_permutations)

    def test_merge_floating_locked_overlap(self):

        permutations = {'ct_c', '_ctc', 'tc_c', 'ctc_', 'cc_t',
                        'c_tc', 'tcc_', '_tcc', 'c_ct', 'cct_', 't_cc', '_cct'}
        self.assertSetEqual(pattern_processor.merge_patterns(
            'ct__', {'___c'}, permutations), {'ctc_'})

    def test_merge_empty_locked(self):
        self.assertSetEqual(pattern_processor.merge_patterns(
            '', {'c___', '_t__'}, self.test_permutations), {'_cta', 't_ca', 'tc_a'})
        self.assertSetEqual(pattern_processor.merge_patterns(
            None, {'c___', '_t__'}, self.test_permutations), {'_cta', 't_ca', 'tc_a'})

    def test_merge_all_locked_letters(self):
        all_permutation = {'acte', 'tace', 'teac', 'atce', 'ecat', 'ceat', 'ceta', 'aect', 'ecta', 'eact', 'caet',
                           'ctae', 'tcae', 'tcea', 'ctea', 'acet', 'etac', 'teca', 'aetc', 'atec', 'eatc', 'etca', 'taec', 'cate'}
        self.assertSetEqual(pattern_processor.merge_patterns(
            'cate', set(), all_permutation), {'cate'})

    def test_merge_locked_and_floating_same_letter(self):
        self.assertSetEqual(pattern_processor.merge_patterns(
            '_a_', {'a__', '__b'}, {'aaa', 'aab', 'aba', 'abb', 'baa', 'bab', 'bba', 'bbb'}), {'baa'})

        big_permutations = {'aab_c', 'acab_', 'acb_a', 'bc_aa', 'bcaa_', 'cab_a', '_abca', 'aa_cb', 'c_baa', '_aacb', 'cba_a', 'aac_b', '_acab', 'a_cba', 'cbaa_', 'a_cab', '_caab', 'b_aac', 'abca_', 'ca_ba', 'caab_', 'bca_a', 'ab_ca', 'ca_ab', 'aacb_', 'aabc_', 'abc_a', '_baac', 'ac_ba',
                            'caba_', 'ba_ac', 'baa_c', '_cbaa', 'abac_', 'baac_', 'aca_b', '_abac', 'a_bac', '_caba', 'a_abc', 'b_aca', 'cb_aa', 'b_caa', '_acba', 'ba_ca', 'a_acb', 'bac_a', 'c_aab', 'caa_b', 'aa_bc', 'aba_c', 'baca_', '_bcaa', 'acba_', 'a_bca', 'ac_ab', 'ab_ac', '_baca', '_aabc', 'c_aba'}

        self.assertSetEqual(
            pattern_processor.merge_patterns(
                '____a', {'a_b__', '_a_b_'}, big_permutations),
            {'bc_aa', 'cba_a', 'bca_a', 'b_aca', 'cb_aa', 'b_caa', '_bcaa', '_baca'})


class TestCalcLetterFrequency(unittest.TestCase):
    def setUp(self):
        self.test_words_for_calc = set(
            ['cat', 'bat', 'rat', 'car', 'far', 'fat', 'baa'])

    def test_no_floating_or_locked_no_remove(self):
        self.assertDictEqual(dict(pattern_processor.calc_letter_frequency(
            self.test_words_for_calc, {''}, '', False)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})
        self.assertDictEqual(dict(pattern_processor.calc_letter_frequency(
            self.test_words_for_calc, {''}, '')), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})
        self.assertDictEqual(dict(pattern_processor.calc_letter_frequency(
            self.test_words_for_calc, {''}, '_____', False)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    def test_no_floating_or_locked_remove(self):
        self.assertDictEqual(dict(pattern_processor.calc_letter_frequency(
            self.test_words_for_calc, {''}, '', True)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    def test_floating_remove(self):
        self.assertDictEqual(dict(pattern_processor.calc_letter_frequency(
            self.test_words_for_calc, {''}, '', True)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    def test_floating_no_remove(self):
        self.assertDictEqual(dict(pattern_processor.calc_letter_frequency(
            self.test_words_for_calc, {''}, '', True)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    def test_locked_remove(self):
        self.assertDictEqual(dict(pattern_processor.calc_letter_frequency(
            self.test_words_for_calc, {''}, '_a_', True)), {'c': 2, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    def test_locked_no_remove(self):
        self.assertDictEqual(dict(pattern_processor.calc_letter_frequency(
            self.test_words_for_calc, {''}, '_a_', False)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})

    def test_floating_and_locked_remove(self):
        self.assertDictEqual(dict(pattern_processor.calc_letter_frequency(
            self.test_words_for_calc, {'_a_'}, '_b_', True)), {'c': 2, 't': 4, 'r': 3, 'f': 2})

    def test_over_under_empty_locked_length(self):
        self.assertDictEqual(dict(pattern_processor.calc_letter_frequency(
            self.test_words_for_calc, {''}, '_______', False)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})
        self.assertDictEqual(dict(pattern_processor.calc_letter_frequency(
            self.test_words_for_calc, {''}, '___', False)), {'c': 2, 'a': 8, 't': 4, 'b': 2, 'r': 3, 'f': 2})


class TestCollectFloatingLetters(unittest.TestCase):
    def setUp(self):
        self.floating_patterns = {'i____', '____s', '_r_m_'}

    def test_collect_standard(self):
        patterns = pattern_processor.collect_floating_letters(
            self.floating_patterns, 5)
        assert patterns is not None
        self.assertListEqual(sorted(patterns), ['i', 'm', 'r', 's'])

    def test_collect_multi_same_letter(self):
        multi_patterns = self.floating_patterns.copy()
        multi_patterns.add('__i_i')
        patterns = pattern_processor.collect_floating_letters(
            multi_patterns, 5)
        assert patterns is not None
        self.assertListEqual(sorted(patterns), ['i', 'i', 'm', 'r', 's'])

    def test_collect_patterns_blank(self):
        patterns = pattern_processor.collect_floating_letters({'_____'}, 5)
        assert patterns is not None
        self.assertListEqual(patterns, [])

        patterns = pattern_processor.collect_floating_letters(set(), 5)
        assert patterns is not None
        self.assertListEqual(patterns, [])

    def test_collect_patterns_none(self):
        self.assertIsNone(
            pattern_processor.collect_floating_letters(None, 5), [])

    def test_collect_pattern_size_smaller_than_template(self):
        patterns = pattern_processor.collect_floating_letters({'_a_b_c'}, 5)
        assert patterns is not None
        self.assertListEqual(sorted(patterns), ['a', 'b'])

    def test_collect_zero_pattern_size(self):
        patterns = pattern_processor.collect_floating_letters({'_a_b_c'}, 0)
        assert patterns is not None
        self.assertListEqual(patterns, [])

    def test_collect_pattern_size_larger_than_template(self):
        patterns = pattern_processor.collect_floating_letters({'_a_b_c'}, 10)
        assert patterns is not None
        self.assertListEqual(sorted(patterns), ['a', 'b', 'c'])

    def test_collect_more_than_word_length(self):
        with self.assertRaises(Exception):
            pattern_processor.collect_floating_letters(
                {'a_b_', 'c_d_', 'e_f_'}, 4)


class TestProcessAllPatterns(unittest.TestCase):
    def setUp(self):
        self.input_patterns = {'a__b_', '_aa_c', 'b__bz', 'z__c_'}

    def test_process_standard(self):
        patterns = pattern_processor.process_all_patterns(self.input_patterns)
        assert patterns is not None
        self.assertCountEqual(patterns, [{'a': 1, 'b': 1}, {'a': 2, 'c': 1}, {
                              'b': 2, 'z': 1}, {'z': 1, 'c': 1}])

    def test_process_empty(self):
        patterns = pattern_processor.process_all_patterns(set())
        assert patterns is not None
        self.assertListEqual(patterns, [])

    def test_process_all_blank(self):
        patterns = pattern_processor.process_all_patterns(
            {'_____', '_____', '_____'})
        assert patterns is not None
        self.assertListEqual(patterns, [])

    def test_process_none(self):
        self.assertIsNone(pattern_processor.process_all_patterns(None))


class TestReducePatterns(unittest.TestCase):
    def setUp(self):
        self.input_patterns = [{'a': 1, 'b': 2},
                               {'c': 2, 'b': 1}, {'a': 4, 'z': 1}]

    def test_reduce_standard(self):
        reduced = pattern_processor.reduce_patterns(self.input_patterns)
        assert reduced is not None
        self.assertDictEqual(reduced, {'a': 4, 'b': 2, 'c': 2, 'z': 1})

    def test_reduce_none(self):
        self.assertIsNone(pattern_processor.reduce_patterns(None))

    def test_reduce_empty(self):
        reduced = pattern_processor.reduce_patterns([{}, {}, {}])
        assert reduced is not None
        self.assertDictEqual(reduced,
                             {})

        reduced = pattern_processor.reduce_patterns([])
        assert reduced is not None
        self.assertDictEqual(reduced, {})


class TestGetCandidateWords(unittest.TestCase):

    def test_get_valid_word(self):
        self.assertSetEqual(pattern_processor.get_candidate_words(
            '_a_t_', {'__n_s'}, 'erip', './data/words_alpha.txt', 5), {'nasty'})


if __name__ == '__main__':
    unittest.main()
