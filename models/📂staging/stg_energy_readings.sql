{{ config(materialized='view') }}

WITH raw_data AS (
    -- Import the raw data from our source declaration
    SELECT * FROM {{ source('energy_raw_data', 'LONDON_ENERGY_RAW') }}
)

SELECT
    -- 1. Standardizing column names for better usability
    LCLID AS meter_id,
    DATETIME AS reading_time,
    KWH_PER_HH_MAX AS energy_consumption_kwh,
    
    -- 2. Generating a Surrogate Key (The "Senior" Engineering Move)
    -- This creates a unique ID for every single row based on the meter and the time.
    -- Essential for de-duplication and joining to other tables later.
    MD5(LCLID || DATETIME) AS reading_unique_id

FROM raw_data