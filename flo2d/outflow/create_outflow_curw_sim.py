#!"D:\outflow\venv\Scripts\python.exe"
import pymysql
from datetime import datetime, timedelta
import traceback
import json
import os
import sys
import getopt

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

from db_adapter.base import get_Pool, destroy_Pool
from db_adapter.constants import CURW_SIM_DATABASE, CURW_SIM_HOST, CURW_SIM_PASSWORD, CURW_SIM_PORT, CURW_SIM_USERNAME
from db_adapter.curw_sim.timeseries.tide import Timeseries as TideTS
from db_adapter.constants import COMMON_DATE_TIME_FORMAT


def write_to_file(file_name, data):
    with open(file_name, 'w+') as f:
        f.write('\n'.join(data))


def append_to_file(file_name, data):
    with open(file_name, 'a+') as f:
        f.write('\n'.join(data))


def append_file_to_file(file_name, file_content):
    with open(file_name, 'a+') as f:
        f.write('\n')
        f.write(file_content)


def read_attribute_from_config_file(attribute, config, compulsory=False):
    """
    :param attribute: key name of the config json file
    :param config: loaded json file
    :param compulsory: Boolean value: whether the attribute is must present or not in the config file
    :return:

    """
    if attribute in config and (config[attribute] != ""):
        return config[attribute]
    elif compulsory:
        print("{} not specified in config file.".format(attribute))
        exit(1)
    else:
        print("{} not specified in config file.".format(attribute))
        return None


def check_time_format(time):
    try:
        time = datetime.strptime(time, DATE_TIME_FORMAT)

        if time.strftime('%S') != '00':
            print("Seconds should be always 00")
            exit(1)
        if time.strftime('%M') != '00':
            print("Minutes should be always 00")
            exit(1)

        return True
    except Exception:
        print("Time {} is not in proper format".format(time))
        exit(1)


def prepare_outflow_250(outflow_file_path, start, end, tide_id):


    try:

        curw_sim_pool = get_Pool(host=CURW_SIM_HOST, user=CURW_SIM_USERNAME, password=CURW_SIM_PASSWORD, port=CURW_SIM_PORT,
                                 db=CURW_SIM_DATABASE)

        TS = TideTS(pool=curw_sim_pool)
        tide_ts = TS.get_timeseries(id_=tide_id, start_date=start, end_date=end)

        tide_data = []
        timeseries = tide_ts
        for i in range(len(timeseries)):
            time_col = (str('%.3f' % (((timeseries[i][0] - timeseries[0][0]).total_seconds()) / 3600))).rjust(16)
            value_col = (str('%.3f' % (timeseries[i][1]))).rjust(16)
            tide_data.append('S' + time_col + value_col)

        outflow = []

        outflow.append('K              91')
        outflow.append('K             171')
        outflow.append('K             214')
        outflow.append('K             491')

        outflow.append('N             134               1')
        outflow.extend(tide_data)

        outflow.append('N             220               1')
        outflow.extend(tide_data)

        outflow.append('N             261               1')
        outflow.extend(tide_data)

        outflow.append('N             558               1')
        outflow.extend(tide_data)

        write_to_file(outflow_file_path, data=outflow)

        tail_file = open("tail_250.txt", "r")
        tail = tail_file.read()
        tail_file.close()

        append_file_to_file(outflow_file_path, file_content=tail)

    except Exception as e:
        print(traceback.print_exc())
    finally:
        destroy_Pool(curw_sim_pool)
        print("Outflow generated")


