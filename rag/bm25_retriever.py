import re

from rank_bm25 import BM25Okapi

from analyst.models import RAGDocument


def tokenize(text):
    return re.findall(
        r"\b\w+\b",
        text.lower()
    )


class BM25Retriever:

    def __init__(self):
        self.documents = []
        self.bm25 = None

    def build_index(self, database):
        self.documents = list(
            RAGDocument.objects.filter(
                database=database
            )
        )

        tokenized_documents = [
            tokenize(document.content)
            for document in self.documents
        ]

        self.bm25 = BM25Okapi(tokenized_documents)

    def search(self, query, top_k=5):
        if self.bm25 is None:
            raise RuntimeError(
                "BM25 index has not been built."
            )

        query_tokens = tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        ranked_documents = sorted(
            zip(self.documents, scores),
            key=lambda item: item[1],
            reverse=True
        )

        return [
            document
            for document, score in ranked_documents[:top_k]
        ]