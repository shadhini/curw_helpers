import pymysql
from datetime import datetime, timedelta
from csv_utils import create_csv, delete_row
import traceback

KUB_Mean = ['b0e008522be904bcf71e290b3b0096b33c3e24d9b623dcbe7e58e7d1cc82d0db','KUB Obs Mean','100034','KUB Obs',7.111666667,80.14983333]


def extract_active_rainfall_obs_stations():
    """
    Extract currently active (active within last week) rainfall obs stations
    :return:
    """
    # Connect to the database
    connection = pymysql.connect(host='104.198.0.87',
            user='root',
            password='cfcwm07',
            db='curw',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    try:
        obs_stations = [['hash_id', 'run_name', 'station_id', 'station_name', 'latitude', 'longitude']]

        # Extract Observed stations and their hash_ids which gives precipitation (total : 59)
        with connection.cursor() as cursor1:
            sql_statement = "SELECT `id` as hash_id, `name`as run_name, `station` as station_id FROM `run` " \
                            "WHERE `variable` = 1 AND `unit` = 1 AND `type` = 1;"
            cursor1.execute(sql_statement)
            results = cursor1.fetchall()

            for result in results:

                start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
                with connection.cursor() as cursor2:
                    sql_statement = "select 1 from `data` where `id`=%s and `time` > %s;"
                    rows = cursor2.execute(sql_statement, (result.get('hash_id'), start_date))

                    if rows > 0 and result.get('station_id') != 100034:  # remove non-active stations and KUB Mean
                        obs_stations.append([result.get('hash_id'), result.get('run_name'), result.get('station_id')])

        for i in range(len(obs_stations) - 1):
            # Extract lat lon of observed stations
            with connection.cursor() as cursor3:
                sql_statement = " select `name`, `latitude`, `longitude` from `station` where `id`=%s;"
                cursor3.execute(sql_statement, obs_stations[i + 1][2])
                result = cursor3.fetchone()
                obs_stations[i + 1].extend([result.get('name'), result.get('latitude'), result.get('longitude')])

        # Write to csv file
        create_csv('all_active_rainfall_obs_stations.csv', obs_stations)

        # delete_row('curw_active_rainfall_obs_stations.csv', match_index=1, match_string='Icharm')

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()


# extract_active_rainfall_obs_stations()

############### to be finished
def extract_active_curw_obs_rainfall_stations():
    """
        Extract currently active (active within last week) rainfall obs stations
        :return:
        """
    # Connect to the database
    connection = pymysql.connect(host='104.198.0.87',
            user='root',
            password='cfcwm07',
            db='curw',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    obs_stations = [['hash_id', 'run_name', 'station_id', 'station_name', 'latitude', 'longitude']]

    try:

        with connection.cursor() as cursor1:
            cursor1.callproc(procname='getActiveRainfallObsStations')
            results = cursor1.fetchall()

            for result in results:

                start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
                with connection.cursor() as cursor2:
                    sql_statement = "select 1 from `data` where `id`=%s and `time` > %s;"
                    rows = cursor2.execute(sql_statement, (result.get('hash_id'), start_date))

                    if rows > 0 and result.get('station_id')!=100034:  # remove non-active stations and KUB Mean
                        obs_stations.append([result.get('hash_id'), result.get('run_name'), result.get('station_id')])

        for i in range(len(obs_stations) - 1):
            # Extract lat lon of observed stations
            with connection.cursor() as cursor3:
                sql_statement = " select `name`, `latitude`, `longitude` from `station` where `id`=%s;"
                cursor3.execute(sql_statement, obs_stations[i + 1][2])
                result = cursor3.fetchone()
                obs_stations[i + 1].extend([result.get('name'), result.get('latitude'), result.get('longitude')])

        # Write to csv file
        create_csv('all_active_rainfall_obs_stations.csv', obs_stations)

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()


extract_active_curw_obs_rainfall_stations()
