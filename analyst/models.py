from django.db import models
from pgvector.django import VectorField
# Create your models here.
class DatabaseConnection(models.Model):
    name = models.CharField(max_length=100)

    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField(default=5432)
    database_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    def get_connection_params(self):
        return {
            "host": self.host,
            "port": self.port,
            "dbname": self.database_name,
            "user": self.username,
            "password": self.password,
        }
    def __str__(self):
        return self.name

class RAGDocument(models.Model):
    database = models.ForeignKey(
        DatabaseConnection,
        on_delete=models.CASCADE,
        related_name="rag_documents"
    )
    content = models.TextField()

    document_type = models.CharField(max_length=50)
    source_table = models.CharField(max_length=255)

    embedding = VectorField(dimensions=384, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["database", "document_type", "source_table"],
                name="unique_rag_document_source"
            )
        ]

    def __str__(self):
        return f"{self.document_type}: {self.source_table}"