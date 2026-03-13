{{ config(
    materialized='table',
    tags=['core', 'dimension']
) }}

/*
  
  using DISTINCT to ensure the Dimension table has a strict grain of 
  1 Row per Household (Meter). We pull from the enriched intermediate model
  to grab the pre-calculated behavioral segments.
*/

WITH enriched_data AS (
    SELECT * FROM {{ ref('int_energy_acorn_enriched') }}
),

unique_households AS (
    SELECT DISTINCT
        meter_id,
        acorn_group,
        acorn_category,
        consumption_decile,  -- The 1 to 10 ranking we calculated earlier
        peak_consumption     -- The max energy they ever used
    FROM enriched_data
    -- Defensive filter: Ensuring we don't bring NULL meters into our clean dimension
    WHERE meter_id IS NOT NULL 
)

SELECT * FROM unique_households