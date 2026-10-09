
SELECT
    machine_id,
    SUM(production_quantity) AS total_production,
    RANK() OVER (
        ORDER BY SUM(production_quantity) DESC
    ) AS production_rank
FROM production
GROUP BY machine_id
ORDER BY production_rank;
