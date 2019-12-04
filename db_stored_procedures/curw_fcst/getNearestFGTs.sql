CREATE DEFINER=`routine_user`@`%` PROCEDURE `getNearestFGTs`(
IN id VARCHAR(64),
IN time DATETIME
)
BEGIN
	SELECT
	temp.fgt,
    abs(time - temp.fgt) as gap
	FROM 
    (select distinct curw_fcst.data.fgt as fgt from curw_fcst.data where curw_fcst.data.id=id) as temp
    order by gap limit 10;
END