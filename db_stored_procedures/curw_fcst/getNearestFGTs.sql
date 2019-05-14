CREATE DEFINER=`root`@`%` PROCEDURE `getNearestFGTs`(
IN id VARCHAR(64),
IN time DATETIME
)
BEGIN
	SELECT
	fgt,
    abs(fgt-time) as gap
	FROM 
    (select distinct fgt from data where id=id) as temp
    order by gap limit 10;
END