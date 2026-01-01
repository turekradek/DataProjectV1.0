from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import os
from datetime import datetime

CSV_FOLDER = "/opt/airflow/filescsv"
CONN_ID = "postgres_main"


def get_csv_list():
    files = [f for f in os.listdir(CSV_FOLDER) if f.endswith(".csv")]
    return files


def check_db_content():
    hook = PostgresHook(postgres_conn_id=CONN_ID)
    records = hook.get_records("SELECT filename FROM files_csv")
    return [r[0] for r in records]


def insert_new_files(ti):
    all_files = ti.xcom_pull(task_ids="list_files")
    existing_files = ti.xcom_pull(task_ids="check_database")

    new_files = [f for f in all_files if f not in existing_files]

    if not new_files:
        print("Brak nowych plików.")
        return

    hook = PostgresHook(postgres_conn_id=CONN_ID)

    for f in new_files:
        full_path = os.path.join(CSV_FOLDER, f)
        # Pobieranie metadanych pliku
        file_size = os.path.getsize(full_path) // 1024  # rozmiar w KB
        extension = f.split(".")[-1]

        sql = """
            INSERT INTO files_csv (
                filename, extension, added, 
                validated, validation_time, 
                table_created, table_name, 
                file_size_kb, row_count, error_message
            )
            VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s)
        """
        # Wypełniamy wartościami domyślnymi dla nowego pliku
        params = (
            f,  # filename
            extension,  # extension
            False,  # validated
            None,  # validation_time
            False,  # table_created
            None,  # table_name
            file_size,  # file_size_kb
            None,  # row_count (wypełnisz później podczas importu danych)
            None,  # error_message
        )

        hook.run(sql, parameters=params)
        print(f"Zarejestrowano plik: {f} ({file_size} KB)")


with DAG(
    dag_id="csv_metadata_sync_v2",
    start_date=datetime(2025, 1, 1),
    schedule="30 3,5,11,15,23 * * *",  # Twoja specyficzna godzina
    catchup=False,
    tags=["mentor_it", "etl"],
) as dag:

    t1 = PythonOperator(task_id="list_files", python_callable=get_csv_list)
    t2 = PythonOperator(task_id="check_database", python_callable=check_db_content)
    t3 = PythonOperator(task_id="insert_new_files", python_callable=insert_new_files)

    t1 >> t2 >> t3
