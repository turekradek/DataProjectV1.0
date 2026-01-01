from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime


def list_tables():
    # Używamy Twojego poprawionego połączenia
    hook = PostgresHook(postgres_conn_id="postgres_main")

    # Zapytanie wyklucza tabele systemowe, skupiając się na 'public'
    sql = """
        SELECT table_name 
         solemn FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """

    try:
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        tables = cursor.fetchall()

        print("##########################################################")
        if tables:
            print(f"✅ ZNALEZIONO {len(tables)} TABEL W SCHEMACIE PUBLIC:")
            for table in tables:
                print(f" -> {table[0]}")
        else:
            print("⚠️ POŁĄCZONO, ALE NIE ZNALEZIONO ŻADNYCH TABEL W 'public'.")
        print("##########################################################")

    except Exception as e:
        print(f"❌ BŁĄD PODCZAS INSPEKCJI: {e}")
        raise e


with DAG(
    dag_id="inspect_postgres_tables_v1",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["mentor_it", "exploration"],
) as dag:

    inspect_task = PythonOperator(task_id="list_public_tables", python_callable=list_tables)
