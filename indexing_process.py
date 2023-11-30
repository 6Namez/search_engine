import json

from documents import Document, TransformedDocument, DictDocumentStore, DocumentStore
from index import  BaseIndex
from tf_idf_inverted_index import TfIdfInvertedIndex
from tokenizer import tokenize


def text_acquisition() -> DocumentStore:
    doc_store = DictDocumentStore()
    doc_store.add_document(
        Document(doc_id='0', text='red is a color'))
    doc_store.add_document(
        Document(doc_id='1', text='red and blue'))
    return doc_store


def transform_documents(documents: list[Document]):
    return [TransformedDocument(doc_id=doc.doc_id, terms=tokenize(doc.text)) for doc in documents]


def create_index(transformed_documents: list[TransformedDocument]) -> BaseIndex:
    """
    Takes a list of TransformedDocument and creates an index out of them.
    :param transformed_documents: list of TransformedDocuments.
    :return: BaseIndex
    """
    index = TfIdfInvertedIndex()
    for doc in transformed_documents:
        index.add_document(doc)
    return index


def docs_from_json(file_path: str) -> DocumentStore:
    doc_store = DictDocumentStore()
    with open(file_path, 'r') as fp:
        for line in fp:
            record = json.loads(line)
            doc = Document(doc_id=record['doc_id'], text=record['text'])  # Same can be done by doc = Document(**record)
            doc_store.add_document(doc)
    return doc_store


def indexing_process(file_path: str) -> tuple[DocumentStore, BaseIndex]:
    documents = docs_from_json(file_path)
    transformed_documents = transform_documents(documents.list_all())
    index = create_index(transformed_documents)
    return documents, index
