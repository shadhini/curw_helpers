use `curw_fcst`;

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

CREATE TABLE `station` (
  `id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model` varchar(25) NOT NULL,
  `version` varchar(25) NOT NULL,
  `parameters` json DEFAULT NULL,
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
  `fgt` datetime DEFAULT NULL,
  `scheduled_date` datetime NOT NULL,
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
    `id` VARCHAR(64) NOT NULL,
    `time` DATETIME NOT NULL,
    `value` DECIMAL(8 , 3 ) NOT NULL,
    PRIMARY KEY (`id` , `time`),
    CONSTRAINT `data_ibfk_1` FOREIGN KEY (`id`)
        REFERENCES `run` (`id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;
