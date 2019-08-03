import hashlib
import json
import logging
import traceback
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
from mysqladapter1 import \
    check_id, \
    get_meta_data, \
    extract_timeseries, \
    insert_id_rows, \
    get_obs_hash

from db_adapter.constants import CURW_OBS_HOST, CURW_OBS_PORT, CURW_OBS_USERNAME, CURW_OBS_PASSWORD, CURW_OBS_DATABASE
from db_adapter.base import get_Pool, destroy_Pool
from db_adapter.curw_obs.station import StationEnum, get_station_id, add_station, update_description
from db_adapter.curw_obs.variable import get_variable_id, add_variable
from db_adapter.curw_obs.unit import get_unit_id, add_unit, UnitType
from db_adapter.curw_obs.timeseries import Timeseries

CURW_WEATHER_STATION = 'CUrW_WeatherStation'
CURW_WATER_LEVEL_STATION = 'CUrW_WaterLevelGauge'

def map_curw_id(result):

    try:
            # if curw_id doesnot exist in the table retrieve meta data to generate curw_obs hash id
            curw_id = check_id(result)
            if curw_id is None:
                print("The event id does not exist in the id_mapping table")
                #generate a new obs hash id, for that get meta data
                meta_data = get_meta_data(result)
                #print("*****************")
                #print(meta_data)
                dict1 = meta_data[0]
                dict2 = meta_data[1]
                dict3 = meta_data[2]
                dict4 = meta_data[3]

                run_name = dict1['run_name']
                start_date = dict1['start_date']
                station_name = dict2['station_name']
                latitude = dict2['latitude']
                longitude = dict2['longitude']
                description = dict2['description']
                variable = dict3['variable']
                unit = dict4['unit']
                unit_type = dict4['unit-type']
                pool = get_Pool(host=CURW_OBS_HOST, port=CURW_OBS_PORT, user=CURW_OBS_USERNAME, password=CURW_OBS_PASSWORD, db=CURW_OBS_DATABASE)


                obs_hash_id = generate_curw_obs_hash_id(pool, variable=variable, unit=unit, unit_type=unit_type, latitude=latitude, longitude=longitude, run_name=run_name, station_name=station_name, description=description, start_date=start_date.strftime(COMMON_DATE_FORMAT))

                #insert the corresponding obs_hash_id to curw_id
                insert_id_rows(result, obs_hash_id)

                #then extract the time series
                timeseries = []
                timeseries = extract_timeseries(obs_hash_id)
                #print("***********")
                #print(timeseries)
                #print("***********")

                #insert the timeseries in obs_db
                insert_timeseries(pool=pool, timeseries=timeseries, tms_id=obs_hash_id, end_date=timeseries[-1][0])
            else:
                #get the relavant obs_hashId to the curw_id
                obs_hash = get_obs_hash(result)
                # then extract the time series
                timeseries = []
                timeseries = extract_timeseries(obs_hash)
                #print("*******")
                #print(timeseries)
                #print(timeseries[-1][0])
                #print("*******")

                # insert the timeseries in obs_db
                pool = get_Pool(host=CURW_OBS_HOST, port=CURW_OBS_PORT, user=CURW_OBS_USERNAME, password=CURW_OBS_PASSWORD, db=CURW_OBS_DATABASE)
                insert_timeseries(pool=pool, timeseries=timeseries, tms_id=result, end_date=timeseries[-1][0])


    except Exception as e:
        traceback.print_exc()
    finally:
        destroy_Pool(pool=pool)
        print("Process finished")

def generate_curw_obs_hash_id(pool, variable, unit, unit_type, latitude, longitude, run_name, station_type=None,
                              station_name=None, description=None, append_description=True, update_runname=True,
                              start_date=None):

    """
    Generate corresponding curw_obs hash id for a given curw observational station
    :param pool: databse connection pool
    :param variable: str: e.g. "Precipitation"
    :param unit: str: e.g. "mm"
    :param unit_type: str: e.g. "Accumulative"
    :param latitude: float: e.g. 6.865576
    :param longitude: float: e.g. 79.958181
    :param run_name: str: e.g "A&T Labs"
    :param station_type: str: enum:  'CUrW_WeatherStation' | 'CUrW_WaterLevelGauge'
    :param station_name: str: "Urumewella"
    :param description: str: "A&T Communication Box, Texas Standard Rain Gauge"
    :param append_description: bool:
    :param update_run_name: bool:
    :param start_date: str: e.g."2019-07-01 00:00:00" ; the timestamp of the very first entry of the timeseries
    :return: new curw_obs hash id
    """
    if run_name not in ('A&T Labs', 'Leecom', 'CUrW IoT'):
        print("This function is dedicated for generating curw_obs hash ids only for 'A&T Labs', 'Leecom', 'CUrW IoT' "
              "weather stations")
        exit(1)

    try:

        lat = '%.6f' % float(latitude)
        lon = '%.6f' % float(longitude)
        meta_data = {
                'run_name' : run_name, 'unit': unit, 'unit_type': unit_type,
                'latitude': lat, 'longitude': lon
                }

        if variable == "Waterlevel":
            variable = "WaterLevel"

        meta_data['variable'] = variable

        if station_type and station_type in (CURW_WATER_LEVEL_STATION, CURW_WEATHER_STATION):
            station_type = StationEnum.getType(station_type)
        else:
            if variable=="WaterLevel":
                station_type = StationEnum.CUrW_WaterLevelGauge
            else:
                station_type = StationEnum.CUrW_WeatherStation

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

        if update_runname:
            TS.update_run_name(id_=tms_id, run_name=run_name)

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


def update_ts_run_name(pool, run_name, tms_id):

    try:

        ts = Timeseries(pool=pool)

        ts.update_run_name(id_=tms_id, run_name=run_name)

    except Exception as e:
        traceback.print_exc()
        print("Exception occurred while updating run name for tms_id {}.".format(tms_id))


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

        if station_type and station_type in (CURW_WATER_LEVEL_STATION, CURW_WEATHER_STATION):
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