import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from analyst.models import DatabaseConnection
from analyst.schema_introspector import SchemaIntrospector
from rag.pipeline import RAGSQLPipeline


# --------------------------------
# Database configuration
# --------------------------------

CONNECTION_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "dbname": "demo_analytics",
    "user": "rag_user",
    "password": "rag_password",
}


# --------------------------------
# Setup
# --------------------------------

database = DatabaseConnection.objects.get(
    name="Demo Analytics"
)

introspector = SchemaIntrospector(
    CONNECTION_PARAMS
)

schema = introspector.inspect()

pipeline = RAGSQLPipeline()


# --------------------------------
# Test questions
# --------------------------------

questions = [
    "What was our revenue in June?",
    "Which customer placed the most orders?",
    "How much does each product cost?",
    "What products were sold?",
    "How many customers do we have?",
]


# --------------------------------
# Run pipeline
# --------------------------------

for question in questions:

    print("\n")
    print("=" * 70)
    print("QUESTION:")
    print(question)
    print("=" * 70)

    result = pipeline.run(
        question,
        database,
        schema,
        CONNECTION_PARAMS
    )

    if not result["success"]:

        print("FAILED")
        print("Stage:", result["stage"])
        print("Error:", result["error"])

        if result.get("sql"):
            print("Generated SQL:")
            print(result["sql"])

        continue

    print("SQL:")
    print(result["sql"])

    print("\nExplanation:")
    print(result["explanation"])

    print("\nResult:")

    # Display column names
    print(result["columns"])

    # Display rows
    for row in result["rows"]:
        print(row)