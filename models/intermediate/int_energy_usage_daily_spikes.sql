{{ config(materialized='view') }}

WITH daily_usage AS (
    SELECT * FROM {{ ref('stg_energy_readings') }}
),

/* 
   The 'Senior' Logic: 
   We calculate a 7-day rolling baseline and a Day-over-Day variance.
   In Utilities, this is the foundation for Leakage Detection and Peak Demand forecasting.
*/
usage_metrics AS (
    SELECT
        reading_unique_id,
        meter_id,
        reading_date,
        energy_consumption_kwh,
        
        -- Window Function: 7-Day Moving Average to smooth volatility
        AVG(energy_consumption_kwh) OVER (
            PARTITION BY meter_id 
            ORDER BY reading_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS moving_avg_7d,

        -- Window Function: LAG to compare against the previous day
        LAG(energy_consumption_kwh) OVER (
            PARTITION BY meter_id 
            ORDER BY reading_date
        ) AS prev_day_usage

    FROM daily_usage
)

SELECT 
    *,
    -- Logic: Calculate the % variance from the moving average
    -- We use NULLIF to prevent "Division by Zero" errors (Senior best practice)
    ROUND(
        ((energy_consumption_kwh - moving_avg_7d) / NULLIF(moving_avg_7d, 0)) * 100, 
        2
    ) AS consumption_variance_pct
FROM usage_metrics