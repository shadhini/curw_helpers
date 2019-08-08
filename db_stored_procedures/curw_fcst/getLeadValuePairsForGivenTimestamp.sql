CREATE DEFINER=`routine_user`@`%` PROCEDURE `getLeadValuePairsForGivenTimestamp`(
IN tms_id VARCHAR(64),
IN timestamp TIME
)
BEGIN
   
SELECT 
    TIMEDIFF(curw_fcst.data.time, curw_fcst.data.fgt) AS lead_time,
    curw_fcst.data.value AS value
FROM
    curw_fcst.data
WHERE
    curw_fcst.data.id = tms_id
        AND curw_fcst.data.time = timestamp
ORDER BY lead_time DESC;

END
