select time, value from data
where id="5c5210be1577a01a138fd646dff963fe4974c4dab1accd175cc8ff73cf11bae8" and time between "2019-06-04 13:00:00" and "2019-06-15 00:00:00"
and convert(MOD((HOUR(TIMEDIFF(time, "2019-05-27 00:00:00"))*60+MINUTE(TIMEDIFF(time, "2019-05-27 00:00:00"))),15),char)  like "0";