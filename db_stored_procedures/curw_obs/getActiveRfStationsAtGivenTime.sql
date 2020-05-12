CREATE DEFINER=`routine_user`@`%` PROCEDURE `getActiveRfStationsAtGivenTime`(
IN start_time DATETIME,
IN end_time DATETIME
)
BEGIN
SELECT 
	unique_runs.id as hash_id,
    unique_runs.station as station_id,
    curw_obs.station.name as station_name,
    curw_obs.station.latitude as latitude,
    curw_obs.station.longitude as longitude
FROM
	(SELECT distinct rainfall.id, rainfall.station  FROM 
		(SELECT curw_obs.run.id, curw_obs.run.station FROM curw_obs.run WHERE curw_obs.run.variable=10 AND curw_obs.run.unit=9) as rainfall
		LEFT JOIN
			curw_obs.data ON rainfall.id = curw_obs.data.id
			WHERE curw_obs.data.time >= start_time
			AND curw_obs.data.time <= end_time) as unique_runs
	LEFT JOIN
	curw_obs.station ON curw_obs.station.id = unique_runs.station;
END