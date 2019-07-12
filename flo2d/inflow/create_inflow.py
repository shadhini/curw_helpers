import pymysql
from datetime import datetime, timedelta
import traceback
import json
import os

from db_adapter.base import  get_Pool, destroy_Pool
from db_adapter.curw_fcst.station import get_hechms_stations

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# connection params
FCST_HOST = "10.138.0.13"
FCST_USER = "routine_user"
FCST_PASSWORD = "aquaroutine"
FCST_DB ="curw_fcst"
FCST_PORT = 3306

OBS_HOST = "10.138.0.13"
OBS_USER = "routine_user"
OBS_PASSWORD = "aquaroutine"
OBS_DB ="curw_sim"
OBS_PORT = 3306

TEMP_HOST = "104.198.0.87"
TEMP_USER = "root"
TEMP_PASSWORD = "cfcwm07"
TEMP_DB ="curw"
TEMP_PORT = 3306

#temp parameter
OBS_WL_ID = "70648fc7b9abd08530b1d735b5db19b3e940b8b5b72dd696c8114b0c4b01a6d2"


def write_to_file(file_name, data):
    with open(file_name, 'w+') as f:
        f.write('\n'.join(data))


def append_to_file(file_name, data):
    with open(file_name, 'a+') as f:
        f.write('\n'.join(data))


def read_attribute_from_config_file(attribute, config, compulsory):
    """
    :param attribute: key name of the config json file
    :param config: loaded json file
    :param compulsory: Boolean value: whether the attribute is must present or not in the config file
    :return:
    """
    if attribute in config and (config[attribute]!=""):
        return config[attribute]
    elif compulsory:
        print("{} not specified in config file.".format(attribute))
        exit(1)
    else:
        print("{} not specified in config file.".format(attribute))
        return None


def get_obs_waterlevel(station_id, start):

    connection = pymysql.connect(host=TEMP_HOST, user=TEMP_USER, password=TEMP_PASSWORD, db=TEMP_DB,
            cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor1:
            sql_statement = "select `value` from `data` where `id`=%s and `time` <= %s ORDER BY `time` DESC limit 1;"
            rows = cursor1.execute(sql_statement, (station_id, start))
            if rows > 0 :
                return cursor1.fetchone()['value']
            else:
                return None

    except Exception as e:
        traceback.print_exc()
        return None
    finally:
        connection.close()


def extract_fcst_discharge_ts(pool, start, end, station_ids):

    connection = pool.connection()

    fcst_ids = {}
    fcst_ts = {}

    try:
        with connection.cursor() as cursor1:
            sql_statement = "SELECT `id`, `station`, `start_date`, `end_date` FROM `run` " \
                            "where `source`=11 and `variable`=3 and `unit`=3;"
            cursor1.execute(sql_statement)
            for result in cursor1:
                fcst_ids[result.get('station')] = [result.get('id'), result.get('start_date'), result.get('end_date')]

        for station_id in station_ids:
            tms_id = fcst_ids.get(station_id)[0]
            fgt = fcst_ids.get(station_id)[2]
            with connection.cursor() as cursor1:
                sql_statement = "SELECT `time`, `value` FROM `data` where `id`=%s and `fgt`=%s " \
                                "and `time` BETWEEN %s AND  %s;"
                cursor1.execute(sql_statement, (tms_id, fgt, start, end))
                timeseries = []
                for result in cursor1:
                    timeseries.append([result.get('time'), result.get('value')])

                fcst_ts[station_id] = timeseries

        return  fcst_ts

    except Exception as e:
        traceback.print_exc()
    finally:
        connection.close()


def prepare_inflow(inflow_file_path, fcst_discharge_ts, obs_wl):

    inflow = []

    inflow.append('0               0')
    inflow.append('            8655')

    timeseries = fcst_discharge_ts
    for i in range(len(timeseries)):
        time_col = ('%.1f' % (((timeseries[i][0] - timeseries[0][0]).total_seconds())/3600)).rjust(16)
        value_col = ('%.1f' % (timeseries[i][1])).rjust(16)
        inflow.append('H' + time_col + value_col)

    inflow.append('R            2265{}'.format(obs_wl.rjust(16)))
    inflow.append('R            3559              6.6')

    write_to_file(inflow_file_path, data=inflow)


if __name__=="__main__":

    try:

        config = json.loads(open('config.json').read())

        start = read_attribute_from_config_file('start_time', config, True)
        end =  read_attribute_from_config_file('end_time', config, True)

        target_stations = read_attribute_from_config_file('station_names', config, True)

        output_dir = read_attribute_from_config_file('output_file_name', config, True)
        file_name = read_attribute_from_config_file('output_dir', config, True)

        pool = get_Pool(host=FCST_HOST, port=FCST_PORT, user=FCST_USER, password=FCST_PASSWORD, db=FCST_DB)
        hechms_stations = get_hechms_stations(pool=pool)

        target_station_ids = []

        for i in range(len(target_stations)):
            target_station_ids.append(hechms_stations.get(target_stations[i]))

        obs_wl = get_obs_waterlevel(station_id=OBS_WL_ID, start=start)
        if obs_wl is None:
            obs_wl = 0.5

        fcst_discharges = extract_fcst_discharge_ts(pool=pool, start=start, end=end, station_ids=target_station_ids)

        for id in target_station_ids:
            file_path = os.path.join(output_dir, '{}_{}'.format(id, file_name))
            prepare_inflow(inflow_file_path=file_path, fcst_discharge_ts=fcst_discharges.get(id), obs_wl=obs_wl)

    except Exception as e:
        traceback.print_exc()
    finally:
        destroy_Pool(pool)
