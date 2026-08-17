import json
from rag.schema_ingestion_service import (
    SchemaIngestionService
)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from analyst.models import DatabaseConnection
from analyst.database_service import DatabaseService


@csrf_exempt

def list_databases(request):

    if request.method != "GET":
        return JsonResponse(
            {
                "error": "Only GET requests are allowed."
            },
            status=405
        )

    databases = DatabaseConnection.objects.all().order_by(
        "name"
    )

    data = [
        {
            "id": database.id,
            "name": database.name,
        }
        for database in databases
    ]

    return JsonResponse(
        data,
        safe=False
    )
def create_database(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "error": "Only POST requests are allowed."
            },
            status=405
        )

    try:
        body = json.loads(request.body)

        required_fields = [
            "name",
            "host",
            "port",
            "database_name",
            "username",
            "password",
        ]

        for field in required_fields:

            if not body.get(field):
                return JsonResponse(
                    {
                        "error": f"{field} is required."
                    },
                    status=400
                )

        database = DatabaseConnection(
            name=body["name"],
            host=body["host"],
            port=body["port"],
            database_name=body["database_name"],
            username=body["username"],
            password=body["password"],
        )

        database.save()

        service = DatabaseService()

        if not service.test_connection(database):

            database.delete()

            return JsonResponse(
                {
                    "error": "Could not connect to the database."
                },
                status=400
            )
        connection_params = (
            database.get_connection_params()
        )

        ingestion_service = SchemaIngestionService()

        document_count = ingestion_service.ingest(
            database,
            connection_params
        )

        return JsonResponse(
            {
                "success": True,
                "database_id": database.id,
                "name": database.name,
                "documents_ingested": document_count,
                "message": "Database connected and schema ingested successfully."
            },
            status=201
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "error": "Invalid JSON."
            },
            status=400
        )

    except Exception as e:

        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )