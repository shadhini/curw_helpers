use curw_sim;

-- rainfall timeseries

CREATE TABLE `run` (
    `id` VARCHAR(64) NOT NULL,
    `latitude` DECIMAL(9 , 6 ) NOT NULL,
    `longitude` DECIMAL(9 , 6 ) NOT NULL,
    `model` VARCHAR(25) NOT NULL,
    `method` VARCHAR(25) NOT NULL,
    `obs_end` DATETIME DEFAULT NULL,
    `grid_id` VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id` (`id`),
    KEY `idx_run_latitude` (`latitude`),
    KEY `idx_run_longitude` (`longitude`),
    KEY `idx_run_model` (`model`),
    KEY `idx_run_method` (`method`),
    FULLTEXT KEY `idx_run_grid_id` ( `grid_id` )
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `data` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `data_ibfk_1` FOREIGN KEY (`id`) REFERENCES `run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `data_max` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `data_ibfk_3` FOREIGN KEY (`id`) REFERENCES `run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `data_min` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `data_ibfk_2` FOREIGN KEY (`id`) REFERENCES `run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- discharge timeseries

CREATE TABLE `dis_run` (
    `id` VARCHAR(64) NOT NULL,
    `latitude` DECIMAL(9 , 6 ) NOT NULL,
    `longitude` DECIMAL(9 , 6 ) NOT NULL,
    `model` VARCHAR(25) NOT NULL,
    `method` VARCHAR(25) NOT NULL,
    `obs_end` DATETIME DEFAULT NULL,
    `grid_id` VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id` (`id`),
    KEY `idx_dis_run_latitude` (`latitude`),
    KEY `idx_dis_run_longitude` (`longitude`),
    KEY `idx_dis_run_model` (`model`),
    KEY `idx_dis_run_method` (`method`),
    FULLTEXT KEY `idx_dis_run_grid_id` ( `grid_id` )
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `dis_data` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `dis_data_ibfk_1` FOREIGN KEY (`id`) REFERENCES `dis_run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dis_data_max` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `dis_data_ibfk_3` FOREIGN KEY (`id`) REFERENCES `dis_run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dis_data_min` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `dis_data_ibfk_2` FOREIGN KEY (`id`) REFERENCES `dis_run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- tide timeseries

CREATE TABLE `tide_run` (
    `id` VARCHAR(64) NOT NULL,
    `latitude` DECIMAL(9 , 6 ) NOT NULL,
    `longitude` DECIMAL(9 , 6 ) NOT NULL,
    `model` VARCHAR(25) NOT NULL,
    `method` VARCHAR(25) NOT NULL,
    `obs_end` DATETIME DEFAULT NULL,
    `grid_id` VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id` (`id`),
    KEY `idx_tide_run_latitude` (`latitude`),
    KEY `idx_tide_run_longitude` (`longitude`),
    KEY `idx_tide_run_model` (`model`),
    KEY `idx_tide_run_method` (`method`),
    FULLTEXT KEY `idx_tide_run_grid_id` ( `grid_id` )
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `tide_data` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `tide_data_ibfk_1` FOREIGN KEY (`id`) REFERENCES `tide_run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tide_data_max` (
    `id` VARCHAR(64) NOT NULL,
    `time` DATETIME NOT NULL,
    `value` DECIMAL(8 , 3 ) NOT NULL,
    PRIMARY KEY (`id` , `time`),
    CONSTRAINT `tide_data_ibfk_3` FOREIGN KEY (`id`)
        REFERENCES `tide_run` (`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `tide_data_min` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `tide_data_ibfk_2` FOREIGN KEY (`id`) REFERENCES `tide_run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- flo2d initial conditions

CREATE TABLE `grid_map_flo2d_initial_cond` (
  `grid_id` varchar(255) NOT NULL,
  `up_strm` int(11) NOT NULL,
  `down_strm` int(11) NOT NULL,
  `canal_seg` varchar(255) NOT NULL,
  `obs_wl` int(11) NOT NULL,
  PRIMARY KEY (`grid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- flo2d boundary conditions :: rain :: raincell

CREATE TABLE `grid_map_flo2d_raincell` (
    `grid_id` VARCHAR(255) NOT NULL,
    `obs1` INT(11) NOT NULL,
    `obs2` INT(11) NOT NULL,
    `obs3` INT(11) NOT NULL,
    `fcst` INT(11) NOT NULL,
    PRIMARY KEY (`grid_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

-- obs to d03 mappings ::

CREATE TABLE `grid_map_obs` (
  `grid_id` varchar(255) NOT NULL,
  `d03_1` int(11) NOT NULL,
  `d03_2` int(11) NOT NULL,
  `d03_3` int(11) NOT NULL,
  PRIMARY KEY (`grid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;