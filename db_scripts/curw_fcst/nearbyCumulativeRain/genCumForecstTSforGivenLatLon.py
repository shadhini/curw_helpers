#!/home/uwcc-admin/rfield_extractor/venv/bin/python3
import traceback
import pymysql
import json
import sys
import getopt
import os
import multiprocessing as mp
import pandas as pd
from datetime import datetime, timedelta


# connection params
HOST = ""
USER = ""
PASSWORD = ""
DB = ""
PORT = ""

VALID_MODELS = ["WRF_A", "WRF_C", "WRF_E", "WRF_SE"]
VALID_VERSIONS = ["v3", "v4", "4.0"]
SIM_TAGS = ["evening_18hrs"]


def read_attribute_from_config_file(attribute, config):
    """
    :param attribute: key name of the config json file
    :param config: loaded json file
    :return:
    """
    if attribute in config and (config[attribute]!=""):
        return config[attribute]
    else:
        print("{} not specified in config file.".format(attribute))
        exit(1)


def write_to_file(file_name, data):
    with open(file_name, 'w+') as f:
        f.write('\n'.join(data))


def create_dataframe(wrf_model, version, sim_tag, latitude, longitude, start_time, end_time, station):

    # Connect to the database
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB,
            cursorclass=pymysql.cursors.DictCursor)

    try:
        # retrieve per 15 mins rainfall
        # rainfallNlead = [['time', 'fgt', 'lead', 'value']]
        rainfallNlead = []
        with connection.cursor() as cursor:
            # 6.935042, 79.915401, "WRF_A", "4.0", "evening_18hrs", "2019-08-01 00:00:00", "2019-08-18 00:00:00"
            cursor.callproc('getNearbyRainWithLead', (latitude, longitude, wrf_model, version, sim_tag, start_time, end_time))
            results = cursor.fetchall()
            for result in results:
                rainfallNlead.append('{},{},{},{}'.format(result.get('time'), result.get('fgt'),
                                                          result.get('lead'), result.get('value')))

        file_name = '/var/www/html/wrf/{}/cumulative_forecast/{}_{}_{}_forecast_rainfall.csv'\
            .format(version, wrf_model, version, station)

        write_to_file(file_name, rainfallNlead)

        return pd.read_csv(file_name, delimiter=',', names=['time', 'fgt', 'lead', 'value'])

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()
        print("Process finished")


def get_fcst_cum_sum_based_on_fgt(dataframe):
    """
    :param dataframe: pandas dataframe with heading ['time', 'fgt', 'lead', 'value']
    :return: data frame with cumulative timeseries
    """
    df = dataframe
    for date in df.fgt.unique():
        df['fcst_cum_value'] = df.groupby('fgt').value.cumsum()
    return df


def get_obs_cum_sum(dataframe):
    """
    :param dataframe: pandas dataframe with heading ['time', 'value']
    :return: data frame with cumulative timeseries
    """
    df = dataframe
    df['obs_cum_value'] = df.value.cumsum()
    return df


def usage():
    usageText = """
    Usage: python genCumForecstTSforGivenLatLon.py -m WRF_X1,WRF_X2,WRF_X3 -v vX -s "evening_18hrs"

    -h  --help          Show usage
    -m  --wrf_model     List of WRF models (e.g. WRF_A, WRF_E). Compulsory arg
    -v  --version       WRF model version (e.g. v4, v3). Compulsory arg
    -t  --sim_tag       Simulation tag (e.g. evening_18hrs). Compulsory arg
    -s  --start_time    Timeseries start time (e.g: "2019-06-05 00:00:00"). Default is 23:30:00, 3 days before today.
    -e  --end_time      Timeseries end time (e.g: "2019-06-05 23:30:00"). Default is 23:30:00, tomorrow.

    """
    print(usageText)


if __name__=="__main__":

    df1 = pd.read_csv('/home/shadhini/dev/repos/shadhini/curw_helpers/db_scripts/curw_fcst/nearbyCumulativeRain/insta_rainfall.csv', delimiter=',')
    df2 = pd.read_csv('/home/shadhini/dev/repos/shadhini/curw_helpers/db_scripts/curw_fcst/nearbyCumulativeRain/obs_rainfall.csv', delimiter=',')

    obs_df = get_obs_cum_sum(df2)
    fcst_df = get_fcst_cum_sum_based_on_fgt(df1)

    dataframe = pd.merge(fcst_df, obs_df, how='left', on='time')
    print(dataframe)#.drop(columns=['fgt', 'value']))


    # mp_pool = None
    #
    # try:
    #     wrf_models = None
    #     version = None
    #     sim_tag = None
    #     start = None
    #     end = None
    #
    #     try:
    #         opts, args = getopt.getopt(sys.argv[1:], "h:m:v:t:s:e:",
    #                 ["help", "wrf_model=", "version=", "sim_tag=", "start=", "end="])
    #     except getopt.GetoptError:
    #         usage()
    #         sys.exit(2)
    #     for opt, arg in opts:
    #         if opt in ("-h", "--help"):
    #             usage()
    #             sys.exit()
    #         elif opt in ("-m", "--wrf_model"):
    #             wrf_models = arg.strip()
    #         elif opt in ("-v", "--version"):
    #             version = arg.strip()
    #         elif opt in ("-t", "--sim_tag"):
    #             sim_tag = arg.strip()
    #         elif opt in ("-s", "--start"):
    #             start = arg.strip()
    #         elif opt in ("-e", "--end"):
    #             end = arg.strip()
    #
    #     # load connection parameters
    #     config = json.loads(open('/home/uwcc-admin/rfield_extractor/config.json').read())
    #
    #     # connection params
    #     HOST = read_attribute_from_config_file('host', config)
    #     USER = read_attribute_from_config_file('user', config)
    #     PASSWORD = read_attribute_from_config_file('password', config)
    #     DB = read_attribute_from_config_file('db', config)
    #     PORT = read_attribute_from_config_file('port', config)
    #
    #     wrf_model_list = wrf_models.split(',')
    #
    #     for wrf_model in wrf_model_list:
    #         if wrf_model is None or wrf_model not in VALID_MODELS:
    #             usage()
    #             exit(1)
    #     if version is None or version not in VALID_VERSIONS:
    #         usage()
    #         exit(1)
    #     if sim_tag is None or sim_tag not in SIM_TAGS:
    #         usage()
    #         exit(1)
    #
    #     cumulative_fcst_home = "/var/www/html/wrf/{}/cumulative_forecast".format(version)
    #     try:
    #         os.makedirs(cumulative_fcst_home)
    #     except FileExistsError:
    #         # directory already exists
    #         pass
    #
    #     mp_pool = mp.Pool(mp.cpu_count())
    #
    #     results = mp_pool.starmap(gen_rfield_d03,
    #                                     [(wrf_model, version, sim_tag) for wrf_model in wrf_model_list]).get()
    #
    #     print("results: ", results)
    #
    # except Exception as e:
    #     print('JSON config data loading error.')
    #     traceback.print_exc()
    # finally:
    #     if mp_pool is not None:
    #         mp_pool.close()


