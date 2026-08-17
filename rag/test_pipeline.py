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


database = DatabaseConnection.objects.get(
        name="Demo Analytics"
    )
CONNECTION_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "dbname": "demo_analytics",
    "user": "rag_user",
    "password": "rag_password",
}
introspector = SchemaIntrospector(
    CONNECTION_PARAMS
)

schema = introspector.inspect()

pipeline = RAGSQLPipeline()

question = "What was our revenue in June?"

result = pipeline.run(
    question,
    database,
    schema,
    CONNECTION_PARAMS
)

print("=" * 60)
print("QUESTION:")
print(question)

print("=" * 60)

if result["success"]:

    print("SQL:")
    print(result["sql"])

    print("=" * 60)
    print("EXPLANATION:")
    print(result["explanation"])

    print("=" * 60)
    print("COLUMNS:")
    print(result["columns"])

    print("=" * 60)
    print("ROWS:")

    for row in result["rows"]:
        print(row)

else:

    print("PIPELINE FAILED")
    print("STAGE:", result["stage"])
    print("ERROR:", result["error"])

    if "sql" in result:
        print("GENERATED SQL:")
        print(result["sql"])