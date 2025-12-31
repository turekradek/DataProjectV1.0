-- Create the postgres role with password
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT
      FROM   pg_catalog.pg_roles
      WHERE  rolname = 'postgres') THEN

      CREATE ROLE postgres WITH LOGIN PASSWORD 'postgres';
   END IF;
END
$$;

-- Create the postgres database
CREATE DATABASE postgres
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

-- Create the dataeng database
CREATE DATABASE dataeng
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;


-- -- Create the 'dataeng' role
-- CREATE ROLE postgres WITH LOGIN PASSWORD 'password';
-- CREATE ROLE dataeng WITH LOGIN PASSWORD 'password';

-- -- Grant privileges to the 'dataeng' role 
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dataeng; 
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres; 

-- -- Create the 'dataeng' schema
-- CREATE SCHEMA IF NOT EXISTS dataeng;

-- -- Grant usage on the schema to the 'dataeng' role
-- GRANT USAGE ON SCHEMA dataeng TO dataeng;
-- GRANT USAGE ON SCHEMA dataeng TO postgres;

-- -- Grant all privileges on the schema to the 'dataeng' role
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA dataeng TO dataeng;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA dataeng TO postgres;
