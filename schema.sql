-- SQL schema for the Aquaponics Calculator database.
-- This schema models species, stock batches, water chemistry, feeding, growth, hardware, maintenance, events, and sensors.

CREATE TABLE species (
    species_id SERIAL PRIMARY KEY,
    common_name TEXT NOT NULL,
    latin_name TEXT,
    growth_opt_temp_min DECIMAL,
    growth_opt_temp_max DECIMAL,
    notes TEXT
);

CREATE TABLE stock_batches (
    batch_id SERIAL PRIMARY KEY,
    species_id INTEGER REFERENCES species(species_id),
    hatch_date DATE,
    origin TEXT,
    initial_quantity INTEGER,
    parent_batch_ids TEXT
);

CREATE TABLE sensors (
    sensor_id SERIAL PRIMARY KEY,
    parameter TEXT NOT NULL,
    model TEXT,
    unit TEXT,
    location TEXT,
    automation_capable BOOLEAN DEFAULT FALSE
);

CREATE TABLE water_targets (
    target_id SERIAL PRIMARY KEY,
    parameter TEXT NOT NULL,
    min_value DECIMAL,
    max_value DECIMAL,
    unit TEXT,
    location TEXT,
    sensor_id INTEGER REFERENCES sensors(sensor_id)
);

CREATE TABLE water_readings (
    reading_id SERIAL PRIMARY KEY,
    parameter TEXT NOT NULL,
    value DECIMAL NOT NULL,
    unit TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location TEXT,
    recorded_by INTEGER,
    CONSTRAINT fk_sensor FOREIGN KEY(recorded_by) REFERENCES sensors(sensor_id)
);

CREATE TABLE feeding_plans (
    plan_id SERIAL PRIMARY KEY,
    batch_id INTEGER REFERENCES stock_batches(batch_id),
    daily_ration_g DECIMAL,
    frequency_per_day INTEGER,
    seasonal_adjustment_rule TEXT,
    smart_trigger TEXT
);

CREATE TABLE feed_logs (
    feed_log_id SERIAL PRIMARY KEY,
    batch_id INTEGER REFERENCES stock_batches(batch_id),
    feed_type TEXT,
    amount_g DECIMAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estimated_fcr DECIMAL
);

CREATE TABLE growth_records (
    record_id SERIAL PRIMARY KEY,
    batch_id INTEGER REFERENCES stock_batches(batch_id),
    weight_avg_g DECIMAL,
    length_avg_cm DECIMAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE system_hardware (
    hardware_id SERIAL PRIMARY KEY,
    type TEXT,
    location TEXT,
    status TEXT
);

CREATE TABLE maintenance_logs (
    log_id SERIAL PRIMARY KEY,
    hardware_id INTEGER REFERENCES system_hardware(hardware_id),
    action TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    technician TEXT
);

CREATE TABLE event_logs (
    event_id SERIAL PRIMARY KEY,
    event_type TEXT,
    description TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location TEXT
);
