import traceback
import csv

# from db_adapter.constants import CURW_OBS_HOST, CURW_OBS_PORT, CURW_OBS_USERNAME, CURW_OBS_PASSWORD, CURW_OBS_DATABASE
from db_adapter.base import get_Pool, destroy_Pool
from db_adapter.curw_obs.station import StationEnum, get_station_id, add_station, update_description
from db_adapter.curw_obs.variable import get_variable_id, add_variable
from db_adapter.curw_obs.unit import get_unit_id, add_unit, UnitType
from db_adapter.curw_obs.timeseries import Timeseries


USERNAME = "root"
PASSWORD = "password"
HOST = "127.0.0.1"
PORT = 3306
DATABASE = "curw_obs"

CURW_WEATHER_STATION = 'CUrW_WeatherStation'
CURW_WATER_LEVEL_STATION = 'CUrW_WaterLevelGauge'
# id[0],name[1],start_date[2],end_date[3],name[4|station],latitude[5],longitude[6],description[7],variable[8],unit[9],type[10]

# 'latitude'    : '',
#                 'longitude'   : '',
#                 'station_type': '',
#                 'variable'    : '',
#                 'unit'        : '',
#                 'unit_type'   : ''


def create_csv(file_name, data):
    """
    Create new csv file using given data
    :param file_name: <file_path/file_name>.csv
    :param data: list of lists
    e.g. [['Person', 'Age'], ['Peter', '22'], ['Jasmine', '21'], ['Sam', '24']]
    :return:
    """
    with open(file_name, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)

    csvFile.close()


def read_csv(file_name):
    """
    Read csv file
    :param file_name: <file_path/file_name>.csv
    :return: list of lists which contains each row of the csv file
    """

    with open(file_name, 'r') as f:
        data = [list(line) for line in csv.reader(f)][1:]

    return data


def insert_curw_obs_runs():

    hash_mapping = [['old_hash_id', 'new_hash_id']]

    try:
        # pool = get_Pool(host=CURW_OBS_HOST, port=CURW_OBS_PORT, user=CURW_OBS_USERNAME, password=CURW_OBS_PASSWORD,
        #         db=CURW_OBS_DATABASE)

        pool = get_Pool(host=HOST, port=PORT, user=USERNAME, password=PASSWORD, db=DATABASE)

        curw_old_obs_entries = read_csv('all_curw_obs.csv')

        for old_index in range(len(curw_old_obs_entries)):

            meta_data = {}

            old_hash_id = curw_old_obs_entries[old_index][0]
            run_name = curw_old_obs_entries[old_index][1]
            station_name = curw_old_obs_entries[old_index][4]
            latitude =curw_old_obs_entries[old_index][5]
            longitude = curw_old_obs_entries[old_index][6]
            description = curw_old_obs_entries[old_index][7]
            variable = curw_old_obs_entries[old_index][8]
            unit = curw_old_obs_entries[old_index][9]
            unit_type = curw_old_obs_entries[old_index][10]

            meta_data['run_name'] = run_name

            meta_data['variable'] = variable
            meta_data['unit'] = unit
            meta_data['unit_type'] = unit_type

            meta_data['latitude'] = latitude
            meta_data['longitude'] = longitude

            if variable == "WaterLevel":
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

            station_id = get_station_id(pool=pool, latitude=latitude, longitude=longitude, station_type=station_type)

            if station_id is None:
                add_station(pool=pool, name=station_name, latitude=latitude, longitude=longitude,
                        station_type=station_type, description=description)
                station_id = get_station_id(pool=pool, latitude=latitude, longitude=longitude,
                        station_type=station_type)

            TS = Timeseries(pool=pool)

            tms_id = TS.get_timeseries_id_if_exists(meta_data=meta_data)

            meta_data['station_id'] = station_id
            meta_data['variable_id'] = variable_id
            meta_data['unit_id'] = unit_id

            if tms_id is None:
                tms_id = TS.generate_timeseries_id(meta_data=meta_data)
                meta_data['tms_id'] = tms_id
                TS.insert_run(run_meta=meta_data)

            hash_mapping.append([old_hash_id, tms_id])

        create_csv(file_name='curw_to_curw_obs_hash_id_mapping.csv', data=hash_mapping)

    except Exception:
        traceback.print_exc()
        print("Exception occurred while inserting run entries to curw_obs run table and making hash mapping")
    finally:
        destroy_Pool(pool=pool)


def generate_curw_obs_hash_id(variable, unit, unit_type, latitude, longitude, run_name, station_type=None,
                              station_name=None, description=None, append_description=True, update_run_name=True):
    if run_name not in ('A&T Labs', 'Leecom', 'CUrW IoT'):
        print("This function is dedicated for generating curw_obs hash ids only for 'A&T Labs', 'Leecom', 'CUrW IoT' "
              "weather stations")
        exit(1)

    try:
        # pool = get_Pool(host=CURW_OBS_HOST, port=CURW_OBS_PORT, user=CURW_OBS_USERNAME, password=CURW_OBS_PASSWORD,
        #         db=CURW_OBS_DATABASE)

        pool = get_Pool(host=HOST, port=PORT, user=USERNAME, password=PASSWORD, db=DATABASE)

        meta_data = { }

        run_name = run_name
        station_name = station_name
        latitude = latitude
        longitude = longitude
        description = description
        variable = variable
        unit = unit
        unit_type = unit_type

        meta_data['run_name'] = run_name

        meta_data['variable'] = variable
        meta_data['unit'] = unit
        meta_data['unit_type'] = unit_type

        meta_data['latitude'] = latitude
        meta_data['longitude'] = longitude

        if variable == "Waterlevel":
            variable = "WaterLevel"

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

        station_id = get_station_id(pool=pool, latitude=latitude, longitude=longitude, station_type=station_type)

        if station_id is None:
            add_station(pool=pool, name=station_name, latitude=latitude, longitude=longitude,
                    station_type=station_type)
            update_description(description=description, append=False)

            station_id = get_station_id(pool=pool, latitude=latitude, longitude=longitude,
                    station_type=station_type)
        elif append_description:
            update_description(description=description, append=True)

        TS = Timeseries(pool=pool)

        tms_id = TS.get_timeseries_id_if_exists(meta_data=meta_data)

        meta_data['station_id'] = station_id
        meta_data['variable_id'] = variable_id
        meta_data['unit_id'] = unit_id

        if tms_id is None:
            tms_id = TS.generate_timeseries_id(meta_data=meta_data)
            meta_data['tms_id'] = tms_id
            TS.insert_run(run_meta=meta_data)

        if update_run_name:
            TS.update_run_name(id_=tms_id, run_name=run_name)

    except Exception:
        traceback.print_exc()
        print("Exception occurred while inserting run entries to curw_obs run table and making hash mapping")
    finally:
        destroy_Pool(pool=pool)


def insert_timeseries(run_name=None):
    return None



