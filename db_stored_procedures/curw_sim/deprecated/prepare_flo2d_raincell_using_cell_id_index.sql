CREATE DEFINER=`routine_user`@`%` PROCEDURE `prepare_flo2d_raincell`(
IN model varchar(25),
IN method varchar(25),
IN time DATETIME
)
BEGIN
SET @@session.wait_timeout = 86400;
SELECT 
    curw_sim.grid_map_flo2d_raincell.cell_id,
    selected.value AS value
FROM
    (SELECT 
        selected_runs.grid_id, curw_sim.data.value AS value
    FROM
        (SELECT 
        curw_sim.run.id AS id, curw_sim.run.grid_id
    FROM
        curw_sim.run
    WHERE
        curw_sim.run.model = model
            AND curw_sim.run.method = method) AS selected_runs
    LEFT JOIN curw_sim.data ON selected_runs.id = curw_sim.data.id
    WHERE
        curw_sim.data.time = time) AS selected
        LEFT JOIN
    curw_sim.grid_map_flo2d_raincell ON selected.grid_id = curw_sim.grid_map_flo2d_raincell.grid_id
ORDER BY curw_sim.grid_map_flo2d_raincell.cell_id;
END