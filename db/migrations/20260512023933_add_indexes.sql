-- migrate:up
CREATE INDEX IF NOT EXISTS idx_matches_event_key ON matches (event_key);
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches (match_date);
CREATE INDEX IF NOT EXISTS idx_matches_event_key ON matches (event_key);
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches (match_date);
CREATE INDEX IF NOT EXISTS idx_match_teams_team_key ON match_teams (team_key);
CREATE INDEX IF NOT EXISTS idx_match_data_match_key ON match_data_2026 (match_key);
CREATE INDEX IF NOT EXISTS idx_events_year_week ON events (year, week);   -- composite

-- migrate:down
DROP INDEX IF EXISTS idx_matches_event_key ON matches (event_key);
DROP INDEX IF EXISTS idx_matches_date ON matches (match_date);
DROP INDEX IF EXISTS idx_matches_event_key ON matches (event_key);
DROP INDEX IF EXISTS idx_matches_date ON matches (match_date);
DROP INDEX IF EXISTS idx_match_teams_team_key ON match_teams (team_key);
DROP INDEX IF EXISTS idx_match_data_match_key ON match_data_2026 (match_key);
DROP INDEX IF EXISTS idx_events_year_week ON events (year, week);   -- composite
