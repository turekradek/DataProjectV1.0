from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.decorators import task
from datetime import datetime
import logging

# Jako conn_id podaj nazwę, którą ustawiłeś w YAML (np. POSTGRES_DB)
CONN_ID = "postgres_main"

with DAG(
    dag_id="list_postgres_tables",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["debug", "postgres"],
) as dag:

    list_tables = PostgresOperator(
        task_id="list_tables_task",
        postgres_conn_id=CONN_ID,
        sql="""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'projecttables'
            ORDER BY table_name;
        """,
        # To sprawi, że wynik zapytania pojawi się w logach taska
        do_xcom_push=True,
    )

    # --- TA LINIA I FUNKCJA WYPISZĄ XCOM DO LOGÓW ---
    @task
    def log_xcom_result(data):
        logging.info(f"Otrzymano z XCom: {data}")
        # return data
        for row in data:
            logging.info(f" -> Schemat: {row[0]}, Tabela: {row[1]}")

    log_xcom_result(list_tables.output)
