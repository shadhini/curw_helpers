CREATE DEFINER=`routine_user`@`%` PROCEDURE `getNearbyRainWithLead`(
IN lat DECIMAL(9,6),
IN lng DECIMAL(9,6),
IN model VARCHAR(25),
IN version VARCHAR(25),
IN sim_tag VARCHAR(100),
IN t1 DATETIME,
IN t2 DATETIME
-- IN lead_time TIME
)
BEGIN
	
	SET @stationID = (SELECT ordered_stations.id
    FROM 
    (SELECT
		id, name, latitude, longitude,
		(  
		   cos(radians(lat)) *
		   cos(radians(latitude)) *
		   cos(radians(longitude) -
		   radians(lng)) +
		   sin(radians(lat)) *
		   sin(radians(latitude))
		) AS distance
		FROM curw_fcst.station
        WHERE curw_fcst.station.id like "11_____"
		ORDER BY distance DESC LIMIT 1) AS ordered_stations);
        
	SET @sourceID = (SELECT curw_fcst.source.id FROM curw_fcst.source WHERE curw_fcst.source.model = model and curw_fcst.source.version = version);
	SET @tmsID = (SELECT curw_fcst.run.id FROM curw_fcst.run WHERE curw_fcst.run.source=@sourceID  AND curw_fcst.run.station=@stationID 
		AND curw_fcst.run.sim_tag=sim_tag AND curw_fcst.run.variable=1 AND curw_fcst.run.unit=1);
        
	SELECT 
    curw_fcst.data.time AS time,
    curw_fcst.data.fgt AS fgt,
    SEC_TO_TIME(FLOOR(TIME_TO_SEC(TIMEDIFF(curw_fcst.data.time, curw_fcst.data.fgt)) / (60 * 30)) * 1800) AS lead,
    curw_fcst.data.value AS value
FROM
    curw_fcst.data
WHERE
    curw_fcst.data.id = @tmsID
        AND curw_fcst.data.time BETWEEN t1 AND t2
ORDER BY time , lead;

END