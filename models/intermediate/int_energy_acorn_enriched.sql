{{ config(materialized='view') }}

WITH metrics AS (
    SELECT * FROM {{ ref('int_energy_usage_daily_spikes') }}
),

behavior AS (
    SELECT * FROM {{ ref('int_household_behavior_ranking') }}
),

metadata AS (
    SELECT * FROM {{ ref('stg_households') }}
),

final_join AS (
    SELECT
        m.reading_unique_id,
        m.meter_id,
        m.reading_date,
        m.energy_consumption_kwh,
        m.moving_avg_7d,
        m.consumption_variance_pct,
        b.consumption_decile,
        b.peak_consumption,
        h.acorn_group,
        h.acorn_category,
        -- Business Logic: Flagging an anomaly (a spike 50% above moving average)
        CASE 
            WHEN m.consumption_variance_pct > 50 THEN 'High Spike'
            WHEN m.consumption_variance_pct < -50 THEN 'Low Drop'
            ELSE 'Normal'
        END AS usage_anomaly_flag
    FROM metrics m
    LEFT JOIN behavior b ON m.meter_id = b.meter_id
    LEFT JOIN metadata h ON m.meter_id = h.meter_id
)

SELECT * FROM final_join