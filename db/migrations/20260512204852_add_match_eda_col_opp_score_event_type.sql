-- migrate:up
ALTER TABLE features.matches_eda ADD COLUMN opponent_total_score INTEGER;
ALTER TABLE features.matches_eda ADD COLUMN event_type VARCHAR;

-- migrate:down
ALTER TABLE features.matches_eda DROP COLUMN opponent_total_score;
ALTER TABLE features.matches_eda ADD COLUMN event_type;
