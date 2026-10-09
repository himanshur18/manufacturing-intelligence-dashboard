
WITH machine_stats AS (
    SELECT
        machine_id,
        SUM(production_quantity) AS total_production,
        SUM(defect_quantity) AS total_defects,
        SUM(downtime_minutes) AS total_downtime
    FROM production
    GROUP BY machine_id
)
SELECT
    machine_id,
    total_production,
    total_defects,
    ROUND(
        100.0 * total_defects
        / NULLIF(total_production, 0),
        2
    ) AS defect_rate_pct,
    total_downtime
FROM machine_stats
WHERE 100.0 * total_defects
      / NULLIF(total_production, 0) > 4
ORDER BY defect_rate_pct DESC;
