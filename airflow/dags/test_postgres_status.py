from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime


def check_conn():
    hook = PostgresHook(postgres_conn_id="postgres_main")
    try:
        # Próba pobrania połączenia i wykonania prostego zapytania
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()

        print("##########################################################")
        print("✅ SUKCES: POŁĄCZENIE Z POSTGRES DZIAŁA POPRAWNIE!")
        print("##########################################################")
        return "Connection successful"
    except Exception as e:
        print("##########################################################")
        print("❌ BŁĄD: NIE MOŻNA POŁĄCZYĆ SIĘ Z BAZĄ POSTGRES!")
        print(f"SZCZEGÓŁY: {e}")
        print("##########################################################")
        raise e  # Rzucamy błąd, aby zadanie w UI zaświeciło się na czerwono


with DAG(
    dag_id="check_postgres_status_v1",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["mentor_it", "status"],
) as dag:

    test_connection = PythonOperator(task_id="verify_db_connection", python_callable=check_conn)
