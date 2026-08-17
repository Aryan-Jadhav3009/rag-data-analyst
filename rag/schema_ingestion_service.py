from django.db import transaction

from analyst.models import RAGDocument
from analyst.schema_introspector import SchemaIntrospector
from rag.document_builder import SchemaDocumentBuilder
from rag.embeddings import EmbeddingService


class SchemaIngestionService:

    def __init__(self):
        self.builder = SchemaDocumentBuilder()
        self.embedding_service = EmbeddingService()

    def ingest(self, database, connection_params):

        # 1. Inspect the actual database
        introspector = SchemaIntrospector(
            connection_params
        )

        schema = introspector.inspect()

        # 2. Convert schema into RAG documents
        documents = self.builder.build(schema)

        # 3. Generate all embeddings in one batch
        texts = [
            document["content"]
            for document in documents
        ]

        embeddings = (
            self.embedding_service.embed_many(texts)
        )

        # 4. Replace existing documents atomically
        with transaction.atomic():

            RAGDocument.objects.filter(
                database=database
            ).delete()

            rag_documents = []

            for document, embedding in zip(
                documents,
                embeddings
            ):

                rag_documents.append(
                    RAGDocument(
                        database=database,
                        content=document["content"],
                        document_type=document["metadata"]["type"],
                        source_table=document["metadata"]["table"],
                        embedding=embedding,
                    )
                )

            RAGDocument.objects.bulk_create(
                rag_documents
            )

        return len(rag_documents)