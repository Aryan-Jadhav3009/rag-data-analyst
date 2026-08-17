from analyst.models import RAGDocument
from pgvector.django import CosineDistance
from rag.embeddings import EmbeddingService


class VectorRetriever:

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def search(self, query, database, top_k=5):
        query_embedding = self.embedding_service.embed(query)

        return (
            RAGDocument.objects
            .filter(database=database)
            .exclude(embedding=None)
            .annotate(
                distance=CosineDistance(
                    "embedding",
                    query_embedding
                )
            )
            .order_by("distance")[:top_k]
        )