DELIMITER $$

-- Create the SafeDiv function
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    -- Check if the second number (b) is 0
    IF b = 0 THEN
        RETURN 0;
    ELSE
        -- Return the result of a divided by b
        RETURN a / b;
    END IF;
END$$

DELIMITER ;

