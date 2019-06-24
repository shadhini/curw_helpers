SELECT * FROM curw.run_view where type="Observed" and name in ('A&T Labs', 'Leecom', 'CUrW IoT');

SELECT * FROM
(SELECT distinct variable FROM curw.run_view where type="Observed" and name in ('A&T Labs', 'Leecom', 'CUrW IoT')) as selected
LEFT JOIN curw.variable on selected.variable = curw.variable.variable; -- where curw.station.stationId like "curw_%";