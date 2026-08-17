from rag.retriever import VectorRetriever
from rag.bm25_retriever import BM25Retriever


class HybridRetriever:

    def __init__(self, rrf_k=60):
        self.vector_retriever = VectorRetriever()
        self.bm25_retriever = BM25Retriever()
        self.rrf_k = rrf_k

    def search(self, query, database, top_k=5):
        vector_results = self.vector_retriever.search(
            query,
            database,
            top_k=top_k
        )

        self.bm25_retriever.build_index(database)

        bm25_results = self.bm25_retriever.search(
            query,
            top_k=top_k
        )

        scores = {}
        documents = {}

        vector_ranks = {}
        bm25_ranks = {}

        for rank, document in enumerate(
            vector_results,
            start=1
        ):
            vector_ranks[document.id] = rank
            documents[document.id] = document

            scores[document.id] = (
                scores.get(document.id, 0)
                + 1 / (self.rrf_k + rank)
            )

        for rank, document in enumerate(
            bm25_results,
            start=1
        ):
            bm25_ranks[document.id] = rank
            documents[document.id] = document

            scores[document.id] = (
                scores.get(document.id, 0)
                + 1 / (self.rrf_k + rank)
            )

        ranked_ids = sorted(
            scores,
            key=scores.get,
            reverse=True
        )

        results = []

        for final_rank, document_id in enumerate(
            ranked_ids[:top_k],
            start=1
        ):
            results.append({
                "document": documents[document_id],
                "final_rank": final_rank,
                "rrf_score": scores[document_id],
                "vector_rank": vector_ranks.get(
                    document_id
                ),
                "bm25_rank": bm25_ranks.get(
                    document_id
                )
            })

        return results