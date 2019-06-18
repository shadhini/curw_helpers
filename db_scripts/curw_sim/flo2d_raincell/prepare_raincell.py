import pymysql
from datetime import datetime, timedelta
import traceback

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# call curw_sim.prepare_flo2d_raincell("flo2d_250", "MME", "2019-06-12 00:00:05", "2019-06-12 00:01:00");


def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        for _list in data:
            for i in range(len(_list) - 1):
                # f.seek(0)
                f.write(str(_list[i]) + ' ')
            f.write(str(_list[len(_list) - 1]))
            f.write('\n')

        f.close()


def append_to_file(file_name, data):
    with open(file_name, 'a+') as f:
        for _list in data:
            for i in range(len(_list) - 1):
                # f.seek(0)
                f.write(str(_list[i]) + ' ')
            f.write(str(_list[len(_list) - 1]))
            f.write('\n')

        f.close()


def prepare_raincell(target_model, interpolation_method, start_time, end_time, time_step_in_minutes):

    # Connect to the database
    connection = pymysql.connect(host='35.230.102.148',
            user='root',
            password='cfcwm07',
            db='curw_sim',
            cursorclass=pymysql.cursors.DictCursor)

    print("Connected to database")

    end_time = datetime.strptime(end_time, DATE_TIME_FORMAT)
    start_time = datetime.strptime(start_time, DATE_TIME_FORMAT)

    length = int(((end_time-start_time).total_seconds()/60)/time_step_in_minutes)

    START = True

    try:

        # Extract raincells
        timestamp = start_time
        while timestamp < end_time:
            raincell = []
            print("timestamp", timestamp)
            start = (timestamp + timedelta(minutes=5)).strftime(DATE_TIME_FORMAT)
            end = (timestamp + timedelta(minutes=time_step_in_minutes)).strftime(DATE_TIME_FORMAT)
            # Extract raincell from db
            # with connection.cursor() as cursor0:
            #     cursor0.execute("SET @@session.wait_timeout = 86400")

            with connection.cursor() as cursor1:
                cursor1.callproc('prepare_flo2d_raincell', (target_model, interpolation_method, start, end))
                # cursor1.callproc('new_procedure', (target_model, interpolation_method, start, end))
                results = cursor1.fetchall()
                for result in results:
                    raincell.append([result.get('cell'), '%.1f' % result.get('value')])

            if START:
                raincell.insert(0, ["{} {} {} {}".format(time_step_in_minutes, length, start_time, end_time)])
                write_to_file('RAINCELL.DAT', raincell)
                START=False
            else:
                append_to_file('RAINCELL.DAT', raincell)

            timestamp = timestamp + timedelta(minutes=time_step_in_minutes)

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()
        print("{} raincell generation process completed".format(datetime.now()))


def prepare_flo2d_250_MME_raincell_5_min_step(start_time, end_time):

    # Connect to the database
    connection = pymysql.connect(host='35.230.102.148',
            user='root',
            password='cfcwm07',
            db='curw_sim',
            cursorclass=pymysql.cursors.DictCursor)

    print("Connected to database")

    end_time = datetime.strptime(end_time, DATE_TIME_FORMAT)
    start_time = datetime.strptime(start_time, DATE_TIME_FORMAT)

    length = int(((end_time-start_time).total_seconds()/60)/5)

    START = True

    try:

        # Extract raincells
        timestamp = start_time
        while timestamp < end_time:

            timestamp = timestamp + timedelta(minutes=5)

            raincell = []


            # Extract raincell from db
            with connection.cursor() as cursor1:
                cursor1.callproc('flo2d_250_MME_5_min_raincell', (timestamp,))
                results = cursor1.fetchall()
                for result in results:
                    raincell.append([result.get('cell_id'), '%.1f' % result.get('value')])

            if START:
                raincell.insert(0, ["{} {} {} {}".format(5, length, start_time, end_time)])
                write_to_file('RAINCELL.DAT', raincell)
                START=False
            else:
                append_to_file('RAINCELL.DAT', raincell)

            print(timestamp)

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()
        print("{} raincell generation process completed".format(datetime.now()))


def prepare_raincell_5_min_step(target_model, interpolation_method, start_time, end_time):

    # Connect to the database
    connection = pymysql.connect(host='35.230.102.148',
            user='root',
            password='cfcwm07',
            db='curw_sim',
            cursorclass=pymysql.cursors.DictCursor)

    print("Connected to database")

    end_time = datetime.strptime(end_time, DATE_TIME_FORMAT)
    start_time = datetime.strptime(start_time, DATE_TIME_FORMAT)

    length = int(((end_time-start_time).total_seconds()/60)/5)

    START = True

    try:

        # Extract raincells
        timestamp = start_time
        while timestamp < end_time:

            timestamp = timestamp + timedelta(minutes=5)

            raincell = []

            # Extract raincell from db
            with connection.cursor() as cursor1:
                cursor1.callproc('`prepare_flo2d_5_min_raincell`', (target_model, interpolation_method, timestamp))
                results = cursor1.fetchall()
                for result in results:
                    raincell.append([result.get('cell_id'), '%.1f' % result.get('value')])

            if START:
                raincell.insert(0, ["{} {} {} {}".format(5, length, start_time, end_time)])
                write_to_file('RAINCELL.DAT', raincell)
                START=False
            else:
                append_to_file('RAINCELL.DAT', raincell)

            print(timestamp)

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()
        print("{} raincell generation process completed".format(datetime.now()))


print("{} start preparing raincell".format(datetime.now()))
# prepare_raincell(target_model="flo2d_250", interpolation_method="MME", start_time="2019-06-07 00:00:00",
#         end_time="2019-06-13 00:00:00", time_step_in_minutes=60)

# prepare_flo2d_250_MME_raincell_5_min_step("2019-06-13 23:30:00", "2019-06-18 23:30:00")

prepare_raincell_5_min_step(target_model="flo2d_150", interpolation_method="MME", start_time="2019-06-13 23:30:00", end_time="2019-06-18 23:30:00")