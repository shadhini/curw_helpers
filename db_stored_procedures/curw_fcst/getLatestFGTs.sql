CREATE DEFINER=`routine_user`@`%` PROCEDURE `getLatestFGTs`(
IN id VARCHAR(64),
IN time DATETIME
)
BEGIN
	SELECT
	fgt,
    abs(fgt- time) as gap
	FROM 
    (select distinct fgt from data where fgt < time and id=id) as temp
    order by gap limit 10;
END