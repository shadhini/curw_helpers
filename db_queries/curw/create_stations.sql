use `curw_stations`;

CREATE TABLE `flo2d_250_stations` (
  `id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `obs_stations` (
  `id` int(11) NOT NULL,
  `stationId` varchar(45) NOT NULL DEFAULT '',
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stationId_UNIQUE` (`stationId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
