-- migrate:up
CREATE INDEX idx_matches_event_key ON matches (event_key);
CREATE INDEX idx_matches_date ON matches (actual_time);
CREATE INDEX idx_match_teams_team_key ON match_teams (team_key);
CREATE INDEX idx_match_data_match_key ON match_data_2026 (match_key);
CREATE INDEX idx_events_year_week ON events (year, week);   -- composite

-- migrate:down
DROP INDEX IF EXISTS idx_matches_event_key;
DROP INDEX IF EXISTS idx_matches_date ;
DROP INDEX IF EXISTS idx_match_teams_team_key ;
DROP INDEX IF EXISTS idx_match_data_match_key ;
DROP INDEX IF EXISTS idx_events_year_week;   -- composite
