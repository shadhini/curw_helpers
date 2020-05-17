import traceback
import csv
from datetime import datetime, timedelta

from db_adapter.constants import CURW_OBS_HOST, CURW_OBS_PORT, CURW_OBS_USERNAME, CURW_OBS_PASSWORD, CURW_OBS_DATABASE
from db_adapter.base import get_Pool, destroy_Pool
from db_adapter.curw_obs.station import StationEnum, get_station_id, add_station, update_description
from db_adapter.curw_obs.variable import get_variable_id, add_variable
from db_adapter.curw_obs.unit import get_unit_id, add_unit, UnitType
from db_adapter.curw_obs.timeseries import Timeseries


IRRIGATION_DEPARTMENT = 'Irrigation_Department'
CURW_WEATHER_STATION = 'CUrW_WeatherStation'
CURW_WATER_LEVEL_STATION = 'CUrW_WaterLevelGauge'
CURW_CROSS_SECTION = 'CUrW_CrossSection'


def read_csv(file_name):
    """
    Read csv file
    :param file_name: <file_path/file_name>.csv
    :return: list of lists which contains each row of the csv file
    """

    with open(file_name, 'r') as f:
        data = [list(line) for line in csv.reader(f)][1:]

    return data


def generate_curw_obs_hash_id(pool, variable, unit, unit_type, latitude, longitude, station_type=None,
                              station_name=None, description=None, append_description=False, start_date=None):

    """
    Generate corresponding curw_obs hash id for a given curw observational station
    :param pool: databse connection pool
    :param variable: str: e.g. "Precipitation"
    :param unit: str: e.g. "mm"
    :param unit_type: str: e.g. "Accumulative"
    :param latitude: float: e.g. 6.865576
    :param longitude: float: e.g. 79.958181
    :param station_type: str: enum:  'CUrW_WeatherStation' | 'CUrW_WaterLevelGauge' | 'CUrW_CrossSection' | 'Irrigation_Department'
    :param station_name: str: "Urumewella"
    :param description: str: "A&T Communication Box, Texas Standard Rain Gauge"
    :param append_description: bool:
    :param start_date: str: e.g."2019-07-01 00:00:00" ; the timestamp of the very first entry of the timeseries

    :return: new curw_obs hash id
    """


    try:

        lat = '%.6f' % float(latitude)
        lon = '%.6f' % float(longitude)
        meta_data = {
                'unit': unit, 'unit_type': unit_type,
                'latitude': lat, 'longitude': lon
                }

        if variable == "Waterlevel":
            variable = "WaterLevel"

        meta_data['variable'] = variable

        if station_type == IRRIGATION_DEPARTMENT:
            station_type = StationEnum.Irrigation_Department
        elif variable== CURW_WEATHER_STATION:
            station_type = StationEnum.CUrW_WeatherStation
        elif variable== CURW_WATER_LEVEL_STATION:
            station_type = StationEnum.CUrW_WaterLevelGauge
        elif variable==CURW_CROSS_SECTION:
            station_type = StationEnum.CUrW_CrossSection
        else:
            print("STATION_TYPE should be either Irrigation_Department or CUrW_WeatherStation or"
                  "CUrW_WaterLevelGauge or CUrW_CrossSection")
            exit(1)

        meta_data['station_type'] = StationEnum.getTypeString(station_type)

        unit_id = get_unit_id(pool=pool, unit=unit, unit_type=UnitType.getType(unit_type))

        if unit_id is None:
            add_unit(pool=pool, unit=unit, unit_type=UnitType.getType(unit_type))
            unit_id = get_unit_id(pool=pool, unit=unit, unit_type=UnitType.getType(unit_type))

        variable_id = get_variable_id(pool=pool, variable=variable)

        if variable_id is None:
            add_variable(pool=pool, variable=variable)
            variable_id = get_variable_id(pool=pool, variable=variable)

        station_id = get_station_id(pool=pool, latitude=lat, longitude=lon, station_type=station_type)

        if station_id is None:
            add_station(pool=pool, name=station_name, latitude=lat, longitude=lon,
                    station_type=station_type)
            station_id = get_station_id(pool=pool, latitude=lat, longitude=lon,
                    station_type=station_type)
            if description:
                update_description(pool=pool, id_=station_id, description=description, append=False)

        elif append_description:
            if description:
                update_description(pool=pool, id_=station_id, description=description, append=True)

        TS = Timeseries(pool=pool)

        tms_id = TS.get_timeseries_id_if_exists(meta_data=meta_data)

        meta_data['station_id'] = station_id
        meta_data['variable_id'] = variable_id
        meta_data['unit_id'] = unit_id

        if tms_id is None:
            tms_id = TS.generate_timeseries_id(meta_data=meta_data)
            meta_data['tms_id'] = tms_id
            TS.insert_run(run_meta=meta_data)
            if start_date:
                TS.update_start_date(id_=tms_id, start_date=start_date)

        return tms_id

    except Exception:
        traceback.print_exc()
        print("Exception occurred while inserting run entries to curw_obs run table and making hash mapping")


def insert_timeseries(pool, timeseries, tms_id, end_date=None):

    """
    Insert timeseries to curw_obs database
    :param pool: database connection pool
    :param timeseries: list of [time, value] lists
    :param end_date: str: timestamp of the latest data
    :param tms_id: str: curw_obs timeseries (hash) id
    :return:
    """
    new_timeseries = []
    for t in [i for i in timeseries]:
        if len(t) > 1:
            # Insert EventId in front of timestamp, value list
            t.insert(0, tms_id)
            new_timeseries.append(t)
        else:
            print('Invalid timeseries data:: %s', t)

    if end_date is None:
        end_date = new_timeseries[-1][1]

    try:

        ts = Timeseries(pool=pool)

        ts.insert_data(timeseries=new_timeseries, upsert=True)
        ts.update_end_date(id_=tms_id, end_date=end_date)

    except Exception as e:
        traceback.print_exc()
        print("Exception occurred while pushing timeseries for tms_id {} to curw_obs".format(tms_id))


def update_station_description_by_id(pool, station_id, description, append_description=True):

    try:

        if append_description:
            update_description(pool=pool, id_=station_id, description=description, append=True)
        else:
            update_description(pool=pool, id_=station_id, description=description, append=False)

    except Exception as e:
        traceback.print_exc()
        print("Exception occurred while updating description for station id {}.".format(station_id))


def update_station_description(pool, latitude, longitude, station_type, description, append_description=True):

    lat = '%.6f' % float(latitude)
    lon = '%.6f' % float(longitude)

    try:

        if station_type and station_type in (CURW_WATER_LEVEL_STATION, CURW_WEATHER_STATION, IRRIGATION_DEPARTMENT, CURW_CROSS_SECTION):
            station_type = StationEnum.getType(station_type)
        else:
            print("Station type cannot be recognized")
            exit(1)

        station_id = get_station_id(pool=pool, latitude=lat, longitude=lon, station_type=station_type)

        if append_description:
            update_description(pool=pool, id_=station_id, description=description, append=True)
        else:
            update_description(pool=pool, id_=station_id, description=description, append=False)

    except Exception as e:
        traceback.print_exc()
        print("Exception occurred while updating description for station id {}.".format(station_id))
