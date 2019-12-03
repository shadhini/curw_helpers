import csv


def read_file(file_name):
    """
    Read content from a file
    :param file_name: file_path/file_name
    :return: return the whole content of the file
    """

    with open(file_name, 'r') as f:
        content = f.read()

    return content


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
        f.write(data)


def append_to_file(file_name, data):

    """
    Append to file (a+, if there's no such file, a file would be created)
    :param file_name: file_path/file_name
    :param data:
    :return:
    """
    with open(file_name, 'a+') as f:
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


def gen_new_infil():

    old_infil_head = read_file('resources/infil/INFIL_head.DAT')

    write_to_file('NEW_INFIL.DAT', old_infil_head)

    new_infil = ['']

    grid_mapping = read_csv('old_new_flo2d_150_grid_id_map.csv')

    grid_map_dict = {}  # [old_id, new_id]

    for line in grid_mapping:
        grid_map_dict[line[0]] = line[1]

    old_infil_tail = read_file_line_by_line('resources/infil/INFIL_tail.DAT')

    for line in old_infil_tail:
        line_parts = line.split()

        new_infil_line = '{}{}'.format(line_parts[0], (grid_map_dict.get(line_parts[1])).rjust(8))
        for i in range(len(line_parts) - 2):
            new_infil_line += '{}'.format(line_parts[i + 2].rjust(12))
        new_infil.append(new_infil_line)

    append_to_file('NEW_INFIL.DAT', new_infil)


gen_new_infil()









