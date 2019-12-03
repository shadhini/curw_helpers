import csv

DEFAULT_COL_1 = 'R'
DEFAULT_COL_4 = '5'
DEFAULT_COL_5 = '2'


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


def change_chan_Ns_to_Rs():

    old_chan = read_file_line_by_line('resources/chan/NEW_CHAN.DAT')

    new_chan = []

    for line in old_chan:
        line_parts = line.split()
        if line_parts[0] == 'N':
            new_chan.append('{}{}{}{}{}{}'.format(DEFAULT_COL_1, line_parts[1].rjust(16), line_parts[2].rjust(16),
                                            DEFAULT_COL_4.rjust(16), DEFAULT_COL_5.rjust(16), line_parts[3].rjust(16)))
        else:
            new_chan.append(line.split('\n')[0])

    write_to_file('R_ONLY_CHAN.DAT', new_chan)


change_chan_Ns_to_Rs()