use curw_sim;

CREATE TABLE `grid_map` (
  `grid_id` varchar(45) NOT NULL,
  `obs1` int(11) NOT NULL,
  `obs2` int(11) NOT NULL,
  `obs3` int(11) NOT NULL,
  `fcst` int(11) NOT NULL,
  PRIMARY KEY (`grid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `run` (
  `id` varchar(64) NOT NULL,
  `latitude` decimal(8,6) NOT NULL,
  `longitude` decimal(8,6) NOT NULL,
  `model` varchar(25) NOT NULL,
  `method` varchar(100) NOT NULL,
  `grid_id` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `idx_run_grid_id` (`grid_id`),
  CONSTRAINT `run_ibfk_1` FOREIGN KEY (`grid_id`) REFERENCES `grid_map` (`grid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `data` (
    `id` VARCHAR(64) NOT NULL,
    `time` DATETIME NOT NULL,
    `value` DECIMAL(8 , 3 ) NOT NULL,
    PRIMARY KEY (`id` , `time`),
    CONSTRAINT `data_ibfk_1` FOREIGN KEY (`id`)
        REFERENCES `run` (`id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;