def prepare_outflow_150(outflow_file_path, start, end, tide_id):


    try:

        curw_sim_pool = get_Pool(host=CURW_SIM_HOST, user=CURW_SIM_USERNAME, password=CURW_SIM_PASSWORD, port=CURW_SIM_PORT,
                                 db=CURW_SIM_DATABASE)

        TS = TideTS(pool=curw_sim_pool)
        tide_ts = TS.get_timeseries(id_=tide_id, start_date=start, end_date=end)

        tide_data = []
        timeseries = tide_ts
        for i in range(len(timeseries)):
            time_col = (str('%.3f' % (((timeseries[i][0] - timeseries[0][0]).total_seconds()) / 3600))).rjust(16)
            value_col = (str('%.3f' % (timeseries[i][1]))).rjust(16)
            tide_data.append('S' + time_col + value_col)

        outflow = []

        outflow.append('K             290')
        outflow.append('K             416')
        outflow.append('K             488')
        outflow.append('K            1218')

        outflow.append('N             356               1')
        outflow.extend(tide_data)

        outflow.append('N             497               1')
        outflow.extend(tide_data)

        outflow.append('N            1330               1')
        outflow.extend(tide_data)

        write_to_file(outflow_file_path, data=outflow)

        tail_file = open("tail_150.txt", "r")
        tail = tail_file.read()
        tail_file.close()

        append_file_to_file(outflow_file_path, file_content=tail)

    except Exception as e:
        print(traceback.print_exc())
    finally:
        destroy_Pool(curw_sim_pool)
        print("Outflow generated")


def create_dir_if_not_exists(path):
    """
    create directory(if needed recursively) or paths
    :param path: string : directory path
    :return: string
    """
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def usage():
    usageText = """
    Usage: .\gen_outflow.py [-m flo2d_XXX] [-s "YYYY-MM-DD HH:MM:SS"] [-e "YYYY-MM-DD HH:MM:SS"]

    -h  --help          Show usage
    -m  --model         FLO2D model (e.g. flo2d_250, flo2d_150). Default is flo2d_250.
    -s  --start_time    Outflow start time (e.g: "2019-06-05 00:00:00"). Default is 00:00:00, 2 days before today.
    -e  --end_time      Outflow end time (e.g: "2019-06-05 23:00:00"). Default is 00:00:00, tomorrow.
    """
    print(usageText)


if __name__ == "__main__":

    try:

        print("started creating outflow")
        start_time = None
        end_time = None
        flo2d_model = None

        try:
            opts, args = getopt.getopt(sys.argv[1:], "h:m:s:e:",
                                       ["help", "flo2d_model=", "start_time=", "end_time="])
        except getopt.GetoptError:
            usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt in ("-m", "--flo2d_model"):
                flo2d_model = arg.strip()
            elif opt in ("-s", "--start_time"):
                start_time = arg.strip()
            elif opt in ("-e", "--end_time"):
                end_time = arg.strip()

        # Load config details and db connection params
        config = json.loads(open('config.json').read())

        output_dir = read_attribute_from_config_file('output_dir', config)
        file_name = read_attribute_from_config_file('output_file_name', config)

        tide_id = read_attribute_from_config_file('tide_id', config, True)

        if flo2d_model is None:
            flo2d_model = "flo2d_250"
        elif flo2d_model not in ("flo2d_250", "flo2d_150"):
            print("Flo2d model should be either \"flo2d_250\" or \"flo2d_150\"")
            exit(1)

        if start_time is None:
            start_time = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d 00:00:00')
        else:
            check_time_format(time=start_time)

        if end_time is None:
            end_time = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
        else:
            check_time_format(time=end_time)

        if output_dir is not None and file_name is not None:
            outflow_file_path = os.path.join(output_dir, file_name)
        else:
            outflow_file_path = os.path.join(r"D:\outflow",
                                          '{}_{}_{}_{}.DAT'.format(file_name, flo2d_model, start_time, end_time).replace(' ', '_').replace(':', '-'))

        if not os.path.isfile(outflow_file_path):
            print("{} start preparing outflow".format(datetime.now()))
            if flo2d_model == "flo2d_250":
                prepare_outflow_250(outflow_file_path, start=start_time, end=end_time, tide_id=tide_id)
            elif flo2d_model == "flo2d_150":
                prepare_outflow_150(outflow_file_path, start=start_time, end=end_time, tide_id=tide_id)
            print("{} completed preparing outflow".format(datetime.now()))
        else:
            print('Outflow file already in path : ', outflow_file_path)

        # os.system(r"deactivate")

    except Exception:
        traceback.print_exc()

