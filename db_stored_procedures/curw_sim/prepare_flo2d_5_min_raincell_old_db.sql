CREATE DEFINER=`routine_user`@`%` PROCEDURE `prepare_flo2d_5_min_raincell`(
IN model varchar(25),
IN method varchar(25),
IN time DATETIME
)
BEGIN
SET @@session.wait_timeout = 86400;
SELECT 
    CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(selected_runs.grid_id,
                        CONCAT(model, "_"),
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
        curw_sim.run.model = model
            AND curw_sim.run.method = method) AS selected_runs
        LEFT JOIN
    curw_sim.data ON selected_runs.id = curw_sim.data.id
WHERE
    curw_sim.data.time = time
ORDER BY cell_id;
END