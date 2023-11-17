from unittest import TestCase
from tokenizer import quotation_parser


class Test(TestCase):
    def test_quotation_parser(self):
        # Test case 1: Regular input with both quoted and unquoted parts
        input_query_1 = 'This is a "test query" with some unquoted parts.'
        expected_output_1 = (['this', 'is', 'a', 'with', 'some', 'unquoted', 'parts', '.'], ['test', 'query'])
        self.assertEqual(quotation_parser(input_query_1), expected_output_1)

        # Test case 2: Input with only unquoted parts
        input_query_2 = 'No quotes here, just unquoted words.'
        expected_output_2 = (['no', 'quotes', 'here', ',', 'just', 'unquoted', 'words', '.'], [])
        self.assertEqual(quotation_parser(input_query_2), expected_output_2)

        # Test case 3: Input with only quoted parts
        input_query_3 = '"Only quoted words here."'
        expected_output_3 = ([], ['only', 'quoted', 'words', 'here', '.'])
        self.assertEqual(quotation_parser(input_query_3), expected_output_3)

        # Test case 4: Input with no quotes or unquoted parts
        input_query_4 = ''
        expected_output_4 = ([], [])
        self.assertEqual(quotation_parser(input_query_4), expected_output_4)

        # Test case 5: Input with multiple quoted and unquoted parts
        input_query_5 = 'This is "test1" and "test2" with some unquoted "parts".'
        expected_output_5 = (['this', 'is', 'and', 'with', 'some', 'unquoted', '.'], ['test1', 'test2', 'parts'])
        self.assertEqual(quotation_parser(input_query_5), expected_output_5)
