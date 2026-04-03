
-- 1. A procedure to insert a new user by name and phone;
-- if the user already exists, update their phone

CREATE OR REPLACE PROCEDURE insert_user(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


-- 2. A procedure to insert many new users from a list of names and phones
-- Validate phone correctness (must be 11 digits) and report invalid contacts

CREATE OR REPLACE PROCEDURE insert_many_users(p_names TEXT[], p_phones TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    invalid_contacts TEXT := '';
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        -- Correct variable name: p_phones[i], not phones[i]
        IF p_phones[i] ~ '^\d{11}$' THEN
            CALL insert_user(p_names[i], p_phones[i]);
        ELSE
            invalid_contacts := invalid_contacts || p_names[i] || ':' || p_phones[i] || ', ';
        END IF;
    END LOOP;

    IF invalid_contacts <> '' THEN
        RAISE NOTICE 'Invalid contacts: %', invalid_contacts;
    END IF;
END;
$$;


-- 3. A procedure to delete data from the table by username or phone

CREATE OR REPLACE PROCEDURE delete_data(p_name VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE (p_name IS NOT NULL AND name = p_name)
       OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;