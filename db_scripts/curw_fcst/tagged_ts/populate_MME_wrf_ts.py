#!/home/uwcc-admin/rfield_extractor/venv/bin/python3
import traceback
import pymysql
import json
import getopt
import sys
import os
import multiprocessing as mp
from datetime import datetime, timedelta

from db_adapter.constants import CURW_FCST_DATABASE, CURW_FCST_HOST, CURW_FCST_PASSWORD, CURW_FCST_PORT, CURW_FCST_USERNAME

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


def append_value_for_timestamp(existing_ts, new_ts):

    """
    Appending timeseries assuming start and end of both timeseries are same
    :param existing_ts: list of [timestamp, value1, value2, .., valuen] lists (note: this might include several values)
    :param new_ts: list of [timestamp, VALUE] list (note: this include single value)
    :return: list of [timestamp, value1, value2, .., valuen, VALUE]
    """

    appended_ts =[]

    if len(existing_ts) == len(new_ts) and existing_ts[0][0] == new_ts[0][0]:
        for i in range(len(existing_ts)):
            appended_ts.append(existing_ts[i])
            appended_ts[i].append(new_ts[i][1])
    else:
        return existing_ts

    return appended_ts


def average_timeseries(timeseries):
    """
    Give the timeseries with avg value for given timeseries containing several values per one timestamp
    :param timeseries:
    :return:
    """
    avg_timeseries = []

    if len(timeseries[0]) <= 2:
        return timeseries
    else:
        for i in range(len(timeseries)):
            count = len(timeseries[i])-1
            avg_timeseries.append([timeseries[i][0], '%.3f' % (sum(timeseries[i][1:])/count)])

    return avg_timeseries


def populate_MME_ts(wrf_model, version, sim_tag):



def usage():
    usageText = """
    Usage: python gen_rfield_kelani_basin_parallelized_optimized_with_past_future.py -m WRF_X1,WRF_X2,WRF_X3 -v vX -s "evening_18hrs"

    -h  --help          Show usage
    -c  --wrf_model     Path to config file (e.g. /home/shadhini/db_scripts/curw_fcst/tagged_ts/MME_config.json). Compulsory arg
    """
    print(usageText)


if __name__=="__main__":

    my_pool = None
    try:

        config_path = None

        try:
            opts, args = getopt.getopt(sys.argv[1:], "h:c:",
                    ["help", "config="])
        except getopt.GetoptError:
            usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt in ("-m", "--wrf_model"):
                wrf_models = arg.strip()

        print(wrf_models)

        # load connection parameters
        config = json.loads(open('/home/uwcc-admin/rfield_extractor/MME_config.json').read())

        wrf_model_list = wrf_models.split(',')

        for wrf_model in wrf_model_list:
            if wrf_model is None or wrf_model not in VALID_MODELS:
                usage()
                exit(1)

        if version is None or version not in VALID_VERSIONS:
            usage()
            exit(1)

        if sim_tag is None or sim_tag not in SIM_TAGS:
            usage()
            exit(1)

        past_rfield_home = "/mnt/disks/wrf_nfs/wrf/{}/rfield/kelani_basin/past".format(version)
        try:
            os.makedirs(past_rfield_home)
        except FileExistsError:
            # directory already exists
            pass

        future_rfield_home = "/mnt/disks/wrf_nfs/wrf/{}/rfield/kelani_basin/future".format(version)
        try:
            os.makedirs(future_rfield_home)
        except FileExistsError:
            # directory already exists
            pass

        mp_pool = mp.Pool(mp.cpu_count())

        results = mp_pool.starmap_async(gen_rfield_d03_kelani_basin,
                                        [(wrf_model, version, sim_tag) for wrf_model in wrf_model_list]).get()

        print("results: ", results)

    except Exception as e:
        print('JSON config data loading error.')
        traceback.print_exc()
    finally:
        if my_pool is not None:
            mp_pool.close()




