import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Path
from db_utils import PostgresManager

# Ładowanie .env
load_dotenv()
db_url = os.getenv("DATABASE_URL")

app = FastAPI(title="Data Project API")

# Inicjalizacja managera
db = PostgresManager(conn_id_or_uri=db_url)


@app.on_event("startup")
def verify_db_connection():
    """Sprawdza czy baza jest dostępna przy starcie kontenera."""
    try:
        # Próba wykonania prostego zapytania, aby sprawdzić DNS i połączenie
        # Zakładamy, że masz metodę do listowania tabel lub po prostu ping
        logging.info(f"Connecting to: {db_url.split('@')[-1]}")  # Loguje tylko hosta dla bezpieczeństwa
    except Exception as e:
        logging.error(f"FATAL: Could not connect to DB: {e}")


@app.get("/")
def read_root():
    return {"status": "online", "message": "FastAPI is running"}


@app.get("/tables/preview/{table_name}")
def get_table_preview(table_name: str = Path(..., example="testtable"), limit: int = 10):
    try:
        data = db.get_sample_rows(table_name, limit=limit)
        if not data and data != []:
            raise Exception("No data returned")
        return {"table": table_name, "count": len(data), "rows": data}
    except Exception as e:
        # Logujemy szczegóły błędu w terminalu, a użytkownikowi dajemy czytelny komunikat
        logging.error(f"Error previewing table {table_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
