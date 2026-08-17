from rag.sql_validator import (
    SQLValidator,
    SQLValidationError
)


schema = {
    "tables": [
        {
            "table": "customers",
            "columns": [
                {"name": "id"},
                {"name": "name"},
                {"name": "email"},
                {"name": "signup_date"}
            ]
        },
        {
            "table": "orders",
            "columns": [
                {"name": "id"},
                {"name": "customer_id"},
                {"name": "product_id"},
                {"name": "quantity"},
                {"name": "order_date"}
            ]
        },
        {
            "table": "products",
            "columns": [
                {"name": "id"},
                {"name": "name"},
                {"name": "category"},
                {"name": "price"}
            ]
        }
    ]
}


validator = SQLValidator()


tests = [
    (
        """
        SELECT *
        FROM customers;
        """,
        "VALID SELECT"
    ),

    (
        """
        SELECT o.quantity, p.price
        FROM orders o
        JOIN products p
            ON o.product_id = p.id;
        """,
        "VALID JOIN"
    ),

    (
        """
        SELECT o.revenue
        FROM orders o;
        """,
        "UNKNOWN COLUMN"
    ),

    (
        """
        SELECT *
        FROM payments;
        """,
        "UNKNOWN TABLE"
    ),

    (
        """
        DELETE FROM customers;
        """,
        "DELETE"
    ),

    (
        """
        SELECT *
        FROM customers;

        DELETE FROM customers;
        """,
        "MULTIPLE STATEMENTS"
    )
]


for sql, name in tests:

    print("=" * 60)
    print(name)

    try:
        validator.validate(
            sql,
            schema
        )

        print("VALID")

    except SQLValidationError as e:

        print("REJECTED:")
        print(e)