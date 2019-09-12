use curw_fcst;

CREATE TABLE `station` (
  `id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_station_latitude` (`latitude`) USING BTREE,
  KEY `idx_station_longitude` (`longitude`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model` varchar(25) NOT NULL,
  `version` varchar(25) NOT NULL,
  `parameters` json DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `variable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `variable` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `unit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `unit` varchar(10) NOT NULL,
  `type` enum('Accumulative','Instantaneous','Mean') NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `run` (
  `id` varchar(64) NOT NULL,
  `sim_tag` varchar(100) NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `station` int(11) NOT NULL,
  `source` int(11) NOT NULL,
  `variable` int(11) NOT NULL,
  `unit` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `station` (`station`),
  KEY `source` (`source`),
  KEY `variable` (`variable`),
  KEY `unit` (`unit`),
  CONSTRAINT `run_ibfk_1` FOREIGN KEY (`station`) REFERENCES `station` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `run_ibfk_2` FOREIGN KEY (`source`) REFERENCES `source` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `run_ibfk_3` FOREIGN KEY (`variable`) REFERENCES `variable` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `run_ibfk_4` FOREIGN KEY (`unit`) REFERENCES `unit` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `data` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `fgt` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`fgt`,`time`),
  KEY `ix_data_fgt` (`fgt`),
  CONSTRAINT `data_ibfk_1` FOREIGN KEY (`id`) REFERENCES `run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
