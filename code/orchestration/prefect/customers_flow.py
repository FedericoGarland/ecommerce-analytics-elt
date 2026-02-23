import os
import subprocess

from dotenv import load_dotenv
import snowflake.connector
from prefect import flow, task

# Ruta fija a tu proyecto dbt
DBT_PROJECT_DIR = r"C:\Users\User\Documents\ecommerce-analytics-elt\code\dbt\ecommerce_dbt"


@task
def truncate_table():
    """
    1) Cargar credenciales
    2) Conectar a Snowflake
    3) Ejecutar COPY INTO directamente
    """

    load_dotenv()

    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
    )

    cur = conn.cursor()

    copy_sql = """
    TRUNCATE TABLE ECOMMERCE.RAW.OLIST_CUSTOMERS;
    """

    cur.execute(copy_sql)

    results = cur.fetchall()

    print("✅ COPY INTO result:")
    for row in results:
        print(row)

    cur.close()
    conn.close()


@task
def ingest_customers():
    """
    1) Cargar credenciales
    2) Conectar a Snowflake
    3) Ejecutar COPY INTO directamente
    """

    load_dotenv()

    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
    )

    cur = conn.cursor()

    copy_sql = """
    COPY INTO ECOMMERCE.RAW.OLIST_CUSTOMERS
    FROM @ECOMMERCE.RAW.AZURE_RAW_STAGE/customers/ingestion_date=2025-12-06
    FILE_FORMAT = (FORMAT_NAME = ECOMMERCE.RAW.CSV_FORMAT)
    PATTERN = '.*\\.csv.*'
    ON_ERROR = 'ABORT_STATEMENT'
    FORCE = TRUE;
    """

    cur.execute(copy_sql)

    results = cur.fetchall()

    print("✅ COPY INTO result:")
    for row in results:
        print(row)

    cur.close()
    conn.close()


@task
def run_dbt_staging():
    """
    Ejecutar dbt para crear/actualizar stg_customers
    """
    subprocess.run(
        ["dbt", "run", "--select", "stg_customers"],
        cwd=DBT_PROJECT_DIR,
        check=True
    )


@flow(name="customers_pipeline_simple")
def customers_pipeline_simple():
    truncate_table()
    ingest_customers()
    run_dbt_staging()


if __name__ == "__main__":
    customers_pipeline_simple()