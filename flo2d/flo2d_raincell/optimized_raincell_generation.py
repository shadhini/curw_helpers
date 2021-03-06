import pymysql
import getopt
from datetime import datetime, timedelta
import traceback
import os
import sys

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# connection params
HOST = "10.138.0.13"
USER = "routine_user"
PASSWORD = "aquaroutine"
DB = "curw_sim"
PORT = 3306


def write_to_file(file_name, data):
    with open(file_name, 'w+') as f:
        f.write('\n'.join(data))


def append_to_file(file_name, data):
    with open(file_name, 'a+') as f:
        f.write('\n'.join(data))


def check_time_format(time, model):
    try:
        time = datetime.strptime(time, DATE_TIME_FORMAT)

        if time.strftime('%S')!='00':
            print("Seconds should be always 00")
            exit(1)
        if model=="flo2d_250" and time.strftime('%M') not in (
        '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '00'):
            print("Minutes should be multiple of 5 fro flo2d_250")
            exit(1)
        if model=="flo2d_150" and time.strftime('%M') not in ('15', '30', '45', '00'):
            print("Minutes should be multiple of 15 for flo2d_150")
            exit(1)

        return True
    except Exception:
        traceback.print_exc()
        print("Time {} is not in proper format".format(time))
        exit(1)


def find_files_with_given_prefix(output_dir, prefix):
    path = output_dir
    files = []
    for file_name in os.listdir(path):
        if os.path.isfile(os.path.join(path, file_name)) and prefix in file_name:
            files.append(file_name)

    return files


def find_latest_matching_raincell(output_dir, flo2d_model, start):
    # assuming raincell is generated only once a day
    nearest_start = (datetime.strptime(start, DATE_TIME_FORMAT) - timedelta(days=1)).strftime('%Y-%m-%d')
    matching_file = find_files_with_given_prefix(output_dir=output_dir,
            prefix='RAINCELL_{}_{}_'.format(flo2d_model, nearest_start))[0]

    return os.path.join(output_dir, matching_file)


def extract_content_from_old_raincell(existing_raincell, start, end, raincell_size):

    content = []

    with open(existing_raincell, 'r') as f:
        line = f.readline().split(' ')
        timestep = int(line[0])
        old_start_date = line[2]
        old_start_time = line[3]
        old_end_date = line[4]
        old_end_time = line[5]

        old_start = datetime.strptime('{} {}'.format(old_start_date, old_start_time), DATE_TIME_FORMAT)
        length_to_avoid = int(((start - old_start).total_seconds() / 60) / timestep) * raincell_size
        # assuming existing raincell is of anough length
        length_to_read = int(((end - start).total_seconds() / 60) / timestep) * raincell_size
        cnt = 0

        while line and cnt <= (length_to_avoid + length_to_read):
            line = f.readline()
            cnt += 1
            if cnt > length_to_avoid:
                content.append(line)

        return content


def prepare_raincell_(raincell_file_path, start_time, end_time, target_model="flo2d_250", interpolation_method="MME",
                      existing_raincell =  None):
    """
    Create raincell for flo2d
    :param raincell_file_path:
    :param start_time: Raincell start time (e.g: "2019-06-05 00:00:00")
    :param end_time: Raincell start time (e.g: "2019-06-05 23:30:00")
    :param target_model: FLO2D model (e.g. flo2d_250, flo2d_150)
    :param interpolation_method: value interpolation method (e.g. "MME")
    :return:
    """
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB,
            cursorclass=pymysql.cursors.DictCursor)
    print("Connected to database")

    end_time = datetime.strptime(end_time, DATE_TIME_FORMAT)
    start_time = datetime.strptime(start_time, DATE_TIME_FORMAT)

    if end_time < start_time:
        print("start_time should be less than end_time")
        exit(1)

    max_end_time = datetime.strptime((datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d 23:30:00'),
            DATE_TIME_FORMAT)
    min_start_time = datetime.strptime("2019-06-28 00:00:00", DATE_TIME_FORMAT)

    if end_time > max_end_time:
        end_time = max_end_time

    if start_time < min_start_time:
        start_time = min_start_time

    if target_model=="flo2d_250":
        timestep = 5
        raincell_size = 9348
    elif target_model=="flo2d_150":
        timestep = 15
        raincell_size = 41767

    length = int(((end_time - start_time).total_seconds() / 60) / timestep)

    write_to_file(raincell_file_path,
            ['{} {} {} {}\n'.format(timestep, length, start_time.strftime(DATE_TIME_FORMAT),
                    end_time.strftime(DATE_TIME_FORMAT))])

    if existing_raincell:
        ex_rc_end = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:00:00'), DATE_TIME_FORMAT) - timedelta(hours=6)
        append_to_file(file_name=raincell_file_path, data=extract_content_from_old_raincell(
                existing_raincell= existing_raincell, start=start_time, end=ex_rc_end, raincell_size=raincell_size))
        start_time = ex_rc_end

    try:
        timestamp = start_time
        while timestamp < end_time:
            raincell = []
            timestamp = timestamp + timedelta(minutes=timestep)
            count = 1
            # Extract raincell from db
            with connection.cursor() as cursor1:
                cursor1.callproc('prepare_flo2d_raincell', (target_model, interpolation_method, timestamp))
                for result in cursor1:
                    raincell.append('{} {}'.format(result.get('cell_id'), '%.1f' % result.get('value')))
                raincell.append('')
            append_to_file(raincell_file_path, raincell)
            print(timestamp)
    except Exception as ex:
        traceback.print_exc()
    finally:
        connection.close()
        print("{} raincell generation process completed".format(datetime.now()))


def create_dir_if_not_exists(path):
    """
    create directory(if needed recursively) or paths
    :param path: string : directory path
    :return: string
    """
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def usage():
    usageText = """
    Usage: .\gen_raincell.py [-m flo2d_XXX][-s "YYYY-MM-DD HH:MM:SS"] [-e "YYYY-MM-DD HH:MM:SS"]

    -h  --help          Show usage
    -m  --model         FLO2D model (e.g. flo2d_250, flo2d_150). Default is flo2d_250.
    -s  --start_time    Raincell start time (e.g: "2019-06-05 00:00:00"). Default is 23:30:00, 3 days before today.
    -e  --end_time      Raincell end time (e.g: "2019-06-05 23:30:00"). Default is 23:30:00, tomorrow.
    """
    print(usageText)


if __name__=="__main__":

    try:
        start_time = None
        end_time = None
        flo2d_model = None

        try:
            opts, args = getopt.getopt(sys.argv[1:], "h:m:s:e:",
                    ["help", "flo2d_model=", "start_time=", "end_time="])
        except getopt.GetoptError:
            usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt in ("-m", "--flo2d_model"):
                flo2d_model = arg.strip()
            elif opt in ("-s", "--start_time"):
                start_time = arg.strip()
            elif opt in ("-e", "--end_time"):
                end_time = arg.strip()

        os.chdir(r"D:\raincells")
        os.system(r"venv\Scripts\activate")

        if flo2d_model is None:
            flo2d_model = "flo2d_250"
        elif flo2d_model not in ("flo2d_250", "flo2d_150"):
            print("Flo2d model should be either \"flo2d_250\" or \"flo2d_150\"")
            exit(1)

        if start_time is None:
            start_time = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d 23:30:00')
        else:
            check_time_format(time=start_time, model=flo2d_model)

        if end_time is None:
            end_time = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d 23:30:00')
        else:
            check_time_format(time=end_time, model=flo2d_model)

        raincell_file_path = os.path.join(r"D:\raincells",
                'RAINCELL_{}_{}_{}.DAT'.format(flo2d_model, start_time, end_time).replace(' ', '_').replace(':', '-'))

        if not os.path.isfile(raincell_file_path):
            print("{} start preparing raincell".format(datetime.now()))
            existing_raincell = find_latest_matching_raincell(output_dir=r"D:\raincells",
                    flo2d_model=flo2d_model, start=start_time)
            prepare_raincell_(raincell_file_path,
                    target_model=flo2d_model, start_time=start_time, end_time=end_time, existing_raincell=existing_raincell)
            # print(raincell_file_path, flo2d_model, start_time, end_time)
            print("{} completed preparing raincell".format(datetime.now()))
        else:
            print('Raincell file already in path : ', raincell_file_path)

        # os.system(r"deactivate")

    except Exception:
        traceback.print_exc()
