import traceback
import pymysql
from csv_utils import create_csv, read_csv, delete_row


# All Rainfall Obs Stations :: variable=Precipitation, unit=mm|Accumulative, type=Observed
# Output: hashid, run name, stationid, station name, latitude, longitude
sql1 = "select id from run where station=100046 and variable=1 and unit=1 and type=1;"

sql2 = """SELECT 
    run_selected.id, run_selected.name, run_selected.station, station.name, station.latitude, station.longitude
FROM
    (SELECT 
        run.id, run.name, run.station
    FROM
        run
    WHERE
        variable = 1 AND unit = 1 AND type = 1) AS run_selected
        LEFT JOIN
    station ON run_selected.station = station.id
;"""

# Retrieve observed timeseries with per 15 mins cumulative data
# sql3 = "select max(time) as time, sum(value) as value from data where id="0af5ecec986be44699e267415799b8b349eeb4e4925881a9fad5cf47fa8f3019" and time > "2019-05-27" group by floor((HOUR(TIMEDIFF(time, "2019-05-27 00:00:00"))*60+MINUTE(TIMEDIFF(time, "2019-05-27 00:00:00"))-1)/15);"
sql3 = """select max(time) as time, sum(value) as value from data 
where `id`=%s and `time` between %s and %s group by 
floor((HOUR(TIMEDIFF(`time`, %s))*60+MINUTE(TIMEDIFF(time, %s))-1)/15);"""

# WRF0 forecast 0-day data ::
sql4 = "select id from run where variable=1 and unit=1 and type=16 and station=1100455;"


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
    finally:
        connection.close()


def extract_wrf0_rain_fcst(connection, station_list, start_time, end_time):
    """
        Extract obs station timeseries (15 min intervals)
        :param connection: connection to curw database
        :param station_list: list of obs station ids
        :param start_time: start of timeseries
        :param end_time: end time of timeseries
        :return:
        """

    forecast_timeseries = {}
    types = [16, 17, 18]

    try:
        # Extract per 15 min observed timeseries
        for station in station_list.keys():

            for type in types:
                with connection.cursor() as cursor1:
                    sql_statement = "select max(time) as time, sum(value) as value from data where " \
                                    "`id`=%s and `time` between %s and %s " \
                                    "group by date(time), hour(time), floor(minute(addtime(time, `-00:01:00`))/15);"
                    rows = cursor1.execute(sql_statement, (station_list.get(station), start_time, end_time))
                    if rows > 0:
                        results = cursor1.fetchall()
                        ts = []
                        for result in results:
                            ts.append([result.get('time'), result.get('value')])

                        # obs_timeseries[station] = ts

        # return obs_timeseries

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()


def extract_active_rainfall_obs_stations():
    return


def generate_mike_input(active_obs_stations_file, start_time, end_time):
    # Connect to the database
    connection = pymysql.connect(host='104.198.0.87',
            user='root',
            password='cfcwm07',
            db='curw',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    active_obs_stations = read_csv(active_obs_stations_file)

    stations_dict={}

    for obs_index in range(len(active_obs_stations)):
        stations_dict[active_obs_stations[obs_index][2]] = active_obs_stations[obs_index][0]

    obs_timeseries = extract_rain_obs(connection=connection, stations_dict=stations_dict,
            start_time=start_time, end_time=end_time)

    for obs_index in range(len(active_obs_stations)):
        data = [['time', 'value']]
        station_id = active_obs_stations[obs_index][2]
        for i in range(len(obs_timeseries[station_id])):
            data.append(obs_timeseries[station_id][i])
        create_csv('{}_{}_{}_{}'.format(active_obs_stations[obs_index][3], active_obs_stations[obs_index][1],
                start_time, end_time), data)


def generate_rain_files(active_obs_stations_file, start_time, end_time):
    # Connect to the database
    connection = pymysql.connect(host='104.198.0.87',
            user='root',
            password='cfcwm07',
            db='curw',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    active_obs_stations = read_csv(active_obs_stations_file)

    stations_dict={}

    for obs_index in range(len(active_obs_stations)):
        stations_dict[active_obs_stations[obs_index][2]] = active_obs_stations[obs_index][0]

    obs_timeseries = extract_rain_obs(connection=connection, stations_dict=stations_dict,
            start_time=start_time, end_time=end_time)

    for obs_index in range(len(active_obs_stations)):
        data = [['time', 'value']]
        station_id = active_obs_stations[obs_index][2]
        for i in range(len(obs_timeseries[station_id])):
            data.append(obs_timeseries[station_id][i])
        create_csv('{}_{}_{}_{}'.format(active_obs_stations[obs_index][3], active_obs_stations[obs_index][1],
                start_time, end_time), data)


# generate_rain_files('active_rainfall_obs_stations.csv', "2019-05-22 23:45:00", "2019-05-25 23:30:00")
