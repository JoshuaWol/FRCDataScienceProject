TRUNCATE TABLE features.matches_eda;

WITH alliance_lineups AS (
  SELECT
    match_key, alliance,
    MAX(team_key) FILTER (WHERE rn = 1) AS team_key1,
    MAX(team_key) FILTER (WHERE rn = 2) AS team_key2,
    MAX(team_key) FILTER (WHERE rn = 3) AS team_key3
  FROM (
    SELECT match_key, alliance, team_key,
           ROW_NUMBER() OVER (PARTITION BY match_key, alliance ORDER BY team_key) AS rn
    FROM match_teams
  ) t
  GROUP BY match_key, alliance
)

INSERT INTO features.matches_eda (
       --identity
    match_key, alliance,
    --teams
    team_key1, team_key2, team_key3,
    -- context
    event_key, event_type, district_key, comp_level, match_number, set_number, actual_time, predicted_time,
    --scoring
    total_score, teleop_count, auto_points, transition_points,
    uncounted_points, teleop_points, shift1_points, shift2_points,
    shift3_points, shift4_points, endgame_points, total_auto_points,
    auto_tower_points, end_game_tower_points, total_tower_points, minor_foul_count, 
    major_foul_count, foul_points, adjust_points, ranking_points, winning_alliance, opponent_total_score 

)
SELECT  
    --identity
    md.match_key, md.alliance,
    --teams
    al.team_key1, al.team_key2, al.team_key3,
    -- context
    m.event_key, e.event_type, e.district_key, m.comp_level, m.match_number, m.set_number, m.actual_time, m.predicted_time,
    --scoring
    md.total_score, md.teleop_count, md.auto_points, md.transition_points,
    md.uncounted_points, md.teleop_points, md.shift1_points, md.shift2_points,
    md.shift3_points, md.shift4_points, md.endgame_points, md.total_auto_points,
    md.auto_tower_points, md.end_game_tower_points, md.total_tower_points, md.minor_foul_count, 
    md.major_foul_count, md.foul_points, md.adjust_points, md.ranking_points, m.winning_alliance, opp.total_score
FROM public.match_data_2026 as md
JOIN alliance_lineups as al USING (match_key, alliance)
JOIN public.matches as m USING (match_key)
JOIN features.filtered_events as e USING (event_key)
JOIN public.match_data_2026 as opp
    ON opp.match_key = md.match_key
    AND opp.alliance <> md.alliance





