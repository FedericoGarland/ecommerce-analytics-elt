{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='order_item_key'
) }}

with order_items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

final as (

    select
        concat(o.order_id, oi.order_item_id) as order_item_key,
        o.order_id,
        o.customer_id,
        oi.order_item_id,
        oi.product_id,
        oi.seller_id,
        o.order_purchase_ts,
        o.delivered_customer_ts,
        o.estimated_delivery_ts,
        oi.price,
        oi.freight_value,
        o.order_status

    from order_items oi
    inner join orders o
        on oi.order_id = o.order_id

    where o.order_status not in ('canceled', 'unavailable')

    {% if is_incremental() %}
        and o.order_purchase_ts >= (
            select dateadd(day, -7, max(order_purchase_ts))
            from {{ this }}
        )
    {% endif %}

)

select * from final