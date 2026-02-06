import logging
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Próba importu Hooka - jeśli nie ma Airflow, przejdzie do except
try:
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    AIRFLOW_AVAILABLE = True
except ImportError:
    AIRFLOW_AVAILABLE = False


class PostgresManager:
    def __init__(self, conn_id_or_uri: str = None):
        """
        conn_id_or_uri: Może to być 'postgres_main' (Airflow)
                        lub 'postgresql://user:pass@host:port/db'
        """
        self.conn_uri = conn_id_or_uri or os.getenv("DATABASE_URL")
        self.hook = None

        if AIRFLOW_AVAILABLE and not self.conn_uri.startswith("postgresql://"):
            # Tryb Airflow
            self.hook = PostgresHook(postgres_conn_id=self.conn_uri or "postgres_main")
            logging.info("PostgresManager: Uruchomiono w trybie Airflow (Hook).")
        else:
            # Tryb Standardowy (FastAPI/Flask)
            logging.info("PostgresManager: Uruchomiono w trybie Standardowym (psycopg2).")

    def _get_cursor(self):
        """Pomocnicza metoda do pobierania kursora niezależnie od trybu."""
        if self.hook:
            conn = self.hook.get_conn()
            return conn.cursor()
        else:
            conn = psycopg2.connect(self.conn_uri)
            # RealDictCursor sprawia, że wiersze to od razu słowniki!
            return conn.cursor(cursor_factory=RealDictCursor)

    def get_sample_rows(self, table: str, limit: int = 10, schema: str = "projecttables"):
        sql = f"SELECT * FROM {schema}.{table} LIMIT %s"

        # W trybie Hook (Airflow)
        if self.hook:
            conn = self.hook.get_conn()
            cursor = conn.cursor()
            cursor.execute(sql, (limit,))
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

        # W trybie Standardowym (FastAPI/Flask)
        with self._get_cursor() as cur:
            cur.execute(sql, (limit,))
            return cur.fetchall()

    def get_row_count(self, table: str, schema: str = "projecttables"):
        sql = f"SELECT COUNT(*) FROM {schema}.{table}"
        if self.hook:
            return self.hook.get_first(sql)[0]

        with self._get_cursor() as cur:
            cur.execute(sql)
            res = cur.fetchone()
            return res["count"] if isinstance(res, dict) else res[0]
