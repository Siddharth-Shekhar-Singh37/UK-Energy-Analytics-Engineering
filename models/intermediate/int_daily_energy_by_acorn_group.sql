{{ config(materialized='view') }}

-- 1. Import the cleaned energy readings
WITH energy_readings AS (
    SELECT * FROM {{ ref('stg_energy_readings') }}
),

-- 2. Import the household metadata
households AS (
    SELECT * FROM {{ ref('stg_households') }}
),

-- 3. Join the datasets (The "Heavy Lifting")
joined AS (
    SELECT
        e.reading_unique_id,
        e.meter_id,
        e.reading_date,
        e.energy_consumption_kwh,
        h.acorn_group,
        h.acorn_category
    FROM energy_readings e
    LEFT JOIN households h 
        ON e.meter_id = h.meter_id
)

SELECT * FROM joined