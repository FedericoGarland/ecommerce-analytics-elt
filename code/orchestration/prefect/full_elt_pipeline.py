import os
import subprocess
from dotenv import load_dotenv
import snowflake.connector
from prefect import flow, task

DBT_PROJECT_DIR = r"C:\Users\User\Documents\ecommerce-analytics-elt\code\dbt\ecommerce_dbt"

# Ajusta esto si cambiaste la carpeta
INGESTION_DATE = "2025-12-06"

STAGE_BASE = "ECOMMERCE.RAW.AZURE_RAW_STAGE"
FILE_FORMAT = "ECOMMERCE.RAW.CSV_FORMAT"


def get_conn():
    load_dotenv()
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
    )


@task
def full_refresh_raw():
    """
    FULL REFRESH RAW:
    - TRUNCATE cada tabla
    - COPY INTO desde el archivo exacto (sin regex)
    - FORCE=TRUE para evitar "0 files processed" por load history
    """

    tables = [
        ("ECOMMERCE.RAW.OLIST_CUSTOMERS", "customers", "olist_customers_dataset.csv"),
        ("ECOMMERCE.RAW.OLIST_ORDERS", "orders", "olist_orders_dataset.csv"),
        ("ECOMMERCE.RAW.OLIST_ORDER_ITEMS", "order_items", "olist_order_items_dataset.csv"),
        ("ECOMMERCE.RAW.OLIST_ORDER_PAYMENTS", "order_payments", "olist_order_payments_dataset.csv"),
        ("ECOMMERCE.RAW.OLIST_ORDER_REVIEWS", "order_reviews", "olist_order_reviews_dataset.csv"),
        ("ECOMMERCE.RAW.OLIST_PRODUCTS", "products", "olist_products_dataset.csv"),
        ("ECOMMERCE.RAW.OLIST_SELLERS", "sellers", "olist_sellers_dataset.csv"),
        ("ECOMMERCE.RAW.OLIST_GEOLOCATION", "geolocation", "olist_geolocation_dataset.csv"),
        ("ECOMMERCE.RAW.PRODUCT_CATEGORY_NAME_TRANSLATION", "product_category_name_translation", "product_category_translation.csv"),
    ]

    conn = get_conn()
    cur = conn.cursor()

    for raw_table, folder, filename in tables:
        print(f"\n=== {raw_table} ===")

        # 1) TRUNCATE
        cur.execute(f"TRUNCATE TABLE {raw_table};")
        print("✅ TRUNCATE OK")

        # 2) COPY (archivo exacto)
        copy_sql = f"""
        COPY INTO {raw_table}
        FROM @{STAGE_BASE}/{folder}/ingestion_date={INGESTION_DATE}/{filename}
        FILE_FORMAT = (FORMAT_NAME = {FILE_FORMAT})
        FORCE = TRUE
        ON_ERROR = 'ABORT_STATEMENT';
        """
        cur.execute(copy_sql)

        res = cur.fetchall()
        print("✅ COPY INTO result:")
        for r in res:
            print(r)

    cur.close()
    conn.close()


@task
def dbt_build():
    """
    dbt build = run + test (lo más 'real' para pipelines)
    """
    subprocess.run(["dbt", "run"], cwd=DBT_PROJECT_DIR, check=True)
    subprocess.run(["dbt", "test"], cwd=DBT_PROJECT_DIR, check=True)


@flow(name="full_elt_pipeline")
def full_elt_pipeline():
    full_refresh_raw()
    dbt_build()


if __name__ == "__main__":
    full_elt_pipeline()


# python ./code/orchestration/prefect/full_elt_pipeline.py