CREATE DEFINER=`routine_user`@`%` PROCEDURE `getValuesForGivenLead`(
IN tms_id VARCHAR(64),
IN t1 DATETIME,
IN t2 DATETIME,
IN lead_time TIME
)
BEGIN

SET @lead_time1 = (SELECT SUBTIME(lead_time, "00:15:00"));

SET @lead_time2 = (SELECT ADDTIME(lead_time, "00:15:00"));
   
SELECT 
    curw_fcst.data.time AS time,
    curw_fcst.data.value AS value
FROM
    curw_fcst.data
WHERE
    curw_fcst.data.id = tms_id
        AND curw_fcst.data.time BETWEEN t1 AND t2
		AND TIMEDIFF(curw_fcst.data.time, curw_fcst.data.fgt) BETWEEN @lead_time1 AND @lead_time2
ORDER BY time;

END