import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from analyst.models import DatabaseConnection
from rag.schema_ingestion_service import (
    SchemaIngestionService
)


database = DatabaseConnection.objects.get(
    name="Demo Analytics"
)

connection_params = (
    database.get_connection_params()
)

service = SchemaIngestionService()

count = service.ingest(
    database,
    connection_params
)

print(
    f"Ingested {count} documents."
)