{{ config(materialized='view') }}

WITH household_summary AS (
    SELECT 
        meter_id,
        AVG(energy_consumption_kwh) as avg_daily_consumption,
        MAX(energy_consumption_kwh) as peak_consumption
    FROM {{ ref('stg_energy_readings') }}
    GROUP BY 1
    -- Only keeping households that have a valid average calculation
    HAVING AVG(energy_consumption_kwh) IS NOT NULL 
       AND AVG(energy_consumption_kwh) > 0
),

ranked_households AS (
    SELECT
        meter_id,
        avg_daily_consumption,
        peak_consumption,
        -- Using Window Function for segmentation
        NTILE(10) OVER (ORDER BY avg_daily_consumption DESC) AS consumption_decile
    FROM household_summary
)

SELECT * FROM ranked_households