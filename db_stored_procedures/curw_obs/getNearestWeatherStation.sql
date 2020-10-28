CREATE DEFINER=`routine_user`@`%` PROCEDURE `getNearestWeatherStation`(
IN lat DECIMAL(9,6),
IN lng DECIMAL(9,6)
)
BEGIN
	SELECT ordered_stations.id AS id, ordered_stations.name AS name, ordered_stations.latitude AS latitude, ordered_stations.longitude AS longitude
    FROM 
    (SELECT
		id, name, latitude, longitude,
		(  
		   cos(radians(lat)) *
		   cos(radians(latitude)) *
		   cos(radians(longitude) -
		   radians(lng)) +
		   sin(radians(lat)) *
		   sin(radians(latitude))
		) AS distance
		FROM 
        (SELECT selected_runs.station_id, selected_runs.name, selected_runs.latitude, selected_runs.longitude
        FROM
        (SELECT curw_obs.station.id AS station_id, curw_obs.station.name, curw_obs.station.latitude, curw_obs.station.longitude
        FROM
        curw_obs.station
        WHERE curw_obs.station.id like "1_____" AND curw_obs.station.station_type = 'CUrW_WeatherStation') AS selected_stations
        LEFT JOIN
        curw_obs.run ON selected_stations.id = curw_obs.run.station
        WHERE 
        curw_obs.run.variable = 10 
        AND curw_obs.run.unit = 9
        AND curw_obs.run.end_date > SUBDATE(CURDATE(), INTERVAL 1 DAY)) AS selected_runs
		ORDER BY distance DESC LIMIT 3) AS ordered_stations;
END