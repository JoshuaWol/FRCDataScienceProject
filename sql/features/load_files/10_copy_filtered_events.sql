TRUNCATE features.filtered_events;
INSERT INTO features.filtered_events
SELECT * FROM public.events
WHERE event_type NOT IN ('-1', '99', '100');