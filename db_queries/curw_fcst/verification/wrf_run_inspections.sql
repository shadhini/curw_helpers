SELECT * FROM curw_fcst.run where curw_fcst.run.scheduled_date like "2019-03-24%" and curw_fcst.run.source = 4;

SELECT * FROM curw_fcst.run where curw_fcst.run.scheduled_date like "2019-03-27%" and curw_fcst.run.source =2 limit 10;

select count(distinct id)  from data where fgt like "2019-05-03%";

select id from run where end_date="2019-05-04 23:45:00";
