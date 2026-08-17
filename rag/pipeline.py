from rag.hybrid_retriever import HybridRetriever
from rag.context_builder import ContextBuilder
from rag.llm import SQLGenerator
from rag.sql_validator import (
    SQLValidator,
    SQLValidationError
)
from rag.query_executor import QueryExecutor


class RAGSQLPipeline:

    def __init__(self):
        self.retriever = HybridRetriever()
        self.context_builder = ContextBuilder()
        self.generator = SQLGenerator()
        self.validator = SQLValidator()
        self.executor = QueryExecutor()

    def run(
    self,
    question,
    database,
    schema,
    connection_params
):

        # --------------------------------
        # 1. Retrieve schema
        # --------------------------------

        results = self.retriever.search(
            question,
            database,
            top_k=5
        )

        # --------------------------------
        # 2. Build LLM context
        # --------------------------------

        context = self.context_builder.build(
            results
        )

        # --------------------------------
        # 3. Generate SQL
        # --------------------------------

        generation = self.generator.generate(
            question,
            context
        )

        sql = generation.sql

        # --------------------------------
        # 4. Validate SQL
        # --------------------------------

        try:
            self.validator.validate(
                sql,
                schema
            )

        except SQLValidationError as e:

            return {
                "success": False,
                "stage": "validation",
                "error": str(e),
                "sql": sql
            }

        # --------------------------------
        # 5. Execute SQL
        # --------------------------------

        try:
            result = self.executor.execute(
                connection_params,
                sql
            )

        except Exception as e:

            return {
                "success": False,
                "stage": "execution",
                "error": str(e),
                "sql": sql
            }

        # --------------------------------
        # 6. Return result
        # --------------------------------

        return {
            "success": True,
            "question": question,
            "sql": sql,
            "explanation": generation.explanation,
            "columns": result["columns"],
            "rows": result["rows"]
        }