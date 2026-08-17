import sqlglot
from sqlglot import exp


class SQLValidationError(Exception):
    pass


class SQLValidator:

    def validate(self, sql, schema):

        sql = sql.strip()

        if not sql:
            raise SQLValidationError(
                "Generated SQL is empty."
            )

        # --------------------------------
        # Parse SQL
        # --------------------------------

        try:
            statements = sqlglot.parse(
                sql,
                dialect="postgres"
            )
        except Exception as e:
            raise SQLValidationError(
                f"Invalid SQL syntax: {e}"
            )

        # --------------------------------
        # Only one statement
        # --------------------------------

        if len(statements) != 1:
            raise SQLValidationError(
                "Only one SQL statement is allowed."
            )

        statement = statements[0]

        # --------------------------------
        # Read-only check
        # --------------------------------

        if not isinstance(statement, exp.Select):
            raise SQLValidationError(
                "Only SELECT queries are allowed."
            )

        # --------------------------------
        # Build schema lookup
        # --------------------------------

        schema_lookup = {
            table["table"]: {
                column["name"]
                for column in table["columns"]
            }
            for table in schema["tables"]
        }

        # --------------------------------
        # Validate tables
        # --------------------------------

        referenced_tables = {
            table.name
            for table in statement.find_all(exp.Table)
        }

        unknown_tables = (
            referenced_tables - schema_lookup.keys()
        )

        if unknown_tables:
            raise SQLValidationError(
                "Query references unknown tables: "
                + ", ".join(sorted(unknown_tables))
            )

        # --------------------------------
        # Build alias → table mapping
        # --------------------------------

        aliases = {}

        for table in statement.find_all(exp.Table):
            table_name = table.name

            if table.alias:
                aliases[table.alias] = table_name

            aliases[table_name] = table_name

        # --------------------------------
        # Validate qualified columns
        # --------------------------------

        for column in statement.find_all(exp.Column):

            column_name = column.name
            table_name = column.table

            if not table_name:
                continue

            actual_table = aliases.get(table_name)

            if not actual_table:
                raise SQLValidationError(
                    f"Unknown table or alias: {table_name}"
                )

            if column_name not in schema_lookup[actual_table]:
                raise SQLValidationError(
                    f"Unknown column: "
                    f"{actual_table}.{column_name}"
                )

        return True