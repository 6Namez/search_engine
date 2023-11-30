from unittest import TestCase
from tokenize import tokenize


class Test(TestCase):
    def test_tokenize__splits_on_space(self):
        self.assertEqual(['some', 'word'], tokenize('some word'))

    def test_tokenize__lowercases(self):
        self.assertEqual(['some', 'word'], tokenize('Some wOrD'))

    def test_tokenize__separate_period(self):
        self.assertEqual(['some', 'sentence', '.'], tokenize('some sentence.'))

    # TODO: Implement in the next version
    # def test_tokenize__period_in_abbreviations(self):
    #     self.assertEqual(['dr.', 'brown'], tokenize('Dr. Brown'))

    def test_tokenize__split_comma(self):
        self.assertEqual(['some', ',', 'word'], tokenize('some, word'))
