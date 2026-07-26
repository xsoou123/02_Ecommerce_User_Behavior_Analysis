CREATE DATABASE IF NOT EXISTS olist_ecommerce_analysis;

USE olist_ecommerce_analysis;


CREATE TABLE customers
(
customer_id VARCHAR(50),
customer_unique_id VARCHAR(50),
customer_zip_code_prefix INT,
customer_city VARCHAR(100),
customer_state VARCHAR(10)
);


CREATE TABLE orders
(
order_id VARCHAR(50),
customer_id VARCHAR(50),
order_status VARCHAR(30),
order_purchase_timestamp DATETIME,
order_delivered_customer_date DATETIME,
order_estimated_delivery_date DATETIME
);


CREATE TABLE order_items
(
order_id VARCHAR(50),
order_item_id INT,
product_id VARCHAR(50),
seller_id VARCHAR(50),
price DECIMAL(10,2),
freight_value DECIMAL(10,2)
);
