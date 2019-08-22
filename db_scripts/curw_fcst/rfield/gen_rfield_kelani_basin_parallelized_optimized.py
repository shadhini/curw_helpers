#!/home/uwcc-admin/curw_rfield_extractor/venv/bin/python3
import traceback
import pymysql
import json
import getopt
import sys
import os
import multiprocessing as mp
from datetime import datetime, timedelta

# connection params
HOST = ""
USER = ""
PASSWORD = ""
DB =""
PORT = ""

VALID_MODELS = ["WRF_A", "WRF_C", "WRF_E", "WRF_SE"]
VALID_VERSIONS = ["v3", "v4", "4.0"]
SIM_TAGS = ["evening_18hrs"]
root_directory = '/mnt/disks/cms-data/temp'


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


def create_rfield(connection, wrf_model, version, sim_tag, timestamp, past_or_future):
    # rfield = [['latitude', 'longitude', 'rainfall']]
    rfield = []
    with connection.cursor() as cursor0:
        cursor0.callproc('get_d03_rfield_kelani_basin_rainfall', (wrf_model, version, sim_tag, timestamp))
        results = cursor0.fetchall()
        for result in results:
            rfield.append('{}'.format(result.get('value')))

    write_to_file('{}/wrf/{}/{}/rfield/kelani_basin/{}/{}_{}_{}_rfield.txt'
                  .format(root_directory, version, sim_tag, past_or_future, wrf_model, version, timestamp.strftime('%Y-%m-%d_%H-%M')), rfield)


#############################
# Raw WRF RFIELD GENERATION #
#############################

def gen_rfield_d03_kelani_basin(wrf_model, version, sim_tag):

    #         os.system("rm /mnt/disks/wrf_nfs/wrf/{}/rfield/{}/kelani_basin/past/{}_{}_*".format(version, sim_tag, wrf_model, version))

    # remove outdated rfields
    try:
        os.system("sudo rm {}/wrf/{}/{}/rfield/kelani_basin/past/{}_{}_*".format(root_directory, version, sim_tag, wrf_model, version))
        os.system("sudo rm {}/wrf/{}/{}/rfield/kelani_basin/future/{}_{}_*".format(root_directory, version, sim_tag, wrf_model, version))
    except Exception as e:
        traceback.print_exc()

    start_time = ''
    end_time = ''

    now = datetime.strptime((datetime.now()+timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S')

    try:
        # Connect to the database
        connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB,
                                     cursorclass=pymysql.cursors.DictCursor)

        # Extract timeseries start time and end time
        with connection.cursor() as cursor1:
            cursor1.callproc('get_TS_start_end', (wrf_model, version, sim_tag))
            result = cursor1.fetchone()
            start_time = result.get('start')
            end_time = result.get('end')

        if end_time > (now + timedelta(days=1)):
            # Extract rfields
            timestamp = start_time

            if timestamp < now and timestamp <= end_time:
                rfield = []
                with connection.cursor() as cursor1:
                    cursor1.callproc('get_d03_rfield_kelani_basin_rainfall', (wrf_model, version, sim_tag, timestamp))
                    results = cursor1.fetchall()
                    for result in results:
                        rfield.append(
                            '{} {} {}'.format(result.get('longitude'), result.get('latitude'), result.get('value')))

                write_to_file('{}/wrf/{}/{}/rfield/kelani_basin/{}/{}_{}_{}_rfield.txt'
                              .format(root_directory, version, sim_tag, "past", wrf_model, version,
                                      timestamp.strftime('%Y-%m-%d_%H-%M')), rfield)

                timestamp = datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S') + timedelta(minutes=15)

            while timestamp < now:
                create_rfield(connection=connection, wrf_model=wrf_model, version=version, sim_tag=sim_tag,
                              timestamp=timestamp, past_or_future="past")

                timestamp = datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S') + timedelta(minutes=15)

            if timestamp <= end_time:
                rfield = []
                with connection.cursor() as cursor1:
                    cursor1.callproc('get_d03_rfield_kelani_basin_rainfall', (wrf_model, version, sim_tag, timestamp))
                    results = cursor1.fetchall()
                    for result in results:
                        rfield.append(
                            '{} {} {}'.format(result.get('longitude'), result.get('latitude'), result.get('value')))

                write_to_file('{}/wrf/{}/{}/rfield/kelani_basin/{}/{}_{}_{}_rfield.txt'
                              .format(root_directory, version, sim_tag, "future", wrf_model, version,
                                      timestamp.strftime('%Y-%m-%d_%H-%M')), rfield)

                timestamp = datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S') + timedelta(minutes=15)

            while timestamp <= end_time:
                create_rfield(connection=connection, wrf_model=wrf_model, version=version, sim_tag=sim_tag,
                              timestamp=timestamp, past_or_future="future")

                timestamp = datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S') + timedelta(minutes=15)

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()
        print("Process finished")


def usage():
    usageText = """
    Usage: python gen_rfield_kelani_basin_parallelized_optimized.py -m WRF_X1,WRF_X2,WRF_X3 -v vX -s "evening_18hrs"

    -h  --help          Show usage
    -m  --wrf_model     List of WRF models (e.g. WRF_A, WRF_E). Compulsory arg
    -v  --version       WRF model version (e.g. v4, v3). Compulsory arg
    -s  --sim_tag       Simulation tag (e.g. evening_18hrs). Compulsory arg
    """
    print(usageText)


if __name__=="__main__":

    my_pool = None
    try:

        wrf_models = None
        version = None
        sim_tag = None

        try:
            opts, args = getopt.getopt(sys.argv[1:], "h:m:v:s:",
                    ["help", "wrf_model=", "version=", "sim_tag="])
        except getopt.GetoptError:
            usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt in ("-m", "--wrf_model"):
                wrf_models = arg.strip()
            elif opt in ("-v", "--version"):
                version = arg.strip()
            elif opt in ("-s", "--sim_tag"):
                sim_tag = arg.strip()

        print(wrf_models, version, sim_tag)
        print(VALID_MODELS, VALID_VERSIONS, SIM_TAGS)

        # load connection parameters
        config = json.loads(open('/home/uwcc-admin/rfield_extractor/config.json').read())

        # connection params
        HOST = read_attribute_from_config_file('host', config)
        USER = read_attribute_from_config_file('user', config)
        PASSWORD = read_attribute_from_config_file('password', config)
        DB = read_attribute_from_config_file('db', config)
        PORT = read_attribute_from_config_file('port', config)

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

        past_rfield_home = "{}/wrf/{}/{}/rfield/kelani_basin/past".format(root_directory, version, sim_tag)
        try:
            os.makedirs(past_rfield_home)
        except FileExistsError:
            # directory already exists
            pass

        future_rfield_home = "{}/wrf/{}/{}/rfield/kelani_basin/future".format(root_directory, version, sim_tag)
        try:
            os.makedirs(future_rfield_home)
        except FileExistsError:
            # directory already exists
            pass

        mp_pool = mp.Pool(mp.cpu_count())

        results = mp_pool.starmap(gen_rfield_d03_kelani_basin,
                                        [(wrf_model, version, sim_tag) for wrf_model in wrf_model_list])
        # results = mp_pool.starmap_async(gen_rfield_d03_kelani_basin,
        #                           [(wrf_model, version, sim_tag) for wrf_model in wrf_model_list]).get()

        print("results: ", results)

    except Exception as e:
        print('JSON config data loading error.')
        traceback.print_exc()
    finally:
        if my_pool is not None:
            mp_pool.close()




