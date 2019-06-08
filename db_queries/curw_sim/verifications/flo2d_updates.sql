SELECT id FROM curw_sim.run where grid_id like "flo2d$_250$_161%" escape '$'limit 1;
SELECT count(*) FROM curw_sim.run where obs_end > "2019-06-08" and model="flo2d_150";
SELECT * FROM curw_sim.data where id="1843787fc3b20e01a44f9edb680ea1cd1a3f1c4d51b6f1ea71aa6ecfd6df190e";