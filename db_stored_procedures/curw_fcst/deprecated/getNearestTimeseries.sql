CREATE DEFINER=`routine_user`@`%` PROCEDURE `getNearestTimeseries`(
IN id VARCHAR(64),
IN t DATETIME
)
BEGIN
SET @final_fgt = (select selected.fgt from (SELECT
	temp.fgt as fgt,
    (t - temp.fgt) as gap
	FROM 
    (select distinct curw_fcst.data.fgt as fgt from curw_fcst.data where curw_fcst.data.id=id and curw_fcst.data.fgt < t) as temp
    order by gap limit 1) as selected);
    
SELECT 
    curw_fcst.data.time AS time, curw_fcst.data.value AS value
FROM
    curw_fcst.data
WHERE
    curw_fcst.data.id = id
        AND curw_fcst.data.fgt = @final_fgt;
END