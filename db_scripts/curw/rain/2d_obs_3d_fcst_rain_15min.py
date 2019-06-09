import traceback
import pymysql
from datetime import datetime, timedelta
import csv


def datetime_utc_to_lk(timestamp_utc, shift_mins=0):
    return timestamp_utc + timedelta(hours=5, minutes=30 + shift_mins)


def create_csv_like_txt(file_name, data):
    """
    Create txt file in the format of csv file
    :param file_name: file_path/file_name
    :param data: list of lists
    :return:
    """
    with open(file_name, 'w') as f:
        for _list in data:
            for i in range(len(_list)-1):
                #f.seek(0)
                f.write(str(_list[i]) + ',')
            f.write(str(_list[len(_list)-1]))
            f.write('\n')

        f.close()


def read_csv(file_name):
    """
    Read csv file
    :param file_name: <file_path/file_name>.csv
    :return: list of lists which contains each row of the csv file
    """

    with open(file_name, 'r') as f:
        data = [list(line) for line in csv.reader(f)][1:]

    return data


def extract_rain_obs(connection, stations_dict, start_time, end_time):
    """
    Extract obs station timeseries (15 min intervals)
    :param connection: connection to curw database
    :param stations_dict: dictionary with station_id as keys and run_ids as values
    :param start_time: start of timeseries
    :param end_time: end time of timeseries
    :return:
    """

    obs_timeseries = { }

    try:
        # Extract per 15 min observed timeseries
        for station in stations_dict.keys():
            with connection.cursor() as cursor1:
                sql_statement = "select max(time) as time, sum(value) as value from data " \
                                "where `id`=%s and `time` between %s and %s " \
                                "group by floor((HOUR(TIMEDIFF(`time`, %s))*60+MINUTE(TIMEDIFF(`time`, %s))-1)/15);"
                rows = cursor1.execute(sql_statement,
                        (stations_dict.get(station), start_time, end_time, start_time, start_time))
                if rows > 0:
                    results = cursor1.fetchall()
                    ts = []
                    for result in results:
                        ts.append([result.get('time'), result.get('value')])

                    obs_timeseries[station] = ts

        return obs_timeseries

    except Exception as ex:
        traceback.print_exc()
    # finally:
    #     connection.close()


def extract_wrf0_rain_fcst(connection, station_dict, start_time, end_time, type):
    """
        Extract obs station timeseries (15 min intervals)
        :param connection: connection to curw database
        :param station_dict: dictionary with observed station id as keys and mapping wrf0 station id as the value
        :param start_time: start of timeseries
        :param end_time: end time of timeseries
        :param type: whether 0-d/1-d/2-d forecast
        :return:
        """

    forecast_timeseries = {}

    try:
        # Extract per 1 hour wrf0 forecasted timeseries
        for station in station_dict.keys():

            with connection.cursor() as cursor1:
                sql_statement = "select id from run where name='Cloud-1' and variable=1 and unit=1  and source=8 and " \
                                "station=%s and type=%s;"
                cursor1.execute(sql_statement, (station_dict.get(station), type))
                id = cursor1.fetchone()['id']

            with connection.cursor() as cursor2:
                sql_statement = "select time, value from data where `id`=%s and `time` between %s and %s;"
                cursor2.execute(sql_statement, (id, start_time, end_time))
                results = cursor2.fetchall()

                ts = []
                for result in results:
                    ts.append([result.get('time'), result.get('value')])

                forecast_timeseries[station] = ts

        return forecast_timeseries

    except Exception as ex:
        traceback.print_exc()
    # finally:
    #     connection.close()


