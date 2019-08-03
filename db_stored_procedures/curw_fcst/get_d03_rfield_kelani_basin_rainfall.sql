CREATE DEFINER=`routine_user`@`%` PROCEDURE `get_d03_rfield_kelani_basin_rainfall`(
IN model VARCHAR(25),
IN version VARCHAR(25),
IN sim_tag VARCHAR(100),
IN time DATETIME
)
BEGIN
SET @sourceID = (SELECT curw_fcst.source.id FROM curw_fcst.source WHERE curw_fcst.source.model = model and curw_fcst.source.version = version);
SET @fgt = (SELECT curw_fcst.run.end_date FROM curw_fcst.run WHERE curw_fcst.run.source = @sourceID limit 1);

SELECT 
    curw_fcst.station_selected.longitude,
    curw_fcst.station_selected.latitude,
    curw_fcst.data.value
FROM
    (SELECT 
        curw_fcst.station.id,
            curw_fcst.station.latitude,
            curw_fcst.station.longitude
    FROM
        curw_fcst.station
    WHERE
        curw_fcst.station.id BETWEEN 1100000 AND 1199999
            AND curw_fcst.station.latitude BETWEEN 6.6 AND 7.4
            AND curw_fcst.station.longitude BETWEEN 79.6 AND 81.0) AS station_selected
        LEFT JOIN
    (SELECT 
        curw_fcst.run.id AS run_id,
            curw_fcst.run.station AS station_id
    FROM
        curw_fcst.run
    WHERE
        curw_fcst.run.sim_tag = sim_tag
            AND curw_fcst.run.variable = 1
            AND curw_fcst.run.unit = 1
            AND curw_fcst.run.source = @sourceID) AS run_selcted ON curw_fcst.run_selcted.station_id = curw_fcst.station_selected.id
        LEFT JOIN
    curw_fcst.data ON curw_fcst.run_selcted.run_id = curw_fcst.data.id
        AND curw_fcst.data.fgt = @fgt
        AND curw_fcst.data.time = time
ORDER BY curw_fcst.station_selected.longitude , curw_fcst.station_selected.latitude;
END