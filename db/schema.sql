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
-- Name: features; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA features;


--
-- Name: ml_studies; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA ml_studies;


--
-- Name: predictions; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA predictions;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: filtered_events; Type: TABLE; Schema: features; Owner: -
--

CREATE TABLE features.filtered_events (
    event_key character varying NOT NULL,
    year integer NOT NULL,
    event character varying,
    event_type character varying,
    event_code character varying,
    date date,
    location character varying,
    webcast character varying,
    week integer,
    district_key character varying,
    state_prov character varying,
    country character varying
);


--
-- Name: match_auto_data_calc; Type: TABLE; Schema: features; Owner: -
--

CREATE TABLE features.match_auto_data_calc (
    team_key character varying NOT NULL,
    match_key character varying NOT NULL,
    actual_time timestamp with time zone,
    last_auto_points integer,
    mean_3_last_auto_points integer,
    max_3_last_auto_points integer,
    min_3_last_auto_points integer,
    std_3_last_auto_points integer,
    trend_3_last_auto_points integer,
    mean_5_last_auto_points integer,
    max_5_last_auto_points integer,
    min_5_last_auto_points integer,
    std_5_last_auto_points integer,
    trend_5_last_auto_points integer,
    mean_10_last_auto_points integer,
    max_10_last_auto_points integer,
    min_10_last_auto_points integer,
    std_10_last_auto_points integer,
    trend_10_last_auto_points integer,
    mean_season_last_auto_points integer,
    max_season_last_auto_points integer,
    min_season_last_auto_points integer,
    std_season_last_auto_points integer,
    trend_season_last_auto_points integer,
    prev_match_count integer,
    auto_points integer,
    alliance character varying,
    opp_auto_points integer
);


--
-- Name: matches_eda; Type: TABLE; Schema: features; Owner: -
--

CREATE TABLE features.matches_eda (
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
    comp_level character varying NOT NULL,
    match_number integer NOT NULL,
    set_number integer,
    winning_alliance character varying,
    actual_time timestamp with time zone,
    team_key1 character varying NOT NULL,
    team_key2 character varying NOT NULL,
    team_key3 character varying NOT NULL,
    opponent_total_score integer,
    event_type character varying,
    opponent_auto_points integer,
    auto_won integer
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
    district_key character varying,
    state_prov character varying,
    country character varying
);


--
-- Name: match_data_2026; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.match_data_2026 (
    match_key character varying NOT NULL,
    alliance character varying NOT NULL,
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
-- Name: matches; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.matches (
    match_key character varying NOT NULL,
    event_key character varying NOT NULL,
    comp_level character varying NOT NULL,
    match_number integer NOT NULL,
    set_number integer,
    winning_alliance character varying,
    actual_time timestamp with time zone,
    predicted_time timestamp with time zone
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
-- Name: filtered_events filtered_events_pkey; Type: CONSTRAINT; Schema: features; Owner: -
--

ALTER TABLE ONLY features.filtered_events
    ADD CONSTRAINT filtered_events_pkey PRIMARY KEY (event_key);


--
-- Name: match_auto_data_calc match_auto_data_calc_pkey; Type: CONSTRAINT; Schema: features; Owner: -
--

ALTER TABLE ONLY features.match_auto_data_calc
    ADD CONSTRAINT match_auto_data_calc_pkey PRIMARY KEY (team_key, match_key);


--
-- Name: matches_eda matches_eda_pkey; Type: CONSTRAINT; Schema: features; Owner: -
--

ALTER TABLE ONLY features.matches_eda
    ADD CONSTRAINT matches_eda_pkey PRIMARY KEY (match_key, alliance);


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
-- Name: matches matches_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_pkey PRIMARY KEY (match_key);


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
-- Name: filtered_events_year_week_idx; Type: INDEX; Schema: features; Owner: -
--

CREATE INDEX filtered_events_year_week_idx ON features.filtered_events USING btree (year, week);


--
-- Name: idx_events_year_week; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_events_year_week ON public.events USING btree (year, week);


--
-- Name: idx_match_data_match_key; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_match_data_match_key ON public.match_data_2026 USING btree (match_key);


--
-- Name: idx_match_teams_team_key; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_match_teams_team_key ON public.match_teams USING btree (team_key);


--
-- Name: idx_matches_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_matches_date ON public.matches USING btree (actual_time);


--
-- Name: idx_matches_event_key; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_matches_event_key ON public.matches USING btree (event_key);


--
-- Name: events events_district_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_district_key_fkey FOREIGN KEY (district_key) REFERENCES public.districts(district_key) DEFERRABLE;


--
-- Name: match_data_2026 fk_match_data_match; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.match_data_2026
    ADD CONSTRAINT fk_match_data_match FOREIGN KEY (match_key) REFERENCES public.matches(match_key);


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
-- Name: matches matches_event_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_event_key_fkey FOREIGN KEY (event_key) REFERENCES public.events(event_key);


--
-- PostgreSQL database dump complete
--

\unrestrict dbmate


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20260512004914'),
    ('20260512023403'),
    ('20260512023933'),
    ('20260512174020'),
    ('20260512175109'),
    ('20260512204852'),
    ('20260513151709'),
    ('20260513155951'),
    ('20260514210821'),
    ('20260515211035'),
    ('20260518194607'),
    ('20260520183834');
