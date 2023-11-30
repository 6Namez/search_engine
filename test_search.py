from unittest import TestCase
import search


class Test(TestCase):
    def test_string_match__matches(self):
        self.assertTrue(search.string_match(document='red and blue', query='red'))

    def test_string_match__dont_match(self):
        self.assertFalse(search.string_match(document='yellow and blue', query='red'))

    def test_string_match__strange_match(self):
        self.assertTrue(search.string_match(document='predict color', query='red'))

    def test_string_match__empty_query(self):
        self.assertTrue(search.string_match(document='predict color', query=''))

    def test_string_match__empty_document(self):
        self.assertFalse(search.string_match(document='', query='query'))

    def test_boolean_term_match__checks_all_terms(self):
        self.assertFalse(search.boolean_term_match(document='red and blue', query='red and yellow'))

    def test_boolean_term_match__checks_a_few_terms(self):
        self.assertFalse(search.boolean_term_match(document='green and blue and black', query='red and yellow'))

    def test_boolean_term_match__empty_query(self):
        self.assertTrue(search.boolean_term_match(document='green and blue and black', query=''))

    def test_boolean_term_match__empty_document(self):
        self.assertFalse(search.boolean_term_match(document='', query='document'))

    def test_search(self):
        self.assertEqual(['red and green'], search.search(query='red', documents=['blue and yellow', 'red and green']))

    def test_search__empty_query(self):
        self.assertEqual(['blue and yellow', 'red and green'],
                         search.search(query='', documents=['blue and yellow', 'red and green']))

    def test_search__empty_documents(self):
        self.assertEqual([],
                         search.search(query='query', documents=[]))
