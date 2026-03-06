{{ config(materialized='view') }}

WITH raw_data AS (
    -- Referencing the raw data we loaded into Snowflake earlier
    SELECT * FROM {{ source('energy_raw_data', 'LONDON_ENERGY_RAW') }}
)

SELECT
    -- Standardizing column names
    LCLID AS meter_id,
    "DAY" AS reading_date,
    ENERGY_SUM AS energy_consumption_kwh,
    
    -- Generating a Surrogate Key
    MD5(LCLID || "DAY") AS reading_unique_id

FROM raw_data
