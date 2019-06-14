import pymysql


def prepare_raincell():
    # Connect to the database
    connection = pymysql.connect(host='35.230.102.148',
            user='root',
            password='cfcwm07',
            db='curw_sim',
            cursorclass=pymysql.cursors.SSCursor)

    start_time = ''
    end_time = ''

    try:

        # Extract timeseries start time and end time
        with connection.cursor() as cursor1:
            cursor1.callproc('get_TS_start_end', (model, version))
            result = cursor1.fetchone()
            start_time = result.get('start')
            end_time = result.get('end')

        # Extract rfields
        timestamp = start_time
        while timestamp <= end_time:
            # rfield = [['latitude', 'longitude', 'rainfall']]
            rfield = []
            with connection.cursor() as cursor2:
                cursor2.callproc('get_d03_rfield_kelani_basin_rainfall', (model, version, timestamp))
                results = cursor2.fetchall()
                for result in results:
                    rfield.append(
                            '{} {} {}'.format(result.get('longitude'), result.get('latitude'), result.get('value')))

            write_to_file('/var/www/html/wrf/{}/rfield/{}_{}_{}_rfield.txt'.format(version, model, version, timestamp),
                    rfield)

            timestamp = datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S') + timedelta(minutes=15)

    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()