CREATE DEFINER=`root`@`%` PROCEDURE `getActiveRainfallObsStations`()
BEGIN
	SELECT curw.station.id as station_id, curw.station.name as name, 
		curw.station.latitude as latitude,  curw.station.longitude as longitude
    FROM
		((SELECT id, name, station FROM curw.run 
			WHERE NAME IN ('A&T Labs', 'Leecom', 'CUrW IoT') 
				AND variable=1 AND unit=1 AND TYPE=1 AND 
				end_date > SUBDATE(CURDATE(), INTERVAL 5 DAY)) AS selected_runs
		LEFT JOIN
		curw.station ON selected_runs.station = curw.station.id);
	
END