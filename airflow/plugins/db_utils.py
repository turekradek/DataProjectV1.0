import logging
from airflow.providers.postgres.hooks.postgres import PostgresHook


class PostgresManager:
    def __init__(self, conn_id: str = "postgres_main"):
        self.conn_id = conn_id
        self.hook = PostgresHook(postgres_conn_id=self.conn_id)

    def list_tables(self, schema: str = "projecttables"):
        """Zwraca listę tabel w danym schemacie."""
        sql = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s
        """
        records = self.hook.get_records(sql, parameters=(schema,))
        logging.info(f"Pobrano {len(records)} tabel ze schematu {schema}")
        return [r[0] for r in records]

    def insert_record(self, table: str, data: dict):
        """Wstawia rekord do wskazanej tabeli."""
        # Budujemy dynamicznie kolumny i placeholdery
        columns = ", ".join(data.keys())
        placeholders = ", ".join([f"%({k})s" for k in data.keys()])

        sql = f"""
            INSERT INTO projecttables.{table} ({columns}) 
            VALUES ({placeholders})
            ON CONFLICT (nb) DO NOTHING;
        """

        self.hook.run(sql, parameters=data)
        logging.info(f"Wykonano INSERT do {table} dla ID: {data.get('nb')}")

    def get_row_count(self, table: str):
        """Zwraca liczbę wierszy w tabeli."""
        sql = f"SELECT COUNT(*) FROM projecttables.{table}"
        return self.hook.get_first(sql)[0]

    def get_sample_rows(self, table: str, limit: int = 10, schema: str = "projecttables"):
        # Używamy get_pandas_df, aby łatwo dostać słowniki (wymaga biblioteki pandas w kontenerze)
        # Albo zostajemy przy czystym SQL i mapujemy nazwy kolumn:
        sql = f"SELECT * FROM {schema}.{table} LIMIT %s"

        # Pobieramy kursor, aby wyciągnąć nazwy kolumn
        conn = self.hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (limit,))

        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        # Mapujemy na listę słowników
        results = [dict(zip(columns, row)) for row in rows]

        logging.info(f"Pobrano {len(results)} rekordów z {schema}.{table}")
        return results
