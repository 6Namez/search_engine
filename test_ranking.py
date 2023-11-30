from unittest import TestCase
import ranking


class Test(TestCase):
    def test_term_count_relevance__single_term_query(self):
        self.assertEqual(
            2, ranking.term_count_relevance(document='red is a color. red is great.', query='red'))

    def test_term_count_relevance__multiple_term_query(self):
        self.assertEqual(
            3, ranking.term_count_relevance(document='red is a color . red is great .',
                                            query='red color'))

    def test_term_count_relevance__partial_match(self):
        self.assertEqual(
            2, ranking.term_count_relevance(
                document='red is a color . red is great .',
                query='red and blue'))

    def test_term_count_relevance__empty_document(self):
        self.assertEqual(
            0, ranking.term_count_relevance(
                document='',
                query='query'))

    def test_term_count_relevance__empty_query(self):
        self.assertEqual(
            0, ranking.term_count_relevance(
                document='red is a color . red is great .',
                query=''))

    def test_boolean_term_count_relevance__single_term_query(self):
        self.assertEqual(
            1, ranking.boolean_term_count_relevance(document='red is a color. red is great.', query='red'))

    def test_boolean_term_count_relevance__multiple_term_query(self):
        self.assertEqual(
            2, ranking.boolean_term_count_relevance(
                document='red is a color . red is great .',
                query='red color'))

    def test_boolean_term_count_relevance__partial_match(self):
        self.assertEqual(
            1, ranking.boolean_term_count_relevance(
                document='red is a color . red is great .',
                query='red and blue'))

    def test_boolean_term_count_relevance__empty_query(self):
        self.assertEqual(
            0, ranking.boolean_term_count_relevance(
                document='red is a color . red is great .',
                query=''))

    def test_boolean_term_count_relevance__empty_document(self):
        self.assertEqual(
            0, ranking.boolean_term_count_relevance(
                document='',
                query='query'))

    def test_search(self):
        self.assertEqual(['red and green', 'blue and yellow'],
                         ranking.search(query='red', documents=['blue and yellow', 'red and green']))

    def test_search__empty_query(self):
        self.assertEqual(['blue and yellow', 'red and green'],
                         ranking.search(query='', documents=['blue and yellow', 'red and green']))

    def test_search__empty_documents(self):
        self.assertEqual([],
                         ranking.search(query='query', documents=[]))
