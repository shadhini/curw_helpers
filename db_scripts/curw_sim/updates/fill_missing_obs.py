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


def fill_missing_obs_with_0s(model, timestep):

    # Connect to the database
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB,
            cursorclass=pymysql.cursors.DictCursor)

    print("Connected to database")

    start = datetime.strptime("2019-06-28 00:00:00", DATE_TIME_FORMAT)

    ids = []

    try:

        # remove -99999
        with connection.cursor() as cursor1:
            sql_statement = "select `id` from `run` where `model`=%s " \
                            "and `obs_end` is null or `obs_end` < %s;"
            cursor1.execute(sql_statement, (model, "2019-07-07"))
            results = cursor1.fetchall()
            for result in results:
                ids.append([result.get('id')])

        for id in ids:
            print(id)
            # with connection.cursor() as cursor2:
            #     sql_statement = "select min(`time`) as `time` from `data` where id=%s;"
            #     cursor2.execute(sql_statement, id)
            #     end = cursor2.fetchone()['time']
            end = datetime.strptime("2019-07-08 00:00:00", DATE_TIME_FORMAT)


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


print("Fill missing obs with 0s in flo2d 250")
fill_missing_obs_with_0s(model="flo2d_250", timestep=5)

print("Fill missing obs with 0s in flo2d 150")
fill_missing_obs_with_0s(model="flo2d_150", timestep=15)

print("Fill missing obs with 0s in hechms_input_rain")
fill_missing_obs_with_0s(model="hechms_input_rain", timestep=5)