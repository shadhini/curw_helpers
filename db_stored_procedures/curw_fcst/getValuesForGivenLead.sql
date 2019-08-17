CREATE DEFINER=`routine_user`@`%` PROCEDURE `getValuesForGivenLead`(
IN tms_id VARCHAR(64),
IN t1 DATETIME,
IN t2 DATETIME,
IN lead_time TIME
)
BEGIN
   
SELECT 
    curw_fcst.data.time AS time,
    curw_fcst.data.value AS value
FROM
    curw_fcst.data
WHERE
    curw_fcst.data.id = tms_id
        AND curw_fcst.data.time BETWEEN t1 AND t2
		AND SEC_TO_TIME(floor(TIME_TO_SEC(TIMEDIFF(curw_fcst.data.time, curw_fcst.data.fgt))/(60*30))*1800) = lead_time
ORDER BY time;

END