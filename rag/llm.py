from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI


class SQLGenerationResult(BaseModel):
    sql: str = Field(
        description="A read-only PostgreSQL SELECT query"
    )

    explanation: str = Field(
        description="Brief explanation of what the SQL does"
    )


class SQLGenerator:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            temperature=0
        )

        self.structured_llm = self.llm.with_structured_output(
            SQLGenerationResult
        )

    def generate(self, question, schema_context):

        prompt = f"""
You are a SQL generation assistant.

Generate a read-only PostgreSQL query
that answers the user's question.

Use ONLY the database schema provided below.

DATABASE SCHEMA:
{schema_context}

USER QUESTION:
{question}

Rules:
- Generate valid PostgreSQL.
- Use only tables and columns present in the schema.
- Do not invent tables or columns.
- Only generate SELECT queries.
- Do not INSERT, UPDATE, DELETE, DROP, ALTER, or modify data.
- The SQL should directly answer the user's question.
- Briefly explain the query.

Return the result using the required structured format.
"""

        return self.structured_llm.invoke(prompt)