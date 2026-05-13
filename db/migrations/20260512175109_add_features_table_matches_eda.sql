-- migrate:up
CREATE TABLE features.matches_eda(
    "match_key" varchar NOT NULL,
    "alliance" varchar NOT NULL,
    "event_key" varchar,
    "district_key" varchar,
    "total_score" integer,
    "teleop_count" integer,
    "auto_points" integer,
    "transition_points" integer,
    "uncounted_points" integer,
    "teleop_points" integer,
    "shift1_points" integer,
    "shift2_points" integer,
    "shift3_points" integer,
    "shift4_points" integer,
    "endgame_points" integer,
    "total_auto_points" integer,
    "auto_tower_points" integer,
    "end_game_tower_points" integer,
    "total_tower_points" integer,
    "minor_foul_count" integer,
    "major_foul_count" integer,
    "foul_points" integer,
    "adjust_points" integer,
    "ranking_points" integer,
    "comp_level" VARCHAR NOT NULL,       
    "match_number" INTEGER NOT NULL,
    "set_number" INTEGER,
    "winning_alliance" VARCHAR,         
    "actual_time" TIMESTAMPTZ,
    "predicted_time" TIMESTAMPTZ,
    "team_key1" varchar NOT NULL,
    "team_key2" varchar NOT NULL,
    "team_key3" varchar NOT NULL,
    PRIMARY KEY ("match_key", "alliance")
);

-- migrate:down
DROP TABLE features.matches_eda;


