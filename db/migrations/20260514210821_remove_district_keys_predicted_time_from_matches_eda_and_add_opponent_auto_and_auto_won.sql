-- migrate:up
ALTER TABLE features.matches_eda DROP COLUMN district_key;
ALTER TABLE features.matches_eda ADD COLUMN opponent_auto_points INTEGER;
ALTER TABLE features.matches_eda ADD COLUMN auto_won INTEGER;
ALTER TABLE features.matches_eda DROP COLUMN predicted_time;

-- migrate:down
ALTER TABLE features.matches_eda ADD COLUMN district_key VARCHAR;
ALTER TABLE features.matches_eda DROP COLUMN opponent_auto_points;
ALTER TABLE features.matches_eda DROP COLUMN auto_won;
ALTER TABLE features.matches_eda ADD COLUMN predicted_time TIMESTAMPTZ;
