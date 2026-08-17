import os
import django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)
django.setup()

from analyst.models import DatabaseConnection
from rag.bm25_retriever import BM25Retriever

database = DatabaseConnection.objects.get(
    name="Demo Analytics"
)
retriever = BM25Retriever()

retriever.build_index(database)

queries = [
    "Which customers bought the most products?",
    "How much do products cost?",
    "What tables contain customer information?",
    "orders customer_id",
    "product price"
]
for query in queries:
    print("="*60)
    print("QUERY:", query)

    documents = retriever.search(
        query,
        top_k=3
    )
    for document in documents:
        print(document.source_table)