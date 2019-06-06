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

-- gives specified stations with station ids
-- for all of these source=6(Weather Station)
SELECT * FROM curw.run where name in ('A&T Labs', 'Leecom', 'CUrW IoT') and station in (100063,100056, 100041, 100038, 100039, 100042, 100043, 100037, 100040, 100064, 100046, 100057) and variable=1 and unit=1 and type=1;

-- gives all curw rainfall observation stations
