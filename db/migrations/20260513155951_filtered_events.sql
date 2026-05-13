-- migrate:up
CREATE TABLE features.filtered_events (LIKE public.events INCLUDING ALL);

-- migrate:down
DROP TABLE features.filtered_events;
