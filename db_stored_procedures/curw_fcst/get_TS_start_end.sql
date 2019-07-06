CREATE DEFINER=`routine_user`@`%` PROCEDURE `get_TS_start_end`(
IN model VARCHAR(25),
IN version VARCHAR(25)
)
BEGIN
SET @sourceID = (SELECT curw_fcst.source.id FROM curw_fcst.source WHERE curw_fcst.source.model = model and curw_fcst.source.version = version);
SET @fgt = (SELECT curw_fcst.run.end_date FROM curw_fcst.run WHERE curw_fcst.run.source = @sourceID limit 1);
SET @random_id = (SELECT curw_fcst.run.id FROM curw_fcst.run WHERE curw_fcst.run.source = @sourceID limit 1);

SELECT 
    MIN(curw_fcst.data.time) AS start,
    MAX(curw_fcst.data.time) AS end
FROM
    curw_fcst.data
WHERE
    curw_fcst.data.id = @random_id
        AND curw_fcst.data.fgt = @fgt;
END