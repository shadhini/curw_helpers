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


def gen_new_chanbank():

    grid_mapping = read_csv('old_new_flo2d_150_grid_id_map.csv')

    grid_map_dict = {}  # [old_id, new_id]

    for line in grid_mapping:
        grid_map_dict[line[0]] = line[1]

    old_chanbank = read_file_line_by_line('resources/chanbank/OLD_CHANBANK.DAT')

    new_chanbank = []

    for line in old_chanbank:
        line_parts = line.split()

        if line_parts[0] == '0':
            first_col = line_parts[0].rjust(8)
        else:
            first_col = (grid_map_dict.get(line_parts[0])).rjust(8)

        if line_parts[1] == '0':
            second_col = line_parts[1].rjust(16)
        else:
            second_col = (grid_map_dict.get(line_parts[1])).rjust(16)

        new_chanbank.append('{}{}'.format(first_col, second_col))

    new_chanbank.append('')

    write_to_file('NEW_CHANBANK.DAT', new_chanbank)


gen_new_chanbank()









