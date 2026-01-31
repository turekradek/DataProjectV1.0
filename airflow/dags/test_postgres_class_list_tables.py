from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from db_utils import PostgresManager
import logging
from tabulate import tabulate

# W Airflow nie używaj logging.basicConfig - Airflow sam zarządza konfiguracją logów.
logger = logging.getLogger(__name__)

with DAG(dag_id="db_class_list_tables", start_date=datetime(2026, 1, 1), schedule_interval=None, catchup=False) as dag:

    @task
    def db_show_table_rows():
        db = PostgresManager()

        # 1. Pobieranie danych
        # tables = db.list_tables() # Odkomentuj, jeśli chcesz używać w return
        rawss = db.get_sample_rows("testtable", limit=10)

        if rawss:
            # tabulate automatycznie bierze klucze ze słowników jako nagłówki
            table_output = tabulate(rawss, headers="keys", tablefmt="grid")

            logger.info("\n" + table_output)  # Dodajemy nową linię dla przejrzystości
        else:
            logger.info("Tabela jest pusta.")

        logger.info("--- END PREVIEW ---")
        return rawss

    db_show_table_rows()
