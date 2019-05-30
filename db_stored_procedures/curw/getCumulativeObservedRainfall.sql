CREATE DEFINER=`root`@`%` PROCEDURE `getObservedRainfall`(
IN startTime DATETIME,
IN endTime DATETIME
)
BEGIN
	SELECT  grids_selected.longitude, grids_selected.latitude, sum(curw.data.value) as value
    FROM
	(SELECT longitude, latitude, observed.id
    FROM
		(SELECT id, station 
			FROM curw.run_view 
			WHERE type ="Observed" AND variable="Precipitation") AS observed
		LEFT JOIN curw.station ON observed.station = curw.station.name
		WHERE
			curw.station.latitude BETWEEN 6.6 AND 7.4
			AND curw.station.longitude BETWEEN 79.6 AND 81.0 ) AS grids_selected
		LEFT JOIN
			curw.data ON grids_selected.id = curw.data.id
		WHERE
			curw.data.time BETWEEN startTime AND endTime
		GROUP BY grids_selected.longitude, grids_selected.latitude;
END