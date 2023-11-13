from typing import List

import tokenizer
from tf_idf_inverted_index import TfIdfInvertedIndex
from tokenizer import tokenize
from documents import TransformedDocument, DictDocumentStore
import json
import sys

doc_store_instance = DictDocumentStore()

PATH_TO_JSON = "/Users/calebwillingham/Desktop/csc299/GitHub/search_engine/json/temp.json"


def handle_empty_querie() -> None:
    print("No query received. Exiting")
    sys.exit(0)


def handle_no_results_for_quoted_query() -> None:
    print("No documents for quoted query. Try searching without quotes. Exiting")
    sys.exit(0)


class PhraseSearch(TfIdfInvertedIndex):
    def __init__(self):
        super().__init__()
        self.doc_store = doc_store_instance


    def initialize_docs(self) -> None:
        with open(PATH_TO_JSON, 'r') as file:
            for line in file:
                document_dict = json.loads(line)

                doc_id = document_dict["doc_id"]
                text = document_dict["text"]

                # Parse the query to separate quoted and unquoted parts
                terms = tokenize(text)

                # Create TransformedDocument instance
                transformed_doc = TransformedDocument(doc_id=doc_id, terms=terms)

                # Create TransformedDocument instances for unquoted and quoted parts
                self.doc_store = DictDocumentStore.read(PATH_TO_JSON)
                self.add_document(transformed_doc)

    def handle_quoted_query(self, quoted_tokens: List[str]) -> List[str]:
        self.initialize_docs()
        refined_document_ids = self.quotes_search(quoted_tokens)
        if len(refined_document_ids) != 0:
            return refined_document_ids
        else:
            handle_no_results_for_quoted_query()

    def handle_unquoted_query(self, unquoted_tokens: List[str], number_of_results: int) -> List[str]:
        self.initialize_docs()
        return self.parent_search(unquoted_tokens, number_of_results)

    def handle_mixed_query(self, unquoted_tokens: List[str], quoted_tokens: List[str], number_of_results: int) -> List[str]:
        self.initialize_docs()
        refined_document_ids = self.quotes_search(quoted_tokens)
        if len(refined_document_ids) != 0:
            return self.limited_document_search(refined_document_ids, unquoted_tokens, number_of_results)
        else:
            handle_no_results_for_quoted_query()

    def parent_search(self, processed_query: List[str], number_of_results: int) -> List[str]:
        self.initialize_docs()
        return super().search(processed_query, number_of_results)

    def quotes_search(self, quoted_tokens: List[str]) -> List[str]:
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

    def limited_document_search(self, refined_document_ids: List[str], processed_query: List[str], number_of_results: int) -> List[str]:
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
