from unittest import TestCase
from priority_search import PhraseSearch
from documents import TransformedDocument


class TestPhraseSearch(TestCase):

    def setUp(self):
        # Create an instance of PhraseSearch
        self.phrase_search = PhraseSearch()

        doc1 = TransformedDocument("doc1", ["document", "test", "for"])
        doc2 = TransformedDocument("doc2", ["test", "document", "for", "document", "got"])
        doc3 = TransformedDocument("doc3", ["this", "document", "is", "also", "got"])
        doc4 = TransformedDocument("doc4", ["this", "is", "text"])
        self.phrase_search.add_document(doc1)
        self.phrase_search.add_document(doc2)
        self.phrase_search.add_document(doc3)
        self.phrase_search.add_document(doc4)

    def test_handle_quoted_query(self):
        # Test case 1: Regular quoted query
        quoted_tokens_1 = ["document", "test"]
        result_1 = self.phrase_search.handle_quoted_query(quoted_tokens_1)
        self.assertEqual(["doc1"], result_1)

    def test_handle_unquoted_query(self):
        # Test case 1: Regular unquoted query
        unquoted_tokens_1 = ["document", "test"]
        number_of_results_1 = 2
        result_1 = self.phrase_search.handle_unquoted_query(unquoted_tokens_1, number_of_results_1)
        self.assertEqual(["doc1", "doc2"], result_1)

    def test_handle_mixed_query(self):
        # Test case 1: Regular mixed query
        unquoted_tokens_1 = ["document", "test"]
        quoted_tokens_1 = ["got"]
        number_of_results_1 = 2
        result_1 = self.phrase_search.handle_mixed_query(unquoted_tokens_1, quoted_tokens_1, number_of_results_1)
        self.assertEqual(["doc2"], result_1)

    def test_parent_search(self):
        # Test case 1: Regular parent search
        processed_query_1 = ["document", "test"]
        number_of_results_1 = 2
        result_1 = self.phrase_search.parent_search(processed_query_1, number_of_results_1)
        self.assertEqual(["doc1", "doc2"], result_1)

        # Test case 2: Parent search with no matching documents
        processed_query_2 = ["nonexistent", "term"]
        number_of_results_2 = 2
        result_2 = self.phrase_search.parent_search(processed_query_2, number_of_results_2)
        self.assertEqual([], result_2)

    def test_quotes_search(self): # this is wrong now, i changed docs
        # Test case 1: Regular quotes search
        quoted_tokens_1 = ["document", "test"]
        result_1 = self.phrase_search.quotes_search(quoted_tokens_1)
        self.assertEqual(["doc1"], result_1)

        # Test case 2: Regular quotes search
        quoted_tokens_2 = ["test", "document"]
        result_2 = self.phrase_search.quotes_search(quoted_tokens_2)
        self.assertEqual(["doc2"], result_2)

        # Test case 3: Quotes search with no matching documents
        quoted_tokens_3 = ["nonexistent", "term"]
        result_3 = self.phrase_search.quotes_search(quoted_tokens_3)
        self.assertEqual([], result_3)

        # Test case 4: Quotes search with no matching documents
        quoted_tokens_4 = ["document"]
        result_4 = self.phrase_search.quotes_search(quoted_tokens_4)
        self.assertEqual(["doc1", "doc2", "doc3"], result_4)

        # Test case 5: Quotes search with no matching documents
        quoted_tokens_5 = ["document", "for"]
        result_5 = self.phrase_search.quotes_search(quoted_tokens_5)
        self.assertEqual(["doc2"], result_5)

        # Test case 6: Quotes search with repeated terms in the document
        quoted_tokens_6 = ["document", "document"]
        result_6 = self.phrase_search.quotes_search(quoted_tokens_6)
        self.assertEqual([], result_6)

    def test_limited_document_search(self):
        # Test case 1: Regular limited document search
        refined_document_ids_1 = ["doc1", "doc2"]
        processed_query_1 = ["document"]
        number_of_results_1 = 2
        result_1 = self.phrase_search.limited_document_search(refined_document_ids_1, processed_query_1, number_of_results_1)
        self.assertEqual(["doc2", "doc1"], result_1)

        # Test case 2: Regular limited document search
        refined_document_ids_2 = ["doc2", "doc3"]
        processed_query_2 = ["got", "document"]
        number_of_results_2 = 2
        result_2 = self.phrase_search.limited_document_search(refined_document_ids_2, processed_query_2, number_of_results_2)
        self.assertEqual(["doc2", "doc3"], result_2)

