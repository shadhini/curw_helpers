CREATE DEFINER=`admin`@`%` TRIGGER `curw_fcst`.`run_AFTER_UPDATE_wl_alert` AFTER UPDATE ON `run` FOR EACH ROW
BEGIN
	DECLARE hash_id varchar(64);
	DECLARE model varchar(25);
	DECLARE model_version varchar(25);
	DECLARE sim_tag varchar(100);
	DECLARE last_run datetime;
	DECLARE station_name varchar(45);
    
    DECLARE finished INTEGER DEFAULT 0;
    	DECLARE time DATETIME;
    	DECLARE value DECIMAL(8,3);

	-- declare cursor for employee email
	DEClARE curWL 
		CURSOR FOR 
			SELECT time, value FROM curw_fcst.data 
				WHERE curw_fcst.data.id = NEW.id 
					AND curw_fcst.data.fgt = last_run;

	-- declare NOT FOUND handler
	DECLARE CONTINUE HANDLER 
	FOR NOT FOUND SET finished = 1;
    
    IF NEW.variable = 2 THEN 

		SELECT 
		curw_fcst.run_view.hash_id,
		curw_fcst.run_view.model,
		curw_fcst.run_view.model_version,
		curw_fcst.run_view.sim_tag,
		curw_fcst.run_view.last_run,
		curw_fcst.run_view.station_name
		INTO hash_id , model , model_version , sim_tag , last_run , station_name FROM
			curw_fcst.run_view
		WHERE
			curw_fcst.run_view.hash_id = NEW.id;
			
		

		OPEN curWL;
			
		checkWL: LOOP
			FETCH curWL INTO time, value;
			IF finished = 1 THEN 
				LEAVE checkWL;
			END IF;
			-- add alert WL to alert table
			IF value > 1.6 THEN 
				INSERT INTO `curw_fcst`.`wl_alert`
				(`hash_id`,`time`,`water_level`,`model`,`model_version`,`sim_tag`,`last_run`,`station_name`)
					VALUES
					(hash_id, time, value, model, model_version,sim_tag,last_run,station_name);
			END IF;
		END LOOP checkWL;
		CLOSE curWL;
		END IF;
END