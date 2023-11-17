SELECT user FROM mysql.user WHERE user='grocerystore';

grant usage on *.* to 'grocerystore'@'localhost';

-- Create database
CREATE DATABASE IF NOT EXISTS grocery_store;

grant all privileges on grocery_store.* to 'grocerystore'@'localhost';


-- Use the database
USE grocery_store;

-- Create 'sales' table
CREATE TABLE IF NOT EXISTS sales (
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
CREATE TABLE IF NOT EXISTS products_recieved (
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
CREATE TABLE IF NOT EXISTS products (
    product VARCHAR(66),
    category VARCHAR(16),
    unit_cost FLOAT,
    unit_price FLOAT,
    product_id INT PRIMARY KEY
);

-- Create 'transactions' table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY,
    date DATE,
    account VARCHAR(16),
    transaction_type VARCHAR(16),
    category VARCHAR(16),
    detail VARCHAR(24),
    total FLOAT
);