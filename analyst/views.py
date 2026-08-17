import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from analyst.models import DatabaseConnection
from analyst.schema_introspector import SchemaIntrospector
from rag.pipeline import RAGSQLPipeline





pipeline = RAGSQLPipeline()


@csrf_exempt
def query_database(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "error": "Only POST requests are allowed."
            },
            status=405
        )

    try:
        body = json.loads(request.body)

        question = body.get("question")
        database_id = body.get("database_id")

        if not question:
            return JsonResponse(
                {"error": "Question is required."},
                status=400
            )

        if not database_id:
            return JsonResponse(
                {"error": "database_id is required."},
                status=400
            )

        try:
            database = DatabaseConnection.objects.get(
                id=database_id
            )
        except DatabaseConnection.DoesNotExist:
            return JsonResponse(
                {"error": "Database not found."},
                status=404
            )
        database = DatabaseConnection.objects.get(
            id=database_id
        )
        CONNECTION_PARAMS = (
            database.get_connection_params()
        )

        introspector = SchemaIntrospector(
            CONNECTION_PARAMS
        )

        schema = introspector.inspect()

        result = pipeline.run(
            question,
            database,
            schema,
            CONNECTION_PARAMS
        )

        if not result["success"]:
            return JsonResponse(
                {
                    "success": False,
                    "stage": result["stage"],
                    "error": result["error"],
                    "sql": result.get("sql"),
                },
                status=400
            )

        return JsonResponse(
            {
                "success": True,
                "question": result["question"],
                "sql": result["sql"],
                "explanation": result["explanation"],
                "columns": result["columns"],
                "rows": [
                    list(row)
                    for row in result["rows"]
                ],
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON."},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )