from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import os
from datetime import datetime

# Ścieżki i konfiguracja
JSON_FOLDER = "/opt/airflow/filesjson"
CONN_ID = "postgres_main"


def get_json_list():
    # Pobieramy tylko pliki .json
    files = [f for f in os.listdir(JSON_FOLDER) if f.endswith(".json")]
    return files


def check_db_content():
    hook = PostgresHook(postgres_conn_id=CONN_ID)
    # Sprawdzamy tabelę files_json
    records = hook.get_records("SELECT filename FROM files_json")
    return [r[0] for r in records]


def insert_new_json_files(ti):
    all_files = ti.xcom_pull(task_ids="list_json_files")
    existing_files = ti.xcom_pull(task_ids="check_json_database")

    new_files = [f for f in all_files if f not in existing_files]

    if not new_files:
        print("Brak nowych plików JSON.")
        return

    hook = PostgresHook(postgres_conn_id=CONN_ID)

    for f in new_files:
        full_path = os.path.join(JSON_FOLDER, f)
        file_size = os.path.getsize(full_path) // 1024  # rozmiar w KB

        sql = """
            INSERT INTO files_json (
                filename, extension, added, 
                validated, validation_time, 
                table_created, table_name, 
                file_size_kb, row_count, error_message
            )
            VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s)
        """

        params = (
            f,  # filename
            "json",  # extension
            False,  # validated
            None,  # validation_time
            False,  # table_created
            None,  # table_name
            file_size,  # file_size_kb
            None,  # row_count
            None,  # error_message
        )

        hook.run(sql, parameters=params)
        print(f"Zarejestrowano plik JSON: {f} ({file_size} KB)")


with DAG(
    dag_id="json_metadata_sync_v1",
    start_date=datetime(2025, 1, 1),
    schedule="30 3,5,11,15,23 * * *",
    catchup=False,
    tags=["mentor_it", "etl", "json"],
) as dag:

    t1 = PythonOperator(task_id="list_json_files", python_callable=get_json_list)
    t2 = PythonOperator(task_id="check_json_database", python_callable=check_db_content)
    t3 = PythonOperator(task_id="insert_new_json_files", python_callable=insert_new_json_files)

    t1 >> t2 >> t3
