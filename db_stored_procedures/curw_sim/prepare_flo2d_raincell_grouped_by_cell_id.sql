CREATE DEFINER=`root`@`%` PROCEDURE `prepare_flo2d_raincell`(
IN model varchar(25),
IN method varchar(25),
IN start_time DATETIME,
IN end_time DATETIME
)
BEGIN
	SELECT cells.cell_id as cell, sum(curw_sim.data.value) as value
    FROM
	(SELECT curw_sim.run.id as id, CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(curw_sim.run.grid_id, CONCAT(model,"_"), -1),"_", 1) as UNSIGNED) as cell_id
		FROM curw_sim.run 
        WHERE curw_sim.run.model=model AND curw_sim.run.method=method ORDER BY cell_id) as cells
	LEFT JOIN
    curw_sim.data  
	ON cells.id = curw_sim.data.id 
    WHERE curw_sim.data.time between start_time and end_time
    GROUP BY cells.id ORDER BY cells.cell_id;
END