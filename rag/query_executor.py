import psycopg2


class QueryExecutor:

    def execute(self, connection_params, sql):

        with psycopg2.connect(
            **connection_params
        ) as conn:

            with conn.cursor() as cursor:

                cursor.execute(sql)

                columns = [
                    column[0]
                    for column in cursor.description
                ]

                rows = cursor.fetchall()

        return {
            "columns": columns,
            "rows": rows
        }