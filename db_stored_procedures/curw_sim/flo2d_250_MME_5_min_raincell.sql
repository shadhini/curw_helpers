CREATE DEFINER=`root`@`%` PROCEDURE `flo2d_250_MME_5_min_raincell`(
IN time DATETIME
)
BEGIN
SET @@session.wait_timeout = 86400;
SELECT 
    CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(selected_runs.grid_id,
                        CONCAT('flo2d_250_'),
                        - 1),
                '_',
                1)
        AS UNSIGNED) AS cell_id,
    curw_sim.data.value AS value
FROM
    (SELECT 
        curw_sim.run.id AS id, curw_sim.run.grid_id
    FROM
        curw_sim.run
    WHERE
        curw_sim.run.model = 'flo2d_250'
            AND curw_sim.run.method = 'MME') AS selected_runs
        LEFT JOIN
    curw_sim.data ON selected_runs.id = curw_sim.data.id
WHERE
    curw_sim.data.time = time
ORDER BY cell_id;
END