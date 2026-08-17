import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from analyst.models import DatabaseConnection
from rag.evaluation import EVALUATION_CASES
from rag.hybrid_retriever import HybridRetriever


database = DatabaseConnection.objects.get(
    name="Demo Analytics"
)

retriever = HybridRetriever()

top_k = 2

total_recall = 0

for case in EVALUATION_CASES:
    question = case["question"]
    required_tables = case["required_tables"]

    results = retriever.search(
        question,
        database,
        top_k=top_k
    )

    retrieved_tables = set()

    for result in results:
        document = result["document"]

        if document.document_type == "table":
            retrieved_tables.add(
                document.source_table
            )

        elif document.document_type == "relationship":
            source, target = (
                document.source_table.split("__")
            )

            retrieved_tables.add(source)
            retrieved_tables.add(target)

    found = required_tables.intersection(
        retrieved_tables
    )

    recall = len(found) / len(required_tables)

    total_recall += recall

    print("=" * 60)
    print(question)
    print("Required:", required_tables)
    print("Retrieved:", retrieved_tables)
    print(f"Recall@{top_k}: {recall:.2f}")


average_recall = (
    total_recall / len(EVALUATION_CASES)
)

print("=" * 60)
print(
    f"Average Recall@{top_k}: "
    f"{average_recall:.2f}"
)