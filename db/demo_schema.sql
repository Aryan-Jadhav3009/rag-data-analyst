CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    order_date DATE NOT NULL,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(id),

    CONSTRAINT fk_orders_product
        FOREIGN KEY (product_id)
        REFERENCES products(id)
);

INSERT INTO customers (name, email, signup_date) VALUES
('Aarav Shah', 'aarav@example.com', '2025-01-10'),
('Riya Mehta', 'riya@example.com', '2025-02-15'),
('Karan Patil', 'karan@example.com', '2025-03-20'),
('Neha Joshi', 'neha@example.com', '2025-04-05');

INSERT INTO products (name, category, price) VALUES
('Laptop', 'Electronics', 70000.00),
('Phone', 'Electronics', 30000.00),
('Headphones', 'Accessories', 2000.00),
('Keyboard', 'Accessories', 3000.00);

INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES
(1, 1, 1, '2025-05-01'),
(1, 3, 2, '2025-05-03'),
(2, 2, 1, '2025-05-10'),
(2, 4, 1, '2025-05-11'),
(3, 2, 2, '2025-06-01'),
(3, 3, 1, '2025-06-05'),
(4, 1, 1, '2025-06-10'),
(4, 4, 2, '2025-06-12');