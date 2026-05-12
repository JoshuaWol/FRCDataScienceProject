-- migrate:up
CREATE SCHEMA features;
CREATE SCHEMA predictions;

-- migrate:down
DROP SCHEMA features;
DROP SCHEMA predictions;
