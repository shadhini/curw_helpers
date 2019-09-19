CREATE DEFINER=`routine_user`@`%` PROCEDURE `getCumulativeObservedRainfallGivenRegion`(
IN startTime DATETIME,
IN endTime DATETIME,
IN minlon DECIMAL(9,6),
IN maxlon DECIMAL(9,6),
IN minlat DECIMAL(9,6),
IN maxlat DECIMAL(9,6)
)
BEGIN
	SELECT  grids_selected.longitude, grids_selected.latitude, sum(curw_obs.data.value) as value
    FROM
	(SELECT longitude, latitude, observed.id, observed.station
    FROM
		(SELECT id, station 
			FROM curw_obs.run 
            where curw_obs.run.variable=10 and curw_obs.run.unit=9) AS observed
		LEFT JOIN curw_obs.station ON observed.station = curw_obs.station.id
		WHERE
			curw_obs.station.latitude BETWEEN minlat AND maxlat
			AND curw_obs.station.longitude BETWEEN minlon AND maxlon ) AS grids_selected
		LEFT JOIN
			curw_obs.data ON grids_selected.id = curw_obs.data.id
		WHERE
			curw_obs.data.time between startTime and endTime
		GROUP BY grids_selected.station;
END