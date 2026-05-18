-- migrate:up
ALTER TABLE features.match_auto_data_calc ADD COLUMN auto_points INTEGER;
ALTER TABLE features.match_auto_data_calc ADD COLUMN alliance VARCHAR;
ALTER TABLE features.match_auto_data_calc ADD COLUMN opp_auto_points INTEGER;


-- migrate:down
ALTER TABLE features.match_auto_data_calc DROP COLUMN auto_points;
ALTER TABLE features.match_auto_data_calc DROP COLUMN opp_auto_points;
ALTER TABLE features.match_auto_data_calc DROP COLUMN alliance;
