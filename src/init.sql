-- Create the 'dataeng' role
CREATE ROLE postgres WITH LOGIN PASSWORD 'password';
CREATE ROLE dataeng WITH LOGIN PASSWORD 'password';

-- Grant privileges to the 'dataeng' role 
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dataeng; 
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres; 

-- Create the 'dataeng' schema
CREATE SCHEMA IF NOT EXISTS dataeng;

-- Grant usage on the schema to the 'dataeng' role
GRANT USAGE ON SCHEMA dataeng TO dataeng;
GRANT USAGE ON SCHEMA dataeng TO postgres;

-- Grant all privileges on the schema to the 'dataeng' role
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA dataeng TO dataeng;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA dataeng TO postgres;