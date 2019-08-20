CREATE DEFINER=`routine_user`@`%` PROCEDURE `getRainfallLatest5min`(
IN t DATETIME
)
BEGIN
SELECT selected_stations.latitude, selected_stations.longitude,  curw_obs.data.value
FROM
	(SELECT precipitation.id, curw_obs.station.latitude, curw_obs.station.longitude
    FROM
		(SELECT curw_obs.run.id, curw_obs.run.station 
			FROM curw_obs.run 
			WHERE curw_obs.run.variable=10 
			AND curw_obs.run.unit=9) AS precipitation
		LEFT JOIN 
			curw_obs.station ON curw_obs.station.id = precipitation.station
			WHERE curw_obs.station.station_type = 'CUrW_WeatherStation') AS selected_stations
		LEFT JOIN
			curw_obs.data ON selected_stations.id = curw_obs.data.id
			WHERE curw_obs.data.time=t;
END