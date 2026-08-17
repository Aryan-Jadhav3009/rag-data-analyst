import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import transaction

from analyst.models import DatabaseConnection, RAGDocument
from analyst.schema_introspector import SchemaIntrospector
from rag.document_builder import SchemaDocumentBuilder
from rag.embeddings import EmbeddingService


CONNECTION_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "dbname": "demo_analytics",
    "user": "rag_user",
    "password": "rag_password",
}


def ingest_schema(database):
    introspector = SchemaIntrospector(CONNECTION_PARAMS)
    schema = introspector.inspect()

    builder = SchemaDocumentBuilder()
    documents = builder.build(schema)

    embedding_service = EmbeddingService()

    texts = [
        document["content"]
        for document in documents
    ]

    embeddings = embedding_service.embed_many(texts)

    with transaction.atomic():
        RAGDocument.objects.filter(
            database=database
        ).delete()

        rag_documents = []

        for document, embedding in zip(documents, embeddings):
            rag_documents.append(
                RAGDocument(
                    database=database,
                    content=document["content"],
                    document_type=document["metadata"]["type"],
                    source_table=document["metadata"]["table"],
                    embedding=embedding,
                )
            )

        RAGDocument.objects.bulk_create(rag_documents)

    return len(rag_documents)


if __name__ == "__main__":
    import os
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    database = DatabaseConnection.objects.get(
        name="Demo Analytics"
    )

    count = ingest_schema(database)

    print(f"Ingested {count} documents.")