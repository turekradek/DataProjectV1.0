from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os


# Funkcja pomocnicza do listowania plików
def list_directory_content(directory_path):
    print(f"Sprawdzam ścieżkę: {directory_path}")
    if os.path.exists(directory_path):
        files = os.listdir(directory_path)
        print(f" \n\nZnaleziono {len(files)} \t plików w {directory_path}:")
        for file in files:
            print(f"\t- {file}")
    else:
        print(f"BŁĄD: Katalog {directory_path} nie istnieje!")
        raise FileNotFoundError(f"Path {directory_path} not found")


with DAG(
    dag_id="check_folders_visibility_v1",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["mentor_it", "debug"],
) as dag:

    check_csv = PythonOperator(task_id="list_csv_files", python_callable=list_directory_content, op_args=["/filescsv"])

    check_json = PythonOperator(
        task_id="list_json_files", python_callable=list_directory_content, op_args=["/filesjson"]
    )

    check_csv
    check_json
