--  Add a generated column for the first letter of the 'name'
ALTER TABLE names 
ADD COLUMN first_letter CHAR(1) GENERATED ALWAYS AS (LEFT(name, 1)) STORED;

-- Create the composite index on 'first_letter' and 'score'
CREATE INDEX idx_name_first_score ON names (first_letter, score);
