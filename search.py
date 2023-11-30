
def string_match(document: str, query: str) -> bool:
    """
    Implements document matching by checking if the query is a substring of the document.
    :param query: The text a user searched for.
    :param document: A candidate document.
    :return: True if the document matches the query and False otherwise.
    """
    return query in document


def boolean_term_match(document: str, query: str) -> bool:
    """
    Boolean matching function.
    :param query: The text a user searched for.
    :param document: A candidate document.
    :return: True if all terms in the query are also in the document and False otherwise.
    """
    query_terms = set(query.lower().split())
    document_terms = set(document.lower().split())
    return query_terms.issubset(document_terms)
    # return query_terms <= document_terms
    # return (query_terms & document_terms) == query_terms


def search(documents: list[str], query: str) -> list[str]:
    """
    Naive search implementation.
    :param query: The text to search for.
    :param documents: A list of strings representing documents that we are searching over.
    :return: Documents matching the query.
    """
    # The code in this function is equivalent to the following list comprehension:
    # return [doc for doc in documents if boolean_term_match(query, doc)]
    out = []
    for doc in documents:
        if boolean_term_match(doc, query):
            out.append(doc)
    return out
