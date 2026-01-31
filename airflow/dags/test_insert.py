from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

CONN_ID = "postgres_main"

with DAG(
    dag_id="test_db_insert_params",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["clean_code", "params"],
) as dag:

    insert_with_params = PostgresOperator(
        task_id="insert_with_params_task",
        postgres_conn_id=CONN_ID,
        sql="""
            INSERT INTO projecttables.testtable (nb, name, lastname, birth, age, weight, high, pesel) 
            VALUES (%(nb)s, %(name)s, %(lastname)s, %(birth)s, %(age)s, %(weight)s, %(high)s, %(pesel)s)
            ON CONFLICT (nb) DO NOTHING;
        """,
        parameters={
            "nb": 51,
            "name": "Jan",
            "lastname": "Nowak",
            "birth": "1985-11-12",
            "age": 40,
            "weight": 85.5,
            "high": 178,
            "pesel": "85111298765",
        },
    )

    insert_with_params
