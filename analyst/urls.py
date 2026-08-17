from django.urls import path

from .views import query_database
from .database_views import (
    create_database,
    list_databases
)


urlpatterns = [
    path(
        "query/",
        query_database,
        name="query_database"
    ),

    path(
        "databases/",
        create_database,
        name="create_database"
    ),

    path(
        "databases/list/",
        list_databases,
        name="list_databases"
    ),
]