def extract_15_min_timeseries(timeseries, MIKE_INPUT, current_row, index):

    dict = {}

    MIKE_INPUT = MIKE_INPUT
    current_row = current_row
    i = 0

    if (timeseries[0][0] + timedelta(hours=1))==timeseries[1][0]:  # hourly series

        print("hourly series")
        while i < len(timeseries):
            if len(MIKE_INPUT[current_row]) == index:  # skip overwriting existing values
                if (datetime.strptime(MIKE_INPUT[current_row][0], '%Y-%m-%d %H:%M:%S') + timedelta(minutes=59)).strftime('%Y-%m-%d %H:00:00') == (timeseries[i][0]).strftime('%Y-%m-%d %H:00:00'):
                    MIKE_INPUT[current_row].append(timeseries[i][1] / 4)
                    current_row += 1
                # time entry is not matching
                elif MIKE_INPUT[current_row][0] < (timeseries[i][0]).strftime('%Y-%m-%d %H:%M:%S'):
                    current_row += 1
                else:
                    i += 1
                    continue
            else:
                current_row +=1

    elif (timeseries[1][0] + timedelta(minutes=15))==timeseries[2][0]:  # 15 min periodical series
        print("15 min series")
        for i in range(len(timeseries)):
            if len(MIKE_INPUT[current_row])==index:  # skip overwriting existing values
                if MIKE_INPUT[current_row][0]==(timeseries[i][0]).strftime('%Y-%m-%d %H:%M:%S'):
                    MIKE_INPUT[current_row].append(timeseries[i][1])
                    current_row += 1
                    # time entry is not matching
                elif MIKE_INPUT[current_row][0] < (timeseries[i][0]).strftime('%Y-%m-%d %H:%M:%S'):
                    current_row += 1
                else:
                    i += 1
                    continue
            else:
                current_row += 1

    dict['MIKE_INPUT'] = MIKE_INPUT
    dict['current_row'] = current_row

    return dict


