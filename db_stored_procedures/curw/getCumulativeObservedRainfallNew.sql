CREATE DEFINER=`routine_user`@`%` PROCEDURE `getCumulativeObservedRainfall`(
IN startTime DATETIME,
IN endTime DATETIME
)
BEGIN
	SELECT  grids_selected.longitude, grids_selected.latitude, sum(curw.data.value) as value
    FROM
	(SELECT longitude, latitude, observed.id, observed.station
    FROM
		(SELECT id, station 
			FROM curw.run 
            where name in ('A&T Labs', 'Leecom', 'CUrW IoT') and variable=1 and unit=1 and type=1) AS observed
		LEFT JOIN curw.station ON observed.station = curw.station.id
		WHERE
			curw.station.latitude BETWEEN 6.6 AND 7.4
			AND curw.station.longitude BETWEEN 79.6 AND 81.0 ) AS grids_selected
		LEFT JOIN
			curw.data ON grids_selected.id = curw.data.id
		WHERE
			curw.data.time between startTime and endTime
		GROUP BY grids_selected.station;
END