CREATE DEFINER=`admin`@`%` PROCEDURE `get_ts_end`(
IN model varchar(25),
IN method varchar(25)
)
BEGIN
SET @randomID = (SELECT curw_sim.run.id FROM curw_sim.run WHERE curw_sim.run.model=model AND curw_sim.run.method=method LIMIT 1);
SELECT max(curw_sim.data.time) AS time 
	FROM curw_sim.data WHERE curw_sim.data.id=@randomID;
END