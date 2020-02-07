CREATE DEFINER=`routine_user`@`%` PROCEDURE `getWL15min`(
IN station_id INT(11),
IN startTime DATETIME,
IN endTime DATETIME
)
BEGIN
SET @tmsID = (SELECT curw_obs.run.id FROM curw_obs.run 
			  WHERE curw_obs.run.variable=17 AND curw_obs.run.unit=15 AND 
                curw_obs.run.station = station_id);
                
SELECT 
    curw_obs.data.time AS time, curw_obs.data.value AS value
FROM
    curw_obs.data
WHERE
    curw_obs.data.id = @tmsID
        AND curw_obs.data.time BETWEEN startTime AND endTime
        AND CONVERT( MOD(FLOOR(TO_SECONDS(curw_obs.data.time) / 60),
        15) , CHAR) LIKE '0';
END