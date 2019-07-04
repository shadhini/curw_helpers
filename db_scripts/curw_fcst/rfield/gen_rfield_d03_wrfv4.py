import traceback
import pymysql
import json
from datetime import datetime, timedelta


# connection params
HOST = ""
USER = ""
PASSWORD = ""
DB =""
PORT = ""


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


def gen_rfield_d03(model, version):
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

        # Extract rfields
        timestamp = start_time
        while timestamp <= end_time :
            # rfield = [['latitude', 'longitude', 'rainfall']]
            rfield = []
            with connection.cursor() as cursor2:
                cursor2.callproc('get_d03_rfield', (model, version, timestamp))
                results = cursor2.fetchall()
                for result in results:
                    rfield.append('{} {} {}'.format(result.get('longitude'), result.get('latitude'), result.get('value')))

            if timestamp < now:
                write_to_file('/var/www/html/wrf/{}/rfield/d03/past/{}_{}_{}_rfield.txt'.format(version, model, version, timestamp), rfield)
            else:
                write_to_file('/var/www/html/wrf/{}/rfield/d03/future/{}_{}_{}_rfield.txt'.format(version, model, version, timestamp), rfield)

            timestamp = datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S') + timedelta(minutes=15)

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()
        print("Process finished")


if __name__=="__main__":

    try:

        config = json.loads(open('config.json').read())

        # connection params
        HOST = read_attribute_from_config_file('host', config)
        USER = read_attribute_from_config_file('user', config)
        PASSWORD = read_attribute_from_config_file('password', config)
        DB = read_attribute_from_config_file('db', config)
        PORT = read_attribute_from_config_file('port', config)

        gen_rfield_d03("WRF_A", "v4")
        gen_rfield_d03("WRF_C", "v4")
        gen_rfield_d03("WRF_E", "v4")
        gen_rfield_d03("WRF_SE", "v4")

    except Exception as e:
        print('JSON config data loading error.')
        traceback.print_exc()


