import logging
import logging.config
import yaml


with open('/home/shadhini/dev/repos/shadhini/curw_helpers/logger_config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

