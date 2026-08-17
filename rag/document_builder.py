class SchemaDocumentBuilder:

    def build(self, schema):
        documents = []

        tables = {
            table["table"]: table
            for table in schema["tables"]
        }

        # -------------------------
        # Table documents
        # -------------------------

        for table in schema["tables"]:
            table_name = table["table"]

            content = self.build_table_document(
                table,
                schema["foreign_keys"]
            )

            documents.append({
                "content": content,
                "metadata": {
                    "type": "table",
                    "table": table_name
                }
            })

        # -------------------------
        # Relationship documents
        # -------------------------

        for relationship in schema["foreign_keys"]:
            content = self.build_relationship_document(
                relationship,
                tables
            )

            source = relationship["from_table"]
            target = relationship["to_table"]

            documents.append({
                "content": content,
                "metadata": {
                    "type": "relationship",
                    "table": f"{source}__{target}"
                }
            })

        return documents

    def build_table_document(self, table, foreign_keys):
        table_name = table["table"]

        lines = [
            f"Table: {table_name}",
            "",
            "Columns:"
        ]

        for column in table["columns"]:
            line = (
                f"- {column['name']}: "
                f"{column['type']}"
            )

            if column.get("nullable") is False:
                line += ", not nullable"

            if column["name"] in table.get("primary_keys", []):
                line += ", primary key"

            lines.append(line)

        relationships = [
            fk for fk in foreign_keys
            if (
                fk["from_table"] == table_name
                or fk["to_table"] == table_name
            )
        ]

        if relationships:
            lines.extend([
                "",
                "Relationships:"
            ])

            for relationship in relationships:
                lines.append(
                    f"- {relationship['from_table']}."
                    f"{relationship['from_column']} → "
                    f"{relationship['to_table']}."
                    f"{relationship['to_column']}"
                )

        return "\n".join(lines)

    def build_relationship_document(self, relationship, tables):
        source_table = relationship["from_table"]
        source_column = relationship["from_column"]

        target_table = relationship["to_table"]
        target_column = relationship["to_column"]

        source = tables[source_table]
        target = tables[target_table]

        lines = [
            "Relationship:",
            "",
            f"{source_table}.{source_column} "
            f"references "
            f"{target_table}.{target_column}.",
            "",
            f"Source table: {source_table}",
            f"Source column: {source_column}",
            "",
            f"Target table: {target_table}",
            f"Target column: {target_column}",
            "",
            f"Columns in {source_table}:"
        ]

        for column in source["columns"]:
            lines.append(
                f"- {column['name']}: {column['type']}"
            )

        lines.extend([
            "",
            f"Columns in {target_table}:"
        ])

        for column in target["columns"]:
            lines.append(
                f"- {column['name']}: {column['type']}"
            )

        return "\n".join(lines)