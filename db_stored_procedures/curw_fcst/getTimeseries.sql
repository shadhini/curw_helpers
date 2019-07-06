CREATE DEFINER=`routine_user`@`%` PROCEDURE `getLatestTimeseries`(
IN id VARCHAR(64),
IN time DATETIME
)
BEGIN
	select * from data where curw_fcst.data.id=id and 
    curw_fcst.data.fgt = (select fgt from (SELECT
	fgt,
    abs(fgt-time) as gap
	FROM 
    (select distinct fgt from data) as distinct_fgt
    order by gap limit 1) as final_fgt);
END