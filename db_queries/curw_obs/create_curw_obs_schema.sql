use curw_obs;

 CREATE TABLE `source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` varchar(25) NOT NULL,
  `description` varchar(45) DEFAULT NULL,
  `parameters` json DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `station` (
  `id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_station_latitude` (`latitude`),
  KEY `idx_station_longitude` (`longitude`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `unit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `unit` varchar(10) NOT NULL,
  `type` enum('Accumulative','Instantaneous','Mean') NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `variable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `variable` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `run` (
  `id` varchar(64) NOT NULL,
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
  CONSTRAINT `run_ibfk_1` FOREIGN KEY (`station`) REFERENCES `station` (`id`),
  CONSTRAINT `run_ibfk_2` FOREIGN KEY (`source`) REFERENCES `source` (`id`),
  CONSTRAINT `run_ibfk_3` FOREIGN KEY (`variable`) REFERENCES `variable` (`id`),
  CONSTRAINT `run_ibfk_4` FOREIGN KEY (`unit`) REFERENCES `unit` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `data` (
  `id` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(8,3) NOT NULL,
  PRIMARY KEY (`id`,`time`),
  CONSTRAINT `data_ibfk_1` FOREIGN KEY (`id`) REFERENCES `run` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
