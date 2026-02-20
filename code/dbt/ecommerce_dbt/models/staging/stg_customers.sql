with source as (

    select * 
    from {{ source('raw', 'OLIST_CUSTOMERS') }}

),

stg_table as (

    select
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    from source

)

select * from stg_table
