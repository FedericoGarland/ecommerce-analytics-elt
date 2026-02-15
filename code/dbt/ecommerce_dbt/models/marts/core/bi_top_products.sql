{{ config(
    materialized = 'view'
)}}

WITH sales AS (
    select * from {{ ref('fct_sales') }}
), 

products AS (
   select * from {{ ref('dim_products') }}
)

SELECT 
p.product_category_name, 
SUM(s.price) AS revenue
FROM sales s INNER JOIN products p  
ON s.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY SUM(s.price) DESC