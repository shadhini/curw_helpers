import os
import numpy as np
from netCDF4 import Dataset

from logger import logger
from stations import KELANI_BASIN_EXTENT


def get_two_element_average(prcp, return_diff=True):
    avg_prcp = (prcp[1:] + prcp[:-1]) * 0.5
    if return_diff:
        return avg_prcp - np.insert(avg_prcp[:-1], 0, [0], axis=0)
    else:
        return avg_prcp


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

get_wrf0_d03_stations_precipitation("/home/shadhini/Documents/CUrW/NetCDF/wrf0/results_wrf0_2019-05-01_18_00_0000_wrf_wrfout_d03_2019-05-01_18_00_00_rf")
