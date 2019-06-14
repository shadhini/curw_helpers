use curw_sim;

CREATE TABLE `grid_map` (
  `grid_id` varchar(45) NOT NULL,
  `obs1` int(11) NOT NULL,
  `obs2` int(11) NOT NULL,
  `obs3` int(11) NOT NULL,
  `fcst` int(11) NOT NULL,
  PRIMARY KEY (`grid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `grid_map_obs` (
  `grid_id` varchar(100) NOT NULL,
  `d03_1` int(11) NOT NULL,
  `d03_2` int(11) NOT NULL,
  `d03_3` int(11) NOT NULL,
  PRIMARY KEY (`grid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `run` (
  `id` varchar(64) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  `model` varchar(25) NOT NULL,
  `method` varchar(25) NOT NULL,
  `grid_id` varchar(100) DEFAULT NULL,
  `obs_end` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `idx_run_latitude` (`latitude`),
  KEY `idx_run_longitude` (`longitude`),
  KEY `idx_run_model` (`model`),
  KEY `idx_run_method` (`method`),
  KEY `fk_run_1_idx` (`grid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `data` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `data_ibfk_1` FOREIGN KEY (`id`) REFERENCES `run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `data_min` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `data_ibfk_2` FOREIGN KEY (`id`) REFERENCES `run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `data_max` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `data_ibfk_3` FOREIGN KEY (`id`) REFERENCES `run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


