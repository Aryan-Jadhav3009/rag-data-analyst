from analyst.schema_introspector import SchemaIntrospector


connection_params = {
    "host": "localhost",
    "port": 5432,
    "dbname": "demo_analytics",
    "user": "rag_user",
    "password": "rag_password",
}

inspector = SchemaIntrospector(connection_params)

schema = inspector.inspect()

print(schema)