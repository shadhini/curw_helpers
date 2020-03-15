SELECT
selected.name,
selected.station_type,
selected.latitude,
selected.longitude,
curw_obs.variable.variable
 FROM
(SELECT
curw_obs.station.name,
curw_obs.station.station_type,
curw_obs.station.latitude,
curw_obs.station.longitude,
curw_obs.run.variable
    FROM
    curw_obs.run
	LEFT JOIN
		curw_obs.station ON curw_obs.station.id = curw_obs.run.station) as selected
        LEFT JOIN
        curw_obs.variable ON curw_obs.variable.id = selected.variable

        ORDER BY selected.name