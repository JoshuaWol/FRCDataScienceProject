-- migrate:up
ALTER TABLE public.events ADD COLUMN state_prov VARCHAR;
ALTER TABLE public.events ADD COLUMN country VARCHAR;

-- migrate:down
ALTER TABLE public.events DROP COLUMN state_prov;
ALTER TABLE public.events DROP COLUMN country;