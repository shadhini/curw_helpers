select max(time) as time, sum(value) as value from data
where `id`=%s and `time` between %s and %s group by
floor((HOUR(TIMEDIFF(`time`, %s))*60+MINUTE(TIMEDIFF(time, %s))-1)/15);

select max(time) as time, sum(value) as value from data
where id="0af5ecec986be44699e267415799b8b349eeb4e4925881a9fad5cf47fa8f3019" and time > "2019-05-27"
group by floor((HOUR(TIMEDIFF(time, "2019-05-27 00:00:00"))*60+MINUTE(TIMEDIFF(time, "2019-05-27 00:00:00"))-1)/15);