def generate_mike_input(active_obs_stations_file, obs_wrf0_mapping_file):

    types = [16, 17, 18]
    now = datetime_utc_to_lk(datetime.now())
    obs_start = (now - timedelta(days=2)).strftime('%Y-%m-%d 00:00:00')
    obs_end = now.strftime('%Y-%m-%d %H:%M:%S')
    d0_forecast_start = (now - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
    d0_forecast_end = (now + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
    d1_forecast_start = d0_forecast_end
    d1_forecast_end = (now + timedelta(days=2)).strftime('%Y-%m-%d 00:00:00')
    d2_forecast_start = d1_forecast_end
    d2_forecast_end = (now + timedelta(days=3)).strftime('%Y-%m-%d 00:00:00')

    try:
        # Connect to the database
        connection = pymysql.connect(host='104.198.0.87',
                user='root',
                password='cfcwm07',
                db='curw',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

        print("{} : Read active obs stations and obs wrf0 station mapping from CSVs".format(datetime.now()))
        active_obs_stations = read_csv(active_obs_stations_file)
        obs_wrf0_mapping = read_csv(obs_wrf0_mapping_file)

        stations_dict_for_obs={}  # keys: obs station id , value: hash id

        for obs_index in range(len(active_obs_stations)):
            stations_dict_for_obs[active_obs_stations[obs_index][2]] = active_obs_stations[obs_index][0]

        print("{} : Pull obs timeseries from db".format(datetime.now()))
        obs_timeseries = extract_rain_obs(connection=connection, stations_dict=stations_dict_for_obs,
                start_time=obs_start, end_time=obs_end)

        stations_dict_for_fcst={}  # keys: obs station id , value: nearest wrf0 station id

        for obs_index in range(len(obs_wrf0_mapping)):
            stations_dict_for_fcst[obs_wrf0_mapping[obs_index][0]] = obs_wrf0_mapping[obs_index][2]

        print("{} : Pull 0-d forecast timeseries from db".format(datetime.now()))
        d0_wrf0_fcst_timeseries = extract_wrf0_rain_fcst(connection=connection, station_dict=stations_dict_for_fcst,
                start_time=d0_forecast_start, end_time=d0_forecast_end, type=16)

        print("{} : Pull 1-d forecast timeseries from db".format(datetime.now()))
        d1_wrf0_fcst_timeseries = extract_wrf0_rain_fcst(connection=connection, station_dict=stations_dict_for_fcst,
                start_time=d1_forecast_start, end_time=d1_forecast_end, type=17)

        print("{} : Pull 2-d forecast timeseries from db".format(datetime.now()))
        d2_wrf0_fcst_timeseries = extract_wrf0_rain_fcst(connection=connection, station_dict=stations_dict_for_fcst,
                start_time=d2_forecast_start, end_time=d2_forecast_end, type=18)

        # format MIKE input
        MIKE_INPUT = [['time']]

        print("{} : Initialize MIKE INPUT".format(datetime.now()))
        ordered_station_ids = []
        for obs_index in range(len(obs_wrf0_mapping)):
            MIKE_INPUT[0].append(obs_wrf0_mapping[obs_index][1])
            ordered_station_ids.append(obs_wrf0_mapping[obs_index][0])

        timestamp = obs_start
        while timestamp <= d2_forecast_end :
            MIKE_INPUT.append([timestamp])
            timestamp = (datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')

        for column in range(len(ordered_station_ids)):
        # for column in range(1):
            print ('station : ', ordered_station_ids[column])
            obs = obs_timeseries.get(ordered_station_ids[column])
            d0_wrf0_fcst = d0_wrf0_fcst_timeseries.get(ordered_station_ids[column])
            d1_wrf0_fcst = d1_wrf0_fcst_timeseries.get(ordered_station_ids[column])
            d2_wrf0_fcst = d2_wrf0_fcst_timeseries.get(ordered_station_ids[column])

            current_row = 1

            print("{} : Add obs timeseries to MIKE INPUT".format(datetime.now()))
            if obs is not None and len(obs) > 0:
                obs_output_dict = extract_15_min_timeseries(timeseries=obs, MIKE_INPUT=MIKE_INPUT,
                        current_row=current_row, index=column+1)
                MIKE_INPUT = obs_output_dict.get('MIKE_INPUT')
                current_row = obs_output_dict.get('current_row')

            current_row = 1

            print("{} : Add 0-d forecast timeseries to MIKE INPUT".format(datetime.now()))
            if d0_wrf0_fcst is not None and len(d0_wrf0_fcst) > 0:
                d0_fcst_output_dict = extract_15_min_timeseries(timeseries=d0_wrf0_fcst, MIKE_INPUT=MIKE_INPUT,
                        current_row=current_row, index=column+1)
                MIKE_INPUT = d0_fcst_output_dict.get('MIKE_INPUT')
                current_row = d0_fcst_output_dict.get('current_row')

            print("{} : Add 1-d forecast timeseries to MIKE INPUT".format(datetime.now()))
            if d1_wrf0_fcst is not None and len(d1_wrf0_fcst) > 0:
                d1_fcst_output_dict = extract_15_min_timeseries(timeseries=d1_wrf0_fcst, MIKE_INPUT=MIKE_INPUT,
                        current_row=current_row, index=column+1)
                MIKE_INPUT = d1_fcst_output_dict.get('MIKE_INPUT')
                current_row = d1_fcst_output_dict.get('current_row')

            print("{} : Add 2-d forecast timeseries to MIKE INPUT".format(datetime.now()))
            if d2_wrf0_fcst is not None and len(d2_wrf0_fcst) > 0:
                d2_fcst_output_dict = extract_15_min_timeseries(timeseries=d2_wrf0_fcst, MIKE_INPUT=MIKE_INPUT,
                        current_row=current_row, index=column+1)
                MIKE_INPUT = d2_fcst_output_dict.get('MIKE_INPUT')
                current_row = d2_fcst_output_dict.get('current_row')

            for i in range(len(MIKE_INPUT)-1):
                if len(MIKE_INPUT[i+1]) < (column + 2):
                    for j in range((column + 2) - len(MIKE_INPUT[i+1])):
                        MIKE_INPUT[i+1].append('')

        create_csv_like_txt('/mnt/disks/cms-data/cfcwm/data/MIKE/RF/mike_kelani_{}.txt'.format(now.strftime('%Y-%m-%d_%H-00-00')), MIKE_INPUT)

    except Exception as e:
        print(traceback.print_exc())
    finally:
        connection.close()
        print("Rain file generation process finished.")


generate_mike_input('all_active_rainfall_obs_stations.csv', 'obs_wrf0_stations_mapping.csv')

