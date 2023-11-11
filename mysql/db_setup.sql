-- Create database
CREATE DATABASE IF NOT EXISTS grocery_store;

-- Use the database
USE grocery_store;

-- Set a password for the root user
ALTER USER 'root'@'localhost' IDENTIFIED BY '${DB_ROOT_PASSWORD}';

-- Create 'sales' table
CREATE TABLE sales (
    sales_id INT PRIMARY KEY,
    invoice_number INT,
    date DATE,
    employee VARCHAR(16),
    payment_type VARCHAR(16),
    platform VARCHAR(16),
    qty INT,
    total FLOAT,
    product_id INT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create 'products_recieved' table
CREATE TABLE products_recieved (
    purchase_id INT PRIMARY KEY,
    invoice_number INT,
    date DATE,
    employee VARCHAR(16),
    account VARCHAR(16),
    platform VARCHAR(16),
    unit_cost FLOAT,
    qty INT,
    unit_price FLOAT,
    total FLOAT,
    product_id INT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create 'products' table
CREATE TABLE products (
    product VARCHAR(66),
    category VARCHAR(16),
    unit_cost FLOAT,
    unit_price FLOAT,
    product_id INT PRIMARY KEY
);

-- Create 'transactions' table
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    date DATE,
    account VARCHAR(16),
    transaction_type VARCHAR(16),
    category VARCHAR(16),
    detail VARCHAR(24),
    total FLOAT
);



