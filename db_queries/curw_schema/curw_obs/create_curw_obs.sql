use curw_obs;

CREATE TABLE `station` (
  `id` int(11) NOT NULL,
  `station_type` enum('CUrW_WeatherStation','CUrW_WaterLevelGauge','CUrW_CrossSection','Public','Other') NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  `description` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_station_latitude` (`latitude`),
  KEY `idx_station_longitude` (`longitude`),
  KEY `idx_station_station_type` (`station_type`)
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
  `station` int(11) NOT NULL,
  `variable` int(11) NOT NULL,
  `unit` int(11) NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `run_ibfk_1_idx` (`station`),
  KEY `run_ibfk_3` (`variable`),
  KEY `run_ibfk_4` (`unit`),
  CONSTRAINT `run_ibfk_1` FOREIGN KEY (`station`) REFERENCES `station` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `run_ibfk_3` FOREIGN KEY (`variable`) REFERENCES `variable` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `run_ibfk_4` FOREIGN KEY (`unit`) REFERENCES `unit` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `data` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `data_ibfk_1` FOREIGN KEY (`id`) REFERENCES `run` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
