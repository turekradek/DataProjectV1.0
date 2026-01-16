-- 1. Tworzenie schematu i nadanie uprawnień do niego
CREATE SCHEMA IF NOT EXISTS projecttables;
GRANT USAGE, CREATE ON SCHEMA projecttables TO dataengieneer;

-- 2. Tworzenie tabeli
CREATE TABLE IF NOT EXISTS projecttables.testtable (
    nb SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    birth DATE,
    age INTEGER CHECK (age >= 0),
    weight NUMERIC(5, 2),
    high INTEGER,
    pesel CHAR(11) UNIQUE
);

-- 3. Nadanie uprawnień do tabeli i sekwencji (SERIAL potrzebuje praw do sekwencji!)
GRANT ALL PRIVILEGES ON TABLE projecttables.testtable TO dataengieneer;
GRANT USAGE, SELECT ON SEQUENCE projecttables.testtable_nb_seq TO dataengieneer;

-- 4. Wstawianie danych (z obsługą konfliktów)
INSERT INTO projecttables.testtable (name, lastname, birth, age, weight, high, pesel)
SELECT 
    'User_' || i AS name,
    'LastName_' || i AS lastname,
    birth_date AS birth,
    extract(year from age(birth_date)) AS age,
    (60 + random() * 40)::numeric(5,2) AS weight,
    (160 + (random() * 35))::integer AS high,
    (
        TO_CHAR(birth_date, 'YY') || 
        LPAD((extract(month from birth_date) + CASE WHEN extract(year from birth_date) >= 2000 THEN 20 ELSE 0 END)::text, 2, '0') || 
        TO_CHAR(birth_date, 'DD') || 
        LPAD(floor(random() * 1000)::text, 3, '0') || 
        (CASE WHEN i % 2 = 0 THEN floor(random() * 5) * 2 ELSE floor(random() * 5) * 2 + 1 END)::text || 
        floor(random() * 10)::text 
    ) AS pesel
FROM (
    SELECT 
        i, 
        CURRENT_DATE - (interval '1 day' * floor(random() * 18250)) AS birth_date
    FROM generate_series(1, 50) AS i
) AS sub
ON CONFLICT (pesel) DO NOTHING;

COMMIT;

-- 5. Aktualizacja na realistyczne dane
WITH gender_logic AS (
    SELECT 
        nb,
        (SUBSTRING(pesel, 10, 1)::int % 2 = 0) AS is_female
    FROM projecttables.testtable
),
random_assignments AS (
    SELECT 
        g.nb,
        CASE  
    WHEN g.is_female THEN  
        (ARRAY['Anna', 'Maria', 'Katarzyna', 'Malgorzata', 'Agnieszka'])[floor(random() * 5)::int + 1]
    ELSE  
        (ARRAY['Adam', 'Piotr', 'Krzysztof', 'Andrzej', 'Tomasz'])[floor(random() * 5)::int + 1]
    END as r_name,
        CASE  
    WHEN g.is_female THEN  
        (ARRAY['Kowalska', 'Nowak', 'Wisniewska', 'Wojcik', 'Kowalczyk'])[floor(random() * 5)::int + 1]
    ELSE  
        (ARRAY['Kowalski', 'Nowak', 'Wisniewski', 'Wojcik', 'Kowalczyk'])[floor(random() * 5)::int + 1]
    END as r_lastname
    FROM gender_logic g
)
UPDATE projecttables.testtable t
SET 
    name = ra.r_name,
    lastname = ra.r_lastname
FROM random_assignments ra
WHERE t.nb = ra.nb;

-- Weryfikacja
SELECT * FROM projecttables.testtable;