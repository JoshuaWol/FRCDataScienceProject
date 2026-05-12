\restrict dbmate

-- Dumped from database version 17.9 (Ubuntu 17.9-0ubuntu0.25.10.1)
-- Dumped by pg_dump version 17.9 (Ubuntu 17.9-0ubuntu0.25.10.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: production; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA production;


--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

-- *not* creating schema, since initdb creates it


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: districts; Type: TABLE; Schema: production; Owner: -
--

CREATE TABLE production.districts (
    district_key character varying NOT NULL,
    district_code character varying,
    district_name character varying
);


--
-- Name: events; Type: TABLE; Schema: production; Owner: -
--

CREATE TABLE production.events (
    event_key character varying NOT NULL,
    year integer NOT NULL,
    event character varying,
    event_type character varying,
    event_code character varying,
    date date,
    location character varying,
    webcast character varying,
    week integer,
    district_key character varying
);


--
-- Name: match_data_2026; Type: TABLE; Schema: production; Owner: -
--

CREATE TABLE production.match_data_2026 (
    match_key character varying NOT NULL,
    alliance character varying NOT NULL,
    event_key character varying,
    total_score integer,
    teleop_count integer,
    auto_points integer,
    transition_points integer,
    uncounted_points integer,
    teleop_points integer,
    shift1_points integer,
    shift2_points integer,
    shift3_points integer,
    shift4_points integer,
    endgame_points integer,
    total_auto_points integer,
    auto_tower_points integer,
    end_game_tower_points integer,
    total_tower_points integer,
    minor_foul_count integer,
    major_foul_count integer,
    foul_points integer,
    adjust_points integer,
    ranking_points integer,
    video_key character varying,
    video_type character varying
);


--
-- Name: match_teams; Type: TABLE; Schema: production; Owner: -
--

CREATE TABLE production.match_teams (
    match_key character varying NOT NULL,
    team_key character varying NOT NULL,
    alliance character varying NOT NULL
);


--
-- Name: teams; Type: TABLE; Schema: production; Owner: -
--

CREATE TABLE production.teams (
    team_key character varying NOT NULL,
    team_number integer,
    name_full character varying,
    name_short character varying,
    district_code character varying,
    rookie_year integer,
    city character varying,
    state_prov character varying,
    country character varying,
    postal_code character varying
);


--
-- Name: teams_info; Type: TABLE; Schema: production; Owner: -
--

CREATE TABLE production.teams_info (
    team_key text,
    team_number bigint,
    name_full text,
    district_key text,
    rookie_year bigint,
    city text,
    state_prov text,
    country text,
    postal_code text
);


--
-- Name: districts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.districts (
    district_key character varying NOT NULL,
    district_code character varying,
    district_name character varying
);


--
-- Name: events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.events (
    event_key character varying NOT NULL,
    year integer NOT NULL,
    event character varying,
    event_type character varying,
    event_code character varying,
    date date,
    location character varying,
    webcast character varying,
    week integer,
    district_key character varying
);


--
-- Name: match_data_2026; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.match_data_2026 (
    match_key character varying NOT NULL,
    alliance character varying NOT NULL,
    event_key character varying,
    total_score integer,
    teleop_count integer,
    auto_points integer,
    transition_points integer,
    uncounted_points integer,
    teleop_points integer,
    shift1_points integer,
    shift2_points integer,
    shift3_points integer,
    shift4_points integer,
    endgame_points integer,
    total_auto_points integer,
    auto_tower_points integer,
    end_game_tower_points integer,
    total_tower_points integer,
    minor_foul_count integer,
    major_foul_count integer,
    foul_points integer,
    adjust_points integer,
    ranking_points integer,
    video_key character varying,
    video_type character varying
);


--
-- Name: match_teams; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.match_teams (
    match_key character varying NOT NULL,
    team_key character varying NOT NULL,
    alliance character varying NOT NULL
);


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying NOT NULL
);


--
-- Name: teams; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teams (
    team_key character varying NOT NULL,
    team_number integer,
    name_full character varying,
    name_short character varying,
    district_code character varying,
    rookie_year integer,
    city character varying,
    state_prov character varying,
    country character varying,
    postal_code character varying
);


