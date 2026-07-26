/*
==================================================
Olist E-commerce Business Analysis SQL
Database:
olist_ecommerce_analysis

Purpose:
Business KPI
Customer Analysis
Sales Analysis
Product Analysis
Payment Analysis
RFM Analysis

Author:
Hongyang

==================================================
*/


-- =================================================
-- 0. 使用数据库
-- =================================================

USE olist_ecommerce_analysis;



-- =================================================
-- 1. 数据规模检查
-- =================================================


-- 用户数量

SELECT
COUNT(DISTINCT customer_unique_id)
AS total_customers
FROM customers;



-- 订单数量

SELECT
COUNT(DISTINCT order_id)
AS total_orders
FROM orders;



-- 商品数量

SELECT
COUNT(DISTINCT product_id)
AS total_products
FROM products;



-- =================================================
-- 2. GMV销售分析
-- =================================================


-- 总销售额

SELECT

ROUND(
SUM(price + freight_value),
2
)
AS total_GMV

FROM order_items;



-- 平均订单金额

SELECT

ROUND(
SUM(price + freight_value)
/
COUNT(DISTINCT order_id),
2
)

AS average_order_value

FROM order_items;



-- =================================================
-- 3. 月销售趋势分析
-- =================================================


SELECT


DATE_FORMAT(
o.order_purchase_timestamp,
'%Y-%m'
)
AS month,


ROUND(
SUM(oi.price),
2
)
AS sales


FROM orders o


JOIN order_items oi

ON o.order_id = oi.order_id


GROUP BY month


ORDER BY month;




-- =================================================
-- 4. 订单状态分析
-- =================================================


SELECT


order_status,


COUNT(order_id)
AS order_count


FROM orders


GROUP BY order_status


ORDER BY order_count DESC;



-- =================================================
-- 5. 用户地区分析
-- =================================================


SELECT


customer_state,


COUNT(
DISTINCT customer_unique_id
)
AS customers


FROM customers


GROUP BY customer_state


ORDER BY customers DESC;



-- =================================================
-- 6. 商品销售排名
-- =================================================


SELECT


p.product_category_name,


ROUND(
SUM(oi.price),
2
)
AS sales


FROM order_items oi


JOIN products p


ON oi.product_id = p.product_id


GROUP BY
p.product_category_name


ORDER BY sales DESC;



-- =================================================
-- 7. Top10商品分析
-- =================================================


SELECT


oi.product_id,


COUNT(
oi.order_id
)
AS order_count,


ROUND(
SUM(oi.price),
2
)
AS sales



FROM order_items oi



GROUP BY oi.product_id



ORDER BY sales DESC



LIMIT 10;



-- =================================================
-- 8. 支付方式分析
-- =================================================


SELECT


payment_type,


COUNT(order_id)
AS payment_count,


ROUND(
SUM(payment_value),
2
)
AS total_payment



FROM payments



GROUP BY payment_type



ORDER BY total_payment DESC;




-- =================================================
-- 9. 用户复购分析
-- =================================================


-- 每个用户购买次数


SELECT


customer_unique_id,


COUNT(order_id)
AS purchase_count



FROM customers c



JOIN orders o


ON c.customer_id=o.customer_id



GROUP BY customer_unique_id



ORDER BY purchase_count DESC;




-- =================================================
-- 10. 复购用户比例
-- =================================================


SELECT


ROUND(

SUM(
CASE

WHEN order_count > 1

THEN 1

ELSE 0

END

)

/

COUNT(*)

*

100

,2)

AS repeat_purchase_rate



FROM

(


SELECT


c.customer_unique_id,


COUNT(o.order_id)
AS order_count



FROM customers c



JOIN orders o


ON c.customer_id=o.customer_id



GROUP BY c.customer_unique_id


) t;




-- =================================================
-- 11. 用户消费排行榜
-- =================================================


SELECT


c.customer_unique_id,


ROUND(
SUM(oi.price),
2
)

AS total_spending



FROM customers c



JOIN orders o


ON c.customer_id=o.customer_id



JOIN order_items oi


ON o.order_id=oi.order_id



GROUP BY c.customer_unique_id



ORDER BY total_spending DESC



LIMIT 20;




-- =================================================
-- 12. RFM分析
-- =================================================


/*

R:
最近购买时间

F:
购买次数

M:
消费金额

*/


SELECT


c.customer_unique_id,


DATEDIFF(

MAX(
o.order_purchase_timestamp
),

'2018-10-01'

)

