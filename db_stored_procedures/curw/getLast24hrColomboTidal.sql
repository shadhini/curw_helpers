CREATE DEFINER=`routine_user`@`%` PROCEDURE `getLast24hrColomboTidal`()
BEGIN
SELECT 
    curw.data.time AS time, curw.data.value AS value
FROM
    curw.data
WHERE
    curw.data.id = "ebcc2df39aea35de15cca81bc5f15baffd94bcebf3f169add1fd43ee1611d367"
        AND curw.data.time >= SUBDATE(CURRENT_TIMESTAMP(),
        INTERVAL 24 HOUR)
        AND curw.data.time LIKE '%:00:00';
END