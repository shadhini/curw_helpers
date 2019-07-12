import pymysql
import traceback
from datetime import datetime, timedelta

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# connection params
HOST = "10.138.0.13"
USER = "admin"
PASSWORD = "floody"
DB ="curw_sim"
PORT = 3306

FLO2D_250 = "flo2d_250"
FLO2D_150 = "flo2d_150"
FLO2D_30 = "flo2d_30"
HecHMS = "hechms"


def fill_missing_obs_with_0s(start, end, model):

    # Connect to the database
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB,
            cursorclass=pymysql.cursors.DictCursor)

    print("Connected to database")

    if model == FLO2D_250:
        timestep = 5
    elif model == FLO2D_150:
        timestep = 15
    elif model == HecHMS:
        timestep = 5
    elif model == FLO2D_30:
        timestep = 15

    start = datetime.strptime(start, DATE_TIME_FORMAT)
    end = datetime.strptime(end, DATE_TIME_FORMAT)

    ids = []

    try:

        expected_obs_end = (datetime.now() - timedelta(hours=6)).strftime('%Y-%m-%d')
        with connection.cursor() as cursor1:
            sql_statement = "select `id` from `run` where `model`=%s " \
                            "and `obs_end` is null or `obs_end` < %s;"
            cursor1.execute(sql_statement, (model, expected_obs_end))
            results = cursor1.fetchall()
            for result in results:
                ids.append([result.get('id')])

        for id in ids:
            print(id)
            # with connection.cursor() as cursor2:
            #     sql_statement = "select min(`time`) as `time` from `data` where id=%s;"
            #     cursor2.execute(sql_statement, id)
            #     end = cursor2.fetchone()['time']

            timestamp = start
            while timestamp < end:
                print(timestamp)

                try:
                    with connection.cursor() as cursor3:
                        sql_statement = "INSERT INTO `data` (`id`,`time`,`value`) VALUES (%s,%s,%s);"
                        cursor3.execute(sql_statement, (id, timestamp, 0))
                    connection.commit()
                except Exception as ex:
                    connection.rollback()
                    traceback.print_exc()

                timestamp = timestamp + timedelta(minutes=timestep)

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()
        print("{} process completed".format(datetime.now()))


def fill_missing_fcsts(end, model):

    # Connect to the database
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB,
            cursorclass=pymysql.cursors.DictCursor)

    print("Connected to database")

    if model == FLO2D_250:
        timestep = 5
    elif model == FLO2D_150:
        timestep = 15
    elif model == HecHMS:
        timestep = 5
    elif model == FLO2D_30:
        timestep = 15

    end = datetime.strptime(end, DATE_TIME_FORMAT)

    ids = []

    try:

        with connection.cursor() as cursor1:
            sql_statement = "select `id` from `run` where `model`=%s;"
            cursor1.execute(sql_statement, model)
            results = cursor1.fetchall()
            for result in results:
                ids.append([result.get('id')])

        for id in ids:
            print(id)
            with connection.cursor() as cursor2:
                sql_statement = "select max(`time`) as `time` from `data` where id=%s;"
                cursor2.execute(sql_statement, id)
                start = cursor2.fetchone()['time']

            timestamp = start
            while timestamp < end:
                print(timestamp)
                try:
                    with connection.cursor() as cursor3:
                        sql_statement = "INSERT INTO `data` (`id`,`time`,`value`) VALUES (%s,%s,%s);"
                        cursor3.execute(sql_statement, (id, timestamp, 0))
                    connection.commit()
                except Exception as ex:
                    connection.rollback()
                    traceback.print_exc()

                timestamp = timestamp + timedelta(minutes=timestep)

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()
        print("{} process completed".format(datetime.now()))

