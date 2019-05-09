import pymysql
import traceback
import csv
import operator
import collections

from math import acos, cos, sin, radians


from csv_utils import read_csv, create_csv, append_csv


obs_station_names = ['curw_kitulgala','curw_hingurana','curw_orugodawatta','curw_mahapallegama','curw_jaffna',
                     'curw_uduwawala','curw_kottawa_dharmapala_north','curw_IBATTARA2','curw_waga','curw_ambewela',
                     'curw_kotikawatta','curw_mulleriyawa','curw_malabe','curw_dickoya','curw_mutwal','curw_urumewella',
                     'curw_kohuwala','curw_attidiya','gov_irr_canyon','gov_irr_castlereigh']


def extract_obs_stations():
    """
    Extract obs stations
    :param connection: connection to curw database
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
        obs_stations = [['id', 'latitude', 'longitude']]
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


def find_nearest_obs_stations_for_flo2d_stations(flo2d_stations_csv, obs_stations_csv):

    obs_stations = read_csv(obs_stations_csv)[1:]

    flo2d_station = read_csv(flo2d_stations_csv)[1:]

    flo2d_obs_mapping_list = [['flo2d_250_station_id', 'ob_1_id', 'ob_2_id', 'ob_3_id', 'ob_4_id', 'ob_5_id', 'ob_6_id', 'ob_7_id', 'ob_8_id', 'ob_9_id', 'ob_10_id']]

    for flo2d_index in range(len(flo2d_station)):

        flo2d_obs_mapping = [flo2d_station[flo2d_index][0]]

        flo2d_lat = float(flo2d_station[flo2d_index][2])
        flo2d_lng = float(flo2d_station[flo2d_index][1])

        distances = {}

        for obs_index in range(len(obs_stations)):
            lat = float(obs_stations[obs_index][2])
            lng = float(obs_stations[obs_index][3])
            distance = acos(cos(radians(flo2d_lat)) * cos(radians(lat)) * cos(radians(lng) - radians(flo2d_lng)) + sin(radians(flo2d_lat)) * sin(radians(lat)))

            distances[obs_stations[obs_index][0]]=distance

        sorted_distances = collections.OrderedDict(sorted(distances.items(), key=operator.itemgetter(1))[:10])

        for key in sorted_distances.keys():
            flo2d_obs_mapping.append(key)

        print(flo2d_obs_mapping)
        flo2d_obs_mapping_list.append(flo2d_obs_mapping)

    create_csv('flo2d_250_obs_mapping.csv', flo2d_obs_mapping_list)





find_nearest_obs_stations_for_flo2d_stations('flo2d_250m_dd.csv','obs_stations.csv')
