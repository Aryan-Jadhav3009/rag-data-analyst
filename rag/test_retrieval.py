import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from analyst.models import DatabaseConnection
from rag.retriever import VectorRetriever


database = DatabaseConnection.objects.get(
    name="Demo Analytics"
)

retriever = VectorRetriever()

queries = [
    "Which customers bought the most products?",
    "How much do products cost?",
    "What tables contain customer information?"
]

for query in queries:
    print("=" * 60)
    print("QUERY:", query)

    documents = retriever.search(
        query,
        database,
        top_k=3
    )

    for document in documents:
        print(
            document.source_table
        )