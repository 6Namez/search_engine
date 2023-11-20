from typing import List
from tf_idf_inverted_index import TfIdfInvertedIndex, count_terms
import sys


def handle_empty_querie() -> None:
    print("No query received. Exiting")
    sys.exit(0)


def handle_no_results_for_quoted_query() -> None:
    print("No documents for quoted query. Try searching without quotes. Exiting")
    sys.exit(0)


class PhraseSearch(TfIdfInvertedIndex):
    def __init__(self):
        super().__init__()
        self.doc_id_to_term_indexes = {}

    def add_document(self, doc):
        self.total_documents_count += 1
        term_counts = count_terms(doc.terms)
        self.doc_counts.update(term_counts.keys())

        # Mapping from doc_ids to term counts in the corresponding document.
        for term, count in term_counts.items():
            self.term_to_doc_id_tf_scores[term][doc.doc_id] = count / len(doc.terms)

        # Adding term indexes
        term_index_dict = {}
        for index, term in enumerate(doc.terms):
            if term in term_index_dict:
                term_index_dict[term].append(index)
            else:
                term_index_dict[term] = [index]
        self.doc_id_to_term_indexes[doc.doc_id] = term_index_dict

    def handle_quoted_query(self, quoted_tokens: List[str]) -> List[str]:
        refined_document_ids = self.quotes_search(quoted_tokens)
        if len(refined_document_ids) != 0:
            return refined_document_ids
        else:
            handle_no_results_for_quoted_query()

    def handle_unquoted_query(self, unquoted_tokens: List[str], number_of_results: int) -> List[str]:
        return self.parent_search(unquoted_tokens, number_of_results)

    def handle_mixed_query(self, unquoted_tokens: List[str], quoted_tokens: List[str], number_of_results: int) -> List[str]:
        refined_document_ids = self.quotes_search(quoted_tokens)
        if len(refined_document_ids) != 0:
            return self.limited_document_search(refined_document_ids, unquoted_tokens, number_of_results)
        else:
            handle_no_results_for_quoted_query()

    def parent_search(self, processed_query: List[str], number_of_results: int) -> List[str]:
        return super().search(processed_query, number_of_results)

    def quotes_search(self, quoted_tokens: List[str]) -> List[str]:
        refined_document_ids = []
        start_index = 0
        matches = []

        for doc_id, term_index_dict in self.doc_id_to_term_indexes.items():
            for term, indexes in (term_index_dict.items()):
                if start_index < len(quoted_tokens):
                    if term == quoted_tokens[start_index]:
                        start_index += 1
                        matches.append(term)
                    else:
                        start_index = 0
                        matches = []
                    if matches == quoted_tokens:
                        refined_document_ids.append(doc_id)
                else:
                    start_index = 0
                    matches = []

        return refined_document_ids

    def limited_document_search(self, refined_document_ids: List[str], processed_query: List[str], number_of_results: int) -> List[str]:
        scores = dict()
        matching_doc_ids = None
        refined_document_ids = set(refined_document_ids)
        for term in processed_query:
            doc_ids = set(self.term_to_doc_id_tf_scores[term].keys())
            matching_doc_ids = doc_ids & refined_document_ids

        for doc_id in matching_doc_ids:
            score = self.combine_term_scores(processed_query, doc_id)
            scores[doc_id] = score
        return sorted(list(matching_doc_ids), key=scores.get, reverse=True)[:number_of_results]
