-- SELECT string_agg(column_name, ', ')
-- FROM information_schema.columns
-- WHERE table_schema = 'public' and table_name = 'match_data_2026' and column_name NOT IN ('video_type', 'video_key');

-- SELECT string_agg('m.'||column_name, ', ')
-- FROM information_schema.columns
-- WHERE table_schema = 'public' and table_name = 'match_data_2026' and column_name NOT IN ('video_type', 'video_key')

SELECT string_agg(column_name, ',')
FROM information_schema.columns
WHERE table_schema = 'features' and table_name = 'matches_eda'