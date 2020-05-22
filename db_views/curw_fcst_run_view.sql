CREATE VIEW `run_view` AS
    SELECT 
        curw_fcst.run.id AS hash_id,
        curw_fcst.run.sim_tag AS sim_tag,
        curw_fcst.station.name AS station_name,
        curw_fcst.source.model AS model,
        curw_fcst.source.version AS model_version,
        curw_fcst.variable.variable AS variable,
        curw_fcst.unit.unit AS unit
    FROM
        (((((curw_fcst.run
        JOIN curw_fcst.station ON ((curw_fcst.run.station = curw_fcst.station.id)))
        JOIN curw_fcst.source ON ((curw_fcst.run.source = curw_fcst.source.id)))
        JOIN curw_fcst.variable ON ((curw_fcst.run.variable = curw_fcst.variable.id)))
        JOIN curw_fcst.unit ON ((curw_fcst.run.unit = curw_fcst.unit.id))))
