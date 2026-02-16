{{ config(
    materialized = 'view'
)}}

WITH sales AS (
    select * from {{ ref('fct_sales') }}
)

SELECT 
CAST(order_purchase_ts AS DATE) AS order_date, 
SUM(price) AS revenue, 
COUNT(DISTINCT(order_id)) AS orders 
FROM sales 
GROUP BY 1
ORDER BY 1 ASC
