import query_process
from tf_idf_inverted_index import TfIdfInvertedIndex
import query_process

import sys


class PhraseSearch(TfIdfInvertedIndex):

    def handle_empty_querie(self):
        pass

    def handle_no_results_for_quoted_query(self):
        pass

    def handle_quoted_query(self, quoted_tokens, number_of_results):
        refined_document_ids = self.quotes_search(quoted_tokens)
        if len(refined_document_ids) != 0:
            return self.limited_document_search(refined_document_ids, quoted_tokens, number_of_results)
        else:
            query_process.not_implemented_yet()
            # self.handle_no_results_for_quoted_query()

    def handle_unquoted_query(self, unquoted_tokens, number_of_results):
        refined_document_ids = self.quotes_search(unquoted_tokens)
        if len(refined_document_ids) == 0:
            return self.parent_search(unquoted_tokens, number_of_results)

    def handle_mixed_query(self, unquoted_tokens, quoted_tokens, number_of_results):
        refined_document_ids = self.quotes_search(quoted_tokens)
        if len(refined_document_ids) != 0:
            return self.limited_document_search(refined_document_ids, unquoted_tokens, number_of_results)
        else:
            query_process.not_implemented_yet()
            # self.handle_no_results_for_quoted_query()

    def parent_search(self, processed_query, number_of_results):
        pass

    def quotes_search(self, quoted_tokens):
        pass

    def limited_document_search(self, refined_document_ids, processed_query, number_of_results):
        pass
