with reviews as (
    select * from {{ ref('stg_order_reviews')}}
), 

orders as (
    select * from {{ ref('stg_orders')}}
),

order_items as (
    select * from {{ ref('stg_order_items')}}
)

SELECT 
o.customer_id, 
oi.seller_id, 
oi.product_id,
r.*
FROM reviews r LEFT JOIN orders o   
ON r.order_id = o.order_id 
INNER JOIN order_items oi  
ON o.order_id = oi.order_id 
