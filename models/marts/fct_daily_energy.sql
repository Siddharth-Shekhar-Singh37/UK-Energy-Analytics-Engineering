{{ config(
    materialized='table',
    tags=['core', 'fact']
) }}

/*
 
  The grain of this Fact table is exactly 1 row per Meter per Day.
  We exclude dimensional text (like Acorn group names) to keep the table narrow and fast.
*/

WITH enriched_data AS (
    SELECT * FROM {{ ref('int_energy_acorn_enriched') }}
),

fact_events AS (
    SELECT
        reading_unique_id AS energy_fact_id,  -- Our Primary Key
        meter_id,                             -- Our Foreign Key (links to dim_households)
        reading_date,
        
        -- The Core Metrics
        energy_consumption_kwh,
        moving_avg_7d,
        consumption_variance_pct,
        
        -- The Anomaly Flag (Boolean conversion for BI efficiency)
        CASE 
            WHEN usage_anomaly_flag = 'High Spike' THEN TRUE 
            ELSE FALSE 
        END AS is_high_spike
        
    FROM enriched_data
)

SELECT * FROM fact_events