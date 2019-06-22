CREATE DEFINER=`root`@`%` PROCEDURE `get_d01_rfield`(
IN model VARCHAR(25),
IN version VARCHAR(25),
IN time DATETIME
)
BEGIN
SET @sourceID = (SELECT curw_fcst.source.id FROM curw_fcst.source WHERE curw_fcst.source.model = model and curw_fcst.source.version = version);
SET @fgt = (SELECT curw_fcst.run.end_date FROM curw_fcst.run WHERE curw_fcst.run.source = @sourceID limit 1);

SELECT 
    curw_fcst.station_selected.latitude,
    curw_fcst.station_selected.longitude,
    curw_fcst.data.value
FROM
    (SELECT 
        curw_fcst.station.id,
            curw_fcst.station.latitude,
            curw_fcst.station.longitude
    FROM
        curw_fcst.station
    WHERE
        curw_fcst.station.id >= 1100000
            AND curw_fcst.station.id < 1200000
            AND curw_fcst.station.latitude IN (5.750061 , 5.993843, 6.237511, 6.481064, 6.724495, 6.967812, 7.211006, 7.454071, 7.696991, 7.939774, 8.182411, 8.424904, 8.667244, 8.909431, 9.151459, 9.393318, 9.635010, 9.876534)
            AND curw_fcst.station.longitude IN (79.548691 , 79.793747, 80.038811, 80.283875, 80.528938, 80.774002, 81.019066, 81.264130, 81.509193, 81.754257, 81.999313)) AS station_selected
        LEFT JOIN
    (SELECT 
        curw_fcst.run.id AS run_id,
            curw_fcst.run.station AS station_id
    FROM
        curw_fcst.run
    WHERE
        curw_fcst.run.sim_tag = 'evening_18hrs'
            AND curw_fcst.run.variable = 1
            AND curw_fcst.run.unit = 1
            AND curw_fcst.run.source = @sourceID) AS run_selcted ON curw_fcst.run_selcted.station_id = curw_fcst.station_selected.id
        LEFT JOIN
    curw_fcst.data ON curw_fcst.run_selcted.run_id = curw_fcst.data.id
        AND curw_fcst.data.fgt = @fgt
        AND curw_fcst.data.time = time;
END