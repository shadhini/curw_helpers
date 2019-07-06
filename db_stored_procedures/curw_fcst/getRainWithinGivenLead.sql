CREATE DEFINER=`routine_user`@`%` PROCEDURE `getRainWithinGivenLead`(
IN model VARCHAR(25),
IN version VARCHAR(25),
IN station_id INT(11),
IN sim_tag VARCHAR(100),
IN start_time DATETIME,
IN lead_time TIME)
BEGIN
	SET @sourceID = (SELECT curw_fcst.source.id FROM curw_fcst.source WHERE curw_fcst.source.model = model and curw_fcst.source.version = version);
	SET @tmsID = (SELECT curw_fcst.run.id FROM curw_fcst.run WHERE curw_fcst.run.source=@sourceID  AND curw_fcst.run.station=station_id 
		AND curw_fcst.run.sim_tag=sim_tag AND curw_fcst.run.variable=1 AND curw_fcst.run.unit=1);

	SET @final_fgt = (SELECT final_fgt.fgt FROM (SELECT
	distinct_fgt.fgt,
    abs(distinct_fgt.fgt-start_time) AS gap
	FROM 
    (SELECT DISTINCT fgt FROM curw_fcst.data WHERE curw_fcst.data.id=@tmsID) AS distinct_fgt
    ORDER BY gap LIMIT 1) AS final_fgt);
        
	SELECT 
    *
	FROM
		data
	WHERE
		curw_fcst.data.id = @tmsID
			AND curw_fcst.data.fgt = @final_fgt
			AND curw_fcst.data.time BETWEEN @final_fgt AND ADDTIME(@final_fgt, lead_time);
END