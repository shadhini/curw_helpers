CREATE DEFINER=`routine_user`@`%` PROCEDURE `getLatestFGTs`(
IN id VARCHAR(64),
IN time DATETIME
)
BEGIN
	SELECT
	temp.fgt,
    (time - temp.fgt) as gap
	FROM 
    (select distinct curw_fcst.data.fgt as fgt from curw_fcst.data where curw_fcst.data.id=id and curw_fcst.data.fgt < time) as temp
    order by gap limit 10;
END