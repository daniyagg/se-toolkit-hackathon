-- Database initialization script
CREATE DATABASE watertracker;

\c watertracker

CREATE TABLE IF NOT EXISTS water_log (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    cups INTEGER NOT NULL DEFAULT 0,
    UNIQUE(user_id, date)
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_water_log_user_date ON water_log(user_id, date);
