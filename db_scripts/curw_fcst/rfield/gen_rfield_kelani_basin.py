import traceback
import pymysql
import json
import getopt
import sys
import os
from datetime import datetime, timedelta

# connection params
HOST = ""
USER = ""
PASSWORD = ""
DB =""
PORT = ""

VALID_MODELS = ["WRF_A", "WRF_C", "WRF_E", "WRF_SE"]
VALID_VERSIONS = ["v3", "v4"]


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


#############################
# Raw WRF RFIELD GENERATION #
#############################

def gen_rfield_d03_kelani_basin(model, version, sim_tag="evening_18hrs"):

    # Connect to the database
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB,
            cursorclass=pymysql.cursors.DictCursor)

    start_time = ''
    end_time = ''

    now = datetime.strptime((datetime.now()+timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S')

    try:

        # Extract timeseries start time and end time
        with connection.cursor() as cursor1:
            cursor1.callproc('get_TS_start_end', (model, version))
            result = cursor1.fetchone()
            start_time = result.get('start')
            end_time = result.get('end')

        if end_time > (now + timedelta(days=1)):
            # Extract rfields
            timestamp = start_time
            while timestamp <= end_time :
                # rfield = [['latitude', 'longitude', 'rainfall']]
                rfield = []
                with connection.cursor() as cursor2:
                    cursor2.callproc('get_d03_rfield_kelani_basin_rainfall', (model, version, sim_tag, timestamp))
                    results = cursor2.fetchall()
                    for result in results:
                        rfield.append('{} {} {}'.format(result.get('longitude'), result.get('latitude'), result.get('value')))

                if timestamp < now:
                    write_to_file('/mnt/disks/wrf_nfs/wrf/{}/rfield/kelani_basin/past/{}_{}_{}_rfield.txt'.format(version, model, version, timestamp), rfield)
                else:
                    write_to_file('/mnt/disks/wrf_nfs/wrf/{}/rfield/kelani_basin/future/{}_{}_{}_rfield.txt'.format(version, model, version, timestamp), rfield)

                timestamp = datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S') + timedelta(minutes=15)

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()
        print("Process finished")


#############################
# MME WRF RFIELD GENERATION #
#############################

def average_timeseries(timeseries):
    """
    Give the timeseries with avg of 2 model values
    :param timeseries: input timeseries e.g. list of lists like [longitude, latitude, model1_value, model2_value]
    :return: list of lists like [longitude, latitude, avg_value]
    """
    avg_timeseries = []

    for i in range(len(timeseries)):
        avg_timeseries.append("{} {} {}".format(timeseries[i][0], timeseries[i][1], '%.3f' % ((timeseries[i][2]+timeseries[i][3])/2)))

    return avg_timeseries


def gen_MME_rfield_d03_kelani_basin(model1, version1, model2, version2):

    # Connect to the database
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB,
            cursorclass=pymysql.cursors.DictCursor)

    start_time = ''
    end_time = ''

    now = datetime.strptime((datetime.now()+timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S')

    try:

        # Extract timeseries start time and end time
        with connection.cursor() as cursor1:
            cursor1.callproc('get_TS_start_end', (model1, version1))
            # parameters are given to above procedure assuming all data of models in model_list are included in
            # one netcdf file and have same start, end timestamps
            result = cursor1.fetchone()
            start_time = result.get('start')
            end_time = result.get('end')

        if end_time > (now + timedelta(days=1)):
            # Extract rfields
            timestamp = start_time
            while timestamp <= end_time :
                # rfield = [['latitude', 'longitude', 'rainfall']]
                rfield = []

                temp_rfield = []

                with connection.cursor() as cursor2:
                    cursor2.callproc('get_d03_rfield_kelani_basin_rainfall', (model1, version1, timestamp))
                    results = cursor2.fetchall()
                    for result in results:
                        temp_rfield.append([result.get('longitude'), result.get('latitude'), result.get('value')])

                with connection.cursor() as cursor3:
                    cursor3.callproc('get_d03_rfield_kelani_basin_rainfall', (model2, version2, timestamp))
                    results = cursor3.fetchall()
                    count = 0
                    for result in results:
                        # this value is appended assuming all output generated by the procedure call (sorts according to
                        # the lon lat) are in same order
                        temp_rfield[count].append(result.get('value'))
                        count += 1

                rfield = average_timeseries(temp_rfield)

                if timestamp < now:
                    write_to_file('/mnt/disks/wrf_nfs/wrf/v4/rfield/kelani_basin/past/WRF_MME_v4_{}_rfield.txt'.format(timestamp), rfield)
                else:
                    write_to_file('/mnt/disks/wrf_nfs/wrf/v4/rfield/kelani_basin/future/WRF_MME_v4_{}_rfield.txt'.format(timestamp), rfield)

                timestamp = datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S') + timedelta(minutes=15)

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()
        print("Process finished")


def usage():
    usageText = """
    Usage: ./gen_rfield_kelani_basin.py -m WRF_X -v vX

    -h  --help          Show usage
    -m  --wrf_model     WRF model (e.g. WRF_A, WRF_E). Compulsory arg
    -v  --version       WRF model version (e.g. v4, v3). Compulsory arg
    """
    print(usageText)


if __name__=="__main__":

    try:

        wrf_model = None
        version = None

        try:
            opts, args = getopt.getopt(sys.argv[1:], "h:m:v:",
                    ["help", "wrf_model=", "version="])
        except getopt.GetoptError:
            usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt in ("-m", "--wrf_model"):
                wrf_model = arg.strip()
            elif opt in ("-v", "--version"):
                version = arg.strip()

        # load connection parameters
        config = json.loads(open('/home/uwcc-admin/rfield_extractor/config.json').read())

        # connection params
        HOST = read_attribute_from_config_file('host', config)
        USER = read_attribute_from_config_file('user', config)
        PASSWORD = read_attribute_from_config_file('password', config)
        DB = read_attribute_from_config_file('db', config)
        PORT = read_attribute_from_config_file('port', config)

        if wrf_model is None or wrf_model not in VALID_MODELS:
            usage()
            exit(1)
        if version is None or version not in VALID_VERSIONS:
            usage()
            exit(1)

        try:
            os.system("rm /mnt/disks/wrf_nfs/wrf/{}/rfield/kelani_basin/past/{}_{}_*".format(version, wrf_model, version))
            os.system("rm /mnt/disks/wrf_nfs/wrf/{}/rfield/kelani_basin/future/{}_{}_*".format(version, wrf_model, version))
        except Exception as e:
            traceback.print_exc()

        gen_rfield_d03_kelani_basin(wrf_model, version)

        # gen_MME_rfield_d03_kelani_basin(model1="WRF_E", version1="v4", model2="WRF_SE", version2="v4")

    except Exception as e:
        print('JSON config data loading error.')
        traceback.print_exc()

