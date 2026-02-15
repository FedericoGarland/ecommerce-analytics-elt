select
  try_to_number(geolocation_zip_code_prefix) as geolocation_zip_code_prefix,
  try_to_double(geolocation_lat) as geolocation_lat,
  try_to_double(geolocation_lng) as geolocation_lng,
  geolocation_city,
  geolocation_state
from {{ source('raw', 'OLIST_GEOLOCATION') }}
