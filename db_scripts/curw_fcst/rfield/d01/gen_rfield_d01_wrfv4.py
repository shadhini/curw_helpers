import traceback
from netCDF4 import Dataset
import numpy as np
import os
import json
from datetime import datetime, timedelta
import time
import paramiko


def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        for _string in data:
            # f.seek(0)
            f.write(str(_string) + '\n')

        f.close()


def read_attribute_from_config_file(attribute, config):
    """
    :param attribute: key name of the config json file
    :param config: loaded json file
    :return:
    """
    if attribute in config and (config[attribute]!=""):
        return config[attribute]
    else:
        print("{} not specified in config file.".format(attribute))
        exit(1)


def ssh_command(ssh, command):
    ssh.invoke_shell()
    stdin, stdout, stderr = ssh.exec_command(command)
    for line in stdout.readlines():
        print(line)
    for line in stderr.readlines():
        print(line)


def remove_older_rfield_files(host, user, key, command):
    try:
        ssh = paramiko.SSHClient()
        print('Calling paramiko')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, key_filename=key)

        ssh_command(ssh, command)
    except Exception as e:
        print('Connection Failed')
        print(e)
    finally:
        print("Close connection")
        ssh.close()


def get_per_time_slot_values(prcp):
    per_interval_prcp = (prcp[1:] - prcp[:-1])
    return per_interval_prcp


def get_file_last_modified_time(file_path):

    # returns local time (UTC + 5 30)
    modified_time = time.gmtime(os.path.getmtime(file_path) + 19800)

    return time.strftime('%Y-%m-%d %H:%M:%S', modified_time)


def datetime_utc_to_lk(timestamp_utc, shift_mins=0):
    return timestamp_utc + timedelta(hours=5, minutes=30 + shift_mins)


def read_netcdf_file(rainnc_net_cdf_file_path, model, version):
    """
    :param rainnc_net_cdf_file_path:
    :return:

    """

    if not os.path.exists(rainnc_net_cdf_file_path):
        print('no rainnc netcdf')
    else:

        """
        RAINNC netcdf data extraction
        """
        nnc_fid = Dataset(rainnc_net_cdf_file_path, mode='r')

        time_unit_info = nnc_fid.variables['XTIME'].units

        time_unit_info_list = time_unit_info.split(' ')

        lats = nnc_fid.variables['XLAT'][0, :, 0]
        lons = nnc_fid.variables['XLONG'][0, 0, :]

        lon_min = lons[0].item()
        lat_min = lats[0].item()
        lon_max = lons[-1].item()
        lat_max = lats[-1].item()
        print('[lon_min, lat_min, lon_max, lat_max] :', [lon_min, lat_min, lon_max, lat_max])

        lat_inds = np.where((lats >= lat_min) & (lats <= lat_max))
        lon_inds = np.where((lons >= lon_min) & (lons <= lon_max))

        rainnc = nnc_fid.variables['RAINNC'][:, lat_inds[0], lon_inds[0]]

        times = nnc_fid.variables['XTIME'][:]

        nnc_fid.close()

        diff = get_per_time_slot_values(rainnc)

        width = len(lons)
        height = len(lats)

        timeseries_dict = {}

        for y in range(height):
            for x in range(width):

                lat = '%.6f' % lats[y]
                lon = '%.6f' % lons[x]

                station = '{} {}'.format(lon, lat)

                data_list = []
                # generate timeseries for each station
                for i in range(len(diff)):
                    data_list.append('%.3f' % float(diff[i, y, x]))

                timeseries_dict[station] = data_list

        now = datetime.strptime((datetime.now() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d 00:00:00'),
                '%Y-%m-%d %H:%M:%S')

        for i in range(len(diff)):
            rfield = []
            ts_time = datetime.strptime(time_unit_info_list[2], '%Y-%m-%dT%H:%M:%S') + timedelta(
                    minutes=times[i + 1].item())
            t = datetime_utc_to_lk(ts_time, shift_mins=0)
            timestamp = t.strftime('%Y-%m-%d %H:%M:%S')

            for station in timeseries_dict.keys():
                rfield.append('{} {}'.format(station, timeseries_dict.get(station)[i]))

            if t < now:
                write_to_file('/home/uwcc-admin/rfield_extractor/d01/past/{}_{}_{}_rfield.txt'.format(model, version, timestamp), rfield)
            else:
                write_to_file('/home/uwcc-admin/rfield_extractor/d01/future/{}_{}_{}_rfield.txt'.format(model, version, timestamp), rfield)


if __name__=="__main__":

    try:
        config = json.loads(open('config.json').read())

        # source details
        wrf_dir = read_attribute_from_config_file('wrf_dir', config)
        model = read_attribute_from_config_file('model', config)
        version = read_attribute_from_config_file('version', config)
        wrf_model_list = read_attribute_from_config_file('wrf_model_list', config)
        wrf_model_list = wrf_model_list.split(',')

        # rfield params
        rfield_host = read_attribute_from_config_file('rfield_host', config)
        rfield_user = read_attribute_from_config_file('rfield_user', config)
        rfield_key = read_attribute_from_config_file('rfield_key', config)
        rfield_command1 = read_attribute_from_config_file('rfield_command1', config)

        remove_older_rfield_files(host=rfield_host, key=rfield_key, user=rfield_user, command=rfield_command1)

        if 'start_date' in config and (config['start_date']!=""):
            run_date_str = config['start_date']
        else:
            run_date_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        # daily_dir = 'STATIONS_{}'.format(run_date_str)

        # output_dir = os.path.join(wrf_dir, daily_dir)

        for wrf_model in wrf_model_list:

            daily_dir = 'OUTPUT_{}_18/'.format(wrf_model, run_date_str)

            output_dir = os.path.join(wrf_dir, daily_dir)

            model_name = "{}_{}".format(model, wrf_model)

            rainnc_net_cdf_file = 'd01_all-Kelani_RAINNC_{}_{}.nc'.format(run_date_str, wrf_model)

            rainnc_net_cdf_file_path = os.path.join(output_dir, rainnc_net_cdf_file)
            print("d01 rainnc_net_cdf_file_path : {}".format(rainnc_net_cdf_file_path))

            try:
                read_netcdf_file(rainnc_net_cdf_file_path=rainnc_net_cdf_file_path, model=model_name, version=version)
            except Exception as e:
                print('Net CDF file reading error.')
                traceback.print_exc()

    except Exception as e:
        print('JSON config data loading error.')
        traceback.print_exc()
    finally:
        os.system("sudo scp -r /home/uwcc-admin/rfield_extractor/d01 "
                  "uwcc-admin@10.138.0.6:/var/www/html/wrf/v4/rfield")

        print("rfields pushed to cms")
        print("Process finished.")