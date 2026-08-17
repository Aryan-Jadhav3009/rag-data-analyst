import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from analyst.models import DatabaseConnection
from analyst.database_service import DatabaseService


database = DatabaseConnection.objects.get(
    name="Demo Analytics"
)

service = DatabaseService()

result = service.test_connection(
    database
)

print("Connection successful:", result)