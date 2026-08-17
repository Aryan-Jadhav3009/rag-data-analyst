import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from analyst.models import DatabaseConnection
from rag.hybrid_retriever import HybridRetriever


database = DatabaseConnection.objects.get(
    name="Demo Analytics"
)

retriever = HybridRetriever()

queries = [
    "Which customers bought the most products?",
    "How much do products cost?",
    "What tables contain customer information?",
    "What was our revenue in June?",
]

for query in queries:
    print("=" * 60)
    print("QUERY:", query)

    results = retriever.search(
        query,
        database,
        top_k=3
    )

    for result in results:
        document = result["document"]

        print(
            f"{result['final_rank']}. "
            f"{document.source_table} | "
            f"RRF={result['rrf_score']:.6f} | "
            f"vector_rank={result['vector_rank']} | "
            f"bm25_rank={result['bm25_rank']}"
        )