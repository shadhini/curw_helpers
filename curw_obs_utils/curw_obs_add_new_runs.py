import traceback
import csv

# from db_adapter.constants import CURW_OBS_HOST, CURW_OBS_PORT, CURW_OBS_USERNAME, CURW_OBS_PASSWORD, CURW_OBS_DATABASE
from db_adapter.base import get_Pool, destroy_Pool
from db_adapter.curw_obs.station import StationEnum, get_station_id, add_station
from db_adapter.curw_obs.variable import get_variable_id, add_variable
from db_adapter.curw_obs.unit import get_unit_id, add_unit, UnitType
from db_adapter.curw_obs.timeseries import Timeseries


USERNAME = "root"
PASSWORD = "password"
HOST = "127.0.0.1"
PORT = 3306
DATABASE = "curw_obs"

# [id[0],name[1],start_date[2],end_date[3],station[4],variable[5],unit[6],type[7],source[8],id[9],stationId[10],name[11],
# control[12],status[13],latitude[14],longitude[15],resolution[16],description[17]]

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

            variable = curw_old_obs_entries[old_index][5]

            meta_data['variable'] = variable

            variable_id = get_variable_id(pool=pool, variable=variable)

            if variable_id is None:
                add_variable(pool=pool, variable=curw_old_obs_entries[old_index][5])
                variable_id = get_variable_id(pool=pool, variable=variable)

            unit = curw_old_obs_entries[old_index][6]

            meta_data['unit'] = unit

            if unit == 'mm':
                unit_id = get_unit_id(pool=pool, unit=unit, unit_type=UnitType.Accumulative)
                meta_data['unit_type'] = UnitType.Accumulative.value
            else:
                unit_id = get_unit_id(pool=pool, unit=unit, unit_type=UnitType.Instantaneous)
                meta_data['unit_type'] = UnitType.Instantaneous.value

            if unit_id is None:
                if unit=='mm':
                    add_unit(pool=pool, unit=unit, unit_type=UnitType.Accumulative)
                    unit_id = get_unit_id(pool=pool, unit=unit, unit_type=UnitType.Accumulative)
                else:
                    add_unit(pool=pool, unit=unit, unit_type=UnitType.Instantaneous)
                    unit_id = get_unit_id(pool=pool, unit=unit, unit_type=UnitType.Instantaneous)

            if variable == "WaterLevel":
                station_type = StationEnum.CUrW_WaterLevelGauge
            else:
                station_type = StationEnum.CUrW_WeatherStation

            name = curw_old_obs_entries[old_index][11]

            latitude = curw_old_obs_entries[old_index][14]

            meta_data['latitude'] = latitude

            longitude = curw_old_obs_entries[old_index][15]

            meta_data['longitude'] = longitude

            description = curw_old_obs_entries[old_index][17]

            station_id = get_station_id(pool=pool, latitude=latitude, longitude=longitude, station_type=station_type)

            if station_id is None:
                add_station(pool=pool, name=name, latitude=latitude, longitude=longitude,
                        description=description, station_type=station_type)
                station_id = get_station_id(pool=pool, latitude=latitude, longitude=longitude,
                        station_type=station_type)

            meta_data['station_type'] = StationEnum.getTypeString(station_type)

            run_name = curw_old_obs_entries[old_index][1]

            TS = Timeseries(pool=pool)

            tms_id = TS.get_timeseries_id_if_exists(meta_data=meta_data)

            meta_data['station_id'] = station_id
            meta_data['variable_id'] = variable_id
            meta_data['unit_id'] = unit_id
            meta_data['run_name'] = run_name

            if tms_id is None:
                tms_id = TS.generate_timeseries_id(meta_data=meta_data)
                meta_data['tms_id'] = tms_id
                TS.insert_run(run_meta=meta_data)

            hash_mapping.append([curw_old_obs_entries[old_index][0], tms_id])

        create_csv(file_name='curw_to_curw_obs_hash_id_mapping.csv', data=hash_mapping)

    except Exception:
        traceback.print_exc()
        print("Exception occurred while inserting run entries to curw_obs run table and making hash mapping")
    finally:
        destroy_Pool(pool=pool)


insert_curw_obs_runs()
