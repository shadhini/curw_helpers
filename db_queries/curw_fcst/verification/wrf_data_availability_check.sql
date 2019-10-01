use curw_fcst;
select * from run where source=12 limit 10;
-- 12 - WRF C,
-- 13 - WRF E,
-- 15 - WRF A,
-- 16 - WRF SE
select distinct fgt from data where id="" and fgt >="2019-08-30";