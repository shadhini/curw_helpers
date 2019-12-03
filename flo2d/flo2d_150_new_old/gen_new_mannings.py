import csv


def read_file_line_by_line(file_name):
    """
    Read file content line by line
    :param file_name: file_path/file_name
    :return: return the lines of the file content as a list
    """

    lines = []

    with open(file_name, 'r') as f:
        content = f.readlines()

        for line in content:
            lines.append(line)

    return lines


def write_to_file(file_name, data):
    """
    Write to file (w+, if there's no such file, a file would be created)
    :param file_name: file_path/file_name
    :param data:
    :return:
    """
    with open(file_name, 'w+') as f:
        f.write('\n'.join(data))


def read_csv(file_name):
    """
    Read csv file
    :param file_name: <file_path/file_name>.csv
    :return: list of lists which contains each row of the csv file
    """

    with open(file_name, 'r') as f:
        data = [list(line) for line in csv.reader(f)][1:]

    return data


def gen_new_mannings():

    grid_mapping = read_csv('old_new_flo2d_150_grid_id_map.csv')

    grid_map_dict = {}  # [new_id, old_id]

    for line in grid_mapping:
        grid_map_dict[line[1]] = line[0]

    old_mannings = read_file_line_by_line('resources/mannings/MANNINGS_OLD.DAT')

    old_mannings_dict = {}

    for line in old_mannings:
        line_parts = line.split()
        old_mannings_dict[line_parts[0]] = line_parts[1]

    new_mannings = []

    for i in range(39526):
        first_col = (str(i+1)).ljust(8)
        second_col = old_mannings_dict.get(grid_map_dict.get(str(i+1)))

        new_mannings.append('{}{}'.format(first_col, second_col))

    write_to_file('NEW_MANNINGS.DAT', new_mannings)


gen_new_mannings()









