import pymysql
from datetime import datetime, timedelta
from csv_utils import create_csv
import traceback


def extract_wrf0_stations_curw():
    """
    Extract wrf0 stations from curw database
    :return:
    """
    # Connect to the database
    connection = pymysql.connect(host='104.198.0.87',
            user='',
            password='',
            db='curw',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    try:
        wrf0_stations = [['id', 'latitude', 'longitude']]

        # Extract wrf0 stations
        with connection.cursor() as cursor1:
            sql_statement = "select `id`, `latitude`, `longitude` from `station` " \
                            "where name like 'wrf$_%' ESCAPE '$' and name not like 'wrf$_v3%' ESCAPE '$';"
            cursor1.execute(sql_statement)
            results = cursor1.fetchall()

            for result in results:
                wrf0_stations.append([result.get('id'), result.get('latitude'), result.get('longitude')])

        # Write to csv file
        create_csv('wrf0_stations_curw.csv', wrf0_stations)

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()


extract_wrf0_stations_curw()
