
SELECT
    machine_id,
    SUM(production_quantity) AS total_production,
    SUM(defect_quantity) AS total_defects,
    ROUND(
        100.0 * SUM(defect_quantity)
        / NULLIF(SUM(production_quantity), 0),
        2
    ) AS defect_rate_pct,
    SUM(downtime_minutes) AS total_downtime
FROM production
GROUP BY machine_id
ORDER BY total_production DESC;
