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


def append_to_file(file_name, data):

    """
    Append to file (a+, if there's no such file, a file would be created)
    :param file_name: file_path/file_name
    :param data:
    :return:
    """
    with open(file_name, 'a+') as f:
        f.write('\n'.join(data))


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


def read_csv(file_name):
    """
    Read csv file
    :param file_name: <file_path/file_name>.csv
    :return: list of lists which contains each row of the csv file
    """

    with open(file_name, 'r') as f:
        data = [list(line) for line in csv.reader(f)][1:]

    return data


def gen_grids_dict(grids_as_lines):
    """

    :param grids_as_lines: list of strings in format '<gird_id>_<x>_<y>'
    :return: grids dict: key = "<x>_<y>" and value = <grid_id>
    """
    grids_dict = {}

    for line in grids_as_lines:
        line_parts = line.split()
        key = '{}_{}'.format(line_parts[1], line_parts[2])
        grids_dict[key] = line_parts[0]

    return grids_dict


def gen_old_new_flo2d_150_grid_mapping():

    mapping = [['old_grid_id', 'new_grid_id']]

    old_grids = read_file_line_by_line('OLD_CADPTS.DAT')
    old_grids_dict = gen_grids_dict(old_grids)

    new_grids = read_file_line_by_line('NEW_CADPTS.DAT')
    new_grid_dict = gen_grids_dict(new_grids)

    for old_coordinate in old_grids_dict.keys():
        mapping.append([old_grids_dict.get(old_coordinate), new_grid_dict.get(old_coordinate)])

    create_csv('old_new_flo2d_150_grid_id_map.csv', mapping)


def gen_new_chan_head():

    grid_mapping = read_csv('old_new_flo2d_150_grid_id_map.csv')

    grid_map_dict = {}

    for line in grid_mapping:
        grid_map_dict[line[0]] = line[1]

    old_chan_head = read_file_line_by_line('OLD_CHAN_head.DAT')

    new_chan_head = []

    for line in old_chan_head:
        line_parts = line.split()
        if len(line_parts) == 3:
            new_chan_head.append('{}{}{}'.format(line_parts[0], line_parts[1].rjust(13), line_parts[2].rjust(16)))
        else:
            new_chan_line = '{}{}'.format(line_parts[0], (grid_map_dict.get(line_parts[1])).rjust(16))
            for i in range(len(line_parts)-2):
                new_chan_line += '{}'.format(line_parts[i+2].rjust(16))
            new_chan_head.append(new_chan_line)

    new_chan_head.append('')

    write_to_file('NEW_CHAN.DAT', new_chan_head)


def gen_new_chan_tail():

    grid_mapping = read_csv('old_new_flo2d_150_grid_id_map.csv')

    grid_map_dict = {}

    for line in grid_mapping:
        grid_map_dict[line[0]] = line[1]

    old_chan_talil= read_file_line_by_line('OLD_CHAN_tail.DAT')

    new_chan_tail = []

    for line in old_chan_talil:
        line_parts = line.split()
        new_chan_tail.append('{}{}{}'.format(line_parts[0],
                                             (grid_map_dict.get(line_parts[1])).rjust(16),
                                             (grid_map_dict.get(line_parts[2])).rjust(16)))

    append_to_file('NEW_CHAN.DAT', new_chan_tail)


def gen_new_chan():
    gen_new_chan_head()
    gen_new_chan_tail()

gen_new_chan()









