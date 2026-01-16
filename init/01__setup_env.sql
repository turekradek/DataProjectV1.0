-- 1. Tworzenie dodatkowych baz danych
-- Uwaga: W Postgres nie ma CREATE DATABASE IF NOT EXISTS, więc używamy triku:
SELECT 'CREATE DATABASE airflow' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'airflow')\gexec

-- 2. Tworzenie użytkowników i ról
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'dataengieneer') THEN
        CREATE ROLE dataengieneer WITH LOGIN PASSWORD 'password';
    END IF;
END
$$;

-- 3. Przygotowanie schematu w głównej bazie (dbpostgres)
CREATE SCHEMA IF NOT EXISTS projecttables;
ALTER SCHEMA projecttables OWNER TO dataengieneer;

-- 4. Uprawnienia dla Airflow (wykonuje się w kontekście bazy dbpostgres, 
-- ale Airflow i tak sam zarządza swoją bazą po połączeniu)
GRANT ALL PRIVILEGES ON DATABASE airflow TO ${POSTGRES_USER:-postgres};