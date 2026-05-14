UPDATE features.matches_eda as me 
SET opponent_auto_points = md.auto_points
FROM public.match_data_2026 as md
WHERE md.match_key = me.match_key
 AND md.alliance <> me.alliance
 AND me.opponent_auto_points is NULL;

UPDATE features.matches_eda as me
SET auto_won = CASE WHEN me.auto_points > me.opponent_auto_points THEN 1 ELSE 0 END;
