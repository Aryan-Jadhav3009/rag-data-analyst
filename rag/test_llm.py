import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from analyst.models import DatabaseConnection
from rag.hybrid_retriever import HybridRetriever
from rag.context_builder import ContextBuilder
from rag.llm import SQLGenerator


database = DatabaseConnection.objects.get(
    name="Demo Analytics"
)

retriever = HybridRetriever()
context_builder = ContextBuilder()
generator = SQLGenerator()

question = "What was our revenue in June?"

# ---------------------------------
# 1. Retrieve relevant schema
# ---------------------------------

results = retriever.search(
    question,
    database,
    top_k=5
)

# ---------------------------------
# 2. Display retrieval results
# ---------------------------------

print("=" * 60)
print("QUESTION:")
print(question)

print("=" * 60)
print("RETRIEVED DOCUMENTS:")

for result in results:
    document = result["document"]

    print(
        f"{result['final_rank']}. "
        f"{document.document_type}: "
        f"{document.source_table}"
    )

# ---------------------------------
# 3. Build LLM context
# ---------------------------------

schema_context = context_builder.build(
    results
)

print("=" * 60)
print("CONTEXT SENT TO LLM:")
print(schema_context)

# ---------------------------------
# 4. Generate SQL
# ---------------------------------

result = generator.generate(
    question,
    schema_context
)

print("=" * 60)
print("GENERATED SQL:")
print(result.sql)

print("=" * 60)
print("EXPLANATION:")
print(result.explanation)