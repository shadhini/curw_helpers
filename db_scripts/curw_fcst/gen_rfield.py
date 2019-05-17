import traceback
import pymysql


def load_kelani_basin_d03_grids():
    # Connect to the database
    connection = pymysql.connect(host='35.230.102.148',
            user='root',
            password='cfcwm07',
            db='curw_fcst',
            cursorclass=pymysql.cursors.Cursor)

    try:
        id_set = [['id', 'latitude', 'longitude']]
        station_names = []

        # Extract Observed station names which gives precipitation (total : 45)
        with connection.cursor() as cursor1:
            sql_statement = "select distinct `station` from `run_view` where `type`=%s and `variable`=%s"
            cursor1.execute(sql_statement, ("Observed", "Precipitation"))
            results = cursor1.fetchall()
            for result in results:
                station_names.append(result.get('station'))

        # Extract lat lon of observed stations
        with connection.cursor() as cursor2:
            sql_statement = "select `id`, `latitude`, `longitude` from `station` where `name` in %s"
            cursor2.execute(sql_statement, tuple(station_names))
            results = cursor2.fetchall()
            obs_station = []
            for result in results:
                obs_station.extend([result.get('id'), result.get('latitude'), result.get('longitude')])
            obs_stations.append(obs_station)

        # Write to csv file
        with open('obs_stations.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(obs_stations)

        csvFile.close()

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()


def gen_rfield_d03_kelani_basin():
    return