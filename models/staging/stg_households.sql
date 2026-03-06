{{ config(materialized='view') }}

WITH raw_households AS (
    SELECT * FROM {{ source('energy_raw_data', 'LONDON_HOUSEHOLDS_RAW') }}
)

SELECT
    -- 1. Standardizing names
    LCLID AS meter_id,
    ACORN AS acorn_category,
    ACORN_GROUPED AS acorn_group,
    
    -- 2. Creating a Surrogate Key
    -- This allows us to join households to consumption data efficiently
    MD5(LCLID) AS household_unique_id

FROM raw_households