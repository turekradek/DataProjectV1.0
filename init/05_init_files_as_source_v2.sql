-- 1. Aktualizacja typu ENUM o nowe cele
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'data_target_type') THEN
        CREATE TYPE data_target_type AS ENUM (
            'prometheus_metrics', 
            'grafana_dashboard', 
            'elasticsearch_index', 
            'postgres_table', 
            'postgres_view', 
            'postgres_mview', 
            'kafka_topic'
        );
    END IF;
END$$;

-- 2. Definicja stanów procesu
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'process_state_type') THEN
        CREATE TYPE process_state_type AS ENUM (
            'active',   -- Proces działa normalnie
            'paused',   -- Wstrzymany przez administratora
            'failed',   -- Zatrzymany z powodu błędu
            'completed' -- Proces jednorazowy, zakończony sukcesem
        );
    END IF;
END$$;

-- 3. Tworzenie tabeli
CREATE TABLE IF NOT EXISTS projecttables.files_as_source (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    target_system data_target_type NOT NULL,
    target_name VARCHAR(255) NOT NULL,
    
    -- Nowa kolumna stanu procesu
    process_state process_state_type DEFAULT 'active',
    
    -- Sugestia: Priorytet procesu (1-najniższy, 10-najwyższy)
    priority INTEGER DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    last_modified_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(filename, target_system, target_name)
);

-- 4. Trigger do automatycznej aktualizacji last_modified_at
CREATE OR REPLACE FUNCTION projecttables.update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_modified_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_source_modified
BEFORE UPDATE ON projecttables.files_as_source
FOR EACH ROW EXECUTE FUNCTION projecttables.update_modified_column();

-- 5. Uprawnienia
GRANT ALL PRIVILEGES ON TABLE projecttables.files_as_source TO dataengieneer;
GRANT USAGE, SELECT ON SEQUENCE projecttables.files_as_source_id_seq TO dataengieneer;

-- 6. Przykład użycia (Seed data)
INSERT INTO projecttables.files_as_source (filename, target_system, target_name, process_state, description)
VALUES 
    ('cars.json', 'postgres_view', 'v_cars_summary', 'active', 'Tworzenie widoku analitycznego dla aut'),
    ('test_data.csv', 'elasticsearch_index', 'logs_idx', 'paused', 'Wstrzymane do czasu konfiguracji klastra Elastic')
ON CONFLICT DO NOTHING;