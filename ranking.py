"""
Similar to matching.py, but search returns an ordered (ranked) results. In search.py the results
from search are logically unordered (could be returned in any order). If we want to return 10 "best"
results from search in this file, you can just take the first 10 results. For search in search.py
"best" has to be defined externally to introduce logical order to the returned results.
"""


def term_count_relevance(document: str, query: str) -> int:
    query_terms = query.lower().split()
    document_terms = document.lower().split()
    count = 0
    for term in query_terms:
        for doc_term in document_terms:
            if term == doc_term:
                count += 1
    return count


def boolean_term_count_relevance(document: str, query: str) -> int:
    query_terms = query.lower().split()
    document_terms = document.lower().split()
    count = 0
    for term in query_terms:
        if term in document_terms:
            count += 1
    return count


def search(documents: list[str], query: str) -> list[str]:
    scores = dict()
    for i, doc in enumerate(documents):
        scores[i] = term_count_relevance(document=doc, query=query)
    indexes = sorted(range(len(documents)), key=scores.get, reverse=True)
    return [documents[i] for i in indexes]


def search2(documents: list[str], query: str) -> list[str]:
    scores = dict()
    for doc in documents:
        scores[doc] = term_count_relevance(document=doc, query=query)
    return sorted(documents, key=scores.get, reverse=True)


def search_with_pairs(documents: list[str], query: str) -> list[str]:
    scored_docs = [(term_count_relevance(document=doc, query=query), doc) for doc in documents]
    sorted_docs = sorted(scored_docs, reverse=True)
    return [doc for score, doc in sorted_docs]


def search_with_anonymous_functions(documents: list[str], query: str) -> list[str]:
    return sorted(documents, key=lambda doc: term_count_relevance(document=doc, query=query), reverse=True)


def run_search(documents: list[str]):
    query = input('Please enter your query:')
    while query:
        print(search2(documents=documents, query=query))
        query = input('Please enter your query:')
