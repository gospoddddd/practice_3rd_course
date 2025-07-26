CREATE TABLE IF NOT EXISTS public.demo_data (
    id SERIAL PRIMARY KEY,
    name TEXT,
    amount NUMERIC,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO public.demo_data(name, amount)
VALUES ('foo', 10.5), ('bar', 20.0), ('baz', 30.75)
ON CONFLICT DO NOTHING;
