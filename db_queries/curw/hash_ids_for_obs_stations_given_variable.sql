select selected.id, curw.station.name
FROM
(SELECT * FROM curw.run where station like '1_____' and type=1 and variable=1) as selected
left join curw.station
ON selected.station = curw.station.id;