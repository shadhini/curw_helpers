SELECT
    curw_fcst.station.id,
    curw_fcst.station.latitude,
    curw_fcst.station.longitude
FROM
    curw_fcst.station
WHERE
    curw_fcst.station.latitude BETWEEN 6.6 AND 7.4
        AND curw_fcst.station.longitude BETWEEN 79.6 AND 81.0