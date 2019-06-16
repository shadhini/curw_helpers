CREATE PROCEDURE `get_raincell` (
IN model varchar(25),
IN method varchar(25),
IN start_time DATETIME,
IN end_time DATETIME
)
BEGIN
	SELECT sum(curw_sim.data.value) as value, curw_sim.data.id
		FROM curw_sim.data
		WHERE curw_sim.data.id in (SELECT curw_sim.run.id FROM curw_sim.run 
			WHERE curw_sim.run.model=model AND curw_sim.run.method=method) 
		AND curw_sim.data.time between start_time and end_time group by curw_sim.data.id;
END
