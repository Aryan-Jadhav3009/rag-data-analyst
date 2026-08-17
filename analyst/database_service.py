import psycopg2


class DatabaseService:

    def test_connection(self, database):

        connection_params = (
            database.get_connection_params()
        )

        try:

            with psycopg2.connect(
                **connection_params
            ):

                return True

        except psycopg2.Error:

            return False