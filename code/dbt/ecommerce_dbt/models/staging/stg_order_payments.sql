select
  order_id,
  try_to_number(payment_sequential) as payment_sequential,
  payment_type,
  try_to_number(payment_installments) as payment_installments,
  try_to_decimal(payment_value, 18, 2) as payment_value
from {{ source('raw', 'OLIST_ORDER_PAYMENTS') }}
