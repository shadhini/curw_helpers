import csv


def read_csv(file_name):
    """
    Read csv file
    :param file_name: <file_path/file_name>.csv
    :return: list of lists which contains each row of the csv file
    """

    with open(file_name, 'r') as f:
        data = [list(line) for line in csv.reader(f)][1:]

    return data


def write_to_file(file_name, data):
    """
    Write to file (w+, if there's no such file, a file would be created)
    :param file_name: file_path/file_name
    :param data:
    :return:
    """
    with open(file_name, 'w+') as f:
        f.write('\n'.join(data))


def create_lat_lon_file(filename, csv_file):

    csv = read_csv(csv_file)
    print(csv)

    lon_lat_set = []

    for i in range(len(csv)):
        lon_lat_set.append("{} {}".format(csv[i][0], csv[i][1]))

    write_to_file(file_name=filename, data=lon_lat_set)


create_lat_lon_file("kelani_basin_xy.txt", 'kelani_basin_ex.csv')

create_lat_lon_file("d03_xy.txt", 'd03_ex.csv')

