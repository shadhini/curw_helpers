CREATE DEFINER=`root`@`%` PROCEDURE `get_d03_rfield`(
IN model VARCHAR(25),
IN version VARCHAR(25),
IN start_time DATETIME,
IN end_time DATETIME
)
BEGIN
SET @sourceID = (SELECT curw_fcst.source.id FROM curw_fcst.source WHERE curw_fcst.source.model = model and curw_fcst.source.version = version);
SET @fgt = (SELECT curw_fcst.run.end_date FROM curw_fcst.run WHERE curw_fcst.run.source = @sourceID limit 1);

SELECT 
    curw_fcst.station_selected.latitude,
    curw_fcst.station_selected.longitude,
    sum(curw_fcst.data.value)
FROM
    (SELECT 
        curw_fcst.station.id,
            curw_fcst.station.latitude,
            curw_fcst.station.longitude
    FROM
        curw_fcst.station
    WHERE
        curw_fcst.station.id >= 1100000
            AND curw_fcst.station.id < 1200000) AS station_selected
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
        AND curw_fcst.data.time BETWEEN start_time AND end_time
GROUP BY curw_fcst.station_selected.latitude , curw_fcst.station_selected.longitude;
END