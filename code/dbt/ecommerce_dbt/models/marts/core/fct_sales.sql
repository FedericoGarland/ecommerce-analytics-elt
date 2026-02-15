with order_items as (
    select * from {{ ref('stg_order_items') }}
),
orders as (
    select * from {{ ref('stg_orders') }}
)

SELECT
o.order_id, 
o.customer_id, 
oi.product_id, 
oi.seller_id,
o.order_purchase_ts, 
o.delivered_customer_ts, 
o.estimated_delivery_ts, 
oi.price, 
oi.freight_value,
o.order_status
from order_items oi INNER JOIN orders o
ON oi.order_id = o.order_id
