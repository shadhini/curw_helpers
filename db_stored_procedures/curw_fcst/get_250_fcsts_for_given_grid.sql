CREATE DEFINER=`routine_user`@`%` PROCEDURE `get_250_fcsts_for_given_grid`(
IN grid VARCHAR(25),
IN variable_id INT(11),
IN sim_tag VARCHAR(100),
IN fgt DATETIME
)
BEGIN
	SET @stationID = (SELECT curw_fcst.station.id FROM curw_fcst.station where id like '12_____'
						AND SUBSTRING_INDEX(SUBSTRING_INDEX(curw_fcst.station.name, '_', 1), '_', -1) = grid);
	SET @tmsID = (SELECT curw_fcst.run.id FROM curw_fcst.run
					WHERE curw_fcst.run.sim_tag = sim_tag AND curw_fcst.run.source = 9 
                    AND curw_fcst.run.variable = variable_id AND curw_fcst.run.station = @stationID);
	
SELECT 
    curw_fcst.data.time, curw_fcst.data.value
FROM
    curw_fcst.data
WHERE
    curw_fcst.data.id = @tmsID
        AND curw_fcst.data.fgt = fgt;
END	