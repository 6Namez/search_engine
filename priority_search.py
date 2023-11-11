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
        refined_document_ids = []

        matching_doc_ids = None

        for term in quoted_tokens:
            term_doc_ids = set(self.term_to_doc_id_tf_scores.get(term, {}))

            if matching_doc_ids is None:
                matching_doc_ids = term_doc_ids
            else:
                matching_doc_ids = matching_doc_ids.intersection(term_doc_ids)

        if matching_doc_ids is None:
            return []

        index = 0
        for token in matching_doc_ids:
            if index < len(quoted_tokens) and token.lower() == quoted_tokens[index].lower():
                refined_document_ids.append(token)
                index += 1

        if index == len(quoted_tokens):
            return refined_document_ids

        return []

    """
        limited_document_search is taking the refined_document_ids (A a list of doc_ids) and running a search with 
        processed_query on the limited doc_id space, so we have better time allocation and are only looking through
        the documents pertaining to the search. and were returning only the number_of_results desired.
    """

    def limited_document_search(self, refined_document_ids, processed_query, number_of_results):
        matching_doc_ids = None

        for term in processed_query:
            term_doc_ids = set(refined_document_ids.get(term, {}).keys())

            if matching_doc_ids is None:
                matching_doc_ids = term_doc_ids
            else:
                matching_doc_ids = matching_doc_ids.intersection(term_doc_ids)

        if matching_doc_ids is None:
            return []

        scores = dict()
        for doc_id in matching_doc_ids:
            score = self.combine_term_scores(processed_query, doc_id)
            scores[doc_id] = score
        sorted_docs = sorted(matching_doc_ids, key=scores.get, reverse=True)

        return sorted_docs[:number_of_results]
