CREATE DEFINER=`root`@`%` PROCEDURE `getNearestStation`(
IN lat DECIMAL(9,6),
IN lng DECIMAL(9,6)
)
BEGIN
	SELECT ordered_stations.id AS id, ordered_stations.name AS name, ordered_stations.latitude AS latitude, ordered_stations.longitude AS longitude
    FROM 
    (SELECT
		id, name, latitude, longitude,
		(  
		   cos(radians(lat)) *
		   cos(radians(latitude)) *
		   cos(radians(longitude) -
		   radians(lng)) +
		   sin(radians(lat)) *
		   sin(radians(latitude))
		) AS distance
		FROM curw_fcst.station
		ORDER BY distance DESC LIMIT 1) AS ordered_stations;
END