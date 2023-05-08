CREATE TABLE cidades (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    humidity INTEGER,
    description TEXT,
    temp_celsius NUMERIC(6, 2),
    temp_min_celsius NUMERIC(6, 2),
    temp_max_celsius NUMERIC(6, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);