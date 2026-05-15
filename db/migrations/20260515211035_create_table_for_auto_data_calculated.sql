-- migrate:up
CREATE TABLE features.match_auto_data_calc(
    "team_key" VARCHAR NOT NULL,
    "match_key" VARCHAR NOT NULL,
    "actual_time" TIMESTAMPTZ,  
    "last_auto_points" INTEGER,  
    "mean_3_last_auto_points" INTEGER,  
    "max_3_last_auto_points" INTEGER,  
    "min_3_last_auto_points" INTEGER,  
    "std_3_last_auto_points" INTEGER,  
    "trend_3_last_auto_points" INTEGER,  
    "mean_5_last_auto_points" INTEGER,  
    "max_5_last_auto_points" INTEGER,  
    "min_5_last_auto_points" INTEGER,  
    "std_5_last_auto_points" INTEGER,  
    "trend_5_last_auto_points" INTEGER,  
    "mean_10_last_auto_points" INTEGER,  
    "max_10_last_auto_points" INTEGER,  
    "min_10_last_auto_points" INTEGER,  
    "std_10_last_auto_points" INTEGER,  
    "trend_10_last_auto_points" INTEGER,  
    "mean_season_last_auto_points" INTEGER,  
    "max_season_last_auto_points" INTEGER,  
    "min_season_last_auto_points" INTEGER,  
    "std_season_last_auto_points" INTEGER,  
    "trend_season_last_auto_points" INTEGER,  
    "prev_match_count" INTEGER,
    PRIMARY KEY ("team_key","match_key")

);
-- migrate:down

DROP TABLE features.match_auto_data_calc;