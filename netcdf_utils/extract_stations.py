import os
import numpy as np
from netCDF4 import Dataset
from datetime import datetime, timedelta

from logger import logger
from stations import KELANI_BASIN_EXTENT


# def get_two_element_average(prcp, return_diff=True):
#     avg_prcp = (prcp[1:] + prcp[:-1]) * 0.5
#     if return_diff:
#         return avg_prcp - np.insert(avg_prcp[:-1], 0, [0], axis=0)
#     else:
#         return avg_prcp


def get_wrf0_d03_stations_precipitation(net_cdf_file_path):

    """
    Extract and push wrf0 d03 stations in the kelani basin extent to the database
    :param net_cdf_file_path:
    :return:
    """
    if not os.path.exists(net_cdf_file_path):
        logger.warning('no netcdf')
        print('no netcdf')
    else:

        ncfile_id = Dataset(net_cdf_file_path, mode='r')

        lats = ncfile_id.variables['XLAT'][0, :, 0]
        lons = ncfile_id.variables['XLONG'][0, 0, :]

        lat_min = KELANI_BASIN_EXTENT[0]
        lon_min = KELANI_BASIN_EXTENT[1]
        lat_max = KELANI_BASIN_EXTENT[2]
        lon_max = KELANI_BASIN_EXTENT[3]
        print('[lat_min, lon_min, lat_max, lon_max,] :', [lat_min, lon_min, lat_max, lon_max])

        lat_inds = np.where((lats >= lat_min) & (lats <= lat_max))
        lon_inds = np.where((lons >= lon_min) & (lons <= lon_max))

        rainc = ncfile_id.variables['RAINC'][:, lon_inds[0], lat_inds[0]]

        rainnc = ncfile_id.variables['RAINNC'][:, lon_inds[0], lat_inds[0]]

        prcp = rainc + rainnc

        ncfile_id.close()

        diff = get_two_element_average(prcp)

        lat_extent = len(lat_inds[0])
        lon_extent = len(lon_inds[0])

        for lat_ind in range(lat_extent):
            for lon_id in range(lon_extent):

                lat = float(lats[lat_ind])
                lon = float(lons[lon_ind])

                station_prefix = 'wrf0_{}_{}'.format(lat, lon)

                # if station_id is None:
                #     add_station(pool=pool, name=station_prefix, latitude=lat, longitude=lon,
                #             description="WRF point", station_type=StationEnum.WRF)

                for i in range(len(diff)):
                    if float(diff[i, y, x]) < 0:
                        print(float(diff[i, y, x]))

# get_wrf0_d03_stations_precipitation("/home/shadhini/Documents/CUrW/NetCDF/wrf0/results_wrf0_2019-05-01_18_00_0000_wrf_wrfout_d03_2019-05-01_18_00_00_rf")


def get_two_element_average(prcp, return_diff=True):
    avg_prcp = (prcp[1:] + prcp[:-1]) * 0.5
    if return_diff:
        return avg_prcp - np.insert(avg_prcp[:-1], 0, [0], axis=0)
    else:
        return avg_prcp


def datetime_utc_to_lk(timestamp_utc, shift_mins=0):
    return timestamp_utc + timedelta(hours=5, minutes=30 + shift_mins)


def view_netcdf_data(rainc_net_cdf_file_path, rainnc_net_cdf_file_path):
    """

        :param pool: database connection pool
        :param rainc_net_cdf_file_path:
        :param rainnc_net_cdf_file_path:
        :param source_id:
        :param variable_id:
        :param unit_id:
        :param tms_meta:
        :return:

        rainc_unit_info:  mm
        lat_unit_info:  degree_north
        time_unit_info:  minutes since 2019-04-02T18:00:00
        """

    if not os.path.exists(rainc_net_cdf_file_path):
        logger.warning('no rainc netcdf')
        print('no rainc netcdf')
    elif not os.path.exists(rainnc_net_cdf_file_path):
        logger.warning('no rainnc netcdf')
        print('no rainnc netcdf')
    else:

        """
        RAINC netcdf data extraction
        """
        nc_fid = Dataset(rainc_net_cdf_file_path, mode='r')

        time_unit_info = nc_fid.variables['XTIME'].units

        time_unit_info_list = time_unit_info.split(' ')

        lats = nc_fid.variables['XLAT'][0, :, 0]
        lons = nc_fid.variables['XLONG'][0, 0, :]

        lon_min = lons[0].item()
        lat_min = lats[0].item()
        lon_max = lons[-1].item()
        lat_max = lats[-1].item()
        print('[lon_min, lat_min, lon_max, lat_max] :', [lon_min, lat_min, lon_max, lat_max])

        lat_inds = np.where((lats >= lat_min) & (lats <= lat_max))
        lon_inds = np.where((lons >= lon_min) & (lons <= lon_max))

        rainc = nc_fid.variables['RAINC'][:, lat_inds[0], lon_inds[0]]

        """
        RAINNC netcdf data extraction
        """
        nnc_fid = Dataset(rainnc_net_cdf_file_path, mode='r')

        rainnc = nnc_fid.variables['RAINNC'][:, lat_inds[0], lon_inds[0]]

        # times = list(set(nc_fid.variables['XTIME'][:]))  # set is used to remove duplicates
        times = nc_fid.variables['XTIME'][:]
        print(   sorted(set(times))[-2])

        # ts_start_date = datetime.strptime(time_unit_info_list[2], '%Y-%m-%dT%H:%M:%S')
        # ts_end_date = datetime.strptime(time_unit_info_list[2], '%Y-%m-%dT%H:%M:%S') + timedelta(
        #         minutes=float(max(times)))
        #
        # start_date = datetime_utc_to_lk(ts_start_date, shift_mins=0).strftime('%Y-%m-%d %H:%M:%S')
        # end_date = datetime_utc_to_lk(ts_end_date, shift_mins=0).strftime('%Y-%m-%d %H:%M:%S')

        prcp = rainc + rainnc

        nc_fid.close()
        nnc_fid.close()

        diff = get_two_element_average(prcp)
        print('diff : ', len(diff))

        width = len(lons)
        height = len(lats)


        for y in range(1):#height
            for x in range(1):

                lat = float(lats[y])
                lon = float(lons[x])

                # print("prcp : ", len(prcp))
                # for i in range(len(prcp)):
                #     ts_time = datetime.strptime(time_unit_info_list[2], '%Y-%m-%dT%H:%M:%S') + timedelta(
                #             minutes=times[i].item())
                #     t = datetime_utc_to_lk(ts_time, shift_mins=0)
                #     print(t.strftime('%Y-%m-%d %H:%M:%S'), prcp[i,y,x])
                # station_prefix = '{}_{}'.format(lat, lon)

                data_list = []
                # generate timeseries for each station
                for i in range(len(diff)):
                    ts_time = datetime.strptime(time_unit_info_list[2], '%Y-%m-%dT%H:%M:%S') + timedelta(
                            minutes=times[i].item())
                    t = datetime_utc_to_lk(ts_time, shift_mins=0)
                    data_list.append([t.strftime('%Y-%m-%d %H:%M:%S'), float(diff[i, y, x])])
                # print(data_list)

print(view_netcdf_data("/home/shadhini/Documents/CUrW/NetCDF/RAINC_2019-03-17_A.nc","/home/shadhini/Documents/CUrW/NetCDF/RAINNC_2019-03-17_A.nc"))