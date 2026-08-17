import psycopg


class SchemaIntrospector:

    def __init__(self, connection_params):
        self.connection_params = connection_params

    def inspect(self):
        with psycopg.connect(**self.connection_params) as conn:
            tables = self.get_tables(conn)

            schema = []

            for table in tables:
                schema.append({
                    "table": table,
                    "columns": self.get_columns(conn, table),
                    "primary_keys": self.get_primary_keys(conn, table)
                })

            foreign_keys = self.get_foreign_keys(conn)

        return {
            "tables": schema,
            "foreign_keys": foreign_keys
        }

    def get_tables(self, conn):
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT tablename
                FROM pg_catalog.pg_tables
                WHERE schemaname = 'public'
                ORDER BY tablename;
            """)

            return [row[0] for row in cursor.fetchall()]

    def get_columns(self, conn, table_name):
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name = %s
                ORDER BY ordinal_position;
            """, (table_name,))

            return [
                {
                    "name": row[0],
                    "type": row[1],
                    "nullable": row[2] == "YES"
                }
                for row in cursor.fetchall()
            ]

    def get_primary_keys(self, conn, table_name):
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT column_name
                FROM information_schema.key_column_usage
                WHERE table_schema = 'public'
                AND table_name = %s
                AND constraint_name IN (
                    SELECT constraint_name
                    FROM information_schema.table_constraints
                    WHERE table_schema = 'public'
                    AND table_name = %s
                    AND constraint_type = 'PRIMARY KEY'
                )
                ORDER BY ordinal_position;
            """, (table_name, table_name))

            return [row[0] for row in cursor.fetchall()]

    def get_foreign_keys(self, conn):
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    tc.table_name AS from_table,
                    kcu.column_name AS from_column,
                    ccu.table_name AS to_table,
                    ccu.column_name AS to_column
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                    AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_schema = 'public'
                ORDER BY tc.table_name;
            """)

            return [
                {
                    "from_table": row[0],
                    "from_column": row[1],
                    "to_table": row[2],
                    "to_column": row[3]
                }
                for row in cursor.fetchall()
            ]