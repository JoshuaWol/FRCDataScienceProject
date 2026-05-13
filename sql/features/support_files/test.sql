-- SELECT alliance, COUNT(*) FROM features.matches_eda WHERE alliance = 'red' GROUP BY alliance;

-- SELECT alliance, COUNT(*) FROM public.match_data_2026 GROUP BY alliance;

SELECT
    match_key, alliance,
    MAX(team_key) FILTER (WHERE rn = 1) AS team_key1,
    MAX(team_key) FILTER (WHERE rn = 2) AS team_key2,
    MAX(team_key) FILTER (WHERE rn = 3) AS team_key3
  FROM (
    SELECT match_key, alliance, team_key,
           ROW_NUMBER() OVER (PARTITION BY match_key, alliance ORDER BY team_key) AS rn
    FROM match_teams
  ) 
  GROUP BY match_key, alliance
