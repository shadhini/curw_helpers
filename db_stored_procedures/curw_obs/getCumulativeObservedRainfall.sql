CREATE DEFINER=`routine_user`@`%` PROCEDURE `getCumulativeObservedRainfall`(
IN startTime DATETIME,
IN endTime DATETIME
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
			curw_obs.station.latitude BETWEEN 6.6 AND 7.4
			AND curw_obs.station.longitude BETWEEN 79.6 AND 81.0 ) AS grids_selected
		LEFT JOIN
			curw_obs.data ON grids_selected.id = curw_obs.data.id
		WHERE
			curw_obs.data.time between startTime and endTime
		GROUP BY grids_selected.station;
END