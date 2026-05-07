-- SQL dump generated using DBML (dbml.dbdiagram.io)
-- Database: PostgreSQL
-- Generated at: 2026-05-06T22:29:54.019Z

CREATE TABLE "Districts" (
  "districtKey" varchar UNIQUE PRIMARY KEY NOT NULL,
  "districtCode" varchar,
  "districtName" varchar
);

CREATE TABLE "TeamInfo" (
  "teamKey" varchar UNIQUE PRIMARY KEY NOT NULL,
  "teamNumber" integer,
  "nameFull" varchar,
  "nameShort" varchar,
  "districtKey" varchar,
  "rookieYear" integer,
  "city" varchar,
  "stateProv" varchar,
  "country" varchar
);

CREATE TABLE "Events" (
  "eventKey" varchar UNIQUE PRIMARY KEY NOT NULL,
  "year" integer NOT NULL,
  "event" varchar,
  "eventType" varchar,
  "date" date,
  "location" varchar,
  "Webcast" varchar,
  "weekNumber" integer,
  "districtKey" varchar
);

CREATE TABLE "MatchTable" (
  "matchKey" varchar UNIQUE PRIMARY KEY NOT NULL,
  "eventKey" varchar NOT NULL,
  "year" integer,
  "matchLevel" varchar
);

CREATE TABLE "MatchTeams" (
  "matchKey" varchar NOT NULL,
  "teamKey" varchar NOT NULL,
  "alliance" varchar NOT NULL,
  PRIMARY KEY ("matchKey", "teamKey")
);

CREATE TABLE "MatchData2026" (
  "matchKey" varchar NOT NULL,
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

ALTER TABLE "TeamInfo" ADD FOREIGN KEY ("districtKey") REFERENCES "Districts" ("districtKey") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "Events" ADD FOREIGN KEY ("districtKey") REFERENCES "Districts" ("districtKey") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "MatchTable" ADD FOREIGN KEY ("eventKey") REFERENCES "Events" ("eventKey") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "MatchTeams" ADD FOREIGN KEY ("matchKey") REFERENCES "MatchTable" ("matchKey") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "MatchTeams" ADD FOREIGN KEY ("teamKey") REFERENCES "TeamInfo" ("teamKey") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "MatchData2026" ADD FOREIGN KEY ("matchKey") REFERENCES "MatchTable" ("matchKey") DEFERRABLE INITIALLY IMMEDIATE;
