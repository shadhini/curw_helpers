import csv
import traceback


def read_csv(file_name):
    """
    Read csv file
    :param file_name: <file_path/file_name>.csv
    :return: list of lists which contains each row of the csv file
    """

    with open(file_name, 'r') as f:
        data = [list(line) for line in csv.reader(f)]

    return data


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

    csvFile.close()


def calculate_hanwella_wl_from_ranwala_wl(ranwala_ts):
    ranwala_ts = ranwala_ts
    hanwella_ts = []

    for i in range(len(ranwala_ts) - 1):
        # x = Ranwala
        # DX Ranwala (x[x] - x[t-1]}
        # Hanwella = X 1.642174610188251` -   DX 3.8585516925010444` -
        #    8.810870547723741`;
        x = float(ranwala_ts[i + 1][1])
        dx = float(ranwala_ts[i + 1][1]) - float(ranwala_ts[i][1])
        hanwella_wl = x * 1.642174610188251 - dx * 3.8585516925010444 - 8.810870547723741
        hanwella_ts.append([ranwala_ts[i + 1][0], hanwella_wl])

    for i in range(len(hanwella_ts)):
        if hanwella_ts[i][1] < 0.2:
            hanwella_ts[i][1] = 0.2

    return hanwella_ts


def calculate_hanwella_discharge_from_hanwella_wl(hanwella_wl_ts):

    hanwella_discharge_ts = []
    for i in range(len(hanwella_wl_ts)):
        wl = float(hanwella_wl_ts[i][1])
        discharge = 26.1131 * (wl ** 1.73499)
        hanwella_discharge_ts.append([hanwella_wl_ts[i][0], discharge])

    return hanwella_discharge_ts


if __name__ == "__main__":

    try:

        ranwala_ts_file_path = "ranwala_wl_06-04_to_06-15.csv"

        hanwella_ts = calculate_hanwella_wl_from_ranwala_wl(ranwala_ts=read_csv(ranwala_ts_file_path))

        # if hanwella_ts is not None and len(hanwella_ts) > 0:
        #     create_csv(file_name='Hanwella_WL.csv', data=hanwella_ts)

        discharge_ts = calculate_hanwella_discharge_from_hanwella_wl(hanwella_ts)

        if discharge_ts is not None and len(discharge_ts) > 0:
            create_csv(file_name='hanwella_estimated_dis_06-04_to_06-15.csv', data=discharge_ts)

    except Exception as e:
        traceback.print_exc()
    finally:
        print("Hanwella WL Generated")


