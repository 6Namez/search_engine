import json
import math
from collections import defaultdict, Counter
from documents import TransformedDocument
from index import BaseIndex


def count_terms(terms: list[str]) -> Counter:
    return Counter(terms)


class TfIdfInvertedIndex(BaseIndex):
    def __init__(self):
        # Mapping of terms to the number of documents they occur in.
        self.doc_counts = Counter()
        # Mapping doc_id to term counts in the corresponding document.
        self.term_to_doc_id_tf_scores = defaultdict(dict)
        self.total_documents_count = 0

    def write(self, path: str):
        with open(path, 'w') as fp:
            fp.write(json.dumps({
                '__metadata__': {
                    'doc_counts': [
                        {
                            'term': term,
                            'count': count
                        }
                        for term, count in self.doc_counts.items()
                    ]
                }
            }) + '\n')
            for doc_id, counts in self.term_to_doc_id_tf_scores.items():
                fp.write(json.dumps({
                    'doc_id': doc_id,
                    'counts': [
                        {
                            'term': term,
                            'count': count
                        }
                        for term, count in counts.items()
                    ]
                }) + '\n')

    def add_document(self, doc: TransformedDocument):
        self.total_documents_count += 1
        term_counts = count_terms(doc.terms)
        self.doc_counts.update(term_counts.keys())

        # Mapping from doc_ids to term counts in the corresponding document.
        for term, count in term_counts.items():
            self.term_to_doc_id_tf_scores[term][doc.doc_id] = count / len(doc.terms)

    def term_frequency(self, term, doc_id):
        return self.term_to_doc_id_tf_scores[term][doc_id]

    def inverse_document_frequency(self, term):
        return math.log(self.total_documents_count / self.doc_counts[term])

    def tf_idf(self, term, doc_id):
        if term in self.doc_counts:
            return self.term_frequency(term, doc_id) * self.inverse_document_frequency(term)
        return 0

    def combine_term_scores(self, terms: list[str], doc_id) -> float:
        return sum([self.tf_idf(term, doc_id) for term in terms])

    def search(self, processed_query: list[str], number_of_results: int) -> list[str]:
        scores = dict()
        matching_doc_ids = None
        for term in processed_query:
            doc_ids = set(self.term_to_doc_id_tf_scores[term].keys())
            if matching_doc_ids is None:
                matching_doc_ids = doc_ids
            else:
                matching_doc_ids = matching_doc_ids & doc_ids

        for doc_id in matching_doc_ids:
            score = self.combine_term_scores(processed_query, doc_id)
            scores[doc_id] = score
        return sorted(list(matching_doc_ids), key=scores.get, reverse=True)[:number_of_results]