--
-- Name: teams_info; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teams_info (
    team_key text,
    team_number bigint,
    name_full text,
    district_key text,
    rookie_year bigint,
    city text,
    state_prov text,
    country text,
    postal_code text
);


--
-- Name: districts districts_pkey; Type: CONSTRAINT; Schema: production; Owner: -
--

ALTER TABLE ONLY production.districts
    ADD CONSTRAINT districts_pkey PRIMARY KEY (district_key);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: production; Owner: -
--

ALTER TABLE ONLY production.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (event_key);


--
-- Name: match_data_2026 match_data_2026_pkey; Type: CONSTRAINT; Schema: production; Owner: -
--

ALTER TABLE ONLY production.match_data_2026
    ADD CONSTRAINT match_data_2026_pkey PRIMARY KEY (match_key, alliance);


--
-- Name: match_teams match_teams_pkey; Type: CONSTRAINT; Schema: production; Owner: -
--

ALTER TABLE ONLY production.match_teams
    ADD CONSTRAINT match_teams_pkey PRIMARY KEY (match_key, team_key);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: production; Owner: -
--

ALTER TABLE ONLY production.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (team_key);


--
-- Name: districts districts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.districts
    ADD CONSTRAINT districts_pkey PRIMARY KEY (district_key);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (event_key);


--
-- Name: match_data_2026 match_data_2026_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.match_data_2026
    ADD CONSTRAINT match_data_2026_pkey PRIMARY KEY (match_key, alliance);


--
-- Name: match_teams match_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.match_teams
    ADD CONSTRAINT match_teams_pkey PRIMARY KEY (match_key, team_key);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (team_key);


--
-- Name: events events_district_key_fkey; Type: FK CONSTRAINT; Schema: production; Owner: -
--

ALTER TABLE ONLY production.events
    ADD CONSTRAINT events_district_key_fkey FOREIGN KEY (district_key) REFERENCES production.districts(district_key) DEFERRABLE;


--
-- Name: match_data_2026 match_data_2026_event_key_fkey; Type: FK CONSTRAINT; Schema: production; Owner: -
--

ALTER TABLE ONLY production.match_data_2026
    ADD CONSTRAINT match_data_2026_event_key_fkey FOREIGN KEY (event_key) REFERENCES production.events(event_key) DEFERRABLE;


--
-- Name: match_teams match_teams_match_key_alliance_fkey; Type: FK CONSTRAINT; Schema: production; Owner: -
--

ALTER TABLE ONLY production.match_teams
    ADD CONSTRAINT match_teams_match_key_alliance_fkey FOREIGN KEY (match_key, alliance) REFERENCES production.match_data_2026(match_key, alliance) DEFERRABLE;


--
-- Name: match_teams match_teams_team_key_fkey; Type: FK CONSTRAINT; Schema: production; Owner: -
--

ALTER TABLE ONLY production.match_teams
    ADD CONSTRAINT match_teams_team_key_fkey FOREIGN KEY (team_key) REFERENCES production.teams(team_key) DEFERRABLE;


--
-- Name: events events_district_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_district_key_fkey FOREIGN KEY (district_key) REFERENCES public.districts(district_key) DEFERRABLE;


--
-- Name: match_data_2026 match_data_2026_event_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.match_data_2026
    ADD CONSTRAINT match_data_2026_event_key_fkey FOREIGN KEY (event_key) REFERENCES public.events(event_key) DEFERRABLE;


--
-- Name: match_teams match_teams_match_key_alliance_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.match_teams
    ADD CONSTRAINT match_teams_match_key_alliance_fkey FOREIGN KEY (match_key, alliance) REFERENCES public.match_data_2026(match_key, alliance) DEFERRABLE;


--
-- Name: match_teams match_teams_team_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.match_teams
    ADD CONSTRAINT match_teams_team_key_fkey FOREIGN KEY (team_key) REFERENCES public.teams(team_key) DEFERRABLE;


--
-- PostgreSQL database dump complete
--

\unrestrict dbmate


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20260512004914');
