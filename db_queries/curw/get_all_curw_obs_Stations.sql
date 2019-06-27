select * from
(select * from curw.run where name in ('A&T Labs', 'Leecom', 'CUrW IoT') ) as selected_runs
left join
curw.station on curw.station.id = selected_runs.station;

select * from
(select * from curw.run_view where name in ('A&T Labs', 'Leecom', 'CUrW IoT') ) as selected_runs
left join
curw.station on curw.station.name = selected_runs.station where stationId like "curw_%" ;
-- from this only latest stations should be selected