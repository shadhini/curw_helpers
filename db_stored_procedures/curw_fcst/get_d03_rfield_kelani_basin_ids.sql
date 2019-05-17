CREATE DEFINER=`root`@`%` PROCEDURE `get_d03_rfield_kelani_basin_ids`(
IN model VARCHAR(25),
IN version VARCHAR(25)
)
BEGIN
SET @sourceID = (SELECT curw_fcst.source.id FROM curw_fcst.source WHERE curw_fcst.source.model = model and curw_fcst.source.version = version);

SELECT 
    filtered_run.id,
    d03_stations.latitude,
    d03_stations.longitude
FROM
    (SELECT 
        curw_fcst.run.id, curw_fcst.run.station
    FROM
        curw_fcst.run
    WHERE
        curw_fcst.run.sim_tag = 'evening_18hrs'
            AND curw_fcst.run.variable = 1
            AND curw_fcst.run.unit = 1
            AND curw_fcst.run.source = @sourceID) AS filtered_run
        INNER JOIN
    (SELECT 
        curw_fcst.station.id, curw_fcst.station.latitude , curw_fcst.station.longitude
    FROM
        curw_fcst.station
    WHERE
        curw_fcst.station.latitude BETWEEN 6.6 AND 7.4
            AND curw_fcst.station.longitude BETWEEN 79.6 AND 81.0) AS d03_stations ON filtered_run.station = d03_stations.id;
END