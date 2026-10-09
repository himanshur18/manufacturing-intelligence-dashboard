
WITH monthly_production AS (
    SELECT
        DATE_TRUNC('month', production_date)::DATE
            AS production_month,
        SUM(production_quantity) AS total_production
    FROM production
    GROUP BY DATE_TRUNC('month', production_date)::DATE
),
production_trends AS (
    SELECT
        production_month,
        total_production,
        LAG(total_production) OVER (
            ORDER BY production_month
        ) AS previous_month_production
    FROM monthly_production
)
SELECT
    production_month,
    total_production,
    previous_month_production,
    total_production - previous_month_production
        AS production_change,
    ROUND(
        100.0 * (total_production - previous_month_production)
        / NULLIF(previous_month_production, 0),
        2
    ) AS growth_percentage
FROM production_trends
ORDER BY production_month;
