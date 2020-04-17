CREATE DEFINER=`routine_user`@`%` PROCEDURE `getActiveRfStationsAtGivenTime`(
IN start_time DATETIME,
IN end_time DATETIME
)
BEGIN
SELECT 
selected_stations.id as hash_id,
    selected_stations.station_id as station_id,
    selected_stations.name as station_name,
    selected_stations.latitude as latitude,
    selected_stations.longitude as longitude
FROM
	(SELECT precipitation.id, curw_obs.station.latitude, curw_obs.station.longitude, curw_obs.station.name, curw_obs.station.id as station_id
    FROM
		(SELECT curw_obs.run.id, curw_obs.run.station 
			FROM curw_obs.run 
			WHERE curw_obs.run.variable=10 
			AND curw_obs.run.unit=9) AS precipitation
		LEFT JOIN 
			curw_obs.station ON curw_obs.station.id = precipitation.station
			WHERE curw_obs.station.station_type = 'CUrW_WeatherStation') AS selected_stations
		LEFT JOIN
			(SELECT distinct id FROM curw_obs.data
            WHERE curw_obs.data.time >= start_time
            AND curw_obs.data.time <= end_time) AS present_data
			ON selected_stations.id = present_data.id;
END