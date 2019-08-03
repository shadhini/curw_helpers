import decimal
import mysql.connector
from datetime import datetime
from mysql.connector import Error

# from itertools import cycle


COMMON_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
mydb = mysql.connector.connect(
    host="104.198.0.87",
    database="curw_iot",
    user="curw",
    passwd="curw@123"
)
cursor = mydb.cursor()


def check_runname(AnT, IoT, Leecom):
    sql = "SELECT id FROM curw_iot.run where (name like %s or name like %s or name like %s)"
    cursor.execute(sql, (AnT, IoT, Leecom))
    check_result = cursor.fetchall()

    return check_result


def check_id(id):
    event_id = None
    sql = "SELECT curw_id FROM curw_iot.id_mapping WHERE curw_id='" + str(id) + "'"
    cursor.execute(sql)
    is_exist = cursor.fetchone()

    if is_exist is not None:
        print("Id does not exist in the id_mapping_table")
        event_id = id

    return event_id


def get_meta_data(curw_id):
    sql = [
        "SELECT name, start_date FROM curw_iot.run WHERE id='" + str(curw_id) + "'",
        "SELECT name, latitude, longitude, description FROM curw_iot.station WHERE id in (SELECT station FROM curw_iot.run WHERE id='" + str(
            curw_id) + "')",
        "SELECT variable FROM curw_iot.variable WHERE id in (SELECT variable FROM curw_iot.run WHERE id='" + str(
            curw_id) + "')",
        "SELECT unit, type FROM curw_iot.unit WHERE id in (SELECT unit FROM curw_iot.run WHERE id='" + str(
            curw_id) + "')"
    ]

    cursor.execute(sql[0])
    result1 = cursor.fetchall()
    # return result1
    run_meta_list = []
    for row in result1:
        run_meta = {}

        run_meta['run_name'] = row[0]
        run_meta['start_date'] = row[1]
        run_meta_list.append(run_meta)

    runmeta = run_meta_list
    #
    # return timeseries_meta_list

    cursor.execute(sql[1])
    result2 = cursor.fetchall()
    # return result2
    station_meta_list = []
    for row in result2:
        station_meta = {}

        station_meta['station_name'] = row[0]
        station_meta['latitude'] = row[1]
        station_meta['longitude'] = row[2]
        station_meta['description'] = row[3]
        station_meta_list.append(station_meta)

    stationmeta = station_meta_list

    cursor.execute(sql[2])
    result3 = cursor.fetchall()
    # return result3

    variable_meta_list = []

    for row in result3:
        variable_meta = {}
        variable_meta['variable'] = row[0]

        variable_meta_list.append(variable_meta)
    variablemeta = variable_meta_list

    cursor.execute(sql[3])
    result4 = cursor.fetchall()
    unit_meta_list = []

    for row in result4:
        unit_meta = {}
        unit_meta['unit'] = row[0]
        unit_meta['unit-type'] = row[1]

        unit_meta_list.append(unit_meta)
    unitmeta = unit_meta_list

    result6 = runmeta + stationmeta + variablemeta + unitmeta

    return result6


def get_obs_hash(curw_id):
    sql = "SELECT curw_obs_id FROM curw_iot.id_mapping WHERE id='" + str(curw_id) + "'"
    cursor.execute(sql)
    obs_hash = cursor.fetchone()
    return obs_hash


def insert_id_rows(curw_id, obs_hash_id):
    cursor.execute("""INSERT INTO curw_iot.id_mapping(curw_id, curw_obs_id) VALUES (%s,%s)""",
                   (str(curw_id), str(obs_hash_id)))
    mydb.commit()


def extract_timeseries(obs_hash_id):
    # def extract_timeseries(result):
    sql1 = "SELECT curw_id FROM curw_iot.run WHERE curw_obs_id='" + str(obs_hash_id) + "'"
    cursor.execute(sql1)
    value = cursor.fetchone()

    # sql = "SELECT id, start_date, end_date from curw.run WHERE id='" + str(result) + "'"
    sql = "SELECT id, start_date, end_date from curw_iot.run WHERE id='" + str(value) + "'"

    cursor.execute(sql)
    values = cursor.fetchall()

    for i in values:
        event_id = i[0]
        start_time = i[1]
        end_time = i[2]

        start = start_time.strftime(COMMON_DATE_FORMAT)
        end = end_time.strftime(COMMON_DATE_FORMAT)
        # print("******")
        # print(str(event_id), start, end)
        # print("******")

        sql = "SELECT time, value FROM curw_iot.processed_data WHERE id='%s' and time<='%s' and time>'%s'" % (
        str(event_id), end, start)

        print(sql)
        timeseries = []
        cursor.execute(sql)
        timeseries = cursor.fetchall()

        return [[time.strftime(COMMON_DATE_FORMAT), float(value)] for time, value in timeseries]