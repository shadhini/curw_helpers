CREATE DEFINER=`root`@`%` PROCEDURE `getGridBasedRainfall`(
IN name varchar(255),
IN source varchar(45),
IN variable varchar(100),
IN type varchar(45),
IN time DATETIME
)
BEGIN
SET @typeID = (SELECT curw.type.id FROM curw.type WHERE curw.type.type = type);
SET @variableID = (SELECT curw.variable.id FROM curw.variable WHERE curw.variable.variable = variable);
SET @sourceID = (SELECT curw.source.id FROM curw.source WHERE curw.source.source = source);

SELECT
    curw.station.latitude,
    curw.station.longitude,
    curw.data_temp.value
FROM
    (SELECT
        curw.data.id,
            curw.data.time,
            curw.data.value,
            curw.run_temp.station
    FROM
        curw.data
    RIGHT JOIN (SELECT
        curw.run.id, curw.run.station
    FROM
        curw.run
    WHERE
        curw.run.name = name
            AND curw.run.source = @sourceID
            AND curw.run.variable = @variableID
            AND curw.run.type = @typeID) AS run_temp ON curw.data.id = curw.run_temp.id
    WHERE
        curw.data.time = time) AS data_temp
        LEFT JOIN
    curw.station ON curw.data_temp.station = curw.station.id;
END