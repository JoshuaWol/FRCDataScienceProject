-- SQL dump generated using DBML (dbml.dbdiagram.io)
-- Database: PostgreSQL
-- Generated at: 2026-05-07T00:15:37.505Z

CREATE TABLE "districts" (
  "district_key" varchar UNIQUE PRIMARY KEY NOT NULL,
  "district_code" varchar,
  "district_name" varchar
);

CREATE TABLE "team_info" (
  "team_key" varchar UNIQUE PRIMARY KEY NOT NULL,
  "team_number" integer,
  "name_full" varchar,
  "name_short" varchar,
  "district_key" varchar,
  "rookie_year" int,
  "city" varchar,
  "state_prov" varchar,
  "country" varchar,
  "postal_code" varchar
);

CREATE TABLE "events" (
  "event_key" varchar UNIQUE PRIMARY KEY NOT NULL,
  "year" integer NOT NULL,
  "event" varchar,
  "event_type" varchar,
  "event_code" varchar,
  "date" date,
  "location" varchar,
  "webcast" varchar,
  "week" integer,
  "district_key" varchar
);

CREATE TABLE "match_teams" (
  "match_key" varchar NOT NULL,
  "team_key" varchar NOT NULL,
  "alliance" varchar NOT NULL,
  PRIMARY KEY ("match_key", "team_key")
);

CREATE TABLE "match_data_2026" (
  "match_key" varchar NOT NULL,
  "alliance" integer NOT NULL,
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
  "video_key" varchar,
  "video_type" varchar,
  PRIMARY KEY ("match_key", "alliance")
);

ALTER TABLE "team_info" ADD FOREIGN KEY ("district_key") REFERENCES "districts" ("district_key") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "events" ADD FOREIGN KEY ("district_key") REFERENCES "districts" ("district_key") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "match_teams" ADD FOREIGN KEY ("team_key") REFERENCES "team_info" ("team_key") DEFERRABLE INITIALLY IMMEDIATE;

CREATE TABLE "match_teams_match_data_2026" (
  "match_teams_match_key" varchar,
  "match_data_2026_match_key" varchar,
  PRIMARY KEY ("match_teams_match_key", "match_data_2026_match_key")
);

ALTER TABLE "match_teams_match_data_2026" ADD FOREIGN KEY ("match_teams_match_key") REFERENCES "match_teams" ("match_key") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "match_teams_match_data_2026" ADD FOREIGN KEY ("match_data_2026_match_key") REFERENCES "match_data_2026" ("match_key") DEFERRABLE INITIALLY IMMEDIATE;

