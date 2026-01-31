from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from db_utils import PostgresManager  # Import Twojej klasy

with DAG(dag_id="db_class_example", start_date=datetime(2026, 1, 1), schedule_interval=None, catchup=False) as dag:

    @task
    def db_operations():
        # Inicjalizacja klasy
        db = PostgresManager()

        # 1. Listowanie
        tables = db.list_tables()

        # # 2. Insert
        # new_user = {
        #     "nb": 50, "name": "Ewa", "lastname": "Klasowa",
        #     "birth": "1995-08-10", "age": 30, "weight": 65.0,
        #     "high": 170, "pesel": "95081012345"
        # }
        # db.insert_record("testtable", new_user)

        # 3. Count
        count = db.get_row_count("testtable")

        return {"tables": tables, "total_rows": count}

    db_operations()
