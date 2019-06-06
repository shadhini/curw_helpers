from db_adapter.base import get_Pool
from db_adapter.curw_sim.grids import add_flo2d_grid_mappings, get_flo2d_to_obs_grid_mappings, \
    get_flo2d_to_wrf_grid_mappings, GridInterpolationEnum
from db_adapter.constants import CURW_SIM_HOST, CURW_SIM_PORT, CURW_SIM_USERNAME, CURW_SIM_PASSWORD, CURW_SIM_DATABASE

print(" Add flo2d grid mappings")

pool = get_Pool(host=CURW_SIM_HOST, port=CURW_SIM_PORT, user=CURW_SIM_USERNAME, password=CURW_SIM_PASSWORD, db=CURW_SIM_DATABASE)

grid_interpolation_method = GridInterpolationEnum.getAbbreviation(GridInterpolationEnum.MDPA)

print(" Add flo2d 250 grid mappings")
add_flo2d_grid_mappings(pool=pool, flo2d_model='flo2d_250', grid_interpolation=grid_interpolation_method)
print("{} flo2d 250 grids added".format(len(get_flo2d_to_wrf_grid_mappings(pool=pool, flo2d_model='flo2d_250', grid_interpolation=grid_interpolation_method).keys())))
print("{} flo2d 250 grids added".format(len(get_flo2d_to_obs_grid_mappings(pool=pool, flo2d_model='flo2d_250', grid_interpolation=grid_interpolation_method).keys())))


print(" Add flo2d 150 grid mappings")
add_flo2d_grid_mappings(pool=pool, flo2d_model='flo2d_150', grid_interpolation=grid_interpolation_method)
print("{} flo2d 150 grids added".format(len(get_flo2d_to_wrf_grid_mappings(pool=pool, flo2d_model='flo2d_150', grid_interpolation=grid_interpolation_method).keys())))
print("{} flo2d 150 grids added".format(len(get_flo2d_to_obs_grid_mappings(pool=pool, flo2d_model='flo2d_150', grid_interpolation=grid_interpolation_method).keys())))

print(" Add flo2d 30 grid mappings")
add_flo2d_grid_mappings(pool=pool, flo2d_model='flo2d_30', grid_interpolation=grid_interpolation_method)
print("{} flo2d 30 grids added".format(len(get_flo2d_to_wrf_grid_mappings(pool=pool, flo2d_model='flo2d_30', grid_interpolation=grid_interpolation_method).keys())))
print("{} flo2d 30 grids added".format(len(get_flo2d_to_obs_grid_mappings(pool=pool, flo2d_model='flo2d_30', grid_interpolation=grid_interpolation_method).keys())))

pool.destroy()

