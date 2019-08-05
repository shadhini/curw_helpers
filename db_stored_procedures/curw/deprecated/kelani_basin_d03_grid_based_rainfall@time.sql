CREATE DEFINER=`root`@`%` PROCEDURE `getV3gridsRainfall`(
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
    curw.station_selected.latitude,
    curw.station_selected.longitude,
    curw.data.value
FROM
    (SELECT
        curw.station.id,
            curw.station.latitude,
            curw.station.longitude
    FROM
        curw.station
    WHERE
        curw.station.latitude BETWEEN 6.6 AND 7.4
            AND curw.station.longitude BETWEEN 79.6 AND 81.0) AS station_selected
        LEFT JOIN
    (SELECT
        curw.run.id AS run_id, curw.run.station AS station_id
    FROM
        curw.run
    WHERE
        curw.run.name = name
            AND curw.run.source = @sourceID
            AND curw.run.variable = @variableID
            AND curw.run.type = @typeID) AS run_selcted ON curw.run_selcted.station_id = curw.station_selected.id
        LEFT JOIN
    curw.data ON curw.run_selcted.run_id = curw.data.id
WHERE
    curw.data.time = time;
END