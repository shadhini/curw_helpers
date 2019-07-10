import traceback
from datetime import datetime, timedelta
import json

from db_adapter.curw_sim.constants import HecHMS
from db_adapter.curw_sim.grids import GridInterpolationEnum
from db_adapter.curw_sim.timeseries import MethodEnum
from db_adapter.curw_sim.rainfall import update_rainfall_fcsts


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


if __name__=="__main__":
    try:
        config = json.loads(open('config.json').read())

        # source details
        model_list = read_attribute_from_config_file('model_list', config)

        method = MethodEnum.getAbbreviation(MethodEnum.MME)
        grid_interpolation = GridInterpolationEnum.getAbbreviation(GridInterpolationEnum.MDPA)

        print("{} : ####### Insert fcst rainfall for Obs Stations grids #######".format(datetime.now()))
        update_rainfall_fcsts(target_model=HecHMS, method=method, grid_interpolation=grid_interpolation,
                model_list=model_list, timestep=5)

    except Exception as e:
        traceback.print_exc()
    finally:
        print("{} : ####### fcst rainfall insertion process finished for {} #######".format(datetime.now(), HecHMS))



