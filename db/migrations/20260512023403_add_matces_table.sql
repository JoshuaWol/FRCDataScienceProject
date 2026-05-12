--Adding a matches table that has meta data about a match but not scoring info

-- migrate:up
CREATE TABLE matches (
  match_key VARCHAR PRIMARY KEY,
  event_key VARCHAR NOT NULL REFERENCES events(event_key),
  comp_level VARCHAR NOT NULL,       
  match_number INTEGER NOT NULL,
  set_number INTEGER,
  winning_alliance VARCHAR,         
  match_date DATE,
  actual_time TIMESTAMPTZ,
  predicted_time TIMESTAMPTZ
);

-- migrate:down
ALTER TABLE match_data_2026 ADD COLUMN event_key VARCHAR REFERENCES events(event_key);
ALTER TABLE match_data_2026 DROP CONSTRAINT fk_match_data_match;
DROP TABLE matches;
