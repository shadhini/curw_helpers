CREATE DEFINER=`routine_user`@`%` PROCEDURE `getLatest24hrWaterLevel`(
IN station_name VARCHAR(45)
)
BEGIN
SET @stationID = (SELECT curw.station.id FROM curw.station WHERE curw.station.stationId = station_name);
SET @tmsID = (SELECT curw.run.id FROM curw.run 
			  WHERE NAME IN ('A&T Labs', 'Leecom', 'CUrW IoT') 
			  AND curw.run.variable=3 AND curw.run.unit=3 AND curw.run.type=1 AND 
                curw.run.station = @stationID);
                
SELECT 
    curw.data.time AS time, curw.data.value AS value
FROM
    curw.data
WHERE
    curw.data.id = @tmsID
        AND curw.data.time >= SUBDATE(CURRENT_TIMESTAMP(),
        INTERVAL 24 HOUR)
        AND curw.data.time LIKE '%:00:00';

END