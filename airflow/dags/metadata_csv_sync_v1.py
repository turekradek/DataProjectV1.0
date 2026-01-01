from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
import os
import logging
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
    # Pobieranie flag konfiguracyjnych
    debug_mode = Variable.get("debug_mode", default_var=False)
    # Domyślnie True - dopóki nie stworzysz zmiennej w UI, nic nie zostanie zapisane
    dry_run = Variable.get("dry_run", default_var=True)

    all_files = ti.xcom_pull(task_ids="list_files") or []
    existing_files = ti.xcom_pull(task_ids="check_database") or []

    if debug_mode:
        logging.info(f"DEBUG: Pliki w folderze: {all_files}")
        logging.info(f"DEBUG: Pliki w bazie: {existing_files}")

    new_files = [f for f in all_files if f not in existing_files]

    if not new_files:
        logging.info("Brak nowych plików.")
        return

    hook = PostgresHook(postgres_conn_id=CONN_ID)

    for f in new_files:
        full_path = os.path.join(CSV_FOLDER, f)

        if not os.path.exists(full_path):
            logging.warning(f"Plik {f} zniknął przed przetworzeniem!")
            continue

        file_size = os.path.getsize(full_path) // 1024
        extension = f.split(".")[-1]

        if debug_mode:
            logging.info(f"DEBUG: Przetwarzanie {f}, rozmiar: {file_size}KB")

        if dry_run:
            logging.info(f"[DRY RUN] Ominięto zapis pliku do bazy: {f}")
            continue

        sql = """
            INSERT INTO files_csv (
                filename, extension, added, 
                validated, validation_time, 
                table_created, table_name, 
                file_size_kb, row_count, error_message
            )
            VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s)
        """

        params = (f, extension, False, None, False, None, file_size, None, None)
        hook.run(sql, parameters=params)
        logging.info(f"ZAPISANO PRODUKCYJNIE: {f} ({file_size} KB)")


with DAG(
    dag_id="csv_metadata_sync_v2",
    start_date=datetime(2025, 1, 1),
    schedule="30 3,5,11,15,23 * * *",
    catchup=False,
    tags=["mentor_it", "etl"],
) as dag:

    t1 = PythonOperator(task_id="list_files", python_callable=get_csv_list)
    t2 = PythonOperator(task_id="check_database", python_callable=check_db_content)
    t3 = PythonOperator(task_id="insert_new_files", python_callable=insert_new_files)

    t1 >> t2 >> t3
