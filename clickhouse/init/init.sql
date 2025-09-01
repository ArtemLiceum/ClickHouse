CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.orders_for_analytics
(
    order_id String,
    order_datetime DateTime,
    customer_id UInt64,
    customer_login String,
    customer_name String,
    customer_last_name String,
    customer_age UInt8,
    product_id UInt64,
    product_title String,
    product_category_id UInt64,
    product_category_title String,
    product_tags Array(String),
    amount UInt32,
    discount Float32,
    total_price Float64,
    version UInt64
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(order_datetime)
ORDER BY (order_datetime, order_id);
