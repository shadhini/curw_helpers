from datetime import timedelta, datetime
import  traceback
from csv_utils import read_csv

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        for _string in data:
            # f.seek(0)
            f.write(str(_string) + '\n')

        f.close()


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


format_rain("6531.csv", datetime.strptime("2019-06-12 23:30:00", DATE_TIME_FORMAT))
