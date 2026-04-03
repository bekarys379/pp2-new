-- 1. Function that returns all records matching a pattern (part of name or phone)
CREATE OR REPLACE FUNCTION matching_patterns(p TEXT)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT name, phone
    FROM phonebook
    WHERE name ILIKE '%' || p || '%'
       OR phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


-- 2. Function that queries data from the table with pagination (LIMIT and OFFSET)
CREATE OR REPLACE FUNCTION pagination(p_limits INT, p_offset INT)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT name, phone
    FROM phonebook
    ORDER BY name
    LIMIT p_limits OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;