CREATE DATABASE IF NOT EXISTS synthetic_cargo;
USE synthetic_cargo;

CREATE TABLE IF NOT EXISTS Cargo (
    cargo_id VARCHAR(50) PRIMARY KEY,
    cargo_type VARCHAR(100) NOT NULL,
    current_temp DECIMAL(8,2) NOT NULL,
    safe_temp DECIMAL(8,2) NOT NULL,
    max_temp_threshold DECIMAL(8,2) NOT NULL,
    flight_delay_minutes INT NOT NULL DEFAULT 0,
    flight_duration_hours DECIMAL(8,2) NOT NULL,
    viability_percentage DECIMAL(6,2) NOT NULL,
    risk_level VARCHAR(20) NOT NULL
);
