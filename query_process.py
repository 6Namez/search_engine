import priority_search
from documents import DocumentStore
from index import BaseIndex
from tokenizer import tokenize, quotation_parser
from typing import List
import json
import sys

phrase_search_instance = priority_search.PhraseSearch()


def user_interface():
    query_str = input("Enter your query: ")
    number_of_results_str = input("Enter number of results desired: ")

    try:
        number_of_results = int(number_of_results_str)
    except ValueError:
        print("Invalid input for the number of results. Please enter a valid integer.")
        # You might want to handle this case further, for example, asking the user to enter the input again.
        sys.exit(1)  # Exiting the program with an error code.

    document_ids = case_handler(query_str, number_of_results)

    print("Document IDs returned by the search:")
    for doc_id in document_ids:
        print(doc_id)


def case_handler(query_str: str, number_of_results: int) -> List[str]:
    print("case_handler.query_str: ", query_str, "case_handler.number_of_results: ", number_of_results)

    unquoted_tokens, quoted_tokens = quotation_parser(query_str)
    print("case_handler.unquoted_tokens: ", unquoted_tokens, "case_handler.quoted_tokens: ", quoted_tokens)

    if len(unquoted_tokens) == 0 and len(quoted_tokens) == 0: #works
        print("case 1")
        priority_search.handle_empty_querie()

    if len(unquoted_tokens) == 0 and len(quoted_tokens) != 0:
        print("case 2")
        number_of_results = 10
        return phrase_search_instance.handle_quoted_query(quoted_tokens)

    if len(unquoted_tokens) != 0 and len(quoted_tokens) == 0:
        print("case 3")
        return phrase_search_instance.handle_unquoted_query(unquoted_tokens, number_of_results)

    if len(unquoted_tokens) != 0 and len(quoted_tokens) != 0:
        print("case 4")
        return phrase_search_instance.handle_mixed_query(unquoted_tokens, quoted_tokens, number_of_results)


class FullDocumentsOutputFormatter:
    def format_out(self, results: list[str], document_store: DocumentStore, unused_processed_query):
        output_string = ''
        for doc_id in results:
            doc = document_store.get_by_doc_id(doc_id)
            output_string += f'({doc.doc_id}) {doc.text}\n\n'
        return output_string


class DocIdsOnlyFormatter:
    def format_out(self, results: list[str], document_store: DocumentStore, unused_processed_query):
        return results


def preprocess_query(query_str: str):
    return tokenize(query_str)


def format_out(results: list[str], document_store: DocumentStore, unused_processed_query) -> str:
    output_string = ''
    for doc_id in results:
        doc = document_store.get_by_doc_id(doc_id)
        output_string += f'({doc.doc_id}) {doc.text}\n\n'
    return output_string


def load_stopwords(stopwords_file):
    if stopwords_file:
        with open(stopwords_file, 'r') as file:
            stopwords = json.load(file)
        return list(stopwords)
    return list()


class QueryProcess:
    def __init__(self, document_store: DocumentStore, index: BaseIndex, stopwords: set[str] = None,
                 output_formatter=FullDocumentsOutputFormatter()):
        self.document_store = document_store
        self.index = index
        self.stopwords = stopwords
        self.output_formatter = output_formatter

    def search(self, query: str, number_of_results: int) -> str:
        if self.stopwords is None:
            processed_query = preprocess_query(query)
        else:
            processed_query = [term for term in preprocess_query(query)
                               if term not in self.stopwords]
        results = self.index.search(processed_query, number_of_results)
        return self.output_formatter.format_out(results, self.document_store, processed_query)


if __name__ == '__main__':
    user_interface()
