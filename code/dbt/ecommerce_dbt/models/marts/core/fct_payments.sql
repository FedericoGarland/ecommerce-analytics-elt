with payments as (
    select * from {{ ref('stg_order_payments') }}
), 

orders as (
    select * from {{ ref('stg_orders') }}
)

SELECT 
p.order_id,
o.customer_id, 
p.payment_sequential, 
p.payment_type, 
p.payment_installments, 
p.payment_value
FROM payments p LEFT JOIN orders o 
ON p.ORDER_ID = o.ORDER_ID