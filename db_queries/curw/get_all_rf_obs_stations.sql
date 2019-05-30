SELECT
    run_selected.id, run_selected.name, run_selected.station, station.name, station.latitude, station.longitude
FROM
    (SELECT
        run.id, run.name, run.station
    FROM
        run
    WHERE
        variable = 1 AND unit = 1 AND type = 1) AS run_selected
        LEFT JOIN
    station ON run_selected.station = station.id
;