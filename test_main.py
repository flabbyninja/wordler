import unittest
import argparse


import main as main


class TestParseArguments(unittest.TestCase):

    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-l',
                                 '--locked_pattern', help='string of known letters in the right position')
        self.parser.add_argument(
            '-f', '--floating_patterns', action='append', help='list of patterns of valid letters in the wrong position')
        self.parser.add_argument('-x', '--excluded_letters',
                                 help='string of letters not in the word')

    def test_valid_args(self):
        command_args = ["-l _a_t_", "-f __n_s", "-x erip"]
        args = self.parser.parse_args(command_args)
        locked_pattern, floating_patterns, excluded_letters = main.parse_arguments(args.locked_pattern,
                                                                                   args.floating_patterns, args.excluded_letters)
        self.assertEqual(locked_pattern, '_a_t_')
        self.assertListEqual(floating_patterns, ['__n_s'])
        self.assertEqual('erip', excluded_letters)

    def test_missing_locked(self):
        command_args = ["-f __n_s", "-x erip"]
        args = self.parser.parse_args(command_args)
        locked_pattern, floating_patterns, excluded_letters = main.parse_arguments(args.locked_pattern,
                                                                                   args.floating_patterns, args.excluded_letters)
        self.assertEqual(locked_pattern, None)
        self.assertListEqual(floating_patterns, ['__n_s'])
        self.assertEqual('erip', excluded_letters)

    def test_missing_floating(self):
        command_args = ["-l _a_t_", "-x erip"]
        args = self.parser.parse_args(command_args)
        locked_pattern, floating_patterns, excluded_letters = main.parse_arguments(args.locked_pattern,
                                                                                   args.floating_patterns, args.excluded_letters)
        self.assertEqual(locked_pattern, '_a_t_')
        self.assertIsNone(floating_patterns, None)
        self.assertEqual('erip', excluded_letters)

    def test_missing_excluded(self):
        command_args = ["-l _a_t_", "-f __n_s"]
        args = self.parser.parse_args(command_args)
        locked_pattern, floating_patterns, excluded_letters = main.parse_arguments(args.locked_pattern,
                                                                                   args.floating_patterns, args.excluded_letters)
        self.assertEqual(locked_pattern, '_a_t_')
        self.assertListEqual(floating_patterns, ['__n_s'])
        self.assertIsNone(excluded_letters)


if __name__ == '__main__':
    unittest.main()
