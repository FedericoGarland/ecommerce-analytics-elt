import os
import subprocess

from dotenv import load_dotenv
import snowflake.connector
from prefect import flow, task

# =========================
# CONFIG (edit if needed)
# =========================
# Ruta a tu carpeta dbt (ajústala si tu nombre difiere)
DBT_PROJECT_DIR = r"C:\Users\User\Documents\ecommerce-analytics-elt\code\dbt\ecommerce_dbt"


@task
def snowflake_smoke_query():
    """
    1) Lee credenciales desde .env
    2) Conecta a Snowflake
    3) Ejecuta un SELECT simple para validar sesión (rol/warehouse/db)
    """
    load_dotenv()  # lee .env del directorio donde ejecutas el script

    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
    )

    cur = conn.cursor()
    cur.execute("SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_TIMESTAMP()")
    print("✅ Snowflake OK:", cur.fetchone())

    cur.close()
    conn.close()


@task
def dbt_smoke_cmd():
    """
    Ejecuta un comando dbt desde Python.
    Usamos subprocess porque dbt es un CLI (command line tool).
    """
    subprocess.run(["dbt", "--version"], cwd=DBT_PROJECT_DIR, check=True)


@flow(name="smoke_flow_simple")
def smoke_flow_simple():
    """
    Flujo completo:
    1) Validar Snowflake
    2) Validar dbt
    """
    snowflake_smoke_query()
    dbt_smoke_cmd()


if __name__ == "__main__":
    smoke_flow_simple()