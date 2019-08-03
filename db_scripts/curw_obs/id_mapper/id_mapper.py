import traceback

from mysqladapter1 import check_runname
from utils import map_curw_id

#get the curw_ids from the curw database where run_name only equals to A&T Labs/CUrW IoT/Leecom
result = check_runname('%A&T Labs', '%CUrW IoT', '%Leecom')
print(result)
for id in result:
    try:
        map_curw_id(id[0])
    except Exception as e:
        traceback.print_exc()