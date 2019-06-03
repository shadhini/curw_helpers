from db_adapter.base import get_Pool
from db_adapter.curw_sim.grids import get_flo2d_grid_mappings, add_flo2d_grid_mappings
from db_adapter.constants import CURW_SIM_HOST, CURW_SIM_PORT, CURW_SIM_USERNAME, CURW_SIM_PASSWORD, CURW_SIM_DATABASE

print(" Add flo2d grid mappings")

pool = get_Pool(host=CURW_SIM_HOST, port=CURW_SIM_PORT, user=CURW_SIM_USERNAME, password=CURW_SIM_PASSWORD, db=CURW_SIM_DATABASE)

print(" Add flo2d 250 grid mappings")
add_flo2d_grid_mappings(pool=pool, flo2d_model='flo2d_250')
print("{} flo2d 250 grids added".format(len(get_flo2d_grid_mappings(pool=pool, flo2d_model='flo2d_250').keys())))

print(" Add flo2d 150 grid mappings")
add_flo2d_grid_mappings(pool=pool, flo2d_model='flo2d_150')
print("{} flo2d 150 grids added".format(len(get_flo2d_grid_mappings(pool=pool, flo2d_model='flo2d_150').keys())))

print(" Add flo2d 30 grid mappings")
add_flo2d_grid_mappings(pool=pool, flo2d_model='flo2d_30')
print("{} flo2d 30 grids added".format(len(get_flo2d_grid_mappings(pool=pool, flo2d_model='flo2d_30').keys())))

pool.destroy()

