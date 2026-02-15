select
  seller_id,
  try_to_number(seller_zip_code_prefix) as seller_zip_code_prefix,
  seller_city,
  seller_state
from {{ source('raw', 'OLIST_SELLERS') }}
