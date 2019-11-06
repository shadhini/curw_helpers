CREATE DEFINER=`routine_user`@`%` PROCEDURE `getFcstWLforGivenStation`(
IN model VARCHAR(25),
IN version VARCHAR(25),
IN station_id INT(11),
IN sim_tag VARCHAR(100),
IN t1 DATETIME,
IN t2 DATETIME
)
BEGIN
	SET @sourceID = (SELECT curw_fcst.source.id FROM curw_fcst.source WHERE curw_fcst.source.model = model and curw_fcst.source.version = version);
	SET @tmsID = (SELECT curw_fcst.run.id FROM curw_fcst.run WHERE curw_fcst.run.source=@sourceID  AND curw_fcst.run.station=station_id 
		AND curw_fcst.run.sim_tag=sim_tag AND curw_fcst.run.variable=2 AND curw_fcst.run.unit=2);
        
SELECT 
    curw_fcst.data.time AS time,
    curw_fcst.data.fgt AS fgt,
    -- TIMEDIFF(curw_fcst.data.time, curw_fcst.data.fgt) AS lead,
    curw_fcst.data.value AS value
FROM
    curw_fcst.data
WHERE
    curw_fcst.data.id = @tmsID
        AND curw_fcst.data.time BETWEEN t1 AND t2
ORDER BY time; -- , lead;
END