AS recency,


COUNT(
DISTINCT o.order_id
)

AS frequency,


ROUND(
SUM(oi.price),
2
)

AS monetary



FROM customers c



JOIN orders o


ON c.customer_id=o.customer_id



JOIN order_items oi


ON o.order_id=oi.order_id



GROUP BY c.customer_unique_id



ORDER BY monetary DESC;



-- =================================================
-- 13. 高价值客户
-- =================================================


SELECT


c.customer_unique_id,


COUNT(
DISTINCT o.order_id
)

AS orders,


ROUND(
SUM(oi.price),
2
)

AS spending



FROM customers c



JOIN orders o


ON c.customer_id=o.customer_id



JOIN order_items oi


ON o.order_id=oi.order_id



GROUP BY c.customer_unique_id



HAVING orders >= 5



ORDER BY spending DESC;



-- =================================================
-- 14. 创建分析结果视图
-- =================================================


USE olist_ecommerce_analysis;



-- ===============================
-- KPI Summary
-- ===============================

DROP VIEW IF EXISTS v_kpi_summary;


CREATE VIEW v_kpi_summary AS


SELECT

'Customers' AS metric,

COUNT(DISTINCT customer_unique_id) AS value


FROM customers



UNION ALL



SELECT

'Orders',

COUNT(DISTINCT order_id)


FROM orders



UNION ALL



SELECT

'GMV',

ROUND(
SUM(price + freight_value),
2
)


FROM order_items;




-- ===============================
-- 月销售趋势
-- ===============================

DROP VIEW IF EXISTS v_monthly_sales;


CREATE VIEW v_monthly_sales AS


SELECT


DATE_FORMAT(
o.order_purchase_timestamp,
'%Y-%m'
)

AS month,


ROUND(
SUM(oi.price),
2
)

AS sales


FROM orders o


JOIN order_items oi

ON o.order_id = oi.order_id


GROUP BY month


ORDER BY month;




-- ===============================
-- 用户地区分析
-- ===============================


DROP VIEW IF EXISTS v_customer_region;



CREATE VIEW v_customer_region AS


SELECT


customer_state,


COUNT(
DISTINCT customer_unique_id
)

AS customers


FROM customers


GROUP BY customer_state


ORDER BY customers DESC;





-- ===============================
-- 商品类别销售
-- ===============================


DROP VIEW IF EXISTS v_category_sales;



CREATE VIEW v_category_sales AS


SELECT


p.product_category_name,


ROUND(
SUM(oi.price),
2
)

AS sales


FROM order_items oi


JOIN products p


ON oi.product_id=p.product_id


GROUP BY p.product_category_name


ORDER BY sales DESC;




-- ===============================
-- Top商品
-- ===============================


DROP VIEW IF EXISTS v_top_products;



CREATE VIEW v_top_products AS


SELECT


oi.product_id,


COUNT(order_id)
AS order_count,


ROUND(
SUM(price),
2
)

AS sales



FROM order_items oi


GROUP BY product_id


ORDER BY sales DESC


LIMIT 20;





-- ===============================
-- 支付分析
-- ===============================


DROP VIEW IF EXISTS v_payment_analysis;



CREATE VIEW v_payment_analysis AS


SELECT


payment_type,


COUNT(order_id)
AS payment_count,


ROUND(
SUM(payment_value),
2
)

AS total_payment


FROM payments


GROUP BY payment_type;


-- ===============================
-- 用户复购
-- ===============================


DROP VIEW IF EXISTS v_repeat_purchase;



CREATE VIEW v_repeat_purchase AS


SELECT


customer_unique_id,


COUNT(order_id)

AS order_count



FROM customers c


JOIN orders o


ON c.customer_id=o.customer_id


GROUP BY customer_unique_id;





-- ===============================
-- RFM
-- ===============================


DROP VIEW IF EXISTS v_rfm_analysis;



CREATE VIEW v_rfm_analysis AS


SELECT


c.customer_unique_id,


DATEDIFF(

MAX(o.order_purchase_timestamp),

'2018-10-01'

)

AS recency,


COUNT(
DISTINCT o.order_id
)

AS frequency,


ROUND(
SUM(oi.price),
2
)

AS monetary



FROM customers c


JOIN orders o

ON c.customer_id=o.customer_id


JOIN order_items oi

ON o.order_id=oi.order_id



GROUP BY c.customer_unique_id;



-- =================================================
-- END
-- =================================================