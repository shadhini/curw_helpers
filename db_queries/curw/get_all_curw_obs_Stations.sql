select selected_runs.id, selected_runs.name,
curw.station.name, curw.station.latitude, curw.station.longitude, curw.station.description,
curw.variable.variable, curw.unit.unit, curw.unit.type from
((select * from curw.run where name in ('A&T Labs', 'Leecom', 'CUrW IoT') ) as selected_runs
 join
curw.station on curw.station.id = selected_runs.station
join
curw.variable on curw.variable.id = selected_runs.variable
join
curw.unit on curw.unit.id = selected_runs.unit)