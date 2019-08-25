CREATE DEFINER=`admin`@`%` PROCEDURE `getActiveRainfallObsStations`()
BEGIN
SELECT 
	selected_runs.id as hash_id,
    curw_obs.station.id as station_id,
    curw_obs.station.name as station_name,
    curw_obs.station.latitude as latitude,
    curw_obs.station.longitude as longitude
FROM
	(SELECT *
    FROM 
    curw_obs.run 
    WHERE
		curw_obs.run.variable = 10 
        AND curw_obs.run.unit = 9
        AND end_date > SUBDATE(CURDATE(), INTERVAL 1 DAY)) AS selected_runs
	LEFT JOIN
		curw_obs.station ON curw_obs.station.id = selected_runs.station
	WHERE
		curw_obs.station.station_type = 'CUrW_WeatherStation';
        
END