CREATE TABLE IF NOT EXISTS close_approaches (
    -- note: needs to be same order as df
    event_id TEXT PRIMARY KEY,
    asteroid_id TEXT NOT NULL,
    name TEXT NOT NULL,
    absolute_magnitude_h REAL,
    diameter_min_km REAL,
    diameter_max_km REAL,
    is_potentially_hazardous INTEGER NOT NULL,
    is_sentry_object INTEGER NOT NULL,
    close_approach_date TEXT NOT NULL,
    close_approach_date_full TEXT NOT NULL,
    relative_velocity_km_s REAL,
    miss_distance_au REAL,
    orbiting_body TEXT NOT NULL
);
