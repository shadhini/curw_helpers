SELECT wl.id, wl.name, wl.latitude, wl.longitude, curw_obs.run.id FROM
(SELECT * FROM curw_obs.station where curw_obs.station.station_type="CUrW_WaterLevelGauge") as wl
LEFT JOIN curw_obs.run ON wl.id= curw_obs.run.station;