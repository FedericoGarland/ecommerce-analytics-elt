with payments as (
    select * from {{ ref('stg_order_payments')}}
), 

orders as (
    select * from {{ ref('stg_orders')}}
)

SELECT 
o.customer_id, 
p.*
FROM payments p LEFT JOIN orders o 
ON p.ORDER_ID = o.ORDER_ID