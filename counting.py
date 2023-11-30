from collections import Counter

from documents import TransformedDocument


# def count_tokens(tokens: list[str]) -> dict[str, int]:
#     counts = dict()
#     for t in tokens:
#         if t in counts:
#             counts[t] += 1
#         else:
#             counts[t] = 1
#     return counts


def count_tokens(tokens: list[str]) -> Counter:
    return Counter(tokens)


def count_tokens_in_doc(doc: TransformedDocument) -> Counter:
    return Counter(doc.terms)


def count_tokens_in_doc_collection(docs: list[TransformedDocument]) -> Counter:
    cnt = Counter()
    for doc in docs:
        cnt.update(doc.terms)
    return cnt


def num_documents_by_token(docs: list[TransformedDocument]) -> Counter:
    cnt = Counter()
    for doc in docs:
        cnt.update(set(doc.terms))
    return cnt
