import pymysql
import traceback
import csv
import operator
import collections

from math import acos, cos, sin, radians


# from csv_utils import read_csv, create_csv, append_csv
def create_csv(file_name, data):
    """
    Create new csv file using given data
    :param file_name: <file_path/file_name>.csv
    :param data: list of lists
    e.g. [['Person', 'Age'], ['Peter', '22'], ['Jasmine', '21'], ['Sam', '24']]
    :return:
    """
    with open(file_name, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)


def append_csv(file_name, row):
    """
    Append existing csv file using given data
    :param file_name: <file_path/file_name>.csv
    :param row: list of row data
    e.g. ['Jasmine', '21']
    :return:
    """
    with open(file_name, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)


def read_csv(file_name):
    """
    Read csv file
    :param file_name: <file_path/file_name>.csv
    :return: list of lists which contains each row of the csv file
    """

    with open(file_name, 'r') as f:
        data = [list(line) for line in csv.reader(f)][1:]

    return data


def delete_row(file_name, match_index, match_string):
    """
    Delete a row from csv file
    :param file_name: <file_path/file_name>.
    :param match_string: value of the field that need to be checked
    :param match_index: index of the field
    :return: update an existing csv file
    """

    with open(file_name, 'r') as f:
        data = [list(line) for line in csv.reader(f)]
    f.close()

    update_data = []

    for i in range(len(data)):
        if data[i][match_index] != match_string:
            update_data.append(data[i])

    with open(file_name, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(update_data)

    csvFile.close()

obs_station_names = ['curw_kitulgala','curw_hingurana','curw_orugodawatta','curw_mahapallegama','curw_jaffna',
                     'curw_uduwawala','curw_kottawa_dharmapala_north','curw_IBATTARA2','curw_waga','curw_ambewela',
                     'curw_kotikawatta','curw_mulleriyawa','curw_malabe','curw_dickoya','curw_mutwal','curw_urumewella',
                     'curw_kohuwala','curw_attidiya','gov_irr_canyon','gov_irr_castlereigh']


def find_nearest_obs_stations_for_flo2d_stations(flo2d_stations_csv, obs_stations_csv):

    obs_stations = read_csv(obs_stations_csv)

    flo2d_station = read_csv(flo2d_stations_csv)

    flo2d_obs_mapping_list = [['flo2d_250_station_id', 'ob_1_id', 'ob_1_dist', 'ob_2_id', 'ob_2_dist', 'ob_3_id',
                               'ob_3_dist', 'ob_4_id', 'ob_4_dist', 'ob_5_id', 'ob_5_dist', 'ob_6_id', 'ob_6_dist',
                               'ob_7_id', 'ob_7_dist', 'ob_8_id', 'ob_8_dist', 'ob_9_id', 'ob_9_dist', 'ob_10_id',
                               'ob_10_dist']]

    for flo2d_index in range(len(flo2d_station)):

        flo2d_obs_mapping = [flo2d_station[flo2d_index][0]]

        flo2d_lat = float(flo2d_station[flo2d_index][2])
        flo2d_lng = float(flo2d_station[flo2d_index][1])

        distances = {}

        for obs_index in range(len(obs_stations)):
            lat = float(obs_stations[obs_index][4])
            lng = float(obs_stations[obs_index][5])

            intermediate_value = cos(radians(flo2d_lat)) * cos(radians(lat)) * cos(
                    radians(lng) - radians(flo2d_lng)) + sin(radians(flo2d_lat)) * sin(radians(lat))
            if intermediate_value < 1:
                distance = 6371 * acos(intermediate_value)
            else:
                distance = 6371 * acos(1)

            distances[obs_stations[obs_index][2]] = distance

        sorted_distances = collections.OrderedDict(sorted(distances.items(), key=operator.itemgetter(1))[:10])

        for key in sorted_distances.keys():
            flo2d_obs_mapping.extend([key, sorted_distances.get(key)])

        print(flo2d_obs_mapping)
        flo2d_obs_mapping_list.append(flo2d_obs_mapping)

    create_csv('MDPA_flo2d_30_obs_mapping.csv', flo2d_obs_mapping_list)


# find_nearest_obs_stations_for_flo2d_stations('flo2d_30m.csv', 'curw_active_rainfall_obs_stations.csv')


def find_nearest_wrf0_station(origin_csv, wrf0_stations_csv):

    origins = read_csv(origin_csv)

    wrf0_stations = read_csv(wrf0_stations_csv)

    nearest_wrf0_stations_list = [['origin_id', 'origin_name', 'nearest_wrf0_station_id', 'dist']]

    for origin_index in range(len(origins)):

        nearest_wrf0_station = [origins[origin_index][2], "{}_{}".format(origins[origin_index][3], origins[origin_index][1])]

        origin_lat = float(origins[origin_index][4])
        origin_lng = float(origins[origin_index][5])

        distances = {}

        for wrf0_index in range(len(wrf0_stations)):
            lat = float(wrf0_stations[wrf0_index][2])
            lng = float(wrf0_stations[wrf0_index][1])

            intermediate_value = cos(radians(origin_lat)) * cos(radians(lat)) * cos(
                    radians(lng) - radians(origin_lng)) + sin(radians(origin_lat)) * sin(radians(lat))
            if intermediate_value < 1:
                distance = 6371 * acos(intermediate_value)
            else:
                distance = 6371 * acos(1)

            distances[wrf0_stations[wrf0_index][0]] = distance

        sorted_distances = collections.OrderedDict(sorted(distances.items(), key=operator.itemgetter(1))[:10])

        count = 0
        for key in sorted_distances.keys():
            if count < 1:
                nearest_wrf0_station.extend([key, sorted_distances.get(key)])
                count += 1

        print(nearest_wrf0_station)
        nearest_wrf0_stations_list.append(nearest_wrf0_station)

    create_csv('obs_wrf0_stations_mapping.csv', nearest_wrf0_stations_list)


# find_nearest_wrf0_station('curw_active_rainfall_obs_stations.csv', 'wrf0_stations_curw.csv')

def find_nearest_d03_station_for_flo2d_grids(flo2d_stations_csv, d03_stations_csv):

    flo2d_grids = read_csv(flo2d_stations_csv)

    d03_stations = read_csv(d03_stations_csv)

    nearest_d03_stations_list = [['flo2d_grid_id', 'nearest_d03_station_id', 'dist']]

    for origin_index in range(len(flo2d_grids)):

        nearest_d03_station = [flo2d_grids[origin_index][0]]

        origin_lat = float(flo2d_grids[origin_index][2])
        origin_lng = float(flo2d_grids[origin_index][1])

        distances = {}

        for d03_index in range(len(d03_stations)):
            lat = float(d03_stations[d03_index][1])
            lng = float(d03_stations[d03_index][2])

            intermediate_value = cos(radians(origin_lat)) * cos(radians(lat)) * cos(
                    radians(lng) - radians(origin_lng)) + sin(radians(origin_lat)) * sin(radians(lat))
            if intermediate_value < 1:
                distance = 6371 * acos(intermediate_value)
            else:
                distance = 6371 * acos(1)

            distances[d03_stations[d03_index][0]] = distance

        sorted_distances = collections.OrderedDict(sorted(distances.items(), key=operator.itemgetter(1))[:10])

        count = 0
        for key in sorted_distances.keys():
            if count < 1:
                nearest_d03_station.extend([key, sorted_distances.get(key)])
                count += 1

        print(nearest_d03_station)
        nearest_d03_stations_list.append(nearest_d03_station)

    create_csv('MDPA_flo2d_30_d03_stations_mapping.csv', nearest_d03_stations_list)


# find_nearest_d03_station_for_flo2d_grids('flo2d_30m.csv', 'd03_stations.csv')

def find_nearest_d03_station_for_obs_grids(obs_stations_csv, d03_stations_csv):

    obs_grids = read_csv(obs_stations_csv)

    d03_stations = read_csv(d03_stations_csv)

    nearest_d03_stations_list = [['obs_grid_id', 'd03_1_id', 'd03_1_dist', 'd03_2_id', 'd03_2_dist', 'd03_3_id', 'd03_3_dist']]

    for origin_index in range(len(obs_grids)):

        nearest_d03_station = [obs_grids[origin_index][2]]

        origin_lat = float(obs_grids[origin_index][4])
        origin_lng = float(obs_grids[origin_index][5])

        distances = {}

        for d03_index in range(len(d03_stations)):
            lat = float(d03_stations[d03_index][1])
            lng = float(d03_stations[d03_index][2])

            intermediate_value = cos(radians(origin_lat)) * cos(radians(lat)) * cos(
                    radians(lng) - radians(origin_lng)) + sin(radians(origin_lat)) * sin(radians(lat))
            if intermediate_value < 1:
                distance = 6371 * acos(intermediate_value)
            else:
                distance = 6371 * acos(1)

            distances[d03_stations[d03_index][0]] = distance

        sorted_distances = collections.OrderedDict(sorted(distances.items(), key=operator.itemgetter(1))[:10])

        count = 0
        for key in sorted_distances.keys():
            if count < 3:
                nearest_d03_station.extend([key, sorted_distances.get(key)])
                count += 1

        print(nearest_d03_station)
        nearest_d03_stations_list.append(nearest_d03_station)

    create_csv('MDPA_obs_d03_stations_mapping.csv', nearest_d03_stations_list)


def find_nearest_flo2d_grid_id_for_given_lat_lon(flo2d_stations_csv, LAT, LON):

    flo2d_stations = read_csv(flo2d_stations_csv)

    distance_dict = {}

    origin_lat = LAT
    origin_lng = LON

    for gird_index in range(len(flo2d_stations)):
        grid_id = flo2d_stations[gird_index][0]
        lat = float(flo2d_stations[gird_index][2])
        lng = float(flo2d_stations[gird_index][1])

        intermediate_value = cos(radians(origin_lat)) * cos(radians(lat)) * cos(
                radians(lng) - radians(origin_lng)) + sin(radians(origin_lat)) * sin(radians(lat))
        if intermediate_value < 1:
            distance = 6371 * acos(intermediate_value)
        else:
            distance = 6371 * acos(1)

        distance_dict[grid_id] = distance

    sorted_distances = collections.OrderedDict(sorted(distance_dict.items(), key=operator.itemgetter(1))[:10])

    print(sorted_distances)


# find_nearest_d03_station_for_obs_grids('curw_active_rainfall_obs_stations.csv', 'd03_stations.csv')

# Mattakkuliya Bridge 2
print('Mattakkuliya Bridge 2', ':::', 'flo2d 250')
find_nearest_flo2d_grid_id_for_given_lat_lon('flo2d_250m_dd.csv', 6.980880, 79.875168)
print('Mattakkuliya Bridge 2', ':::', 'flo2d 150')
find_nearest_flo2d_grid_id_for_given_lat_lon('flo2d_150m.csv', 6.980880, 79.875168)


# Kaduwela Bridge
print('Kaduwela Bridge', ':::', 'flo2d 250')
find_nearest_flo2d_grid_id_for_given_lat_lon('flo2d_250m_dd.csv', 6.936431, 79.985192)
print('Kaduwela Bridge', ':::', 'flo2d 150')
find_nearest_flo2d_grid_id_for_given_lat_lon('flo2d_150m.csv', 6.936431, 79.985192)
