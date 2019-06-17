import pymysql
import traceback
from datetime import datetime, timedelta


def remove_negative_99999(model):

    # Connect to the database
    connection = pymysql.connect(host='35.230.102.148',
            user='root',
            password='cfcwm07',
            db='curw_sim',
            cursorclass=pymysql.cursors.DictCursor)

    print("Connected to database")

    ids = []

    try:

        # remove -99999
        with connection.cursor() as cursor1:
            sql_statement = "SELECT `id` FROM `run` where `obs_end` like %s and `model`=%s;"
            cursor1.execute(sql_statement, ("2019-06-14%", model))
            results = cursor1.fetchall()
            for result in results:
                ids.append((result.get('id')))

        for id in ids:
            with connection.cursor() as cursor2:
                sql_statement = "UPDATE `data` SET `value`=0 WHERE `id`=%s and `value`=-99999 and `time`>%s;"
                cursor2.execute(sql_statement, (id, "2019-06-14%"))
                print(id)

            connection.commit()

    except Exception as ex:
        connection.rollback()
        traceback.print_exc()
    finally:
        connection.close()
        print("{} raincell generation process completed".format(datetime.now()))


print("Remove -99999 in flo2d 250")
remove_negative_99999("flo2d_250")

print("Remove -99999 in flo2d 150")
remove_negative_99999("flo2d_150")
