-- 1. Metadane dla CSV
CREATE TABLE IF NOT EXISTS projecttables.filescsv (
    id SERIAL PRIMARY KEY,
    numer INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL UNIQUE,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_date TIMESTAMPTZ DEFAULT NULL
);

-- 2. Metadane dla JSON
CREATE TABLE IF NOT EXISTS projecttables.filesjson (
    id SERIAL PRIMARY KEY,
    numer INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL UNIQUE,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_date TIMESTAMPTZ DEFAULT NULL
);

-- 3. Definicja celów (Targets)
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'target_system_type') THEN
        CREATE TYPE target_system_type AS ENUM (
            'postgres_table', 
            'postgres_view', 
            'postgres_mview', 
            'prometheus_metric', 
            'grafana_dashboard', 
            'elasticsearch_index', 
            'kafka_topic'
        );
    END IF;
END $$;

-- 4. Tabela łącząca plik z procesem (Droga B)
CREATE TABLE IF NOT EXISTS projecttables.files_as_source (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL, 
    target_system target_system_type NOT NULL,
    target_name VARCHAR(255) NOT NULL, 
    process_state VARCHAR(20) DEFAULT 'active', 
    priority INTEGER DEFAULT 5,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(filename, target_system, target_name)
);

-- 5. Uprawnienia (Zarządzanie dostępem dla roli dataengieneer)
-- Nadajemy uprawnienia do wszystkich tabel i sekwencji w schemacie (podejście profesjonalne)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA projecttables TO dataengieneer;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA projecttables TO dataengieneer;

-- 6. Komentarze dokumentacyjne
COMMENT ON TABLE projecttables.filescsv IS 'Logowanie procesów importu plików CSV dla audytu ETL';
COMMENT ON TABLE projecttables.filesjson IS 'Logowanie procesów importu plików JSON dla audytu ETL';
COMMENT ON TABLE projecttables.files_as_source IS 'Mapowanie plików na konkretne systemy docelowe i procesy';