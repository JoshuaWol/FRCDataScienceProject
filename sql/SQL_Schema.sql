-- SQL dump generated using DBML (dbml.dbdiagram.io)
-- Database: PostgreSQL
-- Generated at: 2026-05-06T21:35:03.578Z

CREATE TABLE "Seasons" (
  "year" integer NOT NULL,
  "gameName" varchar,
  "gameID" integer PRIMARY KEY NOT NULL
);

CREATE TABLE "Districts" (
  "districtCode" varchar PRIMARY KEY NOT NULL,
  "districtName" varchar
);

CREATE TABLE "TeamInfo" (
  "teamNumber" integer NOT NULL,
  "nameFull" varchar,
  "nameShort" varchar,
  "districtCode" varchar,
  "rookieYear" integer,
  "city" varchar,
  "stateProv" varchar,
  "country" varchar
);

CREATE TABLE "Events" (
  "gameID" integer NOT NULL,
  "eventCode" varchar NOT NULL,
  "event" varchar,
  "eventType" varchar,
  "date" date,
  "location" varchar,
  "Webcast" varchar,
  "weekNumber" integer,
  "districtCode" varchar,
  PRIMARY KEY ("gameID", "eventCode")
);

CREATE TABLE "MatchTable" (
  "gameID" integer NOT NULL,
  "eventCode" varchar NOT NULL,
  "matchType" varchar NOT NULL,
  "matchID" integer NOT NULL,
  "matchKey" integer UNIQUE PRIMARY KEY NOT NULL
);

CREATE TABLE "MatchTeams" (
  "matchKey" integer NOT NULL,
  "teamNumber" integer NOT NULL,
  "alliance" varchar NOT NULL,
  PRIMARY KEY ("matchKey", "teamNumber")
);

CREATE TABLE "MatchData2026" (
  "matchKey" integer NOT NULL,
  "alliance" integer NOT NULL,
  "totalScore" integer,
  "teleopCount" integer,
  "autoScore" integer,
  "shift1Points" integer,
  "shift2Points" integer,
  "shift3Points" integer,
  "shift4Points" integer,
  "endgamePoints" integer,
  "autoTowerPoints" integer,
  "totalAutoPoints" integer,
  "endgameTowerPoints" integer,
  "totalTowerPoints" integer,
  "minorFoulCount" integer,
  "majorFoulCount" integer,
  "foulPoints" integer,
  "adjustPoins" integer,
  "RP" integer,
  PRIMARY KEY ("matchKey", "alliance")
);

CREATE UNIQUE INDEX ON "MatchTable" ("gameID", "eventCode", "matchType", "matchID");

ALTER TABLE "TeamInfo" ADD FOREIGN KEY ("districtCode") REFERENCES "Districts" ("districtCode") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "Events" ADD FOREIGN KEY ("gameID") REFERENCES "Seasons" ("gameID") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "MatchTable" ADD FOREIGN KEY ("gameID", "eventCode") REFERENCES "Events" ("gameID", "eventCode") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "MatchTeams" ADD FOREIGN KEY ("matchKey") REFERENCES "MatchTable" ("matchKey") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "MatchTeams" ADD FOREIGN KEY ("teamNumber") REFERENCES "TeamInfo" ("teamNumber") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "MatchData2026" ADD FOREIGN KEY ("matchKey") REFERENCES "MatchTable" ("matchKey") DEFERRABLE INITIALLY IMMEDIATE;
