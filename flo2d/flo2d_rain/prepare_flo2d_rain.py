from datetime import timedelta, datetime
import  traceback
from csv_utils import read_csv

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write('\n'.join(data))
    print("File generated")


def format_rain(csv_file, start):

    timeseries = read_csv(csv_file)

    rain_dat = []

    total_rain = 0

    cumulative_timeseries = []

    for i in range(len(timeseries)):
        total_rain += float(timeseries[i][1])
        cumulative_timeseries.append(total_rain)

    for i in range(len(timeseries)):
        time_col = ((datetime.strptime(timeseries[i][0], DATE_TIME_FORMAT) - start).total_seconds())/3600
        rain_col = float(timeseries[i][1])/total_rain

        rain_dat.append("R   {}   {}".format('%.4f' % time_col, cumulative_timeseries[i]/total_rain))

    rain_dat.insert(0, "R   0   0")
    rain_dat.insert(0, "{}   5   0   0".format(total_rain))
    rain_dat.insert(0, "0   0   ")

    write_to_file("RAIN.DAT", rain_dat)


# format_rain("6531.csv", datetime.strptime("2019-06-12 23:30:00", DATE_TIME_FORMAT))


def generate_time_values(start, end):

    start = datetime.strptime(start, DATE_TIME_FORMAT)
    end = datetime.strptime(end, DATE_TIME_FORMAT)

    times_original = [start]

    time = start
    while times_original[-1] < end:
        time = time + timedelta(minutes=5)
        times_original.append(time)
        print(time)

    times = []
    for i in range(len(times_original)):
        times.append("{}".format('%.4f' % ((times_original[i] - start).total_seconds() / 3600)))
        print((times_original[i] - start).total_seconds() / 3600)

    write_to_file("times.DAT", times)


# generate_time_values(start="2019-06-01 00:00:00", end="2019-06-20 00:00:00")