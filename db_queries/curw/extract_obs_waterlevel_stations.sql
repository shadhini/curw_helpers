SELECT * FROM curw.run where name in ('Observed Water Levels', 'Leecom', 'A&T Labs') and type=1 and variable=3 and unit=3 and end_date> "2019-06-01"

SELECT
    ids.id AS hash_id,
    ids.name AS run_name,
    station.id AS station_id,
    station.name AS station_name,
    station.latitude AS latitude,
    station.longitude AS longitude
FROM
    (SELECT
        *
    FROM
        curw.run
    WHERE
        name IN ('Observed Water Levels' , 'Leecom', 'A&T Labs')
            AND type = 1
            AND variable = 3
            AND unit = 3
            AND end_date > '2019-06-01') AS ids
        LEFT JOIN
    curw.station ON station.id = ids.station;
