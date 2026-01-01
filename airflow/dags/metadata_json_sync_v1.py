from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import os
from datetime import datetime
import logging
from airflow.models import Variable

JSON_FOLDER = "/opt/airflow/filesjson"
CONN_ID = "postgres_main"


def get_json_list():
    files = [f for f in os.listdir(JSON_FOLDER) if f.endswith(".json")]
    return files


def check_db_content():
    hook = PostgresHook(postgres_conn_id=CONN_ID)
    records = hook.get_records("SELECT filename FROM files_json")
    return [r[0] for r in records]


def insert_new_json_files(ti):
    # Pobieranie flag konfiguracyjnych (Best Practice: wewnątrz taska)
    debug_mode = Variable.get("debug_mode", default_var=False)
    # Domyślnie True dla bezpieczeństwa
    dry_run = Variable.get("dry_run", default_var=True)

    all_files = ti.xcom_pull(task_ids="list_json_files") or []
    existing_files = ti.xcom_pull(task_ids="check_json_database") or []

    if debug_mode:
        logging.info(f"DEBUG: Wszystkie pliki w folderze: {all_files}")
        logging.info(f"DEBUG: Pliki już obecne w bazie: {existing_files}")

    new_files = [f for f in all_files if f not in existing_files]

    if not new_files:
        logging.info("Brak nowych plików JSON.")
        return

    hook = PostgresHook(postgres_conn_id=CONN_ID)

    for f in new_files:
        full_path = os.path.join(JSON_FOLDER, f)

        if not os.path.exists(full_path):
            logging.warning(f"Plik {f} zniknął przed przetworzeniem!")
            continue

        file_size = os.path.getsize(full_path) // 1024

        if debug_mode:
            logging.info(f"DEBUG: Przetwarzanie pliku: {f}, rozmiar: {file_size}KB")

        # Logika Dry Run
        if dry_run:
            logging.info(f"[DRY RUN] Ominięto zapis pliku JSON do bazy: {f}")
            continue

        sql = """
            INSERT INTO files_json (
                filename, extension, added, 
                validated, validation_time, 
                table_created, table_name, 
                file_size_kb, row_count, error_message
            )
            VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s)
        """

        params = (f, "json", False, None, False, None, file_size, None, None)
        hook.run(sql, parameters=params)
        logging.info(f"ZAPISANO PRODUKCYJNIE JSON: {f} ({file_size} KB)")


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
