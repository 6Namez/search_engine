from unittest import TestCase

from counting import count_tokens


class Test(TestCase):
    def test_count_tokens(self):
        self.assertEqual({'to': 2, 'be': 2, 'or': 1, 'not': 1}, count_tokens(['to', 'be', 'or', 'not', 'to', 'be']))
